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
        cv2.createTrackbar("blocksize", title, 2, 100, slider_callback)
        cv2.createTrackbar("k", title, 5, 100, slider_callback)
        cv2.createTrackbar("Aperture Size", title, 0, 15, slider_callback)


def harris_corner_detector(frame, self):
    try:

        blocksize, k, Aperture_size = cv2.getTrackbarPos(
            'blocksize', title), cv2.getTrackbarPos('k', title), cv2.getTrackbarPos('Aperture Size', title)*2+1
    except:
        a = 0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray, blocksize, Aperture_size, k/100)
    frame_detected = frame.copy()
    dst = cv2.dilate(dst, None)
    frame_detected[dst > 0.01*dst.max()] = [0, 0, 255]

    combined = np.hstack((frame, frame_detected))
    # add strip to the combined
    combined = add_strip(combined)
    combined = cv2.putText(combined, "Corners Detected", (500, 30), cv2.FONT_HERSHEY_COMPLEX,
                           1, (0, 0, 255), 2, cv2.LINE_AA)

    return combined


if __name__ == "__main__":
    title = "Harris Corner Detection"
    Cameo(filter=harris_corner_detector, title=title).run()
