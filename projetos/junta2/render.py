#!/usr/bin/env python3
"""Aviso do Guerreiro's Grill no Auto Posto Florais: fala (2 tomadas) + churrasqueira abrindo, com legenda.
Tudo configurado em timeline.json.   python3 render.py [--preview]

Legenda: o texto vem do cliente; o tempo de cada trecho vem do detector de voz (silero VAD, já na máquina)
e as palavras são distribuídas dentro do trecho pelo número de sílabas.
"""
import json, math, os, re, subprocess, sys
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
ROOT = os.path.dirname(os.path.abspath(__file__))
P = lambda p: os.path.join(ROOT, p)
SAFE = {"x0": 70, "x1": 160, "y0": 230, "y1": 420}


def ease_out(t): t = min(1, max(0, t)); return 1 - (1 - t) ** 3
def ease_io(t): t = min(1, max(0, t)); return t * t * (3 - 2 * t)


def syllables(w):
    w = w.lower()
    return max(1, len(re.findall(r"[aeiouáéíóúâêôãõà]+", w)))


# ---------------------------------------------------------------- tempo das palavras
def word_times(tl):
    """Cada trecho de fala (texto + [ini, fim] no relógio global) vira palavras com tempo próprio."""
    words = []
    for seg in tl["speech"]:
        ws = seg["text"].split()
        a, b = seg["t"]
        tot = sum(syllables(w) for w in ws)
        t = a
        for w in ws:
            d = (b - a) * syllables(w) / tot
            words.append({"w": w, "a": t, "b": t + d}); t += d
    return words


# ---------------------------------------------------------------- vídeo
def clip_reader(c, W, H, fps, grade):
    zoom = c.get("zoom", [1.0, 1.0])
    vf = f"{grade},scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},fps={fps},format=rgb24"
    n = int(round((c["out"] - c["in"]) * fps))
    p = subprocess.Popen([FF, "-v", "error", "-ss", f"{c['in']:.3f}", "-i", P(c["src"]), "-frames:v", str(n),
                          "-vf", vf, "-an", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    last = None
    for j in range(n):
        b = p.stdout.read(W * H * 3)
        if len(b) < W * H * 3:
            f = last
        else:
            f = np.frombuffer(b, np.uint8).reshape(H, W, 3); last = f
        z = zoom[0] + (zoom[1] - zoom[0]) * ease_io(j / max(1, n - 1))
        if abs(z - 1) > 1e-3:
            M = cv2.getRotationMatrix2D((W / 2, H * c.get("zoom_cy", 0.42)), 0, z)
            f = cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
        yield f.copy()
    p.wait()


# ---------------------------------------------------------------- tipografia
def font(path, size, weight=None):
    f = ImageFont.truetype(P(path), max(8, int(size)))
    if weight:
        try: f.set_variation_by_axes([weight])
        except Exception: pass
    return f


_CACHE = {}
def text_img(text, path, size, weight, color, s, max_w, tracking=0.0):
    key = (text, path, size, weight, tuple(color) if isinstance(color, list) else color, s, max_w)
    if key in _CACHE: return _CACHE[key]
    size *= s
    while True:
        f = font(path, size, weight); sp = f.size * tracking
        w = sum(f.getlength(c) for c in text) + sp * (len(text) - 1)
        if w <= max_w or size < 10: break
        size *= max_w / w * 0.98
    a, d = f.getmetrics(); pad = int(26 * s)
    Wl, Hl = int(w) + 2 * pad, a + d + 2 * pad
    m = Image.new("L", (Wl, Hl), 0); dr = ImageDraw.Draw(m); x = pad
    for c in text:
        dr.text((x, pad), c, font=f, fill=255); x += f.getlength(c) + sp
    A = np.array(m, np.float32) / 255
    if color == "fire":
        yy = np.clip((np.arange(Hl)[:, None] - pad - a * 0.2) / (a * 0.9), 0, 1)[..., None]
        rgb = np.array([255, 208, 84.]) * (1 - yy) + np.array([238, 98, 20.]) * yy
    else:
        rgb = np.array(color if isinstance(color, list) else [255, 252, 246], np.float32)[None, None]
    rgb = np.broadcast_to(rgb, (Hl, Wl, 3)).astype(np.float32)
    # sombra em camadas (contato curto + difusa larga), sem contorno duro
    sh = np.maximum(np.roll(cv2.GaussianBlur(A, (0, 0), 2.0 * s), int(3 * s), 0) * 0.75,
                    np.roll(cv2.GaussianBlur(A, (0, 0), 12 * s), int(9 * s), 0) * 0.55)
    out = (rgb, A, sh, Wl, Hl)
    _CACHE[key] = out
    return out


def paste(f, img, cx, cy, alpha=1.0, scale=1.0):
    rgb, A, sh, w, h = img
    if alpha <= 0: return
    if abs(scale - 1) > 1e-3:
        w2, h2 = max(2, int(w * scale)), max(2, int(h * scale))
        rgb = cv2.resize(rgb, (w2, h2)); A = cv2.resize(A, (w2, h2)); sh = cv2.resize(sh, (w2, h2)); w, h = w2, h2
    x, y = int(cx - w / 2), int(cy - h / 2)
    H, W = f.shape[:2]
    xa, ya, xb, yb = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if xb <= xa or yb <= ya: return
    sl = (slice(ya - y, yb - y), slice(xa - x, xb - x))
    reg = f[ya:yb, xa:xb]
    reg *= 1 - (sh[sl] * alpha)[..., None]
    a = (A[sl] * alpha)[..., None]
    f[ya:yb, xa:xb] = reg * (1 - a) + rgb[sl] * a


def captions(f, t, tl, s, words):
    H, W = f.shape[:2]
    C = tl["captions"]
    max_w = (1080 - 2 * SAFE["x1"]) * s
    for g in C["groups"]:
        a = words[g["w"][0]]["a"] - 0.04; b = words[g["w"][1]]["b"] + g.get("hold", 0.12)
        if not (a <= t < b + 0.12): continue
        txt = " ".join(words[i]["w"] for i in range(g["w"][0], g["w"][1] + 1)).upper().rstrip(",.")
        hot = g.get("hot", False)
        img = text_img(txt, C["font"], C["size_hot"] if hot else C["size"], C.get("weight", 800),
                       "fire" if hot else "white", s, max_w, C.get("tracking", 0.01))
        k = (t - a) * tl["fps"]
        p = ease_out(k / 7)                       # entrada ~0,23 s: escala 0,86 -> 1 e opacidade
        out = ease_io(min(1, (b + 0.12 - t) / 0.12))
        paste(f, img, W / 2, C["cy"] * H, p * out, 0.86 + 0.14 * p)


def chips(f, t, tl, s, words):
    """Dias da semana acendendo um a um, na hora em que ele fala cada um."""
    D = tl["days"]
    a0 = words[D["words"][0]]["a"] - 0.05
    end = words[D["words"][-1]]["b"] + D.get("hold", 0.9)
    if not (a0 <= t < end + 0.2): return
    H, W = f.shape[:2]
    out = ease_io(min(1, (end + 0.2 - t) / 0.2))
    labels = D["labels"]
    size = D["size"]
    while True:                                   # a fileira inteira cabe entre as margens seguras (x 70..920)
        imgs = [text_img(l, D["font"], size, 800, "white", s, 9999, 0.04) for l in labels]
        gap = 14 * s * size / 40
        padx, pady = 22 * s * size / 40, 11 * s * size / 40
        widths = [im[3] - 2 * int(26 * s) + 2 * padx for im in imgs]
        total = sum(widths) + gap * (len(widths) - 1)
        if total <= (1080 - SAFE["x0"] - SAFE["x1"]) * s * 0.96 or size < 14: break
        size -= 2
    x = (SAFE["x0"] * s + W - SAFE["x1"] * s) / 2 - total / 2; cy = D["cy"] * H
    for i, (l, im, wd) in enumerate(zip(labels, imgs, widths)):
        ta = words[D["words"][i]]["a"] - 0.03
        q = ease_out((t - ta) * tl["fps"] / 6)
        if q > 0:
            hot = i == len(labels) - 1
            h = im[4] - 2 * int(26 * s) + 2 * pady
            x0, y0 = int(x), int(cy - h / 2)
            x1, y1 = int(x + wd), int(cy + h / 2)
            sc = 0.8 + 0.2 * q
            cxm, cym = (x0 + x1) / 2, cy
            bx0, by0 = int(cxm - (x1 - x0) * sc / 2), int(cym - (y1 - y0) * sc / 2)
            bx1, by1 = int(cxm + (x1 - x0) * sc / 2), int(cym + (y1 - y0) * sc / 2)
            # sombra difusa da pílula + pílula (vermelho da marca, a última dourada)
            m = np.zeros(f.shape[:2], np.float32)
            cv2.rectangle(m, (bx0, by0 + int(6 * s)), (bx1, by1 + int(6 * s)), 1, -1)
            m = cv2.GaussianBlur(m, (0, 0), 10 * s) * 0.45 * q * out
            f *= (1 - m[..., None])
            col = np.array([232, 170, 40.] if hot else [196, 30, 34.])
            pill = np.zeros(f.shape[:2], np.uint8)
            r = int((by1 - by0) / 2)
            cv2.rectangle(pill, (bx0 + r, by0), (bx1 - r, by1), 255, -1, cv2.LINE_AA)
            cv2.circle(pill, (bx0 + r, (by0 + by1) // 2), r, 255, -1, cv2.LINE_AA)
            cv2.circle(pill, (bx1 - r, (by0 + by1) // 2), r, 255, -1, cv2.LINE_AA)
            a = (pill / 255.0 * q * out)[..., None]
            f[:] = f * (1 - a) + col * a
            paste(f, (im[0], im[1], im[2] * 0, im[3], im[4]), cxm, cym, q * out, sc)
        x += wd + gap


def end_card(f, t, tl, s):
    E = tl["end_card"]
    if t < E["start"]: return
    H, W = f.shape[:2]
    k = (t - E["start"]) * tl["fps"]
    g = E.get("shade", 0.5) * ease_out(k / 10)
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    f *= 1 - g * (0.55 + 0.45 * np.exp(-((yy - 0.36) / 0.24) ** 2))
    if not hasattr(end_card, "logo"):
        lg = Image.open(P(E["logo"])).convert("RGBA")
        lh = int(E["logo_h"] * H); lw = int(lg.width * lh / lg.height)
        end_card.logo = np.array(lg.resize((lw, lh), Image.LANCZOS), np.float32)
    L = end_card.logo; lh, lw = L.shape[:2]
    p = ease_out(k / 9)
    if p > 0:
        sc = 0.9 + 0.1 * p
        w2, h2 = int(lw * sc), int(lh * sc)
        Lg = cv2.resize(L, (w2, h2), interpolation=cv2.INTER_AREA)
        x0, y0 = W // 2 - w2 // 2, int(E["logo_cy"] * H) - h2 // 2
        a = Lg[..., 3:4] / 255 * p
        sub = f[y0:y0 + h2, x0:x0 + w2]
        sub *= 1 - cv2.GaussianBlur(a[..., 0], (0, 0), 16 * s)[..., None] * 0.55
        sub[:] = sub * (1 - a) + Lg[..., :3] * a
    max_w = (1080 - 2 * SAFE["x1"]) * s
    for i, L_ in enumerate(E["lines"]):
        q = ease_out((k - 7 - i * 4) / 7)
        if q <= 0: continue
        img = text_img(L_["text"], L_["font"], L_["size"], L_.get("weight"), L_.get("color", "white"), s, max_w, L_.get("tracking", 0))
        paste(f, img, W / 2, L_["cy"] * H + (1 - q) * 24 * s, q)


# ---------------------------------------------------------------- áudio
def build_audio(tl, out):
    A = tl["audio"]; cl = tl["clips"]
    inp, fc = [], []
    for i, c in enumerate(cl):
        inp += ["-ss", f"{c['in']:.3f}", "-t", f"{c['out'] - c['in']:.3f}", "-i", P(c["src"])]
        fc.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,volume={c.get('vol', 1.0)}[a{i}]")
    cur = "a0"
    for i in range(1, len(cl)):
        d = cl[i - 1].get("xfade", 0.0)
        nxt = f"x{i}"
        if d > 0: fc.append(f"[{cur}][a{i}]acrossfade=d={d}:c1=tri:c2=tri[{nxt}]")
        else: fc.append(f"[{cur}][a{i}]concat=n=2:v=0:a=1[{nxt}]")
        cur = nxt
    fc.append(f"[{cur}]highpass=f=80,loudnorm=I=-13:TP=-1.5:LRA=9,asplit[vz][sc]")
    m = len(cl)
    inp += ["-stream_loop", "-1", "-i", P(A["music"])]
    fc.append(f"[{m}:a]aresample=48000,volume={A['music_db']}dB,afade=t=in:d=0.8[mu0];"
              f"[mu0][sc]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=350[mu];"
              f"[vz][mu]amix=inputs=2:duration=first:normalize=0,afade=t=out:st={A['total'] - 1.2}:d=1.2[a]")
    subprocess.run([FF, "-y", "-v", "error"] + inp + ["-filter_complex", ";".join(fc), "-map", "[a]",
                    "-t", f"{A['total']:.3f}", "-c:a", "pcm_s16le", out], check=True)


def main():
    preview = "--preview" in sys.argv
    tl = json.load(open(P("timeline.json")))
    fps = tl["fps"]; o = tl["output"]
    s = 0.5 if preview else 1.0
    W, H = int(1080 * s) // 2 * 2, int(1920 * s) // 2 * 2
    out = P(o["preview"] if preview else o["file"])
    words = word_times(tl)
    # quadros: clipes em sequência, dissolve onde o clipe anterior pede 'xfade'
    total_frames = 0
    lens = [int(round((c["out"] - c["in"]) * fps)) for c in tl["clips"]]
    xf = [int(round(c.get("xfade", 0) * fps)) for c in tl["clips"]]
    total = sum(lens) - sum(xf[:-1])
    tl["audio"]["total"] = total / fps
    os.makedirs(P("work"), exist_ok=True)
    wav = P("work/audio.wav"); build_audio(tl, wav)
    enc = [FF, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
           "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p",
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]
    enc += (["-preset", "veryfast", "-crf", "24"] if preview else
            ["-preset", "slow", "-crf", "17", "-maxrate", "14M", "-bufsize", "24M", "-profile:v", "high", "-level", "4.1"])
    enc += ["-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", out]
    pe = subprocess.Popen(enc, stdin=subprocess.PIPE)
    n = 0; tail = []
    cuts = []
    for ci, c in enumerate(tl["clips"]):
        cuts.append({"t": round(n / fps, 3), "src": os.path.basename(c["src"])})
        prev_x = xf[ci - 1] if ci else 0
        for j, fr in enumerate(clip_reader(c, W, H, fps, tl["grade"])):
            f = fr.astype(np.float32)
            if j < prev_x and tail:              # dissolve com o fim do clipe anterior
                w_ = (j + 1) / (prev_x + 1)
                f = tail[j] * (1 - w_) + f * w_
            elif j < prev_x: pass
            if j >= lens[ci] - xf[ci] and ci < len(tl["clips"]) - 1:
                if j == lens[ci] - xf[ci]: tail = []
                tail.append(f.copy()); continue
            t = n / fps
            captions(f, t, tl, s, words)
            chips(f, t, tl, s, words)
            end_card(f, t, tl, s)
            pe.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes()); n += 1
    pe.stdin.close(); pe.wait()
    json.dump({"duracao": round(n / fps, 3), "cortes": cuts,
               "palavras": [{"w": w["w"], "a": round(w["a"], 2)} for w in words]},
              open(out + ".cortes.json", "w"), ensure_ascii=False, indent=2)
    print(f"{out}  {n} quadros = {n / fps:.2f} s")


if __name__ == "__main__":
    main()
