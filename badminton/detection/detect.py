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

ROOT_DIR = os.path.abspath("../../Mask_RCNN")
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

sys.path.append(ROOT_DIR)  # To find local version of the library
sys.path.append(os.path.abspath(".."))
from mrcnn import utils
from mrcnn import visualize
from mrcnn.visualize import display_images
import mrcnn.model as modellib
from mrcnn.model import log

from detection.detection_config import DetectionConfig

# %matplotlib inline 

parser = argparse.ArgumentParser(
    description='Detection.')
parser.add_argument('--WEIGHTS', required=True)
parser.add_argument('--INPUT', required=True)
parser.add_argument('--OUTPUT', required=True)
parser.add_argument('--MASK_SIZE', required=True)
args = parser.parse_args()

config=DetectionConfig()
config.MASK_SHAPE = [int(args.MASK_SIZE), int(args.MASK_SIZE)]

model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)
model.load_weights(args.WEIGHTS, by_name=True)


image = skimage.io.imread(args.INPUT)
results = model.detect([image], verbose=1)
r = results[0]

class_names = ['background', 'badminton']
plt = visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], 
                            class_names, r['scores'])
plt.savefig(args.OUTPUT, bbox_inches='tight', pad_inches=0, transparent=True)
