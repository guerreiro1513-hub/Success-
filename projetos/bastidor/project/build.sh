#!/bin/bash
# Bastidor v4 — montagem no ritmo da musica (trilha A do Kairogen, ~133 BPM,
# batida 0,45 s, primeira batida em 0,03 s). Todo corte cai numa batida.
set -e
FF=/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2
P=/home/user/Success-/projetos/bastidor; WK=$P/work/cut; mkdir -p $WK
W=1080; H=1920; CRF=15; PRE=${PRE:-medium}
# cor (v4, "como se fosse gravado numa camera 4K"): imagem limpa e nitida, sem
# grao e sem vinheta. contraste de camera de cinema com altas suaves (sem pretos
# foscos), cor rica sem exagero, amarelo da guia contido, nitidez adaptativa
GD="eq=contrast=1.08:saturation=1.06:gamma=0.99,\
selectivecolor=yellows=0 0 0.10 -0.06:greens=0.08 0 0.05 0:reds=-0.02 0.03 0.05 0,\
colorbalance=rs=-0.01:bs=0.02:rh=0.025:bh=-0.025,\
curves=all='0/0 0.18/0.155 0.5/0.505 0.82/0.84 1/0.97',\
cas=strength=0.55"
cl(){ ID=$1;SRC=$2;SS=$3;NF=$4;Z0=$5;Z1=$6;FX=$7;FY=$8;G=$9
  DU=$(python3 -c "print($NF/30)"); SD=$(python3 -c "print(round($NF/30+0.3,3))")
  E="($Z0+($Z1-$Z0)*t/$DU)"
  case $SRC in *NOVO*) FR="setpts=N/(30*TB)";; *) FR="fps=30";; esac
  $FF -y -ss $SS -t $SD -i "$SRC" -filter_complex \
   "[0:v]scale=${W}*2:${H}*2:force_original_aspect_ratio=increase:flags=lanczos,crop=${W}*2:${H}*2,setsar=1,${FR},\
scale=w='trunc(${W}*${E}/2)*2':h='trunc(${H}*${E}/2)*2':eval=frame:flags=lanczos,\
crop=${W}:${H}:x='(iw-${W})*${FX}':y='(ih-${H})*${FY}',${G},setsar=1,format=yuv420p[v];\
[0:a]aresample=48000,aformat=channel_layouts=stereo[a]" \
   -map "[v]" -map "[a]" -frames:v $NF -r 30 -c:v libx264 -preset $PRE -crf $CRF -c:a pcm_s16le "$WK/$ID.mov" -loglevel error; }
S=$P/source
# quadros de corte = batidas da trilha (a trilha comeca 0,90 s = 2 batidas
# adiantada, entao a virada continua no take novo):
#   0 | 82 (6 bat) | 109 | 136 | 163 | 190 (virada) | 298 | 325 | 352 | 433 | vinheta 480
# gancho (v4, mais curto): ja entra ele levantando o bone, poe e sorri
cl s01 $S/IMG_1459.mov 4.20  82 1.00 1.05 0.50 0.45 "$GD"
# sequencia de 2 batidas por plano
cl s02 $S/IMG_1455.mov 1.00  27 1.04 1.10 0.50 0.50 "$GD"   # virando a carne
cl s03 $S/IMG_1456.mov 1.40  27 1.10 1.02 0.50 0.50 "$GD"   # potes com a marca
cl s04 $S/IMG_1457.mov 1.00  27 1.02 1.08 0.50 0.45 "$GD"   # carne indo pro saco
cl s05 $S/IMG_1471.mov 0.50  27 1.06 1.00 0.50 0.40 "$GD"   # o soprador
# na virada da musica: ele embalando para os clientes, joinha
cl s06 $S/NOVO.mov     0.50 108 1.00 1.05 0.50 0.45 "$GD"
cl s07 $S/IMG_1470.mov 2.00  27 1.02 1.08 0.50 0.45 "$GD"   # tenda cheia
cl s08 $S/IMG_1466.mov 0.40  27 1.08 1.02 0.50 0.45 "$GD"   # atendimento
# o resultado: a peca saindo da grelha
cl s09 $S/IMG_1458.mov 1.40  81 1.00 1.08 0.50 0.50 "$GD"
# vinheta da marca, intacta
cl s10 /home/user/Success-/projetos/escala/source/T07.mov 0.00 47 1.00 1.00 0.50 0.50 null
for i in s01 s02 s03 s04 s05 s06 s07 s08 s09 s10; do echo "file '$WK/$i.mov'"; done > $WK/list.txt
$FF -y -hide_banner -loglevel error -f concat -safe 0 -i $WK/list.txt -c:v copy -c:a pcm_s16le $WK/base.mov
echo base ok
