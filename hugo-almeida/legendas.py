#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera as legendas (.ass) a partir do texto de cada bloco.

O texto fica em falas/bloco{N}.txt — um arquivo por bloco, texto corrido.
Sem modelo de reconhecimento de fala neste ambiente, o sincronismo é feito
pela ENERGIA DO ÁUDIO: detecta onde há voz e onde há pausa, quebra o texto em
blocos curtos e distribui o tempo proporcional ao número de sílabas, pulando
os silêncios. Fica certo no nível de frase; não é sincronismo por palavra.

Para corrigir à mão: edite o .ass gerado, ou o .txt e rode de novo.

    python3 legendas.py
"""
import json, os, re, subprocess, sys
import numpy as np

RAIZ = os.path.dirname(os.path.abspath(__file__))
SR = 16000
VOG = "aeiouáéíóúâêôãõàü"

# destaque na cor da marca
CHAVES = ["25 anos", "adultos", "crianças", "consulta inicial",
          "escaneamento intraoral", "radiografias", "segunda consulta",
          "segurança", "WhatsApp"]
MINT_ASS = "&H00BED38F"          # #8FD3BE em BBGGRR
MAX_CHARS = 24


def silabas(t):
    n = 0
    for p in re.findall(r"[A-Za-zÀ-ÿ0-9]+", t.lower()):
        if p == "25":
            n += 4; continue
        n += max(1, re.sub("[" + VOG + "]+", "V", p).count("V"))
    return n


def fatias_de_voz(path, ini, dur):
    """Intervalos com voz, em segundos relativos a `ini`."""
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", str(ini), "-t", str(dur), "-i", path,
         "-vn", "-ac", "1", "-ar", str(SR), "-af", "highpass=f=90,lowpass=f=6000",
         "-f", "s16le", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768
    w = int(SR * 0.02); n = len(x) // w
    e = np.sqrt((x[:n * w].reshape(n, w) ** 2).mean(1))
    edb = 20 * np.log10(np.maximum(e, 1e-7))
    piso, pico = np.percentile(edb, 12), np.percentile(edb, 96)
    voz = edb > piso + (pico - piso) * 0.22
    # fecha buracos de até 180 ms: respiração dentro da frase não é pausa
    k = 9
    for i in range(n - k):
        if voz[i] and voz[i + k]:
            voz[i:i + k] = True
    fat, i = [], 0
    while i < n:
        if voz[i]:
            j = i
            while j < n and voz[j]:
                j += 1
            if (j - i) * 0.02 >= 0.12:
                fat.append((i * 0.02, j * 0.02))
            i = j
        else:
            i += 1
    return fat or [(0.0, dur)]


def quebra(texto):
    """Blocos de 2 a 4 palavras, no máximo 24 caracteres, quebrando em
    fronteira natural (vírgula, ponto) sempre que possível."""
    pal = texto.split()
    blocos, atual = [], []
    for p in pal:
        atual.append(p)
        corta = (len(" ".join(atual)) >= MAX_CHARS or len(atual) >= 4
                 or re.search(r"[,.;:!?]$", p))
        if corta and len(atual) >= 2:
            blocos.append(" ".join(atual)); atual = []
    if atual:
        if blocos and len(atual) == 1:
            blocos[-1] += " " + atual[0]
        else:
            blocos.append(" ".join(atual))
    return [b for b in blocos if b.strip()]


def pinta(txt):
    """Marca as palavras-chave na cor da marca, de volta ao branco depois."""
    out = txt
    for k in sorted(CHAVES, key=len, reverse=True):
        padrao = re.compile(re.escape(k), re.IGNORECASE)
        out = padrao.sub(lambda m: "{\\c" + MINT_ASS + "}" + m.group(0) + "{\\c&H00FFFFFF&}", out)
    return out


def tc(s):
    h = int(s // 3600); m = int((s % 3600) // 60); seg = s % 60
    return f"{h:d}:{m:02d}:{seg:05.2f}"


def gera(bloco, src, ini, dur, texto, w=1080, h=1920, margem_base=680):
    fat = fatias_de_voz(src, ini, dur)
    blocos = quebra(texto)
    pesos = [max(1, silabas(b)) for b in blocos]
    total_voz = sum(b - a for a, b in fat)
    total_peso = sum(pesos)

    linhas, fi, t_na_fatia = [], 0, 0.0
    for b, peso in zip(blocos, pesos):
        quero = total_voz * peso / total_peso
        t0 = None
        restante = quero
        while restante > 1e-6 and fi < len(fat):
            a, z = fat[fi]
            disp = (z - a) - t_na_fatia
            if t0 is None:
                t0 = a + t_na_fatia
            if disp > restante:
                t_na_fatia += restante; restante = 0
            else:
                restante -= disp; fi += 1; t_na_fatia = 0.0
        t1 = (fat[min(fi, len(fat) - 1)][0] + t_na_fatia) if fi < len(fat) else fat[-1][1]
        if t0 is None:
            t0 = fat[-1][1]
        linhas.append((max(0.0, t0), min(dur, max(t0 + 0.35, t1 + 0.08)), b))

    cab = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {w}
PlayResY: {h}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Fala,Instrument Sans,62,&H00FFFFFF,&H00000000,&HA0000000,-1,0,0,0,100,100,0,0,1,0,3,2,110,110,{margem_base},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = "".join(
        f"Dialogue: 0,{tc(a)},{tc(z)},Fala,,0,0,0,,{{\\fad(120,80)}}{pinta(t)}\n"
        for a, z, t in linhas)
    cam = os.path.join(RAIZ, "falas", f"bloco{bloco}.ass")
    open(cam, "w", encoding="utf-8").write(cab + ev)
    return cam, linhas, total_voz, sum(silabas(b) for b in blocos)


if __name__ == "__main__":
    tl = json.load(open(os.path.join(RAIZ, "timeline.json")))
    print(f"{'bloco':6} {'blocos':>7} {'sílabas':>8} {'voz':>7} {'síl/s':>7}   aviso")
    for s in tl["segmentos"]:
        if s["tipo"] != "fala":
            continue
        b = s["bloco"]
        txt_cam = os.path.join(RAIZ, "falas", f"bloco{b}.txt")
        if not os.path.exists(txt_cam):
            print(f"  bloco{b}: falta falas/bloco{b}.txt"); continue
        texto = " ".join(open(txt_cam, encoding="utf-8").read().split())
        src = os.path.join(RAIZ, "falas", f"bloco{b}.mov")
        cam, linhas, voz, syl = gera(b, src, s["in"], s["dur_fonte"], texto)
        taxa = syl / max(voz, 0.01)
        aviso = "" if taxa <= 7.5 else f"TEXTO LONGO DEMAIS p/ o áudio ({taxa:.1f} síl/s)"
        print(f"  bloco{b} {len(linhas):7} {syl:8} {voz:6.2f}s {taxa:6.1f}   {aviso}")
