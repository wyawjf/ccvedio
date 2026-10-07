#!/usr/bin/env bash
# Pull frames from the finished video at the given times and tile them for a visual check.
set -euo pipefail
cd "$(dirname "$0")/build"
mkdir -p qc && rm -f qc/*.png
for t in "$@"; do ffmpeg -loglevel error -y -ss "$t" -i final.mp4 -frames:v 1 "qc/f$(printf '%06.2f' "$t").png"; done
python3 ../sheet.py qc/sheet.jpg qc/f*.png
echo qc/sheet.jpg
