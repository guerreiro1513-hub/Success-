#!/bin/bash
# Bastidor Tranquilo — montagem. Poucos cortes, takes longos, som natural.
# Sem legenda: nenhum take tem fala clara (so conversa de fundo).
set -e
FF=/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2
P=/home/user/Success-/projetos/bastidor; WK=$P/work/cut; mkdir -p $WK
W=1080; H=1920; CRF=15; PRE=${PRE:-medium}
# cor de documentario: quente mas real, contraste leve, altas seguradas,
# sem empurrar vermelho/laranja
GD="eq=contrast=1.06:saturation=1.03,colorbalance=rm=0.02:bm=-0.02:rh=0.015:bh=-0.015,\
curves=all='0/0.012 0.25/0.235 0.5/0.51 0.8/0.815 1/0.975',unsharp=5:5:0.30"
cl(){ ID=$1;SRC=$2;SS=$3;NF=$4;Z0=$5;Z1=$6;FX=$7;FY=$8;G=$9
  DU=$(python3 -c "print($NF/30)"); SD=$(python3 -c "print(round($NF/30+0.3,3))")
  E="($Z0+($Z1-$Z0)*t/$DU)"
  # exportacao do CapCut: quadro a quadro, sem reconversao de fps
  case $SRC in *NOVO*) FR="setpts=N/(30*TB)";; *) FR="fps=30";; esac
  $FF -y -ss $SS -t $SD -i "$SRC" -filter_complex \
   "[0:v]scale=${W}*2:${H}*2:force_original_aspect_ratio=increase:flags=lanczos,crop=${W}*2:${H}*2,setsar=1,${FR},\
scale=w='trunc(${W}*${E}/2)*2':h='trunc(${H}*${E}/2)*2':eval=frame:flags=lanczos,\
crop=${W}:${H}:x='(iw-${W})*${FX}':y='(ih-${H})*${FY}',${G},setsar=1,format=yuv420p[v];\
[0:a]aresample=48000,aformat=channel_layouts=stereo[a]" \
   -map "[v]" -map "[a]" -frames:v $NF -r 30 -c:v libx264 -preset $PRE -crf $CRF -c:a pcm_s16le "$WK/$ID.mov" -loglevel error; }

# v2: o bone vira o gancho (pedido do cliente), entra o take novo (embalando para
# os clientes) e o soprador sai.
# 0-5,7 s   IMG_1459: a mao molhando o bone na mangueira (curiosidade), ele poe o
#           bone, olha para a camera e sorri
cl a1 $P/source/IMG_1459.mov 2.30 171 1.00 1.02 0.50 0.45 "$GD"
# 5,7-8,7 s IMG_1455: maos virando a carne na grelha aberta, fumaca
cl a2 $P/source/IMG_1455.mov 0.50 90 1.00 1.03 0.50 0.50 "$GD"
# 8,7-13,2 s take novo (exportacao do CapCut, 1080p): ele embalando a carne para
#           os clientes, gente em volta. o logo do CapCut no fim fica de fora
cl a3 $P/source/NOVO.mov 0.50 135 1.00 1.03 0.50 0.45 "$GD"
# 13,2-16,5 s IMG_1458: a carne. a peca grande saindo da grelha no garfo
cl a4 $P/source/IMG_1458.mov 1.40 100 1.00 1.04 0.50 0.50 "$GD"
# 16,5-18,1 s vinheta da marca, intacta
cl o1 /home/user/Success-/projetos/escala/source/T07.mov 0.00 47 1.00 1.00 0.50 0.50 null
for i in a1 a2 a3 a4 o1; do echo "file '$WK/$i.mov'"; done > $WK/list.txt
$FF -y -hide_banner -loglevel error -f concat -safe 0 -i $WK/list.txt -c:v copy -c:a pcm_s16le $WK/base.mov
echo base ok
