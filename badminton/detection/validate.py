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
import csv

ROOT_DIR = os.path.abspath("../../Mask_RCNN")
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

sys.path.append(ROOT_DIR)  # To find local version of the library
sys.path.append(os.path.abspath(".."))
from mrcnn import utils
from mrcnn import visualize
from mrcnn.visualize import display_images
import mrcnn.model as modellib
from mrcnn.model import log

from datasets.badminton_dataset import BadmintonDataset
from detection.detection_config import DetectionConfig

# %matplotlib inline


parser = argparse.ArgumentParser(
    description='Validation.')
parser.add_argument('--WEIGHTS', required=True)
parser.add_argument('--DATASET', required=True)
parser.add_argument('--OUTPUT_PATH', required=True)
parser.add_argument('--MASK_SIZE', required=True)
parser.add_argument('--CI', required=False)
args = parser.parse_args()


config=DetectionConfig()
config.MASK_SHAPE = [int(args.MASK_SIZE), int(args.MASK_SIZE)]

dataset_val = BadmintonDataset()
dataset_val.load_badminton("../datasets/" + args.DATASET, "val")
dataset_val.prepare()

model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)
model.load_weights(args.WEIGHTS, by_name=True)
class_names = ['background', 'badminton']
TPS = []
FPS = []
FNS = []
TNS = []

with open(args.OUTPUT_PATH + "/" + 'validation.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['Image name', 'Image width', 'Image height', 'TP', 'FP', 'FN', 'TN', 'TP+FP+FN+TN', 'width*height'])
    for image_id in dataset_val.image_ids:
        image, image_meta, gt_class_id, gt_bbox, gt_mask =\
            modellib.load_image_gt(dataset_val, config, image_id, use_mini_mask=False)
        gt_mask = gt_mask.astype(np.int)
        basename = os.path.basename(dataset_val.source_image_link(image_id))
        print(basename)

        results = model.detect([image], verbose=0)
        r = results[0]
        result_mask = r['masks'].astype(np.int)

        TP = np.sum(
            np.bitwise_and(gt_mask, result_mask)
        )
        FP = np.sum(
            np.clip(result_mask - gt_mask, 0, 1)
        )
        FN = np.sum(
            np.clip(gt_mask - result_mask, 0, 1)
        )
        TN = np.sum(
            np.clip(np.ones(gt_mask.shape).astype(np.int) - gt_mask - result_mask, 0, 1)
        )
        TPS.append(TP)
        FPS.append(FP)
        FNS.append(FN)
        TNS.append(TN)

        filewriter.writerow([basename, image.shape[1], image.shape[0], str(TP), str(FP), str(FN), str(TN),
            TP+FP+FN+TN, str(image.shape[1] * image.shape[0])])

        diff_mask = np.bitwise_xor(gt_mask, result_mask)
        plt = visualize.display_instances(image, r['rois'], diff_mask, r['class_ids'],
                                class_names, show_bbox=False)
        plt.savefig(args.OUTPUT_PATH + "/" + basename, bbox_inches='tight', pad_inches=0, transparent=True)
        plt.close()
        if args.CI == 'true': break
csvfile.close()

with open(args.OUTPUT_PATH + "/" + 'averages.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['avg TP', 'avg FP', 'avg FN', 'avg TN'])
    filewriter.writerow([np.mean(TPS), np.mean(FPS), np.mean(FNS), np.mean(TNS)])
csvfile.close()
