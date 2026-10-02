#!/bin/bash
# Bastidor v5 CINEMA: versao alternativa com look de cinema por cima da v5.
# Aplicado so nas cenas (0-432); a vinheta da marca (433-479) fica intacta.
#  - curva filmica: preto levemente erguido, altas com rolagem suave
#  - sombras frias / altas quentes (teal & orange contido, pele preservada)
#  - halation: brilho avermelhado em volta das altas luzes (como pelicula)
#  - vinheta leve e grao fino temporal
set -e
FF=/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2
WK=/home/user/Success-/projetos/bastidor/work; O=/home/user/Success-/entrega/guerreiros-BASTIDOR-16s-CINEMA.mp4
LOOK="eq=saturation=0.97:contrast=1.06:gamma=1.07,\
colorbalance=rs=-0.05:gs=-0.01:bs=0.06:rm=0.015:bm=-0.015:rh=0.05:gh=0.015:bh=-0.05:pl=1,\
curves=all='0/0.015 0.2/0.17 0.5/0.54 0.8/0.85 1/0.96'"
C=$WK/cut; ENC="-c:v libx264 -preset medium -crf 14 -pix_fmt yuv420p -an"
# 1) cenas com o look (quadros 0-432)
$FF -y -hide_banner -loglevel error -i $C/base.mov -filter_complex "[0:v]setpts=N/(30*TB),${LOOK},format=gbrp,split[g][h];\
[h]curves=all='0/0 0.82/0 1/1',gblur=sigma=22,colorchannelmixer=rr=1:gg=0.45:bb=0.25[hl];\
[g][hl]blend=all_mode=screen:all_opacity=0.18,vignette=angle=PI/8:mode=forward,format=yuv420p,noise=alls=5:allf=t[v]" \
  -map "[v]" -frames:v 433 -r 30 $ENC $C/cine_a.mov
# 2) vinheta intacta (433 em diante)
$FF -y -hide_banner -loglevel error -i $C/base.mov -vf "setpts=N/(30*TB),trim=start_frame=433,setpts=PTS-STARTPTS,format=yuv420p" -r 30 $ENC $C/cine_b.mov
printf "file '%s'\nfile '%s'\n" $C/cine_a.mov $C/cine_b.mov > $C/cine.txt
$FF -y -hide_banner -loglevel error -f concat -safe 0 -i $C/cine.txt -c copy $C/cine.mov
# 3) texto + musica
$FF -y -hide_banner -loglevel error -i $C/cine.mov -framerate 30 -i $WK/tx/t_%04d.png -i $WK/mix/final_com.wav \
  -filter_complex "[0:v]tpad=stop_mode=clone:stop=2[b];[b][1:v]overlay=0:0:format=auto,format=yuv420p[v]" \
  -map "[v]" -map 2:a -frames:v 480 \
  -c:v libx264 -profile:v high -level 4.1 -preset slow -crf 18 -maxrate 10M -bufsize 16M -g 60 -bf 2 -tune film \
  -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
  -c:a aac -b:a 192k -ar 48000 -movflags +faststart -shortest "$O"
echo "$O"
