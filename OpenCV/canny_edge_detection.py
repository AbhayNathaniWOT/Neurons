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
        cv2.createTrackbar("Min", title, 0, 1000, slider_callback)
        cv2.createTrackbar("Max", title, 0, 1000, slider_callback)
        cv2.createTrackbar("Aperture Size", title, 0, 2, slider_callback)
        
        




def Canny_edge(frame):
    try:

        Min, Max,Aperture_size = cv2.getTrackbarPos(
            'Min', title), cv2.getTrackbarPos('Max', title), cv2.getTrackbarPos('Aperture Size', title)*2+3
    except:
        a = 0
        
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    canny_frame = cv2.Canny(frame,Min,Max,apertureSize=Aperture_size)
    


    combined = np.hstack((frame, canny_frame))
    combined = cv2.putText(combined, "Canny Edge", (200, 400), cv2.FONT_HERSHEY_COMPLEX,
                           1, (0, 0, 0), 2, cv2.LINE_AA)

    return combined


if __name__ == "__main__":
    title = "Canny Edge Detection"
    Cameo(filter=Canny_edge, title=title).run()
