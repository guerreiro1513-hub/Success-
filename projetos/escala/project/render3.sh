#!/bin/bash
# Junta base.mov (imagem), tx3/ (texto) e o mix, e exporta as duas entregas.
set -e
FF=/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2
P=/home/user/Success-/projetos/escala; WK=$P/work; E=/home/user/Success-/entrega
for V in com sem; do
  case $V in com) OUT=$E/guerreiros-ESCALA-V6-20s.mp4;; sem) OUT=$E/guerreiros-ESCALA-V6-20s-SEM-MUSICA.mp4;; esac
  $FF -y -hide_banner -loglevel error -i $WK/cut3/base.mov -framerate 30 -i $WK/tx3/t_%04d.png \
    -i $WK/mix3/final_$V.wav \
    -filter_complex "[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v]" \
    -map "[v]" -map 2:a -r 30 -frames:v 606 \
    -c:v libx264 -profile:v high -level 4.1 -preset slow -crf 18 -maxrate 12M -bufsize 20M \
    -g 60 -bf 2 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
    -c:a aac -b:a 192k -ar 48000 -movflags +faststart -shortest "$OUT"
  echo "$OUT"
done
