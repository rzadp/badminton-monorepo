#!/bin/bash
cd $(dirname $0)
set -e

source cases/example.env

cd ..
python3 ./badminton.py train \
--dataset=./datasets/$DATASET \
--weights=coco \
--epochs=$EPOCHS \
--use_multiprocessing=False \
--steps_per_epoch=1 \
--validation_steps=1 \
--logs=./training/logs \
--case=$CASE
