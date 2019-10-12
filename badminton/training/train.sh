#!/bin/bash
cd $(dirname $0)
set -e
cd ..

OUTPUT_HANDLER=seashells
if [[ $CI == true ]] ; then
  OUTPUT_HANDLER=cat
fi

for f in training/cases/*.env
do
  CASE=$(basename "$f" .env)
  echo "Running for case: $CASE"
  source "$f"

  python3 ./badminton.py train \
  --dataset=./datasets/$DATASET \
  --weights=coco \
  --epochs=$EPOCHS \
  --use_multiprocessing=False \
  --steps_per_epoch=1 \
  --validation_steps=1 \
  --logs=./training/logs \
  --case=$CASE \
  2>&1 | $OUTPUT_HANDLER

  if [[ $NOTIFY_MAIL == true ]] ; then
    echo "Finished training for: $CASE" | mail -s "Badminton training done" roopert7@gmail.com
  fi
done
