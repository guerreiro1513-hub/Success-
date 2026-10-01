#!/bin/bash
# Bastidor v4: uma entrega so, com a musica (sem o audio dos takes, a pedido)
set -e
FF=/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2
WK=/home/user/Success-/projetos/bastidor/work; O=/home/user/Success-/entrega/guerreiros-BASTIDOR-16s.mp4
$FF -y -hide_banner -loglevel error -i $WK/cut/base.mov -framerate 30 -i $WK/tx/t_%04d.png -i $WK/mix/final_com.wav \
  -filter_complex "[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v]" -map "[v]" -map 2:a -frames:v 480 \
  -c:v libx264 -profile:v high -level 4.1 -preset slow -crf 17 -maxrate 14M -bufsize 24M -g 60 -bf 2 \
  -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
  -c:a aac -b:a 192k -ar 48000 -movflags +faststart -shortest "$O"
echo "$O"
