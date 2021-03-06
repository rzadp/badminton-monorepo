import os
ROOT_DIR = os.path.abspath("../../Mask_RCNN")
from common.badminton_config import BadmintonConfig

class DetectionConfig(BadmintonConfig):
    IMAGES_PER_GPU = 1
    GPU_COUNT = 1

    # Skip detections with < 90% confidence
    DETECTION_MIN_CONFIDENCE = 0.9

    USE_MINI_MASK = False
    IMAGE_RESIZE_MODE = "pad64"
    IMAGE_MIN_DIM = 640
    IMAGE_MAX_DIM = 1024
    IMAGE_MIN_SCALE = None
