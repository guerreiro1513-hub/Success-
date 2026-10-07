#!/usr/bin/env python3
"""Guerreiro's Grill — tour pelas unidades. Lê timeline.json e renderiza.

    python3 render.py --preview     # prévia em baixa resolução (rápida)
    python3 render.py               # final 1080x1920, 30 fps, H.264 + AAC

Pipeline por clipe: o FFmpeg decodifica só o trecho usado (corrige rotação,
escala e corta para 9:16, aplica a correção do clipe e o look da marca); o Python
monta a rampa de velocidade quadro a quadro (fontes de 60 fps dão câmera lenta
real), aplica as transições de câmera (whip com desfoque direcional e zoom com
desfoque radial), os títulos e o encerramento, e manda os quadros para o
encoder. O som é só ambiente dos próprios clipes + whooshes sutis (sem música).
Gera também <saida>.cortes.json com os tempos de cada corte, para sincronizar a
música depois.
"""
import json, math, os, subprocess, sys
import numpy as np, cv2
import scipy.io.wavfile as wavfile, scipy.signal as sg
from PIL import Image, ImageDraw, ImageFont

FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
ROOT = os.path.dirname(os.path.abspath(__file__))
SR = 48000


def P(p):
    return p if os.path.isabs(p) else os.path.join(ROOT, p)


def ease_in(t):  return t * t
def ease_out(t): return 1 - (1 - t) ** 3


# ---------------------------------------------------------------- decodificação
def src_fps(path):
    r = subprocess.run([FF, "-i", P(path)], capture_output=True, text=True).stderr
    import re
    m = re.search(r"(\d+(?:\.\d+)?) fps", r)
    return float(m.group(1)) if m else 30.0


def clip_frames(clip, W, H, fps, look):
    """Lista de quadros RGB (uint8, HxWx3) já na velocidade da timeline."""
    segs = clip["segments"]
    t0 = min(s[0] for s in segs); t1 = max(s[1] for s in segs)
    sf = src_fps(clip["file"])
    rf = clip.get("reframe", {"zoom": 1.0, "x": 0.5, "y": 0.5})
    z = rf.get("zoom", 1.0)
    zw, zh = int(math.ceil(W * z / 2) * 2), int(math.ceil(H * z / 2) * 2)
    chain = [f"scale={zw}:{zh}:force_original_aspect_ratio=increase:flags=lanczos",
             f"crop={W}:{H}:(iw-{W})*{rf.get('x', 0.5)}:(ih-{H})*{rf.get('y', 0.5)}"]
    if clip.get("hflip"): chain.append("hflip")
    if clip.get("fix"): chain.append(clip["fix"])
    if look: chain.append(look)
    chain.append("format=rgb24")
    cmd = [FF, "-v", "error", "-ss", f"{t0:.3f}", "-t", f"{t1 - t0 + 0.1:.3f}", "-i", P(clip["file"]),
           "-vf", ",".join(chain), "-fps_mode", "passthrough", "-f", "rawvideo", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    src = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    out = []
    for a, b, sp in segs:
        n = max(1, int(round((b - a) / sp * fps)))
        for i in range(n):
            t = a + i * sp / fps
            k = min(len(src) - 1, max(0, int(round((t - t0) * sf))))
            out.append(src[k])
    return out


# ---------------------------------------------------------------- transições
def shift_blur(img, d0, d1, ang, samples):
    """Desloca a imagem de d0 a d1 px na direção ang (graus) com rastro (motion blur)."""
    H, W = img.shape[:2]
    c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    acc = np.zeros(img.shape, np.float32)
    for i in range(samples):
        d = d0 + (d1 - d0) * (i + 0.5) / samples
        M = np.float32([[1, 0, c * d], [0, 1, s * d]])
        acc += cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return (acc / samples).astype(np.uint8)


def zoom_blur(img, s0, s1, samples, cx=0.5, cy=0.5):
    H, W = img.shape[:2]
    acc = np.zeros(img.shape, np.float32)
    for i in range(samples):
        s = s0 + (s1 - s0) * (i + 0.5) / samples
        M = cv2.getRotationMatrix2D((W * cx, H * cy), 0, s)
        acc += cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return (acc / samples).astype(np.uint8)


def apply_out(frames, tr, W, samples):
    """Fim do clipe A: a câmera acelera na direção do movimento até o corte."""
    if not tr or tr["type"] == "cut": return
    k = tr.get("frames", 5); k = min(k, len(frames))
    for j in range(k):
        p0, p1 = j / k, (j + 1) / k
        i = len(frames) - k + j
        if tr["type"] == "whip":
            D = tr.get("amount", 0.5) * W
            frames[i] = shift_blur(frames[i], D * ease_in(p0), D * ease_in(p1), tr["dir"], samples)
        elif tr["type"] == "zoom":
            Z = tr.get("amount", 0.5)
            frames[i] = zoom_blur(frames[i], 1 + Z * ease_in(p0), 1 + Z * ease_in(p1), samples, tr.get('cx', 0.5), tr.get('cy', 0.5))


def apply_in(frames, tr, W, samples):
    """Começo do clipe B: o mesmo movimento chega do lado oposto e desacelera."""
    if not tr or tr["type"] == "cut": return
    k = tr.get("frames", 5); k = min(k, len(frames))
    for j in range(k):
        p0, p1 = 1 - j / k, 1 - (j + 1) / k
        if tr["type"] == "whip":
            D = tr.get("amount", 0.5) * W
            frames[j] = shift_blur(frames[j], -D * ease_in(p0), -D * ease_in(p1), tr["dir"], samples)
        elif tr["type"] == "zoom":
            Z = tr.get("amount", 0.5)
            frames[j] = zoom_blur(frames[j], 1 + Z * ease_in(p0), 1 + Z * ease_in(p1), samples, tr.get('in_cx', 0.5), tr.get('in_cy', 0.5))


# ---------------------------------------------------------------- tipografia
class Type:
    def __init__(self, cfg, scale):
        self.c, self.s = cfg, scale
        self.fname = ImageFont.truetype(P(cfg["font_name"]), int(cfg["name_size"] * scale))
        self.flabel = ImageFont.truetype(P(cfg["font_label"]), int(cfg["label_size"] * scale))
        try: self.flabel.set_variation_by_axes([cfg.get("label_weight", 500)])
        except Exception: pass

    def line(self, text, font, tracking, color):
        """Texto com espaçamento entre letras, em RGBA, com sombra suave."""
        sp = font.size * tracking
        widths = [font.getlength(ch) for ch in text]
        w = int(sum(widths) + sp * (len(text) - 1)) + 8
        asc, desc = font.getmetrics(); h = asc + desc + 8
        im = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0)); sh = im.copy()
        x = 20
        for ch, cw in zip(text, widths):
            ImageDraw.Draw(sh).text((x + 2, 24), ch, font=font, fill=(0, 0, 0, 150))
            ImageDraw.Draw(im).text((x, 20), ch, font=font, fill=tuple(color) + (255,))
            x += cw + sp
        from PIL import ImageFilter
        return Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(max(1, int(6 * self.s)))), im)

    def block(self, lines, align):
        c = self.c
        L = self.line(lines[0], self.flabel, c["label_tracking"], c["color"])
        N = self.line(lines[1], self.fname, c["name_tracking"], c["color"])
        return L, N

    def draw(self, canvas, lines, f, n, align="left", y=None):
        """f = quadro atual dentro do título, n = duração em quadros.
        Entrada: régua dourada cresce, linhas sobem de trás de uma máscara.
        Saída: sobem um pouco e somem."""
        c, s = self.c, self.s
        L, N = self.block(lines, align)
        W = canvas.width
        x0 = int(c["x"] * s); y0 = int((y if y is not None else c["y"]) * s)
        ex = max(0.0, (f - (n - 7)) / 7)                      # saída
        alpha = 1 - ease_out(ex); lift = int(-30 * s * ease_out(ex))
        # régua
        rw = int(110 * s * ease_out(min(1, f / 9)))
        if rw > 0:
            rx = x0 if align == "left" else (W - int(110 * s)) // 2
            ImageDraw.Draw(canvas).rectangle([rx, y0 + lift, rx + rw, y0 + lift + max(2, int(4 * s))],
                                             fill=tuple(c["accent"]) + (int(255 * alpha),))
        ly = y0 + int(16 * s); ny = ly + L.height - int(30 * s)
        for img, yy, delay in ((L, ly, 2), (N, ny, 5)):
            p = ease_out(min(1, max(0, (f - delay) / 9)))
            if p <= 0: continue
            off = int((1 - p) * img.height * 0.9)
            crop = img.crop((0, 0, img.width, img.height - off))   # máscara: sobe "de trás" da linha
            if alpha < 1:
                a = np.array(crop); a[..., 3] = (a[..., 3] * alpha).astype(np.uint8); crop = Image.fromarray(a)
            xx = x0 - 20 if align == "left" else (W - img.width) // 2
            canvas.alpha_composite(crop, (xx, yy + off + lift))


def composite(frame, layer):
    a = np.asarray(layer, dtype=np.float32)
    al = a[..., 3:4] / 255.0
    return (frame * (1 - al) + a[..., :3] * al).astype(np.uint8)


def gradient(H, W, strength, top=False):
    g = np.linspace(0, 1, H, dtype=np.float32)
    g = np.clip((g - 0.45) / 0.55, 0, 1) if not top else np.clip((0.4 - g) / 0.4, 0, 1)
    return (g ** 1.4 * strength)[:, None, None]


# ---------------------------------------------------------------- som
def whoosh(dur=0.42, peak=0.30):
    n = int(dur * SR); t = np.arange(n) / SR
    noise = np.random.default_rng(7).standard_normal(n)
    lo = sg.lfilter(*sg.butter(2, 900 / (SR / 2)), noise)
    hi = sg.lfilter(*sg.butter(2, [900 / (SR / 2), 5000 / (SR / 2)], "band"), noise)
    mix = np.clip(t / peak, 0, 1)                     # abre o brilho até o pico
    x = lo * (1 - mix) + hi * mix * 0.8
    env = np.where(t < peak, (t / peak) ** 2.2, np.exp(-(t - peak) * 22))
    x = x * env; x /= np.abs(x).max() + 1e-9
    return np.stack([x, x * 0.92], 1), int(peak * SR)


def hit(dur=0.7):
    n = int(dur * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * (52 - 18 * t) * t) * np.exp(-t * 6) * (1 - np.exp(-t * 300))
    return np.stack([x, x], 1) / np.abs(x).max()


def ambience(clip, out_start, nfr, fps, total_n, db):
    if db is None or db <= -59: return None
    a, _, _ = clip["segments"][0]
    dur = nfr / fps
    r = subprocess.run([FF, "-v", "error", "-ss", f"{a:.3f}", "-t", f"{dur:.3f}", "-i", P(clip["file"]),
                        "-vn", "-ac", "2", "-ar", str(SR), "-af", "highpass=f=80", "-f", "s16le", "-"],
                       capture_output=True).stdout
    x = np.frombuffer(r, np.int16).astype(np.float32).reshape(-1, 2) / 32768
    if len(x) == 0: return None
    k = min(int(0.03 * SR), len(x) // 2)
    x[:k] *= np.linspace(0, 1, k)[:, None]; x[-k:] *= np.linspace(1, 0, k)[:, None]
    rms = np.sqrt(np.mean(x ** 2)) + 1e-9
    return x / rms * 10 ** (db / 20)


# ---------------------------------------------------------------- render
def main():
    preview = "--preview" in sys.argv
    tl = json.load(open(os.path.join(ROOT, "timeline.json")))
    o = tl["output"]; fps = o["fps"]
    sc = o.get("preview_scale", 0.5) if preview else 1.0
    W, H = int(o["w"] * sc) // 2 * 2, int(o["h"] * sc) // 2 * 2
    samples = 8 if preview else 16
    out_path = P(o["preview_file"] if preview else o["file"])
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    look = tl.get("look", {}).get("filters", "")
    T = Type(tl["typography"], sc)

    # sequência de clipes com o título/legenda de cada unidade
    seq = []
    if tl.get("opening", {}).get("enabled") and tl["opening"].get("clip"):
        seq.append({"clip": tl["opening"]["clip"], "loc": None})
    for loc in tl["locations"]:
        for i, c in enumerate(loc["clips"]):
            seq.append({"clip": c, "loc": loc, "title": i == loc.get("title_clip", 0)})
    if not seq: sys.exit("timeline sem clipes")
    end = tl.get("ending")
    if end and end.get("tail"):
        seq.append({"clip": end["tail"], "loc": None, "ending": True})

    enc = [FF, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps),
           "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p",
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]
    enc += (["-preset", "veryfast", "-crf", "24"] if preview else
            ["-preset", "slow", "-crf", "17", "-maxrate", "14M", "-bufsize", "24M", "-profile:v", "high", "-level", "4.1"])
    tmpv = out_path + ".video.mp4"
    pe = subprocess.Popen(enc + [tmpv], stdin=subprocess.PIPE)

    cuts, trans_times, amb_list = [], [], []
    frame_no = 0
    prev_out = None
    for idx, item in enumerate(seq):
        c = item["clip"]
        fr = clip_frames(c, W, H, fps, look)
        apply_in(fr, prev_out, W, samples)
        apply_out(fr, c.get("transition_out"), W, samples)
        if prev_out and prev_out.get("type") != "cut":
            trans_times.append(frame_no / fps)
        cuts.append({"t": round(frame_no / fps, 3), "clip": os.path.basename(c["file"]),
                     "unidade": item["loc"]["name"] if item.get("loc") else ("fim" if item.get("ending") else "abertura")})
        amb = ambience(c, frame_no, len(fr), fps, None, c.get("ambience_db", -60))
        if amb is not None: amb_list.append((frame_no, amb))

        loc = item.get("loc")
        tstart = tdur = None
        if loc and item.get("title"):
            tstart = int(loc.get("title_start", 0.15) * fps); tdur = int(loc.get("title_dur", 1.5) * fps)
        for j, f in enumerate(fr):
            f = f.copy()
            if tstart is not None and tstart <= j < tstart + tdur:
                k = j - tstart
                g = min(1, k / 6, (tdur - k) / 6) * 0.55
                f = (f * (1 - gradient(H, W, g))).astype(np.uint8)
                layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                T.draw(layer, loc["title"], k, tdur)
                f = composite(f, layer)
            if item.get("ending"):
                n = len(fr); p = ease_out(min(1, j / 10))
                f = (f * (1 - end.get("darken", 0.5) * p)).astype(np.uint8)
                layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                draw_end(T, layer, end["lines"], j, n + 30)
                f = composite(f, layer)
            pe.stdin.write(f.tobytes()); frame_no += 1
        prev_out = c.get("transition_out")
        print(f"  {os.path.basename(c['file'])}: {len(fr)} quadros", flush=True)
    pe.stdin.close(); pe.wait()
    total = frame_no

    # som: ambiente dos clipes + whoosh em cada transição de câmera + toque grave no fim
    N = int(total / fps * SR) + SR
    A = np.zeros((N, 2), np.float32)
    for f0, x in amb_list:
        i = int(f0 / fps * SR); A[i:i + len(x)] += x[:max(0, N - i)]
    snd = tl.get("sound", {})
    wz, pk = whoosh()
    for t in trans_times:
        i = int(t * SR) - pk
        if i >= 0: A[i:i + len(wz)] += wz * 10 ** (snd.get("whoosh_db", -22) / 20)
    if end:
        i = int(cuts[-1]["t"] * SR); h = hit()
        A[i:i + len(h)] += h * 10 ** (snd.get("end_hit_db", -20) / 20)
    A = A[:int(total / fps * SR)]
    fo = int(0.5 * SR); A[-fo:] *= np.linspace(1, 0, fo)[:, None]
    pk_ = np.abs(A).max()
    if pk_ > 0.89: A *= 0.89 / pk_
    wav = out_path + ".wav"
    wavfile.write(wav, SR, (A * 32767).astype(np.int16))
    subprocess.run([FF, "-y", "-v", "error", "-i", tmpv, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-ar", str(SR), "-movflags", "+faststart", "-shortest", out_path],
                   check=True)
    os.remove(tmpv); os.remove(wav)
    json.dump({"duracao": round(total / fps, 3), "fps": fps, "cortes": cuts,
               "transicoes_de_camera": [round(t, 3) for t in trans_times]},
              open(out_path + ".cortes.json", "w"), ensure_ascii=False, indent=2)
    print(f"{out_path}  {total} quadros = {total / fps:.2f} s")


def draw_end(T, layer, lines, j, n):
    """Encerramento centralizado: marca grande, régua dourada, '3 UNIDADES · CUIABÁ'."""
    c, s = T.c, T.s
    W, H = layer.size
    fend = ImageFont.truetype(P(c["font_name"]), int(c["name_size"] * 0.8 * s))
    N = T.line(lines[0], fend, 0.03, c["color"])
    L = T.line(lines[1], T.flabel, c["label_tracking"], c["color"])
    cy = int(H * 0.46)
    p1 = ease_out(min(1, max(0, (j - 2) / 10)))
    p2 = ease_out(min(1, max(0, (j - 8) / 10)))
    rw = int(150 * s * ease_out(min(1, max(0, (j - 5) / 10))))
    if p1 > 0:
        off = int((1 - p1) * N.height * 0.9)
        layer.alpha_composite(N.crop((0, 0, N.width, N.height - off)), ((W - N.width) // 2, cy - N.height + off))
    if rw > 0:
        ImageDraw.Draw(layer).rectangle([(W - rw) // 2, cy + int(8 * s), (W + rw) // 2, cy + int(8 * s) + max(2, int(4 * s))],
                                        fill=tuple(c["accent"]) + (255,))
    if p2 > 0:
        off = int((1 - p2) * L.height * 0.9)
        layer.alpha_composite(L.crop((0, off, L.width, L.height)), ((W - L.width) // 2, cy + int(24 * s)))


if __name__ == "__main__":
    main()
