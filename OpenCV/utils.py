import cv2, numpy, scipy.interpolate
# more general-purpose math functions will go in utils.py


def isGray(image):
    """Return True if the image has one channel per pixel."""
    return image.ndim < 3
