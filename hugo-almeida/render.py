#!/usr/bin/env python3
"""Monta o vídeo a partir do timeline.json.

    python3 render.py                 # render final 1080x1920
    python3 render.py --preview       # render rápido 540x960 (validar ritmo)
    python3 render.py --do-zero       # ignora o cache de segmentos

Como trocar as falas pelos vídeos reais: ponha os arquivos em `falas/` com os
nomes `bloco1`, `bloco2`, `bloco3`, `bloco4` (.mov ou .mp4) e rode de novo.
Cada bloco que existir entra com a DURAÇÃO REAL do arquivo e o resto da linha
do tempo se reacomoda; os que não existirem viram cartela de placeholder com a
duração prevista. Legenda: se existir `falas/bloco1.srt`, ela é queimada.

Como trocar um B-roll: mude o campo `origem` do segmento no timeline.json.
"""
import argparse, hashlib, json, math, os, shutil, subprocess, sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
REAPROVEITAR = True
CACHE = os.path.join(RAIZ, "_cache")
SAIDA = os.path.join(RAIZ, "output")
GRAF = os.path.join(RAIZ, "graficos")
FONTES = "/mnt/skills/examples/canvas-design/canvas-fonts"
FALLBACK_FONTE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


# ------------------------------------------------------------------ util
def ff(args, saida_erro=True):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y"] + args,
                       capture_output=True, text=True)
    if r.returncode and saida_erro:
        print("\nFALHA no ffmpeg:\n  " + " ".join(args) + "\n" + r.stderr[-2000:])
        sys.exit(1)
    return r


def duracao(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path], capture_output=True, text=True)
    for ln in r.stderr.splitlines():
        if "Duration:" in ln:
            h, m, s = ln.split("Duration:")[1].split(",")[0].strip().split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    return 0.0


def tem_audio(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path], capture_output=True, text=True)
    return "Audio:" in r.stderr


def fonte(nome, tam):
    from PIL import ImageFont
    for c in (os.path.join(FONTES, nome + ".ttf"), FALLBACK_FONTE):
        if os.path.exists(c):
            return ImageFont.truetype(c, tam)
    return ImageFont.load_default()


# ------------------------------------------------- enquadramento e giro
def cadeia_enquadre(W, H, rot, zoom, cx, cy, destino_w, destino_h):
    """Gira, recorta uma janela 9:16 e escala. O zoom sobe sozinho até o
    recorte caber dentro da imagem girada — nunca entra canto preto."""
    a = math.radians(abs(rot))
    if a > 1e-6:
        ca, sa = math.cos(a), math.sin(a)
        s = min(W / (W * ca + H * sa), H / (W * sa + H * ca))
        zoom = max(zoom, 1.0 / s * 1.005)
    else:
        s = 1.0
    uw, uh = W * s, H * s                      # área utilizável depois do giro
    cw = W / zoom
    ch = cw * destino_h / destino_w
    if ch > H / zoom:
        ch = H / zoom
        cw = ch * destino_w / destino_h
    cw, ch = int(cw // 2 * 2), int(ch // 2 * 2)
    # centro preso dentro da área utilizável
    lo_x, hi_x = (W - uw) / 2 + cw / 2, (W + uw) / 2 - cw / 2
    lo_y, hi_y = (H - uh) / 2 + ch / 2, (H + uh) / 2 - ch / 2
    px = min(max(cx * W, min(lo_x, hi_x)), max(lo_x, hi_x))
    py = min(max(cy * H, min(lo_y, hi_y)), max(lo_y, hi_y))
    x, y = int(px - cw / 2), int(py - ch / 2)

    f = []
    if a > 1e-6:
        r = f"{rot}*PI/180"
        f.append(f"rotate={r}:ow=rotw({r}):oh=roth({r}):c=black@0")
        # o giro expande a tela; reposiciona o recorte no centro expandido
        f.append(f"crop={cw}:{ch}:(iw-{cw})/2+{x - (W - cw) // 2}:(ih-{ch})/2+{y - (H - ch) // 2}")
    else:
        f.append(f"crop={cw}:{ch}:{x}:{y}")
    return f, zoom


# ------------------------------------------------------------ gráficos
PALETA = dict(fundo=(15, 17, 21), osso=(242, 244, 246), fraco=(150, 160, 170),
              acento=(92, 196, 180))


def card_placeholder(texto, caminho, w, h):
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (w, h), PALETA["fundo"])
    d = ImageDraw.Draw(img)
    f1 = fonte("InstrumentSans-Bold", int(h * 0.030))
    f2 = fonte("InstrumentSans-Regular", int(h * 0.016))
    t = "  ".join(texto)
    bb = d.textbbox((0, 0), t, font=f1)
    d.text(((w - (bb[2] - bb[0])) / 2 - bb[0], h / 2 - (bb[3] - bb[1])), t,
           font=f1, fill=PALETA["osso"])
    d.line([(w / 2 - 70, h / 2 + 46), (w / 2 + 70, h / 2 + 46)], fill=PALETA["acento"], width=2)
    s = "substitua pondo o arquivo em falas/"
    bb = d.textbbox((0, 0), s, font=f2)
    d.text(((w - (bb[2] - bb[0])) / 2 - bb[0], h / 2 + 76), s, font=f2, fill=PALETA["fraco"])
    img.save(caminho)


def card_faltando(arquivo, caminho, w, h):
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (w, h), (28, 16, 16))
    d = ImageDraw.Draw(img)
    f1 = fonte("InstrumentSans-Bold", int(h * 0.024))
    f2 = fonte("InstrumentSans-Regular", int(h * 0.015))
    for i, (t, f, cor) in enumerate([("B-ROLL FALTANDO", f1, (240, 200, 200)),
                                     (arquivo, f2, (190, 150, 150))]):
        bb = d.textbbox((0, 0), t, font=f)
        d.text(((w - (bb[2] - bb[0])) / 2 - bb[0], h / 2 - 40 + i * 60), t, font=f, fill=cor)
    img.save(caminho)


def png_texto(spec, caminho, w, h, seg_seguranca):
    """Texto de tela: terço superior, nunca sobre o rosto, fundo escuro discreto."""
    from PIL import Image, ImageDraw, ImageFilter
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    estilo = spec.get("estilo", "pergunta")
    if estilo == "nome":
        tams = [int(h * 0.030), int(h * 0.019)]
        cores = [PALETA["osso"], (196, 214, 220)]
        fontes = ["InstrumentSans-Bold", "InstrumentSans-Regular"]
    elif estilo == "cta":
        tams = [int(h * 0.028), int(h * 0.020)]
        cores = [PALETA["osso"], PALETA["acento"]]
        fontes = ["InstrumentSans-Bold", "InstrumentSans-Bold"]
    else:
        tams = [int(h * 0.029)]
        cores = [PALETA["osso"]]
        fontes = ["InstrumentSans-Bold"]

    linhas = spec["linhas"]
    itens = []
    for i, ln in enumerate(linhas):
        f = fonte(fontes[min(i, len(fontes) - 1)], tams[min(i, len(tams) - 1)])
        bb = d.textbbox((0, 0), ln, font=f)
        itens.append((ln, f, cores[min(i, len(cores) - 1)], bb[2] - bb[0], bb[3] - bb[1], bb))

    esp = int(h * 0.012)
    alt = sum(i[4] for i in itens) + esp * (len(itens) - 1)
    topo = seg_seguranca["topo"] + int(h * 0.055)
    larg = max(i[3] for i in itens)

    # placa escura discreta atrás do texto, com borda suave
    pad_x, pad_y = int(h * 0.018), int(h * 0.014)
    placa = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pd = ImageDraw.Draw(placa)
    x0 = (w - larg) / 2 - pad_x
    pd.rounded_rectangle([x0, topo - pad_y, x0 + larg + pad_x * 2, topo + alt + pad_y],
                         radius=int(h * 0.010), fill=(10, 13, 17, 150))
    placa = placa.filter(ImageFilter.GaussianBlur(0.6))
    img = Image.alpha_composite(img, placa)
    d = ImageDraw.Draw(img)

    y = topo
    for ln, f, cor, lw, lh, bb in itens:
        d.text(((w - lw) / 2 - bb[0], y - bb[1]), ln, font=f, fill=cor + (255,))
        y += lh + esp
    img.save(caminho)


# -------------------------------------------------------- um segmento
def chave_cache(spec, extras, saida):
    """Assinatura do segmento. Só re-renderiza o que mudou — é o que faz
    trocar uma fala custar segundos em vez de refazer o vídeo inteiro."""
    partes = [json.dumps(spec, sort_keys=True, ensure_ascii=False)] + [str(e) for e in extras]
    for f in extras:
        if isinstance(f, str) and os.path.exists(f):
            st = os.stat(f); partes.append(f"{st.st_size}:{int(st.st_mtime)}")
    h = hashlib.sha1("|".join(partes).encode()).hexdigest()
    cam = saida + ".chave"
    if os.path.exists(saida) and os.path.exists(cam) and open(cam).read() == h:
        return h, True
    return h, False


def grava_chave(saida, h):
    open(saida + ".chave", "w").write(h)


def render_broll(s, cfg, W, H, fps, idx, preview):
    src = os.path.join(RAIZ, s["origem"])
    saida = os.path.join(CACHE, f"seg{idx:02d}.mp4")
    h, ok = chave_cache(s, [src, W, H, fps, preview, cfg["look"]["comum"]], saida)
    if ok and REAPROVEITAR:
        return saida, s["dur_fonte"] / s.get("speed", 1.0)
    if not os.path.exists(src):
        print(f"  !! {s['id']} {s['rotulo']}: arquivo não encontrado — {s['origem']}")
        dur = s["dur_fonte"] / s.get("speed", 1.0)
        png = os.path.join(GRAF, f"faltando_{idx:02d}.png")
        card_faltando(s["origem"], png, W, H)
        ff(["-loop", "1", "-i", png, "-f", "lavfi", "-i",
            f"anullsrc=r=48000:cl=stereo", "-t", f"{dur:.3f}", "-r", str(fps),
            "-vf", f"scale={W}:{H},format=yuv420p", "-c:v", "libx264", "-crf", "20",
            "-preset", "veryfast", "-c:a", "aac", "-shortest", saida])
        return saida, dur

    # resolução real (o metadado de rotação já é aplicado na decodificação)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", src], capture_output=True, text=True)
    sw = sh = None
    for ln in r.stderr.splitlines():
        if "Video:" in ln:
            for tk in ln.split(","):
                tk = tk.strip().split(" ")[0]
                if "x" in tk and tk.replace("x", "").isdigit():
                    sw, sh = map(int, tk.split("x")); break
    if "rotation of -90" in r.stderr or "rotation of 90" in r.stderr:
        if sw > sh:
            sw, sh = sh, sw

    vel = s.get("speed", 1.0)
    L = s["dur_fonte"]
    dur = L / vel
    enq = s.get("enquadre", {})
    cadeia, zoom_usado = cadeia_enquadre(
        sw, sh, s.get("rotacao", 0.0), enq.get("zoom", 1.0),
        enq.get("cx", 0.5), enq.get("cy", 0.5), W, H)

    vf = [s["wb"]] if s.get("wb") else []
    vf += cadeia

    punch = s.get("punch", 1.0)
    if punch > 1.001:
        n = max(2, int(round(dur * fps)))
        vf.append(f"scale={W*2}:{H*2}:flags=bicubic")
        vf.append(f"zoompan=z='1+{punch-1:.4f}*on/{n-1}':x='iw/2-(iw/zoom/2)':"
                  f"y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={fps}")
    else:
        vf.append(f"scale={W}:{H}:flags=bicubic")

    vf.append(cfg["look"]["comum"])
    if abs(vel - 1.0) > 1e-3:
        vf.append(f"setpts={1/vel:.6f}*PTS")
    vf += [f"fps={fps}", "format=yuv420p"]

    entradas = ["-ss", f"{s['in']:.3f}", "-t", f"{L:.3f}", "-i", src]
    fc_v = ",".join(vf)

    png = sobrepor_texto(s, idx, W, H, cfg)
    if png:
        entradas += ["-loop", "1", "-framerate", str(fps), "-t", f"{dur:.3f}", "-i", png]
        ini, fim = janela_texto(s, dur)
        fc = (f"[0:v]{fc_v}[v];[1:v]format=rgba,"
              f"fade=t=in:st={ini:.2f}:d=0.25:alpha=1,"
              f"fade=t=out:st={fim-0.25:.2f}:d=0.25:alpha=1[m];"
              f"[v][m]overlay=0:0:format=yuv420:eof_action=pass[vo]")
        mapa = ["-filter_complex", fc, "-map", "[vo]"]
    else:
        mapa = ["-vf", fc_v, "-map", "0:v"]

    # ambiente do B-roll, baixo
    if tem_audio(src):
        af = f"atempo={max(0.5,min(2.0,vel)):.4f}," if abs(vel - 1.0) > 1e-3 else ""
        audio_args = ["-map", "0:a", "-af",
                      f"{af}highpass=f=80,volume={cfg['audio']['ambiente_db']}dB",
                      "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2"]
    else:
        audio_args = ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
                      "-map", f"{2 if png else 1}:a", "-c:a", "aac", "-b:a", "160k"]

    crf = "28" if preview else "16"
    ff(entradas + mapa + audio_args + ["-t", f"{dur:.3f}", "-c:v", "libx264", "-crf", crf,
       "-preset", "veryfast" if preview else "medium", saida])
    grava_chave(saida, h)
    return saida, dur


def janela_texto(s, dur):
    t = s.get("texto")
    if not t:
        return 0.0, dur
    if "entra_do_fim" in t:
        ini = max(0.0, dur - t["entra_do_fim"])
    else:
        ini = t.get("entra", 0.3)
    fim = min(dur, ini + t["dura"]) if "dura" in t else dur
    return ini, fim


def sobrepor_texto(s, idx, W, H, cfg):
    if not s.get("texto"):
        return None
    png = os.path.join(GRAF, f"texto_{idx:02d}.png")
    png_texto(s["texto"], png, W, H, cfg["seguranca_instagram"])
    return png


def acha_fala(bloco):
    for ext in (".mov", ".mp4", ".MOV", ".MP4", ".m4v"):
        p = os.path.join(RAIZ, "falas", f"bloco{bloco}{ext}")
        if os.path.exists(p):
            return p
    return None


def render_fala(s, cfg, W, H, fps, idx, preview):
    saida = os.path.join(CACHE, f"seg{idx:02d}.mp4")
    src = acha_fala(s["bloco"])
    a = cfg["audio"]
    srt0 = os.path.join(RAIZ, "falas", f"bloco{s['bloco']}.srt")
    h, ok = chave_cache(s, [src or "", srt0, W, H, fps, preview, cfg["look"]["comum"]], saida)
    if ok and REAPROVEITAR:
        return saida, duracao(saida), src is not None

    if src is None:
        dur = s["dur_prevista"]
        png = os.path.join(GRAF, f"placeholder_{s['bloco']}.png")
        card_placeholder([f"FALA {s['bloco']}", "·", "HUGO", "·", f"{dur:g}s"], png, W, H)
        entradas = ["-loop", "1", "-framerate", str(fps), "-t", f"{dur:.3f}", "-i", png,
                    "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
        vf = f"scale={W}:{H},format=yuv420p"
        png_t = sobrepor_texto(s, idx, W, H, cfg)
        if png_t:
            entradas += ["-loop", "1", "-framerate", str(fps), "-t", f"{dur:.3f}", "-i", png_t]
            ini, fim = janela_texto(s, dur)
            fc = (f"[0:v]{vf}[v];[2:v]format=rgba,fade=t=in:st={ini:.2f}:d=0.25:alpha=1,"
                  f"fade=t=out:st={fim-0.25:.2f}:d=0.25:alpha=1[m];"
                  f"[v][m]overlay=0:0:format=yuv420:eof_action=pass[vo]")
            mapa = ["-filter_complex", fc, "-map", "[vo]"]
        else:
            mapa = ["-vf", vf, "-map", "0:v"]
        ff(entradas + mapa + ["-map", "1:a", "-t", f"{dur:.3f}", "-c:v", "libx264",
                              "-crf", "28" if preview else "18", "-preset", "veryfast",
                              "-c:a", "aac", "-b:a", "160k", "-ar", "48000", saida])
        grava_chave(saida, h)
        return saida, dur, False

    # ---- vídeo real da fala
    dur = duracao(src)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", src], capture_output=True, text=True)
    sw = sh = None
    for ln in r.stderr.splitlines():
        if "Video:" in ln:
            for tk in ln.split(","):
                tk = tk.strip().split(" ")[0]
                if "x" in tk and tk.replace("x", "").isdigit():
                    sw, sh = map(int, tk.split("x")); break
    if ("rotation of -90" in r.stderr or "rotation of 90" in r.stderr) and sw > sh:
        sw, sh = sh, sw

    enq = s.get("enquadre", {})
    cadeia, _ = cadeia_enquadre(sw, sh, s.get("rotacao", 0.0), enq.get("zoom", 1.0),
                                enq.get("cx", 0.5), enq.get("cy", 0.5), W, H)
    vf = ([s["wb"]] if s.get("wb") else []) + cadeia
    vf += [f"scale={W}:{H}:flags=bicubic", cfg["look"]["comum"], f"fps={fps}", "format=yuv420p"]
    fc_v = ",".join(vf)

    srt = os.path.join(RAIZ, "falas", f"bloco{s['bloco']}.srt")
    if os.path.exists(srt):
        lg = cfg["legendas"]
        estilo = (f"FontName={lg['fonte']},FontSize={lg['tamanho']//2},"
                  f"PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,"
                  f"Outline={lg['contorno']//2},Shadow=0,BorderStyle=1,"
                  f"Alignment=2,MarginV={lg['margem_base']//2},MarginL=60,MarginR=60")
        fc_v += (f",subtitles='{srt}':fontsdir='{FONTES}':force_style='{estilo}'")

    entradas = ["-i", src]
    png = sobrepor_texto(s, idx, W, H, cfg)
    if png:
        entradas += ["-loop", "1", "-framerate", str(fps), "-t", f"{dur:.3f}", "-i", png]
        ini, fim = janela_texto(s, dur)
        fc = (f"[0:v]{fc_v}[v];[1:v]format=rgba,fade=t=in:st={ini:.2f}:d=0.25:alpha=1,"
              f"fade=t=out:st={fim-0.25:.2f}:d=0.25:alpha=1[m];"
              f"[v][m]overlay=0:0:format=yuv420:eof_action=pass[vo]")
        mapa = ["-filter_complex", fc, "-map", "[vo]"]
    else:
        mapa = ["-vf", fc_v, "-map", "0:v"]

    af = (f"highpass=f=85,afftdn=nr=10:nf=-30,"
          f"loudnorm=I={a['fala_lufs']}:TP=-1.5:LRA=9")
    ff(entradas + mapa + ["-map", "0:a", "-af", af, "-c:v", "libx264",
       "-crf", "28" if preview else "16", "-preset", "veryfast" if preview else "medium",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", saida])
    grava_chave(saida, h)
    return saida, dur, True


# ------------------------------------------------------------- áudio
def trilha_duckada(total, chave_wav, cfg, saida):
    mus = os.path.join(RAIZ, cfg["audio"]["musica"])
    a = cfg["audio"]
    if not os.path.exists(mus):
        print("  trilha ausente — faixa de música fica silenciosa (musica/LEIA-ME.md)")
        ff(["-f", "lavfi", "-i", f"anullsrc=r=48000:cl=stereo", "-t", f"{total:.3f}",
            "-c:a", "pcm_s16le", saida])
        return saida
    d = cfg["audio"]["ducking"]
    ff(["-stream_loop", "-1", "-i", mus, "-i", chave_wav, "-filter_complex",
        f"[0:a]atrim=0:{total:.3f},asetpts=N/SR/TB,aresample=48000,"
        f"volume={a['musica_db']}dB,afade=t=in:st=0:d=1.2,"
        f"afade=t=out:st={max(0,total-1.6):.2f}:d=1.6[m];"
        f"[1:a]aresample=48000[k];"
        f"[m][k]sidechaincompress=threshold={d['threshold']}:ratio={d['ratio']}:"
        f"attack={d['attack']}:release={d['release']}:makeup={d['makeup']}[o]",
        "-map", "[o]", "-t", f"{total:.3f}", "-c:a", "pcm_s16le", saida])
    return saida


# ------------------------------------------------------------- build
def build(preview, reaproveitar):
    global REAPROVEITAR
    REAPROVEITAR = reaproveitar
    cfg = json.load(open(os.path.join(RAIZ, "timeline.json")))
    fps = cfg["formato"]["fps"]
    W, H = (540, 960) if preview else (cfg["formato"]["w"], cfg["formato"]["h"])
    os.makedirs(CACHE, exist_ok=True); os.makedirs(SAIDA, exist_ok=True)
    os.makedirs(GRAF, exist_ok=True)

    print(f"\n{'='*66}\n  {cfg['projeto']}\n  {'PREVIEW ' + str(W) + 'x' + str(H) if preview else 'FINAL ' + str(W) + 'x' + str(H)}\n{'='*66}")
    partes, chaves, t = [], [], 0.0
    for i, s in enumerate(cfg["segmentos"]):
        if s["tipo"] == "broll":
            arq, dur = render_broll(s, cfg, W, H, fps, i, preview)
            real, marca = True, "B-ROLL  "
        else:
            arq, dur, real = render_fala(s, cfg, W, H, fps, i, preview)
            marca = "FALA    " if real else "cartela "
        partes.append(arq); chaves.append((dur, s["tipo"] == "fala" and real))
        rot = s.get("rotulo", f"bloco {s.get('bloco','')}")
        print(f"  {t:6.2f}s  {s['id']:3} {marca}{rot:24} {dur:5.2f}s"
              + ("" if s["tipo"] == "broll" or real else "  (placeholder)"))
        t += dur
    total = t
    print(f"  {'-'*58}\n  TOTAL {total:.2f}s")

    lista = os.path.join(CACHE, "lista.txt")
    with open(lista, "w") as fh:
        for p in partes:
            fh.write(f"file '{p}'\n")
    corpo = os.path.join(CACHE, "corpo.mp4")
    ff(["-f", "concat", "-safe", "0", "-i", lista, "-c", "copy", corpo])

    # chave do ducking: só as falas reais tocam
    pedacos = []
    for i, (dur, e_fala) in enumerate(chaves):
        w = os.path.join(CACHE, f"chave{i:02d}.wav")
        if e_fala:
            ff(["-i", partes[i], "-vn", "-af", "aresample=48000", "-t", f"{dur:.3f}",
                "-c:a", "pcm_s16le", w])
        else:
            ff(["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", f"{dur:.3f}",
                "-c:a", "pcm_s16le", w])
        pedacos.append(w)
    lk = os.path.join(CACHE, "lista_chave.txt")
    with open(lk, "w") as fh:
        for p in pedacos:
            fh.write(f"file '{p}'\n")
    chave = os.path.join(CACHE, "chave.wav")
    ff(["-f", "concat", "-safe", "0", "-i", lk, "-c", "copy", chave])

    mus = trilha_duckada(total, chave, cfg, os.path.join(CACHE, "musica.wav"))

    nome = "hugo-almeida_PREVIEW.mp4" if preview else "hugo-almeida_FINAL.mp4"
    final = os.path.join(SAIDA, nome)
    vb = (["-crf", "28", "-preset", "veryfast"] if preview else
          ["-crf", "18", "-preset", "slow", "-maxrate", "16M", "-bufsize", "32M",
           "-profile:v", "high", "-level", "4.1"])
    ff(["-i", corpo, "-i", mus, "-filter_complex",
        f"[0:a][1:a]amix=inputs=2:normalize=0:dropout_transition=0[x];"
        f"[x]loudnorm=I={cfg['audio']['master_lufs']}:TP=-1.3:LRA=11,"
        f"afade=t=out:st={max(0,total-0.8):.2f}:d=0.8[a]",
        "-map", "0:v", "-map", "[a]", "-c:v", "libx264"] + vb +
       ["-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart", "-t", f"{total:.3f}", final])
    tam = os.path.getsize(final) / 1e6
    print(f"\n  -> {os.path.relpath(final, RAIZ)}   {total:.2f}s · {tam:.1f} MB\n")
    return final


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", action="store_true", help="render rápido 540x960")
    ap.add_argument("--do-zero", action="store_true", help="limpa o cache antes")
    a = ap.parse_args()
    if a.do_zero and os.path.isdir(CACHE):
        shutil.rmtree(CACHE)
    build(a.preview, not a.do_zero)
