# Bastidor v3 — texto: Anton (condensada, a fonte dos reels virais), maiuscula,
# branca com sombra dura. Duas entradas so: o gancho e o resultado.
import os, shutil
from PIL import Image, ImageDraw, ImageFilter, ImageFont
P = "/home/user/Success-/projetos/bastidor"
W, H, TOT = 1080, 1920, 480
RED = (226, 30, 36)
def clamp(x): return max(0.0, min(1.0, x))
def ob(t, s=2.2): t = clamp(t) - 1; return 1 + t * t * ((s + 1) * t + s)
def oc(t): t = clamp(t); return 1 - (1 - t) ** 3
def block(lines, sz):
    """lines: [[(palavra, cor), ...], ...]"""
    f = ImageFont.truetype(P + "/assets/fonts/Anton-Regular.ttf", sz)
    sp = f.getlength(" "); a, d = f.getmetrics(); lh = int((a + d) * 0.98)
    ws = [sum(f.getlength(t) for t, _ in l) + sp * (len(l) - 1) for l in lines]
    tw = int(max(ws)); pad = 50
    im = Image.new("RGBA", (tw + 2 * pad, lh * len(lines) + 2 * pad), (0, 0, 0, 0)); sh = im.copy()
    for i, (l, lw) in enumerate(zip(lines, ws)):
        x = pad + (tw - lw) / 2; y = pad + i * lh
        for t, col in l:
            ImageDraw.Draw(sh).text((x + 5, y + 7), t, font=f, fill=(0, 0, 0, 200))
            ImageDraw.Draw(im).text((x, y), t, font=f, fill=col + (255,))
            x += f.getlength(t) + sp
    return Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)), im)
WH = (255, 255, 255)
# v4: dupla editorial (revista de gastronomia). "por tras da" em Playfair
# Display italico, "BRASA" grande em Playfair Display Black com espacamento.
# o "O RESULTADO" saiu a pedido
FP = P + "/assets/fonts"
def pf(name, sz, var):
    f = ImageFont.truetype(FP + "/" + name, sz); f.set_variation_by_name(var); return f
def editorial():
    f1 = pf("PlayfairDisplay-Italic[wght].ttf", 84, "Medium Italic")
    f2 = pf("PlayfairDisplay[wght].ttf", 200, "Black")
    l1, l2, tr = "por trás da", "BRASA", 10
    w1 = f1.getlength(l1); w2 = sum(f2.getlength(c) + tr for c in l2) - tr
    Wd = int(max(w1, w2)) + 120; Hd = 340
    im = Image.new("RGBA", (Wd, Hd), (0, 0, 0, 0)); sh = im.copy()
    for img, col1, col2, d in ((sh, (0, 0, 0, 150), (0, 0, 0, 170), 5), (im, (255, 255, 255, 235), (255, 255, 255, 255), 0)):
        dr = ImageDraw.Draw(img)
        dr.text(((Wd - w1) / 2 + d, 18 + d), l1, font=f1, fill=col1)
        x = (Wd - w2) / 2
        for ch in l2:
            dr.text((x + d, 92 + d), ch, font=f2, fill=col2); x += f2.getlength(ch) + tr
    return Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(9)), im)
HOOK = editorial()
# (imagem, entra, sai, y)
ITEMS = [(HOOK, 6, 80, 1250)]
OD = P + "/work/tx"; shutil.rmtree(OD, ignore_errors=True); os.makedirs(OD)
for fr in range(TOT):
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for im, a, b, y in ITEMS:
        if a <= fr <= b:
            r = fr - a; al = oc(r / 6.0) * (1 - clamp((fr - (b - 6)) / 6.0))
            sc = 0.92 + 0.08 * oc(r / 8.0)          # entrada suave, sem pulo
            x = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
            if al < 0.999: x.putalpha(x.split()[3].point(lambda v: int(v * al)))
            c.alpha_composite(x, (int(W / 2 - x.width / 2), int(y - x.height / 2)))
    c.save(f"{OD}/t_{fr:04d}.png", compress_level=1)
print("quadros", TOT)
