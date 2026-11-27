#!/usr/bin/env python3
"""Comercial de produto do cardápio Guerreiros Grill (9:16, 30 fps). Lê produtos/<PRODUTO>.json.
    python3 render.py COSTELA [--preview]
Planos vêm de work/*.mov (prep.py: estabilizado e em câmera lenta). Cor escura e quente, profundidade (bordas e fundo
escurecidos e desfocados), fecho com o logo real e o nome do corte. Som: trilha própria (Kairogen) + ambiente + impacto.
"""
import json, math, os, subprocess, sys
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
from scipy.io import wavfile
FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
ROOT = os.path.dirname(os.path.abspath(__file__)); P = lambda p: os.path.join(ROOT, p)
SR = 48000


def ease_out(t): t = min(1, max(0, t)); return 1 - (1 - t) ** 3
def ease_io(t): t = min(1, max(0, t)); return t * t * (3 - 2 * t)


def read_shot(sh, W, H, grade):
    n = int(round(sh["dur"] * 30))
    vf = f"{grade},scale={W}:{H}:flags=lanczos,format=rgb24"
    if sh.get("speed", 1) != 1: vf = f"setpts={1/sh['speed']:.4f}*PTS,minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1," + vf
    raw = subprocess.run([FF, "-v", "error", "-ss", f"{sh['in']:.3f}", "-i", P(sh["src"]), "-frames:v", str(n), "-vf", vf,
                          "-an", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    fr = list(np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3))
    while len(fr) < n: fr.append(fr[-1])
    out = []
    z0, z1 = sh.get("zoom", [1, 1]); cx, cy = sh.get("center", [0.5, 0.5])
    for j, f in enumerate(fr[:n]):
        z = z0 + (z1 - z0) * ease_io(j / max(1, n - 1))
        if abs(z - 1) > 1e-3:
            M = cv2.getRotationMatrix2D((W * cx, H * cy), 0, z); M[0, 2] += W * (0.5 - cx); M[1, 2] += H * (0.5 - cy)
            f = cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
        out.append(np.ascontiguousarray(f))
    return out


_M = {}
def depth(f, look):
    """Fundo e bordas mais escuros e desfocados (lente aberta, luz concentrada na carne)."""
    H, W = f.shape[:2]
    if (W, H) not in _M:
        y, x = np.mgrid[0:H, 0:W].astype(np.float32)
        cy = look.get("focus_cy", 0.55)
        r = np.sqrt(((x - W / 2) / (W * 0.62)) ** 2 + ((y - H * cy) / (H * 0.42)) ** 2)
        blur = np.clip((r - 0.75) / 0.6, 0, 1) ** 1.4
        dark = np.clip((r - 0.55) / 0.9, 0, 1) ** 1.2 * look.get("vignette", 0.55)
        top = np.clip((H * look.get("top_dark_to", 0.30) - y) / (H * 0.25), 0, 1) * look.get("top_dark", 0.45)
        _M[(W, H)] = (blur[..., None], np.maximum(dark, top)[..., None])
    blur, dark = _M[(W, H)]
    b = cv2.GaussianBlur(f, (0, 0), W / 110)
    f = f * (1 - blur) + b * blur
    # halation leve nas altas luzes
    hl = cv2.GaussianBlur(np.clip(f.max(2) - 205, 0, 50) / 50, (0, 0), W / 60)[..., None]
    f = f + hl * np.array([40, 18, 6.]) * 0.6
    return f * (1 - dark)


def font(path, size, var=None):
    f = ImageFont.truetype(P(path), max(8, int(size)))
    try:
        if isinstance(var, str): f.set_variation_by_name(var)
        elif isinstance(var, (int, float)): f.set_variation_by_axes([var])
    except Exception: pass
    return f


def text_layer(text, path, size, var, tracking, color, W):
    f = font(path, size, var); sp = f.size * tracking
    w = sum(f.getlength(c) for c in text) + sp * (len(text) - 1)
    a, d = f.getmetrics(); pad = int(size * 0.4)
    im = Image.new("L", (int(w) + 2 * pad, a + d + 2 * pad), 0); dr = ImageDraw.Draw(im); x = pad
    for c in text: dr.text((x, pad), c, font=f, fill=255); x += f.getlength(c) + sp
    A = np.array(im, np.float32) / 255
    sh = cv2.GaussianBlur(A, (0, 0), size * 0.12) * 0.6
    return A, sh, np.array(color, np.float32)


def put(f, layer, cx, cy, alpha, dy=0):
    A, sh, col = layer; h, w = A.shape; H, W = f.shape[:2]
    x, y = int(cx - w / 2), int(cy - h / 2 + dy)
    xa, ya, xb, yb = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if xb <= xa or yb <= ya: return
    sl = (slice(ya - y, yb - y), slice(xa - x, xb - x)); reg = f[ya:yb, xa:xb]
    reg *= 1 - (sh[sl] * alpha)[..., None]
    a = (A[sl] * alpha)[..., None]; reg[:] = reg * (1 - a) + col * a


def end_card(frames, E, st, s):
    H, W = frames[0].shape[:2]
    lg = Image.open(P(E["logo"])).convert("RGBA"); lh = int(E["logo_h"] * H); lw = int(lg.width * lh / lg.height)
    logo = np.array(lg.resize((lw, lh), Image.LANCZOS), np.float32)
    name = text_layer(E["name"], "assets/fonts/PlayfairDisplay-Italic[wght].ttf", E["name_size"] * s, "Medium Italic", 0.0, [246, 228, 196], W)
    brand = text_layer(E["brand"], "assets/fonts/Montserrat.ttf", 40 * s, 600, 0.30, [236, 204, 142], W)
    rule_w = int(150 * s)
    for j in range(st, len(frames)):
        k = j - st; f = frames[j].astype(np.float32)
        g = ease_out(k / 18) * E.get("shade", 0.62)
        f *= 1 - g
        p = ease_out((k - 4) / 16)
        if p > 0:
            sc = 0.94 + 0.06 * p; w2, h2 = int(lw * sc), int(lh * sc)
            L = cv2.resize(logo, (w2, h2), interpolation=cv2.INTER_AREA)
            x0, y0 = W // 2 - w2 // 2, int(E["logo_cy"] * H) - h2 // 2
            a = L[..., 3:4] / 255 * p; sub = f[y0:y0 + h2, x0:x0 + w2]
            sub[:] = sub * (1 - a) + L[..., :3] * a
        q = ease_out((k - 12) / 16)
        if q > 0: put(f, name, W / 2, E["name_cy"] * H, q, (1 - q) * 16 * s)
        r = ease_out((k - 18) / 14)
        if r > 0:
            y = int((E["name_cy"] + 0.045) * H); hw = int(rule_w * r / 2)
            f[y:y + max(2, int(2 * s)), W // 2 - hw:W // 2 + hw] = np.array([190, 150, 90.])
        b = ease_out((k - 16) / 12)
        if b > 0: put(f, brand, W / 2, (E["name_cy"] + 0.08) * H, b)
        fo = ease_io((j - (len(frames) - 12)) / 12)
        if fo > 0: f *= 1 - fo
        frames[j] = np.clip(f, 0, 255).astype(np.uint8)


def boom(dur=1.6):
    n = int(dur * SR); t = np.arange(n) / SR
    y = np.sin(2 * np.pi * (52 * t - 9 * t * t)) * np.exp(-t * 3.2)
    y += 0.25 * np.random.default_rng(1).standard_normal(n) * np.exp(-t * 18)
    y = np.convolve(y, np.ones(24) / 24, "same")
    return (y / np.abs(y).max()).astype(np.float32)


def main():
    prod = sys.argv[1]; preview = "--preview" in sys.argv
    C = json.load(open(P(f"produtos/{prod}.json"))); s = 0.5 if preview else 1.0
    W, H = int(1080 * s) // 2 * 2, int(1920 * s) // 2 * 2
    out = P(f"../../entrega/{'previa-' if preview else ''}guerreiros-{prod}.mp4")
    frames, starts = [], []
    for i, sh in enumerate(C["shots"]):
        fr = read_shot(sh, W, H, C["grade"])
        fr = [np.clip(depth(f.astype(np.float32), C["look"]), 0, 255).astype(np.uint8) for f in fr]
        if i == 0:
            for j in range(min(10, len(fr))): fr[j] = (fr[j] * ease_io((j + 1) / 10)).astype(np.uint8)   # entra do preto
        ov = sh.get("dissolve", 0)
        if ov and frames:
            for j in range(ov):
                w = ease_io((j + 1) / (ov + 1)); fr[j] = (frames[-ov + j] * (1 - w) + fr[j] * w).astype(np.uint8)
            frames = frames[:-ov]
        starts.append(len(frames)); frames += fr
    end_st = int(C["end_card"]["start"] * 30)
    end_card(frames, C["end_card"], end_st, s)
    n = len(frames); T = n / 30
    # som
    A = np.zeros((int(T * SR), 2), np.float32)
    mu = C["audio"]
    raw = subprocess.run([FF, "-v", "error", "-i", P(mu["music"]), "-ac", "2", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True).stdout
    m = np.frombuffer(raw, np.int16).reshape(-1, 2).astype(np.float32) / 32768
    i0 = int(mu["music_at"] * SR)
    if i0 < 0: m = m[-i0:]; i0 = 0                       # negativo: começa a trilha mais adiante
    m = m[:len(A) - i0]; A[i0:i0 + len(m)] += m * 10 ** (mu["music_db"] / 20)
    for sh, st in zip(C["shots"], starts):
        if sh.get("amb_src"):
            raw = subprocess.run([FF, "-v", "error", "-ss", str(sh["amb_in"]), "-t", f"{sh['dur'] / sh.get('amb_speed', 1):.3f}", "-i", P(sh["amb_src"]),
                                  "-af", f"atempo={max(0.5, sh.get('amb_speed', 1))},highpass=f=120", "-ac", "2", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True).stdout
            x = np.frombuffer(raw, np.int16).reshape(-1, 2).astype(np.float32) / 32768
            i = int(st / 30 * SR); x = x[:len(A) - i]; fd = min(len(x) // 2, int(0.3 * SR))
            x[:fd] *= np.linspace(0, 1, fd)[:, None]; x[-fd:] *= np.linspace(1, 0, fd)[:, None]
            A[i:i + len(x)] += x * 10 ** (mu["amb_db"] / 20)
    b = boom(); i = int(C["end_card"]["start"] * SR); bb = b[:len(A) - i]; A[i:i + len(bb)] += bb[:, None] * 10 ** (mu["boom_db"] / 20)
    fo = int(0.6 * SR); A[-fo:] *= np.linspace(1, 0, fo)[:, None]
    wav = P(f"work/{prod}.wav"); wavfile.write(wav, SR, (np.clip(A, -1, 1) * 32767).astype(np.int16))
    enc = [FF, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30", "-i", "-", "-i", wav,
           "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]
    enc += (["-preset", "veryfast", "-crf", "24"] if preview else ["-preset", "slow", "-crf", "15", "-maxrate", "20M", "-bufsize", "24M", "-profile:v", "high"])
    enc += ["-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", out]
    pe = subprocess.Popen(enc, stdin=subprocess.PIPE)
    for f in frames: pe.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes())
    pe.stdin.close(); pe.wait()
    print(f"{out}  {n} quadros = {T:.2f} s")


if __name__ == "__main__":
    main()
