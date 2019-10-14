import os
import sys
import random
import math
import re
import time
import numpy as np
import tensorflow as tf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import skimage.io
import argparse

# Root directory of the project
ROOT_DIR = os.path.abspath("../../Mask_RCNN")

# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
sys.path.append(os.path.abspath(".."))
from mrcnn import utils
from mrcnn import visualize
from mrcnn.visualize import display_images
import mrcnn.model as modellib
from mrcnn.model import log

# %matplotlib inline 

# Local path to trained weights file
BADMINTON_MODEL_PATH = os.path.abspath("../detection/weights.h5")

parser = argparse.ArgumentParser(
    description='Detection.')
parser.add_argument('--weights', required=True,
                    metavar="/path/to/weights.h5",
                    help="Path to weights .h5 file")
parser.add_argument('--input', required=True,
                    metavar="/path/to/image/input/",
                    help='Path to image input')
parser.add_argument('--output', required=True,
                    metavar="/path/to/image/output/",
                    help='Path to image output')
args = parser.parse_args()


from detection.detection_config import DetectionConfig
from datasets.badminton_dataset import BadmintonDataset


config = DetectionConfig()


model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)
model.load_weights(args.weights, by_name=True)


image = skimage.io.imread(args.input)

results = model.detect([image], verbose=1)
r = results[0]

class_names = ['background', 'badminton']
plt = visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], 
                            class_names, r['scores'])
plt.savefig(args.output, bbox_inches='tight', pad_inches=0, transparent=True)
