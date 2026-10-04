#!/bin/bash
# O Segredo — montagem. Saida 1080x1920, 30 fps, 468 quadros (15,6 s).
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
# cl ID SRC SS NF ZOOM FX FY GRADE MODO   (MODO: n = normal 30p | s = 60p em camera lenta 2x | x = 30p acelerado 1,6x | f = fps=30)
cl(){ ID=$1;SRC=$2;SS=$3;NF=$4;Z=$5;FX=$6;FY=$7;G=$8;M=$9
  case $M in s) FR="setpts=N/(30*TB)"; SD=$(python3 -c "print(round($NF/60+0.3,3))");;
             x) FR="setpts=N/(48*TB),fps=30"; SD=$(python3 -c "print(round($NF*1.6/30+0.3,3))");;
             f) FR="fps=30"; SD=$(python3 -c "print(round($NF/30+0.3,3))");;
             *) FR="setpts=N/(30*TB)"; SD=$(python3 -c "print(round($NF/30+0.3,3))");; esac
  ZW=$(python3 -c "print(int($W*$Z/2)*2)"); ZH=$(python3 -c "print(int($H*$Z/2)*2)")
  $FF -y -ss $SS -t $SD -i "$SRC" -filter_complex \
   "[0:v]${FR},scale=${ZW}:${ZH}:force_original_aspect_ratio=increase:flags=lanczos,\
crop=${W}:${H}:x='(iw-${W})*${FX}':y='(ih-${H})*${FY}',${G},setsar=1,format=yuv420p[v]" \
   -map "[v]" -frames:v $NF -r 30 -c:v libx264 -preset medium -crf $CRF -an "$WK/$ID.mov" -loglevel error; }
# v4: pergunta ("Sabe o que tem no Guerreiro's Grill?", 1440 take 1) e resposta
# ("No Guerreiro's Grill tem carne de qualidade.", 1440 take 2). Comeco editado:
# punch-in seco no dedo chamando e a chegada da camera acelerada.
cl a1 $S/IMG_1440.mov     0.00 15 1.00 0.50 0.50 "$NAT" n
cl a2 $S/IMG_1440.mov     0.50 15 1.22 0.50 0.32 "$NAT" n
cl a3 $S/IMG_1440.mov     1.00 15 1.00 0.50 0.50 "$NAT" x
cl a4 $S/IMG_1440.mov     1.80 49 1.00 0.50 0.50 "$NAT" n
cl a5 $S/IMG_1440.mov     5.25 47 1.00 0.50 0.50 "$NAT" n
cl a6 $S/IMG_1440.mov     6.80 37 1.00 0.50 0.50 "$NAT" n
# the making (8 planos, ~8 s), entra com o impacto da musica
cl m1 $S/COMIDA_NOITE.mov 11.10 30 1.00 0.50 0.50 "$CINN" s
cl m2 $S/COMIDA_NOITE.mov  1.20 30 1.00 0.50 0.50 "$CINN" s
cl m3 $S/COMIDA_DIA.mov    3.20 30 1.00 0.50 0.50 "$CIN" f
cl m4 $S/COMIDA_DIA.mov    8.50 33 1.00 0.50 0.50 "$CIN" f
cl m5 $S/COMIDA_DIA.mov    5.60 30 1.00 0.50 0.50 "$CIN" f
cl m6 $S/COMIDA_NOITE.mov  8.50 30 1.00 0.50 0.50 "$CINN" s
cl m7 $S/COMIDA_NOITE.mov 12.30 30 1.00 0.50 0.50 "$CINN" f
cl m8 $S/COMIDA_NOITE.mov 13.37 30 1.00 0.50 0.50 "$CINN" f
cl s8 /home/user/Success-/projetos/escala/source/T07.mov 0.00 47 1.00 0.50 0.50 null n
for i in a1 a2 a3 a4 a5 a6 m1 m2 m3 m4 m5 m6 m7 m8 s8; do echo "file '$WK/$i.mov'"; done > $WK/list.txt
$FF -y -hide_banner -loglevel error -f concat -safe 0 -i $WK/list.txt -c:v copy $WK/base.mov
echo base ok
