#!/usr/bin/env python3
"""Prepara um trecho de um vídeo do cardápio: lê com a rotação do iPhone, reduz para 1080x1920 (ou 2160x3840 para
macro), estabiliza (vidstab, 2 passadas, movimento de câmera bem suavizado = 'órbita de grua') e deixa em câmera lenta
com quadros intermediários reais (minterpolate) quando speed < 1. Saída sem cor (a cor é aplicada no render).

    python3 prep.py SRC IN OUT SPEED SMOOTH OUT_PATH [SCALE]
"""
import subprocess, sys, os
FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
src, a, b, speed, smooth, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
scale = int(sys.argv[7]) if len(sys.argv) > 7 else 1
W, H = 1080 * scale, 1920 * scale
trf = out + ".trf"
base = f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},fps=30"
subprocess.run([FF, "-y", "-v", "error", "-ss", str(a), "-t", str(b - a), "-i", src, "-vf",
                f"{base},vidstabdetect=shakiness=7:accuracy=15:stepsize=6:result={trf}", "-f", "null", "-"], check=True)
vf = f"{base},vidstabtransform=input={trf}:smoothing={smooth}:optzoom=1:zoomspeed=0.1:interpol=bicubic,unsharp=5:5:0.4"
if speed < 0.999:
    vf += f",setpts={1/speed:.4f}*PTS,minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1"
subprocess.run([FF, "-y", "-v", "error", "-ss", str(a), "-t", str(b - a), "-i", src, "-vf", vf, "-an",
                "-c:v", "libx264", "-preset", "medium", "-crf", "12", "-pix_fmt", "yuv420p", out], check=True)
os.remove(trf)
print(out)
