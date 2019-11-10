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

from mrcnn import utils
from mrcnn import visualize
from mrcnn.visualize import display_images
import mrcnn.model as modellib
from mrcnn.model import log
from detection_config import DetectionConfig
config=DetectionConfig()
class_names = ['background', 'badminton']

parser = argparse.ArgumentParser(description='Detection.')
parser.add_argument('INPUT', nargs='+')
parser.add_argument('--OUTPUT_DIR', required=False, default='./output')
args = parser.parse_args()
if not os.path.exists(args.OUTPUT_DIR):
    os.makedirs(args.OUTPUT_DIR)

model = modellib.MaskRCNN(mode="inference", model_dir='./', config=config)
model.load_weights('weights.h5', by_name=True)

def plot(type, input, background_image, transparent):
    plt = visualize.display_instances(background_image, r['rois'], r['masks'], r['class_ids'], 
        class_names, show_bbox=False, captions=['']*100)
    plt.savefig(
        '{}/{}_{}'.format(args.OUTPUT_DIR, type, os.path.basename(input)),
        bbox_inches='tight',
        pad_inches=0,
        transparent=transparent
    )

for input_image in args.INPUT:
    image = skimage.io.imread(input_image)
    results = model.detect([image], verbose=0)
    r = results[0]
    plot('visualization', input_image, image, transparent=True)
    plot('mask', input_image, np.zeros(image.shape), transparent=False)
print('Done.')

