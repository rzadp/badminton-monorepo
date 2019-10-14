#!/bin/bash
set -e
cd $(dirname $0)

( [ "$1" = "" ] || [ "$2" = "" ] || [ "$3" = "" ] ) && { 
  echo "Usage: ./detect.sh path/weights.h5 path/input.jpg path/output.png"
  exit 1
}

[ -f "$1" ] || { echo "Weights not found"; exit -1; }
[ -f "$2" ] || { echo "Input image not found"; exit -1; }

rm -f "$3"
python3 ./detect.py \
  --weights=$1 \
  --input=$2 \
  --output=$3 \

[ -f "$3" ] || { echo "Output image not produced"; exit -1; }
echo "Detection completed."
