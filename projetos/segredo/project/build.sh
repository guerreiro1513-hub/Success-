#!/bin/bash
# O Segredo — montagem. Saida 1080x1920, 30 fps, 307 quadros (10,23 s).
# Sem zoom animado (enquadramento fixo por plano, o "punch-in" e um corte seco).
set -e
FF=/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2
P=/home/user/Success-/projetos/segredo; S=$P/source; WK=$P/work/cut; mkdir -p $WK
W=1080; H=1920; CRF=15
# cor natural para o pai: pele real, contraste equilibrado, sem laranja
NAT="eq=contrast=1.05:saturation=1.03:gamma=1.0,\
colorbalance=rs=-0.01:bs=0.015:rh=0.015:bh=-0.015,\
curves=all='0/0 0.2/0.185 0.5/0.505 0.85/0.86 1/0.98',cas=strength=0.3"
# "the making": cinema escuro, sombras fundas, fogo quente, vinheta
CIN="eq=contrast=1.14:saturation=1.06:gamma=0.93,\
colorbalance=rs=-0.03:bs=0.04:rm=0.02:bm=-0.02:rh=0.05:gh=0.015:bh=-0.05:pl=1,\
curves=all='0/0 0.15/0.08 0.5/0.47 0.85/0.88 1/0.97',vignette=angle=PI/5,cas=strength=0.45"
# noite: mesmo look, sem escurecer mais (a fonte ja e escura)
CINN="eq=contrast=1.08:saturation=1.06:gamma=1.04,\
colorbalance=rs=-0.03:bs=0.04:rm=0.02:bm=-0.02:rh=0.05:gh=0.015:bh=-0.05:pl=1,\
curves=all='0/0 0.12/0.08 0.5/0.52 0.85/0.9 1/0.98',vignette=angle=PI/6,cas=strength=0.5"
# cl ID SRC SS NF ZOOM FX FY GRADE MODO   (MODO: n = normal 30p | s = 60p em camera lenta 2x | f = fps=30)
cl(){ ID=$1;SRC=$2;SS=$3;NF=$4;Z=$5;FX=$6;FY=$7;G=$8;M=$9
  case $M in s) FR="setpts=N/(30*TB)"; SD=$(python3 -c "print(round($NF/60+0.3,3))");;
             f) FR="fps=30"; SD=$(python3 -c "print(round($NF/30+0.3,3))");;
             *) FR="setpts=N/(30*TB)"; SD=$(python3 -c "print(round($NF/30+0.3,3))");; esac
  ZW=$(python3 -c "print(int($W*$Z/2)*2)"); ZH=$(python3 -c "print(int($H*$Z/2)*2)")
  $FF -y -ss $SS -t $SD -i "$SRC" -filter_complex \
   "[0:v]${FR},scale=${ZW}:${ZH}:force_original_aspect_ratio=increase:flags=lanczos,\
crop=${W}:${H}:x='(iw-${W})*${FX}':y='(ih-${H})*${FY}',${G},setsar=1,format=yuv420p[v]" \
   -map "[v]" -frames:v $NF -r 30 -c:v libx264 -preset medium -crf $CRF -an "$WK/$ID.mov" -loglevel error; }
# v3: um plano so do 1440 do inicio: ele chama, a camera vai em direcao a ele e ele
# cochicha colado na lente (take 1, fala 1,85-3,35). Depois a risada com joinha.
cl s1 $S/IMG_1440.mov     0.00 104 1.00 0.50 0.50 "$NAT" n
cl s2 $S/IMG_1440.mov     6.95 33 1.00 0.50 0.50 "$NAT" n
# 4) the making: faca na carne crua (noite, 60p -> camera lenta 2x)
cl s4 $S/COMIDA_NOITE.mov 1.84 30 1.00 0.50 0.50 "$CINN" s
# 5) carne levantada no garfo (dia, ja vem em camera lenta)
cl s5 $S/COMIDA_DIA.mov   8.50 33 1.00 0.50 0.50 "$CIN" f
# 6) fatiando a costela (noite, camera lenta 2x)
cl s6 $S/COMIDA_NOITE.mov  8.50 30 1.00 0.50 0.50 "$CINN" s
# 7) fogo na grelha (noite, camera lenta 2x)
cl s7 $S/COMIDA_NOITE.mov 11.10 30 1.00 0.50 0.50 "$CINN" s
# 8) vinheta da marca, intacta
cl s8 /home/user/Success-/projetos/escala/source/T07.mov 0.00 47 1.00 0.50 0.50 null n
for i in s1 s2 s4 s5 s6 s7 s8; do echo "file '$WK/$i.mov'"; done > $WK/list.txt
$FF -y -hide_banner -loglevel error -f concat -safe 0 -i $WK/list.txt -c:v copy $WK/base.mov
echo base ok
