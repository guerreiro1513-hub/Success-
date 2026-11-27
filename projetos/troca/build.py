#!/usr/bin/env python3
"""Guerreiro's Grill — "troca de carne" (match cut com a tábua girando). Reel 1080x1920, 30 fps.

Estrutura (tempos na grade da música da referência, 77 BPM, batida 0,778 s; o drop cai no início da série):
  0,00–2,40  GANCHO     IMG_1663 (churrasqueira girando)          texto ESTAMOS ABERTOS AGORA
  2,40–4,90  FACHADA    fachada.mov se existir; senão cartela FACHADA   texto GUERREIRO'S GRILL
  4,90–12,68 SÉRIE      5 planos de 2 batidas (1,556 s) com a tábua girando, cada entrada alinhada
                        automaticamente para continuar a posição do plano anterior (alignment_log.txt)
  12,68–16,57 CHURRASQUEIRA copy_CD6275E9 (frangos no rolete) + IMG_1663 (outro trecho)
  16,57–21,00 FECHO     IMG_1828 (costela com o garfo) + caixa PEDIDOS: WHATSAPP NA BIO + logo
Transições como na referência: clarão branco rápido entre os blocos; cortes secos (match cut) dentro da série.
Saídas: guerreiros-grill-troca-de-carne-v1.mp4 (sem música, para pôr o áudio no app) e
        guerreiros-grill-troca-de-carne-v1-COM-MUSICA.mp4 (música da referência, só para teste/uso por conta do cliente).
    ./build.sh            (refaz tudo; coloque fachada.mov na pasta e rode de novo)
"""
import json, math, os, subprocess, sys
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
from scipy.io import wavfile

ROOT = os.path.dirname(os.path.abspath(__file__)); P = lambda p: os.path.join(ROOT, p)
W, H, FPS, SR = 1080, 1920, 30, 48000
BEAT = 0.7782
SRC = {"hook": "source/IMG_1663.mov", "1818": "source/IMG_1818.mov", "1822": "source/IMG_1822.mov",
       "1881": "source/IMG_1881.mov", "brasa": "source/copy_CD6275E9-B57A-4CCD-A2A4-672BAF202896.mov",
       "payoff": "source/IMG_1828.mov", "music": "source/v09025g40000csvlbh7og65v09873et0.mp4",
       "facade": "fachada.mov"}
MUSIC_OFFSET = 1.29          # trecho da música = tempo do vídeo + 1,29 s (drop de 6,19 s cai no início da série, 4,90 s)
SERIES = [("1822", 1.0, 8.6), ("1881", 0.4, 6.9), ("1818", 2.4, 7.6), ("1822", 1.0, 8.6), ("1881", 0.4, 6.9)]
SEG = 2 * BEAT
FONT = P("assets/fonts/Montserrat.ttf")
RED = (200, 16, 46)


def ease(t): t = min(1, max(0, t)); return t * t * (3 - 2 * t)


def frames(src, start, n, scale_w=W, scale_h=H, gray=False):
    vf = f"scale={scale_w}:{scale_h}:force_original_aspect_ratio=increase:flags=lanczos,crop={scale_w}:{scale_h},fps={FPS}"
    vf += ",format=gray" if gray else ",format=rgb24"
    raw = subprocess.run(["ffmpeg", "-v", "error", "-threads", "2", "-ss", f"{max(0, start):.3f}", "-i", P(src), "-frames:v", str(n),
                          "-vf", vf, "-an", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    c = 1 if gray else 3
    a = np.frombuffer(raw, np.uint8)
    a = a.reshape(-1, scale_h, scale_w) if gray else a.reshape(-1, scale_h, scale_w, 3)
    out = list(a)
    while len(out) < n: out.append(out[-1])
    return out[:n]


def dur(src):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", P(src)],
                                capture_output=True, text=True).stdout)


# ---------------------------------------------------------------- alinhamento do match cut
def align():
    """Para cada junção: último quadro do plano que sai x cada quadro candidato do clipe que entra (miniatura 135x240
    cinza, diferença absoluta média, sem espelhar). O primeiro plano começa no ponto de giro mais nítido; não repete
    trecho já usado do mesmo clipe."""
    thumbs = {}
    for k in {s[0] for s in SERIES}:
        d = dur(SRC[k]); thumbs[k] = np.array(frames(SRC[k], 0, int(d * FPS), 135, 240, True), np.float32)
    nseg = int(round(SEG * FPS)); used = {k: [] for k in thumbs}; plan = []; log = []
    for i, (k, lo, hi) in enumerate(SERIES):
        T = thumbs[k]; cand = range(int(lo * FPS), int((hi - SEG) * FPS))
        cand = [c for c in cand if all(abs(c - u) > nseg for u in used[k])]
        if i == 0:
            m = np.abs(np.diff(T, axis=0)).mean((1, 2))          # começa onde a tábua está girando bem
            c = max(cand, key=lambda c: m[c:c + nseg].mean()); score = None
        else:
            last = prev_last
            # compara a forma geral (tábua e peça) e não a textura da carne: miniaturas bem desfocadas
            B = lambda x: cv2.GaussianBlur(x, (0, 0), 5)
            lb = B(last); scores = {c: np.abs(B(T[c]) - lb).mean() for c in cand}
            c = min(scores, key=scores.get); score = scores[c]
        used[k].append(c); plan.append((k, c / FPS))
        prev_last = T[min(len(T) - 1, c + nseg - 1)]
        log.append(f"plano {i + 1}: {k} entra em {c / FPS:.2f} s" + (f"  (diferença com o anterior {score:.1f})" if score is not None else "  (primeiro plano)"))
    open(P("alignment_log.txt"), "w").write("\n".join(log) + "\n")
    print("\n".join(log))
    return plan


# ---------------------------------------------------------------- texto
def text_img(text, size, weight=800, stroke=4, box=None, pad=24):
    while True:                                           # cabe na área segura (x 90–990 = 900 px)
        f = ImageFont.truetype(FONT, size); f.set_variation_by_axes([weight])
        l, t, r, b = f.getbbox(text, stroke_width=stroke)
        if r - l + 2 * pad <= 900 or size < 20: break
        size -= 2
    w, h = r - l + 2 * pad, b - t + 2 * pad
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if box: d.rounded_rectangle([0, 0, w - 1, h - 1], radius=int(h * 0.28), fill=box + (255,))
    d.text((pad - l, pad - t), text, font=f, fill=(255, 255, 255, 255), stroke_width=0 if box else stroke, stroke_fill=(0, 0, 0, 255))
    return np.array(im, np.float32)


def paste(f, img, cy, alpha, cx=W / 2):
    h, w = img.shape[:2]; x, y = int(cx - w / 2), int(cy - h / 2)
    x = max(90, min(x, 990 - w)) if w <= 900 else x       # área segura x 90–990
    a = img[..., 3:4] / 255 * alpha
    reg = f[y:y + h, x:x + w]; reg[:] = reg * (1 - a) + img[..., :3] * a


def main():
    plan = align()
    blocks = []   # (nome, fonte, início na fonte, nº de quadros)
    blocks.append(("hook", SRC["hook"], 0.0, 72))
    blocks.append(("facade", SRC["facade"] if os.path.exists(P(SRC["facade"])) else None, 0.0, 75))
    nseg = int(round(SEG * FPS))
    for k, t in plan: blocks.append(("serie", SRC[k], t, nseg))
    blocks.append(("brasa", SRC["brasa"], 0.30, 70))
    blocks.append(("brasa2", SRC["hook"], 5.0, 47))
    t_used = sum(b[3] for b in blocks)
    blocks.append(("payoff", SRC["payoff"], 0.2, 21 * FPS - t_used))
    # luminância média de cada bloco (para igualar exposição ±8%)
    lum = {}
    for name, src, st, n in blocks:
        if src: lum[(name, st)] = np.mean([g.mean() for g in frames(src, st, n, 135, 240, True)[::6]])
    target = np.median(list(lum.values()))
    texts = {
        "t1": (text_img("ESTAMOS ABERTOS AGORA", 78), 0.3, 2.4, 480),
        "t2": (text_img("GUERREIRO'S GRILL", 84), 2.55, 4.9, 1250),
        "t3": (text_img("PEDIDOS: WHATSAPP NA BIO", 64, box=RED), 17.2, 21.0, 1380),
    }
    lg = Image.open(P("assets/logo.png")).convert("RGBA"); lw = 230; lh = int(lg.height * lw / lg.width)
    logo = np.array(lg.resize((lw, lh), Image.LANCZOS), np.float32)
    slate = np.full((H, W, 3), 26, np.float32)
    s = text_img("FACHADA", 90, stroke=0); paste(slate, s, H / 2, 1.0)
    out = P("work/video.mp4")
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-threads", "2", "-pix_fmt", "yuv420p",
                            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", out], stdin=subprocess.PIPE)
    n0 = 0; cuts = []; flash_at = []
    for bi, (name, src, st, n) in enumerate(blocks):
        cuts.append((round(n0 / FPS, 2), name, os.path.basename(src) if src else "cartela", round(st, 2)))
        if name in ("facade", "brasa", "payoff") or (name == "serie" and blocks[bi - 1][0] == "facade"):
            flash_at.append(n0)
        fr = frames(src, st, n) if src else [None] * n
        g = 1.0
        if src: g = float(np.clip(target / max(1, lum[(name, st)]), 0.92, 1.08))
        for j in range(n):
            f = slate.copy() if fr[j] is None else fr[j].astype(np.float32)
            if src:
                f = f * g; f = (f - 128) * 1.04 + 128                      # exposição igualada, contraste +4%
            if name == "payoff" and j < 6:                                  # punch-in 105% no primeiro instante
                z = 1.05 - 0.05 * ease(j / 6)
                M = cv2.getRotationMatrix2D((W / 2, H / 2), 0, z); f = cv2.warpAffine(f, M, (W, H), borderMode=cv2.BORDER_REFLECT)
            t = (n0 + j) / FPS
            for key, (img, a, b, cy) in texts.items():
                if a <= t < b:
                    fi = 0.2 if key == "t3" else 0.15
                    paste(f, img, cy, ease((t - a) / fi) * ease((b - t) / 0.15) if key != "t3" else ease((t - a) / fi))
            if name == "payoff":
                q = ease((t - 16.9) / 0.3)                            # gráfico final: logo centralizado acima da caixa
                if q > 0:
                    a = logo[..., 3:4] / 255 * q; x0 = W // 2 - lw // 2; y0 = 1380 - 70 - lh - 30 + int((1 - q) * 20)
                    reg = f[y0:y0 + lh, x0:x0 + lw]; reg[:] = reg * (1 - a) + logo[..., :3] * a
            for fa in flash_at:                                             # clarão branco curto (como na referência)
                k = n0 + j - fa
                if -3 <= k < 5:
                    w_ = (1 - abs(k + 0.5) / 4.5) ** 1.5 * 0.85
                    f = f * (1 - w_) + 255 * w_
            enc.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes())
        n0 += n
        print(f"  {name}: {n} quadros", flush=True)
    enc.stdin.close(); enc.wait()
    total = n0 / FPS
    # ---------------- som
    def pcm(src, st, d):
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{st:.3f}", "-t", f"{d:.3f}", "-i", P(src), "-vn", "-ac", "2",
                              "-ar", str(SR), "-f", "s16le", "-"], capture_output=True).stdout
        x = np.frombuffer(raw, np.int16).reshape(-1, 2).astype(np.float32) / 32768
        return x
    def norm(x, db):
        r = np.sqrt((x ** 2).mean()) + 1e-9; return x * (10 ** (db / 20) / r)
    N = int(total * SR); A = np.zeros((N, 2), np.float32)
    bed = norm(pcm(SRC["hook"], 0, 8.2), -28)
    pos = 0
    while pos < N:                                                          # cama contínua do som da churrasqueira
        m = min(len(bed), N - pos); A[pos:pos + m] += bed[:m]
        if pos + m >= N: break
        pos += m - int(0.5 * SR)
    n0 = 0
    for name, src, st, n in blocks:
        d = n / FPS; i = int(n0 / FPS * SR)
        if src and name in ("hook", "brasa", "brasa2", "payoff"):
            x = norm(pcm(src, st, d), -20)[:N - i]; fd = int(0.1 * SR)
            x[:fd] *= np.linspace(0, 1, fd)[:, None]; x[-fd:] *= np.linspace(1, 0, fd)[:, None]
            A[i:i + len(x)] += x
        n0 += n
    fo = int(0.8 * SR); A[-fo:] *= np.linspace(1, 0, fo)[:, None]
    def finish(mix, name):
        wav = P(f"work/{name}.wav"); wavfile.write(wav, SR, (np.clip(mix, -1, 1) * 32767).astype(np.int16))
        o = P(f"{name}.mp4")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", out, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                        "-af", "volume=-0.8dB,alimiter=limit=0.80:level=0", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", o], check=True)
        return o
    o1 = finish(A, "guerreiros-grill-troca-de-carne-v1")
    mus = pcm(SRC["music"], MUSIC_OFFSET, total)[:N]
    mus = np.pad(mus, ((0, N - len(mus)), (0, 0)))
    mus[-fo:] *= np.linspace(1, 0, fo)[:, None]
    o2 = finish(A * 0.55 + mus * 0.75, "guerreiros-grill-troca-de-carne-v1-COM-MUSICA")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "0.5", "-i", o1, "-frames:v", "1", "-q:v", "2", P("thumbnail.jpg")], check=True)
    json.dump({"duracao": total, "cortes": cuts}, open(P("cortes.json"), "w"), ensure_ascii=False, indent=2)
    print(o1, o2, f"{total:.2f} s")


if __name__ == "__main__":
    main()
