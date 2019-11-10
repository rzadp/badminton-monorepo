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
dataset_val.load_badminton("../datasets/" + args.DATASET, "split", int(args.SPLIT_VAL))
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
                                class_names, show_bbox=False, captions=['']*100)
    plt.savefig(args.OUTPUT_PATH + "/" + label + "_" + basename, bbox_inches='tight', pad_inches=0, transparent=True)
    plt.close()

with open(args.OUTPUT_PATH + "/" + 'validation.csv', 'w') as file:
    filewriter = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
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
        if result_mask.shape[2] == 0:
            result_mask = np.zeros(gt_mask.shape).astype(np.int)

        TP = np.sum(
            np.bitwise_and(gt_mask, result_mask)
        ) / gt_mask.shape[2]
        FP = np.sum(
            np.clip(
                np.subtract(result_mask, gt_mask), 0, 1
        )
        ) / gt_mask.shape[2]
        FN = np.sum(
            np.clip(
                np.subtract(gt_mask, result_mask), 0, 1
            )
        ) / gt_mask.shape[2]
        gt_background = np.subtract(np.ones(gt_mask.shape).astype(np.int), gt_mask)
        TN = np.sum(
            np.clip(
                np.subtract(gt_background, result_mask), 0, 1
            )
        ) / gt_mask.shape[2]
        TPS.append(TP)
        FPS.append(FP)
        FNS.append(FN)
        TNS.append(TN)
        sensitivities.append(TP / (TP + FN))
        specificities.append(TN / (TN + FP))
        precisions.append(TP / (TP + FP) if (TP + FP) > 0 else 0.0)
        accuracies.append((TP+TN) / (TP+TN+FP+FN))

        filewriter.writerow([basename, image.shape[1], image.shape[0], str(TP), str(FP), str(FN), str(TN),
            TP+FP+FN+TN, str(image.shape[1] * image.shape[0])])

        # visualize_mask(image, np.clip(result_mask - gt_mask, 0, 1), "fp")
        # visualize_mask(image, np.clip(gt_mask - result_mask, 0, 1), "fn")
        if args.CI == 'true': break
file.close()

def row(title, arrays, aggregation, percentage):
    result = r'\hline ' + title
    for arr in arrays:
        result += ' & ' + str(round(aggregation(arr), 2))
        if percentage:
            result += ' ({}\%)'.format(str(round(aggregation(arr) / totalPixel * 100, 2)))
    return result + r' \\' + '\n'

def mean_row(arrays, percentage):
    return row('Średnia', arrays, lambda x: np.mean(x), percentage)

def min_row(arrays, percentage):
    return row('Minimum', arrays, lambda x: np.min(x), percentage)

def max_row(arrays, percentage):
    return row('Maksimum', arrays, lambda x: np.max(x), percentage)

def median_row(arrays, percentage):
    return row('Mediana', arrays, lambda x: np.median(x), percentage)

with open(args.OUTPUT_PATH + "/" + 'grouped.csv', 'w') as file:
    file.write(r'\hline \textbackslash & True Positive & False Positive & False Negative & True Negative \\'  + '\n')
    file.write(mean_row([TPS, FPS, FNS, TNS], True))
    file.write(min_row([TPS, FPS, FNS, TNS], True))
    file.write(max_row([TPS, FPS, FNS, TNS], True))
    file.write(median_row([TPS, FPS, FNS, TNS], True))
    file.write(r'\hline')
    file.write('\n\n\n')

    file.write(r'\hline \textbackslash & Accuracy & Sensitivity & Specificity & Precision \\'  + '\n')
    file.write(mean_row([accuracies, sensitivities, specificities, precisions], False))
    file.write(min_row([accuracies, sensitivities, specificities, precisions], False))
    file.write(max_row([accuracies, sensitivities, specificities, precisions], False))
    file.write(median_row([accuracies, sensitivities, specificities, precisions], False))
    file.write(r'\hline')
    file.write('\n')
file.close()
