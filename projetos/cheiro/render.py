#!/usr/bin/env python3
"""Reel "Se você sentiu esse cheiro..." — Guerreiro's Grill, Jardim Aclimação.
Lê tudo de timeline.json (fontes, trechos, cor, textos, fecho, áudio).

    python3 render.py            -> 1080x1920, 30 fps, H.264 + AAC
    python3 render.py --preview  -> 540x960 rápido

Fluxo: as fontes (vídeo vertical com rotação -90 nos metadados; o ffmpeg aplica a
rotação ao ler) são juntadas numa linha do tempo única a 30 fps em 1080x1920; cada
trecho é recortado por timestamp, sem esticar nem congelar. O Python compõe os textos e
o fecho e manda os quadros para o libx264. Áudio: trilha + ambiente baixo do take.
"""
import json, math, os, subprocess, sys
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy.io import wavfile

FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
ROOT = os.path.dirname(os.path.abspath(__file__))
P = lambda p: os.path.join(ROOT, p)
SR = 48000
SAFE = {"x0": 70, "x1": 160, "y0": 230, "y1": 420}      # área livre da interface do Reels em 1080x1920


def ease_out(t): t = min(1, max(0, t)); return 1 - (1 - t) ** 3


def joined(tl, W, H, fps):
    """Junta as fontes (já rotacionadas) num arquivo único 30 fps; placeholder cinza se faltar fonte."""
    out = P(f"work/joined_{W}x{H}.mp4")
    srcs = [P(s) for s in tl["sources"]]
    if all(os.path.exists(s) for s in srcs) and os.path.exists(out) and \
            os.path.getmtime(out) > max(os.path.getmtime(s) for s in srcs):
        return out
    os.makedirs(P("work"), exist_ok=True)
    if not all(os.path.exists(s) for s in srcs):
        print("AVISO: fonte não encontrada, gerando placeholder cinza de 20 s", file=sys.stderr)
        subprocess.run([FF, "-y", "-v", "error", "-f", "lavfi", "-i", f"color=c=gray:s={W}x{H}:r={fps}:d=20",
                        "-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=stereo", "-t", "20", "-c:v", "libx264", "-crf", "16",
                        "-c:a", "aac", out], check=True)
        return out
    inp, fc = [], []
    for i, s in enumerate(srcs):
        inp += ["-i", s]
        fc.append(f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},"
                  f"fps={fps},setsar=1,setpts=PTS-STARTPTS[v{i}];[{i}:a]aresample={SR},asetpts=PTS-STARTPTS[a{i}]")
    fc.append("".join(f"[v{i}][a{i}]" for i in range(len(srcs))) + f"concat=n={len(srcs)}:v=1:a=1[v][a]")
    subprocess.run([FF, "-y", "-v", "error"] + inp + ["-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "14", "-pix_fmt", "yuv420p",
                    "-c:a", "pcm_s16le", out], check=True)
    return out


def segment_frames(src, a, b, W, H, fps, grade):
    n = int(round((b - a) * fps))
    vf = ",".join(x for x in [grade, "format=rgb24"] if x)
    raw = subprocess.run([FF, "-v", "error", "-ss", f"{a:.3f}", "-i", src, "-frames:v", str(n), "-vf", vf,
                          "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    return [f.copy() for f in fr]


def font(path, size, weight=None):
    f = ImageFont.truetype(P(path), max(8, int(size)))
    if weight:
        try: f.set_variation_by_axes([weight])
        except Exception: pass
    return f


def lockup(lines, s, max_w):
    """Bloco centralizado: cada linha encolhe sozinha se passar da largura segura."""
    rows = []
    for L in lines:
        size = L["size"] * s
        while True:
            f = font(L["font"], size, L.get("weight"))
            w = f.getlength(L["text"])
            if w <= max_w or size < 10: break
            size *= max_w / w * 0.98
        a, d = f.getmetrics()
        rows.append((L, f, w, a + d))
    pad = int(40 * s)
    Wl = int(max(r[2] for r in rows)) + 2 * pad
    Hl = int(sum(r[3] for r in rows) * 0.92) + 2 * pad
    layers = []
    y = pad
    for i, (L, f, w, h) in enumerate(rows):
        m = Image.new("L", (Wl, Hl), 0)
        ImageDraw.Draw(m).text(((Wl - w) / 2, y), L["text"], font=f, fill=255)
        a = np.array(m, np.float32) / 255
        if L.get("color") == "fire":
            yy = np.clip((np.arange(Hl)[:, None] - y) / max(1, h), 0, 1)[..., None]
            rgb = np.array([255, 200, 74.]) * (1 - yy) + np.array([240, 96, 18.]) * yy
            rgb = np.broadcast_to(rgb, (Hl, Wl, 3))
        else:
            rgb = np.broadcast_to(np.array([255, 251, 244.]), (Hl, Wl, 3))
        layers.append((np.concatenate([rgb, a[..., None]], -1).astype(np.float32), i * 4))
        y += int(h * 0.92)
    A = np.maximum.reduce([l[0][..., 3] for l in layers])
    sh = np.roll(cv2.GaussianBlur(A, (0, 0), 10 * s), int(6 * s), 0) * 0.65
    sh = np.maximum(sh, cv2.GaussianBlur(cv2.dilate(A, np.ones((3, 3), np.uint8)), (0, 0), 1.2 * s) * 0.5)
    return layers, sh, Wl, Hl


def draw_text(frames, T, s, fps):
    H, W = frames[0].shape[:2]
    layers, sh, Wl, Hl = lockup(T["lines"], s, (1080 - SAFE["x0"] - SAFE["x1"]) * s)
    st, en = int(T["start"] * fps), int(T["end"] * fps)
    cx = W / 2 + (SAFE["x0"] - SAFE["x1"]) * s / 2 * 0       # centro da tela
    cy = T.get("cy", 0.3) * H
    x0, y0 = int(cx - Wl / 2), int(cy - Hl / 2)
    for j in range(max(0, st), min(len(frames), en)):
        k, left = j - st, en - j
        out_a = min(1, left / 6)
        lay = np.zeros((Hl, Wl, 4), np.float32)
        for img, dl in layers:
            p = ease_out((k - dl) / 8)
            if p <= 0: continue
            dy = int((1 - p) * 26 * s)
            im = np.roll(img, dy, 0).copy(); im[..., 3] *= p
            a = im[..., 3:4]
            lay[..., :3] = lay[..., :3] * (1 - a) + im[..., :3] * a
            lay[..., 3:4] = a + lay[..., 3:4] * (1 - a)
        vis = lay[..., 3].max()
        f = frames[j].astype(np.float32)
        ys, xs = slice(max(0, y0), min(H, y0 + Hl)), slice(max(0, x0), min(W, x0 + Wl))
        ly, lx = slice(ys.start - y0, ys.stop - y0), slice(xs.start - x0, xs.stop - x0)
        reg = f[ys, xs]
        reg *= (1 - sh[ly, lx, None] * vis * out_a)
        a = lay[ly, lx, 3:4] * out_a
        f[ys, xs] = reg * (1 - a) + lay[ly, lx, :3] * a
        frames[j] = np.clip(f, 0, 255).astype(np.uint8)


def end_card(frames, E, s, fps):
    H, W = frames[0].shape[:2]
    st = int(E["start"] * fps)
    logo = Image.open(P(E["logo"])).convert("RGBA")
    lh = int(E["logo_h"] * H); lw = int(logo.width * lh / logo.height)
    logo = np.array(logo.resize((lw, lh), Image.LANCZOS), np.float32)
    lab = lockup([{"text": E["label"], "font": "assets/fonts/Montserrat.ttf", "weight": 600, "size": 40, "color": "white"},
                  {"text": E["name"], "font": "assets/fonts/Anton-Regular.ttf", "size": 120, "color": "fire"}],
                 s, (1080 - SAFE["x0"] - SAFE["x1"]) * s)
    yy = np.linspace(0, 1, H)[:, None, None]
    for j in range(max(0, st), len(frames)):
        k = j - st
        f = frames[j].astype(np.float32)
        g = E.get("shade", 0.45) * ease_out(k / 10)
        f *= 1 - g * (0.55 + 0.45 * np.exp(-((yy - 0.36) / 0.22) ** 2))
        # logo: entra de cima com leve quique e brilho
        p = ease_out(k / 10)
        if p > 0:
            sc = 1 + 0.25 * (1 - p) + (0.05 * math.exp(-(k - 10) / 3) * math.cos((k - 10) * 1.4) if k >= 10 else 0)
            w2, h2 = max(2, int(lw * sc)), max(2, int(lh * sc))
            L = cv2.resize(logo, (w2, h2), interpolation=cv2.INTER_LINEAR)
            cx, cy = W // 2, int(E["logo_cy"] * H - (1 - p) * 120 * s)
            x0, y0 = cx - w2 // 2, cy - h2 // 2
            a = L[..., 3:4] / 255 * p
            sub = f[y0:y0 + h2, x0:x0 + w2]
            sub[:] = sub * (1 - a) + L[..., :3] * a
            if 10 <= k < 20:
                gl = cv2.GaussianBlur(a[..., 0], (0, 0), 25 * s)[..., None] * (1 - (k - 10) / 10) * 0.6
                sub[:] = sub + (255 - sub) * gl
        frames[j] = np.clip(f, 0, 255).astype(np.uint8)
    T = {"start": E["start"] + 0.45, "end": len(frames) / fps + 1, "cy": E["text_cy"]}
    layers, sh, Wl, Hl = lab
    # reaproveita o desenho de texto com o bloco já montado
    st2 = int(T["start"] * fps)
    x0, y0 = int(W / 2 - Wl / 2), int(T["cy"] * H - Hl / 2)
    for j in range(st2, len(frames)):
        k = j - st2
        lay = np.zeros((Hl, Wl, 4), np.float32)
        for img, dl in layers:
            p = ease_out((k - dl) / 8)
            if p <= 0: continue
            im = np.roll(img, int((1 - p) * 26 * s), 0).copy(); im[..., 3] *= p
            a = im[..., 3:4]
            lay[..., :3] = lay[..., :3] * (1 - a) + im[..., :3] * a
            lay[..., 3:4] = a + lay[..., 3:4] * (1 - a)
        f = frames[j].astype(np.float32)
        reg = f[y0:y0 + Hl, x0:x0 + Wl]
        reg *= (1 - sh[..., None] * lay[..., 3].max())
        a = lay[..., 3:4]
        f[y0:y0 + Hl, x0:x0 + Wl] = reg * (1 - a) + lay[..., :3] * a
        frames[j] = np.clip(f, 0, 255).astype(np.uint8)


def audio(tl, src, total_s, cut_list, out_wav):
    au = tl["audio"]
    n = int(total_s * SR)
    amb = np.zeros((n, 2), np.float32)
    pos = 0
    for a, b in cut_list:                      # ambiente do próprio take, nos mesmos trechos
        raw = subprocess.run([FF, "-v", "error", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", src, "-vn", "-ac", "2",
                              "-ar", str(SR), "-f", "s16le", "-"], capture_output=True).stdout
        x = np.frombuffer(raw, np.int16).reshape(-1, 2).astype(np.float32) / 32768
        m = min(len(x), n - pos)
        fd = min(int(0.03 * SR), m // 2)
        x = x[:m].copy()
        if fd: x[:fd] *= np.linspace(0, 1, fd)[:, None]; x[-fd:] *= np.linspace(1, 0, fd)[:, None]
        amb[pos:pos + m] += x; pos += int(round((b - a) * SR))
    raw = subprocess.run([FF, "-v", "error", "-ss", str(au.get("music_start", 0)), "-i", P(au["music"]), "-vn", "-ac", "2",
                          "-ar", str(SR), "-f", "s16le", "-"], capture_output=True, check=True).stdout
    mus = np.frombuffer(raw, np.int16).reshape(-1, 2).astype(np.float32) / 32768
    mus = mus[:n] if len(mus) >= n else np.pad(mus, ((0, n - len(mus)), (0, 0)))
    mix = mus * 10 ** (au.get("music_db", 0) / 20) + amb * 10 ** (au.get("ambience_db", -20) / 20)
    fo = int(au.get("fade_out", 1.2) * SR); mix[-fo:] *= np.linspace(1, 0, fo)[:, None]
    pk = np.abs(mix).max()
    if pk > 0.89: mix *= 0.89 / pk
    wavfile.write(out_wav, SR, (mix * 32767).astype(np.int16))


def main():
    preview = "--preview" in sys.argv
    tl = json.load(open(P("timeline.json")))
    o = tl["output"]; fps = o["fps"]
    s = o.get("preview_scale", 0.5) if preview else 1.0
    W, H = int(o["w"] * s) // 2 * 2, int(o["h"] * s) // 2 * 2
    out = P(o["preview_file"] if preview else o["file"])
    src = joined(tl, o["w"], o["h"], fps)
    frames, cut_list, cuts = [], [], []
    tr = tl.get("transition", {})
    for i, sg in enumerate(tl["segments"]):
        fr = segment_frames(src, sg["start"], sg["end"], W, H, fps,
                            tl.get("grade", "") + (f",scale={W}:{H}:flags=area" if preview else ""))
        jump = i > 0 and abs(sg["start"] - tl["segments"][i - 1]["end"]) > 0.05
        if jump:                                # salto de tempo: clarão curto no corte
            k = tr.get("flash_frames", 4)
            for j in range(min(k, len(fr))):
                g = tr.get("flash", 0.35) * (1 - j / k) ** 2
                fr[j] = np.clip(fr[j] * (1 - g) + 255 * g, 0, 255).astype(np.uint8)
        cuts.append({"t": round(len(frames) / fps, 3), "trecho": sg["name"], "de": sg["start"], "ate": sg["end"]})
        frames += fr; cut_list.append((sg["start"], sg["end"]))
    for T in tl.get("texts", []): draw_text(frames, T, s, fps)
    if tl.get("end_card"): end_card(frames, tl["end_card"], s, fps)
    total_s = len(frames) / fps
    os.makedirs(os.path.dirname(out), exist_ok=True)
    wav = out + ".wav"
    audio(tl, src, total_s, cut_list, wav)
    enc = [FF, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
           "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p",
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]
    enc += (["-preset", "veryfast", "-crf", "24"] if preview else
            ["-preset", "slow", "-crf", "17", "-maxrate", "14M", "-bufsize", "24M", "-profile:v", "high", "-level", "4.1"])
    enc += ["-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", out]
    pe = subprocess.Popen(enc, stdin=subprocess.PIPE)
    for f in frames: pe.stdin.write(f.tobytes())
    pe.stdin.close(); pe.wait(); os.remove(wav)
    json.dump({"duracao": round(total_s, 3), "fps": fps, "cortes": cuts}, open(out + ".cortes.json", "w"),
              ensure_ascii=False, indent=2)
    print(f"{out}  {len(frames)} quadros = {total_s:.2f} s")


if __name__ == "__main__":
    main()
