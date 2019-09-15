#!/bin/bash
set -e

rm -f ./output.png ./output*.txt
python3 ./detect.py

[ -f "./output.png" ] || { echo "Output image not produced"; exit -1; }
echo "Detection completed."
