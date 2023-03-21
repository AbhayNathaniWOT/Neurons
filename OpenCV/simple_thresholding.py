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
        cv2.createTrackbar("Threshold Type", title, 0, 7, slider_callback)
        cv2.createTrackbar("Threshold Lower", title, 0, 255, slider_callback)
        cv2.createTrackbar("Threshold Upper", title, 0, 255, slider_callback)


Threshold_Options = [cv2.THRESH_BINARY, cv2.THRESH_BINARY_INV, cv2.THRESH_MASK, cv2.THRESH_OTSU,
                     cv2.THRESH_TOZERO, cv2.THRESH_TOZERO_INV, cv2.THRESH_TRIANGLE, cv2.THRESH_TRUNC]

Threshold_Options_str = ["cv2.THRESH_BINARY", "cv2.THRESH_BINARY_INV", "cv2.THRESH_MASK", "cv2.THRESH_OTSU",
                         "cv2.THRESH_TOZERO", "cv2.THRESH_TOZERO_INV", "cv2.THRESH_TRIANGLE", "cv2.THRESH_TRUNC"]


def simple_threshold(frame):
    try:

        Threshold_type_id, Threshold_Lower, Threshold_Upper = cv2.getTrackbarPos(
            'Threshold Type', title), cv2.getTrackbarPos('Threshold Lower', title), cv2.getTrackbarPos('Threshold Upper', title)
        Threshold_type = Threshold_Options[Threshold_type_id]
        Threshold_type_str = Threshold_Options_str[Threshold_type_id]
    except:
        Threshold_type_id, Threshold = 0, 127
        Threshold_type = Threshold_Options[Threshold_type_id]
        Threshold_type_str = Threshold_Options_str[Threshold_type_id]
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    
    ret, threshold_frame = cv2.threshold(
        frame, Threshold_Lower, Threshold_Upper, Threshold_type)

    combined = np.hstack((frame, threshold_frame))
    combined = cv2.putText(combined, Threshold_type_str, (200, 400), cv2.FONT_HERSHEY_COMPLEX,
                           1, (0, 0, 0), 2, cv2.LINE_AA)
    
    return combined


if __name__ == "__main__":
    title = "Thresholding"
    Cameo(filter=simple_threshold, title=title).run()
