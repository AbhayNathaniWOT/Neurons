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
        cv2.createTrackbar("threshold", title, 70, 500, slider_callback)
        cv2.createTrackbar("nonMaxSuppression", title, 0, 1, slider_callback)


def fast_feature_extraction(frame, self):
    try:

        threshold, nonMaxSuppression = cv2.getTrackbarPos(
            'threshold', title), True if cv2.getTrackbarPos("nonMaxSuppression", title) else False

    except:
        a = 0

    print("NonMaxSuppression", nonMaxSuppression)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    frame_detected = frame.copy()
    fast = cv2.FastFeatureDetector_create(threshold, nonMaxSuppression)

    gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX).astype('uint8')
    kp = fast.detect(gray, None)
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
