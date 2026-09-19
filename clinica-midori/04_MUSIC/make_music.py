#!/usr/bin/env python3
"""Trilha SCRATCH original, sintetizada aqui — 100 BPM, 29.4s.

NAO e trilha final. Serve pra travar o ritmo do corte: cada corte do
timeline.json cai exatamente num tempo desta trilha. Quando entrar a trilha
definitiva (Epidemic / Artlist / biblioteca comercial), e so escolher uma de
100 BPM e trocar o arquivo — os cortes continuam sincronizados.
"""
import numpy as np, os, wave

SR   = 48000
BPM  = 100.0
BEAT = 60.0 / BPM          # 0.6s
BAR  = BEAT * 4            # 2.4s
DUR  = 30.6
N    = int(SR * DUR)
t    = np.arange(N) / SR
mix  = np.zeros((2, N))

def idx(seg):  # segundos -> amostra
    return int(seg * SR)

def por(nome, oit=0):
    semis = {'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':7,'G#':8,'A':9,'A#':10,'B':11}
    return 261.625565 * 2 ** (semis[nome] / 12 + oit)

def env(n, ataque, decai, sustenta, solta):
    e = np.ones(n)
    a, d, r = idx(ataque), idx(decai), idx(solta)
    a, d, r = min(a, n), min(d, n), min(r, n)
    if a: e[:a] = np.linspace(0, 1, a) ** 1.6
    if d: e[a:a+d] = np.linspace(1, sustenta, d)
    e[a+d:] = sustenta
    if r: e[-r:] *= np.linspace(1, 0, r) ** 1.4
    return e

def passa_baixa(x, corte):
    a = np.exp(-2 * np.pi * corte / SR)
    y = np.zeros_like(x); ant = 0.0
    for i in range(len(x)):
        ant = (1 - a) * x[i] + a * ant
        y[i] = ant
    return y

def soma(sig, t0, pan=0.5, g=1.0):
    i0 = idx(t0); n = min(len(sig), N - i0)
    if n <= 0: return
    mix[0, i0:i0+n] += sig[:n] * g * (1 - pan)
    mix[1, i0:i0+n] += sig[:n] * g * pan

# ---------------------------------------------------------------- pad
def pad(notas, t0, dur, g=0.16, brilho=900):
    n = idx(dur); tt = np.arange(n) / SR
    s = np.zeros(n)
    for k, f in enumerate(notas):
        for det in (-0.16, 0.0, 0.16):        # leve coro
            s += np.sin(2*np.pi*(f+det)*tt + k) / (1 + 0.55*k)
        s += 0.22 * np.sin(2*np.pi*2*f*tt) / (1 + k)
    s /= len(notas) * 3
    s = passa_baixa(s, brilho)
    s *= env(n, 0.55, 0.30, 0.82, 0.70)
    soma(s, t0, 0.5, g)

# ------------------------------------------------------------- sininho
def sino(f, t0, g=0.10, dur=1.1, pan=0.5):
    n = idx(dur); tt = np.arange(n) / SR
    s = (np.sin(2*np.pi*f*tt) + 0.42*np.sin(2*np.pi*2.01*f*tt)
         + 0.16*np.sin(2*np.pi*3.02*f*tt))
    s *= np.exp(-tt * 4.2)
    s *= np.minimum(1, tt * SR / 120)
    soma(s, t0, pan, g)

# ------------------------------------------------------------- pulso
def bumbo(t0, g=0.30):
    n = idx(0.30); tt = np.arange(n) / SR
    f = 92 * np.exp(-tt * 22) + 42
    s = np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-tt * 9.5)
    soma(s, t0, 0.5, g)

def chocalho(t0, g=0.055):
    n = idx(0.075); tt = np.arange(n) / SR
    rng = np.random.default_rng(int(t0*1000) % 9973)
    s = rng.normal(0, 1, n) * np.exp(-tt * 55)
    s = s - passa_baixa(s, 2800)          # tira grave
    soma(s, t0, 0.55, g)

def subida(t0, dur, g=0.14):
    n = idx(dur); tt = np.arange(n) / SR
    rng = np.random.default_rng(31)
    s = rng.normal(0, 1, n)
    s = s - passa_baixa(s, 300)
    s *= (tt / dur) ** 2.2
    s *= (0.6 + 0.4*np.sin(2*np.pi*0.8*tt))
    soma(s, t0, 0.5, g)

# ---------------------------------------------------------------- arranjo
# Fmaj7 | Am7 | Dm7 | Bbmaj7  (x3) — 2,4s por compasso
acordes = [
    [por('F',-1), por('A'), por('C',1), por('E',1)],
    [por('A',-1), por('C'), por('E',1), por('G',1)],
    [por('D',-1), por('F'), por('A'), por('C',1)],
    [por('A#',-2), por('D'), por('F'), por('A')],
]
for b in range(13):
    ac = acordes[b % 4]
    t0 = b * BAR
    if t0 >= DUR: break
    brilho = 620 if t0 < 3.6 else (760 if 19.2 <= t0 < 22.8 else 1150)
    ganho  = 0.13 if t0 < 3.6 else (0.12 if 19.2 <= t0 < 22.8 else 0.17)
    if t0 >= 26.4: ganho = 0.20
    pad(ac, t0, BAR * 1.05, g=ganho, brilho=brilho)

# sininhos a partir de 3.6s, pausa na entrevista
padrao = [0, 1.5, 2.5, 3.5]
for b in range(1, 13):
    t0 = b * BAR
    if t0 < 3.6 or t0 >= DUR: continue
    if 19.2 <= t0 < 22.8: continue
    ac = acordes[b % 4]
    for j, p in enumerate(padrao):
        tn = t0 + p * BEAT
        if tn >= DUR: break
        f = ac[2 + (j % 2)] * 2
        sino(f, tn, g=0.085 if j % 2 else 0.11, pan=0.38 + 0.24 * (j % 2))

# pulso a partir de 10.2s, fora da entrevista
tb = 10.2
while tb < DUR - 0.4:
    if not (19.2 <= tb < 22.8):
        bumbo(tb, g=0.26 if tb < 22.8 else 0.30)
    tb += BEAT * 2
ts = 12.0
while ts < DUR - 0.4:
    if not (19.2 <= ts < 22.8):
        chocalho(ts)
    ts += BEAT

subida(22.2, 4.2, g=0.13)      # sobe pra assinatura
bumbo(26.4, g=0.40)            # impacto da marca

# ---------------------------------------------------------------- reverb
ir_n = idx(1.6)
rng = np.random.default_rng(5)
ir = rng.normal(0, 1, ir_n) * np.exp(-np.arange(ir_n) / SR * 3.6)
ir = passa_baixa(ir, 3800); ir /= np.abs(ir).sum()
molhado = np.zeros_like(mix)
for c in range(2):
    molhado[c] = np.convolve(mix[c], ir)[:N]
mix = mix * 0.80 + molhado * 0.45

# fade final + normalizacao
saida_n = idx(1.6)
mix[:, -saida_n:] *= np.linspace(1, 0, saida_n) ** 1.5
mix[:, :idx(0.25)] *= np.linspace(0, 1, idx(0.25))
mix /= max(np.abs(mix).max(), 1e-9)
mix *= 0.72

cam = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trilha-scratch-100bpm.wav")
with wave.open(cam, "w") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix.T * 32767).astype("<i2").tobytes())
print("trilha:", cam, f"{DUR}s @ {BPM:.0f} BPM")
