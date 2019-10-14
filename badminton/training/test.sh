#!/bin/bash
cd $(dirname $0)
set -e
cd ..

for f in training/logs/*/
do
  echo -e "\nTesting for $(basename $f)\n\n"

  LOG_FOLDER=$(basename "$f" .env)
  WEIGHTS=$(ls "./$f" | grep .h5)
  WEIGHTS=${f}$WEIGHTS
  DATASET=$(echo $(basename "$f") | cut -f 1-2 -d "_")

  for img in datasets/$DATASET/test/*
  do
    echo "running for $img"
    OUTPUT=${f}$(basename $img)
    ./detection/detect.sh \
      $(realpath "$WEIGHTS") \
      $(realpath "$img") \
      $(realpath "$OUTPUT")
  done
done
