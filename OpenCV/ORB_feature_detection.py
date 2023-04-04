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
        cv2.createTrackbar("scale_factor", title, 5, 100, slider_callback)
        cv2.createTrackbar("nlevels", title,
                           0, 100, slider_callback)
        cv2.createTrackbar("edge_threshold", title, 1, 15, slider_callback)


def fast_feature_extraction(frame, self):
    try:

        n_features, scale_factor, nlevels, edge_threshold = cv2.getTrackbarPos(
            'n_features', title), cv2.getTrackbarPos("scale_factor", title)+1, cv2.getTrackbarPos('nlevels', title)+1, cv2.getTrackbarPos('edge_threshold', title)

    except:
        a = 0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    frame_detected = frame.copy()
    orb = cv2.ORB_create(n_features, nlevels=nlevels,
                         edgeThreshold=edge_threshold)
    # orb = cv2.ORB_create()
    gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX).astype('uint8')
    kp = orb.detect(gray, None)
    frame_detected = cv2.drawKeypoints(
        frame_detected, kp, None, color=(0, 0, 255))

    combined = np.hstack((frame, frame_detected))
    # add strip to the combined
    combined = add_strip(combined)
    combined = cv2.putText(combined, "Corners Detected", (500, 30), cv2.FONT_HERSHEY_COMPLEX,
                           1, (0, 0, 255), 2, cv2.LINE_AA)

    return combined


if __name__ == "__main__":
    title = "Fast Feature Extraction"
    Cameo(filter=fast_feature_extraction, title=title).run()
