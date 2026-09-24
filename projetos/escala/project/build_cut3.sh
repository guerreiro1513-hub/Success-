#!/bin/bash
# Versao 3 — passe de refinamento sobre o corte PAI-22s.
# Mesma montagem ate o reveal; fala aparada no respiro inicial; final sem as
# passadas repetidas pela fileira; grades revisadas (mais cor, menos nitidez).
set -e
FF=/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2
P=/home/user/Success-/projetos/escala
W=${W:-1080}; H=${H:-1920}; CRF=${CRF:-15}; PRE=${PRE:-slow}; OUTD=${OUTD:-$P/work/cut3}
mkdir -p $OUTD
SC="selectivecolor=reds=-0.08 0.07 0.16:yellows=-0.06 0.04 0.12"
# curva em S mais suave que a da v2: nao esmaga a sombra da grelha, segura o alto da brasa
CV="curves=all='0/0.012 0.22/0.19 0.5/0.52 0.78/0.83 0.94/0.945 1/0.975'"
# GA closes de carne: mais vibrance, nitidez contida
GA="eq=contrast=1.10:saturation=1.07,vibrance=intensity=0.28,${SC},${CV},unsharp=5:5:0.42"
# GB o aberto: T01 e mais fria e mole. v2 usava unsharp 0.95, que serrilhava as bordas
GB="eq=contrast=1.13:saturation=1.10,vibrance=intensity=0.32,\
colorbalance=rm=0.05:gm=0.01:bm=-0.04:rh=0.03:bh=-0.03,${SC},${CV},unsharp=7:7:0.62"
# GC o pai: pele primeiro, vibrance so levanta o que esta lavado
GC="eq=contrast=1.09:saturation=1.02,vibrance=intensity=0.20,\
colorbalance=rs=0.01:bs=-0.01,${SC},${CV},unsharp=5:5:0.40"
# GN o video novo (T06): ja vem tratado pelo celular. grade leve, sem
# selectivecolor, senao o frango vira laranja
GN="eq=contrast=1.05:saturation=0.94,vibrance=intensity=0.06,\
colorbalance=rh=-0.02:bh=0.01,${CV},unsharp=5:5:0.30"
cl(){ ID=$1;SRC=$2;SS=$3;NF=$4;Z0=$5;Z1=$6;FX=$7;FY=$8;GK=$9
  DU=$(python3 -c "print($NF/30)"); SD=$(python3 -c "print(round($NF/30+0.3,3))")
  E="($Z0+($Z1-$Z0)*t/$DU)"
  case $GK in NO) G="null";; GN) G="$GN";; GA) G="$GA";; GB) G="$GB";; GC) G="$GC";; esac
  $FF -y -ss $SS -t $SD -i "$SRC" -filter_complex \
   "[0:v]scale=${W}*2:${H}*2:force_original_aspect_ratio=increase:flags=lanczos,crop=${W}*2:${H}*2,setsar=1,fps=30,\
scale=w='trunc(${W}*${E}/2)*2':h='trunc(${H}*${E}/2)*2':eval=frame:flags=lanczos,\
crop=${W}:${H}:x='(iw-${W})*${FX}':y='(ih-${H})*${FY}',${G},setsar=1,format=yuv420p[v];\
[0:a]aresample=48000,aformat=channel_layouts=stereo[a]" \
   -map "[v]" -map "[a]" -frames:v $NF -r 30 -c:v libx264 -preset $PRE -crf $CRF -c:a pcm_s16le "$OUTD/$ID.mov" -loglevel error; }

# abertura na churrasqueira: o take comeca 1,6 s em cima da costela e vira
# para o pai. fala inteira, 0,00 a 10,30. a primeira silaba cai em 2,48
cl p1 $P/source/T05.mov 0.00 309 1.00 1.05 0.50 0.50 GC
# gancho: uma churrasqueira por corte, nenhuma volta. 40, 30, 40, 20 quadros
# (T02 saiu: e a mesma churrasqueira do T03. costela do T06 saiu: repete a da abertura)
cl c1 $P/source/T04.mov 1.00  40 1.02 1.12 0.50 0.50 GA
cl c2 $P/source/T03.mov 3.30  30 1.12 1.03 0.50 0.50 GA
cl c3 $P/source/T06.mov 2.60  40 1.00 1.08 0.50 0.50 GN
cl c4 $P/source/T06.mov 11.30 20 1.03 1.10 0.50 0.50 GN
# reveal: mesmo punch-out da v2
cl r1 $P/source/T01.mov 0.30 100 1.62 1.26 0.50 0.92 GB
# a operacao: banner, fumaca, gente trabalhando. nenhuma carne repetida
cl d1 $P/source/T01.mov 6.30  40 1.80 1.68 0.56 0.60 GB
# fecho: a vinheta da marca (T07), intacta, sem grade nem zoom
cl o1 $P/source/T07.mov 0.00  47 1.00 1.00 0.50 0.50 NO
for i in p1 c1 c2 c3 c4 r1 d1 o1; do echo "file '$OUTD/$i.mov'"; done > $OUTD/list.txt
$FF -y -hide_banner -loglevel error -f concat -safe 0 -i $OUTD/list.txt -c:v copy -c:a pcm_s16le $OUTD/base.mov
echo base ok
