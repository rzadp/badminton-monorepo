import os
ROOT_DIR = os.path.abspath("../../Mask_RCNN")
from mrcnn.config import Config

class BadmintonConfig(Config):
    """Configuration for training on the toy dataset.
    Derives from the base Config class and overrides some values.
    """
    # Give the configuration a recognizable name
    NAME = "badminton"

    # LEARNING_RATE = 0.0001
    # LEARNING_MOMENTUM = 0.09

    # We use a GPU with 12GB memory, which can fit two images.
    # Adjust down if you use a smaller GPU.
    IMAGES_PER_GPU = 1
    GPU_COUNT = 1

    # Number of classes (including background)
    NUM_CLASSES = 1 + 1  # Background + badminton

    # Skip detections with < 90% confidence
    DETECTION_MIN_CONFIDENCE = 0.9

    USE_MINI_MASK = False

    MASK_SHAPE = [28, 28]
    # MASK_SHAPE = [56, 56]
