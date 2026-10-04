# O Segredo v5 — textos.
# Abertura de cinema (como "The making / Steak" da referencia): "o segredo do" em
# Playfair italico + "Guerreiro's Grill" em Playfair Black italico dourado.
# Legendas palavra a palavra: a palavra falada entra com um "pop" e fica dourada
# enquanto e dita; marca e QUALIDADE ficam douradas.
import os, shutil
from PIL import Image, ImageDraw, ImageFilter, ImageFont
P = "/home/user/Success-/projetos/segredo"; FP = P + "/assets/fonts"
W, H, TOT = 1080, 1920, 468; FPS = 30
GOLD = (240, 190, 70); WHITE = (255, 255, 255)
def clamp(x): return max(0.0, min(1.0, x))
def oc(t): t = clamp(t); return 1 - (1 - t) ** 3
def ob(t, s=1.9): t = clamp(t) - 1; return 1 + t * t * ((s + 1) * t + s)
def pf(name, sz, var):
    f = ImageFont.truetype(FP + "/" + name, sz); f.set_variation_by_name(var); return f

# ---------- abertura ----------
def titulo():
    f1 = pf("PlayfairDisplay-Italic[wght].ttf", 66, "Medium Italic")
    f2 = pf("PlayfairDisplay-Italic[wght].ttf", 116, "Black Italic")
    l1, l2 = "o segredo do", "Guerreiro's Grill"
    w1, w2 = f1.getlength(l1), f2.getlength(l2)
    Wd = int(max(w1, w2)) + 120; Hd = 300
    im = Image.new("RGBA", (Wd, Hd), (0, 0, 0, 0)); sh = im.copy(); gl = im.copy()
    for img, c1, c2, d in ((sh, (0, 0, 0, 170), (0, 0, 0, 190), 5), (im, WHITE + (240,), GOLD + (255,), 0)):
        dr = ImageDraw.Draw(img)
        dr.text(((Wd - w1) / 2 + d, 20 + d), l1, font=f1, fill=c1)
        dr.text(((Wd - w2) / 2 + d, 100 + d), l2, font=f2, fill=c2)
    ImageDraw.Draw(gl).text(((Wd - w2) / 2, 100), l2, font=f2, fill=(255, 170, 60, 150))
    base = Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)), gl.filter(ImageFilter.GaussianBlur(14)))
    return Image.alpha_composite(base, im)
TIT = titulo()

# ---------- legendas palavra a palavra ----------
def fnt(sz, w="Poppins-ExtraBold.ttf"): return ImageFont.truetype(FP + "/" + w, sz)
def word_img(t, f, col):
    l, tp, r, b = f.getbbox(t, stroke_width=3); pad = 24
    im = Image.new("RGBA", (r - l + 2 * pad, b - tp + 2 * pad), (0, 0, 0, 0)); sh = im.copy()
    ImageDraw.Draw(sh).text((pad - l + 2, pad - tp + 6), t, font=f, fill=(0, 0, 0, 170))
    ImageDraw.Draw(im).text((pad - l, pad - tp), t, font=f, fill=col + (255,), stroke_width=3, stroke_fill=(20, 12, 6, 200))
    return Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)), im), pad
def frames(t_src, src0, out0): return out0 + (t_src - src0) * FPS
# linhas: (palavras [(texto, inicio em quadros, sempre dourada?)], tamanho, y, quadro de saida)
def syl_times(words, t0, t1):
    tot = sum(n for _, n, _ in words); out = []; acc = 0
    for w, n, g in words:
        out.append((w, t0 + (t1 - t0) * acc / tot, g)); acc += n
    return out
Q1 = syl_times([("Sabe", 2, 0), ("o", 1, 0), ("que", 1, 0), ("tem", 1, 0)], 1.85, 2.42)
Q2 = syl_times([("no", 1, 0), ("Guerreiro's", 3, 1), ("Grill?", 1, 1)], 2.45, 3.35)
A1 = syl_times([("CARNE", 2, 0), ("DE", 1, 0)], 5.45, 5.82)
A2 = syl_times([("QUALIDADE.", 4, 1)], 5.82, 6.75)
LINES = [
    # pergunta: take 1, quadro 45 = 1,80 s
    ([(w, frames(t, 1.80, 45), g) for w, t, g in Q1], 82, 1440, int(frames(2.44, 1.80, 45))),
    ([(w, frames(t, 1.80, 45), g) for w, t, g in Q2], 82, 1440, 93),
    # resposta: take 2, quadro 94 = 5,25 s
    ([(w, frames(t, 5.25, 94), g) for w, t, g in A1], 92, 1380, 150),
    ([(w, frames(t, 5.25, 94), g) for w, t, g in A2], 128, 1500, 150),
]
CACHE = {}
def draw_line(c, words, sz, y, fr):
    f = fnt(sz); sp = f.getlength(" ")
    ws = [f.getlength(w) for w, _, _ in words]; tw = sum(ws) + sp * (len(ws) - 1)
    x = W / 2 - tw / 2
    vis = [i for i, (_, s, _) in enumerate(words) if fr >= s]
    act = vis[-1] if vis else -1
    for i, (w, s, g) in enumerate(words):
        if fr >= s:
            ativo = (i == act and fr - s < 9)
            col = GOLD if (g or ativo) else WHITE
            key = (w, sz, col)
            if key not in CACHE: CACHE[key] = word_img(w, f, col)
            im, pad = CACHE[key]
            r = fr - s; sc = 0.78 + 0.22 * ob(r / 5.0)
            if sc != 1.0:
                im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
            cx = x + ws[i] / 2
            c.alpha_composite(im, (int(cx - im.width / 2), int(y - im.height / 2)))
        x += ws[i] + sp

OD = P + "/work/tx"; shutil.rmtree(OD, ignore_errors=True); os.makedirs(OD)
for fr in range(TOT):
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # abertura: entra suave, sai antes da fala (q 1-40)
    if 1 <= fr <= 40:
        al = oc((fr - 1) / 8) * (1 - clamp((fr - 34) / 6)); sc = 0.94 + 0.06 * oc((fr - 1) / 12)
        x = TIT.resize((int(TIT.width * sc), int(TIT.height * sc)), Image.LANCZOS)
        x.putalpha(x.split()[3].point(lambda v: int(v * al)))
        c.alpha_composite(x, (int(W / 2 - x.width / 2), int(1400 - x.height / 2)))
    for L in LINES:
        words, sz, y, end = L[0], L[1], L[2], L[3]
        cut = L[4] if len(L) > 4 else None
        if cut is not None and fr < cut: continue
        if words[0][1] <= fr <= end:
            draw_line(c, words, sz, y, fr)
    c.save(f"{OD}/t_{fr:04d}.png", compress_level=1)
print("quadros", TOT)
