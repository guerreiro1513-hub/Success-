#!/usr/bin/env python3
"""Aviso do Guerreiro's Grill no Auto Posto Florais (v2).
Fala reconstruída em 4K com os mesmos cortes do CapCut do cliente (IMG_1885 + NOVO_1885 são a mesma tomada),
whip pan seguindo o movimento da câmera até a churrasqueira (IMG_1878), legenda palavra por palavra e fecho.
Tudo em timeline.json.      python3 render.py [--preview]
"""
import json, math, os, re, subprocess, sys
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
from scipy.io import wavfile

FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
ROOT = os.path.dirname(os.path.abspath(__file__))
P = lambda p: os.path.join(ROOT, p)
SAFE = {"x0": 70, "x1": 160, "y0": 230, "y1": 420}
SR = 48000


def ease_out(t): t = min(1, max(0, t)); return 1 - (1 - t) ** 3
def ease_in(t): t = min(1, max(0, t)); return t * t * t
def ease_io(t): t = min(1, max(0, t)); return t * t * (3 - 2 * t)
def syl(w): return max(1, len(re.findall(r"[aeiouáéíóúâêôãõà]+", w.lower())))


# ---------------------------------------------------------------- tempo das palavras
def word_times(tl, env, hop):
    """Texto do cliente + trechos do detector de voz. Dentro de cada trecho as palavras são divididas por sílabas
    e cada fronteira é puxada para o vale de energia mais próximo (±90 ms), onde a palavra realmente troca."""
    words = []
    for seg in tl["speech"]:
        ws = seg["text"].split(); a, b = seg["t"]
        tot = sum(syl(w) for w in ws); acc = 0; bounds = [a]
        per = (b - a) / tot                                # duração média de uma sílaba neste trecho
        for k_, w in enumerate(ws[:-1]):
            acc += syl(w); est = a + per * acc
            win = min(0.09, 0.4 * per * min(syl(w), syl(ws[k_ + 1])))   # janela menor que meia palavra
            i0, i1 = max(int((est - win) / hop), 0), min(int((est + win) / hop), len(env) - 1)
            bnd = (i0 + int(np.argmin(env[i0:i1 + 1]))) * hop if i1 > i0 else est
            lo = bounds[-1] + 0.6 * per * syl(w)             # cada palavra dura pelo menos 60 % do previsto
            hi = b - 0.6 * per * sum(syl(x) for x in ws[k_ + 1:])
            bounds.append(min(max(bnd, lo), max(lo, hi)))
        bounds.append(b)
        for w, x, y in zip(ws, bounds[:-1], bounds[1:]):
            words.append({"w": w, "a": x, "b": max(y, x + 0.08)})
    return words


# ---------------------------------------------------------------- vídeo
def reader(c, W, H, fps, grade):
    vf = f"{grade},scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},fps={fps},format=rgb24"
    n = int(round((c["out"] - c["in"]) * fps))
    p = subprocess.Popen([FF, "-v", "error", "-ss", f"{c['in']:.3f}", "-i", P(c["src"]), "-frames:v", str(n),
                          "-vf", vf, "-an", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    last = None
    for _ in range(n):
        b = p.stdout.read(W * H * 3)
        if len(b) == W * H * 3: last = np.frombuffer(b, np.uint8).reshape(H, W, 3)
        yield last.astype(np.float32)
    p.wait()


def shift_blur(img, d0, d1, samples):
    """Desloca na horizontal de d0 a d1 px com rastro (motion blur do whip pan)."""
    H, W = img.shape[:2]; acc = np.zeros_like(img)
    for i in range(samples):
        d = d0 + (d1 - d0) * (i + 0.5) / samples
        acc += cv2.warpAffine(img, np.float32([[1, 0, d], [0, 1, 0]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    return acc / samples


def grab(c, j, W, H, fps, grade):
    t = c["in"] + j / fps
    vf = f"{grade},scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},format=rgb24"
    raw = subprocess.run([FF, "-v", "error", "-ss", f"{t:.3f}", "-i", P(c["src"]), "-frames:v", "1", "-vf", vf,
                          "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(H, W, 3)


def match_matrix(a, b):
    """Similaridade que leva o plano A (fim) até o enquadramento do plano B (início): A ampliado por M = B."""
    g1, g2 = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY), cv2.cvtColor(b, cv2.COLOR_RGB2GRAY)
    sift = cv2.SIFT_create(4000)
    k1, d1 = sift.detectAndCompute(g1, None); k2, d2 = sift.detectAndCompute(g2, None)
    good = [m for m, n in cv2.BFMatcher().knnMatch(d1, d2, k=2) if m.distance < 0.75 * n.distance]
    src = np.float32([k1[m.queryIdx].pt for m in good]); dst = np.float32([k2[m.trainIdx].pt for m in good])
    M, inl = cv2.estimateAffinePartial2D(src, dst, method=cv2.RANSAC, ransacReprojThreshold=4 * a.shape[1] / 540)
    return M, int(inl.sum())


def part_matrix(M, p, W, H):
    """Fração p da similaridade M (escala, giro e deslocamento interpolados)."""
    sc = math.hypot(M[0, 0], M[1, 0]); th = math.atan2(M[1, 0], M[0, 0])
    c = np.array([W / 2, H / 2]); c2 = M[:, :2] @ c + M[:, 2]      # para onde vai o centro
    s_ = 1 + (sc - 1) * p; th_ = th * p; cc = c + (c2 - c) * p
    R = np.array([[s_ * math.cos(th_), -s_ * math.sin(th_)], [s_ * math.sin(th_), s_ * math.cos(th_)]])
    return np.hstack([R, (cc - R @ c)[:, None]])


def zoom_m(z, W, H):
    return np.array([[z, 0, W / 2 * (1 - z)], [0, z, H / 2 * (1 - z)]])


def compose(A, B):                                   # A depois de B
    A3, B3 = np.vstack([A, [0, 0, 1]]), np.vstack([B, [0, 0, 1]])
    return (A3 @ B3)[:2]


def cover_zoom(M, W, H):
    """Menor zoom (no centro) que, aplicado depois de M, não deixa borda vazia."""
    z = 1.0
    while z < 1.6:
        T = np.vstack([compose(zoom_m(z, W, H), M), [0, 0, 1]]); Ti = np.linalg.inv(T)
        pts = Ti @ np.array([[0, W, 0, W], [0, 0, H, H], [1, 1, 1, 1]], float)
        if pts[0].min() >= 0 and pts[0].max() <= W and pts[1].min() >= 0 and pts[1].max() <= H: return z
        z += 0.005
    return z


def warp(img, M):
    H, W = img.shape[:2]
    return cv2.warpAffine(img, M.astype(np.float32), (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)


# ---------------------------------------------------------------- tipografia
def font(path, size):
    return ImageFont.truetype(P(path), max(8, int(size)))


_G = {}
def glyph_word(word, path, size, color, s):
    """Palavra como camada com contorno escuro arredondado e sombra difusa em duas camadas."""
    key = (word, path, size, tuple(color), s)
    if key in _G: return _G[key]
    f = font(path, size * s); a, d = f.getmetrics(); pad = int(30 * s)
    w = int(f.getlength(word)) + 2 * pad; h = a + d + 2 * pad
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).text((pad, pad), word, font=f, fill=255)
    A = np.array(m, np.float32) / 255
    r = max(2, int(round(size * s * 0.075)))                  # contorno ~7,5 % do corpo
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    stroke = cv2.GaussianBlur(cv2.dilate(A, k), (0, 0), 0.8 * s)
    shadow = np.maximum(np.roll(cv2.GaussianBlur(stroke, (0, 0), 3 * s), int(5 * s), 0) * 0.55,
                        np.roll(cv2.GaussianBlur(stroke, (0, 0), 16 * s), int(12 * s), 0) * 0.45)
    out = {"A": A, "stroke": stroke, "shadow": shadow, "w": w, "h": h, "pad": pad, "adv": f.getlength(word),
           "color": np.array(color, np.float32)}
    _G[key] = out
    return out


def put(f, gw, x, y, alpha, scale=1.0, color=None):
    A, st, sh = gw["A"], gw["stroke"], gw["shadow"]
    w, h = gw["w"], gw["h"]
    if abs(scale - 1) > 1e-3:
        w2, h2 = max(2, int(w * scale)), max(2, int(h * scale))
        A = cv2.resize(A, (w2, h2)); st = cv2.resize(st, (w2, h2)); sh = cv2.resize(sh, (w2, h2))
        x += (w - w2) / 2; y += (h - h2) / 2; w, h = w2, h2
    x, y = int(x), int(y)
    H, W = f.shape[:2]
    xa, ya, xb, yb = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if xb <= xa or yb <= ya: return
    sl = (slice(ya - y, yb - y), slice(xa - x, xb - x))
    reg = f[ya:yb, xa:xb]
    reg *= 1 - (sh[sl] * alpha)[..., None]
    sa = (st[sl] * alpha * 0.92)[..., None]
    reg[:] = reg * (1 - sa) + np.array([14, 10, 8.]) * sa
    aa = (A[sl] * alpha)[..., None]
    reg[:] = reg * (1 - aa) + (gw["color"] if color is None else color) * aa


def captions(f, t, tl, s, words, fps):
    """Páginas de 1-3 palavras. Cada palavra entra quando é falada (sobe 10 px e assenta); a palavra
    falada no momento fica dourada e um pouco maior. Páginas 'hot' são douradas fixas e maiores."""
    C = tl["captions"]; H, W = f.shape[:2]
    pages = C["pages"]
    for pi, pg in enumerate(pages):
        i0, i1 = pg["w"]
        a = words[i0]["a"] - 0.05
        b = words[i1]["b"] + pg.get("hold", 0.25)
        if pi + 1 < len(pages):                            # nunca sobrepõe a página seguinte
            b = min(b, words[pages[pi + 1]["w"][0]]["a"] - 0.05)
        if not (a <= t < b): continue
        size = C["size_hot"] if pg.get("hot") else C["size"]
        gws = [(i, glyph_word(words[i]["w"].upper().strip(",.!?"), C["font"], size,
                              C["gold"] if pg.get("hot") else C["white"], s)) for i in range(i0, i1 + 1)]
        space = 0.36 * size * s                           # espaço folgado: a palavra falada cresce 6-16 %
        total = sum(g["adv"] for _, g in gws) + space * (len(gws) - 1)
        k = min(1.0, (1080 - SAFE["x0"] - SAFE["x1"]) * s * 0.96 / total)   # nunca sai da área segura
        x = (SAFE["x0"] * s + W - SAFE["x1"] * s) / 2 - total * k / 2
        cy = C["cy"] * H
        out = ease_io(min(1, (b - t) / 0.08))
        for i, g in gws:
            q = (t - (words[i]["a"] - 0.03)) * fps
            if q >= 0:
                p = ease_out(q / 4)
                nxt = words[i + 1]["a"] - 0.03 if i + 1 < len(words) else 1e9
                speaking = words[i]["a"] - 0.03 <= t < min(words[i]["b"] + 0.04, nxt)   # só uma palavra por vez
                pop = 1.0 + (0.10 * (1 - ease_out(q / 5)) if q < 5 else 0)
                col = np.array(C["gold"], np.float32) if (speaking and not pg.get("hot")) else None
                sc = k * (1.06 if speaking else 1.0) * pop
                cxw = x + g["adv"] * k / 2                  # centro real da palavra (a escala parte dele)
                put(f, g, cxw - g["w"] / 2, cy - g["h"] / 2 + (1 - p) * 10 * s, p * out, sc, col)
            x += (g["adv"] + space) * k


def end_card(f, t, tl, s):
    E = tl["end_card"]
    if t < E["start"]: return
    H, W = f.shape[:2]; k = (t - E["start"]) * tl["fps"]
    g = E.get("shade", 0.5) * ease_out(k / 10)
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    f *= 1 - g * (0.55 + 0.45 * np.exp(-((yy - 0.36) / 0.24) ** 2))
    if not hasattr(end_card, "logo"):
        lg = Image.open(P(E["logo"])).convert("RGBA")
        lh = int(E["logo_h"] * H); lw = int(lg.width * lh / lg.height)
        end_card.logo = np.array(lg.resize((lw, lh), Image.LANCZOS), np.float32)
    L = end_card.logo; lh, lw = L.shape[:2]
    p = ease_out(k / 9)
    if p > 0:
        sc = 0.9 + 0.1 * p; w2, h2 = int(lw * sc), int(lh * sc)
        Lg = cv2.resize(L, (w2, h2), interpolation=cv2.INTER_AREA)
        x0, y0 = W // 2 - w2 // 2, int(E["logo_cy"] * H) - h2 // 2
        a = Lg[..., 3:4] / 255 * p
        sub = f[y0:y0 + h2, x0:x0 + w2]
        sub *= 1 - cv2.GaussianBlur(a[..., 0], (0, 0), 16 * s)[..., None] * 0.55
        sub[:] = sub * (1 - a) + Lg[..., :3] * a
    for i, L_ in enumerate(E["lines"]):
        q = ease_out((k - 7 - i * 4) / 7)
        if q <= 0: continue
        size = L_["size"]
        while True:
            g_ = glyph_word(L_["text"], L_["font"], size, L_["color"], s)
            if g_["adv"] <= (1080 - 2 * SAFE["x1"]) * s or size < 12: break
            size -= 4
        put(f, g_, W / 2 - g_["w"] / 2, L_["cy"] * H - g_["h"] / 2 + (1 - q) * 22 * s, q)


# ---------------------------------------------------------------- áudio
def pcm(src, a, b):
    raw = subprocess.run([FF, "-v", "error", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", P(src), "-vn", "-ac", "2",
                          "-ar", str(SR), "-f", "s16le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).reshape(-1, 2).astype(np.float32) / 32768


def whoosh(dur=0.45):
    n = int(dur * SR); t = np.arange(n) / SR
    x = np.random.default_rng(3).standard_normal(n)
    fc = 300 + 3500 * np.sin(np.pi * t / dur) ** 2
    al = 1 - np.exp(-2 * np.pi * fc / SR); y = np.zeros(n); lp = 0.0
    for i in range(n):                                   # passa-baixa varrendo (sopro do whip)
        lp += al[i] * (x[i] - lp); y[i] = lp
    y *= np.sin(np.pi * t / dur) ** 2
    y /= np.abs(y).max() + 1e-9
    return np.stack([y, y], 1).astype(np.float32)


def build_audio(tl, plan, total_s, out):
    n = int(total_s * SR); A = np.zeros((n, 2), np.float32)
    for c, start in plan:
        x = pcm(c["src"], c["in"], c["out"]) * c.get("vol", 1.0)
        i = int(start * SR); m = min(len(x), n - i)
        fd = int(0.012 * SR); x = x[:m].copy()
        x[:fd] *= np.linspace(0, 1, fd)[:, None]; x[-fd:] *= np.linspace(1, 0, fd)[:, None]
        A[i:i + m] += x
    tmp = out + ".v.wav"; wavfile.write(tmp, SR, (np.clip(A, -1, 1) * 32767).astype(np.int16))
    au = tl["audio"]
    wz = whoosh(); wi = int((tl["whip_at"] - 0.22) * SR)
    Wz = np.zeros((n, 2), np.float32); Wz[wi:wi + len(wz)] = wz[:max(0, n - wi)] * tl["whip"].get("whoosh", 0.30)
    wz_path = out + ".w.wav"; wavfile.write(wz_path, SR, (Wz * 32767).astype(np.int16))
    subprocess.run([FF, "-y", "-v", "error", "-i", tmp, "-stream_loop", "-1", "-i", P(au["music"]), "-i", wz_path,
                    "-filter_complex",
                    "[0:a]highpass=f=80,loudnorm=I=-14:TP=-2:LRA=9,asplit[v][sc];"
                    f"[1:a]aresample={SR},volume={au['music_db']}dB,afade=t=in:d=0.8[m0];"
                    "[m0][sc]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=350[m];"
                    f"[v][m][2:a]amix=inputs=3:duration=first:normalize=0,afade=t=out:st={total_s - 1.2}:d=1.2,"
                    "alimiter=limit=0.89[a]",
                    "-map", "[a]", "-t", f"{total_s:.3f}", "-c:a", "pcm_s16le", out], check=True)
    os.remove(tmp); os.remove(wz_path)


def main():
    preview = "--preview" in sys.argv
    tl = json.load(open(P("timeline.json")))
    fps = tl["fps"]; s = 0.5 if preview else 1.0
    W, H = int(1080 * s) // 2 * 2, int(1920 * s) // 2 * 2
    out = P(tl["output"]["preview" if preview else "file"])
    os.makedirs(P("work"), exist_ok=True)
    clips = tl["clips"]
    lens = [int(round((c["out"] - c["in"]) * fps)) for c in clips]
    ov = [c.get("overlap", 0) for c in clips]             # quadros sobrepostos com o clipe seguinte
    starts, acc = [], 0
    for L, o in zip(lens, ov): starts.append(acc); acc += L - o
    total = acc + ov[-1]; total_s = total / fps
    whip = next(i for i, c in enumerate(clips) if c.get("whip_out"))
    tl["whip_at"] = (starts[whip] + lens[whip] - ov[whip] / 2) / fps
    voice = np.concatenate([pcm(c["src"], c["in"], c["out"]).mean(1) for c in clips[:whip + 1]])
    hop = 0.01; hs = int(hop * SR)
    env = np.array([np.sqrt((voice[i:i + hs] ** 2).mean()) for i in range(0, len(voice) - hs, hs)])
    env = np.convolve(env, np.ones(3) / 3, "same")
    words = word_times(tl, env, hop)
    wav = P("work/audio.wav"); build_audio(tl, [(c, st / fps) for c, st in zip(clips, starts)], total_s, wav)
    enc = [FF, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
           "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p",
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]
    enc += (["-preset", "veryfast", "-crf", "24"] if preview else
            ["-preset", "slow", "-crf", "16", "-maxrate", "16M", "-bufsize", "24M", "-profile:v", "high", "-level", "4.2"])
    enc += ["-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", out]
    pe = subprocess.Popen(enc, stdin=subprocess.PIPE)
    D = tl["whip"]["amount"] * W; K = tl["whip"]["frames"]; smp = 8 if preview else 14
    MM = None; KP = tl["whip"].get("push_frames", 16); ZC = 1.0; KC = 1
    if tl["whip"].get("type") == "match":               # fim da fala alinhado ao início da churrasqueira
        a_ = grab(clips[whip], lens[whip] - 4, W, H, fps, tl["grade"])   # perto do fim (o último quadro fica além do -ss)
        b_ = grab(clips[whip + 1], 0, W, H, fps, tl["grade"])
        MM, ninl = match_matrix(a_, b_)
        ZC = cover_zoom(MM, W, H); KC = tl["whip"].get("settle_frames", 20)
        print(f"  alinhamento: {ninl} pontos, escala {math.hypot(MM[0, 0], MM[1, 0]):.3f}, zoom de cobertura {ZC:.3f}")
    n = 0; pend = []
    for ci, c in enumerate(clips):
        for j, f in enumerate(reader(c, W, H, fps, tl["grade"])):
            if MM is not None and c.get("whip_out") and j >= lens[ci] - KP:   # câmera avança até o enquadramento do próximo
                p_ = ease_io((j - (lens[ci] - KP) + 1) / KP)
                f = warp(f, compose(zoom_m(1 + (ZC - 1) * p_, W, H), part_matrix(MM, p_, W, H)))
            if MM is not None and ci and clips[ci - 1].get("whip_out") and j < KC and ZC > 1.001:
                f = warp(f, zoom_m(1 + (ZC - 1) * (1 - ease_io((j + 1) / KC)), W, H))   # o zoom extra se desfaz devagar
            elif MM is None and c.get("whip_out") and j >= lens[ci] - K:     # whip (modo antigo)
                p0, p1 = (j - (lens[ci] - K)) / K, (j - (lens[ci] - K) + 1) / K
                f = shift_blur(f, D * ease_in(p0), D * ease_in(p1), smp)
            if MM is None and ci and clips[ci - 1].get("whip_out") and j < K:
                p0, p1 = 1 - j / K, 1 - (j + 1) / K
                f = shift_blur(f, -D * ease_in(p0), -D * ease_in(p1), smp)
            if ci and j < ov[ci - 1] and pend:                  # mistura dentro do borrão
                w_ = ease_io((j + 1) / (ov[ci - 1] + 1)); f = pend.pop(0) * (1 - w_) + f * w_
            if j >= lens[ci] - ov[ci] and ci < len(clips) - 1:
                pend.append(f); continue
            t = n / fps
            captions(f, t, tl, s, words, fps)
            end_card(f, t, tl, s)
            pe.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes()); n += 1
    pe.stdin.close(); pe.wait()
    json.dump({"duracao": round(n / fps, 3), "whip_em": round(tl["whip_at"], 2),
               "palavras": [{"w": w["w"], "a": round(w["a"], 2), "b": round(w["b"], 2)} for w in words]},
              open(out + ".cortes.json", "w"), ensure_ascii=False, indent=2)
    print(f"{out}  {n} quadros = {n / fps:.2f} s")


if __name__ == "__main__":
    main()
