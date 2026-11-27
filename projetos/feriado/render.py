#!/usr/bin/env python3
"""Guerreiro's Grill — aviso de funcionamento no feriado (9:16, 30 fps).
Lê timeline.json: planos (vídeo ou foto) medidos em batidas da trilha, textos, fecho e música.

    python3 render.py            -> 1080x1920 final (+ versão leve para WhatsApp)
    python3 render.py --preview  -> 540x960 rápido
"""
import json, math, os, subprocess, sys
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
ROOT = os.path.dirname(os.path.abspath(__file__))
P = lambda p: os.path.join(ROOT, p)
SAFE = {"x0": 70, "x1": 160, "y0": 230, "y1": 420}      # interface do Reels/TikTok/Shorts em 1080x1920
FONTS = {"Anton": "assets/fonts/Anton-Regular.ttf", "Montserrat": "assets/fonts/Montserrat.ttf"}


def ease_out(t): t = min(1, max(0, t)); return 1 - (1 - t) ** 3
def ease_io(t): t = min(1, max(0, t)); return t * t * (3 - 2 * t)


# ---------------------------------------------------------------- planos
def video_frames(sh, n, W, H, fps, tl):
    g = tl["grade_hdr"] if sh.get("hdr") else tl["grade_video"]
    vf = (f"{g},scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},"
          f"fps={fps},format=rgb24")
    raw = subprocess.run([FF, "-v", "error", "-ss", f"{sh['in']:.3f}", "-i", P(sh["src"]), "-frames:v", str(n),
                          "-vf", vf, "-an", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    fr = list(np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3))
    while len(fr) < n: fr.append(fr[-1])          # segurança (não deve acontecer com os 'in' escolhidos)
    return [f.copy() for f in fr[:n]]


_IMG = {}
def photo_frames(sh, n, W, H):
    """Foto com movimento lento: pan horizontal (fotos deitadas) e zoom suave, sub-pixel (sem tremer)."""
    key = sh["src"]
    if key not in _IMG:
        im = cv2.cvtColor(cv2.imread(P(sh["src"])), cv2.COLOR_BGR2RGB).astype(np.float32)
        # cor: levemente mais contraste e calor, sem mudar a comida
        im = np.clip((im - 128) * 1.05 + 128, 0, 255)
        im[..., 0] *= 1.015; im[..., 2] *= 0.985
        _IMG[key] = np.clip(im, 0, 255)
    im = _IMG[key]
    ih, iw = im.shape[:2]
    base = max(W / iw, H / ih)                    # cobre o quadro 9:16
    out = []
    x0, x1 = sh.get("pan", [0.5, 0.5]); z0, z1 = sh.get("z", [1.0, 1.0]); cy = sh.get("cy", 0.5)
    for j in range(n):
        t = ease_io(j / max(1, n - 1))
        s = base * (z0 + (z1 - z0) * t)
        vw, vh = W / s, H / s                     # janela na foto (em px da foto)
        px = (iw - vw) * (x0 + (x1 - x0) * t)
        py = (ih - vh) * cy
        M = np.float32([[s, 0, -px * s], [0, s, -py * s]])
        out.append(cv2.warpAffine(im, M, (W, H), flags=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC,
                                  borderMode=cv2.BORDER_REFLECT).astype(np.uint8))
    return out


# ---------------------------------------------------------------- tipografia
def font(name, size, weight=None):
    f = ImageFont.truetype(P(FONTS[name]), max(8, int(size)))
    if weight:
        try: f.set_variation_by_axes([weight])
        except Exception: pass
    return f


def line_layer(L, s, max_w):
    size = L["size"] * s
    tr = L.get("tracking", 0.0)
    while True:
        f = font(L["font"], size, L.get("weight"))
        sp = f.size * tr
        w = sum(f.getlength(c) for c in L["text"]) + sp * (len(L["text"]) - 1)
        if w <= max_w or size < 10: break
        size *= max_w / w * 0.98
    a, d = f.getmetrics()
    pad = int(30 * s)
    Wl, Hl = int(w) + 2 * pad, a + d + 2 * pad
    m = Image.new("L", (Wl, Hl), 0); dr = ImageDraw.Draw(m); x = pad
    for c in L["text"]:
        dr.text((x, pad), c, font=f, fill=255); x += f.getlength(c) + sp
    A = np.array(m, np.float32) / 255
    if L.get("color") == "fire":                  # brasa: dourado em cima, laranja queimado embaixo
        yy = np.clip((np.arange(Hl)[:, None] - pad - a * 0.15) / (a * 0.95), 0, 1)[..., None]
        rgb = np.array([255, 205, 80.]) * (1 - yy) + np.array([236, 88, 16.]) * yy
        rgb = np.broadcast_to(rgb, (Hl, Wl, 3))
    else:
        rgb = np.broadcast_to(np.array([255, 251, 244.]), (Hl, Wl, 3))
    # sombra própria (contorno escuro suave + sombra larga) para ler em qualquer fundo
    edge = cv2.GaussianBlur(cv2.dilate(A, np.ones((3, 3), np.uint8), iterations=max(1, int(2 * s))), (0, 0), 1.2 * s) * 0.55
    soft = np.roll(cv2.GaussianBlur(A, (0, 0), 14 * s), int(8 * s), 0) * 0.7
    return {"rgb": rgb.astype(np.float32), "a": A, "sh": np.maximum(edge, soft), "w": Wl, "h": Hl,
            "asc": a, "pad": pad, "L": L}


def block_layout(lines, s, W, H, cy):
    max_w = (1080 - 2 * SAFE["x1"]) * s         # margens iguais dos dois lados (centralizado de verdade)
    ls = [line_layer(L, s, max_w) for L in lines]
    gap = [int(-0.20 * l["h"]) if l["L"]["font"] == "Anton" else int(-0.12 * l["h"]) for l in ls]
    tot = sum(l["h"] for l in ls) + sum(gap[1:])
    y = int(cy * H - tot / 2)
    y = max(int(SAFE["y0"] * s), min(y, int(H - SAFE["y1"] * s - tot)))
    pos = []
    for i, l in enumerate(ls):
        if i: y += gap[i]
        pos.append((int(W / 2 - l["w"] / 2), y)); y += l["h"]
    return ls, pos


def paste(f, l, x, y, alpha, scale=1.0, dy=0, blur=0.0):
    rgb, A, sh = l["rgb"], l["a"] * alpha, l["sh"] * alpha
    if scale != 1.0:
        w2, h2 = max(2, int(l["w"] * scale)), max(2, int(l["h"] * scale))
        rgb = cv2.resize(rgb, (w2, h2)); A = cv2.resize(A, (w2, h2)); sh = cv2.resize(sh, (w2, h2))
        x, y = int(x + l["w"] / 2 - w2 / 2), int(y + l["h"] / 2 - h2 / 2)
    if blur > 0.3:
        A = cv2.GaussianBlur(A, (0, 0), blur); sh = cv2.GaussianBlur(sh, (0, 0), blur)
    y += int(dy)
    H, W = f.shape[:2]; h, w = A.shape
    xa, ya, xb, yb = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if xb <= xa or yb <= ya: return
    sl = (slice(ya - y, yb - y), slice(xa - x, xb - x))
    reg = f[ya:yb, xa:xb]
    reg *= (1 - sh[sl][..., None])
    a = A[sl][..., None]
    f[ya:yb, xa:xb] = reg * (1 - a) + rgb[sl] * a


def draw_block(frames, T, s, fps, beat):
    H, W = frames[0].shape[:2]
    ls, pos = block_layout(T["lines"], s, W, H, T.get("cy", 0.3))
    st, en = int(round(T["start"] * fps)), int(round(T["end"] * fps))
    for j in range(max(0, st), min(len(frames), en)):
        k, left = j - st, en - j
        out = ease_io(min(1, left / 7))
        f = frames[j].astype(np.float32)
        # escurecimento local suave atrás do bloco (leitura)
        y0 = pos[0][1]; y1 = pos[-1][1] + ls[-1]["h"]
        yy = np.arange(H, dtype=np.float32)[:, None]
        g = 0.38 * out * ease_out((k + 1) / 6)
        band = np.exp(-0.5 * ((yy - (y0 + y1) / 2) / ((y1 - y0) * 0.75)) ** 2)
        f *= 1 - g * band[..., None]
        for l, (x, y) in zip(ls, pos):
            d = l["L"].get("delay", 0); q = k - d
            if q < 0: continue
            if l["L"].get("punch"):               # bate no lugar, na batida
                p = min(1, q / 7)
                sc = 1 + 0.38 * (1 - ease_out(p)) ** 2 - 0.05 * math.sin(math.pi * min(1, q / 10)) * (q > 4)
                a = min(1, (q + 1) / 3)
                paste(f, l, x, y, a * out, sc, 0, 3.5 * (1 - min(1, q / 4)))
            else:                                  # sobe e aparece
                p = ease_out(q / 8)
                paste(f, l, x, y, p * out, 1.0, (1 - p) * 34 * s, 2.5 * (1 - p))
        if T.get("bar"):                           # régua vermelha desenhando sob a palavra principal
            i = next(i for i, l in enumerate(ls) if l["L"].get("punch"))
            l, (x, y) = ls[i], pos[i]
            p = ease_out((k - l["L"].get("delay", 0) - 6) / 10)
            if p > 0:
                bw = int((l["w"] - 2 * l["pad"]) * 0.62 * p); by = y + l["h"] - int(l["pad"] * 0.55)
                cx = x + l["w"] // 2
                f[by:by + max(3, int(9 * s)), cx - bw // 2:cx + bw // 2] = f[by:by + max(3, int(9 * s)), cx - bw // 2:cx + bw // 2] * (1 - out) + np.array([214, 36, 36.]) * out
        frames[j] = np.clip(f, 0, 255).astype(np.uint8)


def end_card(frames, E, st, s, fps):
    H, W = frames[0].shape[:2]
    logo = Image.open(P(E["logo"])).convert("RGBA")
    lh = int(E["logo_h"] * H); lw = int(logo.width * lh / logo.height)
    logo = np.array(logo.resize((lw, lh), Image.LANCZOS), np.float32)
    ls, pos = block_layout(E["lines"], s, W, H, E["text_cy"])
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    n = len(frames)
    for j in range(st, n):
        k = j - st
        f = frames[j].astype(np.float32)
        g = E.get("shade", 0.5) * ease_out(k / 10)
        f *= 1 - g * (0.6 + 0.4 * np.exp(-((yy - 0.38) / 0.25) ** 2))
        p = ease_out(k / 11)
        if p > 0:                                  # logo entra de cima, assenta com quique e acende
            sc = 1 + 0.22 * (1 - p) + (0.05 * math.exp(-(k - 11) / 3) * math.cos((k - 11) * 1.4) if k >= 11 else 0)
            w2, h2 = max(2, int(lw * sc)), max(2, int(lh * sc))
            Lg = cv2.resize(logo, (w2, h2), interpolation=cv2.INTER_AREA)
            cx, cy = W // 2, int(E["logo_cy"] * H - (1 - p) * 90 * s)
            x0, y0 = cx - w2 // 2, cy - h2 // 2
            a = Lg[..., 3:4] / 255 * p
            sub = f[y0:y0 + h2, x0:x0 + w2]
            shd = cv2.GaussianBlur(a[..., 0], (0, 0), 18 * s)[..., None] * 0.6
            sub *= (1 - shd)
            sub[:] = sub * (1 - a) + Lg[..., :3] * a
            if 11 <= k < 22:
                gl = cv2.GaussianBlur(a[..., 0], (0, 0), 28 * s)[..., None] * (1 - (k - 11) / 11) * 0.55
                sub[:] = sub + (255 - sub) * gl
        for i, (l, (x, y)) in enumerate(zip(ls, pos)):
            q = k - 9 - i * 4
            if q < 0: continue
            pp = ease_out(q / 8)
            paste(f, l, x, y, pp, 1.0, (1 - pp) * 30 * s, 2.0 * (1 - pp))
        # fade final suave
        fo = ease_io((j - (n - 9)) / 9)
        if fo > 0: f *= 1 - fo * 0.85
        frames[j] = np.clip(f, 0, 255).astype(np.uint8)


# ---------------------------------------------------------------- som
def music(tl, total_s, out_wav):
    m = tl["music"]
    af = f"atrim=start={m['start']}:end={m['start'] + total_s},asetpts=PTS-STARTPTS,afade=t=out:st={total_s - m['fade_out']}:d={m['fade_out']}," \
         f"loudnorm=I={m['target_lufs']}:TP=-1.5:LRA=11,aresample=48000"
    subprocess.run([FF, "-y", "-v", "error", "-i", P(m["file"]), "-vn", "-af", af, "-ac", "2", out_wav], check=True)


# ---------------------------------------------------------------- main
def main():
    preview = "--preview" in sys.argv
    tl = json.load(open(P("timeline.json")))
    o = tl["output"]; fps = o["fps"]
    s = o.get("preview_scale", 0.5) if preview else 1.0
    W, H = int(o["w"] * s) // 2 * 2, int(o["h"] * s) // 2 * 2
    out = P(o["preview_file"] if preview else o["file"])
    b0, bp = tl["beat"]["first"], tl["beat"]["period"]
    frames, cuts, t_beat, end_st = [], [], 0, None
    for sh in tl["shots"]:
        if "dur_to_beat" in sh:
            t_beat = sh["dur_to_beat"]; t_end = b0 + t_beat * bp
        else:
            t_beat += sh["beats"]; t_end = b0 + t_beat * bp
        if sh is tl["shots"][-1]: t_end = tl["music"]["end"] - tl["music"]["start"]
        n = int(round(t_end * fps)) - len(frames)
        fr = (photo_frames(sh, n, W, H) if sh["src"].lower().endswith((".jpg", ".png"))
              else video_frames(sh, n, W, H, fps, tl))
        # entrada do plano: 2 quadros de leve clarão só nos cortes do gancho e do fecho (sem flash constante)
        cuts.append({"t": round(len(frames) / fps, 3), "src": os.path.basename(sh["src"]), "o_que": sh.get("_o_que", "")})
        if sh.get("end_card"): end_st = len(frames)
        frames += fr
    for T in tl["texts"]: draw_block(frames, T, s, fps, (b0, bp))
    if tl.get("end_card") and end_st is not None: end_card(frames, tl["end_card"], end_st, s, fps)
    total_s = len(frames) / fps
    os.makedirs(os.path.dirname(out), exist_ok=True)
    wav = P("work/musica.wav"); os.makedirs(P("work"), exist_ok=True)
    music(tl, total_s, wav)
    enc = [FF, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
           "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p",
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]
    enc += (["-preset", "veryfast", "-crf", "24"] if preview else
            ["-preset", "slow", "-crf", "17", "-maxrate", "14M", "-bufsize", "24M", "-profile:v", "high", "-level", "4.1"])
    enc += ["-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", out]
    pe = subprocess.Popen(enc, stdin=subprocess.PIPE)
    for f in frames: pe.stdin.write(f.tobytes())
    pe.stdin.close(); pe.wait()
    if not preview:                                # versão para WhatsApp: ~12 MB, mesma imagem
        wa = out.replace(".mp4", "-WHATSAPP.mp4")
        subprocess.run([FF, "-y", "-v", "error", "-i", out, "-c:v", "libx264", "-preset", "slow", "-b:v", "3000k",
                        "-maxrate", "3800k", "-bufsize", "6000k", "-profile:v", "high", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", wa], check=True)
    json.dump({"duracao": round(total_s, 3), "fps": fps, "cortes": cuts}, open(out + ".cortes.json", "w"),
              ensure_ascii=False, indent=2)
    print(f"{out}  {len(frames)} quadros = {total_s:.2f} s")


if __name__ == "__main__":
    main()
