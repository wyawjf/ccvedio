#!/usr/bin/env bash
# Splice re-rendered patch ranges into the v2 render, frame-accurately, into segments/v2_all.mp4.
# c covers frames 1050-1679, d covers 1680-2333.
#   life patch  frames 1182-1272 (p_1a, p_1b) -> replaces c[132:223]
#   dream patch frames 1530-1692 (p_2a..p_2c) -> replaces c[480:630] + d[0:13]
set -euo pipefail
cd "$(dirname "$0")/build/segments"
ffmpeg -y -loglevel error -i v2_a.mp4 -i v2_b.mp4 -i v2_c.mp4 -i v2_d.mp4 -i p_1a.mp4 -i p_1b.mp4 -i p_2a.mp4 -i p_2b.mp4 -i p_2c.mp4 \
  -filter_complex "\
[0:v]setpts=PTS-STARTPTS[a];[1:v]setpts=PTS-STARTPTS[b];\
[2:v]split[cx][cy];[cx]trim=start_frame=0:end_frame=132,setpts=PTS-STARTPTS[c1];[cy]trim=start_frame=223:end_frame=480,setpts=PTS-STARTPTS[c2];\
[3:v]trim=start_frame=13,setpts=PTS-STARTPTS[d1];\
[4:v]setpts=PTS-STARTPTS[p1];[5:v]setpts=PTS-STARTPTS[p2];[6:v]setpts=PTS-STARTPTS[p3];[7:v]setpts=PTS-STARTPTS[p4];[8:v]setpts=PTS-STARTPTS[p5];\
[a][b][c1][p1][p2][c2][p3][p4][p5][d1]concat=n=10:v=1:a=0[out]" \
  -map "[out]" -c:v libx264 -preset slow -crf 14 -pix_fmt yuv420p -r 30 v2_all.mp4
ffprobe -v error -count_frames -select_streams v -show_entries stream=nb_read_frames -of csv=p=0 v2_all.mp4
