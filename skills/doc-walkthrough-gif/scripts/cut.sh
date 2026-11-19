#!/bin/zsh
# Plain cut (no overlays): retimed segments + optional privacy blur -> lossless ffv1 -> GIF + MP4.
# Usage: cut.sh SRC.mov WORK_DIR OUT_BASENAME "a b speed  a b speed ..." [BLUR "w:h:x:y:t0:t1"]
#   Times are source pts seconds; BLUR coords are source px, t0/t1 source seconds.
# Writes OUT_BASENAME.gif / .mp4; refuses to overwrite.
set -e
SRC=$1; W=$2; OUT=$3; SEGS=(${=4}); BLUR=$5
[[ -e $OUT.gif || -e $OUT.mp4 ]] && { echo "exists: $OUT.gif/.mp4"; exit 1; }
n=$(( ${#SEGS} / 3 ))
if [[ -n $BLUR ]]; then
  IFS=: read bw bh bx by bt0 bt1 <<< "$BLUR"
  FC="[0:v]split[base][c];[c]crop=${bw}:${bh}:${bx}:${by},boxblur=25:3[bl];[base][bl]overlay=${bx}:${by}:enable='between(t,${bt0},${bt1})',split=${n}"
else
  FC="[0:v]split=${n}"
fi
for i in $(seq 1 $n); do FC+="[s$i]"; done; FC+=";"
CAT=""
for i in $(seq 1 $n); do
  a=${SEGS[$(( (i-1)*3+1 ))]}; b=${SEGS[$(( (i-1)*3+2 ))]}; s=${SEGS[$(( (i-1)*3+3 ))]}
  FC+="[s${i}]trim=start=${a}:end=${b},setpts=(PTS-STARTPTS)/${s},fps=12[v${i}];"; CAT+="[v$i]"
done
FC+="${CAT}concat=n=${n}:v=1:a=0,scale=1300:-2:flags=lanczos,tpad=stop_mode=clone:stop_duration=2.5,fps=12[out]"
mkdir -p $W
ffmpeg -y -v error -i "$SRC" -filter_complex "$FC" -map "[out]" -an -c:v ffv1 -level 3 -pix_fmt yuv444p $W/cut.mkv
rm -rf $W/frames && mkdir $W/frames
ffmpeg -v error -i $W/cut.mkv -pix_fmt rgb24 $W/frames/f%05d.png
gifski --fps 12 --width 1300 --quality 90 -o $OUT.gif $W/frames/f*.png
ffmpeg -v error -framerate 12 -i $W/frames/f%05d.png -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -movflags +faststart $OUT.mp4
rm -rf $W/frames
du -sh $W
for f in $OUT.gif $OUT.mp4; do ffprobe -v error -show_entries stream=width,height:format=duration,size -of compact "$f"; done
