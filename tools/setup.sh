#!/usr/bin/env bash
# Prepara el entorno de la nube: ffmpeg, Python y Node para HyperFrames.
set -e
if ! command -v ffmpeg >/dev/null; then
  (sudo apt-get update -y && sudo apt-get install -y ffmpeg) || (apt-get update -y && apt-get install -y ffmpeg)
fi
python3 -m pip install --quiet numpy scipy soundfile
node --version
npx --yes hyperframes@0.8.186 --version || true
ffmpeg -version | head -1
