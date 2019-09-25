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

# Root directory of the project
ROOT_DIR = os.path.abspath("../../Mask_RCNN")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
sys.path.append(os.path.abspath(".."))
from mrcnn import utils
from mrcnn import visualize
from mrcnn.visualize import display_images
import mrcnn.model as modellib
from mrcnn.model import log

# %matplotlib inline 

# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

# Local path to trained weights file
BADMINTON_MODEL_PATH = os.path.abspath("../detection/weights.h5")
BADMINTON_DATASET_DIR = os.path.abspath("../datasets/badminton_high")


from detection.detection_config import DetectionConfig
from datasets.badminton_dataset import BadmintonDataset


config = DetectionConfig()


model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)
model.load_weights(BADMINTON_MODEL_PATH, by_name=True)


image = skimage.io.imread("./input.jpg")

results = model.detect([image], verbose=1)

r = results[0]
masks = r['masks']
[y_len, x_len, detected_len] = masks.shape

for n in range(0, detected_len):
    output = open(str.format("output{0}.txt", n),"w+")
    for y in range(0, y_len):
        for x in range(0, x_len):
            output.write('1' if masks[y, x, n] else '0')
        output.write('\n')
    output.close()


class_names = ['background', 'badminton']
plt = visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], 
                            class_names, r['scores'])
plt.savefig("./output.png", bbox_inches='tight', pad_inches=0, transparent=True)
