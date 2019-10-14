#!/bin/bash
cd $(dirname $0)
set -e
cd ..

for f in training/logs/*/
do
  echo -e "\nTesting for $(basename $f)\n\n"

  WEIGHTS=$(ls "./$f" | grep .h5)
  WEIGHTS=${f}$WEIGHTS

  for DATASET in datasets/*/
  do
    DATASET=$(basename $DATASET)
    [ $DATASET = "badminton_low" ] && { echo "skipping low before RGB issue is resolved"; continue; }
    [ -d datasets/$DATASET/test ] || { echo "$DATASET not a dataset wtih test"; continue; }
    echo "Running for dataset $DATASET"

    for img in datasets/$DATASET/test/*
    do
      OUTPUT=${f}$(basename $DATASET)/$(basename $img)
      mkdir ${f}$(basename $DATASET) && touch $OUTPUT

      ./detection/detect.sh \
        $(realpath "$WEIGHTS") \
        $(realpath "$img") \
        $(realpath "$OUTPUT")
    done
  done
done
