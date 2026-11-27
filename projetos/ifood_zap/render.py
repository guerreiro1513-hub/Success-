#!/usr/bin/env python3
"""Guerreiro's Grill no iFood — vídeo para WhatsApp (roteiro "Roteiro-iFood-v2-com-o-pai.pdf"). 1080x1920, 30 fps.
Falas reais do Fabrício; silêncios longos encurtados; B-roll no ritmo da fala. Sem preço/promoção.   python3 render.py
"""
import os, subprocess, math
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
from scipy.io import wavfile
ROOT = os.path.dirname(os.path.abspath(__file__)); P = lambda p: os.path.join(ROOT, p)
W, H, FPS, SR = 1080, 1920, 30, 48000
HIST = P("../historia/source/")
SRC = dict(HOOK=P("source/B2488.mov"), VO=P("source/FALA.mov"), L3=P("source/B2496b.mov"), L4=P("source/B2496a.mov"),
           GUAR=P("source/G04a.mov"), ROL=P("source/ROLETE.mov"), FER=P("source/FERIADO.mov"),
           E4K=HIST + "HOJE_E.mov", TROP=HIST + "HOJE_B.mov", FERF=HIST + "HOJE_G.mov")
OUT = P("../../entrega/guerreirosgrill_ifood_whatsapp_v1.mp4")
ACC = np.array([214, 164, 54], np.float32); OFF = np.array([243, 236, 224], np.float32); BG = (20, 16, 12)
FB = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"; FS = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
FILL = f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H}"
GRADE = "eq=contrast=1.05:saturation=1.0"                # só correção básica (comida como é)

# ---- linha do tempo (s) -----------------------------------------------------------------------
# (t0, t1, fonte, início na fonte, zoom) ; zoom: ("punch", t_rel, z1, dur) | ("push", z0, z1) | None
V = [
    (0.00, 3.80, "HOOK", 0.15, ("punch", 0.80, 1.15, 0.4)),        # "Cuiabá, chegou a novidade. O Guerreiro's agora está no iFood."
    (3.80, 5.00, "E4K", 0.4, None),                                  # V.O. "A gente começa com o que o povo já conhece:"
    (5.00, 6.25, "TROP", 18.4, None),
    (6.25, 7.55, "FER", 0.0, None),                                  # "costela" (costela no rolete)
    (7.55, 8.95, "ROL", 2.55, None),                                 # "frango assado" (corta a legenda queimada)
    (8.95, 10.35, "GUAR", 0.0, None),                                # "e as guarnições"
    (10.35, 15.65, "L3", 0.7, ("punch", 1.60, 1.12, 0.5)),           # diferencial (2º zoom)
    (15.65, 16.90, "FERF", 15.6, None),                              # Em breve: mais cortes
    (16.90, 18.15, "FERF", 7.0, None),
    (18.15, 21.10, "L4", 0.7, ("push", 1.00, 1.055)),                # crescimento: zoom lento no rosto
    (21.10, 22.65, "L4", 4.85, ("push", 1.065, 1.08)),
]
CTA0, T_END = 22.65, 26.65
# áudio de voz: (fonte, início, fim, posição no vídeo)
VOZ = [("HOOK", 0.15, 3.95, 0.00),
       ("VO", 0.35, 2.80, 3.80), ("VO", 4.00, 4.35, 6.30), ("VO", 4.90, 6.15, 7.60), ("VO", 6.95, 8.10, 9.00),
       ("L3", 0.70, 6.00, 10.35), ("L4", 0.70, 3.65, 18.15), ("L4", 4.85, 6.40, 21.10)]
LABELS = [("Costela", 6.30, 7.55), ("Frango assado", 7.60, 8.95), ("Guarnições", 9.00, 10.35), ("Em breve: mais cortes", 15.70, 18.10)]

def eo(t): t = min(1, max(0, t)); return 1 - (1 - t) ** 3
def back(t, s=1.7): t = min(1, max(0, t)) - 1; return 1 + (s + 1) * t ** 3 + s * t ** 2

def layer(text, font, size, color, maxw=960):
    while True:
        f = ImageFont.truetype(font, size); w = f.getlength(text)
        if w <= maxw or size < 30: break
        size -= 2
    a, d = f.getmetrics(); pad = 30
    m = Image.new("L", (int(w) + 2 * pad, a + d + 2 * pad), 0); ImageDraw.Draw(m).text((pad, pad), text, font=f, fill=255)
    A = np.array(m, np.float32) / 255
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))
    edge = np.clip(cv2.dilate(A, k), 0, 1)                                        # contorno preto 6 px
    sh = np.roll(cv2.GaussianBlur(edge, (0, 0), 8), 5, axis=0) * 0.5
    return dict(A=A, E=edge, S=sh, rgb=np.array(color, np.float32), w=A.shape[1], h=A.shape[0])

def put(f, L, cx, cy, al, sc=1.0, under=False):
    A, E, S = L["A"], L["E"], L["S"]
    if abs(sc - 1) > 1e-3: A, E, S = [cv2.resize(x, None, fx=sc, fy=sc) for x in (A, E, S)]
    h, w = A.shape; x0, y0 = int(cx - w / 2), int(cy - h / 2)
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    sl = (slice(ya - y0, yb - y0), slice(xa - x0, xb - x0)); reg = f[ya:yb, xa:xb]
    reg *= (1 - np.maximum(S[sl], E[sl]) * al)[..., None]
    a = (A[sl] * al)[..., None]; reg[:] = reg * (1 - a) + L["rgb"] * a
    if under:                                                                      # sublinhado dourado
        uw = int((w - 60) * min(1, al * 1.2)); uy = y0 + h - 22
        cv2.rectangle(f, (int(cx - uw / 2), uy), (int(cx + uw / 2), uy + 10), ACC.tolist(), -1)

HOOK_L = [layer("O GUERREIRO'S", FB, 96, (255, 255, 255)), layer("CHEGOU NO IFOOD", FB, 96, (255, 255, 255))]
LAB_L = {t: layer(t, FB, 84, (255, 255, 255)) for t, _, _ in LABELS}
CTA_L = [layer("Sábado e domingo,", FB, 82, OFF), layer("pelo iFood", FB, 96, ACC), layer("Procure Guerreiro's Grill", FS, 56, OFF)]
lg = Image.open(P("../historia/assets/logo_clean.png")).convert("RGBA")
def logo_arr(w):
    h = int(lg.height * w / lg.width); return np.array(lg.resize((w, h), Image.LANCZOS), np.float32)
LOGO_S, LOGO_B = logo_arr(120), logo_arr(440)

def paste_logo(f, L, x0, y0, al):
    h, w = L.shape[:2]; a = L[..., 3:4] / 255 * al; reg = f[y0:y0 + h, x0:x0 + w]; reg[:] = reg * (1 - a) + L[..., :3] * a

CROP = {"ROL": "crop=iw*0.75:ih*0.74:iw*0.125:0,"}
def frames(src, st, n):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{st:.3f}", "-i", SRC[src], "-frames:v", str(n), "-vf",
                          f"fps={FPS},{CROP.get(src, '')}{FILL},{GRADE},format=rgb24", "-an", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    fr = list(np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3))
    while len(fr) < n: fr.append(fr[-1])
    return fr[:n]

def zoom(f, z, cy=0.40):
    if abs(z - 1) < 1e-3: return f
    return cv2.warpAffine(f, cv2.getRotationMatrix2D((W / 2, H * cy), 0, z), (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

os.makedirs(P("work"), exist_ok=True)
enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                        "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", P("work/video.mp4")], stdin=subprocess.PIPE)
NF = int(round(T_END * FPS)); last = None
seq = []
for t0, t1, src, st, zm in V:
    n = int(round(t1 * FPS)) - int(round(t0 * FPS)); seq.append((t0, t1, src, st, zm, frames(src, st, n)))
g = 0
for t0, t1, src, st, zm, frs in seq:
    for j, fr in enumerate(frs):
        t = g / FPS; tr = j / FPS; f = fr.astype(np.float32)
        if zm:
            if zm[0] == "punch": z = 1 + (zm[2] - 1) * eo((tr - zm[1]) / zm[3]) if tr > zm[1] else 1.0
            else: z = zm[1] + (zm[2] - zm[1]) * j / max(1, len(frs) - 1)
            f = zoom(f, z)
        if t < 3.5:                                                                # texto do gancho
            for i, L in enumerate(HOOK_L):
                k = (t - 0.05 - i * 0.12) / 0.15
                if k > 0: put(f, L, W / 2, 1300 + i * 120, min(1, k) * (1 if t < 3.3 else max(0, (3.5 - t) / 0.2)), back(k) * 0.15 + 0.85, under=(i == 1))
        for txt, a0, a1 in LABELS:
            if a0 <= t <= a1 + 0.1:
                k = (t - a0) / 0.15; al = min(1, k) * (1 if t <= a1 else max(0, 1 - (t - a1) / 0.1))
                put(f, LAB_L[txt], W / 2, 1380, al, 0.85 + 0.15 * back(k), under=True)
        paste_logo(f, LOGO_S, W - 60 - 120, H - 380 - LOGO_S.shape[0], 0.7)       # logo canto inferior direito, 70%
        last = f.copy(); enc.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes()); g += 1
# CTA: flash + cartão final
yy_, xx_ = np.mgrid[0:H, 0:W]; VIGN = (1 - 0.35 * np.clip((np.hypot((xx_ - W / 2) / W, (yy_ - H / 2) / H) - 0.2) * 1.4, 0, 1))[..., None].astype(np.float32)
lastb = cv2.GaussianBlur(cv2.resize(last, (W // 4, H // 4)), (0, 0), 5); lastb = cv2.resize(lastb, (W, H))
while g < NF:
    t = g / FPS; k = t - CTA0
    f = lastb * 0.18 + np.float32(BG) * 0.82
    f *= VIGN
    sc = 0.9 + 0.1 * back(k / 0.3); al = min(1, k / 0.15)
    Lg = cv2.resize(LOGO_B, None, fx=sc, fy=sc); paste_logo(f, Lg, int(W / 2 - Lg.shape[1] / 2), int(620 - Lg.shape[0] / 2), al)
    for i, (L, y, d) in enumerate(zip(CTA_L, (1020, 1130, 1270), (0.25, 0.4, 0.6))):
        kk = (k - d) / 0.15
        if kk > 0: put(f, L, W / 2, y, min(1, kk), 0.85 + 0.15 * back(kk), under=(i == 1))
    fl = max(0, 1 - k / 0.18)                                                      # flash branco na entrada do CTA
    if fl > 0: f = f * (1 - fl) + 255 * fl
    fo = (T_END - t) / 0.5
    if fo < 1: f *= max(0, fo)
    enc.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes()); g += 1
enc.stdin.close(); enc.wait()

# ---- áudio ------------------------------------------------------------------------------------
def pcm(f, ss, t):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(ss), "-t", str(t), "-i", f, "-vn", "-ac", "1", "-ar", str(SR),
                        "-af", "highpass=f=90,afftdn=nf=-30,acompressor=threshold=-20dB:ratio=3:attack=10:release=150", "-f", "s16le", "-"],
                       capture_output=True, check=True).stdout
    return np.frombuffer(r, np.int16).astype(np.float32) / 32768
N = int(T_END * SR); voz = np.zeros(N, np.float32)
for src, a, b, pos in VOZ:
    x = pcm(SRC[src], a, b - a); fd = int(0.02 * SR); x[:fd] *= np.linspace(0, 1, fd); x[-fd:] *= np.linspace(1, 0, fd)
    p0 = int(pos * SR); m = min(len(x), N - p0); voz[p0:p0 + m] += x[:m]
voz *= 0.25 / (np.sqrt(np.mean(voz[voz != 0] ** 2)) + 1e-9)
rms = lambda v: np.sqrt(np.mean(v ** 2)) + 1e-9
mus = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-ss", "15", "-t", str(T_END + 1), "-i", P("../tres/assets/trilha-gaucha-loop.wav"),
                                    "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True).stdout, np.int16).astype(np.float32)[:N] / 32768
mus = np.pad(mus, (0, N - len(mus))); mus = mus / rms(mus) * 0.25
env = np.full(N, 10 ** (-22 / 20)); c0 = int(CTA0 * SR); env[c0:] = 10 ** (-12 / 20)          # sobe no CTA
env = np.convolve(env, np.ones(int(0.3 * SR)) / int(0.3 * SR), "same")
ch = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-ss", "11.6", "-t", "7.5", "-i", P("../../entrega/guerreiros-FLORAIS-QUI-A-DOM.mp4"),
                                   "-vn", "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True).stdout, np.int16).astype(np.float32) / 32768
siz = np.zeros(N, np.float32)
for a, b in ((3.8, 10.35), (15.65, 18.15)):                                    # chiado sob o B-roll, −26 dB
    i0, i1 = int(a * SR), int(b * SR); s = np.resize(ch, i1 - i0); s = s / rms(s) * 0.25 * 10 ** (-26 / 20)
    r_ = np.minimum(1, np.minimum(np.arange(i1 - i0), (i1 - i0) - np.arange(i1 - i0)) / (0.15 * SR)); siz[i0:i1] += s * r_
sfx = np.zeros(N, np.float32); rg = np.random.default_rng(2)
i = int(0.80 * SR); tt = np.arange(int(0.9 * SR)) / SR                          # impacto grave no zoom do gancho
boom = np.sin(2 * np.pi * (55 + 40 * np.exp(-tt * 12)) * tt) * np.exp(-tt * 4.5) + rg.standard_normal(len(tt)) * np.exp(-tt * 30) * 0.3
sfx[i:i + len(boom)] += boom * 0.35
i = int((CTA0 - 0.35) * SR); m = int(0.45 * SR); tt = np.arange(m) / SR      # whoosh na entrada do CTA
sp = np.fft.rfft(rg.standard_normal(m)); fr = np.fft.rfftfreq(m, 1 / SR); sp *= np.exp(-((fr - 1800) / 1500) ** 2)
wh = np.fft.irfft(sp, m); wh = wh / np.abs(wh).max() * np.sin(np.pi * tt / tt[-1]) ** 2; sfx[i:i + m] += wh * 0.25
mix = voz + mus * env + siz + sfx
fo = int(0.5 * SR); mix[-fo:] *= np.linspace(1, 0, fo)
wavfile.write(P("work/audio.wav"), SR, (np.clip(mix, -1, 1) * 32767).astype(np.int16))
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", P("work/video.mp4"), "-i", P("work/audio.wav"), "-map", "0:v", "-map", "1:a",
                "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-b:v", "8M", "-maxrate", "10M", "-bufsize", "16M", "-pix_fmt", "yuv420p",
                "-af", "loudnorm=I=-13:TP=-2:LRA=9,alimiter=limit=0.84:level=disabled", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                "-movflags", "+faststart", OUT], check=True)
print(OUT, T_END)
