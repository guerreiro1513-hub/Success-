#!/usr/bin/env python3
"""Monta o corte a partir do timeline.json.

    python3 build.py                 # gera os dois cortes
    python3 build.py --versao limpo  # so o corte assistivel
    python3 build.py --estab         # liga a estabilizacao (ver aviso no codigo)

Pra integrar material novo NAO refaca nada: edite timeline.json
(troque um bloco "placeholder" por um bloco com "fonte"/"in", ou adicione
uma fonte nova em "fontes") e rode build.py de novo. As duracoes ficam na
grade de 0,6s, entao a trilha continua sincronizada.
"""
import argparse, hashlib, json, math, os, shutil, subprocess, sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
REN  = os.path.join(RAIZ, "_render")
FIM  = os.path.join(RAIZ, "08_FINAL")
GRAF = os.path.join(RAIZ, "06_GRAPHICS")
W, H, FPS = 1080, 1920, 30
DISS_BLOCO, DISS_MARCA = 0.2, 8 / 30      # so usados se timeline.json pedir


def ff(args, **kw):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y"] + args,
                       capture_output=True, text=True, **kw)
    if r.returncode:
        print("\n".join(["FALHA:", " ".join(args), r.stderr[-1600:]]))
        sys.exit(1)


def dur_fonte_ramp(dur, s0, s1):
    """Quanto de fonte consumir pra um speed ramp render 'dur' de saida."""
    return dur * (s1 - s0) / math.log(s1 / s0)


def expr_ramp(L, s0, s1):
    k = s1 - s0
    return f"setpts='({L}/{k})*log(1+({k})*T/({s0}*{L}))/TB'"


# --------------------------------------------------------------- um plano
def render_plano(s, tl, extra, versao, estab, marcadores, reaproveitar=True):
    saida = os.path.join(REN, f"{versao}_{s['id']}.mp4")
    dur = s["dur"] + extra

    # cache: so re-renderiza o plano que mudou. e o que faz integrar material
    # novo custar segundos em vez de refazer o corte inteiro.
    assin = json.dumps([s, tl["fontes"].get(s.get("fonte")), tl["show_look"],
                        extra, versao, estab, marcadores], sort_keys=True,
                       ensure_ascii=False)
    chave = hashlib.sha1(assin.encode()).hexdigest()
    cam_chave = os.path.join(REN, f"{versao}_{s['id']}.chave")
    if (reaproveitar and os.path.exists(saida) and os.path.exists(cam_chave)
            and open(cam_chave).read() == chave):
        print("     (reaproveitado do cache)")
        return saida

    if s.get("placeholder"):
        png = os.path.join(GRAF, f"slate_{s['slot']}.png")
        ff(["-loop", "1", "-i", png, "-t", f"{dur:.4f}", "-r", str(FPS),
            "-vf", f"scale={W}:{H},format=yuv420p", "-c:v", "libx264",
            "-crf", "16", "-preset", "medium", "-an", saida])
        open(cam_chave, "w").write(chave)
        return saida

    f = tl["fontes"][s["fonte"]]
    src = os.path.join(RAIZ, f["arquivo"])

    # quanto de fonte consumir
    if s.get("ramp"):
        s0, s1 = s["ramp"]
        L = dur_fonte_ramp(dur, s0, s1)
        tempo = expr_ramp(round(L, 4), s0, s1)
    elif s.get("speed"):
        L = dur * s["speed"]
        tempo = f"setpts={1/s['speed']:.6f}*PTS"
    else:
        L = dur
        tempo = "setpts=PTS"
    if s["in"] + L > f["dur_util"] + 0.02:
        print(f"  ! {s['id']}: fonte {s['fonte']} nao tem {L:.2f}s a partir de {s['in']}s")

    cadeia = []
    if estab and s.get("estab"):
        trf = os.path.join(REN, f"{versao}_{s['id']}.trf")
        ff(["-ss", f"{s['in']:.3f}", "-i", src, "-t", f"{L+0.2:.4f}",
            "-vf", f"vidstabdetect=shakiness=6:accuracy=14:result={trf}",
            "-f", "null", "-"])
        cadeia.append(f"vidstabtransform=input={trf}:smoothing=6:optzoom=1:"
                      f"zoom=3:crop=black:maxshift=16:interpol=bicubic")

    cadeia.append(f["grade"])
    cadeia.append(tl["show_look"])

    p = s.get("push", 1.0)
    if p and p > 1.001:
        nf = max(2, int(round(dur * FPS)))
        cadeia.append(f"scale={W*2}:{H*2}:flags=bicubic")
        cadeia.append(f"zoompan=z='1+{p-1:.4f}*on/{nf-1}':x='iw/2-(iw/zoom/2)':"
                      f"y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS}")
    else:
        cadeia.append(f"scale={W}:{H}")

    cadeia += [tempo, f"fps={FPS}", "format=yuv420p"]
    vf = ",".join(c for c in cadeia if c)

    # -ss/-t antes do -i sao opcoes de ENTRADA: limitam a leitura da fonte.
    args = ["-ss", f"{s['in']:.3f}", "-t", f"{L:.4f}", "-i", src]
    mk = os.path.join(GRAF, f"marcador_{s['id']}.png")
    if marcadores and os.path.exists(mk):
        # o PNG precisa virar stream com duracao, senao o fade nao tem frames
        args += ["-loop", "1", "-framerate", str(FPS), "-t", f"{dur:.4f}", "-i", mk,
                 "-filter_complex",
                 f"[0:v]{vf}[v];[1:v]format=rgba,fade=t=in:st=0.15:d=0.35:alpha=1,"
                 f"fade=t=out:st={max(0.5, dur-0.55):.2f}:d=0.35:alpha=1[m];"
                 f"[v][m]overlay=0:0:format=yuv420:eof_action=pass[vo]",
                 "-map", "[vo]"]
    else:
        args += ["-vf", vf]
    args += ["-t", f"{dur:.4f}", "-c:v", "libx264", "-crf", "15",
             "-preset", "medium", "-an", saida]
    ff(args)
    return saida


# ------------------------------------------------------------- transicoes
def mapa_dissolves(planos, ligado):
    """Onde entra dissolve. A referencia e corte seco em tudo, entao por padrao
    isso devolve so zeros — o campo "dissolves" no timeline.json e que liga."""
    if not ligado:
        return [0.0] * max(0, len(planos) - 1)
    d = []
    for i in range(len(planos) - 1):
        a, b = planos[i], planos[i + 1]
        if b.get("cta"):
            d.append(DISS_MARCA)
        elif bool(a.get("placeholder")) != bool(b.get("placeholder")):
            d.append(DISS_BLOCO)
        else:
            d.append(0.0)
    return d


# ------------------------------------------------------------------ audio
def garante_audio():
    """Os .wav sao gerados por script e nao vao pro git. Refaz o que faltar."""
    faltando = [
        (os.path.join(RAIZ, "04_MUSIC", "trilha-scratch-100bpm.wav"),
         os.path.join(RAIZ, "04_MUSIC", "make_music.py")),
        (os.path.join(RAIZ, "05_SOUND_DESIGN", "ambiencia.wav"),
         os.path.join(RAIZ, "05_SOUND_DESIGN", "make_sound.py")),
        (os.path.join(RAIZ, "05_SOUND_DESIGN", "transicoes_limpo.wav"),
         os.path.join(RAIZ, "05_SOUND_DESIGN", "make_sound.py")),
    ]
    for wav, script in faltando:
        if not os.path.exists(wav):
            print(f"  gerando {os.path.basename(wav)} ...")
            subprocess.run([sys.executable, script], check=True)


def monta_audio(versao, total, t_marca, saida, impacto):
    mus = os.path.join(RAIZ, "04_MUSIC", "trilha-scratch-100bpm.wav")
    amb = os.path.join(RAIZ, "05_SOUND_DESIGN", "ambiencia.wav")
    trs = os.path.join(RAIZ, "05_SOUND_DESIGN", f"transicoes_{versao}.wav")
    tmp = os.path.join(REN, f"musica_{versao}.wav")

    # a trilha tem o impacto da marca num tempo fixo. se o corte e mais curto,
    # tira compassos inteiros do meio pra assinatura cair no lugar certo.
    IMPACTO = impacto
    if abs(t_marca - IMPACTO) < 0.05:
        shutil.copy(mus, tmp)
    else:
        corte = IMPACTO - t_marca
        ff(["-i", mus, "-filter_complex",
            f"[0:a]atrim=0:{t_marca:.3f},asetpts=N/SR/TB[a];"
            f"[0:a]atrim={IMPACTO:.3f},asetpts=N/SR/TB[b];"
            f"[a][b]acrossfade=d=0.12:c1=tri:c2=tri[o]", "-map", "[o]", tmp])
        print(f"  musica remontada: -{corte:.1f}s do miolo (multiplo de compasso)")

    ff(["-i", tmp, "-i", amb, "-i", trs, "-filter_complex",
        f"[0:a]atrim=0:{total:.3f},asetpts=N/SR/TB,volume=1.0[m];"
        f"[1:a]atrim=0:{total:.3f},asetpts=N/SR/TB,volume=0.55[a];"
        f"[2:a]atrim=0:{total:.3f},asetpts=N/SR/TB,volume=1.0[t];"
        f"[m][a][t]amix=inputs=3:normalize=0:dropout_transition=0[x];"
        f"[x]loudnorm=I=-14:TP=-1.2:LRA=11,"
        f"afade=t=out:st={max(0,total-1.3):.2f}:d=1.3[o]",
        "-map", "[o]", "-ar", "48000", "-ac", "2", saida])


# ------------------------------------------------------------------ build
def build(versao, tl, estab, reaproveitar=True):
    marcadores = versao == "estrutura"
    planos = [s for s in tl["timeline"]
              if versao == "estrutura" or not s.get("placeholder")]
    diss = mapa_dissolves(planos, tl.get("dissolves", False))

    print(f"\n=== corte {versao.upper()} — {len(planos)} planos, "
          f"{sum(s['dur'] for s in planos):.1f}s ===")
    arqs = []
    for i, s in enumerate(planos):
        extra = diss[i] if i < len(diss) else 0.0
        print(f"  {s['id']:4} {s.get('rotulo',''):26} {s['dur']:.1f}s"
              + (f" +{extra:.2f}s dissolve" if extra else ""))
        arqs.append(render_plano(s, tl, extra, versao, estab, marcadores, reaproveitar))

    # grafo: concat nos cortes secos, xfade nos dissolves
    ins, fc, rot, n = [], [], None, 0
    acum = 0.0
    for i, (a, s) in enumerate(zip(arqs, planos)):
        ins += ["-i", a]
        fc.append(f"[{i}:v]settb=1/{FPS*1000},setpts=PTS-STARTPTS,fps={FPS}[c{i}]")
    rot, acum = "[c0]", planos[0]["dur"]
    for i in range(1, len(planos)):
        d = diss[i - 1]
        if d > 0:
            fc.append(f"{rot}[c{i}]xfade=transition=fade:duration={d:.4f}:"
                      f"offset={acum:.4f},settb=1/{FPS*1000},fps={FPS}[x{i}]")
            rot = f"[x{i}]"
        else:
            fc.append(f"{rot}[c{i}]concat=n=2:v=1:a=0,settb=1/{FPS*1000},fps={FPS}[x{i}]")
            rot = f"[x{i}]"
        acum += planos[i]["dur"]

    total = acum
    # CTA sobre a assinatura (so no corte estrutura)
    if versao == "estrutura":
        cta = os.path.join(GRAF, "cta_placeholder.png")
        t_cta = total - planos[-1]["dur"] + 0.5
        ins += ["-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}", "-i", cta]
        k = len(planos)
        fc.append(f"[{k}:v]format=rgba,fade=t=in:st={t_cta:.2f}:d=0.6:alpha=1,"
                  f"setpts=PTS-STARTPTS[cta]")
        fc.append(f"{rot}[cta]overlay=0:0:enable='gte(t,{t_cta:.2f})':format=yuv420[vf]")
        rot = "[vf]"
    fc.append(f"{rot}fade=t=out:st={total-0.45:.2f}:d=0.45,format=yuv420p[vout]")

    mudo = os.path.join(REN, f"video_{versao}.mp4")
    ff(ins + ["-filter_complex", ";".join(fc), "-map", "[vout]",
              "-t", f"{total:.3f}", "-c:v", "libx264", "-crf", "20",
              "-preset", "slow", "-an", mudo])

    t_marca = total - planos[-1]["dur"]
    aud = os.path.join(REN, f"audio_{versao}.wav")
    monta_audio(versao, total, t_marca, aud,
                tl["musica"].get("impacto_marca_s", 36.0))

    nome = {"estrutura": "MIDORI_ref-v2_ESTRUTURA.mp4",
            "limpo": "MIDORI_ref-v2_LIMPO.mp4"}[versao]
    final = os.path.join(FIM, nome)
    ff(["-i", mudo, "-i", aud, "-map", "0:v", "-map", "1:a",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart", "-shortest", final])
    print(f"  -> {os.path.relpath(final, RAIZ)}  ({total:.1f}s)")
    return final


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--versao", choices=["estrutura", "limpo", "ambas"], default="ambas")
    ap.add_argument("--estab", action="store_true",
                    help="liga a estabilizacao (vidstab). DESLIGADA por padrao: "
                         "neste material ela deforma a imagem — o pan da mao ja "
                         "e suave o bastante e o filtro tenta remover o proprio pan")
    ap.add_argument("--do-zero", action="store_true", help="ignora o cache de planos")
    a = ap.parse_args()
    os.makedirs(REN, exist_ok=True); os.makedirs(FIM, exist_ok=True)
    tl = json.load(open(os.path.join(RAIZ, "timeline.json")))
    garante_audio()
    alvos = ["estrutura", "limpo"] if a.versao == "ambas" else [a.versao]
    for v in alvos:
        build(v, tl, a.estab, not a.do_zero)
