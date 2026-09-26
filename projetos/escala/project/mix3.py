# Mix da versao 3.
# A trilha original nao esta no repositorio. Ela e recuperada do mix da v2:
# PAI-22s (com musica) menos PAI-22s-SEM-MUSICA escalado por trecho. Em cada
# corte da v2 o ambiente tinha ganho fixo, entao o ganho de projecao por trecho
# tira o ambiente e deixa a trilha.
import numpy as np, scipy.io.wavfile as w, scipy.signal as sg, subprocess, os
FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
P = "/home/user/Success-/projetos/escala"; WK = P + "/work"; OUT = WK + "/mix3"
os.makedirs(OUT, exist_ok=True)
SR = 48000; FPS = 30; TOT = 746
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
# o impacto da trilha cai no corte que sai do pai, agora no quadro 279
HIT = 279; OLDHIT = 250
T = np.zeros((int(TOT / FPS * SR), 2))
src0 = int(OLDHIT / FPS * SR); dst0 = int(HIT / FPS * SR)
mm = mus[src0:]
# v8: o gancho ficou maior que a trilha recuperada. repete o 2o e o 3o compasso
# depois do impacto (4 batidas de 90 BPM cada), emendado na batida com cruzamento de 10 ms
b4 = int(4 * 0.666667 * SR); xf = int(0.010 * SR)
a_, b_ = mm[:2 * b4].copy(), mm[b4:].copy()
r_ = np.linspace(0, 1, xf)[:, None]
a_[-xf:] = a_[-xf:] * (1 - r_) + b_[:xf] * r_
mm = np.concatenate([a_, b_[xf:]])
seg = mm[:len(T) - dst0]
T[dst0:dst0 + len(seg)] += seg
# cauda: a trilha desce junto com o escurecimento da vinheta
L = len(T); fo = int(1.1 * SR)
T[L - fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.6

# ---- voz ----
# 1,00 a 10,30 do take (abre na churrasqueira). limpeza leve: grave cortado, ruido de feira reduzido
# sem deixar a voz metalica, presenca em 3 kHz, compressao 3:1
ff("-ss", "1.00", "-t", "9.30", "-i", P + "/source/T05.mov", "-vn", "-af",
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
ramp(HIT / FPS, 19.300, 0.30, 0.30)            # gancho: chiado da carne por baixo
ramp(19.300, 19.967, 0.30, 0.55)               # antecipacao, sobe um pouco
ramp(19.967, 19.974, 0.55, 0.26)              # reveal: a trilha manda
ramp(19.974, TOT / FPS, 0.26, 0.26)
Amb = A * env[:, None]
k = int(0.02 * SR); Amb[dst0:dst0 + k] *= np.linspace(0, 1, k)[:, None]

# ---- impacto sutil no reveal: sub de 48 Hz decaindo, sem clique ----
R = int(599 / FPS * SR); d = int(0.55 * SR); t = np.arange(d) / SR
sub = np.sin(2 * np.pi * (48 - 14 * t) * t) * np.exp(-t * 7.5) * (1 - np.exp(-t * 400))
Hit = np.zeros_like(T); Hit[R:R + d, 0] = Hit[R:R + d, 1] = sub * 0.20

# ---- fundo musical baixo por baixo da fala ----
# trecho da mesma trilha ANTERIOR ao impacto, recuperado da versao 25s
# (ESCALA-25s menos a SEM-MUSICA, janelas de 0,25 s). Nao repete nada do
# que toca depois do impacto.
e25 = rd(WK + "/e25.wav"); s25 = rd(WK + "/e25_sm.wav")
n25 = min(len(e25), len(s25)); e25, s25 = e25[:n25], s25[:n25]
m25 = np.zeros_like(e25); wn = int(0.25 * SR)
for i in range(0, n25, wn):
    x, y = e25[i:i + wn].ravel(), s25[i:i + wn].ravel()
    g = min(max(np.dot(x, y) / (np.dot(y, y) + 1e-12), 0), 1.2)
    m25[i:i + wn] = e25[i:i + wn] - g * s25[i:i + wn]
bed = m25[int(6.10 * SR):int(14.90 * SR)]
# alinha a grade de 90 BPM do fundo com o impacto: uma batida do fundo cai
# exatamente no corte que sai do pai
env_b = np.abs(sg.hilbert(bed.mean(1)))
env_b = sg.resample_poly(env_b, 1, 480)             # 100 Hz
on = np.maximum(np.diff(env_b), 0); beat = 0.66667
ph = np.arange(0, beat, 0.01)
score = [on[np.clip(((np.arange(0, len(on) / 100 - beat, beat) + p) * 100).astype(int), 0, len(on) - 1)].sum() for p in ph]
p0 = ph[int(np.argmax(score))]                       # fase da batida dentro do fundo
L = len(bed) / SR
end_t = HIT / FPS                                    # o fundo termina no impacto
k = int(np.floor((L - p0) / beat))                  # ultima batida inteira do trecho
cut = p0 + k * beat                                  # corta o fundo numa batida
bed = bed[:int(cut * SR)]
# o fundo tem que tocar desde o quadro 0 (pedido do cliente): comeca o trecho
# numa batida e repete o 1o compasso na frente, emendado com 10 ms, ate cobrir
# toda a fala. a grade de 90 BPM continua passando pelo impacto
bed = bed[int(p0 * SR):]
bar = int(4 * beat * SR); xf = int(0.010 * SR); rr = np.linspace(0, 1, xf)[:, None]
while len(bed) / SR < end_t:
    lp = bed[:bar].copy(); nx = bed.copy()
    lp[-xf:] = lp[-xf:] * (1 - rr) + nx[:xf] * rr
    bed = np.concatenate([lp, nx[xf:]])
start = end_t - len(bed) / SR
if start < 0: bed = bed[int(-start * SR):]; start = 0.0
b1, a1 = sg.butter(2, 150 / (SR / 2), "high"); bed = sg.lfilter(b1, a1, bed, axis=0)
# abre espaco para a voz: -4 dB na faixa de 1 a 4 kHz
bb, ab = sg.butter(2, [1000 / (SR / 2), 4000 / (SR / 2)], "band")
bed = bed - (1 - 10 ** (-4 / 20)) * sg.lfilter(bb, ab, bed, axis=0)
Bed = np.zeros_like(T); i0 = int(start * SR); Bed[i0:i0 + len(bed)] = bed
fi = int(0.25 * SR); Bed[i0:i0 + fi] *= np.linspace(0, 1, fi)[:, None]   # ja no comeco, so sem clique
fo2 = int(0.03 * SR); Bed[dst0 - fo2:dst0] *= np.linspace(1, 0, fo2)[:, None]
# fica 17 dB abaixo da voz
vr = np.sqrt(np.mean(voz[:dst0] ** 2)); br = np.sqrt(np.mean(Bed[i0:dst0] ** 2)) + 1e-12
Bed *= vr / br * 10 ** (-17 / 20)
print("fundo: %.2f s, entra em %.2f s, fase %.2f" % (len(bed) / SR, start, p0))

def lvl(x): return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)
full = voz + Bed + T + Amb + Hit
seco = voz + A * np.where(np.arange(len(T)) < dst0, 0, 0.9)[:, None]
for nm, x in (("com", full), ("sem", seco)):
    x = x * (0.5 / np.abs(x).max())  # sem clipar antes do loudnorm
    w.write(OUT + f"/pre_{nm}.wav", SR, (x * 32767).astype(np.int16))
    # -14 LUFS, pico abaixo de -1 dBTP
    ff("-i", OUT + f"/pre_{nm}.wav", "-af", "loudnorm=I=-14:TP=-1.2:LRA=9,alimiter=limit=0.61:level=false:attack=2:release=60,aresample=48000",
       "-ar", "48000", OUT + f"/final_{nm}.wav")
print("voz", round(lvl(voz[:dst0]), 1), "trilha", round(lvl(T[dst0:]), 1),
      "amb", round(lvl(Amb[dst0:]), 1))
