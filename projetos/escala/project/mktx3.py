# Camada de texto da versao 3: legenda da fala, titulos do reveal e fecho.
# Montserrat ExtraBold (OFL, assets/fonts). Tudo desenhado quadro a quadro.
import os, shutil
from PIL import Image, ImageDraw, ImageFilter, ImageFont
P = "/home/user/Success-/projetos/escala"
W, H, TOT = 1080, 1920, 640
FONT = P + "/assets/fonts/Montserrat.ttf"
WHITE = (255, 255, 255); YEL = (255, 206, 38); RED = (214, 38, 30)
# area segura do Reels: nada abaixo de ~1480 (legenda do post e botoes)
# nem colado na direita (coluna de icones). Texto largo no maximo 820 px.
MAXW = 820

def font(sz, wt="ExtraBold"):
    f = ImageFont.truetype(FONT, sz); f.set_variation_by_name(wt); return f
def clamp(x): return max(0.0, min(1.0, x))
def out_cubic(t): t = clamp(t); return 1 - (1 - t) ** 3
def out_back(t, s=1.6): t = clamp(t) - 1; return 1 + t * t * ((s + 1) * t + s)

def line_img(parts, sz, track=0, wt="ExtraBold"):
    """parts: [(texto, cor)]. Devolve RGBA com sombra suave e contorno fino."""
    f = font(sz, wt)
    while True:
        ws = [sum(f.getlength(ch) + track for ch in t) for t, _ in parts]
        tw = int(sum(ws) - track)
        if tw <= MAXW: break
        sz -= 2; f = font(sz, wt)
    asc, desc = f.getmetrics(); pad = 40
    im = Image.new("RGBA", (tw + 2 * pad, asc + desc + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d, ds = ImageDraw.Draw(im), ImageDraw.Draw(sh)
    x = pad
    for (t, col), wdt in zip(parts, ws):
        for ch in t:
            ds.text((x, pad + 6), ch, font=f, fill=(0, 0, 0, 150))
            d.text((x, pad), ch, font=f, fill=col + (255,),
                   stroke_width=max(2, sz // 30), stroke_fill=(15, 10, 8, 110))
            x += f.getlength(ch) + track
    sh = sh.filter(ImageFilter.GaussianBlur(9))
    return Image.alpha_composite(sh, im), sz

def place(canvas, im, cx, cy, a=1.0, sc=1.0, dy=0):
    if a <= 0.001: return
    if abs(sc - 1) > 1e-3:
        im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
    if a < 0.999:
        im = im.copy(); im.putalpha(im.split()[3].point(lambda v: int(v * a)))
    canvas.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2 + dy)))

def rule(wd, h=6, col=RED):
    return Image.new("RGBA", (max(1, wd), h), col + (255,))

# ---- legenda da fala: tempos medidos no espectrograma do take ----
# quadro 0 = 2,30 s do take. Cada grupo tem ate 2 linhas; a 2a entra no tempo dela.
CAP = [
    (4, 38,   [([("FALA, ", WHITE), ("GURIZADA!", YEL)], 4)]),
    (39, 107, [([("ESSA É UMA DAS", WHITE)], 39), ([("SEIS CHURRASQUEIRAS", YEL)], 74)]),
    (108, 163, [([("QUE TEMOS NO ", WHITE), ("FLORAIS.", YEL)], 108)]),
    (164, 207, [([("VEM PRA CÁ,", WHITE)], 164), ([("TEM MUITA COISA BOA.", WHITE)], 179)]),
    (208, 239, [([("UM ABRAÇO,", WHITE)], 208), ([("VEM SER ", WHITE), ("FELIZ!", YEL)], 219)]),
]
CSZ = 62; CY = 1180; LEAD = 78
capl = [(s, e, [(line_img(p, CSZ)[0], f0) for p, f0 in ls]) for s, e, ls in CAP]

# ---- reveal: comeca no quadro 370 ----
T1, _ = line_img([("6 ", YEL), ("CHURRASQUEIRAS.", WHITE)], 78, track=2)
T2, _ = line_img([("AO MESMO TEMPO.", WHITE)], 78, track=2)
R_IN1, R_IN2, R_OUT = 376, 404, 462

# ---- fecho: quadro 580 ----
badge = Image.open(P + "/assets/logo_key.png").convert("RGBA")
bw = 420; badge = badge.resize((bw, int(bw * badge.height / badge.width)), Image.LANCZOS)
HDL, _ = line_img([("@GUERREIROSGRILL", WHITE)], 40, track=5, wt="Bold")
LOCK = 580
scrim = Image.new("L", (1, H))
for y in range(H):
    scrim.putpixel((0, y), int((clamp((y - H * 0.30) / (H * 0.70)) ** 1.3) * 200))
scrim = scrim.resize((W, H)); SCR = Image.new("RGBA", (W, H), (0, 0, 0, 255)); SCR.putalpha(scrim)

OUT = P + "/work/tx3"; shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
for fr in range(TOT):
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # legenda
    for s, e, ls in capl:
        if not (s <= fr <= e): continue
        ex = clamp((e - fr) / 3.0) if fr > e - 3 else 1.0
        n = len(ls); y0 = CY - (n - 1) * LEAD / 2
        for i, (im, f0) in enumerate(ls):
            r = fr - f0
            if r < 0: continue
            t = out_cubic(r / 5.0)
            place(c, im, W / 2, y0 + i * LEAD, a=t * ex, sc=0.90 + 0.10 * out_back(r / 6.0), dy=12 * (1 - t))
    # titulos do reveal
    if R_IN1 <= fr < R_OUT + 6:
        ex = 1 - clamp((fr - R_OUT) / 6.0)
        for im, f0, yy in ((T1, R_IN1, 360), (T2, R_IN2, 452)):
            r = fr - f0
            if r < 0: continue
            t = out_cubic(r / 7.0)
            place(c, im, W / 2, yy, a=t * ex, dy=26 * (1 - t))
        pr = out_cubic((fr - R_IN2 - 4) / 10.0) * ex
        if pr > 0:
            wd = int(420 * pr); c.alpha_composite(rule(wd), (W // 2 - wd // 2, 524))
    # fecho
    if fr >= LOCK:
        sa = out_cubic((fr - LOCK) / 12.0)
        sc = SCR.copy(); sc.putalpha(SCR.split()[3].point(lambda v: int(v * sa))); c = Image.alpha_composite(c, sc)
        r = fr - (LOCK + 4)
        if r >= 0:
            t = out_cubic(r / 12.0)
            b = badge.filter(ImageFilter.GaussianBlur(3.5 * (1 - out_cubic(r / 9.0)))) if r < 9 else badge
            place(c, b, W / 2, 1010, a=t, sc=1.10 - 0.10 * out_back(r / 14.0))
        pr = out_cubic((fr - LOCK - 16) / 10.0)
        if pr > 0:
            wd = int(260 * pr); c.alpha_composite(rule(wd, 5), (W // 2 - wd // 2, 1010 + badge.height // 2 + 30))
        r = fr - (LOCK + 20)
        if r >= 0:
            t = out_cubic(r / 8.0); place(c, HDL, W / 2, 1010 + badge.height // 2 + 92, a=t, dy=10 * (1 - t))
    c.save(f"{OUT}/t_{fr:04d}.png", compress_level=1)
print("quadros", len(os.listdir(OUT)))
