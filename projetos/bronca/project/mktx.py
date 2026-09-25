# Bronca Fake — camada de texto.
#  - frase da trend no topo (TikTok Sans, a fonte das trends do TikTok): entra
#    quando ele levanta a cabeca para a bronca, nao no primeiro quadro, e sai no
#    corte para a cor
#  - legenda do video 1 (transcricao do cliente) em Poppins ExtraBold minuscula,
#    branca com contorno, palavra-chave em vermelho (linguagem do video-modelo)
#  - sem logo no fim (o cliente pediu para cortar o final)
import os, shutil
from PIL import Image, ImageDraw, ImageFilter, ImageFont
E_ = "/home/user/Success-/projetos/escala"; P = "/home/user/Success-/projetos/bronca"
W, H, TOT = 1080, 1920, 597
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

def boxed_lines(lines, ft, pad_x=26, pad_y=12, r=20, gap=-4):
    """texto preto em caixa branca arredondada, uma por linha, centralizadas."""
    asc, dsc = ft.getmetrics(); lh = asc + dsc
    boxes = []
    for l in lines:
        bb = ft.getbbox(l); tw = bb[2] - bb[0]
        bw_, bh_ = int(tw + 2 * pad_x), int(lh + 2 * pad_y - 6)
        im = Image.new("RGBA", (bw_, bh_), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, bw_ - 1, bh_ - 1], radius=r, fill=(255, 255, 255, 255))
        d.text((pad_x - bb[0], pad_y - 3), l, font=ft, fill=(12, 12, 12, 255))
        boxes.append(im)
    W_ = max(b.width for b in boxes); H_ = sum(b.height for b in boxes) + gap * (len(boxes) - 1)
    out = Image.new("RGBA", (W_ + 40, H_ + 40), (0, 0, 0, 0)); y = 20
    for b in boxes:
        out.alpha_composite(b, ((out.width - b.width) // 2, y)); y += b.height + gap
    sh = Image.new("RGBA", out.size, (0, 0, 0, 0)); sh.putalpha(out.split()[3].point(lambda v: int(v * 0.35)))
    sh = sh.filter(ImageFilter.GaussianBlur(10))
    base = Image.new("RGBA", out.size, (0, 0, 0, 0)); base.alpha_composite(sh, (0, 6)); base.alpha_composite(out)
    return base

# ---- frase da trend ----
TREND = boxed_lines(["quando o marketing pede pra", "gravar mais um vídeo que", "vai dar 0 curtidas"], tiktok(62, 600))
TR_IN, TR_OUT, TR_Y = 12, Q - 1, 318     # entra em 0,4 s (nao no primeiro quadro)

# ---- legenda do video 1 ----
# a transcricao do cliente cobre o trecho depois de 4,55 do video 1. tempos no
# video 1 (s), medidos no espectrograma: rapaaaz 4,62-5,95 | ta macia mesmo hein
# 7,60-8,50 | vale ate uma dancinha 9,50-11,45 | besta de tao macia que ta
# 11,60-13,40 | eita trem bom 13,45-14,65 | rapaz 14,85-15,55 | eeeee 16,15-16,75
# video 1 4,55 -> quadro 228; 8,667 -> quadro 347
CAPS = [
    (230, 270, ["rapaaaz"], {"rapaaaz"}),
    (320, 346, ["tá macia mesmo hein"], {"macia"}),
    (372, 430, ["vale até uma", "dancinha"], {"dancinha"}),
    (435, 489, ["besta de tão", "macia que tá"], {"macia"}),
    (491, 526, ["eita trem bom"], {"trem", "bom"}),
    (532, 553, ["rapaz"], {"rapaz"}),
    (571, 592, ["eeeee"], {"eeeee"}),
]
import re
def syl(w): return max(1, len(re.findall(r"[aeiouáéíóúâêôãõ]+", w.lower())))
def karaoke_img(lines, act, ft, stroke=6):
    """legenda estilo CapCut: todas as palavras brancas com contorno; a palavra
    ativa (indice global act) ganha caixa vermelha arredondada atras."""
    asc, dsc = ft.getmetrics(); lh = int((asc + dsc) * 1.10); sp = ft.getlength(" "); pad = 44
    ws = [[ft.getlength(x) for x in l] for l in lines]
    lw = [sum(a) + sp * (len(a) - 1) for a in ws]; tw = int(max(lw))
    im = Image.new("RGBA", (tw + 2 * pad, lh * len(lines) + 2 * pad), (0, 0, 0, 0)); sh = im.copy()
    d, ds = ImageDraw.Draw(im), ImageDraw.Draw(sh); k = 0
    for i, (l, wl) in enumerate(zip(lines, ws)):
        x = pad + (tw - lw[i]) / 2; y = pad + i * lh
        for wd, w_ in zip(l, wl):
            if k == act:
                bb = ft.getbbox(wd)
                d.rounded_rectangle([x - 14, y + bb[1] - 12, x + w_ + 14, y + bb[3] + 14], radius=16, fill=RED + (255,))
                d.text((x, y), wd, font=ft, fill=WHITE + (255,))
            else:
                ds.text((x, y + 5), wd, font=ft, fill=(0, 0, 0, 160), stroke_width=stroke, stroke_fill=(0, 0, 0, 160))
                d.text((x, y), wd, font=ft, fill=WHITE + (255,), stroke_width=stroke, stroke_fill=INK + (255,))
            x += w_ + sp; k += 1
    return Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)), im)
CAPI = []
for s0, e0, ls, hl in CAPS:
    lines = [l.split(" ") for l in ls]; words = [x for l in lines for x in l]
    tot = sum(syl(x) for x in words); acc = 0; starts = []
    for x in words:   # cada palavra acende proporcional as silabas dentro do trecho falado
        starts.append(s0 + int(round(acc / tot * (e0 - s0)))); acc += syl(x)
    CAPI.append((s0, e0, starts, [karaoke_img(lines, i, poppins(84)) for i in range(len(words))]))
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
    for s0, e0, starts, imgs in CAPI:
        if s0 - 3 <= fr <= e0:
            act = max([i for i, st in enumerate(starts) if st - 2 <= fr] or [0])
            r = fr - (s0 - 3); rw = fr - (starts[act] - 2)
            sc = (0.82 + 0.18 * out_back(r / 4.0)) * (1.0 + 0.05 * (1 - out_cubic(rw / 4.0)))
            place(c, imgs[act], W / 2, CY, out_cubic(r / 2.0), sc)
    c.save(f"{OUT}/t_{fr:04d}.png", compress_level=1)
print("quadros", TOT)
