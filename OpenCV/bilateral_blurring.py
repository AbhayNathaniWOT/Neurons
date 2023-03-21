from cameo import Cameo as Cameo_Base
import cv2
import numpy as np


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
        cv2.createTrackbar("D", title, 0, 50, slider_callback)
        cv2.createTrackbar("Sigma Color", title, 0, 300, slider_callback)
        cv2.createTrackbar("Sigma Space", title, 0, 300, slider_callback)


def bilateral_blurring(frame):

    d = cv2.getTrackbarPos("D", title)
    sigma_color = cv2.getTrackbarPos("Sigma Color", title)
    sigma_space = cv2.getTrackbarPos("Sigma Space", title)

    blurred_frame = cv2.bilateralFilter(frame,d,sigma_color,sigma_space)
    combined = np.hstack((frame, blurred_frame))
    combined = cv2.putText(combined, "Orignal ", (50, 50), cv2.FONT_HERSHEY_COMPLEX,
                           1, (0, 0, 0), 2, cv2.LINE_AA)
    combined = cv2.putText(combined, "Bilateral Blurred", (700, 50), cv2.FONT_HERSHEY_COMPLEX,
                           1, (0, 0, 0), 2, cv2.LINE_AA)

    return combined


if __name__ == "__main__":
    title = "Bilateral Blurring"
    Cameo(filter=bilateral_blurring, title=title).run()
