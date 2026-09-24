# Camada de texto da versao 3: legenda da fala, titulos do reveal e fecho.
# Montserrat ExtraBold (OFL, assets/fonts). Tudo desenhado quadro a quadro.
import os, shutil
from PIL import Image, ImageDraw, ImageFilter, ImageFont
P = "/home/user/Success-/projetos/escala"
W, H, TOT = 1080, 1920, 691
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
# quadro 0 = 1,00 s do take (fala comeca em 2,48 s = quadro 44).
# cada frase entra 5 quadros ANTES da voz: com a animacao, entrar junto parece atraso Cada grupo tem ate 2 linhas; a 2a entra no tempo dela.
CAP = [
    (38, 72,   [([("FALA, ", WHITE), ("GURIZADA!", YEL)], 38)]),
    (73, 141,  [([("ESSA É UMA DAS", WHITE)], 73), ([("SEIS CHURRASQUEIRAS", YEL)], 108)]),
    (142, 197, [([("QUE TEMOS NO ", WHITE), ("FLORAIS.", YEL)], 142)]),
    (198, 241, [([("VEM PRA CÁ,", WHITE)], 198), ([("TEM MUITA COISA BOA.", WHITE)], 213)]),
    (242, 278, [([("UM ABRAÇO,", WHITE)], 242), ([("VEM SER ", WHITE), ("FELIZ!", YEL)], 253)]),
]
CSZ = 62; CY = 1180; LEAD = 78
capl = [(s, e, [(line_img(p, CSZ)[0], f0) for p, f0 in ls]) for s, e, ls in CAP]

# ---- reveal: comeca no quadro 504 ----
T1, _ = line_img([("6 ", YEL), ("CHURRASQUEIRAS.", WHITE)], 78, track=2)
T2, _ = line_img([("AO MESMO TEMPO.", WHITE)], 78, track=2)
R_IN1, R_IN2, R_OUT = 510, 538, 596

# ---- fecho: a vinheta da marca entra no quadro 644 e ja traz o logo.
# aqui so o @ embaixo dele, saindo junto com o escurecimento da vinheta
HDL, _ = line_img([("@GUERREIROSGRILL", WHITE)], 40, track=5, wt="Bold")
LOCK = 644
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
            t = out_cubic(r / 3.0)
            place(c, im, W / 2, y0 + i * LEAD, a=t * ex, sc=0.94 + 0.06 * out_back(r / 4.0), dy=8 * (1 - t))
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
    r = fr - (LOCK + 4)
    if r >= 0:
        t = out_cubic(r / 8.0) * (1 - clamp((fr - (LOCK + 26)) / 14.0))
        place(c, HDL, W / 2, 1372, a=t, dy=10 * (1 - out_cubic(r / 8.0)))
    c.save(f"{OUT}/t_{fr:04d}.png", compress_level=1)
print("quadros", len(os.listdir(OUT)))
