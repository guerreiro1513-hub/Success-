# Bronca Fake — som. Voz e ambiente reais na bronca e na quebra; a trilha
# (gaucha 100 BPM, sintetizada neste repositorio) so entra no corte da carne.
import numpy as np, scipy.io.wavfile as w, subprocess, os
FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
P = "/home/user/Success-/projetos/bronca"; WK = P + "/work"; OUT = WK + "/mix"
os.makedirs(OUT, exist_ok=True)
SR = 48000; FPS = 30
B1, Q1, M1, O1 = 222, 81, 63, 47
TOT = B1 + Q1 + M1 + O1
def rd(p):
    x = w.read(p)[1].astype(np.float64) / 32768
    return x if x.ndim == 2 else np.stack([x, x], 1)
def ff(*a): subprocess.run([FF, "-y", "-v", "error", *a], check=True)

# voz: limpeza leve para nao soar processada. grave cortado, ruido reduzido de
# leve, presenca discreta, compressao 2,5:1
ff("-i", WK + "/cut/base.mov", "-vn", "-t", str((B1 + Q1) / FPS), "-af",
   "highpass=f=90,afftdn=nr=6:nf=-40:tn=1,equalizer=f=250:t=q:w=1:g=-2,"
   "equalizer=f=3200:t=q:w=1.2:g=2.5,acompressor=threshold=-24dB:ratio=2.5:attack=10:release=150:makeup=2",
   "-ar", "48000", "-ac", "2", OUT + "/voz.wav")
ff("-i", WK + "/cut/base.mov", "-vn", "-ar", "48000", "-ac", "2", OUT + "/base.wav")
V = rd(OUT + "/voz.wav"); A = rd(OUT + "/base.wav")
N = int(TOT / FPS * SR); A = np.pad(A, ((0, max(0, N - len(A))), (0, 0)))[:N]
iq = int((B1 + Q1) / FPS * SR)                      # corte para a carne
voz = np.zeros((N, 2)); voz[:min(len(V), iq)] = V[:iq]
k = int(0.015 * SR); voz[iq - k:iq] *= np.linspace(1, 0, k)[:, None]

# ambiente da carne: o chiado real do IMG_1452 por baixo da trilha
amb = np.zeros((N, 2)); io = int((B1 + Q1 + M1) / FPS * SR)
amb[iq:io] = A[iq:io] * 0.45
k = int(0.02 * SR); amb[iq:iq + k] *= np.linspace(0, 1, k)[:, None]
amb[io - int(0.3 * SR):io] *= np.linspace(1, 0, int(0.3 * SR))[:, None]

# trilha: entra seca no corte, numa cabeca de compasso da faixa (2,50 s), e
# desce junto com o escurecimento da vinheta
T = rd("/home/user/Success-/entrega/trilha-gaucha-100bpm.wav")
seg = T[int(2.50 * SR):int(2.50 * SR) + (N - iq)]
mus = np.zeros((N, 2)); mus[iq:iq + len(seg)] = seg
fo = int(1.1 * SR); mus[N - fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
vr = np.sqrt(np.mean(voz[:iq] ** 2)); mr = np.sqrt(np.mean(mus[iq:io] ** 2)) + 1e-12
mus *= vr / mr * 10 ** (-1.5 / 20)                  # a trilha fica logo abaixo da voz

for nm, x in (("com", voz + amb + mus), ("sem", voz + amb / 0.45 * 0.9)):
    x = x * (0.5 / np.abs(x).max())
    w.write(OUT + f"/pre_{nm}.wav", SR, (x * 32767).astype(np.int16))
    ff("-i", OUT + f"/pre_{nm}.wav", "-af",
       "loudnorm=I=-14:TP=-1.5:LRA=9,alimiter=limit=0.66:level=false:attack=2:release=60,aresample=48000",
       "-ar", "48000", OUT + f"/final_{nm}.wav")
print("ok", TOT, "quadros")
