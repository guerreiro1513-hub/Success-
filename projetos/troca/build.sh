#!/bin/bash
# Refaz o Reel inteiro. Coloque fachada.mov nesta pasta e rode de novo: ./build.sh
set -e
cd "$(dirname "$0")"
mkdir -p work
python3 build.py
