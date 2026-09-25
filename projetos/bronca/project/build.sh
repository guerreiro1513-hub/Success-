#!/bin/bash
# Bronca Fake — montagem. Sem legenda (o cliente coloca depois).
# Preto e branco na bronca; a cor volta no sorriso; trilha so na carne.
set -e
FF=/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2
P=/home/user/Success-/projetos/bronca; WK=$P/work/cut; mkdir -p $WK
W=1080; H=1920; CRF=15; PRE=${PRE:-medium}
CV="curves=all='0/0.01 0.22/0.19 0.5/0.52 0.78/0.83 0.94/0.945 1/0.975'"
# pele natural; o preto e branco sai daqui com hue s=0
GC="eq=contrast=1.08:saturation=1.02,vibrance=intensity=0.16,${CV},unsharp=5:5:0.35"
# carne: textura e brilho natural, sem empurrar o laranja
GM="eq=contrast=1.08:saturation=1.03,vibrance=intensity=0.14,${CV},unsharp=5:5:0.40"
# preto e branco com corpo: contraste um pouco maior, altas seguradas
BW="hue=s=0,eq=contrast=1.14:brightness=-0.01,curves=all='0/0.02 0.25/0.21 0.5/0.52 0.8/0.84 1/0.97',unsharp=5:5:0.35"
cl(){ ID=$1;SRC=$2;SS=$3;NF=$4;Z0=$5;Z1=$6;FX=$7;FY=$8;G=$9
  DU=$(python3 -c "print($NF/30)"); SD=$(python3 -c "print(round($NF/30+0.3,3))")
  E="($Z0+($Z1-$Z0)*t/$DU)"
  case $SRC in *T12*) FR="setpts=N/(30*TB)";; *) FR="fps=30";; esac
  $FF -y -ss $SS -t $SD -i "$SRC" -filter_complex \
   "[0:v]scale=${W}*2:${H}*2:force_original_aspect_ratio=increase:flags=lanczos,crop=${W}*2:${H}*2,setsar=1,${FR},\
scale=w='trunc(${W}*${E}/2)*2':h='trunc(${H}*${E}/2)*2':eval=frame:flags=lanczos,\
crop=${W}:${H}:x='(iw-${W})*${FX}':y='(ih-${H})*${FY}',${G},setsar=1,format=yuv420p[v];\
[0:a]aresample=48000,aformat=channel_layouts=stereo[a]" \
   -map "[v]" -map "[a]" -frames:v $NF -r 30 -c:v libx264 -preset $PRE -crf $CRF -c:a pcm_s16le "$WK/$ID.mov" -loglevel error; }

# 1 a bronca (video 1, take A): 0,95 a 8,35. duas frases, 1,6 s calado virando a
#   carne, uma palavra final. o video 1 e 1080p: aproximacao no maximo 1,07
cl b1 $P/source/T12.mov 0.95 222 1.00 1.07 0.50 0.30 "$BW"
# 2 a quebra (IMG_1442, 4K): 0,90 a 3,60. calado e serio, levanta os olhos em ~1,7,
#   sorri em ~2,3. a cor volta no sorriso (quadro 38 do clipe) em 4 quadros
cl q1 $P/source/T13.mov 0.90 81 1.08 1.16 0.55 0.32 \
  "${GC},hue=s='if(lt(t,1.27),0,min(1,(t-1.27)/0.13))'"
# 3 a carne (IMG_1452, grade com ceu e fumaca). a trilha entra aqui
cl m1 $P/source/T09.mov 3.30 63 1.02 1.09 0.50 0.50 "$GM"
# 4 vinheta da marca, intacta
cl o1 $P/source/T07.mov 0.00 47 1.00 1.00 0.50 0.50 null
for i in b1 q1 m1 o1; do echo "file '$WK/$i.mov'"; done > $WK/list.txt
$FF -y -hide_banner -loglevel error -f concat -safe 0 -i $WK/list.txt -c:v copy -c:a pcm_s16le $WK/base.mov
echo base ok
