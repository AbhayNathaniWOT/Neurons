from cameo import Cameo as Cameo_Base
import cv2
import numpy as np
from utils import add_strip


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
        cv2.createTrackbar("n_features", title, 2, 100, slider_callback)
        cv2.createTrackbar("n_octave", title, 5, 100, slider_callback)
        cv2.createTrackbar("contrast_threshold", title, 0, 100, slider_callback)
        cv2.createTrackbar("edge_threshold", title, 0, 15, slider_callback)


def sift_corner_detector(frame, self):
    try:

        n_features, n_octave, contrast_threshold,edge_threshold = cv2.getTrackbarPos(
            'n_features', title), cv2.getTrackbarPos("n_octave", title), cv2.getTrackbarPos('contrast_threshold', title), cv2.getTrackbarPos('edge_threshold', title)
    except:
        a = 0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    frame_detected  = frame.copy()
    sift = cv2.SIFT_create(n_features,n_octave, contrast_threshold/100,edge_threshold)
    gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX).astype('uint8')
    kp = sift.detect(gray,None)
    frame_detected = cv2.drawKeypoints(gray,kp,frame_detected)
   

    combined = np.hstack((frame, frame_detected))
    # add strip to the combined
    combined = add_strip(combined)
    combined = cv2.putText(combined, "Corners Detected", (500, 30), cv2.FONT_HERSHEY_COMPLEX,
                           1, (0, 0, 255), 2, cv2.LINE_AA)

    return combined


if __name__ == "__main__":
    title = "Sift Corner Detection"
    Cameo(filter=sift_corner_detector, title=title).run()
