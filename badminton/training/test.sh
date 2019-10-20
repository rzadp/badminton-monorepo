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

  for DS in datasets/*/
  do
    DS=$(basename $DS)
    [ -d datasets/$DS/test ] || { echo "$DS not a dataset wtih test"; continue; }
    echo "Running for dataset $DS"
    echo "weights are $WEIGHTS"

    for img in datasets/$DS/test/*
    do
      OUTPUT=${f}$(basename $DS)/$(basename $img)
      mkdir ${f}$(basename $DS) && touch $OUTPUT

      ./detection/detect.sh \
        $(realpath "$WEIGHTS") \
        $MASK_SIZE \
        $(realpath "$img") \
        $(realpath "$OUTPUT")
    done
  done
done
