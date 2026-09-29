# Bastidor Tranquilo — som. O som natural de cada take (grelha, brasa, movimento)
# e o protagonista: cada trecho e nivelado com os outros, emendas de 20 ms nos
# cortes, limpeza leve. A versao "com" leva a trilha gaucha (sintetizada neste
# repositorio) bem baixa por baixo; a "sem" e so o som natural.
import numpy as np, scipy.io.wavfile as w, scipy.signal as sg, subprocess, os
FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
P = "/home/user/Success-/projetos/bastidor"; WK = P + "/work"; OUT = WK + "/mix"
os.makedirs(OUT, exist_ok=True)
SR = 48000; FPS = 30
CUTS = [0, 105, 285, 360, 460, 507]          # a1 a2 a3 a4 | vinheta
def rd(p):
    x = w.read(p)[1].astype(np.float64) / 32768
    return x if x.ndim == 2 else np.stack([x, x], 1)
def ff(*a): subprocess.run([FF, "-y", "-v", "error", *a], check=True)
ff("-i", WK + "/cut/base.mov", "-vn", "-af",
   "highpass=f=70,afftdn=nr=4:nf=-45,acompressor=threshold=-26dB:ratio=2:attack=15:release=200",
   "-ar", "48000", "-ac", "2", OUT + "/nat.wav")
N = int(CUTS[-1] / FPS * SR)
A = rd(OUT + "/nat.wav"); A = np.pad(A, ((0, max(0, N - len(A))), (0, 0)))[:N]
# nivela cada take no mesmo RMS (o IMG_1459 veio ~10 dB mais baixo)
ref = None
for a, b in zip(CUTS[:-2], CUTS[1:-1]):
    i, j = int(a / FPS * SR), int(b / FPS * SR)
    r = np.sqrt(np.mean(A[i:j] ** 2)) + 1e-9
    if ref is None: ref = r
    A[i:j] *= min(ref / r, 4.0)
iv = int(CUTS[-2] / FPS * SR)
k = int(0.35 * SR); A[iv - k:iv] *= np.linspace(1, 0, k)[:, None]; A[iv:] = 0   # sai na vinheta
for c in CUTS[1:-2]:                          # emendas sem estalo
    i = int(c / FPS * SR); m = int(0.02 * SR)
    A[i - m:i] *= np.linspace(1, 0.4, m)[:, None]; A[i:i + m] *= np.linspace(0.4, 1, m)[:, None]
T = rd("/home/user/Success-/entrega/trilha-gaucha-100bpm.wav")
mus = np.zeros_like(A); seg = T[int(2.5 * SR):int(2.5 * SR) + N]; mus[:len(seg)] = seg
env = np.ones(N) * 10 ** (-16 / 20)           # muito baixa: o ambiente manda
fi = int(1.0 * SR); env[:fi] *= np.linspace(0, 1, fi)
env[iv:] = np.linspace(10 ** (-16 / 20), 10 ** (-6 / 20), N - iv)   # sobe um pouco no logo
fo = int(0.8 * SR); env[N - fo:] *= np.linspace(1, 0, fo) ** 1.5
mus *= (np.sqrt(np.mean(A[:iv] ** 2)) / (np.sqrt(np.mean(mus[:iv] ** 2)) + 1e-12)) * env[:, None]
for nm, x in (("com", A + mus), ("sem", A)):
    x = x * (0.5 / np.abs(x).max())
    w.write(OUT + f"/pre_{nm}.wav", SR, (x * 32767).astype(np.int16))
    ff("-i", OUT + f"/pre_{nm}.wav", "-af",
       "loudnorm=I=-15:TP=-1.5:LRA=9,alimiter=limit=0.60:level=false:attack=2:release=60,aresample=48000",
       "-ar", "48000", OUT + f"/final_{nm}.wav")
print("ok", CUTS[-1], "quadros")
