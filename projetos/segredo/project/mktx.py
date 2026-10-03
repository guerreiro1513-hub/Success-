# O Segredo — textos: chamada no topo (some antes da fala) e legendas da fala.
# Branco com contorno preto sutil, Poppins. Longe do rosto e da mao.
import os, shutil
from PIL import Image, ImageDraw, ImageFilter, ImageFont
P = "/home/user/Success-/projetos/segredo"; FP = P + "/assets/fonts"
W, H, TOT = 1080, 1920, 307
def clamp(x): return max(0.0, min(1.0, x))
def oc(t): t = clamp(t); return 1 - (1 - t) ** 3
def txt(s, sz, font="Poppins-Bold.ttf", stroke=5):
    f = ImageFont.truetype(FP + "/" + font, sz)
    l, t, r, b = f.getbbox(s, stroke_width=stroke); pad = 30
    im = Image.new("RGBA", (r - l + 2 * pad, b - t + 2 * pad), (0, 0, 0, 0)); sh = im.copy()
    ImageDraw.Draw(sh).text((pad - l + 3, pad - t + 5), s, font=f, fill=(0, 0, 0, 140), stroke_width=stroke, stroke_fill=(0, 0, 0, 140))
    ImageDraw.Draw(im).text((pad - l, pad - t), s, font=f, fill=(255, 255, 255, 255), stroke_width=stroke, stroke_fill=(0, 0, 0, 235))
    return Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5)), im)
# (imagem, entra, sai, y centro, entrada em quadros)
ITEMS = [
    (txt("Ele vai contar um segredo…", 64, "Poppins-SemiBold.ttf", 5), 4, 48, 1480, 6),
    # fala (1440 take 1, 1,85-3,35 s): "No Guerreiro's Grill" ate a pausa de 2,42 s
    (txt("No Guerreiro's Grill", 78), 55, 72, 1450, 3),
    (txt("tem carne", 78), 73, 103, 1400, 3),
    (txt("DE QUALIDADE.", 100, "Poppins-ExtraBold.ttf", 6), 82, 103, 1510, 3),
]
OD = P + "/work/tx"; shutil.rmtree(OD, ignore_errors=True); os.makedirs(OD)
for fr in range(TOT):
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for im, a, b, y, ent in ITEMS:
        if a <= fr <= b:
            r = fr - a
            al = (oc(r / ent) if ent else 1.0) * (1 - clamp((fr - (b - 3)) / 3.0) if b - a > 20 else 1.0)
            sc = (0.94 + 0.06 * oc(r / ent)) if ent else 1.0
            x = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS) if sc < 0.999 else im.copy()
            if al < 0.999: x.putalpha(x.split()[3].point(lambda v: int(v * al)))
            c.alpha_composite(x, (int(W / 2 - x.width / 2), int(y - x.height / 2)))
    c.save(f"{OD}/t_{fr:04d}.png", compress_level=1)
print("quadros", TOT)
