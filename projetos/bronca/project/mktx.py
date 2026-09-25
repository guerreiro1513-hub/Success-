# Bronca Fake v2 — camada do fecho: o logo entra por cima do ceu nos ultimos
# segundos, como no video-modelo, e o @ embaixo. Sem legenda da fala.
import os, shutil
from PIL import Image, ImageDraw, ImageFilter, ImageFont
E_ = "/home/user/Success-/projetos/escala"; P = "/home/user/Success-/projetos/bronca"
W, H, TOT = 1080, 1920, 394
LOGO_IN = 352          # 0,4 s antes do quadro parado, ainda com a imagem andando
def clamp(x): return max(0.0, min(1.0, x))
def out_cubic(t): t = clamp(t); return 1 - (1 - t) ** 3
def out_back(t, s=2.0): t = clamp(t) - 1; return 1 + t * t * ((s + 1) * t + s)
badge = Image.open(E_ + "/assets/logo_key.png").convert("RGBA")
bw = 470; badge = badge.resize((bw, int(bw * badge.height / badge.width)), Image.LANCZOS)
f = ImageFont.truetype(E_ + "/assets/fonts/RobotoCondensed.ttf", 66); f.set_variation_by_name("ExtraBold")
txt = "@guerreirosgrill"; tw = int(f.getlength(txt)); asc, dsc = f.getmetrics()
hdl = Image.new("RGBA", (tw + 60, asc + dsc + 60), (0, 0, 0, 0)); sh = hdl.copy()
ImageDraw.Draw(sh).text((30, 35), txt, font=f, fill=(0, 0, 0, 170), stroke_width=5, stroke_fill=(0, 0, 0, 170))
ImageDraw.Draw(hdl).text((30, 30), txt, font=f, fill=(255, 255, 255, 255), stroke_width=5, stroke_fill=(10, 8, 8, 255))
hdl = Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)), hdl)
def place(c, im, cx, cy, a, sc):
    if a <= 0.001: return
    im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
    if a < 0.999: im.putalpha(im.split()[3].point(lambda v: int(v * a)))
    c.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))
OUT = P + "/work/tx"; shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
for fr in range(TOT):
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    r = fr - LOGO_IN
    if r >= 0:
        place(c, badge, W / 2, 480, out_cubic(r / 3.0), 0.70 + 0.30 * out_back(r / 6.0))
    r2 = fr - (LOGO_IN + 8)
    if r2 >= 0:
        place(c, hdl, W / 2, 1450, out_cubic(r2 / 3.0), 0.82 + 0.18 * out_back(r2 / 4.0))
    c.save(f"{OUT}/t_{fr:04d}.png", compress_level=1)
print("quadros", TOT)
