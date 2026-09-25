#!/bin/bash
# Bronca Fake v2 — so os videos 1 e 2, na linguagem do video-modelo:
# bronca em preto e branco, corte seco para a cor quando a carne aparece,
# logo por cima no fim. Sem legenda (o cliente coloca depois).
set -e
FF=/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2
P=/home/user/Success-/projetos/bronca; WK=$P/work/cut; mkdir -p $WK
W=1080; H=1920; CRF=15; PRE=${PRE:-medium}
CV="curves=all='0/0.01 0.22/0.19 0.5/0.52 0.78/0.83 0.94/0.945 1/0.975'"
# cor: correcao leve, pele e carne naturais, sem empurrar o laranja
GC="eq=contrast=1.08:saturation=1.04,vibrance=intensity=0.16,${CV},unsharp=5:5:0.35"
# preto e branco com corpo, como no modelo: contraste alto, altas seguradas
BW="hue=s=0,eq=contrast=1.16:brightness=-0.01,curves=all='0/0.02 0.25/0.20 0.5/0.52 0.8/0.85 1/0.97',unsharp=5:5:0.35"
cl(){ ID=$1;SRC=$2;SS=$3;NF=$4;Z0=$5;Z1=$6;FX=$7;FY=$8;G=$9
  DU=$(python3 -c "print($NF/30)"); SD=$(python3 -c "print(round($NF/30+0.3,3))")
  E="($Z0+($Z1-$Z0)*t/$DU)"
  # o video 1 e exportacao do CapCut: quadro a quadro, sem reconversao de fps
  case $SRC in *T12*) FR="setpts=N/(30*TB)";; *) FR="fps=30";; esac
  $FF -y -ss $SS -t $SD -i "$SRC" -filter_complex \
   "[0:v]scale=${W}*2:${H}*2:force_original_aspect_ratio=increase:flags=lanczos,crop=${W}*2:${H}*2,setsar=1,${FR},\
scale=w='trunc(${W}*${E}/2)*2':h='trunc(${H}*${E}/2)*2':eval=frame:flags=lanczos,\
crop=${W}:${H}:x='(iw-${W})*${FX}':y='(ih-${H})*${FY}',${G},setsar=1,format=yuv420p[v];\
[0:a]aresample=48000,aformat=channel_layouts=stereo[a]" \
   -map "[v]" -map "[a]" -frames:v $NF -r 30 -c:v libx264 -preset $PRE -crf $CRF -c:a pcm_s16le "$WK/$ID.mov" -loglevel error; }

# 1 video 2 (IMG_1442, 4K), 1,00 a 1,77: trabalhando calado e serio
cl q1 $P/source/T13.mov 1.00  23 1.06 1.08 0.58 0.30 "$BW"
# 2 video 2, 1,77 a 6,30: levanta a cabeca e da a bronca olhando para a camera.
#   punch-in seco no corte (1,08 -> 1,22), a fala inteira sem picotar
cl q2 $P/source/T13.mov 1.767 136 1.22 1.17 0.60 0.28 "$BW"
# 3 video 1 do inicio do 2o take ate o fim, 8,67 a 17,73 (a emenda do CapCut vai ate 8,63): corte seco para a cor. ele na churrasqueira, a camera abre, cestos cheios girando
#   na frente, ele andando e abrindo os bracos. fonte 1080p: aproximacao ate 1,05
cl e1 $P/source/T12.mov 8.667 272 1.00 1.05 0.50 0.40 "$GC"
# 4 ultimo quadro do video 1 parado, aproximacao lenta, logo por cima (camada de texto)
$FF -y -loglevel error -sseof -0.04 -i $WK/e1.mov -frames:v 1 -update 1 $WK/last.png
$FF -y -loglevel error -loop 1 -framerate 30 -i $WK/last.png -f lavfi -i anullsrc=r=48000:cl=stereo \
 -filter_complex "[0:v]scale=w='trunc(${W}*(1.00+0.035*t/1.2)/2)*2':h='trunc(${H}*(1.00+0.035*t/1.2)/2)*2':eval=frame:flags=lanczos,crop=${W}:${H},setsar=1,format=yuv420p[v]" \
 -map "[v]" -map 1:a -frames:v 36 -r 30 -c:v libx264 -preset $PRE -crf $CRF -c:a pcm_s16le -t 1.2 $WK/f1.mov
for i in q1 q2 e1 f1; do echo "file '$WK/$i.mov'"; done > $WK/list.txt
$FF -y -hide_banner -loglevel error -f concat -safe 0 -i $WK/list.txt -c:v copy -c:a pcm_s16le $WK/base.mov
echo base ok
