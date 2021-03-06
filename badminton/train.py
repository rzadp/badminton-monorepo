from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) 
import os
import sys
import datetime
import time
import argparse

# Root directory of the project
ROOT_DIR = os.path.abspath("../Mask_RCNN")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn import model as modellib, utils
from common.badminton_config import BadmintonConfig
from datasets.badminton_dataset import BadmintonDataset

# Path to trained weights file
COCO_WEIGHTS_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")


def train(model, epochs, use_multiprocessing):
    """Train the model."""
    # Training dataset.
    dataset_train = BadmintonDataset()
    dataset_train.load_badminton(args.DATASET, "split", int(args.SPLIT_TRAIN))
    dataset_train.prepare()

    # Validation dataset
    dataset_val = BadmintonDataset()
    dataset_val.load_badminton(args.DATASET, "split", int(args.SPLIT_VAL))
    dataset_val.prepare()

    # *** This training schedule is an example. Update to your needs ***
    # Since we're using a very small dataset, and starting from
    # COCO trained weights, we don't need to train too long. Also,
    # no need to train all layers, just the heads should do it.
    print("Training layers: " + str(args.LAYERS))
    model.train(dataset_train, dataset_val,
                learning_rate=config.LEARNING_RATE,
                epochs=epochs,
                use_multiprocessing=use_multiprocessing,
                layers=args.LAYERS)

    print("Done!")


def parse_args():
    parser = argparse.ArgumentParser(description='Train Mask R-CNN to detect badminton.')
    parser.add_argument('--DATASET', required=True)
    parser.add_argument('--STARTING_WEIGHTS', required=True)
    parser.add_argument('--EPOCHS', required=True)
    parser.add_argument('--STEPS_PER_EPOCH', required=True)
    parser.add_argument('--VALIDATION_STEPS', required=True)
    parser.add_argument('--USE_MULTIPROCESSING', required=True)
    parser.add_argument('--LOGS', required=True)
    parser.add_argument('--CASE', required=True)
    parser.add_argument('--MASK_SIZE', required=True)
    parser.add_argument('--USE_MINI_MASK', required=True)
    parser.add_argument('--MINI_MASK_SIZE', required=True)
    parser.add_argument('--MAX_GT_INSTANCES', required=True)
    parser.add_argument('--TRAIN_ROIS_PER_IMAGE', required=True)
    parser.add_argument('--LAYERS', required=True)
    parser.add_argument('--SPLIT_VAL', required=True)
    parser.add_argument('--SPLIT_TRAIN', required=True)
    args = parser.parse_args()
    print("Logs: ", args.LOGS)
    return args


def prepare_config():
    config = BadmintonConfig()
    config.STEPS_PER_EPOCH = int(args.STEPS_PER_EPOCH)
    config.VALIDATION_STEPS = int(args.VALIDATION_STEPS)
    config.NAME = args.CASE + "_"
    config.MASK_SHAPE = [int(args.MASK_SIZE), int(args.MASK_SIZE)]
    config.USE_MINI_MASK = str(args.USE_MINI_MASK).lower() == 'true'
    config.USE_MULTIPROCESSING = str(args.USE_MULTIPROCESSING).lower() == 'true'
    config.MINI_MASK_SHAPE = (int(args.MINI_MASK_SIZE), int(args.MINI_MASK_SIZE))
    config.MAX_GT_INSTANCES = int(args.MAX_GT_INSTANCES)
    config.TRAIN_ROIS_PER_IMAGE = int(args.TRAIN_ROIS_PER_IMAGE)
    return config
    

def select_weights():
    if args.STARTING_WEIGHTS.lower() == "coco":
        weights_path = COCO_WEIGHTS_PATH
        if not os.path.exists(weights_path):
            utils.download_trained_weights(weights_path)
        return weights_path
    elif args.STARTING_WEIGHTS.lower() == "last":
        # Find last trained weights
        return model.find_last()
    elif args.STARTING_WEIGHTS.lower() == "imagenet":
        # Start from ImageNet trained weights
        return model.get_imagenet_weights()
    else:
        return args.STARTING_WEIGHTS


############################################################
#  Training entry point
############################################################

if __name__ == '__main__':
    args = parse_args()
    config = prepare_config()
    model = modellib.MaskRCNN(mode="training", config=config, model_dir=args.LOGS)
    weights_path = select_weights()

    print("Loading weights ", weights_path)
    if args.STARTING_WEIGHTS.lower() == "coco":
        # Exclude the last layers because they require a matching number of classes
        model.load_weights(weights_path, by_name=True, exclude=[
            "mrcnn_class_logits", "mrcnn_bbox_fc",
            "mrcnn_bbox", "mrcnn_mask"])
    else:
        model.load_weights(weights_path, by_name=True)


    # Perfrom the training
    start = time.time()
    train(model, int(args.EPOCHS), config.USE_MULTIPROCESSING)
    end = time.time()
    print("Done. train(model) took " + str(round((end - start) / 60, 1)) + " minutes")


    # Save args in logs for reference
    f = open(model.log_dir + '/' + args.CASE + '.env', "w+")
    for k in args.__dict__:
        f.write(str(k) + '=' + str(args.__dict__[k]) + '\n')
    f.close()
