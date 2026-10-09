#!/usr/bin/env python3
"""Guerreiro's Grill — tour pelas unidades. Lê timeline.json e renderiza.

    python3 render.py --preview     # prévia em baixa resolução (rápida)
    python3 render.py               # final 1080x1920, 30 fps, H.264 + AAC

Pipeline por clipe: o FFmpeg decodifica só o trecho usado (corrige rotação,
escala e corta para 9:16, aplica a correção do clipe e o look da marca); o Python
monta a rampa de velocidade quadro a quadro (fontes de 60 fps dão câmera lenta
real), aplica as transições de câmera (whip com desfoque direcional e zoom com
desfoque radial), os títulos e o encerramento, e manda os quadros para o
encoder. O som é só ambiente dos próprios clipes + whooshes sutis (sem música).
Gera também <saida>.cortes.json com os tempos de cada corte, para sincronizar a
música depois.
"""
import json, math, os, subprocess, sys
import numpy as np, cv2
import scipy.io.wavfile as wavfile, scipy.signal as sg
from PIL import Image, ImageDraw, ImageFont

FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
ROOT = os.path.dirname(os.path.abspath(__file__))
SR = 48000


def P(p):
    return p if os.path.isabs(p) else os.path.join(ROOT, p)


def ease_in(t):  return t * t
def ease_out(t): return 1 - (1 - t) ** 3


# ---------------------------------------------------------------- decodificação
def src_fps(path):
    r = subprocess.run([FF, "-i", P(path)], capture_output=True, text=True).stderr
    import re
    m = re.search(r"(\d+(?:\.\d+)?) fps", r)
    return float(m.group(1)) if m else 30.0


def clip_frames(clip, W, H, fps, look):
    """Lista de quadros RGB (uint8, HxWx3) já na velocidade da timeline."""
    segs = clip["segments"]
    t0 = min(min(s[0], s[1]) for s in segs); t1 = max(max(s[0], s[1]) for s in segs)
    sf = src_fps(clip["file"])
    rf = clip.get("reframe", {"zoom": 1.0, "x": 0.5, "y": 0.5})
    z = rf.get("zoom", 1.0)
    zw, zh = int(math.ceil(W * z / 2) * 2), int(math.ceil(H * z / 2) * 2)
    chain = ([clip["pre"]] if clip.get("pre") else []) + [
             f"scale={zw}:{zh}:force_original_aspect_ratio=increase:flags=lanczos",
             f"crop={W}:{H}:(iw-{W})*{rf.get('x', 0.5)}:(ih-{H})*{rf.get('y', 0.5)}"]
    if clip.get("hflip"): chain.append("hflip")
    if clip.get("fix"): chain.append(clip["fix"])
    if look and not clip.get("no_look"): chain.append(look)
    chain.append("format=rgb24")
    cmd = [FF, "-v", "error", "-ss", f"{t0:.3f}", "-t", f"{t1 - t0 + 0.1:.3f}", "-i", P(clip["file"]),
           "-vf", ",".join(chain), "-fps_mode", "passthrough", "-f", "rawvideo", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    src = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    out = []
    def grab(t, v):
        k = (t - t0) * sf
        n = int(round(abs(v) * sf / fps)) if abs(v) > 1.3 else 1   # rapido: mistura os quadros que a camera percorreu
        if n <= 1:
            return src[min(len(src) - 1, max(0, int(round(k))))]
        ks = [min(len(src) - 1, max(0, int(round(k + (1 if v > 0 else -1) * i)))) for i in range(n)]
        return np.mean([src[i].astype(np.float32) for i in ks], axis=0).astype(np.uint8)
    for seg in segs:
        if len(seg) == 4:                        # rampa: velocidade vai de v0 a v1 (desacelera)
            a, b, v0, v1 = seg; d = 1 if b >= a else -1; t = a
            while (t - b) * d < 0:
                p = abs(t - a) / max(1e-6, abs(b - a))
                v = v1 + (v0 - v1) * (1 - p) ** 2
                out.append(grab(t, d * v)); t += d * v / fps
            continue
        a, b, sp = seg                           # b < a = reverse (a imagem volta)
        d = 1 if b >= a else -1
        n = max(1, int(round(abs(b - a) / sp * fps)))
        for i in range(n):
            t = a + d * i * sp / fps
            out.append(grab(t, d * sp))
    return out


# ---------------------------------------------------------------- transições
def shift_blur(img, d0, d1, ang, samples):
    """Desloca a imagem de d0 a d1 px na direção ang (graus) com rastro (motion blur)."""
    H, W = img.shape[:2]
    c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    acc = np.zeros(img.shape, np.float32)
    for i in range(samples):
        d = d0 + (d1 - d0) * (i + 0.5) / samples
        M = np.float32([[1, 0, c * d], [0, 1, s * d]])
        acc += cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return (acc / samples).astype(np.uint8)


def zoom_blur(img, s0, s1, samples, cx=0.5, cy=0.5):
    H, W = img.shape[:2]
    acc = np.zeros(img.shape, np.float32)
    for i in range(samples):
        s = s0 + (s1 - s0) * (i + 0.5) / samples
        M = cv2.getRotationMatrix2D((W * cx, H * cy), 0, s)
        acc += cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return (acc / samples).astype(np.uint8)


def match_zoom_blur(img, a0, a1, cx, cy, samples):
    """Mergulho da camera ate o ponto (cx, cy): amplia e traz o ponto para o centro."""
    H, W = img.shape[:2]
    acc = np.zeros(img.shape, np.float32)
    for i in range(samples):
        z, p = a0 + (a1 - a0) * (i + 0.5) / samples      # (zoom, quanto o ponto ja veio pro centro)
        px, py = W * cx + (W / 2 - W * cx) * p, H * cy + (H / 2 - H * cy) * p
        M = np.float32([[z, 0, px - z * W * cx], [0, z, py - z * H * cy]])
        acc += cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return (acc / samples).astype(np.uint8)


def apply_out(frames, tr, W, samples):
    """Fim do clipe A: a câmera acelera na direção do movimento até o corte."""
    if not tr or tr["type"] in ("cut", "ramp_in"): return
    k = tr.get("frames", 5); k = min(k, len(frames))
    for j in range(k):
        p0, p1 = j / k, (j + 1) / k
        i = len(frames) - k + j
        if tr["type"] == "whip":
            D = tr.get("amount", 0.5) * W
            frames[i] = shift_blur(frames[i], D * ease_in(p0), D * ease_in(p1), tr["dir"], samples)
        elif tr["type"] == "zoom":
            Z = tr.get("amount", 0.5)
            frames[i] = zoom_blur(frames[i], 1 + Z * ease_in(p0), 1 + Z * ease_in(p1), samples, tr.get('cx', 0.5), tr.get('cy', 0.5))
        elif tr["type"] == "match_zoom":
            Z = tr.get("amount", 2.5)
            st = lambda p: np.array([1 + (Z - 1) * ease_in(p), ease_in(p)])
            frames[i] = match_zoom_blur(frames[i], st(p0), st(p1), tr["cx"], tr["cy"], samples)


def apply_in(frames, tr, W, samples):
    """Começo do clipe B: o mesmo movimento chega do lado oposto e desacelera."""
    if not tr or tr["type"] == "cut": return
    if tr["type"] == "ramp_in":
        lift = tr.get("lift", 0.16)
        for j in range(min(tr.get("in_frames", 5), len(frames))):
            g = lift * (1 - j / tr.get("in_frames", 5)) ** 2
            frames[j] = np.clip(frames[j] * (1 - g) + 255 * g, 0, 255).astype(np.uint8)
        return
    k = tr.get("in_frames", tr.get("frames", 5)); k = min(k, len(frames))
    for j in range(k):
        p0, p1 = 1 - j / k, 1 - (j + 1) / k
        if tr["type"] == "whip":
            D = tr.get("amount", 0.5) * W
            frames[j] = shift_blur(frames[j], -D * ease_in(p0), -D * ease_in(p1), tr["dir"], samples)
        elif tr["type"] == "zoom":
            Z = tr.get("amount", 0.5)
            frames[j] = zoom_blur(frames[j], 1 + Z * ease_in(p0), 1 + Z * ease_in(p1), samples, tr.get('in_cx', 0.5), tr.get('in_cy', 0.5))
        elif tr["type"] == "match_zoom":
            Z = tr.get("in_amount", 1.2)
            frames[j] = zoom_blur(frames[j], 1 + (Z - 1) * ease_in(p0), 1 + (Z - 1) * ease_in(p1), samples)



# ---------------------------------------------------------------- efeito fachada
_LOGO = {}
def load_logo(path, depth):
    """Logo RGBA com espessura (efeito placa 3D). O telefone e coberto (sem numero no video)."""
    key = (path, depth)
    if key in _LOGO: return _LOGO[key]
    im = np.array(Image.open(P(path)).convert("RGBA")).astype(np.float32)
    h, w = im.shape[:2]
    # telefone fica na faixa de baixo, dentro do fundo preto do brasao
    y0, y1 = int(h * 0.835), int(h * 0.935); x0, x1 = int(w * 0.22), int(w * 0.80)
    im[y0:y1, x0:x1, :3] = im[y0 - 6:y0 - 4, x0:x1, :3].mean((0, 1))
    pad = depth + 4
    out = np.zeros((h + pad, w + pad, 4), np.float32)
    a = im[..., 3:4] / 255
    for d in range(depth, 0, -1):          # lateral da placa, mais escura para tras
        sh = 0.22 + 0.25 * (1 - d / depth)
        sl = out[d:d + h, d:d + w]
        col = np.concatenate([im[..., :3] * 0 + np.array([38, 30, 26]) * (sh / 0.47), im[..., 3:4]], -1)
        sl[:] = sl * (1 - a) + col * a
    sl = out[:h, :w]; sl[:] = sl * (1 - a) + im * a
    _LOGO[key] = out
    return out


def track_affines(frames, land, ymin, ymax):
    """Movimento da fachada (so a faixa ymin..ymax, sem a arvore verde) quadro a quadro.
    Devolve, para cada quadro, a matriz que leva coordenadas do quadro 'land' para ele."""
    sm = [cv2.cvtColor(cv2.resize(f, (f.shape[1] // 4, f.shape[0] // 4), interpolation=cv2.INTER_AREA), cv2.COLOR_RGB2GRAY)
          for f in frames]
    h, w = sm[0].shape
    def step(i, j):
        mask = np.zeros_like(sm[i]); mask[int(h * ymin):int(h * ymax)] = 255
        hsv = cv2.cvtColor(cv2.resize(frames[i], (w, h), interpolation=cv2.INTER_AREA), cv2.COLOR_RGB2HSV)
        mask[(hsv[..., 0] > 22) & (hsv[..., 0] < 60) & (hsv[..., 1] > 70)] = 0
        p0 = cv2.goodFeaturesToTrack(sm[i], 300, 0.01, 5, mask=mask)
        if p0 is None: return np.float32([[1, 0, 0], [0, 1, 0]])
        p1, st, _ = cv2.calcOpticalFlowPyrLK(sm[i], sm[j], p0, None)
        g = st.ravel() == 1
        M, _ = cv2.estimateAffinePartial2D(p0[g], p1[g], method=cv2.RANSAC, ransacReprojThreshold=1.5)
        if M is None: M = np.float32([[1, 0, 0], [0, 1, 0]])
        M = M.astype(np.float32); M[:, 2] *= 4
        return M
    def mul(A, B):   # A depois de B
        A3 = np.vstack([A, [0, 0, 1]]); B3 = np.vstack([B, [0, 0, 1]]); return (A3 @ B3)[:2]
    T = [None] * len(frames); T[land] = np.float32([[1, 0, 0], [0, 1, 0]])
    for j in range(land + 1, len(frames)): T[j] = mul(step(j - 1, j), T[j - 1])
    for j in range(land - 1, -1, -1): T[j] = mul(step(j + 1, j), T[j + 1])
    return T


def apply_logo(frames, cfg):
    """Logo chega voando (gira, encolhe, com rastro), encaixa na fachada com um
    pequeno quique e fica preso a ela seguindo a camera. Folhas da arvore passam na frente."""
    H, W = frames[0].shape[:2]
    land, F = cfg.get("land", 12), cfg.get("fly_frames", 10)
    logo = load_logo(cfg["file"], max(2, int(cfg.get("depth", 10) * W / 1080)))
    lh, lw = logo.shape[:2]
    target_h = cfg.get("h", 0.14) * H
    base_s = target_h / lh
    T = track_affines(frames, land, *cfg.get("track_y", [0.1, 0.45]))
    ax, ay = cfg.get("cx", 0.5) * W, cfg.get("cy", 0.2) * H
    def place(j, extra_s, extra_rot, off):
        Tj = T[j]
        px, py = Tj @ np.float32([ax, ay, 1])
        ts = math.hypot(Tj[0, 0], Tj[1, 0]); tr = math.degrees(math.atan2(Tj[1, 0], Tj[0, 0]))
        s = base_s * ts * extra_s
        M = cv2.getRotationMatrix2D((lw / 2, lh / 2), -(tr + extra_rot), s)
        M[0, 2] += px + off[0] - lw / 2; M[1, 2] += py + off[1] - lh / 2
        return cv2.warpAffine(logo, M, (W, H), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
    for j in range(len(frames)):
        q = (j - (land - F)) / F
        if q < 0: continue
        layers = []
        subs = 4 if q < 1 else 1
        for k in range(subs):
            qq = min(1.0, q - (subs - 1 - k) / (F * subs)) if q < 1 else 1.0
            e = ease_out(max(0.0, qq))
            if q < 1:
                es, rot = 1 + cfg.get("fly_scale", 1.6) * (1 - e), cfg.get("fly_rot", 12) * (1 - e)
                off = (cfg.get("fly_dx", 0.0) * W * (1 - e), cfg.get("fly_dy", -0.45) * H * (1 - e))
            else:
                b = j - land                  # quique ao encaixar
                es = 1 + 0.07 * math.exp(-b / 2.2) * math.cos(b * 1.3) if b < 10 else 1.0
                rot, off = 0, (0, 0)
            layers.append(place(j, es, rot, off))
        L = sum(layers) / len(layers)
        f = frames[j].astype(np.float32)
        a = L[..., 3:4] / 255
        # sombra da placa na fachada (so depois de encaixar)
        if q >= 1:
            sh = cv2.GaussianBlur(a[..., 0], (0, 0), W / 160)
            sh = np.roll(np.roll(sh, int(W / 90), 1), int(W / 70), 0)[..., None] * 0.45
            f *= (1 - sh)
        if cfg.get("occlude_green", True):
            hsv = cv2.cvtColor(frames[j], cv2.COLOR_RGB2HSV)
            leaf = ((hsv[..., 0] > 22) & (hsv[..., 0] < 60) & (hsv[..., 1] > 70) & (hsv[..., 2] > 60)).astype(np.float32)
            leaf = cv2.GaussianBlur(leaf, (0, 0), 1.5)[..., None]
            a = a * (1 - leaf)
        f = f * (1 - a) + L[..., :3] * a
        if 0 <= j - land < 10:                     # brilho de letreiro acendendo
            gl = cv2.GaussianBlur(a[..., 0], (0, 0), W / 70)[..., None] * (1 - (j - land) / 10) * 0.8
            f = f + (255 - f) * gl
        frames[j] = np.clip(f, 0, 255).astype(np.uint8)


# ---------------------------------------------------------------- rotulos 3D (ref. 3)
def track_h(frames, at, rects):
    """Homografias que levam o quadro 'at' para cada quadro, rastreando so as areas
    'rects' ([x0,y0,x1,y1] normalizados: superficies paradas, fora da grelha que gira)."""
    sc = 4
    sm = [cv2.cvtColor(cv2.resize(f, (f.shape[1] // sc, f.shape[0] // sc), interpolation=cv2.INTER_AREA),
                       cv2.COLOR_RGB2GRAY) for f in frames]
    h, w = sm[0].shape
    mask = np.zeros((h, w), np.uint8)
    for x0, y0, x1, y1 in rects: mask[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)] = 255
    S = np.diag([sc, sc, 1.0]); Si = np.diag([1 / sc, 1 / sc, 1.0])
    def step(i, j):
        p0 = cv2.goodFeaturesToTrack(sm[i], 400, 0.008, 4, mask=mask)
        if p0 is None or len(p0) < 8: return np.eye(3)
        p1, st, _ = cv2.calcOpticalFlowPyrLK(sm[i], sm[j], p0, None)
        g = st.ravel() == 1
        if g.sum() < 8: return np.eye(3)
        Hm, _ = cv2.findHomography(p0[g], p1[g], cv2.RANSAC, 1.5)
        if Hm is None: return np.eye(3)
        return S @ Hm @ Si
    Hs = [None] * len(frames); Hs[at] = np.eye(3)
    for j in range(at + 1, len(frames)): Hs[j] = step(j - 1, j) @ Hs[j - 1]
    for j in range(at - 1, -1, -1): Hs[j] = step(j + 1, j) @ Hs[j + 1]
    return Hs


def label_letters(text, font, tracking, color, glow):
    """Cada letra como camada separada (para entrar uma a uma). Devolve imagem cheia + caixas."""
    sp = font.size * tracking
    ws = [font.getlength(ch) for ch in text]
    W_ = int(sum(ws) + sp * (len(text) - 1)) + 2 * glow + 8
    asc, desc = font.getmetrics(); H_ = asc + desc + 2 * glow + 8
    out, x = [], glow + 4
    from PIL import ImageFilter
    for ch, cw in zip(text, ws):
        im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((x, glow + 4), ch, font=font, fill=tuple(color) + (255,))
        a = np.array(im).astype(np.float32)
        g = np.array(im.filter(ImageFilter.GaussianBlur(glow))).astype(np.float32)   # brilho de letreiro
        d = np.array(im.filter(ImageFilter.GaussianBlur(max(1, glow // 2)))).astype(np.float32)  # sombra
        d = np.roll(d, max(1, glow // 4), axis=0)
        al = a[..., 3:4] / 255
        ga = g[..., 3:4] / 255 * 0.28; da = d[..., 3:4] / 255 * 0.75
        rgb = np.zeros_like(a[..., :3]); aa = np.zeros_like(al)
        for col, alpha in ((0.0, da), (255.0, ga)):            # sombra, depois brilho
            rgb = rgb * (1 - alpha) + col * alpha; aa = aa + alpha * (1 - aa)
        rgb = rgb * (1 - al) + a[..., :3] * al; aa = aa + al * (1 - aa)
        comb = np.concatenate([np.where(aa > 0, rgb * 1.0, 0), aa * 255], -1)
        out.append((comb, x, cw)); x += cw + sp
    return out, W_, H_


def apply_labels(frames, labels, scale):
    """Rotulos presos ao cenario (perspectiva acompanhando a camera), letras entrando uma a uma."""
    H, W = frames[0].shape[:2]
    for L in labels:
        font = ImageFont.truetype(P(L.get("font", "assets/fonts/Oswald[wght].ttf")), max(8, int(L.get("size", 60) * scale)))
        try: font.set_variation_by_axes([L.get("weight", 600)])
        except Exception: pass
        letters, lw, lh = label_letters(L["text"], font, L.get("tracking", 0.06), L.get("color", [255, 255, 255]),
                                        max(2, int(10 * scale)))
        at = min(len(frames) - 1, L.get("at", 0))
        Hs = track_h(frames, at, L.get("track", [[0, 0, 1, 1]])) if L.get("track") else [np.eye(3)] * len(frames)
        # colocacao no quadro 'at': centro, rotacao e inclinacao (perspectiva) da superficie
        cx, cy = L["cx"] * W, L["cy"] * H
        ang = math.radians(L.get("rot", 0)); sk = L.get("skew", 0.0)
        A = np.array([[math.cos(ang), -math.sin(ang), 0], [math.sin(ang), math.cos(ang), 0], [0, 0, 1]])
        Pp = np.array([[1, 0, 0], [0, 1, 0], [sk / lw, 0, 1]])        # um lado mais perto que o outro
        C = np.array([[1, 0, -lw / 2], [0, 1, -lh / 2], [0, 0, 1]])
        Tm = np.array([[1, 0, cx], [0, 1, cy], [0, 0, 1]])
        base = Tm @ A @ Pp @ C
        st, du, stag = L.get("start", 0), L.get("dur", 40), L.get("stagger", 1.5)
        for j in range(len(frames)):
            k = j - st
            if k < 0 or k >= du: continue
            lay = np.zeros((lh, lw, 4), np.float32)
            out_a = 1 - ease_out(max(0, (k - (du - 6)) / 6))
            for n, (img, x, cw) in enumerate(letters):
                p = ease_out(min(1, max(0, (k - n * stag) / 5)))
                if p <= 0: continue
                dx = int((1 - p) * lh * L.get("slide", 0.0))
                sl = np.roll(img, dx, axis=1) if dx else img
                lay = lay + sl * np.array([1, 1, 1, p * out_a], np.float32) * (1 - lay[..., 3:4] / 255)
            M = Hs[j] @ base
            wl = cv2.warpPerspective(lay, M, (W, H), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
            a = wl[..., 3:4] / 255
            frames[j] = np.clip(frames[j] * (1 - a) + wl[..., :3] * a, 0, 255).astype(np.uint8)


def apply_pop(frames, cfg, scale):
    """Texto grande que salta letra por letra sobre o produto (como o '2200W' da ref. 3) e segue o movimento."""
    H, W = frames[0].shape[:2]
    font = ImageFont.truetype(P(cfg.get("font", "assets/fonts/Anton-Regular.ttf")), int(cfg.get("size", 200) * scale))
    try: font.set_variation_by_axes([cfg.get("weight", 800)])
    except Exception: pass
    letters, lw, lh = label_letters(cfg["text"], font, cfg.get("tracking", 0.03), [255, 255, 255], max(3, int(16 * scale)))
    at = cfg.get("start", 0)
    Hs = (track_h(frames, min(at, len(frames) - 1), cfg.get("track", [[0.1, 0.1, 0.9, 0.9]]))
          if cfg.get("follow", 0.3) > 0 else [np.eye(3)] * len(frames))
    cx, cy = cfg.get("cx", 0.5) * W, cfg.get("cy", 0.3) * H
    du, stag = cfg.get("dur", 30), cfg.get("stagger", 2)
    for j in range(len(frames)):
        k = j - at
        if k < 0 or k >= du: continue
        lay = np.zeros((lh, lw, 4), np.float32)
        out_a = 1 - ease_out(max(0, (k - (du - 5)) / 5))
        for n, (img, x, cw) in enumerate(letters):
            q = (k - n * stag) / 6
            if q <= 0: continue
            sc_ = 1 + 0.35 * math.exp(-q * 3) * math.cos(q * 5) if q < 2 else 1.0   # salta e assenta
            cxl, cyl = x + cw / 2, lh / 2
            M = cv2.getRotationMatrix2D((cxl, cyl), 0, sc_)
            sl = cv2.warpAffine(img, M, (lw, lh), borderValue=(0, 0, 0, 0))
            sl[..., 3] *= min(1, q * 2) * out_a
            lay = lay + sl * (1 - lay[..., 3:4] / 255)
        pc = Hs[j] @ np.array([cx, cy, 1.0]); pc = pc[:2] / pc[2]
        fo = cfg.get("follow", 0.3)
        px, py = cx + (pc[0] - cx) * fo, cy + (pc[1] - cy) * fo
        M3 = np.array([[1, 0, px - lw / 2], [0, 1, py - lh / 2], [0, 0, 1]])
        wl = cv2.warpPerspective(lay, M3, (W, H), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
        a = wl[..., 3:4] / 255
        frames[j] = np.clip(frames[j] * (1 - a) + wl[..., :3] * a, 0, 255).astype(np.uint8)


# ---------------------------------------------------------------- texto v8 (ref. de tipografia)
SAFE = {"x0": 70, "x1": 160, "y0": 230, "y1": 420}     # margens do Reels/TikTok em 1080x1920

def _font(path, size, weight):
    f = ImageFont.truetype(P(path), max(8, int(size)))
    try: f.set_variation_by_axes([weight])
    except Exception: pass
    return f

def build_lockup(lines, scale, max_w):
    """Bloco de texto: linhas empilhadas (pequena em italico branco + grande em laranja-fogo).
    Cada linha encolhe sozinha se passar de max_w (nunca corta palavra)."""
    from PIL import ImageFilter
    rows = []
    for L in lines:
        size = L.get("size", 80) * scale
        path = L.get("font") or ("assets/fonts/Montserrat-Italic.ttf" if L.get("italic", True) else "assets/fonts/Montserrat.ttf")
        while True:
            f = _font(path, size, L.get("weight", 800))
            sp = f.size * L.get("tracking", 0.0)
            w = sum(f.getlength(ch) for ch in L["text"]) + sp * (len(L["text"]) - 1)
            if w <= max_w or size < 10: break
            size *= max_w / w * 0.98
        asc, desc = f.getmetrics()
        rows.append((L, f, sp, int(w), asc + desc))
    pad = int(40 * scale)
    Wl = max(r[3] for r in rows) + 2 * pad
    gap = [int(L.get("gap", -0.12) * h) for (L, f, sp, w, h) in rows]
    Hl = sum(r[4] for r in rows) + sum(gap[1:]) + 2 * pad
    out = []
    y = pad
    for i, (L, f, sp, w, h) in enumerate(rows):
        if i: y += gap[i]
        im = Image.new("L", (Wl, Hl), 0)
        al = L.get("align", "center")
        x = pad + ((Wl - 2 * pad - w) // 2 if al == "center" else 0 if al == "left" else (Wl - 2 * pad - w))
        d = ImageDraw.Draw(im)
        for ch in L["text"]:
            d.text((x, y), ch, font=f, fill=255); x += f.getlength(ch) + sp
        a = np.array(im, np.float32) / 255
        if L.get("color", "white") == "chrome":         # metal escovado do '2200W' da ref.
            yy = (np.linspace(0, 1, Hl)[:, None] * Hl - y) / max(1, h)
            v = np.interp(np.clip(yy, 0, 1), [0, 0.35, 0.55, 0.62, 1], [255, 236, 168, 205, 246])
            rgb = np.broadcast_to(np.stack([v, v, v * 1.01], -1), (Hl, Wl, 3)).clip(0, 255)
        elif L.get("color", "white") == "orange":         # laranja chapado da ref. (leve luz em cima)
            yy = np.linspace(0, 1, Hl)[:, None]
            band = np.clip((yy * Hl - y) / max(1, h), 0, 1)
            top, bot = np.array([255, 128, 34.]), np.array([246, 92, 8.])
            rgb = np.broadcast_to(top[None, None] * (1 - band[..., None]) + bot[None, None] * band[..., None], (Hl, Wl, 3))
        elif L.get("color", "white") == "fire":           # degrade de brasa: amarelo-alaranjado em cima, laranja queimado embaixo
            yy = np.linspace(0, 1, Hl)[:, None]
            band = np.clip((yy * Hl - y) / max(1, h), 0, 1)
            top, bot = np.array([255, 196, 70.]), np.array([238, 92, 16.])
            rgb = top[None, None] * (1 - band[..., None]) + bot[None, None] * band[..., None]
            rgb = np.broadcast_to(rgb, (Hl, Wl, 3))
        else:
            rgb = np.broadcast_to(np.array([255, 250, 242.]), (Hl, Wl, 3))
        img = np.concatenate([rgb * 1.0, a[..., None] * 255], -1).astype(np.float32)
        if L.get("glow"):                                # halo laranja em volta da palavra grande (ref.)
            g = cv2.GaussianBlur(a, (0, 0), L.get("glow_r", 16) * scale) * L["glow"]
            gl = np.concatenate([np.broadcast_to(np.array(L.get("glow_color", [255, 110, 20]), np.float64), (Hl, Wl, 3)), g[..., None] * 255], -1).astype(np.float32)
            out.append((gl, L.get("delay", i * 3)))
        out.append((img, L.get("delay", i * 3)))
        y += h
    # sombra unica do bloco (contraste em qualquer fundo)
    A = np.maximum.reduce([o[0][..., 3] for o in out])
    edge_k = float(lines[0].get("_edge", 0.45)) if lines else 0.45
    soft_k = float(lines[0].get("_soft", 0.55)) if lines else 0.55
    r = max(1, int(round(2 * scale)))
    edge = cv2.dilate(A, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1)))
    edge = cv2.GaussianBlur(edge, (0, 0), 0.8 * scale + 0.3) * edge_k        # contorno escuro bem leve
    soft = np.roll(cv2.GaussianBlur(A, (0, 0), 12 * scale), int(7 * scale), 0) * soft_k   # sombra larga
    sh = np.maximum(edge, soft)
    return out, sh, Wl, Hl

def _over(lay, im):
    """composicao 'over' correta (cor ponderada pelo alfa de cada camada)"""
    a = im[..., 3:4] / 255; b = lay[..., 3:4] / 255
    ao = a + b * (1 - a)
    rgb = (im[..., :3] * a + lay[..., :3] * b * (1 - a)) / np.maximum(ao, 1e-6)
    return np.concatenate([rgb, ao * 255], -1)


TEXT_MODE = "fixo"

def cam_offsets(frames, factor=0.6, limit=90):
    """Deslocamento suavizado da camera (para o texto 'andar' junto com a cena sem tremer)."""
    H, W = frames[0].shape[:2]
    Hs = track_h(frames, 0, [[0.05, 0.05, 0.95, 0.95]])
    pts = []
    for Hm in Hs:
        p = Hm @ np.array([W / 2, H / 2, 1.0]); pts.append(p[:2] / p[2])
    pts = np.array(pts) - np.array([W / 2, H / 2])
    k = np.exp(-0.5 * (np.arange(-9, 10) / 3.5) ** 2); k /= k.sum()
    pad = np.pad(pts, ((9, 9), (0, 0)), mode="edge")
    sm = np.stack([np.convolve(pad[:, i], k, "valid") for i in range(2)], 1)
    lim = limit * W / 1080
    return np.clip(sm * factor, -lim, lim)

def apply_texts(frames, texts, scale):
    H, W = frames[0].shape[:2]
    for T_ in texts:
        max_w = (1080 - SAFE["x0"] - SAFE["x1"]) * scale * T_.get("max_w", 1.0)
        rows, sh, Wl, Hl = build_lockup(T_["lines"], scale, max_w)
        st, du = T_.get("start", 4), T_.get("dur", 45)
        cx, cy = T_.get("cx", 0.5) * W, T_.get("cy", 0.5) * H
        tilt, rot = T_.get("tilt", 0.0), math.radians(T_.get("rot", 0))
        A = np.array([[math.cos(rot), -math.sin(rot), 0], [math.sin(rot), math.cos(rot), 0], [0, 0, 1]])
        Pp = np.array([[1, 0, 0], [0, 1, 0], [T_.get("skew", 0.0) / Wl, tilt / Hl, 1]])   # chao (tilt) / parede (skew)
        C = np.array([[1, 0, -Wl / 2], [0, 1, -Hl / 2], [0, 0, 1]])
        M0 = A @ Pp @ C
        # caixa do bloco ja em perspectiva; se passar da largura segura, encolhe o bloco todo
        cs = np.array([[0, 0, 1], [Wl, 0, 1], [0, Hl, 1], [Wl, Hl, 1]], np.float64).T
        q = M0 @ cs; q = q[:2] / q[2]
        avail = W - (SAFE["x0"] + SAFE["x1"]) * scale
        k_ = min(1.0, avail / (q[0].max() - q[0].min()))
        if k_ < 1:
            M0 = np.diag([k_, k_, 1.0]) @ M0
            q = M0 @ cs; q = q[:2] / q[2]
        bx0, bx1, by0, by1 = q[0].min(), q[0].max(), q[1].min(), q[1].max()
        fo = 0.0 if TEXT_MODE != "fixo" else T_.get("follow", 0.0)
        Hs = (track_h(frames, min(st, len(frames) - 1), T_.get("track", [[0.05, 0.05, 0.95, 0.95]]))
              if fo > 0 else None)
        CO = cam_offsets(frames) if TEXT_MODE == "movimento" else None
        for j in range(len(frames)):
            k = j - st
            if k < 0 or k >= du: continue
            px, py = cx, cy
            if Hs is not None:
                pc = Hs[j] @ np.array([cx, cy, 1.0]); pc = pc[:2] / pc[2]
                px, py = cx + (pc[0] - cx) * fo, cy + (pc[1] - cy) * fo
            if CO is not None:
                o0 = CO[min(st, len(CO) - 1)]
                px += CO[j][0] - o0[0]; py += CO[j][1] - o0[1]
            # trava na area segura
            px = min(max(px, SAFE["x0"] * scale - bx0), W - SAFE["x1"] * scale - bx1)
            py = min(max(py, SAFE["y0"] * scale - by0), H - SAFE["y1"] * scale - by1)
            lay = np.zeros((Hl, Wl, 4), np.float32)
            out_k = k - (du - 6)
            for img, dl in rows:                       # entrada: cada linha sobe 3 quadros depois da outra
                if T_.get("reveal") == "sweep":       # letreiro acendendo letra a letra (ref. T TECH)
                    p = min(1, max(0, (k - dl) / T_.get("sweep_frames", 12)))
                    if p <= 0: continue
                    xs = np.arange(Wl, dtype=np.float32)
                    m = np.clip((p * (Wl + 120 * scale) - xs) / (60 * scale), 0, 1)
                    im = img.copy(); im[..., 3] *= m[None, :]
                    lay = _over(lay, im)
                    continue
                p = ease_out(min(1, max(0, (k - dl) / 7)))
                if p <= 0: continue
                sc_ = 1.10 - 0.10 * p
                if T_.get("punch"):                    # entra grande e "bate" no lugar (estalo)
                    q = min(1, max(0, (k - dl) / 9))
                    sc_ = 1 + 0.45 * (1 - q) ** 3 - 0.06 * math.sin(math.pi * q) * (q > 0.5)
                    p = min(1, (k - dl + 1) / 3)
                M = cv2.getRotationMatrix2D((Wl / 2, Hl / 2), 0, sc_); M[1, 2] += (1 - p) * 18 * scale
                im = cv2.warpAffine(img, M, (Wl, Hl), borderValue=(0, 0, 0, 0))
                if p < 1: im = cv2.GaussianBlur(im, (0, 0), 0.1 + 4 * (1 - p))
                im[..., 3] *= p
                lay = _over(lay, im)
            alpha_all = 1.0
            if out_k > 0:                              # saida: clarao rapido e some
                e = out_k / 6; alpha_all = 1 - ease_out(e)
                if T_.get("reveal") != "sweep":
                    lay[..., :3] = lay[..., :3] + (255 - lay[..., :3]) * min(1, e * 2.5) * 0.8
            shl = sh * (lay[..., 3].max() / 255 if lay[..., 3].max() > 0 else 0) * alpha_all
            T3 = np.array([[1, 0, px], [0, 1, py], [0, 0, 1]]) @ M0
            wl = cv2.warpPerspective(lay, T3, (W, H), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
            ws = cv2.warpPerspective(shl, T3, (W, H), flags=cv2.INTER_LINEAR, borderValue=0)
            f = frames[j].astype(np.float32) * (1 - ws[..., None] / 255 * 0.0 - ws[..., None] / 255)
            a = wl[..., 3:4] / 255 * alpha_all
            frames[j] = np.clip(f * (1 - a) + wl[..., :3] * a, 0, 255).astype(np.uint8)

# ---------------------------------------------------------------- tipografia
class Type:
    def __init__(self, cfg, scale):
        self.c, self.s = cfg, scale
        self.fname = ImageFont.truetype(P(cfg["font_name"]), int(cfg["name_size"] * scale))
        try: self.fname.set_variation_by_axes([cfg.get("name_weight", 800)])
        except Exception: pass
        self.flabel = ImageFont.truetype(P(cfg["font_label"]), int(cfg["label_size"] * scale))
        try: self.flabel.set_variation_by_axes([cfg.get("label_weight", 500)])
        except Exception: pass

    def hot_line(self, text, font, tracking):
        """Nome em degrade dourado->brasa com brilho quente e sombra (titulos/frases v12)."""
        from PIL import ImageFilter
        base = self.line(text, font, tracking, (255, 255, 255))
        a = np.array(base).astype(np.float32)
        A = a[..., 3] / 255
        rows = np.where(A.max(1) > 0.5)[0]
        y0, y1 = (rows.min(), rows.max()) if len(rows) else (0, a.shape[0])
        t = np.clip((np.arange(a.shape[0]) - y0) / max(1, y1 - y0), 0, 1)[:, None]
        top, mid, bot = np.array([255, 236, 170.]), np.array([255, 190, 64.]), np.array([240, 118, 22.])
        col = np.where(t[..., None] < 0.5, top + (mid - top) * (t[..., None] / 0.5), mid + (bot - mid) * ((t[..., None] - 0.5) / 0.5))
        white = (a[..., :3].mean(-1) > 200)[..., None]
        a[..., :3] = np.where(white, np.broadcast_to(col, a[..., :3].shape), a[..., :3])
        img = Image.fromarray(a.clip(0, 255).astype(np.uint8))
        glow = np.zeros_like(a); glow[..., 0], glow[..., 1], glow[..., 2] = 255, 140, 30
        glow[..., 3] = cv2.GaussianBlur((A * white[..., 0]).astype(np.float32), (0, 0), 14 * self.s) * 150
        return Image.alpha_composite(Image.fromarray(glow.astype(np.uint8)), img)

    def line(self, text, font, tracking, color):
        """Texto com espaçamento entre letras, em RGBA, com sombra suave."""
        sp = font.size * tracking
        widths = [font.getlength(ch) for ch in text]
        w = int(sum(widths) + sp * (len(text) - 1)) + 8
        asc, desc = font.getmetrics(); h = asc + desc + 8
        im = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0)); sh = im.copy()
        x = 20
        for ch, cw in zip(text, widths):
            ImageDraw.Draw(sh).text((x + 2, 24), ch, font=font, fill=(0, 0, 0, 150))
            ImageDraw.Draw(im).text((x, 20), ch, font=font, fill=tuple(color) + (255,))
            x += cw + sp
        from PIL import ImageFilter
        return Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(max(1, int(6 * self.s)))), im)

    def block(self, lines, align):
        c = self.c
        L = self.line(lines[0], self.flabel, c["label_tracking"], c["color"])
        N = (self.hot_line(lines[1], self.fname, c["name_tracking"]) if c.get("hot") else
             self.line(lines[1], self.fname, c["name_tracking"], c["color"]))
        return L, N

    def draw(self, canvas, lines, f, n, align="left", y=None):
        """f = quadro atual dentro do título, n = duração em quadros.
        Entrada: régua dourada cresce, linhas sobem de trás de uma máscara.
        Saída: sobem um pouco e somem."""
        c, s = self.c, self.s
        L, N = self.block(lines, align)
        W = canvas.width
        maxw = W - int(c["x"] * s) - int(c.get("right_margin", 150) * s) + 40
        if N.width > maxw:          # nome comprido (ex.: JARDIM ACLIMACAO): reduz so o nome para caber
            f2 = ImageFont.truetype(P(c["font_name"]), int(c["name_size"] * s * maxw / N.width))
            try: f2.set_variation_by_axes([c.get("name_weight", 800)])
            except Exception: pass
            N = (self.hot_line(lines[1], f2, c["name_tracking"]) if c.get("hot") else
                 self.line(lines[1], f2, c["name_tracking"], c["color"]))
        x0 = int(c["x"] * s); y0 = int((y if y is not None else c["y"]) * s)
        ex = max(0.0, (f - (n - 7)) / 7)                      # saída
        alpha = 1 - ease_out(ex); lift = int(-30 * s * ease_out(ex))
        # régua
        rw = int(110 * s * ease_out(min(1, f / 9)))
        if rw > 0:
            rx = x0 if align == "left" else (W - int(110 * s)) // 2
            ImageDraw.Draw(canvas).rectangle([rx, y0 + lift, rx + rw, y0 + lift + max(2, int(4 * s))],
                                             fill=tuple(c["accent"]) + (int(255 * alpha),))
        ly = y0 + int(16 * s); ny = ly + L.height - int(30 * s)
        for img, yy, delay in ((L, ly, 2), (N, ny, 5)):
            p = ease_out(min(1, max(0, (f - delay) / 9)))
            if p <= 0: continue
            off = int((1 - p) * img.height * 0.9)
            crop = img.crop((0, 0, img.width, img.height - off))   # máscara: sobe "de trás" da linha
            if alpha < 1:
                a = np.array(crop); a[..., 3] = (a[..., 3] * alpha).astype(np.uint8); crop = Image.fromarray(a)
            xx = x0 - 20 if align == "left" else (W - img.width) // 2
            canvas.alpha_composite(crop, (xx, yy + off + lift))


def composite(frame, layer):
    a = np.asarray(layer, dtype=np.float32)
    al = a[..., 3:4] / 255.0
    return (frame * (1 - al) + a[..., :3] * al).astype(np.uint8)


def band(H, y0, y1, strength):
    """Sombra suave so na faixa do texto (bordas em degrade de 160 px)."""
    y = np.arange(H, dtype=np.float32); e = 160 * H / 1920
    g = np.clip((y - (y0 - e)) / e, 0, 1) * np.clip(((y1 + e) - y) / e, 0, 1)
    g = g * g * (3 - 2 * g)
    return (g * strength)[:, None, None]


def gradient(H, W, strength, top=False):
    g = np.linspace(0, 1, H, dtype=np.float32)
    g = np.clip((g - 0.45) / 0.55, 0, 1) if not top else np.clip((0.4 - g) / 0.4, 0, 1)
    return (g ** 1.4 * strength)[:, None, None]


# ---------------------------------------------------------------- som
def whoosh(dur=0.42, peak=0.30):
    n = int(dur * SR); t = np.arange(n) / SR
    noise = np.random.default_rng(7).standard_normal(n)
    lo = sg.lfilter(*sg.butter(2, 900 / (SR / 2)), noise)
    hi = sg.lfilter(*sg.butter(2, [900 / (SR / 2), 5000 / (SR / 2)], "band"), noise)
    mix = np.clip(t / peak, 0, 1)                     # abre o brilho até o pico
    x = lo * (1 - mix) + hi * mix * 0.8
    env = np.where(t < peak, (t / peak) ** 2.2, np.exp(-(t - peak) * 22))
    x = x * env; x /= np.abs(x).max() + 1e-9
    return np.stack([x, x * 0.92], 1), int(peak * SR)


def hit(dur=0.7):
    n = int(dur * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * (52 - 18 * t) * t) * np.exp(-t * 6) * (1 - np.exp(-t * 300))
    return np.stack([x, x], 1) / np.abs(x).max()


def ambience(clip, out_start, nfr, fps, total_n, db):
    """Som do proprio clipe. Com "audio_speed": true o som segue as rampas de
    velocidade (atempo por trecho, sem mudar o tom) e fica sincronizado com a imagem."""
    if db is None or db <= -59: return None
    dur = nfr / fps
    if clip.get("audio_speed"):
        parts, labels = [], []
        for i, (a, b, sp) in enumerate(clip["segments"]):
            parts.append(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,atempo={sp:.4f}[a{i}]")
            labels.append(f"[a{i}]")
        fc = ";".join(parts) + ";" + "".join(labels) + f"concat=n={len(labels)}:v=0:a=1,highpass=f=60[o]"
        cmd = [FF, "-v", "error", "-i", P(clip["file"]), "-filter_complex", fc, "-map", "[o]",
               "-ac", "2", "-ar", str(SR), "-f", "s16le", "-"]
    else:
        a = clip["segments"][0][0]
        cmd = [FF, "-v", "error", "-ss", f"{a:.3f}", "-t", f"{dur:.3f}", "-i", P(clip["file"]),
               "-vn", "-ac", "2", "-ar", str(SR), "-af", "highpass=f=80", "-f", "s16le", "-"]
    r = subprocess.run(cmd, capture_output=True).stdout
    x = np.frombuffer(r, np.int16).astype(np.float32).reshape(-1, 2) / 32768
    x = x[:int(dur * SR)].copy()
    if len(x) == 0: return None
    k = min(int(0.03 * SR), len(x) // 2)
    x[:k] *= np.linspace(0, 1, k)[:, None]; x[-k:] *= np.linspace(1, 0, k)[:, None]
    rms = np.sqrt(np.mean(x ** 2)) + 1e-9
    return x / rms * 10 ** (db / 20)


# ---------------------------------------------------------------- render
def main():
    preview = "--preview" in sys.argv
    so_entrada = "--entrada" in sys.argv          # so a abertura + o 1o clipe, em qualidade final
    global TEXT_MODE
    TEXT_MODE = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--texto=")), "fixo")   # fixo | movimento | sem
    tl = json.load(open(os.path.join(ROOT, "timeline.json")))
    o = tl["output"]; fps = o["fps"]
    sc = o.get("preview_scale", 0.5) if preview else 1.0
    W, H = int(o["w"] * sc) // 2 * 2, int(o["h"] * sc) // 2 * 2
    samples = 8 if preview else 16
    out_path = P(o["preview_file"] if preview else o["file"])
    if TEXT_MODE != "fixo":
        out_path = out_path.replace(".mp4", "-TEXTO-EM-MOVIMENTO.mp4" if TEXT_MODE == "movimento" else "-SEM-TEXTO.mp4")
    if so_entrada: out_path = P(o.get("entrada_file", "../../entrega/teste-ENTRADA-GTA.mp4"))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    look = tl.get("look", {}).get("filters", "")
    T = Type(tl["typography"], sc)

    # sequência de clipes com o título/legenda de cada unidade
    seq = []
    if tl.get("opening", {}).get("enabled") and tl["opening"].get("clip"):
        seq.append({"clip": tl["opening"]["clip"], "loc": None})
    for loc in tl["locations"]:
        for i, c in enumerate(loc["clips"]):
            seq.append({"clip": c, "loc": loc, "title": i == loc.get("title_clip", 0)})
    if not seq: sys.exit("timeline sem clipes")
    end = tl.get("ending")
    if so_entrada:
        seq = seq[:2]; end = None
        seq[-1]["clip"] = dict(seq[-1]["clip"], transition_out={"type": "cut"})
    if end and end.get("tail"):
        seq.append({"clip": end["tail"], "loc": None, "ending": True})
    if end and end.get("final_clip"):            # vinheta da marca, intacta, fechando o video
        seq.append({"clip": end["final_clip"], "loc": None, "vinheta": True})

    enc = [FF, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps),
           "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p",
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]
    enc += (["-preset", "veryfast", "-crf", "24"] if preview else
            ["-preset", "slow", "-crf", "17", "-maxrate", "14M", "-bufsize", "24M", "-profile:v", "high", "-level", "4.1"])
    tmpv = out_path + ".video.mp4"
    pe = subprocess.Popen(enc + [tmpv], stdin=subprocess.PIPE)

    cuts, trans_times, amb_list = [], [], []
    frame_no = 0
    prev_out = None
    pending = []
    for idx, item in enumerate(seq):
        c = item["clip"]
        hr = c.get("hires", 1)
        fr = clip_frames(c, W * hr, H * hr, fps, look)
        apply_in(fr, prev_out, W * hr, samples)
        if c.get("logo"): apply_logo(fr, c["logo"])
        if TEXT_MODE != "sem":
            if c.get("labels"): apply_labels(fr, c["labels"], sc * hr)
            for pp in ([c["pop"]] if isinstance(c.get("pop"), dict) else c.get("pop", [])):
                apply_pop(fr, pp, sc * hr)
            if c.get("texts"): apply_texts(fr, c["texts"], sc * hr)
        apply_out(fr, c.get("transition_out"), W * hr, samples)
        if hr != 1: fr = [cv2.resize(f, (W, H), interpolation=cv2.INTER_AREA) for f in fr]
        start = frame_no + len(pending) - min((prev_out or {}).get("overlap", 0), len(pending))
        if prev_out and prev_out.get("type") != "cut":
            trans_times.append(start / fps)
        cuts.append({"t": round(start / fps, 3), "clip": os.path.basename(c["file"]),
                     "unidade": item["loc"]["name"] if item.get("loc") else ("vinheta" if item.get("vinheta") else "fim" if item.get("ending") else "abertura")})
        amb = ambience(c, start, len(fr), fps, None, c.get("ambience_db", -60))
        if amb is not None: amb_list.append((start, amb))

        loc = item.get("loc")
        tstart = tdur = None
        if loc and item.get("title"):
            tstart = int(loc.get("title_start", 0.15) * fps); tdur = int(loc.get("title_dur", 1.5) * fps)
        blk = c.get("block")                     # mesmo bloco de texto do titulo, para as frases (v11)
        if blk:
            tstart, tdur = int(blk.get("start", 0.3) * fps), int(blk.get("dur", 1.3) * fps)
            loc = dict(loc or {}, title=blk["lines"], title_y=blk.get("y"))
        if TEXT_MODE == "sem": tstart = None
        TCO = cam_offsets(fr) if (TEXT_MODE == "movimento" and tstart is not None) else None
        out_frames = []
        for j, f in enumerate(fr):
            f = f.copy()
            if tstart is not None and tstart <= j < tstart + tdur:
                k = j - tstart
                g = min(1, k / 6, (tdur - k) / 6) * loc.get("title_shade", 0.42)
                ty = ((loc.get("title_y") if loc else None) or tl["typography"]["y"]) * sc
                f = (f * (1 - band(H, ty - 140 * sc, ty + 330 * sc, g))).astype(np.uint8)
                layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                T.draw(layer, loc["title"], k, tdur, y=loc.get("title_y"))
                if TCO is not None:
                    o0 = TCO[min(tstart, len(TCO) - 1)]
                    dx, dy = int(TCO[j][0] - o0[0]), int(TCO[j][1] - o0[1])
                    sh_ = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh_.alpha_composite(layer, (dx, dy)) if dx >= 0 and dy >= 0 else sh_.paste(layer, (dx, dy), layer)
                    layer = sh_
                f = composite(f, layer)
            if item.get("ending") and end.get("style") == "white":
                n = len(fr); fl = end.get("flash", 8)
                w_ = ease_in(min(1, max(0, (j - (n - fl)) / fl)))
                if w_ > 0:
                    b = cv2.GaussianBlur(f, (0, 0), 1 + w_ * W / 60)
                    f = (b * (1 - w_) + np.array(end.get("bg", [245, 240, 232])) * w_).astype(np.uint8)
            elif item.get("ending") and end.get("style") != "none":
                n = len(fr); p = ease_out(min(1, j / 10))
                f = (f * (1 - end.get("darken", 0.5) * p)).astype(np.uint8)
                layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                draw_end(T, layer, end["lines"], j, n + 30)
                f = composite(f, layer)
            out_frames.append(f)
        if item.get("ending") and end.get("style") == "white":
            out_frames += white_card(T, end, W, H, fps)
        # emenda com sobreposicao (dissolve dentro do borrao) entre o fim do clipe anterior e este
        ov = (prev_out or {}).get("overlap", 0)
        if ov and pending:
            for j in range(min(ov, len(pending), len(out_frames))):
                w_ = (j + 1) / (ov + 1)
                out_frames[j] = (pending[j] * (1 - w_) + out_frames[j] * w_).astype(np.uint8)
            pending = []
        for f in pending: pe.stdin.write(f.tobytes()); frame_no += 1
        my_ov = (c.get("transition_out") or {}).get("overlap", 0)
        keep = out_frames[len(out_frames) - my_ov:] if my_ov else []
        for f in (out_frames[:len(out_frames) - my_ov] if my_ov else out_frames):
            pe.stdin.write(f.tobytes()); frame_no += 1
        pending = keep
        prev_out = c.get("transition_out")
        print(f"  {os.path.basename(c['file'])}: {len(fr)} quadros", flush=True)
    for f in pending: pe.stdin.write(f.tobytes()); frame_no += 1
    pe.stdin.close(); pe.wait()
    total = frame_no

    # som: ambiente dos clipes + whoosh em cada transição de câmera + toque grave no fim
    N = int(total / fps * SR) + SR
    A = np.zeros((N, 2), np.float32)
    for f0, x in amb_list:
        i = int(f0 / fps * SR); A[i:i + len(x)] += x[:max(0, N - i)]
    snd = tl.get("sound", {})
    wz, pk = whoosh()
    for t in trans_times:
        i = int(t * SR) - pk
        if i >= 0: A[i:i + len(wz)] += wz * 10 ** (snd.get("whoosh_db", -22) / 20)
    if end:
        i = int(cuts[-1]["t"] * SR); h = hit()
        A[i:i + len(h)] += h * 10 ** (snd.get("end_hit_db", -20) / 20)
    A = A[:int(total / fps * SR)]
    fo = int(0.5 * SR); A[-fo:] *= np.linspace(1, 0, fo)[:, None]
    pk_ = np.abs(A).max()
    if pk_ > 0.89: A *= 0.89 / pk_
    wav = out_path + ".wav"
    wavfile.write(wav, SR, (A * 32767).astype(np.int16))
    subprocess.run([FF, "-y", "-v", "error", "-i", tmpv, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-ar", str(SR), "-movflags", "+faststart", "-shortest", out_path],
                   check=True)
    os.remove(tmpv); os.remove(wav)
    json.dump({"duracao": round(total / fps, 3), "fps": fps, "cortes": cuts,
               "transicoes_de_camera": [round(t, 3) for t in trans_times]},
              open(out_path + ".cortes.json", "w"), ensure_ascii=False, indent=2)
    print(f"{out_path}  {total} quadros = {total / fps:.2f} s")


def white_card(T, end, W, H, fps):
    """Encerramento como o da ref. 3: fundo claro, o brasao entra e assenta, linha embaixo."""
    c, s = T.c, T.s
    n = int(end.get("card_dur", 1.6) * fps)
    bg = np.zeros((H, W, 3), np.uint8); bg[:] = end.get("bg", [245, 240, 232])
    logo = np.array(Image.open(P(end["logo"])).convert("RGBA")).astype(np.float32)
    lh, lw = logo.shape[:2]
    y0, y1 = int(lh * 0.835), int(lh * 0.935); x0, x1 = int(lw * 0.22), int(lw * 0.80)
    logo[y0:y1, x0:x1, :3] = logo[y0 - 6:y0 - 4, x0:x1, :3].mean((0, 1))
    base = end.get("logo_w", 0.62) * W / lw
    lab = T.line(end["lines"][1], T.flabel, c["label_tracking"], end.get("ink", [40, 30, 26]))
    out = []
    for j in range(n):
        q = j / 8
        sc_ = base * (1 + 0.12 * math.exp(-q * 2.2) * math.cos(q * 3.2)) if j < 24 else base
        al = min(1, j / 4)
        M = cv2.getRotationMatrix2D((lw / 2, lh / 2), 0, sc_)
        M[0, 2] += W / 2 - lw / 2; M[1, 2] += H * 0.44 - lh / 2
        L = cv2.warpAffine(logo, M, (W, H), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
        a = L[..., 3:4] / 255 * al
        sh = cv2.GaussianBlur(a[..., 0], (0, 0), W / 60)[..., None] * 0.25
        f = bg * (1 - sh)
        f = f * (1 - a) + L[..., :3] * a
        f = Image.fromarray(np.clip(f, 0, 255).astype(np.uint8)).convert("RGBA")
        p2 = ease_out(min(1, max(0, (j - 8) / 10)))
        if p2 > 0:
            lay = lab.copy(); A_ = np.array(lay); A_[..., 3] = (A_[..., 3] * p2).astype(np.uint8)
            f.alpha_composite(Image.fromarray(A_), ((W - lab.width) // 2, int(H * 0.44 + base * lh / 2 + 30 * s + (1 - p2) * 20 * s)))
        out.append(np.array(f.convert("RGB")))
    return out


def draw_end(T, layer, lines, j, n):
    """Encerramento centralizado: marca grande, régua dourada, '3 UNIDADES · CUIABÁ'."""
    c, s = T.c, T.s
    W, H = layer.size
    fend = ImageFont.truetype(P(c["font_name"]), int(c["name_size"] * 0.8 * s))
    N = T.line(lines[0], fend, 0.03, c["color"])
    L = T.line(lines[1], T.flabel, c["label_tracking"], c["color"])
    cy = int(H * 0.46)
    p1 = ease_out(min(1, max(0, (j - 2) / 10)))
    p2 = ease_out(min(1, max(0, (j - 8) / 10)))
    rw = int(150 * s * ease_out(min(1, max(0, (j - 5) / 10))))
    if p1 > 0:
        off = int((1 - p1) * N.height * 0.9)
        layer.alpha_composite(N.crop((0, 0, N.width, N.height - off)), ((W - N.width) // 2, cy - N.height + off))
    if rw > 0:
        ImageDraw.Draw(layer).rectangle([(W - rw) // 2, cy + int(8 * s), (W + rw) // 2, cy + int(8 * s) + max(2, int(4 * s))],
                                        fill=tuple(c["accent"]) + (255,))
    if p2 > 0:
        off = int((1 - p2) * L.height * 0.9)
        layer.alpha_composite(L.crop((0, off, L.width, L.height)), ((W - L.width) // 2, cy + int(24 * s)))


if __name__ == "__main__":
    main()
