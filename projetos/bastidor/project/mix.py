# Bastidor v3 — som. A trilha A gerada no Kairogen (sertanejo-funk, ~133 BPM) e
# o motor do video; o som natural de cada take fica por baixo, nivelado, com
# emendas de 20 ms. A versao "sem" e so o som natural.
import numpy as np, scipy.io.wavfile as w, subprocess, os
FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
P = "/home/user/Success-/projetos/bastidor"; WK = P + "/work"; OUT = WK + "/mix"
os.makedirs(OUT, exist_ok=True)
SR = 48000; FPS = 30
CUTS = [0, 109, 136, 163, 190, 217, 325, 352, 379, 460, 507]   # ultimo trecho = vinheta
def rd(p):
    x = w.read(p)[1].astype(np.float64) / 32768
    return x if x.ndim == 2 else np.stack([x, x], 1)
def ff(*a): subprocess.run([FF, "-y", "-v", "error", *a], check=True)
ff("-i", WK + "/cut/base.mov", "-vn", "-af",
   "highpass=f=70,afftdn=nr=4:nf=-45,acompressor=threshold=-26dB:ratio=2:attack=15:release=200",
   "-ar", "48000", "-ac", "2", OUT + "/nat.wav")
N = int(CUTS[-1] / FPS * SR)
A = rd(OUT + "/nat.wav"); A = np.pad(A, ((0, max(0, N - len(A))), (0, 0)))[:N]
rms = [np.sqrt(np.mean(A[int(a / FPS * SR):int(b / FPS * SR)] ** 2)) + 1e-9 for a, b in zip(CUTS[:-2], CUTS[1:-1])]
ref = float(np.median(rms))
for (a, b), r in zip(zip(CUTS[:-2], CUTS[1:-1]), rms):
    A[int(a / FPS * SR):int(b / FPS * SR)] *= min(ref / r, 10.0)
iv = int(CUTS[-2] / FPS * SR)
k = int(0.3 * SR); A[iv - k:iv] *= np.linspace(1, 0, k)[:, None]; A[iv:] = 0
for c in CUTS[1:-2]:
    i = int(c / FPS * SR); m = int(0.02 * SR)
    A[i - m:i] *= np.linspace(1, 0.4, m)[:, None]; A[i:i + m] *= np.linspace(0.4, 1, m)[:, None]
M = rd(WK + "/m_A_sertanejo-funk.wav")[:N]; M = np.pad(M, ((0, N - len(M)), (0, 0)))
fo = int(0.6 * SR); M[N - fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
# a trilha manda; o ambiente fica 9 dB abaixo dela
amb = A * (np.sqrt(np.mean(M[:iv] ** 2)) / (np.sqrt(np.mean(A[:iv] ** 2)) + 1e-12)) * 10 ** (-9 / 20)
for nm, x in (("com", M + amb), ("sem", A)):
    x = x * (0.5 / np.abs(x).max())
    w.write(OUT + f"/pre_{nm}.wav", SR, (x * 32767).astype(np.int16))
    ff("-i", OUT + f"/pre_{nm}.wav", "-af",
       "loudnorm=I=-14:TP=-1.5:LRA=9,alimiter=limit=0.62:level=false:attack=2:release=60,aresample=48000",
       "-ar", "48000", OUT + f"/final_{nm}.wav")
print("ok", CUTS[-1], "quadros")
