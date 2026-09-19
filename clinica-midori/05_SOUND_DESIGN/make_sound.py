#!/usr/bin/env python3
"""Camada de som: ambiencia real da clinica + 2 transicoes discretas.

A ambiencia vem do audio nativo dos proprios clipes (room tone de verdade,
nao biblioteca). As transicoes sao ruido filtrado, sintetizado aqui.
Saida: 05_SOUND_DESIGN/ambiencia.wav e transicoes.wav (48k estereo, 30.6s).
"""
import numpy as np, os, subprocess, wave

SR, DUR = 48000, 30.6
N = int(SR * DUR)
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = os.path.join(RAIZ, "05_SOUND_DESIGN")

FF = "ffmpeg"
FONTES = ["03_lounge-copa-cafe.mov", "01_recepcao-logo-midori.mov", "04_consultorio-01-janela.mov"]

# ---- ambiencia: room tone real, limpo e rebaixado --------------------------
partes = []
for f in FONTES:
    cam = os.path.join(RAIZ, "02_CLINIC_FOOTAGE", f)
    raw = subprocess.run(
        [FF, "-v", "error", "-i", cam,
         "-af", "afftdn=nr=12:nf=-45,highpass=f=60,lowpass=f=7000",
         "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
        capture_output=True).stdout
    partes.append(np.frombuffer(raw, dtype="<f4").reshape(-1, 2).T.copy())

amb = np.concatenate(partes, axis=1)
cruz = int(SR * 0.5)
for i in range(1, len(partes)):                      # suaviza as emendas
    p = sum(x.shape[1] for x in partes[:i])
    if p + cruz < amb.shape[1]:
        amb[:, p-cruz:p] *= np.linspace(1, 0, cruz)
        amb[:, p:p+cruz] *= np.linspace(0, 1, cruz)
while amb.shape[1] < N:
    amb = np.concatenate([amb, amb[:, ::-1]], axis=1)  # espelha em vez de repetir
amb = amb[:, :N]
amb /= max(np.abs(amb).max(), 1e-9)
amb *= 0.30
amb[:, :int(SR*0.8)] *= np.linspace(0, 1, int(SR*0.8))
amb[:, -int(SR*1.2):] *= np.linspace(1, 0, int(SR*1.2))

with wave.open(os.path.join(SAIDA, "ambiencia.wav"), "w") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((amb.T * 32767).astype("<i2").tobytes())

# ---- transicoes: 2 passagens discretas -------------------------------------
tr = np.zeros((2, N))

def passagem(t0, dur=0.9, g=0.13, seed=3):
    n = int(SR * dur); tt = np.arange(n) / SR
    rng = np.random.default_rng(seed)
    s = rng.normal(0, 1, n)
    a = np.exp(-2*np.pi*400/SR); y = np.zeros(n); ant = 0.0
    for i in range(n):                                # passa-baixa movel simples
        ant = (1-a)*s[i] + a*ant
        y[i] = s[i] - ant
    forma = np.sin(np.pi * (tt/dur) ** 1.7) ** 2
    y *= forma
    i0 = int(SR * (t0 - dur * 0.72))
    if i0 < 0: i0 = 0
    m = min(n, N - i0)
    tr[0, i0:i0+m] += y[:m] * g * 0.92
    tr[1, i0:i0+m] += y[:m] * g * 1.00

# tempos por versao: (entrada do bloco clinico, entrada da assinatura)
VERSOES = {"estrutura": (12.0, 26.4), "limpo": (10.2, 16.8)}
for nome, (t_clin, t_marca) in VERSOES.items():
    tr[:] = 0
    passagem(t_clin, 0.85, 0.11, seed=3)
    passagem(t_marca, 1.15, 0.15, seed=11)
    with wave.open(os.path.join(SAIDA, f"transicoes_{nome}.wav"), "w") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((tr.T * 32767).astype("<i2").tobytes())
print("ambiencia.wav + transicoes_estrutura.wav + transicoes_limpo.wav gerados")
