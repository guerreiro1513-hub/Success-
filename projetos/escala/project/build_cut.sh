set -e
FF=/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2
P=/home/user/Success-/projetos/escala
W=${W:-1080}; H=${H:-1920}; CRF=${CRF:-15}; PRE=${PRE:-slow}; OUTD=${OUTD:-cut}
SC="selectivecolor=reds=-0.10 0.06 0.15:yellows=-0.07 0.03 0.12"
CV="curves=all='0/0 0.25/0.21 0.5/0.52 0.75/0.82 1/1'"
# GA: closes. ja sao nitidos (70 e 59 de nitidez medida), pede pouca faca
GA="eq=contrast=1.14:saturation=1.04,vibrance=intensity=0.22,${SC},${CV},unsharp=5:5:0.55"
# GB: o aberto. medi 45 de nitidez e calor -17, o mais mole e o mais frio do lote.
#     leva mais faca e um empurrao de quente, senao o reveal cai de qualidade
GB="eq=contrast=1.16:saturation=1.09,vibrance=intensity=0.30,\
colorbalance=rm=0.05:gm=0.01:bm=-0.04:rh=0.03:bh=-0.03,${SC},${CV},unsharp=7:7:0.95"
# GC: o pai. saturacao contida pra pele nao virar laranja
GC="eq=contrast=1.12:saturation=1.00,vibrance=intensity=0.16,${SC},${CV},unsharp=5:5:0.50"
cl(){ ID=$1;SRC=$2;SS=$3;NF=$4;Z0=$5;Z1=$6;FY=$7;GK=$8
  DU=$(python3 -c "print($NF/30)"); SD=$(python3 -c "print(round($NF/30+0.3,3))")
  E="($Z0+($Z1-$Z0)*t/$DU)"
  case $GK in GA) G="$GA";; GB) G="$GB";; GC) G="$GC";; esac
  $FF -y -ss $SS -t $SD -i "$SRC" -filter_complex \
   "[0:v]scale=${W}:${H}:force_original_aspect_ratio=increase:flags=lanczos,crop=${W}:${H},setsar=1,fps=30,\
scale=w='trunc(${W}*${E}/2)*2':h='trunc(${H}*${E}/2)*2':eval=frame:flags=bicubic,\
crop=${W}:${H}:x='(iw-${W})/2':y='(ih-${H})*${FY}',${G},setsar=1,format=yuv420p[v];\
[0:a]aresample=48000,aformat=channel_layouts=stereo[a]" \
   -map "[v]" -map "[a]" -frames:v $NF -r 30 -c:v libx264 -preset $PRE -crf $CRF -c:a pcm_s16le "$OUTD/$ID.mov" -loglevel error; }

cl h1 $P/source/T04.mov 1.00 45 1.02 1.12 0.50 GA
cl h2 $P/source/T03.mov 3.40 40 1.12 1.02 0.50 GA
cl h3 $P/source/T02.mov 0.20 35 1.02 1.11 0.50 GA
cl h4 $P/source/T03.mov 2.20 25 1.11 1.02 0.50 GA
cl h5 $P/source/T04.mov 1.85 20 1.10 1.22 0.50 GA
cl h6 $P/source/T02.mov 1.45 15 1.16 1.30 0.50 GA
cl r1 $P/source/T01.mov 0.30 120 1.62 1.26 0.92 GB
cl s1 $P/source/T01.mov 4.60 60 1.20 1.34 0.92 GB
cl s2 $P/source/T04.mov 1.20 20 1.06 1.16 0.50 GA
cl s3 $P/source/T01.mov 6.70 40 1.45 1.30 0.86 GB
cl s4 $P/source/T03.mov 0.30 20 1.04 1.12 0.50 GA
cl s5 $P/source/T01.mov 8.10 40 1.28 1.44 0.94 GB
cl b1 $P/source/T05.mov 2.40 80 1.00 1.05 0.50 GC
# fecho: quadro congelado no pico de nitidez do T01 (9,55 s)
$FF -y -hide_banner -loglevel error -ss 9.55 -i $P/source/T01.mov \
  -vf "scale=${W}:${H}:force_original_aspect_ratio=increase:flags=lanczos,crop=${W}:${H},setsar=1,\
scale=w='trunc(${W}*1.22/2)*2':h='trunc(${H}*1.22/2)*2':flags=lanczos,crop=${W}:${H}:x='(iw-${W})/2':y='(ih-${H})*0.88'" \
  -frames:v 1 $OUTD/endbg.png
$FF -y -hide_banner -loglevel error -loop 1 -framerate 30 -i $OUTD/endbg.png -f lavfi -i anullsrc=r=48000:cl=stereo \
 -filter_complex "[0:v]scale=w='trunc(${W}*(1.00+0.04*t/2.667)/2)*2':h='trunc(${H}*(1.00+0.04*t/2.667)/2)*2':eval=frame:flags=bicubic,crop=${W}:${H},${GB},setsar=1,format=yuv420p[v]" \
 -map "[v]" -map 1:a -frames:v 80 -r 30 -c:v libx264 -preset $PRE -crf $CRF -c:a pcm_s16le -t 2.667 $OUTD/b2.mov
for i in h1 h2 h3 h4 h5 h6 r1 s1 s2 s3 s4 s5 b1 b2; do echo "file '$PWD/$OUTD/$i.mov'"; done > $OUTD/list.txt
$FF -y -hide_banner -loglevel error -f concat -safe 0 -i $OUTD/list.txt -c:v copy -c:a pcm_s16le $OUTD/base.mov
