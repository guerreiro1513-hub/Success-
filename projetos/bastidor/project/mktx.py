# Bastidor — camada de texto: uma linha so, pequena e discreta no topo, nos
# primeiros segundos (a maioria assiste sem som). Nada inventado: e o que o
# video mostra.
import os, shutil
from PIL import Image, ImageDraw, ImageFilter, ImageFont
P = "/home/user/Success-/projetos/bastidor"; F = "/home/user/Success-/projetos/bronca/assets/fonts"
W, H, TOT = 1080, 1920, 543
TXT = "bastidores do Guerreiro's Grill"
IN, OUT_, Y = 8, 96, 300          # 0,27 s a 3,2 s
def clamp(x): return max(0.0, min(1.0, x))
def oc(t): t = clamp(t); return 1 - (1 - t) ** 3
f = ImageFont.truetype(F + "/TikTokSans[opsz,slnt,wdth,wght].ttf", 50); f.set_variation_by_axes([36, 100, 600, 0])
tw = int(f.getlength(TXT)); a, d = f.getmetrics(); pad = 40
im = Image.new("RGBA", (tw + 2 * pad, a + d + 2 * pad), (0, 0, 0, 0)); sh = im.copy()
ImageDraw.Draw(sh).text((pad, pad + 3), TXT, font=f, fill=(0, 0, 0, 170))
ImageDraw.Draw(im).text((pad, pad), TXT, font=f, fill=(255, 255, 255, 240))
im = Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)), im)
OD = P + "/work/tx"; shutil.rmtree(OD, ignore_errors=True); os.makedirs(OD)
for fr in range(TOT):
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if IN <= fr <= OUT_ + 10:
        al = oc((fr - IN) / 8.0) * (1 - clamp((fr - OUT_) / 10.0))
        x = im.copy(); x.putalpha(x.split()[3].point(lambda v: int(v * al)))
        c.alpha_composite(x, ((W - im.width) // 2, Y - im.height // 2 + int(8 * (1 - oc((fr - IN) / 8.0)))))
    c.save(f"{OD}/t_{fr:04d}.png", compress_level=1)
print("quadros", TOT)
