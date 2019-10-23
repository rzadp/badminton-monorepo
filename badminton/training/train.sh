#!/bin/bash
cd $(dirname $0)
set -e
cd ..

OUTPUT_HANDLER=seashells
if [[ $CI == true ]] || ! command -v seashells || true ; then
  OUTPUT_HANDLER=cat
fi

for f in training/cases/*.env
do
  CASE=$(basename "$f" .env)
  source "$f"
  [[ $SKIP == true ]] && continue || echo "Running for case: $CASE"

  python3 -u ./badminton.py \
  --DATASET=./datasets/$DATASET \
  --STARTING_WEIGHTS=${STARTING_WEIGHTS:-coco} \
  --EPOCHS=$EPOCHS \
  --USE_MULTIPROCESSING=False \
  --STEPS_PER_EPOCH=$STEPS_PER_EPOCH \
  --VALIDATION_STEPS=$VALIDATION_STEPS \
  --LOGS=./training/logs \
  --CASE=$CASE \
  --MASK_SIZE=$MASK_SIZE \
  --USE_MINI_MASK=$USE_MINI_MASK \
  --MINI_MASK_SIZE=$MINI_MASK_SIZE \
  --TRAIN_ROIS_PER_IMAGE=$TRAIN_ROIS_PER_IMAGE \
  --MAX_GT_INSTANCES=$MAX_GT_INSTANCES \
  2>&1 | $OUTPUT_HANDLER

  [ ${PIPESTATUS[0]} -eq 0 ] && RESULT="SUCCESS" || RESULT="FAIL"

  if [[ $NOTIFY_MAIL == true ]] ; then
    echo -e "Finished training for: ${CASE}\nResult: ${RESULT}\n" | mail -s "Badminton training done" roopert7@gmail.com
  fi
done
