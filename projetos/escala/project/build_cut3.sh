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
  case $GK in GN) G="$GN";; GA) G="$GA";; GB) G="$GB";; GC) G="$GC";; esac
  $FF -y -ss $SS -t $SD -i "$SRC" -filter_complex \
   "[0:v]scale=${W}*2:${H}*2:force_original_aspect_ratio=increase:flags=lanczos,crop=${W}*2:${H}*2,setsar=1,fps=30,\
scale=w='trunc(${W}*${E}/2)*2':h='trunc(${H}*${E}/2)*2':eval=frame:flags=lanczos,\
crop=${W}:${H}:x='(iw-${W})*${FX}':y='(ih-${H})*${FY}',${G},setsar=1,format=yuv420p[v];\
[0:a]aresample=48000,aformat=channel_layouts=stereo[a]" \
   -map "[v]" -map "[a]" -frames:v $NF -r 30 -c:v libx264 -preset $PRE -crf $CRF -c:a pcm_s16le "$OUTD/$ID.mov" -loglevel error; }

# fala inteira: 2,30 a 10,30 do take. a primeira silaba cai em 2,48
cl p1 $P/source/T05.mov 2.30 240 1.00 1.06 0.50 0.50 GC
# gancho intacto da v2, grade nova. tempos e meios tempos de 90 BPM (20 quadros)
cl c1 $P/source/T04.mov 1.00  40 1.02 1.12 0.50 0.50 GA
cl c2 $P/source/T03.mov 3.40  30 1.12 1.02 0.50 0.50 GA
cl c3 $P/source/T02.mov 0.20  20 1.02 1.11 0.50 0.50 GA
cl c4 $P/source/T03.mov 2.20  20 1.11 1.02 0.50 0.50 GA
cl c5 $P/source/T04.mov 1.85  10 1.10 1.20 0.50 0.50 GA
cl c6 $P/source/T02.mov 1.45  10 1.18 1.32 0.50 0.50 GA
# reveal: mesmo punch-out da v2
cl r1 $P/source/T01.mov 0.30 100 1.62 1.26 0.50 0.92 GB
# final novo. v2 voltava 4 vezes ao mesmo travelling; aqui entra um recorte
# apertado da operacao (fumaca, gente trabalhando), informacao que o aberto nao da
cl d1 $P/source/T01.mov 6.30  40 1.80 1.68 0.56 0.60 GB
# variedade: o que tem dentro das outras churrasqueiras (T06, 1080p nativo,
# zoom baixo para nao ampliar pixel). frango, costela na fumaca, carne em bloco
cl n1 $P/source/T06.mov 2.80  20 1.00 1.06 0.50 0.50 GN
cl n2 $P/source/T06.mov 7.10  20 1.06 1.00 0.50 0.50 GN
cl n3 $P/source/T06.mov 11.30 30 1.00 1.08 0.50 0.50 GN
# fecho em movimento, nao congelado
cl e1 $P/source/T01.mov 7.60  60 1.24 1.30 0.50 0.88 GB
for i in p1 c1 c2 c3 c4 c5 c6 r1 d1 n1 n2 n3 e1; do echo "file '$OUTD/$i.mov'"; done > $OUTD/list.txt
$FF -y -hide_banner -loglevel error -f concat -safe 0 -i $OUTD/list.txt -c:v copy -c:a pcm_s16le $OUTD/base.mov
echo base ok
