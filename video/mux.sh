#!/usr/bin/env bash
# Concatenate rendered segments, add the mixed audio, normalize loudness to -14 LUFS.
set -euo pipefail
cd "$(dirname "$0")/build"
printf "file 'segments/%s.mp4'\n" a b c > concat.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i concat.txt -c copy video.mp4
ffmpeg -y -loglevel error -i video.mp4 -i mix.wav \
  -filter_complex "[1:a]loudnorm=I=-14:TP=-1.0:LRA=11,aresample=48000[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart final.mp4
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate -of compact final.mp4
