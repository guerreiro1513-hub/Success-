# Bastidor v5 — som: so a musica. Trilha C (groove funk, Kairogen) no lugar da A.
# Trilha A gerada no Kairogen (sertanejo-funk, ~133 BPM), comecando em 0,90 s
# (2 batidas) para a virada cair no take novo depois do gancho mais curto.
import numpy as np, scipy.io.wavfile as w, subprocess, os
FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
P = "/home/user/Success-/projetos/bastidor"; WK = P + "/work"; OUT = WK + "/mix"
os.makedirs(OUT, exist_ok=True)
SR = 48000; FPS = 30; TOT = 480; OFF = 0.44
def rd(p):
    x = w.read(p)[1].astype(np.float64) / 32768
    return x if x.ndim == 2 else np.stack([x, x], 1)
N = int(TOT / FPS * SR)
M = rd(WK + "/m_C_groove.wav")[int(OFF * SR):int(OFF * SR) + N]
M = np.pad(M, ((0, N - len(M)), (0, 0)))
fo = int(0.6 * SR); M[N - fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
M = M * (0.5 / np.abs(M).max())
w.write(OUT + "/pre_com.wav", SR, (M * 32767).astype(np.int16))
subprocess.run([FF, "-y", "-v", "error", "-i", OUT + "/pre_com.wav", "-af",
    "loudnorm=I=-14:TP=-1.5:LRA=9,alimiter=limit=0.74:level=false:attack=2:release=60,aresample=48000",
    "-ar", "48000", OUT + "/final_com.wav"], check=True)
print("ok", TOT, "quadros")
