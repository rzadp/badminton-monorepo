#!/bin/bash
cd $(dirname $0)
set -e
cd ..

for f in training/logs/*/
do
  source ${f}$(ls "./$f" | grep .env)
  WEIGHTS=$(ls "./$f" | grep best.h5)
  WEIGHTS=${f}$WEIGHTS
  echo -e "\n\n ...::: Testing for $(basename $f), mask size is ${MASK_SIZE} :::..."
  echo -e "weights are ${WEIGHTS}\n\n"

  for DS in datasets/*/
  do
    DS=$(basename $DS)
    [ -d datasets/$DS/test ] || { echo "$DS not a dataset wtih test"; continue; }
    echo -e "\n\nRunning for dataset ${DS}\n\n"

    for img in datasets/$DS/test/*.jpg
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
