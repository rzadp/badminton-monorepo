#!/bin/bash
cd $(dirname $0)
set -e
cd ..
export CI=$CI

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
    [ "$DS" = "badminton_high" ] && { echo "Skipping $DS"; continue; }
    echo -e "\n\nRunning for dataset ${DS}\n\n"

    for img in datasets/$DS/test/*.jpg
    do
      OUTPUT_DETECTION=${f}$(basename $DS)/test/$(basename $img)
      mkdir -p ${f}$(basename $DS)/test && touch $OUTPUT_DETECTION
      ./detection/detect.sh \
        $(realpath "$WEIGHTS") \
        $MASK_SIZE \
        $(realpath "$img") \
        $(realpath "$OUTPUT_DETECTION")
      [ -n "$CI" ] && break
    done

    OUTPUT_VALIDATION=${f}$(basename $DS)/validation
    mkdir -p "$OUTPUT_VALIDATION"
    ./detection/validate.sh \
        $(realpath "$WEIGHTS") \
        $MASK_SIZE \
        $(basename $DS) \
        $(realpath "$OUTPUT_VALIDATION") \
        $SPLIT_VAL
  done
done
