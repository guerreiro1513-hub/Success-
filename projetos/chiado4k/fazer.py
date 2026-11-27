#!/usr/bin/env python3
"""Tira a música (com direitos autorais) do vídeo da churrasqueira e coloca só o chiado real da churrasqueira do
Guerreiro's Grill; sobe para 4K (2160x3840).

A música estava misturada no mesmo canal do som da churrasqueira e domina o vídeo inteiro (medido: espectro tonal
em todos os trechos). Separar sem modelo de IA não fica limpo (os modelos estão bloqueados pela rede), então o áudio
é TROCADO pelo chiado real da churrasqueira, recortado do vídeo do Florais (entrega/guerreiros-FLORAIS-QUI-A-DOM.mp4,
11,6–21,0 s: só a churrasqueira, sem voz e sem música), emendado com cruzamentos suaves até cobrir o vídeo.

    python3 fazer.py work/ORIGINAL.mov ../../entrega/guerreiros-CHURRASQUEIRA-4K.mp4
"""
import subprocess, sys, numpy as np
from scipy.io import wavfile
SR = 48000
src, out = sys.argv[1], sys.argv[2]
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                           capture_output=True, text=True).stdout)
raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", "11.6", "-t", "9.4", "-i", "../../entrega/guerreiros-FLORAIS-QUI-A-DOM.mp4",
                      "-vn", "-ac", "2", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True, check=True).stdout
bed = np.frombuffer(raw, np.int16).reshape(-1, 2).astype(np.float32) / 32768
n = int(dur * SR); A = np.zeros((n, 2), np.float32)
x = int(1.2 * SR)                                          # cruzamento de 1,2 s entre as voltas
starts = [0.0, 2.7, 5.1, 1.3]                              # cada volta começa num ponto diferente (sem repetição óbvia)
pos, k = 0, 0
while pos < n:
    seg = bed[int(starts[k % len(starts)] * SR):]
    if k % 2: seg = seg[:, ::-1]                           # alterna os canais
    m = min(len(seg), n - pos)
    seg = seg[:m].copy()
    if pos > 0:
        seg[:x] *= np.sqrt(np.linspace(0, 1, x))[:, None]; A[pos:pos + x] *= np.sqrt(np.linspace(1, 0, x))[:, None]
    A[pos:pos + m] += seg
    if pos + m >= n: break                                 # cobriu o vídeo inteiro
    pos += m - x; k += 1
fi, fo = int(0.3 * SR), int(1.2 * SR)
A[:fi] *= np.linspace(0, 1, fi)[:, None]; A[-fo:] *= np.linspace(1, 0, fo)[:, None]
wav = "work/chiado.wav"; wavfile.write(wav, SR, (np.clip(A, -1, 1) * 32767).astype(np.int16))
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-i", wav, "-map", "0:v", "-map", "1:a",
                "-vf", "hqdn3d=1.2:1.2:3:3,scale=2160:3840:flags=lanczos,cas=strength=0.45,format=yuv420p",
                "-c:v", "libx265", "-preset", "medium", "-crf", "20", "-tag:v", "hvc1",
                "-x265-params", "log-level=error", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                "-af", "highpass=f=90,loudnorm=I=-16:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k",
                "-movflags", "+faststart", "-shortest", out], check=True)
print(out)
