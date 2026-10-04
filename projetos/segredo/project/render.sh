#!/bin/bash
# v5: acabamento de cinema (halation nas altas luzes + grao fino) em tudo menos a vinheta,
# depois texto e som.
set -e
FF=/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2
WK=/home/user/Success-/projetos/segredo/work; C=$WK/cut; O=/home/user/Success-/entrega/guerreiros-SEGREDO-15s.mp4
ENC="-c:v libx264 -preset medium -crf 14 -pix_fmt yuv420p -an"
$FF -y -hide_banner -loglevel error -i $C/base.mov -filter_complex "[0:v]setpts=N/(30*TB),format=gbrp,split[g][h];\
[h]curves=all='0/0 0.80/0 1/1',gblur=sigma=20,colorchannelmixer=rr=1:gg=0.5:bb=0.3[hl];\
[g][hl]blend=all_mode=screen:all_opacity=0.16,format=yuv420p,noise=alls=4:allf=t[v]" \
  -map "[v]" -frames:v 421 -r 30 $ENC $C/fin_a.mov
$FF -y -hide_banner -loglevel error -i $C/base.mov -vf "setpts=N/(30*TB),trim=start_frame=421,setpts=PTS-STARTPTS,format=yuv420p" -r 30 $ENC $C/fin_b.mov
printf "file '%s'\nfile '%s'\n" $C/fin_a.mov $C/fin_b.mov > $C/fin.txt
$FF -y -hide_banner -loglevel error -f concat -safe 0 -i $C/fin.txt -c copy $C/fin.mov
$FF -y -hide_banner -loglevel error -i $C/fin.mov -framerate 30 -i $WK/tx/t_%04d.png -i $WK/mix/final.wav \
  -filter_complex "[0:v]tpad=stop_mode=clone:stop=2[b];[b][1:v]overlay=0:0:format=auto,format=yuv420p[v]" -map "[v]" -map 2:a -frames:v 468 \
  -c:v libx264 -profile:v high -level 4.1 -preset slow -crf 18 -maxrate 10M -bufsize 16M -g 60 -bf 2 \
  -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
  -c:a aac -b:a 192k -ar 48000 -movflags +faststart -shortest "$O"
echo "$O"
