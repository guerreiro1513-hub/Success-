#!/usr/bin/env python3
"""3 unidades, o mesmo chiado — montagem dos 3 vídeos já postados (um por unidade): só a churrasqueira girando e o som
real dela. Bloco por unidade com o nome; fecho com logo e as 3 unidades. 1080x1920, 30 fps.   python3 render.py
"""
import os, subprocess
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
from scipy.io import wavfile
ROOT = os.path.dirname(os.path.abspath(__file__)); P = lambda p: os.path.join(ROOT, p)
W, H, FPS, SR = 1080, 1920, 30, 48000
AN, MO = P("assets/fonts/Anton-Regular.ttf"), P("assets/fonts/Montserrat.ttf")
OUT = P("../../entrega/guerreiros-3-UNIDADES-CHIADO.mp4")
A, B, C = "source/A.mov", "source/B.mov", "source/C.mp4"     # A = Jardim Aclimação, B = Tropical Ville, C = Florais
# (fonte, início, segundos, unidade)
SHOTS = [(C, 10.0, 2.0, None),
         (B, 2.4, 1.7, "TROPICAL VILLE"), (B, 13.0, 1.6, "TROPICAL VILLE"), (B, 18.4, 1.7, "TROPICAL VILLE"),
         (C, 12.6, 1.7, "FLORAIS"), (C, 15.2, 1.6, "FLORAIS"), (C, 17.6, 1.7, "FLORAIS"),
         (A, 7.6, 1.7, "JARDIM ACLIMAÇÃO"), (A, 15.6, 1.6, "JARDIM ACLIMAÇÃO"), (A, 17.2, 1.7, "JARDIM ACLIMAÇÃO"),
         (A, 9.6, 3.0, "FIM")]
GRADE = {A: "eq=contrast=1.06:saturation=1.06", B: "eq=contrast=1.06:saturation=1.06", C: "null"}

def eo(t): t = min(1, max(0, t)); return 1 - (1 - t) ** 3
def ei(t): t = min(1, max(0, t)); return t * t * (3 - 2 * t)

def line(text, font, size, color, track=0.0, weight=None):
    while True:
        f = ImageFont.truetype(font, size)
        if weight: f.set_variation_by_axes([weight])
        sp = size * track; w = sum(f.getlength(c) for c in text) + sp * (len(text) - 1)
        if w <= 860 or size < 20: break
        size -= 2
    a, d = f.getmetrics(); pad = int(size * 0.25)
    m = Image.new("L", (int(w) + 2 * pad, a + d + 2 * pad), 0); dr = ImageDraw.Draw(m); x = pad
    for c in text: dr.text((x, pad), c, font=f, fill=255); x += f.getlength(c) + sp
    Am = np.array(m, np.float32) / 255; h, wd = Am.shape
    if color == "fire":
        yy = np.clip((np.arange(h)[:, None] - pad - a * 0.15) / (a * 0.95), 0, 1)[..., None]
        rgb = np.array([255, 206, 82.]) * (1 - yy) + np.array([238, 92, 18.]) * yy
    elif color == "gold": rgb = np.array([240, 196, 98.])[None, None]
    else: rgb = np.array([255, 251, 244.])[None, None]
    rgb = np.broadcast_to(rgb, (h, wd, 3)).astype(np.float32)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * max(2, size // 22) + 1,) * 2)
    edge = cv2.GaussianBlur(cv2.dilate(Am, k), (0, 0), 1.2) * 0.75
    soft = np.roll(cv2.GaussianBlur(Am, (0, 0), size * 0.14), int(size * 0.06), 0) * 0.6
    return {"rgb": rgb, "A": Am, "sh": np.maximum(edge, soft), "w": wd, "h": h}

def put(f, L, cx, cy, alpha, dy=0.0, scale=1.0):
    rgb, Am, sh = L["rgb"], L["A"], L["sh"]; w, h = L["w"], L["h"]
    if abs(scale - 1) > 1e-3:
        w, h = max(2, int(w * scale)), max(2, int(h * scale)); rgb, Am, sh = cv2.resize(rgb, (w, h)), cv2.resize(Am, (w, h)), cv2.resize(sh, (w, h))
    x, y = int(cx - w / 2), int(cy - h / 2 + dy)
    xa, ya, xb, yb = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    sl = (slice(ya - y, yb - y), slice(xa - x, xb - x)); reg = f[ya:yb, xa:xb]
    reg *= 1 - (sh[sl] * alpha)[..., None]
    a = (Am[sl] * alpha)[..., None]; reg[:] = reg * (1 - a) + rgb[sl] * a

T_HOOK = [line("AUMENTA O SOM", MO, 54, "white", 0.18, 800)]
LAB = {u: (line("UNIDADE", MO, 42, "gold", 0.30, 800), line(u, AN, 118, "white")) for u in ["TROPICAL VILLE", "FLORAIS", "JARDIM ACLIMAÇÃO"]}
END = (line("3 UNIDADES", AN, 120, "fire"), line("TROPICAL VILLE · FLORAIS · JARDIM ACLIMAÇÃO", MO, 40, "white", 0.03, 800))
lg = Image.open(P("assets/logo.png")).convert("RGBA"); lw = 380; lh = int(lg.height * lw / lg.width)
LOGO = np.array(lg.resize((lw, lh), Image.LANCZOS), np.float32)

def frames(src, st, n):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{st:.3f}", "-i", P(src), "-frames:v", str(n), "-vf",
                          f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},{GRADE[src]},format=rgb24",
                          "-an", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    fr = list(np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3))
    while len(fr) < n: fr.append(fr[-1])
    return fr[:n]

enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                        "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", P("work/video.mp4")], stdin=subprocess.PIPE)
yy = np.arange(H, dtype=np.float32)[:, None, None]
t0 = {}; n0 = 0
for src, st, d, u in SHOTS:
    if u not in t0: t0[u] = n0
    n0 += int(round(d * FPS))
n0 = 0
for src, st, d, u in SHOTS:
    n = int(round(d * FPS))
    for j, fr in enumerate(frames(src, st, n)):
        f = fr.astype(np.float32); g = n0 + j; t = g / FPS
        if u is None and t >= 0.2:                                   # gancho
            put(f, T_HOOK[0], W / 2, 0.20 * H, eo((t - 0.2) / 0.25) * ei((2.0 - t) / 0.15), (1 - eo((t - 0.2) / 0.25)) * 20)
        if u in LAB:                                                 # nome da unidade, segura o bloco inteiro
            k = (g - t0[u]) / FPS; end = [s for s in SHOTS if s[3] == u]; dur_u = sum(s[2] for s in end)
            al = eo(k / 0.25) * ei((dur_u - k) / 0.15)
            f *= 1 - 0.38 * al * np.exp(-0.5 * ((yy - 0.72 * H) / 170) ** 2)
            put(f, LAB[u][0], W / 2, 0.68 * H, al, (1 - eo(k / 0.25)) * 18)
            put(f, LAB[u][1], W / 2, 0.735 * H, al, 0, 1 + 0.25 * (1 - eo(min(1, k / 0.18))) ** 2)
        if u == "FIM":
            k = j / FPS; q = eo(k / 0.4)
            f *= 1 - 0.55 * q
            a = LOGO[..., 3:4] / 255 * eo((k - 0.1) / 0.4); x0, y0 = W // 2 - lw // 2, int(0.40 * H) - lh // 2
            reg = f[y0:y0 + lh, x0:x0 + lw]; reg[:] = reg * (1 - a) + LOGO[..., :3] * a
            put(f, END[0], W / 2, 0.585 * H, eo((k - 0.45) / 0.3), (1 - eo((k - 0.45) / 0.3)) * 20)
            put(f, END[1], W / 2, 0.635 * H, eo((k - 0.7) / 0.3))
            fo = ei((j - (n - 10)) / 10)
            if fo > 0: f *= 1 - fo
        enc.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes())
    n0 += n
enc.stdin.close(); enc.wait()
T = n0 / FPS
# som: só o chiado real da churrasqueira (áudio do vídeo da Tropical Ville, que é só a churrasqueira), contínuo
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", P(B), "-vn", "-ac", "2", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True).stdout
bed = np.frombuffer(raw, np.int16).reshape(-1, 2).astype(np.float32) / 32768
N = int(T * SR); bed = bed[:N] if len(bed) >= N else np.pad(bed, ((0, N - len(bed)), (0, 0)), mode="wrap")
fi, fo = int(0.2 * SR), int(0.8 * SR); bed[:fi] *= np.linspace(0, 1, fi)[:, None]; bed[-fo:] *= np.linspace(1, 0, fo)[:, None]
wavfile.write(P("work/audio.wav"), SR, (np.clip(bed, -1, 1) * 32767).astype(np.int16))
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", P("work/video.mp4"), "-i", P("work/audio.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                "-af", "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", OUT], check=True)
print(OUT, f"{T:.2f} s")
