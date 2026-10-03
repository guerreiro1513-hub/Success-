# Redução de ruído de carro/rua por subtração espectral (STFT), com perfil de
# ruído tirado dos trechos sem fala do proprio take. Uso: denoise.py in.wav out.wav "a-b,c-d"
import sys, numpy as np, scipy.io.wavfile as w, scipy.signal as sg
src, dst, spans = sys.argv[1], sys.argv[2], sys.argv[3]
sr, x = w.read(src); x = x.astype(np.float64) / 32768
if x.ndim == 1: x = x[:, None]
NP = 2048; HOP = 512
out = np.zeros_like(x)
for ch in range(x.shape[1]):
    f, t, Z = sg.stft(x[:, ch], sr, nperseg=NP, noverlap=NP - HOP)
    mag, ph = np.abs(Z), np.angle(Z)
    idx = np.zeros(len(t), bool)
    for s in spans.split(","):
        a, b = map(float, s.split("-")); idx |= (t >= a) & (t <= b)
    noise = np.percentile(mag[:, idx], 80, axis=1)[:, None]
    # sobre-subtracao forte no grave (motor/pneu), mais leve na faixa da voz
    k = np.where(f < 250, 2.5, np.where(f < 4000, 1.0, 1.8))[:, None]
    g = np.maximum(1 - k * noise / (mag + 1e-12), 0.10)
    g = sg.medfilt2d(g, (3, 5))                     # sem "agua"/artefato musical
    _, y = sg.istft(mag * g * np.exp(1j * ph), sr, nperseg=NP, noverlap=NP - HOP)
    out[:, ch] = y[:len(x)]
w.write(dst, sr, (np.clip(out, -1, 1) * 32767).astype(np.int16))
