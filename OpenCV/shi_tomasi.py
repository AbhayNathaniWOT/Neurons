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
        cv2.createTrackbar("max_corners", title, 25, 100, slider_callback)
        cv2.createTrackbar("quality_level", title, 5, 100, slider_callback)
        cv2.createTrackbar("min_distance", title, 0, 15, slider_callback)


def shi_tomasi_corner_detection(frame, self):
    try:

        max_corners, quality_level, min_distance = cv2.getTrackbarPos(
            'max_corners', title), cv2.getTrackbarPos('quality_level', title), cv2.getTrackbarPos('min_distance', title)
    except:
        a = 0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)

    corners = cv2.goodFeaturesToTrack(
        gray, max_corners, quality_level/100, min_distance)
    corners = np.int0(corners)
    for i in corners:
        x, y = i.ravel()
        cv2.circle(frame, (x, y), 4, (0, 255, 0), -1)

    # add strip to the combined
    frame = add_strip(frame)
    frame = cv2.putText(frame, "Corners Detected", (100, 30), cv2.FONT_HERSHEY_COMPLEX,
                        1, (0, 0, 255), 2, cv2.LINE_AA)

    return frame


if __name__ == "__main__":
    title = "Shi-Tomasi Corner Detection"
    Cameo(filter=shi_tomasi_corner_detection, title=title).run()
