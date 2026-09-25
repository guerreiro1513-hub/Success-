# Bronca Fake v2 — som. Voz e ambiente reais na bronca; a trilha gaucha
# (sintetizada neste repositorio) entra baixa no corte para a cor, por baixo da
# voz, e sobe quando o logo aparece.
import numpy as np, scipy.io.wavfile as w, subprocess, os
FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
P = "/home/user/Success-/projetos/bronca"; WK = P + "/work"; OUT = WK + "/mix"
os.makedirs(OUT, exist_ok=True)
SR = 48000; FPS = 30
Q, E1, F1 = 41 + 187, 115 + 272, 36
TOT = Q + E1 + F1; LOGO_IN = 609
def rd(p):
    x = w.read(p)[1].astype(np.float64) / 32768
    return x if x.ndim == 2 else np.stack([x, x], 1)
def ff(*a): subprocess.run([FF, "-y", "-v", "error", *a], check=True)
# voz com limpeza leve (as duas partes, cada uma com seu ambiente real)
ff("-i", WK + "/cut/base.mov", "-vn", "-af",
   "highpass=f=90,afftdn=nr=6:nf=-40:tn=1,equalizer=f=250:t=q:w=1:g=-2,"
   "equalizer=f=3200:t=q:w=1.2:g=2.5,acompressor=threshold=-24dB:ratio=2.5:attack=10:release=150:makeup=2",
   "-ar", "48000", "-ac", "2", OUT + "/voz.wav")
N = int(TOT / FPS * SR); V = rd(OUT + "/voz.wav"); V = np.pad(V, ((0, max(0, N - len(V))), (0, 0)))[:N]
ic = int(Q / FPS * SR); il = int(LOGO_IN / FPS * SR); ie = int((Q + E1) / FPS * SR)
# as duas fontes tem niveis diferentes: iguala a fala do video 1 a do video 2
g = np.sqrt(np.mean(V[:ic] ** 2)) / (np.sqrt(np.mean(V[ic:ie] ** 2)) + 1e-12)
V[ic:ie] *= min(g, 2.0)
k = int(0.3 * SR); V[ie - k:ie] *= np.linspace(1, 0, k)[:, None]; V[ie:] = 0
# trilha a partir de uma cabeca de compasso (2,50 s)
T = rd("/home/user/Success-/entrega/trilha-gaucha-100bpm.wav")
seg = T[int(2.50 * SR):int(2.50 * SR) + (N - ic)]
mus = np.zeros((N, 2)); mus[ic:ic + len(seg)] = seg
vr = np.sqrt(np.mean(V[:ic] ** 2)); mr = np.sqrt(np.mean(mus[ic:il] ** 2)) + 1e-12
env = np.zeros(N)
env[ic:il] = 10 ** (-11 / 20)                       # por baixo da voz
ramp = int(0.25 * SR); env[il:il + ramp] = np.linspace(10 ** (-11 / 20), 10 ** (-1 / 20), ramp)
env[il + ramp:] = 10 ** (-1 / 20)                   # o logo: a trilha sobe
fo = int(0.9 * SR); env[N - fo:] *= np.linspace(1, 0, fo) ** 1.5
k = int(0.02 * SR); env[ic:ic + k] *= np.linspace(0, 1, k)
mus = mus * (vr / mr) * env[:, None]
for nm, x in (("com", V + mus), ("sem", V)):
    x = x * (0.5 / np.abs(x).max())
    w.write(OUT + f"/pre_{nm}.wav", SR, (x * 32767).astype(np.int16))
    ff("-i", OUT + f"/pre_{nm}.wav", "-af",
       "loudnorm=I=-14:TP=-1.5:LRA=9,alimiter=limit=0.66:level=false:attack=2:release=60,aresample=48000",
       "-ar", "48000", OUT + f"/final_{nm}.wav")
print("ok", TOT, "quadros, ganho video1 %.2f" % g)
