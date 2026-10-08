#!/usr/bin/env bash
# Concatenate rendered segments, add the soundtrack (loudness -14 LUFS), then make
# master.mp4 (high bitrate), final.mp4 (upload quality) and preview.mp4 (< 30 MB).
set -euo pipefail
cd "$(dirname "$0")/build"
printf "file 'segments/%s.mp4'\n" ${SEGMENTS:-v2_a v2_b v2_c v2_d} > concat.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i concat.txt -c copy video.mp4
ffmpeg -y -loglevel error -i video.mp4 -i mix.wav \
  -filter_complex "[1:a]loudnorm=I=-14:TP=-1.0:LRA=11,aresample=48000[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart master.mp4
ffmpeg -y -loglevel error -i master.mp4 -c:v libx264 -preset slow -crf 21 -maxrate 12M -bufsize 24M \
  -profile:v high -pix_fmt yuv420p -c:a copy -movflags +faststart final.mp4
ffmpeg -y -loglevel error -i final.mp4 -c:v libx264 -preset slow -b:v 2700k -pass 1 -an -f null /dev/null
ffmpeg -y -loglevel error -i final.mp4 -c:v libx264 -preset slow -b:v 2700k -pass 2 -c:a aac -b:a 160k -movflags +faststart preview.mp4
rm -f ffmpeg2pass*
ls -la master.mp4 final.mp4 preview.mp4
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate -of compact final.mp4
