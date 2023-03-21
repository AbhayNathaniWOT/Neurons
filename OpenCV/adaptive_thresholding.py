# The adaptiveMethod decides how the threshold value is calculated:

# 1. cv2.ADAPTIVE_THRESH_MEAN_C: The threshold value is the mean of the neighbourhood area minus the constant C.
# 2. cv2.ADAPTIVE_THRESH_GAUSSIAN_C: The threshold value is a gaussian-weighted sum of the neighbourhood values minus the constant C.


from cameo import Cameo as Cameo_Base
import cv2
import numpy as np

# We will convert BGR to HSV Model
# -  As its easy to represent color in HSV model Space than in BGR

# Method :
#     1. Take Each frame
#     2. Convert from BGR 2 HSV
#     3. Threshold HSV image for a range of Intrest Color
#     4. Extract the blue object alone, we can do whatever we want on that image


color_range_lower = np.array([0, 0, 0])
# (Darkness)
color_range_upper = np.array([180, 255, 50])


def slider_callback(s): pass


class Cameo(Cameo_Base):
    def __init__(self, filter, title) -> None:
        super().__init__(filter, title)
        self.apply_filter = filter

    def Keypress_Events(self, keycode):
        print("Key_pressed", keycode)

    def loop_Events(self, title):
        self._windowManager.apply_filter = self.apply_filter

    def window_changes(self, title):
        cv2.createTrackbar("Block Size", title, 0, 10, slider_callback)
        cv2.createTrackbar("C", title, 0, 500, slider_callback)


def adaptive_thresholding(frame):
    try:

        Block_Size, C = cv2.getTrackbarPos(
            'Block Size', title)*2 + 3, cv2.getTrackbarPos('C', title)/100
    except:
        Block_Size, C = 11, 1

    height, width = frame.shape[:2]
    hf, wf = 0.75, 0.75
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    frame = cv2.resize(frame, (int(wf*width),
                               int(hf*height)), interpolation=cv2.INTER_CUBIC)
    retv, simple_threshold = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)

    adaptive_threshold_mean = cv2.adaptiveThreshold(
        frame, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, Block_Size, C)
    adaptive_threshold_guassian = cv2.adaptiveThreshold(
        frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, Block_Size, C)

    combined_h1 = np.hstack((frame, simple_threshold))
    combined_h2 = np.hstack(
        (adaptive_threshold_mean, adaptive_threshold_guassian))
    combined = np.vstack((combined_h1, combined_h2))
    combined = cv2.cvtColor(combined, cv2.COLOR_GRAY2BGR)
    combined = cv2.putText(combined, "Grayscale Image", (150, 20), cv2.FONT_HERSHEY_COMPLEX,
                           0.5, (0, 0, 255), 1, cv2.LINE_AA)
    combined = cv2.putText(combined, "Simple / Global Thresholding th = 127", (600, 20), cv2.FONT_HERSHEY_COMPLEX,
                           0.5, (0, 0, 255), 1, cv2.LINE_AA)
    combined = cv2.putText(combined, "Adaptive Mean Thresholding", (150, 350), cv2.FONT_HERSHEY_COMPLEX,
                           0.5, (0, 0, 255), 1, cv2.LINE_AA)
    combined = cv2.putText(combined, "Adaptive Guassian Thresholding", (600, 350), cv2.FONT_HERSHEY_COMPLEX,
                           0.5, (0, 0, 255), 1, cv2.LINE_AA)

    return combined


if __name__ == "__main__":
    title = "Adaptive Thresholding"
    Cameo(filter=adaptive_thresholding, title=title).run()
