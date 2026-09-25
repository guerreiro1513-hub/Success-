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

# 1 video 2 (IMG_1442, 4K), 0,40 a 1,77: trabalhando calado e serio (mais longo
#   para a frase da trend ter tempo de ser lida)
cl q1 $P/source/T13.mov 0.40  41 1.06 1.09 0.58 0.30 "$BW"
# 2 video 2, 1,77 a 8,00: levanta a cabeca e da a bronca olhando para a camera,
#   ate o fim da ultima frase (7,96). punch-in seco no corte, a fala inteira
cl q2 $P/source/T13.mov 1.767 187 1.22 1.15 0.60 0.28 "$BW"
# 3 video 1 de 4,70 ate o fim (pedido do cliente): corte seco para a cor.
#   take A 4,70-8,53 (ele na churrasqueira) + take B 8,67-17,73 (a camera abre,
#   cestos cheios, ele andando e abrindo os bracos). os quadros da emenda do
#   CapCut (8,53-8,63) ficam de fora: vira um corte seco. fonte 1080p: ate 1,05
cl e1 $P/source/T12.mov 4.70 115 1.00 1.03 0.50 0.40 "$GC"
cl e2 $P/source/T12.mov 8.667 272 1.00 1.05 0.50 0.40 "$GC"
# 4 ultimo quadro do video 1 parado, aproximacao lenta, logo por cima (camada de texto)
$FF -y -loglevel error -sseof -0.04 -i $WK/e2.mov -frames:v 1 -update 1 $WK/last.png
$FF -y -loglevel error -loop 1 -framerate 30 -i $WK/last.png -f lavfi -i anullsrc=r=48000:cl=stereo \
 -filter_complex "[0:v]scale=w='trunc(${W}*(1.00+0.035*t/1.2)/2)*2':h='trunc(${H}*(1.00+0.035*t/1.2)/2)*2':eval=frame:flags=lanczos,crop=${W}:${H},setsar=1,format=yuv420p[v]" \
 -map "[v]" -map 1:a -frames:v 36 -r 30 -c:v libx264 -preset $PRE -crf $CRF -c:a pcm_s16le -t 1.2 $WK/f1.mov
for i in q1 q2 e1 e2 f1; do echo "file '$WK/$i.mov'"; done > $WK/list.txt
$FF -y -hide_banner -loglevel error -f concat -safe 0 -i $WK/list.txt -c:v copy -c:a pcm_s16le $WK/base.mov
echo base ok
