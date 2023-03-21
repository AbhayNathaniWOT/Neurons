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
        cv2.createTrackbar("hf", title, 10, 500, slider_callback)
        cv2.createTrackbar("wf", title, 10, 500, slider_callback)


def resize(frame):
    try:
    
        height_factor, width_factor = cv2.getTrackbarPos(
            'hf', title), cv2.getTrackbarPos('wf', title)
    except:
        height_factor, width_factor = 1, 1
    if height_factor<50:height_factor=100
    if width_factor<50:width_factor=100
    height, width = frame.shape[:2]
    print(height_factor,width_factor)
    res = cv2.resize(frame, (int(width_factor*width/100),
                    int( height_factor*height/100)), interpolation=cv2.INTER_CUBIC)
    return res


if __name__ == "__main__":
    title = "Resize"
    Cameo(filter=resize, title=title).run()
