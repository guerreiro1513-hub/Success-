#!/usr/bin/env python3
"""3 unidades — versão SÓ CARNES: nenhum texto, nenhum logo. Só planos de churrasqueira com cor natural
(sem os clipes do Florais/ESCALA, que tinham outra coloração). Som = trilha gaúcha baixa + o melhor chiado do estoque
(chiado realçado do Florais, entregue antes) + chiado da Tropical Ville por baixo. 1080x1920, 30 fps.
    python3 render_carnes.py
"""
import os, subprocess
import numpy as np
from scipy.io import wavfile
ROOT = os.path.dirname(os.path.abspath(__file__)); P = lambda p: os.path.join(ROOT, p)
W, H, FPS, SR = 1080, 1920, 30, 48000
OUT = P("../../entrega/guerreiros-3-UNIDADES-SO-CARNES.mp4")
GAUCHO, GAUCHO_GAIN = P("assets/trilha-gaucha-loop.wav"), 0.55     # trilha abaixo do chiado
CHIADO = P("../../entrega/guerreiros-FLORAIS-QUI-A-DOM.mp4"); CH_ST, CH_D = 11.6, 8.9   # trecho só de chiado
# A = Jardim Aclimação, B = Tropical Ville, D = vídeo novo (frango no rolete), E = IMG_1663 (4K girando), F = frangos tenda, G = vídeo do feriado (carnes), K = costela na grade (copy_A4FD)
A, B, D, E, F, G, K = "source/A.mov", "source/B.mov", "source/D.mov", "source/E.mov", "source/F.mov", "source/G.mov", "source/H.mov"
FIT = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
ZOOM_D = f"crop=540:960:90:0,scale={W}:{H}:flags=lanczos,cas=0.35"      # corta a legenda queimada (y≈0,77)
BASE = "eq=contrast=1.06:saturation=1.06"
# (fonte, início, segundos, enquadramento, cor)
SHOTS = [(E, 0.4, 2.2, FIT, BASE),                                  # costela/cupim girando (4K)
         (G, 3.0, 2.0, FIT, BASE),                                  # rolete com carnes
         (A, 7.6, 1.6, FIT, BASE),                                  # grelha girando
         (B, 12.4, 1.8, FIT, BASE),                                 # costela na grelha
         (G, 7.0, 1.4, FIT, BASE),                                  # panceta
         (D, 5.6, 1.35, FIT, "eq=contrast=1.04:saturation=0.92"),   # o ÚNICO plano de frango
         (K, 6.6, 1.4, FIT, BASE),                                  # costela na grade girando (troca do plano com frango)
         (B, 18.4, 1.9, FIT, BASE),                                 # costelinha
         (G, 15.4, 2.3, FIT, BASE)]                                 # carne girando no sol, fecha escurecendo

def frames(src, st, n, vf, grade):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{st:.3f}", "-i", P(src), "-frames:v", str(n), "-vf",
                          f"{vf},fps={FPS},{grade},format=rgb24", "-an", "-f", "rawvideo", "-"],
                         capture_output=True, check=True).stdout
    fr = list(np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3))
    while len(fr) < n: fr.append(fr[-1])
    return fr[:n]

os.makedirs(P("work"), exist_ok=True)
enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                        "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", P("work/video_carnes.mp4")], stdin=subprocess.PIPE)
total = sum(int(round(s[2] * FPS)) for s in SHOTS); g = 0
for src, st, d, vf, grade in SHOTS:
    n = int(round(d * FPS))
    for fr in frames(src, st, n, vf, grade):
        k = min(1.0, g / 8, (total - 1 - g) / 18)                # entra de 8 quadros, sai pro preto em 18
        out = fr if k >= 1 else (fr.astype(np.float32) * max(0.0, k)).astype(np.uint8)
        enc.stdin.write(out.tobytes()); g += 1
enc.stdin.close(); enc.wait()
T = total / FPS

def pcm(f, ss=None, t=None):
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", str(ss), "-t", str(t)] if ss is not None else []) + ["-i", P(f), "-vn", "-ac", "2", "-ar", str(SR), "-f", "s16le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.int16).reshape(-1, 2).astype(np.float32) / 32768

def loop(x, N, xf):
    """emenda o trecho nele mesmo com crossfade (chiado é ruído, a emenda some)"""
    out = np.zeros((N, 2), np.float32); pos = 0; ramp = np.linspace(0, 1, xf)[:, None]; first = True
    while pos < N:
        seg = x.copy()
        if not first: seg[:xf] *= ramp
        seg[-xf:] *= ramp[::-1]
        m = min(len(seg), N - pos); out[pos:pos + m] += seg[:m]
        if pos + len(seg) >= N: break
        pos += len(seg) - xf; first = False
    return out

N = int(T * SR)
top = loop(pcm(CHIADO, CH_ST, CH_D), N, int(1.0 * SR))
bed = pcm(B); bed = bed[:N] if len(bed) >= N else loop(bed, N, int(1.0 * SR))
rms = lambda v: np.sqrt(np.mean(v ** 2)) + 1e-9
mix = top / rms(top) + 0.35 * bed / rms(bed)                     # chiado realçado na frente, brasa da Tropical por baixo
mix *= 0.1 / rms(mix)
gau = loop(pcm(GAUCHO), N, int(0.5 * SR))                       # trilha gaúcha original (projeto PACU), sem direitos de terceiros
mix += GAUCHO_GAIN * 0.1 * gau / rms(gau)
fi, fo = int(0.25 * SR), int(0.7 * SR); mix[:fi] *= np.linspace(0, 1, fi)[:, None]; mix[-fo:] *= np.linspace(1, 0, fo)[:, None]
wavfile.write(P("work/audio_carnes.wav"), SR, (np.clip(mix, -1, 1) * 32767).astype(np.int16))
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", P("work/video_carnes.mp4"), "-i", P("work/audio_carnes.wav"), "-map", "0:v", "-map", "1:a",
                "-c:v", "copy", "-af", "highpass=f=70,loudnorm=I=-15:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k",
                "-movflags", "+faststart", "-shortest", OUT], check=True)
print(OUT, f"{T:.2f} s")
