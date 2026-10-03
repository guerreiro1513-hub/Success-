# O Segredo — som. Fala original do 1441 (take 2) com limpeza leve; abertura
# so com o ambiente do 1440 (antes da fala dele). Musica epica (Kairogen) entra
# com o impacto no corte para o "the making".
import numpy as np, scipy.io.wavfile as w, subprocess, os
FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
P = "/home/user/Success-/projetos/segredo"; S = P + "/source"; OUT = P + "/work/mix"
os.makedirs(OUT, exist_ok=True)
SR = 48000; FPS = 30; TOT = 337; N = int(TOT / FPS * SR)
def ff(*a): subprocess.run([FF, "-y", "-v", "error", *a], check=True)
def rd(p):
    x = w.read(p)[1].astype(np.float64) / 32768
    return x if x.ndim == 2 else np.stack([x, x], 1)
VOZ = ("aresample=48000,highpass=f=90,afftdn=nr=6:nf=-40:tn=1,"
       "equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1.2:g=2.5,"
       "acompressor=threshold=-24dB:ratio=2.5:attack=8:release=150:makeup=2,aformat=channel_layouts=stereo")
ff("-ss", "0", "-t", str(38 / FPS), "-i", S + "/IMG_1440.mov", "-vn", "-af", VOZ, "-ar", "48000", OUT + "/a1.wav")
ff("-ss", "3.0", "-t", str(129 / FPS), "-i", S + "/IMG_1441.mov", "-vn", "-af", VOZ, "-ar", "48000", OUT + "/a2.wav")
a1, a2 = rd(OUT + "/a1.wav"), rd(OUT + "/a2.wav")
D = np.zeros((N, 2)); i1 = int(38 / FPS * SR); i2 = int(167 / FPS * SR)
a1 = a1[:i1]; D[:len(a1)] = a1 * 0.8
a2 = a2[:i2 - i1]; D[i1:i1 + len(a2)] = a2
# suspense quieto: ambiente de rua 8 dB abaixo fora da fala (fala: 5,00-7,05 s do take = 3,30-5,35 s na saida)
g = np.full(N, 10 ** (-8 / 20)); s0, s1 = int((38 / FPS + 2.00 - 0.08) * SR), int((38 / FPS + 4.05) * SR)
r = int(0.08 * SR); g[s0:s1] = 1.0
g[s0 - r:s0] = np.linspace(10 ** (-8 / 20), 1, r); g[s1:s1 + r] = np.linspace(1, 10 ** (-8 / 20), r)
D *= g[:, None]
k = int(0.015 * SR)
D[i1 - k:i1] *= np.linspace(1, 0, k)[:, None]; D[i1:i1 + k] *= np.linspace(0, 1, k)[:, None]
D[i2 - k:i2] *= np.linspace(1, 0, k)[:, None]
M = rd(P + "/work/musica.wav")[:N - i2]
Mu = np.zeros((N, 2)); Mu[i2:i2 + len(M)] = M
fo = int(0.8 * SR); Mu[N - fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
# musica no mesmo nivel percebido da fala (a fala ja acabou quando ela entra)
rv = np.sqrt(np.mean(D[s0:s1] ** 2)); rm = np.sqrt(np.mean(Mu[i2:] ** 2)) + 1e-12
Mu *= rv / rm * 10 ** (-2.0 / 20)
X = D + Mu; X = X * (0.5 / np.abs(X).max())
w.write(OUT + "/pre.wav", SR, (X * 32767).astype(np.int16))
# ganho fixo (loudnorm dinamico subia o ambiente de novo): mede e ajusta para -14 LUFS
import re
r = subprocess.run([FF, "-i", OUT + "/pre.wav", "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1]); gdb = -14.0 - I
ff("-i", OUT + "/pre.wav", "-af", f"volume={gdb:.2f}dB,alimiter=limit=0.70:level=false:attack=2:release=60,aresample=48000",
   "-ar", "48000", OUT + "/final.wav")
print("ganho", round(gdb, 1))
print("ok")
