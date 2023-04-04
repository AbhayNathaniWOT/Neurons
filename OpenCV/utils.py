import cv2, numpy, scipy.interpolate,numpy as np
# more general-purpose math functions will go in utils.py


def isGray(image):
    """Return True if the image has one channel per pixel."""
    return image.ndim < 3

def add_strip(frame,strip_size=50,orientation = "top",c="white"):
    if orientation=="top":
        strip = np.ones(
            ((strip_size), frame.shape[1], frame.shape[2]), np.uint8)*255 if c == "white" else np.zeros(
            ((strip_size), frame.shape[1], frame.shape[2]), np.uint8)
        combined  = np.vstack((strip, frame))
    elif orientation=="bottom":
        strip = np.ones(
            ((strip_size), frame.shape[1], frame.shape[2]), np.uint8)*255 if c == "white" else np.zeros(
            ((strip_size), frame.shape[1], frame.shape[2]), np.uint8)
        combined  = np.vstack((frame,strip))
    elif orientation=="right":
        strip = np.ones((frame.shape[0], (strip_size), frame.shape[2]), np.uint8)*255 if c == "white" else np.zeros(
            (frame.shape[0], (strip_size), frame.shape[2]), np.uint8)
        combined  = np.hstack((strip, frame))
    elif orientation=="left":
        strip = strip = np.ones((frame.shape[0], (strip_size), frame.shape[2]), np.uint8)*255 if c == "white" else np.zeros(
            (frame.shape[0], (strip_size), frame.shape[2]), np.uint8)
        combined  = np.hstack((frame,strip))  
    else:
        strip = np.ones(
            ((strip_size), frame.shape[1], frame.shape[2]), np.uint8)*255 if c == "white" else np.zeros(
            ((strip_size), frame.shape[1], frame.shape[2]), np.uint8)
        combined  = np.vstack((strip, frame))
          
    return combined