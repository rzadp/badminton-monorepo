from mrcnn.config import Config

class DetectionConfig(Config):
    NAME = "badminton"
    NUM_CLASSES = 1 + 1  # Background + badminton
    IMAGES_PER_GPU = 1
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    GPU_COUNT = 1

    # Skip detections with < 90% confidence
    DETECTION_MIN_CONFIDENCE = 0.9

    MASK_SHAPE = [56, 56]
    USE_MINI_MASK = False
    IMAGE_RESIZE_MODE = "pad64"
    IMAGE_MIN_DIM = 640
    IMAGE_MAX_DIM = 1024
    IMAGE_MIN_SCALE = None
