# Mix da versao 3.
# A trilha original nao esta no repositorio. Ela e recuperada do mix da v2:
# PAI-22s (com musica) menos PAI-22s-SEM-MUSICA escalado por trecho. Em cada
# corte da v2 o ambiente tinha ganho fixo, entao o ganho de projecao por trecho
# tira o ambiente e deixa a trilha.
import numpy as np, scipy.io.wavfile as w, scipy.signal as sg, subprocess, os
FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
P = "/home/user/Success-/projetos/escala"; WK = P + "/work"; OUT = WK + "/mix3"
os.makedirs(OUT, exist_ok=True)
SR = 48000; FPS = 30; TOT = 626
def rd(p):
    sr, x = w.read(p); assert sr == SR
    x = x.astype(np.float64) / 32768.0
    return x if x.ndim == 2 else np.stack([x, x], 1)
def ff(*a): subprocess.run([FF, "-y", "-v", "error", *a], check=True)

# ---- trilha ----
mix = rd(WK + "/pai.wav"); sm = rd(WK + "/pai_sm.wav")
n = min(len(mix), len(sm)); mix, sm = mix[:n], sm[:n]
B = [250, 290, 320, 340, 360, 370, 380, 480, 520, 540, 570, 590, 620, 660]  # cortes da v2
mus = np.zeros_like(mix)
for a, b in zip(B[:-1], B[1:]):
    i, j = int(a / FPS * SR), min(n, int(b / FPS * SR))
    m, s = mix[i:j].ravel(), sm[i:j].ravel()
    g = float(np.dot(m, s) / (np.dot(s, s) + 1e-12))
    mus[i:j] = mix[i:j] - g * sm[i:j]
# o impacto da trilha cai no corte que sai do pai, agora no quadro 309
HIT = 309; OLDHIT = 250
T = np.zeros((int(TOT / FPS * SR), 2))
src0 = int(OLDHIT / FPS * SR); dst0 = int(HIT / FPS * SR)
seg = mus[src0:src0 + len(T) - dst0]
T[dst0:dst0 + len(seg)] += seg
# cauda: a trilha desce junto com o escurecimento da vinheta
L = len(T); fo = int(1.1 * SR)
T[L - fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.6

# ---- voz ----
# 0,00 a 10,30 do take (abre na churrasqueira). limpeza leve: grave cortado, ruido de feira reduzido
# sem deixar a voz metalica, presenca em 3 kHz, compressao 3:1
ff("-ss", "0", "-t", "10.30", "-i", P + "/source/T05.mov", "-vn", "-af",
   "aresample=48000,highpass=f=95,afftdn=nr=8:nf=-38:tn=1,"
   "equalizer=f=220:t=q:w=1.0:g=-2.5,equalizer=f=3000:t=q:w=1.2:g=3,"
   "equalizer=f=7000:t=q:w=1.5:g=-1.5,"
   "acompressor=threshold=-22dB:ratio=3:attack=8:release=120:makeup=3,"
   "aformat=channel_layouts=stereo", "-ar", "48000", OUT + "/voz.wav")
V = rd(OUT + "/voz.wav")
voz = np.zeros_like(T); voz[:min(len(V), dst0)] = V[:dst0] * 10 ** (2.5 / 20)
# micro fade na saida da voz para o corte seco nao estalar
k = int(0.012 * SR); voz[dst0 - k:dst0] *= np.linspace(1, 0, k)[:, None]

# ---- ambiente real de cada corte, por baixo da trilha ----
ff("-i", WK + "/cut3/base.mov", "-vn", "-ac", "2", "-ar", "48000", OUT + "/amb.wav")
A = rd(OUT + "/amb.wav")[:len(T)]
A = np.pad(A, ((0, len(T) - len(A)), (0, 0)))
A[:dst0] = 0  # a voz tratada ja carrega o ambiente dela
b, a = sg.butter(2, 120 / (SR / 2), "high"); A = sg.lfilter(b, a, A, axis=0)
env = np.zeros(len(T))
def ramp(t0, t1, v0, v1):
    i, j = int(t0 * SR), int(t1 * SR); env[i:j] = np.linspace(v0, v1, j - i)
ramp(HIT / FPS, 13.967, 0.30, 0.30)            # gancho: chiado da carne por baixo
ramp(13.967, 14.633, 0.30, 0.55)               # antecipacao, sobe um pouco
ramp(14.633, 14.64, 0.55, 0.26)              # reveal: a trilha manda
ramp(14.64, TOT / FPS, 0.26, 0.26)
Amb = A * env[:, None]
k = int(0.02 * SR); Amb[dst0:dst0 + k] *= np.linspace(0, 1, k)[:, None]

# ---- impacto sutil no reveal: sub de 48 Hz decaindo, sem clique ----
R = int(439 / FPS * SR); d = int(0.55 * SR); t = np.arange(d) / SR
sub = np.sin(2 * np.pi * (48 - 14 * t) * t) * np.exp(-t * 7.5) * (1 - np.exp(-t * 400))
Hit = np.zeros_like(T); Hit[R:R + d, 0] = Hit[R:R + d, 1] = sub * 0.20

def lvl(x): return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)
full = voz + T + Amb + Hit
seco = voz + A * np.where(np.arange(len(T)) < dst0, 0, 0.9)[:, None]
for nm, x in (("com", full), ("sem", seco)):
    x = x * (0.5 / np.abs(x).max())  # sem clipar antes do loudnorm
    w.write(OUT + f"/pre_{nm}.wav", SR, (x * 32767).astype(np.int16))
    # -14 LUFS, pico abaixo de -1 dBTP
    ff("-i", OUT + f"/pre_{nm}.wav", "-af", "loudnorm=I=-14:TP=-1.2:LRA=9,alimiter=limit=0.72:level=false:attack=2:release=60,aresample=48000",
       "-ar", "48000", OUT + f"/final_{nm}.wav")
print("voz", round(lvl(voz[:dst0]), 1), "trilha", round(lvl(T[dst0:]), 1),
      "amb", round(lvl(Amb[dst0:]), 1))
