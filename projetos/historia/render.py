#!/usr/bin/env python3
"""GUERREIRO'S GRILL — "A nossa história" (reel de evolução). 1080x1920, 30 fps CFR.

Cortes na grade de batidas de "Time" (Pink Floyd), medida no trecho de referência (135,5 BPM).
A música NÃO é embutida no arquivo final (direitos autorais): o cliente adiciona pela biblioteca do Instagram.
Gera também uma prévia com o trecho de referência (só para conferir o sincronismo, não postar).

    python3 render.py            -> work/master.mp4 + entregas
"""
import os, subprocess, math, json
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
from scipy.io import wavfile

ROOT = os.path.dirname(os.path.abspath(__file__)); P_ = lambda p: os.path.join(ROOT, p)
W, H, FPS, SR = 1080, 1920, 30, 48000
TITLE = P_("assets/fonts/Montserrat.ttf"); BODY = P_("assets/fonts/Inter-SemiBold.otf")
BRAND = np.array([246, 250, 40], np.float32)           # amarelo do "GRILL" no logo
BRAND_BG = (10, 10, 10)
DATE = "20261122"
OUT = P_(f"../../entrega/guerreiros-grill_historia_{DATE}.mp4")
OUT_PREV = P_(f"../../entrega/guerreiros-grill_historia_{DATE}_COM-MUSICA.mp4")
COVER = P_(f"../../entrega/guerreiros-grill_historia_{DATE}_capa.png")

# ---- grade de batidas -------------------------------------------------------------------------
BPM = 135.5; BEAT = 60 / BPM                            # 0,4428 s
CLIP_PHASE = 0.296                                       # 1ª batida (tempo forte) no trecho de referência
def fb(b): return int(round(b * BEAT * FPS))             # batida -> quadro

S = {k: P_("source/" + v) for k, v in dict(V1="V1.mov", V2="V2.mp4", HB="HOJE_B.mov", HA="HOJE_A.mov", HC="HOJE_C.mp4",
                                            HD="HOJE_D.mov", HE="HOJE_E.mov", HG="HOJE_G.mov", HK="HOJE_K.mov", V3="V3.mov", V4="V4.mov", FA1="FACH1.mov", FA2="FACH2.mov",
                                            MUS="MUSICA_REF.mp4").items()}
FOTO = {i: P_(f"source/F{i}.jpg") for i in range(1, 10)}
CHIADO = P_("../../entrega/guerreiros-FLORAIS-QUI-A-DOM.mp4")
MUS_LEN = 19.0                                           # a música do trecho de referência para em 19 s

FILL = f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H}"
OLD = "hqdn3d=3:3:5:5,"                                  # denoise médio nos vídeos antigos (comprimidos pelo WhatsApp)
SHARP = ",cas=0.55"                                      # nitidez adaptativa depois do upscale lanczos
BASE = ",eq=contrast=1.06,curves=all='0/0 0.6/0.6 1/0.93'"   # contraste +6%, altas −10
VF = {
    "V1": "crop=iw:ih*0.80:0:0," + OLD + FILL + SHARP + BASE,          # corta o logo queimado (canto inferior esq.)
    "V2": "crop=iw:ih*0.80:0:ih*0.20," + OLD + FILL + SHARP + BASE,    # corta o logo queimado (canto superior esq.)
    "HB": FILL + BASE, "HA": FILL + BASE, "HG": FILL + BASE, "HK": FILL + BASE,
    "HE": FILL + BASE,
    "V2a": "crop=461:819:130:332," + OLD + FILL + SHARP + BASE,       # latão mais fechado nas carnes
    "V2f": "crop=480:853:62:367," + OLD + FILL + SHARP + BASE,        # fraldinha gigante na grelha
    "FA1": FILL + ",cas=0.4" + BASE, "FA2": FILL + BASE,
    "V3": FILL + BASE, "V4": "hqdn3d=1:1:3:3," + FILL + ",cas=0.45" + BASE,
    "HD": "crop=iw*0.75:ih*0.74:iw*0.125:0," + FILL + ",cas=0.4" + BASE + ",eq=saturation=0.92",   # corta a legenda queimada
    "HC": "crop=iw:ih*0.68:0:ih*0.32," + FILL + BASE + ",eq=saturation=0.88",   # Florais: corta a legenda queimada e
    "HCf": FILL + BASE + ",eq=saturation=0.88",                                  # tira o excesso de saturação do original
}

# ---- linha do tempo (em batidas) --------------------------------------------------------------
# Música: gravação de "Time" (135,5 BPM). Começa no "And you run and you run…" (voz entra no 2º tempo do compasso,
# 23,838 s da gravação). batida b do vídeo = MUS_S0 + b*BEAT. Versos (sempre no 2º tempo): b0 "And you run", b16 "Racing
# around", b32 "The sun is the same…", b48 "Shorter of breath", b64 "Every year…", b80 "Plans…", b96 "Hanging on…",
# b112 "The time is gone, the song is over" (logo). Tempos fortes em b = 3, 7, 11…
MUS_FILE = P_("source/MUSICA.mp4"); MUS_S0 = 23.395 + BEAT
WM = (734, 422, 1072, 620)                                 # selo @ do Instagram no vídeo da fachada
SEG = [
    (0, 5, "clip", dict(src="V2", t0=0.6, vf="V2a", mem=1)),                       # ABRE NA LATÃO (2024) — "And you run"
    (5, 9, "foto", dict(f=9, mode="cover", focus=(0.5, 0.45), z=(1.0, 1.08), pan=(0.0, -0.02))),      # Fabrício na latão
    (9, 13, "clip", dict(src="V2", t0=38.3, vf="V2f", mem=1)),                     # fraldinha gigante
    (13, 17, "clip", dict(src="V2", t0=8.3, vf="V2", mem=1)),
    (17, 21, "clip", dict(src="V1", t0=0.3, vf="V1", mem=1)),                      # A ALEGRIA DO PAI
    (21, 25, "clip", dict(src="V4", t0=15.0, vf="V4", mem=0.7)),
    (25, 29, "clip", dict(src="V1", t0=13.0, vf="V1", mem=1)),
    (29, 33, "clip", dict(src="V3", t0=8.6, vf="V3", mem=0.7)),
    (33, 37, "clip", dict(src="V4", t0=25.6, vf="V4", mem=0.7)),                   # "The sun is the same…"
    (37, 43, "album", dict(f=5, z=(1.0, 1.08), pan=(0.0, -0.02), rot=-2.0)),       # A FAMÍLIA
    (43, 47, "foto", dict(f=4, mode="cover", focus=(0.50, 0.42), z=(1.08, 1.0), pan=(0.02, 0.0))),   # OS CLIENTES
    (47, 51, "foto", dict(f=8, mode="fit", z=(1.0, 1.08), pan=(-0.03, 0.0))),
    (51, 59, "wall", dict()),
    (59, 63, "foto", dict(f=2, mode="fit", z=(1.0, 1.08), pan=(0.04, 0.0), mem=(1, 0))),             # A VIRADA latão -> inox
    (63, 69, "clip", dict(src="HA", t0=0.6, vf="HA", mem=0)),                      # HOJE ("Every year is getting shorter")
    (69, 76, "clip", dict(src="FA2", t0=0.2, vf="FA2", mem=0)),                    # fachada (tenda com as churrasqueiras)
    (76, 79, "clip", dict(src="FA1", t0=0.0, vf="FA1", mem=0, inpaint="tudo")),       # fachada (vista de cima)
    (79, 83, "clip", dict(src="HB", t0=18.4, vf="HB", mem=0)),
    (83, 87, "clip", dict(src="HE", t0=0.4, vf="HE", mem=0)),
    (87, 91, "clip", dict(src="FA1", t0=18.4, vf="FA1", mem=0, inpaint="tudo")),   # corte na tábua
    (91, 95, "clip", dict(src="HG", t0=3.0, vf="HG", mem=0)),
    (95, 99, "clip", dict(src="HC", t0=16.8, vf="HCf", mem=0)),
    (99, 103, "clip", dict(src="FA1", t0=21.0, vf="FA1", mem=0)),                  # grelha cheia na unidade
    (103, 107, "clip", dict(src="HA", t0=8.0, vf="HA", mem=0)),
    (107, 113, "clip", dict(src="HD", t0=0.2, vf="HD", mem=0, push=0.06)),        # FECHAMENTO: o Fabrício hoje
    (113, 121, "end", dict()),                                                     # logo animado ("the song is over")
]
BURNS = [17, 63, 107]                                     # film-burn âmbar de 6 quadros nas trocas de capítulo
TRANS_BEAT = 1; M0 = TRANS_BEAT * BEAT - CLIP_PHASE
TOTAL_B = SEG[-1][1]; NF = fb(TOTAL_B)

# ---- textos (verbatim do roteiro); palavras entre * ficam na cor da marca ----------------------
TXT = [  # (texto, ano, b_in, b_out, tipo)
    ("Uma churrasqueira de *latão.", "2024.", 0.15, 8.6, "std"),
    ("Mas tinha uma coisa que *ninguém tirava dele:", None, 17.25, 24.6, "std"),
    ("a alegria.", None, 25.0, 29.0, "pop"),
    ("A *família inteira na churrasqueira.", None, 37.25, 42.8, "std"),
    ("Cada *cliente virou foto.", None, 43.15, 46.8, "std"),
    ("E cada foto virou *amizade.", None, 47.1, 51.0, "std"),
    ("*3 *unidades em Cuiabá.", "2026.", 63.25, 71.8, "std"),
    ("Obrigado por fazer parte da *nossa *história.", None, 107.25, 112.8, "std"),
]
T11 = ("Jardim Aclimação · Tropical Ville · Florais", 64.0, 71.8)

def eo(t): t = min(1, max(0, t)); return 1 - (1 - t) ** 3
def expo(t): t = min(1, max(0, t)); return 1 - 2 ** (-10 * t) if t < 1 else 1.0
def backout(t, s=1.6):
    t = min(1, max(0, t)) - 1; return 1 + (s + 1) * t ** 3 + s * t ** 2

# ---- texto: camadas por palavra ---------------------------------------------------------------
def font(path, size, wght=None):
    f = ImageFont.truetype(path, size)
    if wght: f.set_variation_by_axes([wght])
    return f

def word_layer(word, f, color, glow=0.0, track=0.0):
    a, d = f.getmetrics(); pad = 40
    w = int(sum(f.getlength(c) for c in word) + track * (len(word) - 1)) + 2
    m = Image.new("L", (w + 2 * pad, a + d + 2 * pad), 0); dr = ImageDraw.Draw(m); x = pad
    for c in word: dr.text((x, pad), c, font=f, fill=255); x += f.getlength(c) + track
    A = np.array(m, np.float32) / 255
    sh = np.maximum(np.roll(cv2.GaussianBlur(A, (0, 0), 8), 3, axis=0) * 0.6,              # sombra 0 3px 16px
                    cv2.GaussianBlur(cv2.dilate(A, np.ones((3, 3), np.uint8)), (0, 0), 1.5) * 0.35)   # contorno escuro suave
    G = cv2.GaussianBlur(A, (0, 0), 14) * glow if glow else None
    B = cv2.GaussianBlur(A, (0, 0), 5)                                                     # versão desfocada (entrada)
    return dict(A=A, sh=sh, B=B, G=G, rgb=np.array(color, np.float32), w=w, pad=pad, asc=a)

def comp(f, L, x, y_base, alpha, dy=0.0, scale=1.0, clip_x=None, blur=0.0):
    """x = esquerda do texto, y_base = linha de base. blur 0..1 mistura a versão desfocada (entrada)."""
    A, sh, G = L["A"], L["sh"], L["G"]
    if blur > 0: A = A * (1 - blur) + L["B"] * blur
    if abs(scale - 1) > 1e-3:
        A = cv2.resize(A, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR); sh = cv2.resize(sh, None, fx=scale, fy=scale)
        if G is not None: G = cv2.resize(G, None, fx=scale, fy=scale)
    h, w = A.shape; pad = L["pad"] * scale
    x0 = int(round(x - pad)); y0 = int(round(y_base - L["asc"] * scale - pad + dy))
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if xb <= xa or yb <= ya: return
    sl = (slice(ya - y0, yb - y0), slice(xa - x0, xb - x0))
    a = A[sl] * alpha; s = sh[sl] * alpha
    if clip_x is not None:
        keep = (np.arange(xa, xb)[None, :] > clip_x).astype(np.float32); a = a * keep; s = s * keep
    reg = f[ya:yb, xa:xb]
    if G is not None: reg[:] = 255 - (255 - reg) * (1 - (G[sl] * alpha)[..., None] * L["rgb"] / 255)   # brilho (screen)
    reg *= (1 - s)[..., None]; reg[:] = reg * (1 - a[..., None]) + L["rgb"] * a[..., None]

CX, MAXW = 500, 880                                       # área de texto x 60–940 -> centro 500
SIZE = 84                                                 # títulos maiores e mais firmes (pedido do cliente)
def build_text(text, year, kind):
    if kind == "pop":
        f = font(TITLE, 160, 800); L = word_layer(text, f, BRAND, glow=0.55, track=-3)
        return dict(kind=kind, items=[(L, CX - L["w"] / 2, 960 + f.getmetrics()[0] / 2 - 18)], box=None)
    size = SIZE; maxl = 3 if len(text) > 40 else 2          # frase longa: 3 linhas em vez de letra miúda
    if maxl == 3: size = 76
    raw = text.split(" ")
    while True:
        f = font(TITLE, size, 800); sp = f.getlength(" ") * 0.9; tr = -size * 0.01
        wl = lambda w: sum(f.getlength(c) for c in w) + tr * (len(w) - 1)
        lines = [[]]
        for w in raw:
            ww = w.lstrip("*")
            trial = sum(wl(x.lstrip("*")) for x in lines[-1] + [w]) + sp * len(lines[-1])
            if lines[-1] and trial > MAXW: lines.append([w])
            else: lines[-1].append(w)
        if len(lines) <= maxl: break
        size -= 2
    items = []; base_last = 1180; lh = int(size * 1.08)
    top = base_last - lh * (len(lines) - 1) - size
    if year:
        fy = font(TITLE, 150, 800); Ly = word_layer(year, fy, BRAND, glow=0.35, track=-4)
        yb_year = base_last - lh * (len(lines) - 1) - size - 26
        items.append((Ly, CX - Ly["w"] / 2, yb_year)); top = yb_year - 150 * 0.75
    for li, ln in enumerate(lines):
        tw = sum(wl(w.lstrip("*")) for w in ln) + sp * (len(ln) - 1); x = CX - tw / 2; yb = base_last - lh * (len(lines) - 1 - li)
        for w in ln:
            hl = w.startswith("*"); w = w.lstrip("*")
            L = word_layer(w, f, BRAND if hl else (255, 255, 255), glow=0.25 if hl else 0, track=tr); items.append((L, x, yb)); x += wl(w) + sp
    return dict(kind=kind, items=items, box=(top - 60, base_last + 60))

TXTL = [(build_text(t, y, k), bi, bo) for t, y, bi, bo, k in TXT]
fs = 36
while font(BODY, fs).getlength(T11[0]) + 2 * (len(T11[0]) - 1) > MAXW: fs -= 1
T11L = word_layer(T11[0], font(BODY, fs), (235, 235, 235), track=2); T11W = T11L["w"]
LAB = {k: word_layer(k, font(TITLE, 44, 800), (255, 255, 255), track=1) for k in ("2024", "2026")}
fend = font(BODY, 34); ENDL = word_layer("Guerreiro's Grill", fend, (220, 220, 220), track=4)
yy0 = np.arange(H, dtype=np.float32)[:, None, None]

def scrim(f, box, a):
    """escurecimento suave atrás do bloco de texto (legibilidade), sem caixa visível."""
    if a <= 0: return
    c = (box[0] + box[1]) / 2; hh = (box[1] - box[0]) / 2 + 140
    f *= 1 - 0.42 * a * np.exp(-0.5 * ((yy0 - c) / hh) ** 4)

def draw_texts(f, t):
    for T, bi, bo in TXTL:
        ti, to = bi * BEAT, bo * BEAT
        if not (ti - 0.01 <= t <= to + 0.45): continue
        if T["kind"] == "pop":
            L, x, yb = T["items"][0]; k = (t - ti) / 0.3; out = 1 - eo((t - to) / 0.22) if t > to else 1
            sc = 0.85 + 0.15 * backout(k); al = min(1, (t - ti) / 0.1) * out
            scrim(f, (yb - 160, yb + 40), al * 0.8)
            w = L["w"] * sc; comp(f, L, CX - w / 2, yb + (1 - sc) * 40, al, scale=sc); continue
        clip = None; wipe = T["kind"] == "wipe" and t > 4 * BEAT
        if wipe: clip = (t - 4 * BEAT) / (2 * BEAT) * (W + 200) - 100
        n = len(T["items"])
        sa = min(1, (t - ti) / 0.25) * (1 if t <= to else max(0, 1 - (t - to) / 0.35))
        if wipe: sa *= max(0, 1 - (t - 4 * BEAT) / (2 * BEAT))
        scrim(f, T["box"], sa)
        for i, (L, x, yb) in enumerate(T["items"]):
            k = (t - ti - i * 0.07) / 0.26                                     # entra: sobe 24px, desfoque -> nítido
            if k <= 0: continue
            e = expo(k); al = e; dy = (1 - e) * 24; bl = 1 - e
            if t > to:                                                          # sai: palavra por palavra, sobe e some
                ko = (t - to - i * 0.03) / 0.22
                if ko > 0: al *= 1 - eo(ko); dy -= eo(ko) * 14
            if wipe and t >= 6 * BEAT: al = 0
            comp(f, L, x, yb, al, dy=dy, clip_x=clip, blur=bl)
    ti, to = T11[1] * BEAT, T11[2] * BEAT
    if ti <= t <= to + 0.3:
        al = eo((t - ti) / 0.35) * (1 if t <= to else max(0, 1 - (t - to) / 0.25))
        comp(f, T11L, CX - T11W / 2, 1262, al, dy=(1 - eo((t - ti) / 0.35)) * 10)

# ---- looks ------------------------------------------------------------------------------------
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
VIG = np.clip(((xx - W / 2) / (W / 2)) ** 2 * 0.5 + ((yy - H / 2) / (H / 2)) ** 2 * 0.5, 0, 1) ** 1.2
rng = np.random.default_rng(7)
GRAIN = [cv2.GaussianBlur(rng.standard_normal((H, W)).astype(np.float32), (0, 0), 0.8) for _ in range(6)]
for g in GRAIN: g /= g.std()

def look(f, gi, mem):
    """mem 0..1: look 'memória' (sat −10%, âmbar +5, grão 6%, vinheta 12%, gate weave ≤1px). Grão 2% sempre."""
    if mem > 0:
        L = f @ np.array([0.299, 0.587, 0.114], np.float32)
        f += (f - L[..., None]) * (-0.10 * mem)
        f[..., 0] += 5 * mem; f[..., 1] += 1.5 * mem; f[..., 2] -= 5 * mem
        f *= (1 - 0.12 * mem * VIG)[..., None]
        sx = int(round(math.sin(gi * 0.9) * 1.0 * mem)); sy = int(round(math.cos(gi * 0.7) * 1.0 * mem))
        if sx or sy: f[:] = np.roll(f, (sy, sx), axis=(0, 1))
    amp = 1.6 * mem                                       # grão bem fino só no material antigo (hoje: limpo)
    f += (GRAIN[gi % 6] * amp)[..., None]
    return f

def burn(f, d):
    """d = distância (em quadros) do corte; 6 quadros (−3..+2)."""
    a = {-3: 0.25, -2: 0.6, -1: 0.9, 0: 0.9, 1: 0.55, 2: 0.2}.get(d, 0)
    if a <= 0: return
    cxp, cyp = W * (0.75 - 0.08 * d), H * (0.3 + 0.05 * d)
    g = np.exp(-(((xx - cxp) / (W * 0.55)) ** 2 + ((yy - cyp) / (H * 0.45)) ** 2)) * a
    amber = np.array([255, 160, 60], np.float32)
    f[:] = 255 - (255 - f) * (1 - g[..., None] * amber / 255)                 # screen

# ---- fontes de imagem -------------------------------------------------------------------------
def decode(src, t0, n, vf, step=1):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-i", S[src], "-frames:v", str(n * step), "-vf",
                          f"fps={FPS},{VF[vf]},format=rgb24", "-an", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    fr = list(np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3))
    while len(fr) < n * step: fr.append(fr[-1])
    return fr[: n * step]

_PH = {}
def photo(i):
    if i not in _PH: _PH[i] = np.array(Image.open(FOTO[i]).convert("RGB"), np.float32)
    return _PH[i]

def cover_rect(iw, ih, focus, z, panx, pany):
    """retângulo 9:16 dentro da imagem, zoom z, centrado no foco + pan (fração)."""
    if iw / ih > W / H: ch = ih / z; cw = ch * W / H
    else: cw = iw / z; ch = cw * H / W
    cx = focus[0] * iw + panx * iw; cy = focus[1] * ih + pany * ih
    cx = min(max(cx, cw / 2), iw - cw / 2); cy = min(max(cy, ch / 2), ih - ch / 2)
    return cx - cw / 2, cy - ch / 2, cw, ch

def crop_resize(img, x, y, w, h, ow, oh):
    if w > ow * 1.3:                                      # reduz antes (sem serrilhado)
        s = ow * 1.15 / w; img = cv2.resize(img, None, fx=s, fy=s, interpolation=cv2.INTER_AREA); x, y, w, h = x * s, y * s, w * s, h * s
    M = np.float32([[ow / w, 0, -x * ow / w], [0, oh / h, -y * oh / h]])
    return cv2.warpAffine(img, M, (ow, oh), flags=cv2.INTER_LINEAR if w > ow else cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)

def blur_bg(img):
    ih, iw = img.shape[:2]; x, y, w, h = cover_rect(iw, ih, (0.5, 0.5), 1.0, 0, 0)
    bg = crop_resize(img, x, y, w, h, W // 4, H // 4); bg = cv2.GaussianBlur(bg, (0, 0), 10)   # ≈ 40 px em 1080
    return cv2.resize(bg, (W, H), interpolation=cv2.INTER_LINEAR) * 0.75                         # brilho −25%

def render_photo(i, k, mode, z, pan, focus=(0.5, 0.5)):
    img = photo(i); ih, iw = img.shape[:2]; zz = z[0] + (z[1] - z[0]) * k; px, py = pan[0] * k, pan[1] * k
    if mode == "cover":
        x, y, w, h = cover_rect(iw, ih, focus, zz, px, py); return crop_resize(img, x, y, w, h, W, H)
    out = blur_bg(img)
    if iw > W * 1.3:
        s = W * 1.15 / iw; img = cv2.resize(img, None, fx=s, fy=s, interpolation=cv2.INTER_AREA); ih, iw = img.shape[:2]
    fw = W * zz; fh = fw * ih / iw; cx = W / 2 - px * W; cy = 860 - py * H
    M = np.float32([[fw / iw, 0, cx - fw / 2], [0, fh / ih, cy - fh / 2]])
    fg = cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LANCZOS4); m = cv2.warpAffine(np.ones((ih, iw), np.float32), M, (W, H), flags=cv2.INTER_LINEAR)
    return out * (1 - m[..., None]) + fg * m[..., None]

def card(img, width, border, rot, shadow=True):
    """foto com borda branca, rotação e sombra -> (rgb, alpha)."""
    ih, iw = img.shape[:2]; w = int(width); h = int(width * ih / iw)
    c = np.full((h + 2 * border, w + 2 * border, 3), 255, np.float32)
    c[border:border + h, border:border + w] = cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)
    ch, cw = c.shape[:2]; padd = 60; big = np.zeros((ch + 2 * padd, cw + 2 * padd, 3), np.float32); A = np.zeros(big.shape[:2], np.float32)
    big[padd:padd + ch, padd:padd + cw] = c; A[padd:padd + ch, padd:padd + cw] = 1
    R = cv2.getRotationMatrix2D((big.shape[1] / 2, big.shape[0] / 2), rot, 1.0)
    big = cv2.warpAffine(big, R, (big.shape[1], big.shape[0]), flags=cv2.INTER_LINEAR)
    A = cv2.warpAffine(A, R, (A.shape[1], A.shape[0]), flags=cv2.INTER_LINEAR)
    S_ = np.roll(cv2.GaussianBlur(A, (0, 0), 14), 8, axis=0) * 0.55 if shadow else np.zeros_like(A)
    return big, A, S_

def paste(f, rgb, A, Sh, cx, cy, scale=1.0, alpha=1.0):
    if abs(scale - 1) > 1e-3:
        rgb = cv2.resize(rgb, None, fx=scale, fy=scale); A = cv2.resize(A, None, fx=scale, fy=scale); Sh = cv2.resize(Sh, None, fx=scale, fy=scale)
    h, w = A.shape; x0, y0 = int(cx - w / 2), int(cy - h / 2)
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if xb <= xa or yb <= ya: return
    sl = (slice(ya - y0, yb - y0), slice(xa - x0, xb - x0)); reg = f[ya:yb, xa:xb]
    reg *= (1 - Sh[sl] * alpha)[..., None]; a = (A[sl] * alpha)[..., None]; reg[:] = reg * (1 - a) + rgb[sl] * a

# ---- mural de fotos ---------------------------------------------------------------------------
def still(src, t):
    return decode(src, t, 1, src)[0].astype(np.float32)
def crop34(img, focus=(0.5, 0.45)):
    ih, iw = img.shape[:2]
    if iw / ih > 3 / 4: cw, ch = ih * 3 / 4, ih
    else: cw, ch = iw, iw * 4 / 3
    cx = min(max(focus[0] * iw, cw / 2), iw - cw / 2); cy = min(max(focus[1] * ih, ch / 2), ih - ch / 2)
    return img[int(cy - ch / 2):int(cy + ch / 2), int(cx - cw / 2):int(cx + cw / 2)]
WALL_SRC = [(photo(4), (0.5, 0.4)), (photo(8), (0.45, 0.45)), (photo(5), (0.5, 0.5)), (photo(7), (0.4, 0.5)),
            (photo(3), (0.3, 0.4)), (still("V2", 38.0), (0.5, 0.5)), (photo(1), (0.68, 0.45)), (photo(9), (0.5, 0.5)),
            (photo(6), (0.55, 0.6)), (still("V1", 1.0), (0.5, 0.4)), (still("V4", 15.0), (0.5, 0.4)), (photo(2), (0.75, 0.45))]
SLOTS = [(0, 0), (2, 1), (1, 3), (0, 2), (2, 3), (1, 0), (0, 3), (2, 0), (1, 1), (0, 1), (2, 2), (1, 2)]   # F2 por último, no meio
wr = np.random.default_rng(11)
WALL = []
for (img, foc), (col, row) in zip(WALL_SRC, SLOTS):
    th = crop34(img, foc); rgb, A, Sh = card(th, 316, 8, float(wr.uniform(-4, 4)))      # 332x440 ≈ 7% da tela (< 25%)
    WALL.append((rgb, A, Sh, 190 + col * 350 + wr.uniform(-14, 14), 330 + row * 420 + wr.uniform(-14, 14)))
WALL_BG = blur_bg(photo(2)) * 0.55

def render_wall(j, n):
    t = j / FPS; f = WALL_BG.copy(); half = BEAT / 2
    k_out = (t - 12 * half) / 0.85; z = 1 - 0.15 * eo(k_out) if k_out > 0 else 1.0    # recua 1,0 -> 0,85
    for i, (rgb, A, Sh, cx, cy) in enumerate(WALL):
        ti = i * half
        if t < ti: break
        k = min(1, (t - ti) / 0.15)
        paste(f, rgb, A, Sh, W / 2 + (cx - W / 2) * z, H / 2 + (cy - H / 2) * z, (1.15 - 0.15 * eo(k)) * z, eo(k))
    return f

# ---- render -----------------------------------------------------------------------------------
os.makedirs(P_("work"), exist_ok=True)
enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                        "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-g", "30", "-pix_fmt", "yuv420p", P_("work/video.mp4")], stdin=subprocess.PIPE)
burn_frames = {fb(b) for b in BURNS}
edl = []
for b0, b1, kind, p in SEG:
    F0, F1 = fb(b0), fb(b1); n = F1 - F0
    edl.append(dict(b0=b0, b1=b1, ini=round(F0 / FPS, 3), fim=round(F1 / FPS, 3), kind=kind, **{("src_" + k if k in ("t0", "t1") else k): v for k, v in p.items() if k != "vf"}))
    frames = None
    if kind == "clip":
        frames = decode(p["src"], p["t0"], n, p["vf"])
        if p.get("inpaint"):                                     # apaga o selo @guerreirosgrill (fixo na tela) do vídeo
            MK = np.zeros((H, W), np.uint8)
            cv2.circle(MK, (968, 504), 40, 255, -1)
            if p["inpaint"] == "tudo": cv2.rectangle(MK, (752, 560), (1012, 608), 255, -1)
            frames = [cv2.inpaint(np.ascontiguousarray(fr), MK, 5, cv2.INPAINT_TELEA) for fr in frames]
    elif kind == "rewind":
        src = decode(p["src"], p["t0"], int(round((p["t1"] - p["t0"]) * FPS)), p["vf"])[::-1]
        frames = [src[min(len(src) - 1, i * 4)] for i in range(n)]
    elif kind == "split":
        L = decode(p["l"][0], p["l"][1], n, p["l"][0]); R = decode(p["r"][0], p["r"][1], n, p["r"][0])
    for j in range(n):
        g = F0 + j; t = g / FPS; k = j / max(1, n - 1); mem = 0.0
        if kind in ("clip", "rewind"):
            f = frames[j].astype(np.float32); mem = p.get("mem", 0)
            if p.get("push"):
                z = 1 + p["push"] * k; f = cv2.warpAffine(f, cv2.getRotationMatrix2D((W / 2, H * 0.42), 0, z), (W, H), borderMode=cv2.BORDER_REFLECT)
            if kind == "rewind":
                mem = k                                                         # entra no look de memória durante o rebobinar
                yb = int((1 - (j * 0.37) % 1) * H); hb = 90
                band = slice(max(0, yb - hb), min(H, yb + hb))
                f[band] = f[band] * 0.75 + (np.roll(f[band], 18, axis=1) * 0.6 + 255 * 0.4) * 0.25      # linha de tracking 25%
                f[..., 0] = np.roll(f[..., 0], 3, axis=1)
        elif kind == "foto":
            f = render_photo(p["f"], k, p["mode"], p["z"], p["pan"], p.get("focus", (0.5, 0.5)))
            mm = p.get("mem", (1, 1)); mem = mm[0] + (mm[1] - mm[0]) * eo(k)
        elif kind == "album":
            img = photo(p["f"]); f = blur_bg(img); zz = p["z"][0] + (p["z"][1] - p["z"][0]) * k
            if j == 0: CARD = card(img, 840, 12, p["rot"])
            paste(f, *CARD, W / 2 + p["pan"][0] * W * k, 900 + p["pan"][1] * H * k, zz); mem = 1
        elif kind == "wall":
            f = render_wall(j, n); mem = 1
        elif kind == "split":
            f = np.empty((H, W, 3), np.float32)
            f[:, :540] = L[j][:, 270:810]; f[:, 540:] = R[j][:, 270:810]
            fm = look(f.copy(), g, 1.0); f = look(f, g, 0.0); f[:, :540] = fm[:, :540]; f[:, 537:543] = 255
            mem = 0
        elif kind == "end":
            if j == 0:
                lg = Image.open(P_("assets/logo_clean.png")).convert("RGBA"); lw = 640; lh = int(lg.height * lw / lg.width)
                LGi = np.array(lg.resize((lw, lh), Image.LANCZOS), np.float32); LGA = LGi[..., 3] / 255; LGB = cv2.GaussianBlur(LGA, (0, 0), 6)
                BGF = cv2.GaussianBlur(cv2.resize(last_frame, (W // 4, H // 4)), (0, 0), 6); BGF = cv2.resize(BGF, (W, H))
                er = np.random.default_rng(5); EMB = [(er.uniform(80, W - 80), er.uniform(H * 0.55, H * 1.1), er.uniform(60, 220), er.uniform(2, 6), er.uniform(0, 6.28)) for _ in range(70)]
                GLOW = np.exp(-(((xx - W / 2) / 420) ** 2 + ((yy - 860) / 420) ** 2))
            tt = j / FPS
            f = BGF * (0.32 - 0.12 * eo(tt / 2.0)) + np.float32(BRAND_BG) * 0.0
            f += (GLOW * (0.35 + 0.08 * math.sin(tt * 7)) * eo(tt / 0.5))[..., None] * np.array([200, 60, 20], np.float32)
            for ex, ey, sp, rr, ph in EMB:                                       # brasas subindo
                y_ = ey - sp * tt * 2.2; x_ = ex + 18 * math.sin(tt * 3 + ph)
                if 0 < y_ < H:
                    fl = 0.5 + 0.5 * math.sin(tt * 12 + ph); r_ = int(rr)
                    cv2.circle(f, (int(x_), int(y_)), r_, (255 * fl, 140 * fl, 40 * fl), -1, lineType=cv2.LINE_AA)
            k = tt / 0.55; sc = 1.35 - 0.35 * backout(k, 1.4); al = min(1, tt / 0.18)
            A_ = LGA * (1 - max(0, 1 - k)) + LGB * max(0, 1 - k)                  # entra desfocado -> nítido
            w_, h_ = int(lw * sc), int(lh * sc)
            rgbS = cv2.resize(LGi[..., :3], (w_, h_)); aS = cv2.resize(A_, (w_, h_)) * al
            sw = (tt - 0.75) / 0.55                                              # brilho diagonal passando
            if 0 < sw < 1:
                gx = np.arange(w_)[None, :] + np.arange(h_)[:, None] * 0.5
                band = np.exp(-((gx - (-0.3 + 1.6 * sw) * (w_ + h_ * 0.5)) / 40) ** 2) * 0.55
                rgbS = rgbS + (255 - rgbS) * band[..., None]
            x0, y0 = W // 2 - w_ // 2, 860 - h_ // 2
            xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w_), min(H, y0 + h_)
            sh_ = cv2.GaussianBlur(aS, (0, 0), 18) * 0.7
            reg = f[ya:yb, xa:xb]; sl = (slice(ya - y0, yb - y0), slice(xa - x0, xb - x0))
            reg *= (1 - sh_[sl])[..., None]; reg[:] = reg * (1 - aS[sl][..., None]) + rgbS[sl] * aS[sl][..., None]
        if kind != "split" and kind != "end":
            f = look(f, g, mem)
        if g in burn_frames or any(abs(g - c) <= 3 for c in burn_frames):
            for c in burn_frames:
                if -3 <= g - c <= 2: burn(f, g - c)
        if kind == "split":
            comp(f, LAB["2024"], 270 - LAB["2024"]["w"] / 2, 300 + 30, 1.0); comp(f, LAB["2026"], 810 - LAB["2026"]["w"] / 2, 300 + 30, 1.0)
        draw_texts(f, t)
        fo = (g - (NF - 12)) / 12                                             # fade pro preto 0,4 s
        if fo > 0: f *= 1 - min(1, fo)
        if kind != "end": last_frame = f.copy()
        enc.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes())
enc.stdin.close(); enc.wait()
T = NF / FPS
json.dump(dict(bpm=BPM, beat=BEAT, M0=M0, total=T, segments=edl), open(P_("work/edl.json"), "w"), indent=1, ensure_ascii=False)

# ---- áudio ------------------------------------------------------------------------------------
def pcm(f, ss, t):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(ss), "-t", str(t), "-i", f, "-vn", "-ac", "2", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(r, np.int16).reshape(-1, 2).astype(np.float32) / 32768
db = lambda x: 10 ** (x / 20)
N = int(T * SR); sfx = np.zeros((N, 2), np.float32); r2 = np.random.default_rng(3)
# rebobinar (sintetizado aqui): ruído com banda subindo + chiado de fita, −18 dB
a0, a1 = int(4 * BEAT * SR), int(6 * BEAT * SR); m = a1 - a0; tt = np.arange(m) / SR
noise = r2.standard_normal(m).astype(np.float32); spec = np.fft.rfft(noise); fr = np.fft.rfftfreq(m, 1 / SR)
spec *= np.exp(-((fr - 2500) / 2200) ** 2); swish = np.fft.irfft(spec, m)
chirp = np.sin(2 * np.pi * np.cumsum(np.linspace(300, 2600, m)) / SR) * 0.35
rw = (swish / np.abs(swish).max() + chirp) * np.sin(np.pi * tt / tt[-1]) ** 0.5
# sem rebobinar nesta versão
# sfx[a0:a1] += (rw / np.sqrt(np.mean(rw ** 2)) * db(-18) * 0.25)[:, None]
# chiado da churrasqueira no bloco 1, −24 dB
c0, c1 = int(0 * BEAT * SR), int(17 * BEAT * SR); ch = pcm(CHIADO, 11.6, (c1 - c0) / SR + 0.1)[: c1 - c0]
env = np.minimum(1, np.minimum(np.arange(c1 - c0), (c1 - c0) - np.arange(c1 - c0)) / (0.4 * SR))[:, None]
sfx[c0:c1] += ch / np.sqrt(np.mean(ch ** 2)) * db(-24) * 0.25 * env
# obturador nas 3 primeiras fotos de cliente, −22 dB
for b in (43, 47, 51):
    s0 = int(b * BEAT * SR); cl = np.zeros(int(0.12 * SR), np.float32)
    for off, amp in ((0, 1.0), (int(0.055 * SR), 0.7)):
        burst = r2.standard_normal(int(0.012 * SR)) * np.exp(-np.arange(int(0.012 * SR)) / (0.003 * SR)); cl[off:off + len(burst)] += burst * amp
    sfx[s0:s0 + len(cl)] += (cl * db(-22) * 0.5)[:, None]
fo = int(0.4 * SR); sfx[-fo:] *= np.linspace(1, 0, fo)[:, None]
wavfile.write(P_("work/sfx.wav"), SR, (np.clip(sfx, -1, 1) * 32767).astype(np.int16))
# versão COM MÚSICA: "Time" do começo ao fim, já no talo (gravação enviada pelo cliente), + chiado e cliques por baixo
mus = pcm(MUS_FILE, MUS_S0, T + 0.2)[:N]
if len(mus) < N: mus = np.pad(mus, ((0, N - len(mus)), (0, 0)))
fi = int(0.03 * SR); mus[:fi] *= np.linspace(0, 1, fi)[:, None]
prev = mus * 0.9 + sfx * 0.6
prev[-fo:] *= np.linspace(1, 0, fo)[:, None]
wavfile.write(P_("work/previa.wav"), SR, (np.clip(prev, -1, 1) * 32767).astype(np.int16))

enc_a = ["-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-ac", "2"]
vcopy = ["-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-crf", "18", "-g", "30", "-pix_fmt", "yuv420p", "-r", "30"]
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", P_("work/video.mp4"), "-i", P_("work/sfx.wav"), "-map", "0:v", "-map", "1:a", *vcopy,
                *enc_a, "-movflags", "+faststart", "-shortest", OUT], check=True)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", P_("work/video.mp4"), "-i", P_("work/previa.wav"), "-map", "0:v", "-map", "1:a", *vcopy,
                "-af", "loudnorm=I=-14:TP=-2:LRA=11,alimiter=limit=0.84:level=disabled", *enc_a, "-movflags", "+faststart", "-shortest", OUT_PREV], check=True)
tc = (fb(25) + 6) / FPS
subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{tc:.3f}", "-i", P_("work/video.mp4"), "-frames:v", "1", COVER], check=True)
print("ok", T, "s | M0 =", round(M0, 3))
