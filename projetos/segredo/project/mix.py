# O Segredo v4 — som. Fala do 1440 (pergunta take 1 + resposta take 2) sem ruido
# de carro (denoise.py). Musica de suspense "na ponta dos pes" por baixo da fala,
# corte seco para a musica epica no impacto do making.
import numpy as np, scipy.io.wavfile as w, subprocess, os, re
FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
P = "/home/user/Success-/projetos/segredo"; S = P + "/source"; OUT = P + "/work/mix"
os.makedirs(OUT, exist_ok=True)
SR = 48000; FPS = 30; TOT = 468; N = int(TOT / FPS * SR)
def ff(*a): subprocess.run([FF, "-y", "-v", "error", *a], check=True)
def rd(p):
    x = w.read(p)[1].astype(np.float64) / 32768
    return x if x.ndim == 2 else np.stack([x, x], 1)
def fr(n): return int(n / FPS * SR)
ff("-i", S + "/IMG_1440.mov", "-vn", "-ac", "2", "-ar", "48000", "-af", "highpass=f=100", OUT + "/r1440.wav")
subprocess.run(["python3", P + "/project/denoise.py", OUT + "/r1440.wav", OUT + "/d1440.wav", "0-1.6,3.5-4.5,7.0-8.1"], check=True)
ff("-i", OUT + "/d1440.wav", "-af", "equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1.2:g=3,"
   "acompressor=threshold=-26dB:ratio=2.5:attack=8:release=150:makeup=3", "-ar", "48000", OUT + "/v1440.wav")
A = rd(OUT + "/v1440.wav")
# (inicio no take, quadro de saida, quadros) — a3 (acelerado) usa o ambiente de 1,0 s
SEG = [(0.00, 0, 15), (0.50, 15, 15), (1.00, 30, 15), (1.80, 45, 49), (5.25, 94, 47), (6.80, 141, 37)]
D = np.zeros((N, 2)); k = int(0.010 * SR)
for t0, o, nf in SEG:
    seg = A[int(t0 * SR):int(t0 * SR) + fr(nf)].copy()
    seg[:k] *= np.linspace(0, 1, k)[:, None]; seg[-k:] *= np.linspace(1, 0, k)[:, None]
    D[fr(o):fr(o) + len(seg)] = seg
# ambiente 10 dB abaixo fora das falas
sp = [(fr(47) - 2400, fr(93) + 2400), (fr(100) - 2400, fr(141) + 2400)]
g = np.full(N, 10 ** (-10 / 20))
for a, b in sp: g[a:b] = 1.0
g = np.convolve(g, np.ones(4800) / 4800, "same"); D *= g[:, None]
rv = np.sqrt(np.mean(np.concatenate([D[a:b] for a, b in sp]) ** 2))
# suspense: do quadro 0 ate o impacto (178), 13 dB abaixo da fala
MAKE = fr(178)
Su = rd(P + "/work/suspense.wav")
while len(Su) < MAKE: Su = np.concatenate([Su, Su])
Su = Su[:MAKE].copy(); Su *= rv / (np.sqrt(np.mean(Su ** 2)) + 1e-12) * 10 ** (-13 / 20)
fi = int(0.15 * SR); Su[:fi] *= np.linspace(0, 1, fi)[:, None]
fo = int(0.04 * SR); Su[-fo:] *= np.linspace(1, 0, fo)[:, None]
# epica: impacto no corte para o making
M = rd(P + "/work/musica.wav")[:N - MAKE]
Mu = np.zeros((N, 2)); Mu[MAKE:MAKE + len(M)] = M
fo = int(0.9 * SR); Mu[N - fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
Mu *= rv / (np.sqrt(np.mean(Mu[MAKE:] ** 2)) + 1e-12) * 10 ** (-2.0 / 20)
X = D + Mu; X[:MAKE] += Su; X = X * (0.5 / np.abs(X).max())
w.write(OUT + "/pre.wav", SR, (X * 32767).astype(np.int16))
r = subprocess.run([FF, "-i", OUT + "/pre.wav", "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1]); gdb = -14.0 - I
ff("-i", OUT + "/pre.wav", "-af", f"volume={gdb:.2f}dB,alimiter=limit=0.62:level=false:attack=2:release=60,aresample=48000",
   "-ar", "48000", OUT + "/final.wav")
print("ganho", round(gdb, 1))
