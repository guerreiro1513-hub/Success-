#!/usr/bin/env python3
"""Aviso: abertos no feriado nas 3 unidades — textos animados sobre o vídeo do cliente (1080x1920, 60 fps).
Os textos entram nos cortes do próprio vídeo. Áudio original mantido.   python3 render.py
"""
import math, os, subprocess
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.abspath(__file__)); P = lambda p: os.path.join(ROOT, p)
W, H, FPS = 1080, 1920, 60
SRC, OUT = P("source/VIDEO.mov"), P("../../entrega/guerreiros-FERIADO-3-UNIDADES.mp4")
AN, MO = P("assets/fonts/Anton-Regular.ttf"), P("assets/fonts/Montserrat.ttf")
SAFE_W = 900                                              # x 90–990

def eo(t): t = min(1, max(0, t)); return 1 - (1 - t) ** 3
def ei(t): t = min(1, max(0, t)); return t * t * (3 - 2 * t)

def line(text, font, size, color, track=0.0, weight=None):
    while True:
        f = ImageFont.truetype(font, size)
        if weight: f.set_variation_by_axes([weight])
        sp = size * track; w = sum(f.getlength(c) for c in text) + sp * (len(text) - 1)
        if w <= SAFE_W - 40 or size < 20: break
        size -= 2
    a, d = f.getmetrics(); pad = int(size * 0.25)
    m = Image.new("L", (int(w) + 2 * pad, a + d + 2 * pad), 0); dr = ImageDraw.Draw(m); x = pad
    for c in text: dr.text((x, pad), c, font=f, fill=255); x += f.getlength(c) + sp
    A = np.array(m, np.float32) / 255; h, wd = A.shape
    if color == "fire":
        yy = np.clip((np.arange(h)[:, None] - pad - a * 0.15) / (a * 0.95), 0, 1)[..., None]
        rgb = np.array([255, 206, 82.]) * (1 - yy) + np.array([238, 92, 18.]) * yy
    elif color == "gold": rgb = np.array([240, 196, 98.])[None, None]
    else: rgb = np.array([255, 251, 244.])[None, None]
    rgb = np.broadcast_to(rgb, (h, wd, 3)).astype(np.float32)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * max(2, size // 22) + 1,) * 2)
    edge = cv2.GaussianBlur(cv2.dilate(A, k), (0, 0), 1.2) * 0.75
    soft = np.roll(cv2.GaussianBlur(A, (0, 0), size * 0.14), int(size * 0.06), 0) * 0.6
    return {"rgb": rgb, "A": A, "sh": np.maximum(edge, soft), "w": wd, "h": h}

def put(f, L, cx, cy, alpha, scale=1.0, dy=0.0, blur=0.0):
    rgb, A, sh = L["rgb"], L["A"], L["sh"]; w, h = L["w"], L["h"]
    if abs(scale - 1) > 1e-3:
        w, h = max(2, int(w * scale)), max(2, int(h * scale))
        rgb, A, sh = cv2.resize(rgb, (w, h)), cv2.resize(A, (w, h)), cv2.resize(sh, (w, h))
    if blur > 0.3: A, sh = cv2.GaussianBlur(A, (0, 0), blur), cv2.GaussianBlur(sh, (0, 0), blur)
    x, y = int(cx - w / 2), int(cy - h / 2 + dy)
    xa, ya, xb, yb = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if xb <= xa or yb <= ya: return
    sl = (slice(ya - y, yb - y), slice(xa - x, xb - x)); reg = f[ya:yb, xa:xb]
    reg *= 1 - (sh[sl] * alpha)[..., None]
    a = (A[sl] * alpha)[..., None]; reg[:] = reg * (1 - a) + rgb[sl] * a

# blocos: (início, fim, centro y, [(linha, atraso s, efeito)])
B = []
def block(t0, t1, cy, rows, gap=0.92): B.append((t0, t1, cy, rows, gap))
block(0.15, 2.92, 0.235, [(line("NO FERIADO", MO, 66, "white", 0.14, 800), 0.0, "rise"),
                          (line("ESTAMOS ABERTOS", AN, 150, "fire"), 0.12, "punch")])
block(2.97, 5.42, 0.225, [(line("NAS", MO, 66, "white", 0.14, 800), 0.0, "rise"),
                          (line("3 UNIDADES", AN, 200, "fire"), 0.10, "punch")])
for i, (t0, t1, nome) in enumerate([(5.47, 6.88, "TROPICAL VILLE"), (6.93, 8.42, "FLORAIS"), (8.47, 9.88, "JARDIM ACLIMAÇÃO")]):
    block(t0, t1, 0.705, [(line(f"UNIDADE {i + 1}/3", MO, 46, "gold", 0.22, 800), 0.0, "rise"),
                          (line(nome, AN, 128, "white"), 0.06, "punch")])
block(11.47, 15.40, 0.235, [(line("FERIADO É DIA DE", MO, 62, "white", 0.10, 800), 0.0, "rise"),
                            (line("CHURRASCO", AN, 190, "fire"), 0.12, "punch")])
block(18.15, 20.42, 0.715, [(line("ABERTOS NO FERIADO", AN, 92, "fire"), 0.0, "rise"),
                            (line("TROPICAL VILLE · FLORAIS · JARDIM ACLIMAÇÃO", MO, 44, "white", 0.03, 800), 0.18, "rise")], gap=1.0)

def layout(rows, cy, gap):
    hs = [r[0]["h"] for r in rows]; tot = sum(hs) * gap
    y = cy * H - tot / 2; out = []
    for r, h in zip(rows, hs): out.append(y + h * gap / 2); y += h * gap
    return out

dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", SRC], capture_output=True, text=True).stdout)
n = int(round(dur * FPS))
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", SRC, "-vf", f"fps={FPS},format=rgb24", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                        "-i", SRC, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
                        "-profile:v", "high", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                        "-c:a", "copy", "-movflags", "+faststart", "-shortest", OUT], stdin=subprocess.PIPE)
yy = np.arange(H, dtype=np.float32)[:, None, None]
for j in range(n):
    b = dec.stdout.read(W * H * 3)
    if len(b) < W * H * 3: break
    f = np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.float32); t = j / FPS
    for t0, t1, cy, rows, gap in B:
        if not (t0 <= t < t1): continue
        out = ei((t1 - t) / 0.18)
        ys = layout(rows, cy, gap)
        g = 0.42 * out * eo((t - t0) / 0.2)                  # sombra local atrás do bloco (leitura)
        f *= 1 - g * np.exp(-0.5 * ((yy - cy * H) / (sum(r[0]["h"] for r in rows) * 0.8)) ** 2)
        for (L, dl, fx), y in zip(rows, ys):
            k = t - t0 - dl
            if k < 0: continue
            if fx == "punch":
                q = min(1, k / 0.16); sc = 1 + 0.35 * (1 - eo(q)) ** 2
                put(f, L, W / 2, y, min(1, k / 0.05) * out, sc, 0, 4 * (1 - q))
            else:
                p = eo(k / 0.22); put(f, L, W / 2, y, p * out, 1.0, (1 - p) * 26, 3 * (1 - p))
    enc.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes())
enc.stdin.close(); enc.wait(); dec.wait()
print(OUT, j + 1, "quadros")
