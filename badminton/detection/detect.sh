#!/bin/bash
set -e
cd $(dirname $0)

( [ "$1" = "" ] || [ "$2" = "" ] || [ "$3" = "" ] || [ "$4" = "" ] ) && { 
  echo "Usage: ./detect.sh path/weights.h5 mask_size=28/56/.. path/input.jpg path/output.png"
  exit 1
}

[ -f "$1" ] || { echo "Weights not found"; exit -1; }
[ -f "$3" ] || { echo "Input image not found"; exit -1; }

rm -f "$4"
python3 ./detect.py \
  --weights=$1 \
  --mask_size=$2 \
  --input=$3 \
  --output=$4 \

[ -f "$4" ] || { echo "Output image not produced"; exit -1; }
echo "Detection completed."
