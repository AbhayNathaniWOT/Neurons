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
        cv2.createTrackbar("Min", title, 0, 1000, slider_callback)
        cv2.createTrackbar("Max", title, 0, 1000, slider_callback)
        cv2.createTrackbar("Aperture Size", title, 0, 2, slider_callback)


def contours_detector(frame):
    try:

        Min, Max, Aperture_size = cv2.getTrackbarPos(
            'Min', title), cv2.getTrackbarPos('Max', title), cv2.getTrackbarPos('Aperture Size', title)*2+3
    except:
        a = 0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_contors = frame.copy()

    edged = cv2.Canny(gray, Min, Max, apertureSize=Aperture_size)
    contours, hierarchy = cv2.findContours(edged,
                                           cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    print("Number of Contours found = " + str(len(contours)))
    for i in range(30):
        try:
            rect = cv2.minAreaRect(contours[i])
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(frame_contors, [box], 0, (0, 0, 255), 2)
            (x, y), radius = cv2.minEnclosingCircle(contours[i])
            center = (int(x), int(y))
            radius = int(radius)
            cv2.circle(frame_contors, center, radius, (0, 255, 0), 1)
        except:pass
    # Draw all contours
    # -1 signifies drawing all contours
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)
    combined = np.hstack((frame, frame_contors))
    combined = cv2.putText(combined, "Countours", (200, 400), cv2.FONT_HERSHEY_COMPLEX,
                           1, (0, 0, 0), 2, cv2.LINE_AA)

    return combined


if __name__ == "__main__":
    title = "Contours"
    Cameo(filter=contours_detector, title=title).run()
