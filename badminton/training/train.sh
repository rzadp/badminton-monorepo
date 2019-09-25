#!/bin/bash
cd $(dirname $0)
set -e

cd ..
python3 ./badminton.py train \
--dataset=./datasets/badminton_high \
--weights=coco \
--epochs=1 \
--use_multiprocessing=False \
--steps_per_epoch=1 \
--validation_steps=1 \
--logs=./training/logs
