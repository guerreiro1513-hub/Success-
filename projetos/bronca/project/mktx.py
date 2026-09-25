# Bronca Fake — camada de texto.
#  - frase da trend no topo (TikTok Sans, a fonte das trends do TikTok): entra
#    quando ele levanta a cabeca para a bronca, nao no primeiro quadro, e sai no
#    corte para a cor
#  - legenda do video 1 (transcricao do cliente) em Poppins ExtraBold minuscula,
#    branca com contorno, palavra-chave em vermelho (linguagem do video-modelo)
#  - logo por cima do ceu no fim, com o @
import os, shutil
from PIL import Image, ImageDraw, ImageFilter, ImageFont
E_ = "/home/user/Success-/projetos/escala"; P = "/home/user/Success-/projetos/bronca"
W, H, TOT = 1080, 1920, 651
Q = 41 + 187                     # fim do video 2 (corte para a cor)
LOGO_IN = 609
WHITE = (255, 255, 255); RED = (230, 22, 32); INK = (8, 6, 6)
def clamp(x): return max(0.0, min(1.0, x))
def out_cubic(t): t = clamp(t); return 1 - (1 - t) ** 3
def out_back(t, s=2.0): t = clamp(t) - 1; return 1 + t * t * ((s + 1) * t + s)
def tiktok(sz, wt=700):
    f = ImageFont.truetype(P + "/assets/fonts/TikTokSans[opsz,slnt,wdth,wght].ttf", sz)
    f.set_variation_by_axes([36, 100, wt, 0]); return f
def poppins(sz): return ImageFont.truetype(P + "/assets/fonts/Poppins-ExtraBold.ttf", sz)

def text_img(lines, ft, stroke, hl=(), lead=1.12):
    """lines: lista de linhas (str). palavras em hl ficam vermelhas. centralizado."""
    asc, dsc = ft.getmetrics(); lh = int((asc + dsc) * lead); sp = ft.getlength(" ")
    ws = [ft.getlength(l) for l in lines]; tw = int(max(ws)); pad = 40
    im = Image.new("RGBA", (tw + 2 * pad, lh * len(lines) + 2 * pad), (0, 0, 0, 0)); sh = im.copy()
    d, ds = ImageDraw.Draw(im), ImageDraw.Draw(sh)
    for i, (l, lw) in enumerate(zip(lines, ws)):
        x = pad + (tw - lw) / 2; y = pad + i * lh
        for wd in l.split(" "):
            ds.text((x, y + 5), wd, font=ft, fill=(0, 0, 0, 160), stroke_width=stroke, stroke_fill=(0, 0, 0, 160))
            d.text((x, y), wd, font=ft, fill=(RED if wd in hl else WHITE) + (255,), stroke_width=stroke, stroke_fill=INK + (255,))
            x += ft.getlength(wd) + sp
    return Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)), im)

def place(c, im, cx, cy, a, sc=1.0):
    if a <= 0.001: return
    if abs(sc - 1) > 1e-3: im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
    if a < 0.999: im = im.copy(); im.putalpha(im.split()[3].point(lambda v: int(v * a)))
    c.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))

# ---- frase da trend ----
TREND = text_img(["quando o marketing pede pra", "gravar mais um vídeo que", "vai dar 0 curtidas"], tiktok(70, 700), 6)
TR_IN, TR_OUT, TR_Y = 38, Q - 1, 318     # entra em 1,27 s, com o punch-in da bronca

# ---- legenda do video 1 (video 1 4,70 -> quadro 228; 8,67 -> quadro 343) ----
CAPS = [
    (228, 265, ["macia que tá"], {"macia"}),
    (313, 341, ["eita trem bom"], {"trem", "bom"}),
    (366, 391, ["rapaz"], {"rapaz"}),
    (565, 589, ["eeeee"], {"eeeee"}),
]
CAPI = [(s0, e0, text_img(ls, poppins(88), 6, hl)) for s0, e0, ls, hl in CAPS]
CY = 1400

# ---- fecho ----
badge = Image.open(E_ + "/assets/logo_key.png").convert("RGBA")
bw = 470; badge = badge.resize((bw, int(bw * badge.height / badge.width)), Image.LANCZOS)
HDL = text_img(["@guerreirosgrill"], poppins(58), 5)

OUT = P + "/work/tx"; shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
for fr in range(TOT):
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if TR_IN <= fr <= TR_OUT:
        r = fr - TR_IN
        place(c, TREND, W / 2, TR_Y, out_cubic(r / 4.0), 0.90 + 0.10 * out_back(r / 7.0))
    for s0, e0, im in CAPI:
        if s0 - 3 <= fr <= e0:
            r = fr - (s0 - 3); place(c, im, W / 2, CY, out_cubic(r / 2.0), 0.82 + 0.18 * out_back(r / 4.0))
    r = fr - LOGO_IN
    if r >= 0: place(c, badge, W / 2, 480, out_cubic(r / 3.0), 0.70 + 0.30 * out_back(r / 6.0))
    r = fr - (LOGO_IN + 8)
    if r >= 0: place(c, HDL, W / 2, 1450, out_cubic(r / 3.0), 0.82 + 0.18 * out_back(r / 4.0))
    c.save(f"{OUT}/t_{fr:04d}.png", compress_level=1)
print("quadros", TOT)
