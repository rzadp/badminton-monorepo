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
parser.add_argument('--SPLIT_VAL', required=True)
args = parser.parse_args()


config=DetectionConfig()
config.MASK_SHAPE = [int(args.MASK_SIZE), int(args.MASK_SIZE)]

dataset_val = BadmintonDataset()
dataset_val.load_badminton("../datasets/" + args.DATASET, "split", args.SPLIT_VAL)
dataset_val.prepare()

model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)
model.load_weights(args.WEIGHTS, by_name=True)
class_names = ['background', 'badminton']
TPS = []
FPS = []
FNS = []
TNS = []
sensitivities = []
specificities = []
precisions = []
accuracies = []
totalPixel = -1

def visualize_mask(image, mask, label):
    plt = visualize.display_instances(image, r['rois'], mask, r['class_ids'],
                                class_names, show_bbox=False, captions=['']*10)
    plt.savefig(args.OUTPUT_PATH + "/" + label + "_" + basename, bbox_inches='tight', pad_inches=0, transparent=True)
    plt.close()

with open(args.OUTPUT_PATH + "/" + 'validation.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['Image name', 'Image width', 'Image height', 'TP', 'FP', 'FN', 'TN', 'TP+FP+FN+TN', 'width*height'])
    for image_id in dataset_val.image_ids:
        image, image_meta, gt_class_id, gt_bbox, gt_mask =\
            modellib.load_image_gt(dataset_val, config, image_id, use_mini_mask=False)
        totalPixel = image.shape[1] * image.shape[0]
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
        sensitivities.append(TP / (TP + FN))
        specificities.append(TN / (TN + FP))
        precisions.append(TP / (TP + FP))
        accuracies.append((TP+TN) / (TP+TN+FP+FN))

        filewriter.writerow([basename, image.shape[1], image.shape[0], str(TP), str(FP), str(FN), str(TN),
            TP+FP+FN+TN, str(image.shape[1] * image.shape[0])])

        visualize_mask(image, np.clip(result_mask - gt_mask, 0, 1), "fp")
        visualize_mask(image, np.clip(gt_mask - result_mask, 0, 1), "fn")
        if args.CI == 'true': break
csvfile.close()

with open(args.OUTPUT_PATH + "/" + 'grouped.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    mean = lambda name, arr: filewriter.writerow([
        'avg ' + name,
        round(np.mean(arr), 2),
        str(round(np.mean(arr) / totalPixel * 100, 2)) + "%"
    ])
    mean('TP', TPS)
    mean('FP', FPS)
    mean('FN', FNS)
    mean('TN', TNS)
    filewriter.writerow(['avg sensitivity', round(np.mean(sensitivities), 2)])
    filewriter.writerow(['avg specificity', round(np.mean(specificities), 2)])
    filewriter.writerow(['avg precision', round(np.mean(precisions), 2)])
    filewriter.writerow(['avg accuracy', round(np.mean(accuracies), 2)])

    min = lambda name, arr: filewriter.writerow([
        'min ' + name,
        round(np.min(arr), 2),
        str(round(np.min(arr) / totalPixel * 100, 2)) + "%"
    ])
    min('TP', TPS)
    min('FP', FPS)
    min('FN', FNS)
    min('TN', TNS)
    filewriter.writerow(['min sensitivity', round(np.min(sensitivities), 2)])
    filewriter.writerow(['min specificity', round(np.min(specificities), 2)])
    filewriter.writerow(['min precision', round(np.min(precisions), 2)])
    filewriter.writerow(['min accuracy', round(np.min(accuracies), 2)])

    max = lambda name, arr: filewriter.writerow([
        'max ' + name,
        round(np.max(arr), 2),
        str(round(np.max(arr) / totalPixel * 100, 2)) + "%"
    ])
    max('TP', TPS)
    max('FP', FPS)
    max('FN', FNS)
    max('TN', TNS)
    filewriter.writerow(['max sensitivity', round(np.max(sensitivities), 2)])
    filewriter.writerow(['max specificity', round(np.max(specificities), 2)])
    filewriter.writerow(['max precision', round(np.max(precisions), 2)])
    filewriter.writerow(['max accuracy', round(np.max(accuracies), 2)])

    median = lambda name, arr: filewriter.writerow([
        'median ' + name,
        round(np.median(arr), 2),
        str(round(np.median(arr) / totalPixel * 100, 2)) + "%"
    ])
    median('TP', TPS)
    median('FP', FPS)
    median('FN', FNS)
    median('TN', TNS)
    filewriter.writerow(['median sensitivity', round(np.median(sensitivities), 2)])
    filewriter.writerow(['median specificity', round(np.median(specificities), 2)])
    filewriter.writerow(['median precision', round(np.median(precisions), 2)])
    filewriter.writerow(['median accuracy', round(np.median(accuracies), 2)])
csvfile.close()
