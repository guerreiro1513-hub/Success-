# O Segredo v2 — som. Fala do 1440 (take 2) e ambiente dos takes com o ruido de
# carro tirado por subtracao espectral (denoise.py). Musica epica entra no making.
import numpy as np, scipy.io.wavfile as w, subprocess, os, re
FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
P = "/home/user/Success-/projetos/segredo"; S = P + "/source"; OUT = P + "/work/mix"
os.makedirs(OUT, exist_ok=True)
SR = 48000; FPS = 30; TOT = 307; N = int(TOT / FPS * SR)
def ff(*a): subprocess.run([FF, "-y", "-v", "error", *a], check=True)
def rd(p):
    x = w.read(p)[1].astype(np.float64) / 32768
    return x if x.ndim == 2 else np.stack([x, x], 1)
DN = P + "/project/denoise.py"
for nm, spans in (("1440", "0-1.6,3.5-4.5,7.0-8.1"), ("1441", "0-1.3,3.0-5.8,6.8-8.3")):
    ff("-i", f"{S}/IMG_{nm}.mov", "-vn", "-ac", "2", "-ar", "48000", "-af", "highpass=f=100", f"{OUT}/r{nm}.wav")
    subprocess.run(["python3", DN, f"{OUT}/r{nm}.wav", f"{OUT}/d{nm}.wav", spans], check=True)
    ff("-i", f"{OUT}/d{nm}.wav", "-af", "equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1.2:g=3,"
       "acompressor=threshold=-26dB:ratio=2.5:attack=8:release=150:makeup=3", "-ar", "48000", f"{OUT}/v{nm}.wav")
A, B = rd(OUT + "/v1440.wav"), rd(OUT + "/v1441.wav")
def take(x, t0, nf): i = int(t0 * SR); return x[i:i + int(nf / FPS * SR)]
D = np.zeros((N, 2)); pos = 0
for x, t0, nf in ((A, 0.0, 104), (A, 6.95, 33)):
    seg = take(x, t0, nf); n = len(seg); k = int(0.012 * SR)
    seg = seg.copy(); seg[:k] *= np.linspace(0, 1, k)[:, None]; seg[-k:] *= np.linspace(1, 0, k)[:, None]
    D[pos:pos + n] = seg; pos = int((pos / SR * FPS + nf) / FPS * SR)
# ambiente restante 10 dB abaixo fora da fala (suspense limpo)
s0, s1 = int(1.82 * SR), int(3.40 * SR)   # fala (take 1)
lo = 10 ** (-10 / 20); g = np.full(N, lo); r = int(0.1 * SR)
g[s0 - r:s1 + r] = 1.0; g[s0 - 2 * r:s0 - r] = np.linspace(lo, 1, r); g[s1 + r:s1 + 2 * r] = np.linspace(1, lo, r)
D *= g[:, None]
i2 = int(137 / FPS * SR)
M = rd(P + "/work/musica.wav")[:N - i2]
Mu = np.zeros((N, 2)); Mu[i2:i2 + len(M)] = M
fo = int(0.8 * SR); Mu[N - fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
rv = np.sqrt(np.mean(D[s0:s1] ** 2)); rm = np.sqrt(np.mean(Mu[i2:] ** 2)) + 1e-12
Mu *= rv / rm * 10 ** (-2.0 / 20)
X = D + Mu; X = X * (0.5 / np.abs(X).max())
w.write(OUT + "/pre.wav", SR, (X * 32767).astype(np.int16))
r = subprocess.run([FF, "-i", OUT + "/pre.wav", "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1]); gdb = -14.0 - I
ff("-i", OUT + "/pre.wav", "-af", f"volume={gdb:.2f}dB,alimiter=limit=0.62:level=false:attack=2:release=60,aresample=48000",
   "-ar", "48000", OUT + "/final.wav")
print("ganho", round(gdb, 1))
