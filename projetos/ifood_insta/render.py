#!/usr/bin/env python3
"""Guerreiro's Grill no iFood — Reels/TikTok. Gancho com texto empilhado (palavras gigantes + pequenas, glitch de cor,
um som por palavra), legenda palavra por palavra, falas inteiras, B-roll enxuto e celular 3D do iFood no final.
    python3 render.py
"""
import os, subprocess, math, re
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
from scipy.io import wavfile
from scipy.signal import butter, sosfilt
ROOT = os.path.dirname(os.path.abspath(__file__)); P = lambda p: os.path.join(ROOT, p)
W, H, FPS, SR = 1080, 1920, 30, 48000
SRC = dict(HOOK=P("source/HOOK.mov"), VO=P("source/VO.mov"), A=P("work/A_join.mov"), CTA=P("source/CTA.mov"),
           GUAR=P("source/GUAR.mov"), ROL=P("source/ROL.mov"), FER=P("source/FER.mov"))
PHONE_REC = P("source/IFOOD_REC.mp4")                       # gravação de tela do iFood (quando chegar)
OUT = P("../../entrega/guerreirosgrill_ifood_reels_v1.mp4")
GOLD = np.array([232, 178, 58], np.float32); GOLD2 = np.array([255, 214, 120], np.float32); WHITE = np.array([255, 255, 255], np.float32)
BGc = np.array([20, 16, 12], np.float32)
F_BIG = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"; F_IT = P("../tour3/assets/fonts/Montserrat-Italic.ttf")
FILL = f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H}"
GRADE = "eq=contrast=1.06:saturation=1.0"
CROP = {"ROL": "crop=iw*0.75:ih*0.74:iw*0.125:0,"}

# ---- falas inteiras --------------------------------------------------------------------------
CL = [("HOOK", 0.00, 4.35), ("VO", 0.25, 8.40), ("A", 0.00, 17.40), ("CTA", 0.30, 4.65)]
T0 = {}; t = 0.0
for k, a, b in CL: T0[k] = t; t += b - a
CTA_END = t
HAS_PHONE = os.path.exists(PHONE_REC)
PHONE_LEN = 5.0 if HAS_PHONE else 0.0
END0 = CTA_END + PHONE_LEN; T_END = END0 + 1.8
# marcação: |…| = bloco de texto empilhado; ^GRANDE, _pequena (dentro do bloco); *destaque (legenda de baixo)
TXT = {
    "HOOK": "|^Cuiabá,| |_chegou ^novidade, _hein!| |^Guerreiro's ^Grill| |_agora _está _no ^iFood.|",
    "VO": "Vamos iniciar no *iFood com o que você já conhece, a nossa *costela e o nosso *frango no *rolete e todas as *guarnições.",
    "A": ("Só que isso, pessoal, |_é _só _o ^início.| |^Em ^breve| nós teremos todos os nossos portfólios de carnes no *iFood também. "
          "Aí nós estamos falando de |^joelho _de _porco,| |^paleta _de _cordeiro,| |^panceta,| |^maminha,| |^maminha _com ^bacon,| "
          "|^fraldinha,| todo o nosso portfólio vai para o *iFood também. |^Em ^breve!|"),
    "CTA": "|^Sábado, ^domingo _e ^feriado,| |_procure ^Guerreiro's ^Grill| |_no ^iFood.|",
}
GOLDW = {"novidade,", "ifood.", "ifood", "início.", "em", "breve", "breve!", "grill", "feriado,"}

def sil(w): return max(1, len(re.findall(r"[aeiouáéíóúâêôãõà]+", w.lower())))
def pcm(f, ss=0, t=None, af="anull", sr=SR):
    cmd = ["ffmpeg", "-v", "error", "-ss", str(ss)] + (["-t", str(t)] if t else []) + ["-i", f, "-vn", "-ac", "1", "-ar", str(sr), "-af", af, "-f", "s16le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.int16).astype(np.float32) / 32768

def parse(text):
    toks = []; stack = False; sid = 0
    for raw in text.replace("|", " | ").split():
        if raw == "|":
            stack = not stack
            if stack: sid += 1
            continue
        kind = "cap"; w = raw
        if stack: kind = "big" if raw.startswith("^") else "small"; w = raw.lstrip("^_")
        hl = w.startswith("*"); w = w.lstrip("*")
        toks.append(dict(w=w, kind=kind, hl=hl, sid=(sid if stack else None)))
    return toks

def voiced_times(src, a, b, words):
    x = pcm(SRC[src], a, b - a, sr=16000); bb = sosfilt(butter(4, [250, 3500], btype="band", fs=16000, output="sos"), x)
    hop = 160; e = np.array([10 * np.log10(np.mean(bb[i:i + 320] ** 2) + 1e-12) for i in range(0, len(bb) - 320, hop)])
    e = np.convolve(e, np.ones(5) / 5, "same"); v = (e > np.median(e) + 6.0).astype(float)
    cum = np.concatenate([[0], np.cumsum(v)]); tv = cum[-1]; ss = [sil(w) for w in words]; tot = sum(ss); out = []; acc = 0
    for s in ss: out.append(int(np.searchsorted(cum, tv * acc / tot + 0.5)) * hop / 16000); acc += s
    return out
def hook_times(words):
    segs = [(1, 0.30, 0.70), (3, 0.95, 1.80), (6, 2.35, 3.75)]       # (nº de palavras, início, fim) medidos no IMG_2488
    out = []; i = 0
    for n, a, b in segs:
        ws = words[i:i + n]; ss = [sil(w) for w in ws]; tot = sum(ss); acc = 0
        for s in ss: out.append(a + (b - a) * acc / tot); acc += s
        i += n
    return out
LAG = 0.10
TOK = []; SID_OFF = 0
for k, a, b in CL:
    tk = parse(TXT[k]); words = [x["w"] for x in tk]
    times = hook_times(words) if k == "HOOK" else voiced_times(k, a, b, words)
    for x, tt in zip(tk, times):
        x["t"] = T0[k] + tt + LAG
        if x["sid"] is not None: x["sid"] += SID_OFF
        x["clip"] = k; TOK.append(x)
    SID_OFF = max([x["sid"] or 0 for x in TOK] + [SID_OFF])
TOK[0]["t"] = 0.0                                              # "CUIABÁ" já no 1º quadro
STACKS = {}
for x in TOK:
    if x["sid"] is not None: STACKS.setdefault(x["sid"], []).append(x)
SID_LIST = sorted(STACKS)
for i, s in enumerate(SID_LIST):
    ws = STACKS[s]; nxt = next((y["t"] for y in TOK if y["t"] > ws[-1]["t"] and (y["sid"] != s)), None)
    STACKS[s] = dict(words=ws, t0=ws[0]["t"], t1=min(ws[-1]["t"] + 1.3, (nxt - 0.02) if nxt else ws[-1]["t"] + 1.0))
def wt(clip, word):
    return next(x["t"] for x in TOK if x["clip"] == clip and x["w"].lower().startswith(word))

# ---- tipografia -------------------------------------------------------------------------------
def eo(t): t = min(1, max(0, t)); return 1 - (1 - t) ** 3
def back(t, s=1.9): t = min(1, max(0, t)) - 1; return 1 + (s + 1) * t ** 3 + s * t ** 2
_LC = {}
def mask(text, font, size, var=None, track=0.0):
    key = (text, font, size, var, track)
    if key in _LC: return _LC[key]
    f = ImageFont.truetype(font, size)
    if var: f.set_variation_by_axes([var])
    a, d = f.getmetrics(); pad = 40; tw = int(sum(f.getlength(c) for c in text) + track * (len(text) - 1)) + 2
    m = Image.new("L", (tw + 2 * pad, a + d + 2 * pad), 0); dr = ImageDraw.Draw(m); x = pad
    for c in text: dr.text((x, pad), c, font=f, fill=255); x += f.getlength(c) + track
    A = np.array(m, np.float32) / 255
    S = np.maximum(np.roll(cv2.GaussianBlur(A, (0, 0), size * 0.08), int(size * 0.04), axis=0) * 0.75,
                   cv2.GaussianBlur(cv2.dilate(A, np.ones((5, 5), np.uint8)), (0, 0), 2) * 0.55)
    out = dict(A=A, S=S, w=A.shape[1], h=A.shape[0], pad=pad, asc=a, size=size); _LC[key] = out; return out   # w inclui a margem

def fill(L, gold):
    h = L["h"]; yy = np.linspace(0, 1, h)[:, None, None]
    if gold: return GOLD2 * (1 - yy) + GOLD * yy                  # dourado com degradê
    return WHITE * (1 - yy * 0.12) + GOLD2 * (yy * 0.12)

def put(f, L, x, y_top, al, sc=1.0, gold=False, chroma=0.0, white_flat=False):
    A, S = L["A"], L["S"]; rgb = np.broadcast_to(WHITE, (L["h"], 1, 3)) if white_flat else fill(L, gold)
    if abs(sc - 1) > 1e-3:
        A = cv2.resize(A, None, fx=sc, fy=sc); S = cv2.resize(S, None, fx=sc, fy=sc)
        rgb = cv2.resize(np.ascontiguousarray(np.broadcast_to(rgb, (L["h"], 2, 3))), (2, A.shape[0]))[:, :1]
    h, w = A.shape; x0, y0 = int(x), int(y_top)
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if xb <= xa or yb <= ya: return
    sl = (slice(ya - y0, yb - y0), slice(xa - x0, xb - x0)); reg = f[ya:yb, xa:xb]
    reg *= (1 - S[sl] * al)[..., None]
    if chroma > 0.5:                                                   # glitch: canais vermelho/azul deslocados
        dx = int(chroma)
        for sh, col in ((dx, np.array([255, 30, 60], np.float32)), (-dx, np.array([40, 140, 255], np.float32))):
            As = np.roll(A, sh, axis=1)[sl] * al * 0.55; reg[:] = reg * (1 - As[..., None]) + col * As[..., None]
    a = (A[sl] * al)[..., None]; rr = rgb[sl[0]] if rgb.shape[0] == h else rgb[:h][sl[0]]
    reg[:] = reg * (1 - a) + rr * a

def layout_stack(ws):
    """linhas: palavras pequenas grudadas à esquerda/acima da grande seguinte; pequenas no fim ganham linha própria."""
    lines = []; pend = []
    for x in ws:
        if x["kind"] == "small": pend.append(x)
        else: lines.append((pend, x)); pend = []
    if pend: lines.append((pend, None))
    items = []; y = 0
    for smalls, big in lines:
        Ls = [mask(s["w"], F_IT, 66, 600) for s in smalls]; sw = sum(l["w"] - 2 * l["pad"] for l in Ls) + 26 * max(0, len(Ls) - 1)
        if big:
            size = 230 if len(big["w"]) <= 6 else 190 if len(big["w"]) <= 9 else 150
            word = big["w"].upper()
            while True:
                Lb = mask(word, F_BIG, size, None, -size * 0.03); bw = Lb["w"] - 2 * Lb["pad"]
                if bw <= 940 or size < 70: break
                size -= 6
            side = smalls and (sw + 18 + bw) <= 960
            if smalls and not side:                                      # pequenas em cima, alinhadas à esquerda da grande
                x0 = W / 2 - bw / 2; xs = x0
                for s, l in zip(smalls, Ls): items.append((s, l, xs - l["pad"], y - l["pad"] + 4)); xs += l["w"] - 2 * l["pad"] + 26
                y += 66 * 1.25
            tw = (sw + 18 if side else 0) + bw; x0 = W / 2 - tw / 2
            if side:
                xs = x0
                for s, l in zip(smalls, Ls): items.append((s, l, xs - l["pad"], y + size * 0.06 - l["pad"])); xs += l["w"] - 2 * l["pad"] + 26
                x0 = xs + 4
            items.append((big, Lb, x0 - Lb["pad"], y - Lb["pad"] - size * 0.12)); y += size * 0.92
        else:
            x0 = W / 2 - sw / 2; xs = x0
            for s, l in zip(smalls, Ls): items.append((s, l, xs - l["pad"], y - l["pad"])); xs += l["w"] - 2 * l["pad"] + 26
            y += 66 * 1.1
    return items, y
STACK_Y = 1060                                                         # área do meio-baixo (não cobre o rosto)
for s in SID_LIST:
    items, hgt = layout_stack(STACKS[s]["words"]); STACKS[s]["items"] = items; STACKS[s]["y0"] = min(STACK_Y, 1540 - hgt)

def draw_stacks(f, t):
    for s in SID_LIST:
        S_ = STACKS[s]
        if not (S_["t0"] - 0.01 <= t <= S_["t1"] + 0.14): continue
        out = 1.0 if t <= S_["t1"] else 1 - eo((t - S_["t1"]) / 0.14); so = 1.0 if t <= S_["t1"] else 1 - 0.1 * eo((t - S_["t1"]) / 0.14)
        for x, L, ix, iy in S_["items"]:
            if t < x["t"]: continue
            k = (t - x["t"]) / 0.16; big = x["kind"] == "big"
            sc = ((1.45 - 0.45 * back(k)) if big else (1.06 - 0.06 * eo(k))) * so
            cx = ix + L["w"] / 2; cy = S_["y0"] + iy + L["h"] / 2
            gold = big and x["w"].lower() in GOLDW
            put(f, L, cx - L["w"] * sc / 2, cy - L["h"] * sc / 2, min(1, k * 2) * out, sc, gold=gold,
                chroma=(22 * (1 - eo(k * 0.9)) if big else 0), white_flat=not big)

def draw_caps(f, t, y=1300):
    if any(STACKS[s]["t0"] - 0.05 <= t <= STACKS[s]["t1"] + 0.1 for s in SID_LIST): return
    caps = [x for x in TOK if x["kind"] == "cap" and x["t"] <= t < x["t"] + 0.9]
    if not caps or t >= CTA_END: return
    x = caps[-1]; nxt = next((y_["t"] for y_ in TOK if y_["t"] > x["t"]), x["t"] + 0.9)
    if t > nxt + 0.02: return
    if x["hl"]: L = mask(x["w"].upper(), F_BIG, 104, None, -2); gold = True
    else: L = mask(x["w"], F_IT, 84, 600); gold = False
    k = (t - x["t"]) / 0.12; sc = (1.35 - 0.35 * back(k)) if x["hl"] else (1.18 - 0.18 * eo(k))
    put(f, L, W / 2 - L["w"] * sc / 2, y - L["h"] * sc / 2, min(1, k * 2), sc, gold=gold, white_flat=not gold, chroma=(10 * (1 - eo(k)) if x["hl"] else 0))

lg = Image.open(P("../historia/assets/logo_clean.png")).convert("RGBA")
def logo_arr(w): h = int(lg.height * w / lg.width); return np.array(lg.resize((w, h), Image.LANCZOS), np.float32)
LOGO_S, LOGO_B = logo_arr(120), logo_arr(480)
def paste(f, L, x0, y0, al):
    h, w = L.shape[:2]; xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if xb <= xa or yb <= ya: return
    s = L[ya - y0:yb - y0, xa - x0:xb - x0]; a = s[..., 3:4] / 255 * al; reg = f[ya:yb, xa:xb]; reg[:] = reg * (1 - a) + s[..., :3] * a

# ---- vídeo ------------------------------------------------------------------------------------
def decode(src, st, n, speed=1.0, path=None):
    need = int(math.ceil(n * speed)) + 2
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{st:.3f}", "-i", path or SRC[src], "-frames:v", str(need), "-vf",
                          f"fps={FPS},{CROP.get(src, '')}{FILL},{GRADE},format=rgb24", "-an", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    fr = list(np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3))
    while len(fr) < need: fr.append(fr[-1])
    return [fr[min(len(fr) - 1, int(j * speed))] for j in range(n)]
KH = {}
def hblur(f, k):
    if k < 3: return f
    if k not in KH: KH[k] = np.full((1, k), 1 / k, np.float32)
    return cv2.filter2D(f, -1, KH[k], borderType=cv2.BORDER_REFLECT)
def zoom(f, z, cy=0.40):
    return f if abs(z - 1) < 1e-3 else cv2.warpAffine(f, cv2.getRotationMatrix2D((W / 2, H * cy), 0, z), (W, H), borderMode=cv2.BORDER_REFLECT)
fi = lambda t: int(round(t * FPS))

tc, tf, tg = wt("VO", "costela") - 0.12, wt("VO", "frango") - 0.12, wt("VO", "guarni") - 0.12
VO0, VO1 = T0["VO"], T0["A"]
PLAN = [(T0["HOOK"], T0["VO"], "HOOK", 0.0, 1.0),
        (VO0, tc, "ROL", 2.55, max(0.6, min(1.0, 2.0 / (tc - VO0)))),                 # "Vamos iniciar no iFood…"
        (tc, tf, "FER", 0.0, max(0.6, min(1.0, 1.88 / (tf - tc)))),                   # "a nossa costela"
        (tf, tg, "ROL", 0.0, max(0.6, min(1.0, 2.4 / (tg - tf)))),                    # "frango no rolete"
        (tg, VO1, "GUAR", 0.0, max(0.6, min(1.0, 3.85 / (VO1 - tg)))),                # "todas as guarnições"
        (T0["A"], T0["CTA"], "A", 0.0, 1.0), (T0["CTA"], CTA_END, "CTA", 0.30, 1.0)]
ENTRIES = [T0["A"], T0["CTA"]]                                          # cada vez que ele volta: entrada com cara de gancho
PUNCH = [(0.0, 1.12, 0.22), (wt("HOOK", "novidade"), 1.10, 0.2), (wt("HOOK", "ifood"), 1.14, 0.2),
         (T0["A"], 1.14, 0.25), (wt("A", "início"), 1.10, 0.2), (STACKS[[s for s in SID_LIST if STACKS[s]["words"][0]["w"].lower() == "em"][0]]["t0"], 1.12, 0.2),
         (T0["CTA"], 1.14, 0.25), (wt("CTA", "ifood"), 1.12, 0.2)]
PUNCH = sorted(PUNCH)
CUTS = [fi(p[0]) for p in PLAN[1:]] + ([fi(CTA_END)] if True else [])
yy_, xx_ = np.mgrid[0:H, 0:W]; VIG = (1 - 0.22 * np.clip((np.hypot((xx_ - W / 2) / W, (yy_ - H / 2) / H) - 0.25) * 1.6, 0, 1))[..., None].astype(np.float32)

os.makedirs(P("work"), exist_ok=True)
enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                        "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", P("work/video.mp4")], stdin=subprocess.PIPE)
g = 0; last = None; cta_frames = []
for t0, t1, src, st, spd in PLAN:
    n = fi(t1) - fi(t0); frs = decode(src, st, n, spd)
    for j, fr in enumerate(frs):
        t = g / FPS; f = fr.astype(np.float32)
        if src in ("HOOK", "A", "CTA"):
            z = 1.0
            for pt, pz, pd in PUNCH:
                if t0 - 0.01 <= pt < t1 and t >= pt:
                    z *= 1 + (pz - 1) * eo((t - pt) / pd) * (1 if t < pt + 1.2 else max(0, 1 - (t - pt - 1.2) / 0.3))
                    if t < pt + 0.15: f = np.roll(f, int(14 * (1 - (t - pt) / 0.15)) * (1 if g % 2 else -1), axis=0)
            f = zoom(f, z)
        for c in CUTS:
            d = g - c
            if -3 <= d < 0: s = (4 + d) / 4; f = np.roll(hblur(f, int(90 * s) | 1), int(-170 * s * s), axis=1)
            elif 0 <= d < 3: s = (3 - d) / 3; f = np.roll(hblur(f, int(90 * s) | 1), int(170 * s * s), axis=1)
        for e in ENTRIES:
            if 0 <= g - fi(e) < 3: f = f * 0.4 + 255 * 0.6 * (1 - (g - fi(e)) / 3)
        f *= VIG
        draw_stacks(f, t); draw_caps(f, t)
        paste(f, LOGO_S, W - 60 - 120, H - 380 - LOGO_S.shape[0], 0.7)
        last = f.copy(); enc.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes()); g += 1

# ---- celular 3D com a tela do iFood (se a gravação existir) ------------------------------------
def phone_frame(screen, ang_y, ang_x, scale, cx, cy, al, bg):
    """tela num celular com bordas arredondadas, girado em 3D (perspectiva), com sombra."""
    sh, sw = 1500, int(1500 * 1180 / 2556); scr = cv2.resize(screen, (sw, sh), interpolation=cv2.INTER_AREA)
    bez = 26; ph = np.zeros((sh + 2 * bez, sw + 2 * bez, 3), np.float32); ph[:] = (18, 18, 20); ph[bez:-bez, bez:-bez] = scr
    m = np.zeros(ph.shape[:2], np.uint8); cv2.rectangle(m, (0, 0), (ph.shape[1] - 1, ph.shape[0] - 1), 255, -1)
    r = 90; m[:] = 0; cv2.rectangle(m, (r, 0), (ph.shape[1] - r, ph.shape[0]), 255, -1); cv2.rectangle(m, (0, r), (ph.shape[1], ph.shape[0] - r), 255, -1)
    for xx, yy in ((r, r), (ph.shape[1] - r, r), (r, ph.shape[0] - r), (ph.shape[1] - r, ph.shape[0] - r)): cv2.circle(m, (xx, yy), r, 255, -1)
    hh, ww = ph.shape[:2]; pts = np.float32([[-ww / 2, -hh / 2, 0], [ww / 2, -hh / 2, 0], [ww / 2, hh / 2, 0], [-ww / 2, hh / 2, 0]]) * scale
    ay, ax = math.radians(ang_y), math.radians(ang_x)
    Ry = np.array([[math.cos(ay), 0, math.sin(ay)], [0, 1, 0], [-math.sin(ay), 0, math.cos(ay)]]); Rx = np.array([[1, 0, 0], [0, math.cos(ax), -math.sin(ax)], [0, math.sin(ax), math.cos(ax)]])
    p3 = pts @ (Rx @ Ry).T; foc = 2200.0; p2 = np.float32([[cx + foc * p[0] / (foc + p[2]), cy + foc * p[1] / (foc + p[2])] for p in p3])
    M = cv2.getPerspectiveTransform(np.float32([[0, 0], [ww, 0], [ww, hh], [0, hh]]), p2)
    warped = cv2.warpPerspective(ph, M, (W, H)); wm = cv2.warpPerspective(m.astype(np.float32) / 255, M, (W, H)) * al
    shadow = cv2.GaussianBlur(np.roll(wm, 40, axis=0), (0, 0), 40) * 0.6
    out = bg * (1 - shadow[..., None]); return out * (1 - wm[..., None]) + warped * wm[..., None]
NOVO = mask("NOVO NO IFOOD", F_BIG, 104, None, -2)
if HAS_PHONE:
    n = fi(END0) - fi(CTA_END); rec = decode(None, 0.0, n, 1.0, path=PHONE_REC) if False else None
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", PHONE_REC, "-frames:v", str(n), "-vf", f"fps={FPS},scale=1180:2556,format=rgb24", "-an", "-f", "rawvideo", "-"],
                         capture_output=True, check=True).stdout
    rec = list(np.frombuffer(raw, np.uint8).reshape(-1, 2556, 1180, 3))
    while len(rec) < n: rec.append(rec[-1])
    bgv = decode("CTA", 4.65, n, 0.5)                                   # o ambiente do pai continua atrás (câmera lenta)
    for j in range(n):
        t = g / FPS; k = j / FPS
        bg = cv2.GaussianBlur(bgv[j].astype(np.float32), (0, 0), 6 + 6 * eo(k / 0.5)) * (1 - 0.35 * eo(k / 0.5))
        e = back(k / 0.7, 1.3); ang = 40 * (1 - e) - 13 * math.sin(k * 1.2); sc = 0.50 + 0.32 * e
        f = phone_frame(rec[j].astype(np.float32), ang, 6 * (1 - e) + 3 * math.sin(k * 0.8), sc, W / 2, 1010 + 300 * (1 - eo(k / 0.6)), min(1, k / 0.2), bg)
        if j < 3: f = f * 0.4 + 255 * 0.6 * (1 - j / 3)
        kb = (k - 0.45) / 0.16                                          # selo verdadeiro: a loja é nova no iFood
        if kb > 0:
            sc_ = 1.4 - 0.4 * back(kb); put(f, NOVO, W / 2 - NOVO['w'] * sc_ / 2, 210 - NOVO['h'] * sc_ / 2, min(1, kb * 2), sc_, gold=True, chroma=20 * (1 - eo(kb)))
        enc.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes()); g += 1; last = f.copy()
# cartão final
END_T = [mask("Sábado, domingo e feriado", F_BIG, 70, None, -1), mask("PELO IFOOD", F_BIG, 130, None, -3)]
bg = cv2.resize(cv2.GaussianBlur(cv2.resize(last, (W // 6, H // 6)), (0, 0), 4), (W, H)) * 0.30 + BGc * 0.70
while g < fi(T_END):
    t = g / FPS; k = t - END0; f = bg.copy()
    s = 0.85 + 0.15 * back(k / 0.3); Lg = cv2.resize(LOGO_B, None, fx=s, fy=s); paste(f, Lg, W // 2 - Lg.shape[1] // 2, 690 - Lg.shape[0] // 2, min(1, k / 0.12))
    for i, (L, y, dl) in enumerate(zip(END_T, (1080, 1180), (0.2, 0.35))):
        kk = (k - dl) / 0.15
        if kk > 0: sc = 1.35 - 0.35 * back(kk); put(f, L, W / 2 - L["w"] * sc / 2, y - L["h"] * sc / 2 + 30, min(1, kk * 2), sc, gold=(i == 1), white_flat=(i == 0), chroma=18 * (1 - eo(kk)))
    if 0 <= g - fi(END0) < 3: f = f * 0.35 + 255 * 0.65 * (1 - (g - fi(END0)) / 3)
    if T_END - t < 0.4: f *= max(0, (T_END - t) / 0.4)
    enc.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes()); g += 1
enc.stdin.close(); enc.wait()

# ---- áudio ------------------------------------------------------------------------------------
N = int(T_END * SR); rms = lambda v: np.sqrt(np.mean(v ** 2)) + 1e-9
voz = np.zeros(N, np.float32)
for k, a, b in CL:
    af = "highpass=f=80,acompressor=threshold=-22dB:ratio=2.5:attack=15:release=200"
    if k == "VO":
        af = ("highpass=f=120,equalizer=f=320:t=q:w=1.1:g=-6,equalizer=f=650:t=q:w=1.4:g=-3,equalizer=f=3200:t=q:w=1.4:g=3,"
              "agate=threshold=0.025:ratio=4:attack=4:release=90:range=0.25,acompressor=threshold=-22dB:ratio=3:attack=10:release=150")
    x = pcm(SRC[k], a, b - a, af=af); fd = int(0.015 * SR); x[:fd] *= np.linspace(0, 1, fd); x[-fd:] *= np.linspace(1, 0, fd)
    p0 = int(T0[k] * SR); m = min(len(x), N - p0); voz[p0:p0 + m] += x[:m]
voz *= 0.25 / rms(voz[np.abs(voz) > 2e-3])
seg = pcm(P("source/MUSICA.mp4"), 7.2, 14.8); xf = int(0.8 * SR); mus = np.zeros(N, np.float32); pos = 0
while pos < N:
    x = seg.copy(); x[-xf:] *= np.linspace(1, 0, xf)
    if pos: x[:xf] *= np.linspace(0, 1, xf)
    m = min(len(x), N - pos); mus[pos:pos + m] += x[:m]; pos += len(x) - xf
mus = mus / rms(mus) * 0.25
env = np.full(N, 10 ** (-17 / 20)); env[int(CTA_END * SR):] = 10 ** (-10 / 20); env = np.convolve(env, np.ones(int(0.3 * SR)) / int(0.3 * SR), "same")
def sfx(name): x = pcm(P(f"../ifood_zap/sfx/{name}.wav")); return x / (np.abs(x).max() + 1e-9)
S_ = {k: sfx(k) for k in ("whooshfast", "whooshlow", "riser", "lens", "paper", "pencil", "film", "shutter")}
fx = np.zeros(N, np.float32)
def add(name, t, gain, maxlen=None):
    x = S_[name][: int(maxlen * SR) if maxlen else None]; p0 = int(t * SR)
    if p0 < 0: x = x[-p0:]; p0 = 0
    m = max(0, min(len(x), N - p0)); fx[p0:p0 + m] += x[:m] * gain
tt = np.arange(int(1.0 * SR)) / SR; BOOM = (np.sin(2 * np.pi * (48 + 50 * np.exp(-tt * 14)) * tt) * np.exp(-tt * 3.8)).astype(np.float32)
def boom(t, gain): p0 = int(t * SR); m = min(len(BOOM), N - p0); fx[p0:p0 + m] += BOOM[:m] * gain
TICKS = [("lens", 0.07), ("paper", 0.10), ("shutter", 0.07)]
for i, x in enumerate(TOK):                                                  # um sonzinho em cada palavra
    if x["t"] >= CTA_END: continue
    nm, ln = TICKS[i % 3]
    if x["kind"] == "big": add("whooshfast", x["t"] - 0.10, 0.22, 0.35); add(nm, x["t"], 0.22, ln)
    else: add(nm, x["t"], 0.13 if x["kind"] == "cap" else 0.16, ln)
for pt, pz, pd in PUNCH: boom(pt, 0.40 if pt < 0.1 else 0.30)
for c in [p[0] for p in PLAN[1:]]: add("whooshfast", c - 0.12, 0.30)
add("riser", CTA_END - 4.0, 0.20)
if HAS_PHONE: add("whooshlow", CTA_END - 0.25, 0.45); boom(CTA_END + 0.35, 0.45)
boom(END0, 0.5); add("film", END0, 0.15, 0.5)
mix = voz + mus * env + fx
fo = int(0.4 * SR); mix[-fo:] *= np.linspace(1, 0, fo)
wavfile.write(P("work/audio.wav"), SR, (np.clip(mix, -1, 1) * 32767).astype(np.int16))
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", P("work/video.mp4"), "-i", P("work/audio.wav"), "-map", "0:v", "-map", "1:a",
                "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-b:v", "12M", "-maxrate", "14M", "-bufsize", "20M", "-pix_fmt", "yuv420p",
                "-af", "loudnorm=I=-13:TP=-2:LRA=9,alimiter=limit=0.84:level=disabled", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                "-movflags", "+faststart", OUT], check=True)
for x in TOK: print(f"{x['t']:6.2f} {x['kind'][0]} {x['w']}")
print(OUT, round(T_END, 2), "celular 3D:", HAS_PHONE)
