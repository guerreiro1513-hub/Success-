# Bastidor v3 — texto: Anton (condensada, a fonte dos reels virais), maiuscula,
# branca com sombra dura. Duas entradas so: o gancho e o resultado.
import os, shutil
from PIL import Image, ImageDraw, ImageFilter, ImageFont
P = "/home/user/Success-/projetos/bastidor"
W, H, TOT = 1080, 1920, 507
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
HOOK = block([[("POR", WH), ("TRÁS", WH)], [("DA", WH), ("BRASA", RED)]], 150)
RES = block([[("O", WH), ("RESULTADO", RED)]], 120)
# (imagem, entra, sai, y)
ITEMS = [(HOOK, 6, 104, 1250), (RES, 392, 456, 300)]
OD = P + "/work/tx"; shutil.rmtree(OD, ignore_errors=True); os.makedirs(OD)
for fr in range(TOT):
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for im, a, b, y in ITEMS:
        if a <= fr <= b:
            r = fr - a; al = oc(r / 3.0) * (1 - clamp((fr - (b - 4)) / 4.0))
            sc = 0.70 + 0.30 * ob(r / 6.0)
            x = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
            if al < 0.999: x.putalpha(x.split()[3].point(lambda v: int(v * al)))
            c.alpha_composite(x, (int(W / 2 - x.width / 2), int(y - x.height / 2)))
    c.save(f"{OD}/t_{fr:04d}.png", compress_level=1)
print("quadros", TOT)
