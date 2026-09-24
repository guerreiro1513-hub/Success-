# Camada de texto (v8): legenda no estilo do video-modelo do cliente.
# Minuscula, Roboto Condensed ExtraBold, branca com contorno preto, a palavra
# que esta sendo falada em vermelho (karaoke), 2 a 3 palavras por vez.
import os, shutil
from PIL import Image, ImageDraw, ImageFilter, ImageFont
P = "/home/user/Success-/projetos/escala"
W, H, TOT = 1080, 1920, 826
FONT = P + "/assets/fonts/RobotoCondensed.ttf"
WHITE = (255, 255, 255); RED = (226, 18, 28); INK = (10, 8, 8)
MAXW = 860

def font(sz, wt="ExtraBold"):
    f = ImageFont.truetype(FONT, sz); f.set_variation_by_name(wt); return f
def clamp(x): return max(0.0, min(1.0, x))
def out_cubic(t): t = clamp(t); return 1 - (1 - t) ** 3
def out_back(t, s=2.0): t = clamp(t) - 1; return 1 + t * t * ((s + 1) * t + s)

def words_img(words, active, sz):
    """words: lista de palavras; active: indice da palavra em vermelho (-1 nenhuma)."""
    f = font(sz); sp = f.getlength(" ")
    ws = [f.getlength(w) for w in words]
    tw = int(sum(ws) + sp * (len(words) - 1))
    while tw > MAXW:
        sz -= 2; f = font(sz); sp = f.getlength(" ")
        ws = [f.getlength(w) for w in words]; tw = int(sum(ws) + sp * (len(words) - 1))
    asc, desc = f.getmetrics(); pad = 34; st = max(4, sz // 16)
    im = Image.new("RGBA", (tw + 2 * pad, asc + desc + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d, ds = ImageDraw.Draw(im), ImageDraw.Draw(sh)
    x = pad
    for i, (w, wd) in enumerate(zip(words, ws)):
        ds.text((x, pad + 5), w, font=f, fill=(0, 0, 0, 170), stroke_width=st, stroke_fill=(0, 0, 0, 170))
        d.text((x, pad), w, font=f, fill=(RED if i == active else WHITE) + (255,),
               stroke_width=st, stroke_fill=INK + (255,))
        x += wd + sp
    sh = sh.filter(ImageFilter.GaussianBlur(7))
    return Image.alpha_composite(sh, im)

def place(canvas, im, cx, cy, a=1.0, sc=1.0):
    if a <= 0.001: return
    if abs(sc - 1) > 1e-3:
        im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
    if a < 0.999:
        im = im.copy(); im.putalpha(im.split()[3].point(lambda v: int(v * a)))
    canvas.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))

# ---- legenda da fala ----
# tempos de cada palavra no take (s), medidos no espectrograma silaba a silaba.
# quadro 0 = 1,00 s do take. cada palavra acende 3 quadros antes da voz.
CH = [
    [("fala", 2.48), ("gurizada", 2.82)],
    [("essa", 3.62), ("é", 3.92), ("uma", 4.02)],
    [("das", 4.50), ("seis", 4.80)],
    [("churrasqueiras", 5.05)],
    [("que", 5.96), ("temos", 6.74)],
    [("no", 7.10), ("florais", 7.33)],
    [("vem", 7.80), ("pra", 7.96), ("cá", 8.10)],
    [("tem", 8.26), ("muita", 8.45)],
    [("coisa", 8.80), ("boa", 8.97)],
    [("um", 9.28), ("abraço", 9.42)],
    [("vem", 9.65), ("ser", 9.82), ("feliz", 9.95)],
]
LEAD = 3; CEND = 278; CSZ = 92; CY = 1400
def fr_of(t): return int(round((t - 1.00) * 30)) - LEAD
chunks = []
for k, ch in enumerate(CH):
    s = fr_of(ch[0][1]); e = (fr_of(CH[k + 1][0][1]) - 1) if k + 1 < len(CH) else CEND
    words = [w for w, _ in ch]; starts = [fr_of(t) for _, t in ch]
    imgs = [words_img(words, i, CSZ) for i in range(len(words))]
    chunks.append((s, e, starts, imgs))

# ---- reveal: comeca no quadro 679 ----
R1 = words_img(["6", "churrasqueiras"], 0, 104)
R2 = words_img(["ao", "mesmo", "tempo"], 2, 104)
R_IN1, R_IN2, R_OUT = 685, 713, 771

# ---- fecho: a vinheta da marca entra no quadro 779 e ja traz o logo ----
HDL = words_img(["@guerreirosgrill"], -1, 64)
LOCK = 779

OUT = P + "/work/tx3"; shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
for fr in range(TOT):
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for s, e, starts, imgs in chunks:
        if not (s <= fr <= e): continue
        act = max(i for i, st in enumerate(starts) if st <= fr) if fr >= starts[0] else 0
        r = fr - s
        place(c, imgs[act], W / 2, CY, a=out_cubic(r / 2.0), sc=0.82 + 0.18 * out_back(r / 4.0))
    if R_IN1 <= fr < R_OUT + 5:
        ex = 1 - clamp((fr - R_OUT) / 5.0)
        for im, f0, yy in ((R1, R_IN1, 360), (R2, R_IN2, 470)):
            r = fr - f0
            if r >= 0: place(c, im, W / 2, yy, a=out_cubic(r / 2.0) * ex, sc=0.82 + 0.18 * out_back(r / 4.0))
    r = fr - (LOCK + 4)
    if r >= 0:
        a = out_cubic(r / 6.0) * (1 - clamp((fr - (LOCK + 26)) / 14.0))
        place(c, HDL, W / 2, 1372, a=a, sc=0.85 + 0.15 * out_back(r / 6.0))
    c.save(f"{OUT}/t_{fr:04d}.png", compress_level=1)
print("quadros", len(os.listdir(OUT)))
