#!/usr/bin/env python3
"""Guerreiro's Grill no iFood — WhatsApp v3. Falas inteiras (sem cortar nada dentro da fala), legenda palavra por
palavra com a transcrição enviada, só os B-rolls enviados, sem busca animada, sem chiado de fundo.   python3 render3.py
"""
import os, subprocess, math, re
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
from scipy.io import wavfile
from scipy.signal import butter, sosfilt
ROOT = os.path.dirname(os.path.abspath(__file__)); P = lambda p: os.path.join(ROOT, p)
W, H, FPS, SR = 1080, 1920, 30, 48000
SRC = dict(HOOK=P("source/B2488.mov"), VO=P("source/FALA.mov"), L1=P("source/B2496b.mov"), L2=P("source/B2496a.mov"),
           GUAR=P("source/G04a.mov"), ROL=P("source/ROLETE.mov"), FER=P("source/FERIADO.mov"))
OUT = P("../../entrega/guerreirosgrill_ifood_whatsapp_v3.mp4")
ACC = (214, 164, 54); WHITE = (255, 255, 255); BGc = np.array([20, 16, 12], np.float32)
F_BOLD = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"; F_SEMI = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
F_IT = P("../tour3/assets/fonts/Montserrat-Italic.ttf")
FILL = f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H}"
GRADE = "eq=contrast=1.06:saturation=1.0"
CROP = {"ROL": "crop=iw*0.75:ih*0.74:iw*0.125:0,"}          # tira a legenda queimada do vídeo do rolete

# ---- falas (inteiras) e transcrição ------------------------------------------------------------
INTRO = 0.0
LAG = 0.12                                             # legenda entra no instante em que a palavra soa
CL = [("HOOK", 0.00, 4.05), ("VO", 0.25, 8.40), ("L1", 0.55, 8.56), ("L2", 0.00, 7.60)]   # L1 e L2: o mesmo take, emendados
T0 = {}; t = INTRO
for k, a, b in CL: T0[k] = t; t += b - a
END0 = t; T_END = END0 + 2.0
TXT = {
    "HOOK": "*Cuiabá, chegou *novidade, hein! *Guerreiro's *Grill agora está no *iFood.",
    "VO": "Vamos iniciar no *iFood com o que você já conhece, a nossa *costela e o nosso *frango no *rolete e todas as *guarnições.",
    "L1": "*Em *breve, pessoal, no *iFood não só a *costela e o *frango, também teremos todos os *cortes do *Guerreiro's *Grill. Então, você vai",
    "L2": "poder pedir no *iFood, aquela *panceta, aquele *joelho, aquela *maminha com *bacon, todo o portfólio do *Guerreiro's *Grill. Um *abraço!",
}
def sil(w): return max(1, len(re.findall(r"[aeiouáéíóúâêôãõà]+", w.lower())))
def pcm(f, ss=0, t=None, af="anull", sr=SR, ch=1):
    cmd = ["ffmpeg", "-v", "error", "-ss", str(ss)] + (["-t", str(t)] if t else []) + ["-i", f, "-vn", "-ac", str(ch), "-ar", str(sr), "-af", af, "-f", "s16le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.int16).astype(np.float32) / 32768

def word_times(src, a, b, text):
    """distribui as palavras pelo tempo em que há voz (pula os silêncios), proporcional às sílabas."""
    x = pcm(SRC[src], a, b - a, sr=16000); bb = sosfilt(butter(4, [250, 3500], btype="band", fs=16000, output="sos"), x)
    hop = 160; e = np.array([10 * np.log10(np.mean(bb[i:i + 320] ** 2) + 1e-12) for i in range(0, len(bb) - 320, hop)])
    e = np.convolve(e, np.ones(5) / 5, "same"); thr = np.median(e) + 6.0; v = (e > thr).astype(float)
    cum = np.concatenate([[0], np.cumsum(v)]); tot_v = cum[-1]
    ws = text.split(); ss = [sil(w) for w in ws]; tot = sum(ss); out = []; acc = 0
    for w, s in zip(ws, ss):
        target = tot_v * acc / tot; i = int(np.searchsorted(cum, target + 0.5)); out.append((w, i * hop / 16000)); acc += s
    return out

def hook_times():
    """gancho: frases nos trechos de voz medidos (0,30 / 0,95–1,80 / 2,35–3,75 s do IMG_2488)."""
    out = []
    for txt, a, b in (("*Cuiabá,", 0.30, 0.70), ("chegou *novidade, hein!", 0.95, 1.80), ("*Guerreiro's *Grill agora está no *iFood.", 2.35, 3.75)):
        ws = txt.split(); ss = [sil(w) for w in ws]; tot = sum(ss); acc = 0
        for w, s_ in zip(ws, ss): out.append((w, a + (b - a) * acc / tot - HOOK_A)); acc += s_
    return out
HOOK_A = 0.0
WORDS = []; gid = 0          # (texto, destaque, t_in, grupo)
for k, a, b in CL:
    grp = 0
    for w, tw in (hook_times() if k == "HOOK" else word_times(k, a, b, TXT[k])):
        hl = w.startswith("*"); w = w.lstrip("*")
        if grp == 3 or (WORDS and grp and WORDS[-1][0].endswith((",", ".", "!", ":"))): gid += 1; grp = 0
        WORDS.append((w, hl, T0[k] + tw + LAG, gid)); grp += 1
    gid += 1
GEND = {}
for i, (w, hl, tt, g) in enumerate(WORDS):
    nxt = next((x[2] for x in WORDS[i + 1:] if x[3] != g), None)
    GEND[g] = max(tt + 0.35, min(tt + 1.5, nxt) if nxt else tt + 1.0)
def wt(clip, word):
    """tempo (no vídeo) da 1ª palavra que começa com `word` dentro de um trecho."""
    a0 = T0[clip]; b0 = a0 + [b - a for k, a, b in CL if k == clip][0]
    return next(x[2] for x in WORDS if a0 <= x[2] < b0 and x[0].lower().startswith(word))

# ---- B-roll da narração (só os vídeos enviados) ------------------------------------------------
tc, tf, tg = wt("VO", "costela") - 0.12, wt("VO", "frango") - 0.12, wt("VO", "guarni") - 0.12
VO0, VO1 = T0["VO"], T0["L1"]
mid = VO0 + (tc - VO0) * 0.62
BROLL = [(VO0, mid, "ROL", 2.55, 2.0), (mid, tc, "ROL", 4.65, 0.95),   # "Vamos iniciar no iFood…": frango na grelha + corte
         (tc, tf, "FER", 0.0, 1.88),                                  # "a nossa costela"
         (tf, tg, "ROL", 0.0, 2.4),                                   # "e o nosso frango no rolete"
         (tg, VO1, "GUAR", 0.0, 3.85)]                                # "e todas as guarnições"  (último número = trecho útil)
SRC_LEN = {"FER": 1.88, "GUAR": 3.85, "ROL": 5.6}

# ---- texto ------------------------------------------------------------------------------------
def eo(t): t = min(1, max(0, t)); return 1 - (1 - t) ** 3
def back(t, s=1.8): t = min(1, max(0, t)) - 1; return 1 + (s + 1) * t ** 3 + s * t ** 2
_cache = {}
def wlayer(w, hl):
    if (w, hl) in _cache: return _cache[(w, hl)]
    f = ImageFont.truetype(F_BOLD, 96) if hl else ImageFont.truetype(F_IT, 72)
    if not hl: f.set_variation_by_axes([500])
    txt = w.upper() if hl else w; a, d = f.getmetrics(); pad = 34; tw = int(f.getlength(txt)) + 2
    m = Image.new("L", (tw + 2 * pad, a + d + 2 * pad), 0); ImageDraw.Draw(m).text((pad, pad), txt, font=f, fill=255)
    A = np.array(m, np.float32) / 255
    S = np.maximum(np.roll(cv2.GaussianBlur(A, (0, 0), 10), 4, axis=0) * 0.8, cv2.GaussianBlur(cv2.dilate(A, np.ones((7, 7), np.uint8)), (0, 0), 2) * 0.7)
    L = dict(A=A, S=S, rgb=np.array(ACC if hl else WHITE, np.float32), w=tw, pad=pad, asc=a); _cache[(w, hl)] = L; return L
def comp(f, L, x, yb, al, sc=1.0):
    A, S = L["A"], L["S"]
    if abs(sc - 1) > 1e-3: A = cv2.resize(A, None, fx=sc, fy=sc); S = cv2.resize(S, None, fx=sc, fy=sc)
    h, w = A.shape; x0 = int(x - L["pad"] * sc); y0 = int(yb - (L["asc"] + L["pad"]) * sc)
    xa, ya, xb, yb2 = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if xb <= xa or yb2 <= ya: return
    sl = (slice(ya - y0, yb2 - y0), slice(xa - x0, xb - x0)); reg = f[ya:yb2, xa:xb]
    reg *= (1 - S[sl] * al)[..., None]; a = (A[sl] * al)[..., None]; reg[:] = reg * (1 - a) + L["rgb"] * a
def draw_caps(f, t, y=1210):
    act = [x for x in WORDS if x[2] - 0.001 <= t < GEND[x[3]] + 0.12]
    if not act or t >= END0: return
    g = act[-1][3]; ws = [x for x in WORDS if x[3] == g]
    sp = 20; wd = [wlayer(w, hl)["w"] for w, hl, _, _ in ws]; tot = sum(wd) + sp * (len(ws) - 1)
    sca = min(1.0, 950 / tot); x = W / 2 - tot * sca / 2; out = 1 - eo((t - GEND[g]) / 0.12) if t > GEND[g] else 1
    for (w, hl, ti, _), d in zip(ws, wd):
        if t >= ti:
            k = (t - ti) / 0.12; s = sca * ((1.3 - 0.3 * back(k)) if hl else (1.1 - 0.1 * eo(k)))
            comp(f, wlayer(w, hl), x + d * sca / 2 - d * s / 2, y + (1 - eo(k)) * 16 - (0 if hl else 6), min(1, k * 1.5) * out, s)
        x += (d + sp) * sca

lg = Image.open(P("../historia/assets/logo_clean.png")).convert("RGBA")
def logo_arr(w): h = int(lg.height * w / lg.width); return np.array(lg.resize((w, h), Image.LANCZOS), np.float32)
LOGO_S, LOGO_B = logo_arr(120), logo_arr(460)
def paste(f, L, x0, y0, al):
    h, w = L.shape[:2]; xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if xb <= xa or yb <= ya: return
    s = L[ya - y0:yb - y0, xa - x0:xb - x0]; a = s[..., 3:4] / 255 * al; reg = f[ya:yb, xa:xb]; reg[:] = reg * (1 - a) + s[..., :3] * a
def big(text, font, size, color):
    f = ImageFont.truetype(font, size); a, d = f.getmetrics(); pad = 40; tw = int(f.getlength(text)) + 2
    m = Image.new("L", (tw + 2 * pad, a + d + 2 * pad), 0); ImageDraw.Draw(m).text((pad, pad), text, font=f, fill=255)
    A = np.array(m, np.float32) / 255
    S = np.maximum(np.roll(cv2.GaussianBlur(A, (0, 0), 12), 5, axis=0) * 0.8, cv2.GaussianBlur(cv2.dilate(A, np.ones((7, 7), np.uint8)), (0, 0), 2) * 0.6)
    return dict(A=A, S=S, rgb=np.array(color, np.float32), w=tw, pad=pad, asc=a)
END_T = [big("Sábado e domingo,", F_BOLD, 80, WHITE), big("pelo iFood", F_BOLD, 112, ACC)]

# ---- vídeo ------------------------------------------------------------------------------------
def decode(src, st, n, speed=1.0):
    need = int(math.ceil(n * speed)) + 2
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{st:.3f}", "-i", SRC[src], "-frames:v", str(need), "-vf",
                          f"fps={FPS},{CROP.get(src, '')}{FILL},{GRADE},format=rgb24", "-an", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    fr = list(np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3))
    while len(fr) < need: fr.append(fr[-1])
    return [fr[min(len(fr) - 1, int(j * speed))] for j in range(n)]
KH = {}
def hblur(f, k):
    if k < 3: return f
    if k not in KH: KH[k] = np.full((1, k), 1 / k, np.float32)
    return cv2.filter2D(f, -1, KH[k], borderType=cv2.BORDER_REFLECT)
def zoom(f, z, cy=0.42):
    return f if abs(z - 1) < 1e-3 else cv2.warpAffine(f, cv2.getRotationMatrix2D((W / 2, H * cy), 0, z), (W, H), borderMode=cv2.BORDER_REFLECT)
fi = lambda t: int(round(t * FPS))

# plano de quadros: (t0, t1, fonte, início, velocidade, zooms)
PLAN = []
PLAN.append((T0["HOOK"], T0["VO"], "HOOK", 0.0, 1.0))
for a, b, src, st, avail in BROLL:
    PLAN.append((a, b, src, st, max(0.6, min(1.0, avail / (b - a)))))
PLAN.append((T0["L1"], T0["L2"], "L1", 0.55, 1.0)); PLAN.append((T0["L2"], END0, "L2", 0.0, 1.0))
PUNCH = [(T0["HOOK"] + 0.30, 1.10, 0.18), (wt("HOOK", "chegou"), 1.18, 0.22), (wt("L1", "em"), 1.12, 0.25),
         (wt("L1", "cortes"), 1.20, 0.22), (wt("L2", "panceta"), 1.10, 0.2), (wt("L2", "abraço"), 1.16, 0.22)]
CUTS = [fi(p[0]) for p in PLAN[1:]] + [fi(END0)]
CUTS = [c for c in CUTS if c not in (fi(T0["L2"]),)]                      # L1→L2 é o mesmo take: sem transição
yy_, xx_ = np.mgrid[0:H, 0:W]; VIG = (1 - 0.22 * np.clip((np.hypot((xx_ - W / 2) / W, (yy_ - H / 2) / H) - 0.25) * 1.6, 0, 1))[..., None].astype(np.float32)

os.makedirs(P("work"), exist_ok=True)
enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                        "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", P("work/video3.mp4")], stdin=subprocess.PIPE)
g = 0; last = None
for t0, t1, src, st, spd in PLAN:
    n = fi(t1) - fi(t0); frs = decode(src, st, n, spd)
    for j, fr in enumerate(frs):
        t = g / FPS; f = fr.astype(np.float32)
        if src in ("HOOK", "L1", "L2"):
            z = 1.0
            if src == "L2": z = 1.0 + 0.06 * (t - T0["L2"]) / (END0 - T0["L2"])          # aproximação lenta
            for pt, pz, pd in PUNCH:
                if t0 <= pt < t1 and t >= pt:
                    z *= 1 + (pz - 1) * eo((t - pt) / pd) * (1 if t < pt + 1.4 else max(0, 1 - (t - pt - 1.4) / 0.25))
                if pt <= t < pt + 0.16 and t0 <= pt < t1: f = np.roll(f, int(12 * (1 - (t - pt) / 0.16)) * (1 if g % 2 else -1), axis=0)
            f = zoom(f, z)
        for c in CUTS:                                                            # chicote nas trocas
            d = g - c
            if -3 <= d < 0: s = (4 + d) / 4; f = np.roll(hblur(f, int(90 * s) | 1), int(-170 * s * s), axis=1)
            elif 0 <= d < 3: s = (3 - d) / 3; f = np.roll(hblur(f, int(90 * s) | 1), int(170 * s * s), axis=1)
        if t < INTRO and g % 5 == 0: f = f * 0.4 + 255 * 0.6                     # flash em cada plano da abertura
        f *= VIG
        draw_caps(f, t)
        paste(f, LOGO_S, W - 60 - 120, H - 380 - LOGO_S.shape[0], 0.7)
        last = f.copy(); enc.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes()); g += 1
# cartão final
bg = cv2.resize(cv2.GaussianBlur(cv2.resize(last, (W // 6, H // 6)), (0, 0), 4), (W, H)) * 0.30 + BGc * 0.70
NF = fi(T_END)
while g < NF:
    t = g / FPS; k = t - END0; f = bg.copy()
    s = 0.88 + 0.12 * back(k / 0.3); Lg = cv2.resize(LOGO_B, None, fx=s, fy=s); paste(f, Lg, W // 2 - Lg.shape[1] // 2, 700 - Lg.shape[0] // 2, min(1, k / 0.12))
    for i, (L, y, dl) in enumerate(zip(END_T, (1130, 1260), (0.25, 0.4))):
        kk = (k - dl) / 0.14
        if kk > 0: ss = 1.25 - 0.25 * back(kk); comp(f, L, W / 2 - L["w"] * ss / 2, y, min(1, kk), ss)
    if 0 <= g - fi(END0) < 3: f = f * 0.35 + 255 * 0.65 * (1 - (g - fi(END0)) / 3)
    fo = (T_END - t) / 0.4
    if fo < 1: f *= max(0, fo)
    enc.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes()); g += 1
enc.stdin.close(); enc.wait()

# ---- áudio: voz limpa (sem redutor de ruído), música baixa, efeitos. Sem chiado de fundo. ----
N = int(T_END * SR); rms = lambda v: np.sqrt(np.mean(v ** 2)) + 1e-9
voz = np.zeros(N, np.float32)
for k, a, b in CL:
    src = k if k in ("HOOK", "VO", "L1", "L2") else k
    af = "highpass=f=80,acompressor=threshold=-22dB:ratio=2.5:attack=15:release=200"
    if k == "VO":   # narração gravada sem lapela (som de banheiro): tira o "oco" e corta a cauda de eco entre as palavras
        af = ("highpass=f=120,equalizer=f=320:t=q:w=1.1:g=-6,equalizer=f=650:t=q:w=1.4:g=-3,equalizer=f=3200:t=q:w=1.4:g=3,"
              "agate=threshold=0.025:ratio=4:attack=4:release=90:range=0.25,acompressor=threshold=-22dB:ratio=3:attack=10:release=150")
    x = pcm(SRC[src], a, b - a, af=af)
    fd = int(0.015 * SR); x[:fd] *= np.linspace(0, 1, fd); x[-fd:] *= np.linspace(1, 0, fd)
    p0 = int(T0[k] * SR); m = min(len(x), N - p0); voz[p0:p0 + m] += x[:m]
voz *= 0.25 / rms(voz[np.abs(voz) > 2e-3])
mus = pcm(P("../tres/assets/trilha-gaucha-loop.wav"), 15, T_END + 1)[:N]; mus = np.pad(mus, (0, N - len(mus))); mus = mus / rms(mus) * 0.25
env = np.full(N, 10 ** (-23 / 20)); env[int(END0 * SR):] = 10 ** (-12 / 20); env = np.convolve(env, np.ones(int(0.3 * SR)) / int(0.3 * SR), "same")
def sfx(name): x = pcm(P(f"sfx/{name}.wav")); return x / (np.abs(x).max() + 1e-9)
S_ = {k: sfx(k) for k in ("whooshfast", "whooshlow", "riser", "lens", "film")}
fx = np.zeros(N, np.float32)
def add(name, t, gain, maxlen=None):
    x = S_[name][: int(maxlen * SR) if maxlen else None]; p0 = int(t * SR)
    if p0 < 0: x = x[-p0:]; p0 = 0
    m = max(0, min(len(x), N - p0)); fx[p0:p0 + m] += x[:m] * gain
tt = np.arange(int(1.0 * SR)) / SR; BOOM = (np.sin(2 * np.pi * (48 + 50 * np.exp(-tt * 14)) * tt) * np.exp(-tt * 3.8)).astype(np.float32)
def boom(t, gain): p0 = int(t * SR); m = min(len(BOOM), N - p0); fx[p0:p0 + m] += BOOM[:m] * gain
boom(0.0, 0.45)
for pt, pz, pd in PUNCH: boom(pt, 0.30); add("lens", pt, 0.22)                   # impacto em cada zoom
for c in [p[0] for p in PLAN[1:]] + [END0]:
    if abs(c - T0["L2"]) > 0.01: add("whooshfast", c - 0.12, 0.35)               # whoosh nos cortes
for w, hl, ti, _ in WORDS:
    if hl: add("lens", ti, 0.07, 0.07)                                             # clique leve nas palavras de destaque
add("riser", END0 - 4.0, 0.22); boom(END0, 0.5); add("film", END0, 0.15, 0.5)
# música gaúcha enviada pelo cliente: trecho cheio 7,2–22,0 s em loop com cruzamento, por baixo da voz
seg = pcm(P("source/MUSICA_GAUCHA.mp4"), 7.2, 14.8); xf = int(0.8 * SR); mus = np.zeros(N, np.float32); pos = 0
while pos < N:
    x = seg.copy(); x[:xf] *= np.linspace(0, 1, xf) if pos else 1; x[-xf:] *= np.linspace(1, 0, xf)
    m = min(len(x), N - pos); mus[pos:pos + m] += x[:m]; pos += len(x) - xf
mus = mus / rms(mus) * 0.25
env = np.full(N, 10 ** (-17 / 20)); env[int(END0 * SR):] = 10 ** (-9 / 20); env = np.convolve(env, np.ones(int(0.3 * SR)) / int(0.3 * SR), "same")
fi_ = int(0.3 * SR); env[:fi_] *= np.linspace(0, 1, fi_)
mix = voz + mus * env + fx
fo = int(0.4 * SR); mix[-fo:] *= np.linspace(1, 0, fo)
wavfile.write(P("work/audio3.wav"), SR, (np.clip(mix, -1, 1) * 32767).astype(np.int16))
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", P("work/video3.mp4"), "-i", P("work/audio3.wav"), "-map", "0:v", "-map", "1:a",
                "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-b:v", "8M", "-maxrate", "10M", "-bufsize", "16M", "-pix_fmt", "yuv420p",
                "-af", "loudnorm=I=-13:TP=-2:LRA=9,alimiter=limit=0.84:level=disabled", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                "-movflags", "+faststart", OUT], check=True)
for w, hl, ti, g_ in WORDS: print(f"{ti:6.2f} {'*' if hl else ' '}{w}")
print(OUT, round(T_END, 2))
