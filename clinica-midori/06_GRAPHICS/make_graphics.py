#!/usr/bin/env python3
"""Gera os PNGs de grafismo do projeto (placeholders, marcadores, barra de CTA).

Tudo em 1080x1920 com alpha, pra ser sobreposto pelo ffmpeg no build.py.
Rode de novo depois de mexer nos textos: python3 06_GRAPHICS/make_graphics.py
"""
import json, os, random
from PIL import Image, ImageDraw, ImageFont

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = os.path.join(RAIZ, "06_GRAPHICS")
FONTES = "/mnt/skills/examples/canvas-design/canvas-fonts"
W, H = 1080, 1920

TEAL      = (44, 122, 107)
TEAL_CLARO= (108, 186, 168)
OSSO      = (238, 240, 237)
FUNDO     = (9, 18, 16)


def fonte(nome, tam):
    for cam in (os.path.join(FONTES, nome), "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(cam):
            return ImageFont.truetype(cam, tam)
    return ImageFont.load_default()


def espacado(txt, n=1):
    return (" " * n).join(txt)


def centro(d, y, txt, f, cor, espaco=0):
    t = espacado(txt, espaco) if espaco else txt
    l, t_, r, b = d.textbbox((0, 0), t, font=f)
    d.text(((W - (r - l)) / 2 - l, y), t, font=f, fill=cor)
    return b - t_


def grao(img, forca=6):
    random.seed(7)
    ruido = Image.new("L", (W // 4, H // 4))
    ruido.putdata([random.randint(128 - forca, 128 + forca) for _ in range(ruido.width * ruido.height)])
    ruido = ruido.resize((W, H), Image.BILINEAR)
    base = img.convert("RGB")
    return Image.blend(base, Image.merge("RGB", (ruido, ruido, ruido)), 0.06)


def slate(slot, rotulo, briefing, dur):
    """Cartela de placeholder — so existe no corte ESTRUTURA."""
    img = Image.new("RGB", (W, H), FUNDO)
    d = ImageDraw.Draw(img)
    # moldura de cantos
    m, c, e = 90, 70, 2
    for x0, y0, dx, dy in ((m, m, 1, 1), (W - m, m, -1, 1), (m, H - m, 1, -1), (W - m, H - m, -1, -1)):
        d.line([(x0, y0), (x0 + dx * c, y0)], fill=TEAL, width=e)
        d.line([(x0, y0), (x0, y0 + dy * c)], fill=TEAL, width=e)

    f_slot = fonte("InstrumentSans-Bold.ttf", 34)
    f_tit  = fonte("InstrumentSans-Bold.ttf", 74)
    f_sub  = fonte("InstrumentSans-Regular.ttf", 30)
    f_bri  = fonte("InstrumentSans-Regular.ttf", 32)

    centro(d, 700, f"SLOT {slot}", f_slot, TEAL_CLARO, espaco=3)
    y = 790
    for linha in rotulo.split(" / "):
        y += centro(d, y, linha.upper(), f_tit, OSSO, espaco=1) + 28
    d.line([(W / 2 - 110, y + 24), (W / 2 + 110, y + 24)], fill=TEAL, width=2)
    centro(d, y + 70, f"A GRAVAR  ·  {dur:.1f}s", f_sub, (150, 165, 158), espaco=2)

    # briefing quebrado em linhas
    pal, linhas, atual = briefing.split(), [], ""
    for p in pal:
        teste = (atual + " " + p).strip()
        if d.textlength(teste, font=f_bri) > W - 300:
            linhas.append(atual); atual = p
        else:
            atual = teste
    linhas.append(atual)
    yb = H - 430
    for ln in linhas:
        yb += centro(d, yb, ln, f_bri, (118, 132, 126)) + 16

    img = grao(img)
    img.save(os.path.join(SAIDA, f"slate_{slot}.png"))


def marcador(sid, secao, rotulo):
    """Etiqueta discreta de leitura do corte — so no corte ESTRUTURA."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f_id = fonte("InstrumentSans-Bold.ttf", 26)
    f_rt = fonte("InstrumentSans-Regular.ttf", 24)
    x, y = 62, 72
    d.rectangle([x, y, x + 3, y + 46], fill=TEAL_CLARO + (210,))
    d.text((x + 18, y), f"{sid}  {secao}", font=f_id, fill=OSSO + (215,))
    d.text((x + 18, y + 26), espacado(rotulo, 1), font=f_rt, fill=TEAL_CLARO + (190,))
    img.save(os.path.join(SAIDA, f"marcador_{sid}.png"))


def barra_cta(texto):
    """Faixa de CTA sobre o plano final — placeholder ate a marca mandar os dados."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # degrade de leitura no rodape
    for i in range(520):
        a = int(200 * (i / 520) ** 2.0)
        d.line([(0, H - 520 + i), (W, H - 520 + i)], fill=(6, 14, 12, a))
    f = fonte("InstrumentSans-Regular.ttf", 36)
    d.line([(W / 2 - 60, H - 300), (W / 2 + 60, H - 300)], fill=TEAL_CLARO + (230,), width=2)
    t = espacado(texto, 1)
    l, t_, r, b = d.textbbox((0, 0), t, font=f)
    d.text(((W - (r - l)) / 2 - l, H - 250), t, font=f, fill=OSSO + (235,))
    img.save(os.path.join(SAIDA, "cta_placeholder.png"))


if __name__ == "__main__":
    tl = json.load(open(os.path.join(RAIZ, "timeline.json")))
    for s in tl["timeline"]:
        if s.get("placeholder"):
            slate(s["slot"], s["rotulo"], s["briefing"], s["dur"])
        else:
            marcador(s["id"], s["secao"], s["rotulo"])
    barra_cta(tl["texto"]["cta_placeholder"])
    print("grafismo gerado em 06_GRAPHICS/")
