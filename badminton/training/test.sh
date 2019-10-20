#!/bin/bash
cd $(dirname $0)
set -e
cd ..

for f in training/logs/*/
do
  echo -e "\nTesting for $(basename $f)\n\n"
  
  source ${f}$(ls "./$f" | grep .env)
  WEIGHTS=$(ls "./$f" | grep .h5)
  WEIGHTS=${f}$WEIGHTS
  echo "Mask size is $MASK_SIZE"

  for DATASET in datasets/*/
  do
    DATASET=$(basename $DATASET)
    [ $DATASET = "badminton_low" ] && { echo "skipping low before RGB issue is resolved"; continue; }
    [ -d datasets/$DATASET/test ] || { echo "$DATASET not a dataset wtih test"; continue; }
    echo "Running for dataset $DATASET"
    echo "weights are $WEIGHTS"

    for img in datasets/$DATASET/test/*
    do
      OUTPUT=${f}$(basename $DATASET)/$(basename $img)
      mkdir ${f}$(basename $DATASET) && touch $OUTPUT

      ./detection/detect.sh \
        $(realpath "$WEIGHTS") \
        $MASK_SIZE \
        $(realpath "$img") \
        $(realpath "$OUTPUT")
    done
  done
done
