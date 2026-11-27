#!/usr/bin/env python3
"""Guerreiro's Grill no iFood — WhatsApp v2 (estilo da referência: legenda palavra por palavra, cortes com chicote,
rampa de velocidade no B-roll, efeitos sonoros em tudo, busca animada no final).   python3 render2.py
"""
import os, subprocess, math, re
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
from scipy.io import wavfile
ROOT = os.path.dirname(os.path.abspath(__file__)); P = lambda p: os.path.join(ROOT, p)
W, H, FPS, SR = 1080, 1920, 30, 48000
HIST = P("../historia/source/")
SRC = dict(HOOK=P("source/B2488.mov"), VO=P("source/FALA.mov"), L3=P("source/B2496b.mov"), CTA=P("source/B2496a.mov"),
           GUAR=P("source/G04a.mov"), ROL=P("source/ROLETE.mov"), FER=P("source/FERIADO.mov"),
           E4K=HIST + "HOJE_E.mov", TROP=HIST + "HOJE_B.mov", FERF=HIST + "HOJE_G.mov")
OUT = P("../../entrega/guerreirosgrill_ifood_whatsapp_v2.mp4")
ACC = (214, 164, 54); WHITE = (255, 255, 255); BGc = np.array([20, 16, 12], np.float32)
F_BOLD = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"; F_SEMI = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
F_IT = P("../tour3/assets/fonts/Montserrat-Italic.ttf")
FILL = f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H}"
GRADE = "eq=contrast=1.07:saturation=1.0"
CROP = {"ROL": "crop=iw*0.75:ih*0.74:iw*0.125:0,"}

# ---- linha do tempo -----------------------------------------------------------------------------
# (t0, t1, fonte, início na fonte, tipo, extra)   tipo: A (fala na tela) | B (b-roll com rampa)
V = [
    (0.00, 3.60, "HOOK", 0.25, "A", dict(punch=(0.70, 1.15, 0.25))),
    (3.60, 4.80, "E4K", 0.4, "B", {}), (4.80, 6.05, "TROP", 18.4, "B", {}),
    (6.05, 7.30, "FER", 0.0, "B", {}), (7.30, 8.70, "ROL", 2.55, "B", {}), (8.70, 10.00, "GUAR", 0.0, "B", {}),
    (10.00, 15.25, "L3", 0.75, "A", dict(punch=(1.55, 1.12, 0.3))),
    (15.25, 16.50, "FERF", 15.6, "B", {}), (16.50, 17.75, "FERF", 7.0, "B", {}),
    (17.75, 20.70, "CTA", 0.75, "A", dict(push=(1.0, 1.08))),
]
SEARCH0, T_END = 20.70, 25.40
# voz: (fonte, início, fim, posição)
VOZ = [("HOOK", 0.25, 3.85, 0.00),
       ("VO", 0.35, 2.80, 3.60), ("VO", 4.00, 4.35, 6.10), ("VO", 4.90, 6.15, 7.35), ("VO", 6.95, 8.10, 8.75),
       ("L3", 0.75, 6.00, 10.00), ("CTA", 0.75, 3.65, 17.75), ("CTA", 4.85, 6.35, 20.80)]
# frases (texto do roteiro) com o trecho falado no vídeo (início, fim); *palavra = destaque
FRASES = [
    ("*Cuiabá,", 0.05, 0.45), ("chegou a *novidade.", 0.70, 1.55), ("O *Guerreiro's agora está no *iFood.", 2.10, 3.50),
    ("A gente começa com o que o povo já conhece:", 3.65, 6.05),
    ("*costela,", 6.10, 6.45), ("*frango *assado", 7.35, 8.60), ("e as *guarnições.", 8.75, 9.90),
    ("Mas isso é só o *começo.", 10.10, 11.00), ("Nossa força sempre foi a *variedade de *carnes,", 11.55, 13.75),
    ("e ela vai chegar no *iFood.", 14.20, 15.10),
    ("*Sábado e *domingo,", 17.85, 19.20), ("pelo *iFood.", 19.40, 20.60), ("Procure *Guerreiro's *Grill.", 20.80, 22.25),
]
EMBREVE = (15.30, 17.70)

def eo(t): t = min(1, max(0, t)); return 1 - (1 - t) ** 3
def back(t, s=1.8): t = min(1, max(0, t)) - 1; return 1 + (s + 1) * t ** 3 + s * t ** 2
def sil(w): return max(1, len(re.findall(r"[aeiouáéíóúâêôãõà]+", w.lower())))

# ---- palavras com tempo (proporcional às sílabas dentro do trecho falado) -----------------------
WORDS = []   # (texto, destaque, t_in, grupo)
gid = 0
for txt, a, b in FRASES:
    ws = txt.split(); ss = [sil(w) for w in ws]; tot = sum(ss); acc = 0
    grp = []
    for w, s in zip(ws, ss):
        if len(grp) == 3 or (grp and grp[-1][0].endswith((",", ".", ":"))): gid += 1; grp = []
        hl = w.startswith("*"); w = w.lstrip("*")
        item = (w, hl, a + (b - a) * acc / tot, gid); WORDS.append(item); grp.append(item); acc += s
    gid += 1
GROUP_END = {}
for i, (w, hl, t, g) in enumerate(WORDS):
    nxt = next((x[2] for x in WORDS[i + 1:] if x[3] != g), None)
    GROUP_END[g] = min(t + 1.6, nxt) if nxt else t + 1.2
    GROUP_END[g] = max(GROUP_END[g], t + 0.35)

_cache = {}
def wlayer(w, hl):
    k = (w, hl)
    if k in _cache: return _cache[k]
    f = ImageFont.truetype(F_BOLD, 92) if hl else ImageFont.truetype(F_IT, 70)
    if not hl: f.set_variation_by_axes([400])
    txt = w.upper() if hl else w
    a, d = f.getmetrics(); pad = 34; tw = int(f.getlength(txt)) + 2
    m = Image.new("L", (tw + 2 * pad, a + d + 2 * pad), 0); ImageDraw.Draw(m).text((pad, pad), txt, font=f, fill=255)
    A = np.array(m, np.float32) / 255
    sh = np.maximum(np.roll(cv2.GaussianBlur(A, (0, 0), 10), 4, axis=0) * 0.75, cv2.GaussianBlur(cv2.dilate(A, np.ones((5, 5), np.uint8)), (0, 0), 2) * 0.55)
    L = dict(A=A, S=sh, rgb=np.array(ACC if hl else WHITE, np.float32), w=tw, pad=pad, asc=a); _cache[k] = L; return L

def comp(f, L, x, yb, al, sc=1.0):
    A, S = L["A"], L["S"]
    if abs(sc - 1) > 1e-3: A = cv2.resize(A, None, fx=sc, fy=sc); S = cv2.resize(S, None, fx=sc, fy=sc)
    h, w = A.shape; x0 = int(x - L["pad"] * sc); y0 = int(yb - (L["asc"] + L["pad"]) * sc)
    xa, ya, xb, yb2 = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if xb <= xa or yb2 <= ya: return
    sl = (slice(ya - y0, yb2 - y0), slice(xa - x0, xb - x0)); reg = f[ya:yb2, xa:xb]
    reg *= (1 - S[sl] * al)[..., None]; a = (A[sl] * al)[..., None]; reg[:] = reg * (1 - a) + L["rgb"] * a

def draw_caps(f, t, y=1190):
    if SEARCH0 + 0.2 < t or EMBREVE[0] - 0.05 <= t <= EMBREVE[1]: return
    act = [x for x in WORDS if x[2] - 0.001 <= t < GROUP_END[x[3]] + 0.15]
    if not act: return
    g = act[-1][3]; ws = [x for x in WORDS if x[3] == g]
    sp = 18; widths = [wlayer(w, hl)["w"] for w, hl, _, _ in ws]; tot = sum(widths) + sp * (len(ws) - 1)
    sc_all = min(1.0, 940 / tot); x = W / 2 - tot * sc_all / 2
    out = 1 - eo((t - GROUP_END[g]) / 0.15) if t > GROUP_END[g] else 1
    for (w, hl, ti, _), wd in zip(ws, widths):
        L = wlayer(w, hl)
        if t >= ti:
            k = (t - ti) / 0.12; s = sc_all * (1.25 - 0.25 * back(k)) if hl else sc_all * (1.10 - 0.10 * eo(k))
            al = min(1, k * 1.5) * out; yb = y + (0 if hl else -6)
            comp(f, L, x + wd * sc_all / 2 - wd * s / 2, yb + (1 - eo(k)) * 14, al, s)
        x += (wd + sp) * sc_all

# títulos grandes (gancho e "em breve")
def big(text, font, size, color, track=0):
    f = ImageFont.truetype(font, size); a, d = f.getmetrics(); pad = 40
    tw = int(sum(f.getlength(c) for c in text) + track * (len(text) - 1)) + 2
    m = Image.new("L", (tw + 2 * pad, a + d + 2 * pad), 0); dr = ImageDraw.Draw(m); x = pad
    for c in text: dr.text((x, pad), c, font=f, fill=255); x += f.getlength(c) + track
    A = np.array(m, np.float32) / 255
    sh = np.maximum(np.roll(cv2.GaussianBlur(A, (0, 0), 14), 6, axis=0) * 0.8, cv2.GaussianBlur(cv2.dilate(A, np.ones((7, 7), np.uint8)), (0, 0), 2) * 0.6)
    return dict(A=A, S=sh, rgb=np.array(color, np.float32), w=tw, pad=pad, asc=a)
T_HOOK = [big("O GUERREIRO'S", F_BOLD, 104, WHITE, -2), big("CHEGOU NO", F_BOLD, 104, WHITE, -2), big("IFOOD", F_BOLD, 150, ACC, -3)]
T_EB = [big("EM BREVE", F_BOLD, 130, ACC, 4)]; T_EB2 = wlayer("mais cortes", False)

lg = Image.open(P("../historia/assets/logo_clean.png")).convert("RGBA")
def logo_arr(w):
    h = int(lg.height * w / lg.width); return np.array(lg.resize((w, h), Image.LANCZOS), np.float32)
LOGO_S, LOGO_M = logo_arr(120), logo_arr(170)
def paste(f, L, x0, y0, al):
    h, w = L.shape[:2]; xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if xb <= xa or yb <= ya: return
    s = L[ya - y0:yb - y0, xa - x0:xb - x0]; a = s[..., 3:4] / 255 * al; reg = f[ya:yb, xa:xb]; reg[:] = reg * (1 - a) + s[..., :3] * a

# ---- vídeo --------------------------------------------------------------------------------------
def decode(src, st, n, fps=FPS):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{st:.3f}", "-i", SRC[src], "-frames:v", str(n), "-vf",
                          f"fps={fps},{CROP.get(src, '')}{FILL},{GRADE},format=rgb24", "-an", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    fr = list(np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3))
    while len(fr) < n: fr.append(fr[-1])
    return fr[:n]

def ramp_frames(src, st, n):
    """rampa: começa 2,5x e desacelera para 1x (sensação de câmera rápida)."""
    pos = []; p = 0.0
    for j in range(n):
        k = j / max(1, n - 1); sp = 2.5 - 1.5 * eo(min(1, k / 0.35)); pos.append(p); p += sp
    need = int(math.ceil(p)) + 2; src_fr = decode(src, st, need)
    return [src_fr[min(len(src_fr) - 1, int(round(q)))] for q in pos]

KH = {}
def hblur(f, k):
    if k < 3: return f
    if k not in KH: K = np.zeros((1, k), np.float32); K[:] = 1 / k; KH[k] = K
    return cv2.filter2D(f, -1, KH[k], borderType=cv2.BORDER_REFLECT)

def zoom(f, z, cy=0.42):
    if abs(z - 1) < 1e-3: return f
    return cv2.warpAffine(f, cv2.getRotationMatrix2D((W / 2, H * cy), 0, z), (W, H), borderMode=cv2.BORDER_REFLECT)

os.makedirs(P("work"), exist_ok=True)
enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                        "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", P("work/video2.mp4")], stdin=subprocess.PIPE)
NF = int(round(T_END * FPS)); CUTS = [int(round(s[0] * FPS)) for s in V[1:]] + [int(round(SEARCH0 * FPS))]
yy_, xx_ = np.mgrid[0:H, 0:W]; VIG = (1 - 0.22 * np.clip((np.hypot((xx_ - W / 2) / W, (yy_ - H / 2) / H) - 0.25) * 1.6, 0, 1))[..., None].astype(np.float32)
g = 0; last = None
for t0, t1, src, st, kind, ex in V:
    n = int(round(t1 * FPS)) - int(round(t0 * FPS))
    frs = ramp_frames(src, st, n) if kind == "B" else decode(src, st, n)
    for j, fr in enumerate(frs):
        t = g / FPS; tr = j / FPS; f = fr.astype(np.float32)
        if "punch" in ex:
            a, z1, d = ex["punch"]; z = 1 + (z1 - 1) * eo((tr - a) / d) if tr > a else 1.0; f = zoom(f, z)
            if a <= tr < a + 0.2: sh = int(10 * (1 - (tr - a) / 0.2)); f = np.roll(f, (sh if j % 2 else -sh), axis=0)   # tremida no impacto
        if "push" in ex: f = zoom(f, ex["push"][0] + (ex["push"][1] - ex["push"][0]) * j / max(1, n - 1))
        # chicote nas trocas: 3 quadros antes / 3 depois com desfoque e deslocamento horizontal
        for c in CUTS:
            d = g - c
            if -3 <= d < 0: s = (4 + d) / 4; f = np.roll(hblur(f, int(90 * s) | 1), int(-160 * s * s), axis=1)
            elif 0 <= d < 3: s = (3 - d) / 3; f = np.roll(hblur(f, int(90 * s) | 1), int(160 * s * s), axis=1)
        f *= VIG
        for fc in (int(round(EMBREVE[0] * FPS)) - 1, ):
            if 0 <= g - fc < 3: f = f * 0.35 + 255 * 0.65 * (1 - (g - fc) / 3)
        if t < 3.4:                                                               # título do gancho
            for i, (L, y) in enumerate(zip(T_HOOK, (360, 470, 640))):
                k = (t - 0.05 - i * 0.18) / 0.14
                if k > 0:
                    out = 1 if t < 3.2 else max(0, (3.4 - t) / 0.2); s = 1.3 - 0.3 * back(k)
                    comp(f, L, W / 2 - L["w"] * s / 2, y, min(1, k) * out, s)
        if EMBREVE[0] <= t <= EMBREVE[1]:
            k = (t - EMBREVE[0]) / 0.15; out = 1 if t < EMBREVE[1] - 0.15 else max(0, (EMBREVE[1] - t) / 0.15)
            L = T_EB[0]; s = 1.3 - 0.3 * back(k); comp(f, L, W / 2 - L["w"] * s / 2, 940, min(1, k) * out, s)
            k2 = (t - EMBREVE[0] - 0.35) / 0.15
            if k2 > 0: comp(f, T_EB2, W / 2 - T_EB2["w"] / 2, 1060, min(1, k2) * out)
        draw_caps(f, t)
        paste(f, LOGO_S, W - 60 - 120, H - 380 - LOGO_S.shape[0], 0.7)
        last = f.copy(); enc.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes()); g += 1

# ---- final: busca animada ("Guerreiro's Grill") e cartão da loja --------------------------------
bg = cv2.resize(cv2.GaussianBlur(cv2.resize(last, (W // 6, H // 6)), (0, 0), 4), (W, H)) * 0.35 + BGc * 0.65
f_q = ImageFont.truetype(F_SEMI, 52); f_n = ImageFont.truetype(F_BOLD, 64); f_s = ImageFont.truetype(F_SEMI, 40)
QUERY = "Guerreiro's Grill"; T_TYPE0, T_TYPE1 = 20.95, 22.15; T_CARD = 22.55
def rr(img, box, r, fill): ImageDraw.Draw(img).rounded_rectangle(box, r, fill=fill)
while g < NF:
    t = g / FPS; k = t - SEARCH0
    f = bg.copy()
    # barra de busca: entra de baixo com mola
    ky = 1 - back(k / 0.35, 1.4); by = int(700 + 500 * ky); al = min(1, k / 0.15)
    bar = Image.new("RGBA", (W, 260), (0, 0, 0, 0)); rr(bar, (70, 60, W - 70, 190), 65, (255, 255, 255, 255))
    d = ImageDraw.Draw(bar); d.ellipse((120, 98, 168, 146), outline=(120, 120, 120, 255), width=7); d.line((160, 140, 182, 162), fill=(120, 120, 120, 255), width=8)
    nchar = int(len(QUERY) * min(1, max(0, (t - T_TYPE0) / (T_TYPE1 - T_TYPE0))))
    q = QUERY[:nchar] if nchar else "Buscar"
    d.text((210, 96), q, font=f_q, fill=(30, 30, 30, 255) if nchar else (150, 150, 150, 255))
    if nchar < len(QUERY) and int(t * 3) % 2 == 0 and t > T_TYPE0 - 0.3:
        cx = 210 + int(f_q.getlength(q if nchar else "")) + 4; d.line((cx, 98, cx, 152), fill=(214, 164, 54, 255), width=4)
    B = np.array(bar, np.float32); sh = cv2.GaussianBlur(B[..., 3] / 255, (0, 0), 18) * 0.5
    reg = f[by:by + 260]; reg *= (1 - np.roll(sh, 10, axis=0) * al)[..., None]; a_ = B[..., 3:4] / 255 * al; reg[:] = reg * (1 - a_) + B[..., :3] * a_
    # cartão da loja
    kc = (t - T_CARD) / 0.4
    if kc > 0:
        card = Image.new("RGBA", (W, 520), (0, 0, 0, 0)); rr(card, (70, 20, W - 70, 480), 48, (255, 255, 255, 255))
        dc = ImageDraw.Draw(card); dc.text((330, 120), "Guerreiro's Grill", font=f_n, fill=(25, 20, 15, 255))
        dc.text((330, 215), "Churrasco raiz", font=f_s, fill=(110, 100, 90, 255))
        rr(card, (330, 300, 330 + int(f_s.getlength("Sábado e domingo")) + 60, 380), 40, (214, 164, 54, 255))
        dc.text((360, 316), "Sábado e domingo", font=f_s, fill=(255, 255, 255, 255))
        C = np.array(card, np.float32); s = 0.85 + 0.15 * back(kc); al2 = min(1, kc * 2)
        C = cv2.resize(C, None, fx=s, fy=s); ch, cw = C.shape[:2]; x0, y0 = W // 2 - cw // 2, 1230 - ch // 2 + int((1 - eo(kc)) * 60)
        shc = cv2.GaussianBlur(C[..., 3] / 255, (0, 0), 22) * 0.55
        xa, ya = max(0, x0), max(0, y0); xb, yb = min(W, x0 + cw), min(H, y0 + ch); sl = (slice(ya - y0, yb - y0), slice(xa - x0, xb - x0))
        reg = f[ya:yb, xa:xb]; reg *= (1 - np.roll(shc, 14, axis=0)[sl] * al2)[..., None]; a_ = C[sl][..., 3:4] / 255 * al2; reg[:] = reg * (1 - a_) + C[sl][..., :3] * a_
        Lm = cv2.resize(LOGO_M, None, fx=s, fy=s); paste(f, Lm, x0 + int(110 * s), y0 + int(95 * s), al2)
    for c in CUTS:
        d_ = g - c
        if 0 <= d_ < 3: s_ = (3 - d_) / 3; f = np.roll(hblur(f, int(90 * s_) | 1), int(160 * s_ * s_), axis=1)
    if 0 <= g - int(round(SEARCH0 * FPS)) < 3: f = f * 0.35 + 255 * 0.65 * (1 - (g - int(round(SEARCH0 * FPS))) / 3)
    fo = (T_END - t) / 0.5
    if fo < 1: f *= max(0, fo)
    enc.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes()); g += 1
enc.stdin.close(); enc.wait()

# ---- áudio --------------------------------------------------------------------------------------
def pcm(f, ss, t, af="highpass=f=90,afftdn=nf=-30,acompressor=threshold=-20dB:ratio=3:attack=10:release=150"):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(ss), "-t", str(t), "-i", f, "-vn", "-ac", "1", "-ar", str(SR), "-af", af, "-f", "s16le", "-"],
                       capture_output=True, check=True).stdout
    return np.frombuffer(r, np.int16).astype(np.float32) / 32768
N = int(T_END * SR); rms = lambda v: np.sqrt(np.mean(v ** 2)) + 1e-9
voz = np.zeros(N, np.float32)
for src, a, b, pos in VOZ:
    x = pcm(SRC[src], a, b - a); fd = int(0.02 * SR); x[:fd] *= np.linspace(0, 1, fd); x[-fd:] *= np.linspace(1, 0, fd)
    p0 = int(pos * SR); m = min(len(x), N - p0); voz[p0:p0 + m] += x[:m]
voz *= 0.25 / rms(voz[np.abs(voz) > 1e-4])
mus = pcm(P("../tres/assets/trilha-gaucha-loop.wav"), 15, T_END + 1, "anull")[:N]; mus = np.pad(mus, (0, N - len(mus))) / 1.0
mus = mus / rms(mus) * 0.25
env = np.full(N, 10 ** (-21 / 20)); env[int(SEARCH0 * SR):] = 10 ** (-13 / 20); env = np.convolve(env, np.ones(int(0.3 * SR)) / int(0.3 * SR), "same")
def sfx(name):
    x = pcm(P(f"sfx/{name}.wav"), 0, 10, "anull"); return x / (np.abs(x).max() + 1e-9)
S_ = {k: sfx(k) for k in ("whooshfast", "whooshlow", "riser", "digits", "lens", "shutter", "paper", "film")}
fx = np.zeros(N, np.float32)
def add(name, t, gain, maxlen=None):
    x = S_[name][: int(maxlen * SR) if maxlen else None]; p0 = int(t * SR)
    if p0 < 0: x = x[-p0:]; p0 = 0
    m = min(len(x), N - p0); fx[p0:p0 + m] += x[:m] * gain
# impacto grave sintetizado (sub) para gancho e cartão
tt = np.arange(int(1.0 * SR)) / SR; BOOM = (np.sin(2 * np.pi * (48 + 50 * np.exp(-tt * 14)) * tt) * np.exp(-tt * 3.8)).astype(np.float32)
def boom(t, gain):
    p0 = int(t * SR); m = min(len(BOOM), N - p0); fx[p0:p0 + m] += BOOM[:m] * gain
boom(0.0, 0.55); boom(0.70, 0.45); add("lens", 0.68, 0.30)                        # gancho: impacto + zoom
for i in range(3): add("paper", 0.05 + i * 0.18, 0.22, 0.25)                      # entrada das linhas do título
for c in [s[0] for s in V[1:]]: add("whooshfast", c - 0.12, 0.40)                # whoosh em cada corte
add("whooshlow", 3.60 - 0.25, 0.35); add("lens", 11.55, 0.30); boom(11.55, 0.30)  # 2º zoom
for w, hl, ti, _ in WORDS:
    if hl and ti < SEARCH0: add("shutter", ti, 0.10, 0.08)                         # clique leve nas palavras de destaque
add("riser", 17.75 - 4.0, 0.30); boom(EMBREVE[0], 0.35)                           # "em breve" + subida pro final
add("whooshlow", SEARCH0 - 0.3, 0.40)                                             # entrada da busca
for k in range(len(QUERY)):
    add("digits", T_TYPE0 + (T_TYPE1 - T_TYPE0) * k / len(QUERY), 0.12, 0.06)    # digitação
boom(T_CARD, 0.5); add("film", T_CARD, 0.18, 0.5)
siz = np.zeros(N, np.float32)
ch = pcm(P("../../entrega/guerreiros-FLORAIS-QUI-A-DOM.mp4"), 11.6, 7.5, "anull")
for a, b in ((3.6, 10.0), (15.25, 17.75)):
    i0, i1 = int(a * SR), int(b * SR); s = np.resize(ch, i1 - i0); s = s / rms(s) * 0.25 * 10 ** (-24 / 20)
    r_ = np.minimum(1, np.minimum(np.arange(i1 - i0), (i1 - i0) - np.arange(i1 - i0)) / (0.15 * SR)); siz[i0:i1] += s * r_
mix = voz + mus * env + siz + fx
fo = int(0.5 * SR); mix[-fo:] *= np.linspace(1, 0, fo)
wavfile.write(P("work/audio2.wav"), SR, (np.clip(mix, -1, 1) * 32767).astype(np.int16))
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", P("work/video2.mp4"), "-i", P("work/audio2.wav"), "-map", "0:v", "-map", "1:a",
                "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-b:v", "8M", "-maxrate", "10M", "-bufsize", "16M", "-pix_fmt", "yuv420p",
                "-af", "loudnorm=I=-13:TP=-2:LRA=9,alimiter=limit=0.84:level=disabled", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                "-movflags", "+faststart", OUT], check=True)
print(OUT, T_END)
