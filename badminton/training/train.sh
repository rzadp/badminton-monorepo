#!/bin/bash
cd $(dirname $0)
set -e
cd ..

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
  --case=$CASE
done
