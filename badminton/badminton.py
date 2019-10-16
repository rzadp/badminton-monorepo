"""
Mask R-CNN
Badminton
"""

from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) 

import os
import sys
import datetime
import time

# Root directory of the project
ROOT_DIR = os.path.abspath("../Mask_RCNN")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn import model as modellib, utils
sys.path.append(os.path.abspath(".."))
from common.badminton_config import BadmintonConfig
from datasets.badminton_dataset import BadmintonDataset

# Path to trained weights file
COCO_WEIGHTS_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")

# Directory to save logs and model checkpoints, if not provided
# through the command line argument --logs
DEFAULT_LOGS_DIR = os.path.join(ROOT_DIR, "logs")


def train(model, epochs, use_multiprocessing):
    """Train the model."""
    # Training dataset.
    dataset_train = BadmintonDataset()
    dataset_train.load_badminton(args.dataset, "train")
    dataset_train.prepare()

    # Validation dataset
    dataset_val = BadmintonDataset()
    dataset_val.load_badminton(args.dataset, "val")
    dataset_val.prepare()

    # *** This training schedule is an example. Update to your needs ***
    # Since we're using a very small dataset, and starting from
    # COCO trained weights, we don't need to train too long. Also,
    # no need to train all layers, just the heads should do it.
    print("Training network heads")
    model.train(dataset_train, dataset_val,
                learning_rate=config.LEARNING_RATE,
                epochs=epochs,
                use_multiprocessing=use_multiprocessing,
                layers='heads')
    #model_path = os.path.join(ROOT_DIR, "samples/badminton/mask_rcnn_badminton.h5")
    print("Saving weights...")
    model.keras_model.save_weights("./training/result.h5")
    print("Done!")


############################################################
#  Training
############################################################

if __name__ == '__main__':
    import argparse

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Train Mask R-CNN to detect badminton.')
    parser.add_argument("command",
                        metavar="<command>",
                        help="'train'")
    parser.add_argument('--dataset', required=False,
                        metavar="/path/to/badminton/dataset/",
                        help='Directory of the Badminton dataset')
    parser.add_argument('--weights', required=True,
                        metavar="/path/to/weights.h5",
                        help="Path to weights .h5 file or 'coco'")
    parser.add_argument('--epochs', required=True,
                        metavar="20",
                        help="Number of epochs")
    parser.add_argument('--steps_per_epoch', required=False,
                        default=1000,
                        metavar="1000",
                        help="Steps per epoch")
    parser.add_argument('--validation_steps', required=False,
                        default=50,
                        metavar="50",
                        help="Validation steps")
    parser.add_argument('--use_multiprocessing', required=True,
                        metavar="False",
                        help="Should use multiprocessing")
    parser.add_argument('--verbose', required=False,
                        default=0,
                        metavar="0",
                        help='Verbosity')
    parser.add_argument('--logs', required=False,
                        default=DEFAULT_LOGS_DIR,
                        metavar="/path/to/logs/",
                        help='Logs and checkpoints directory (default=logs/)')
    parser.add_argument('--case', required=False,
                        default="",
                        metavar="example",
                        help='Case name, to identify configuration')
    parser.add_argument('--mask_size', required=True,
                        default="",
                        metavar="28",
                        help='Mask size, e.g. 28, 56')
    args = parser.parse_args()

    # Validate arguments
    assert args.command == "train"
    assert args.dataset, "Argument --dataset is required for training"

    print("Logs: ", args.logs)

    # Configurations
    config = BadmintonConfig()
    config.STEPS_PER_EPOCH = int(args.steps_per_epoch)
    config.VALIDATION_STEPS = int(args.validation_steps)
    config.NAME = config.NAME + "_" + args.case + "_"
    config.MASK_SHAPE = [int(args.mask_size), int(args.mask_size)]
    # config.display()

    # Create model
    model = modellib.MaskRCNN(mode="training", config=config, model_dir=args.logs)

    # Select weights file to load
    if args.weights.lower() == "coco":
        weights_path = COCO_WEIGHTS_PATH
        # Download weights file
        if not os.path.exists(weights_path):
            utils.download_trained_weights(weights_path)
    elif args.weights.lower() == "last":
        # Find last trained weights
        weights_path = model.find_last()
    elif args.weights.lower() == "imagenet":
        # Start from ImageNet trained weights
        weights_path = model.get_imagenet_weights()
    else:
        weights_path = args.weights

    # Load weights
    print("Loading weights ", weights_path)
    if args.weights.lower() == "coco":
        # Exclude the last layers because they require a matching
        # number of classes
        model.load_weights(weights_path, by_name=True, exclude=[
            "mrcnn_class_logits", "mrcnn_bbox_fc",
            "mrcnn_bbox", "mrcnn_mask"])
    else:
        model.load_weights(weights_path, by_name=True)

    # Train or evaluate
    start = time.time()
    train(model, int(args.epochs), args.use_multiprocessing == "True")
    end = time.time()
    print("Done. train(model) took " + str(round((end - start) / 60, 1)) + " minutes")

    f = open(model.log_dir + '/' + args.case + '.env', "w+")
    f.write("MASK_SIZE=" + args.mask_size + '\n')
    f.close()
