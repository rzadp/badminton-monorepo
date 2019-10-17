#!/bin/bash
cd $(dirname $0)
set -e
cd ..

OUTPUT_HANDLER=seashells
if [[ $CI == true ]] || ! command -v seashells ; then
  OUTPUT_HANDLER=cat
fi

for f in training/cases/*.env
do
  CASE=$(basename "$f" .env)
  source "$f"
  [[ $SKIP == true ]] && continue || echo "Running for case: $CASE"

  python3 ./badminton.py train \
  --dataset=./datasets/$DATASET \
  --weights=coco \
  --epochs=$EPOCHS \
  --use_multiprocessing=False \
  --steps_per_epoch=$STEPS_PER_EPOCH \
  --validation_steps=$VALIDATION_STEPS \
  --logs=./training/logs \
  --case=$CASE \
  --mask_size=$MASK_SIZE \
  2>&1 | $OUTPUT_HANDLER

  if [[ $NOTIFY_MAIL == true ]] ; then
    echo "Finished training for: $CASE" | mail -s "Badminton training done" roopert7@gmail.com
  fi
done
