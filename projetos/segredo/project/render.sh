#!/bin/bash
set -e
FF=/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2
WK=/home/user/Success-/projetos/segredo/work; O=/home/user/Success-/entrega/guerreiros-SEGREDO-11s.mp4
$FF -y -hide_banner -loglevel error -i $WK/cut/base.mov -framerate 30 -i $WK/tx/t_%04d.png -i $WK/mix/final.wav \
  -filter_complex "[0:v]tpad=stop_mode=clone:stop=2[b];[b][1:v]overlay=0:0:format=auto,format=yuv420p[v]" -map "[v]" -map 2:a -frames:v 337 \
  -c:v libx264 -profile:v high -level 4.1 -preset slow -crf 18 -maxrate 10M -bufsize 16M -g 60 -bf 2 \
  -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
  -c:a aac -b:a 192k -ar 48000 -movflags +faststart -shortest "$O"
echo "$O"
