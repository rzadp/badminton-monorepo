#!/bin/bash
set -e
cd $(dirname $0)

( [ "$1" = "" ] || [ "$2" = "" ] || [ "$3" = "" ] || [ "$4" = "" ] || [ "$5" = "" ] ) && {
  echo "Usage: ./detect.sh path/weights.h5 mask_size=28/56/.. dataset path/output split_val"
  exit 1
}

[ -f "$1" ] || { echo "Weights not found: $1"; exit -1; }

rm -rf "$4"
mkdir -p "$4"
python3 -u ./validate.py \
  --WEIGHTS=$1 \
  --MASK_SIZE=$2 \
  --DATASET=$3 \
  --OUTPUT_PATH=$4 \
  --CI=$CI
  --SPLIT_VAL=$5

echo "Validation completed."
