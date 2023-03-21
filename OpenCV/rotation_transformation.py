from cameo import Cameo as Cameo_Base
import cv2
import numpy as np

# Rotates the image by 90 degree with respect to center without any scaling.


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
        cv2.createTrackbar("rotation", title, 0, 360, slider_callback)


def rotate(frame):
    try:

        Rotation_Angle = cv2.getTrackbarPos('rotation', title)
    except:
        Rotation_Angle = 0
    
    # cols-1 rows-1 are coordinate limits
    rows,cols = frame.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D(((cols-1)/2,(rows-1)/2),Rotation_Angle,1)
    rotated_frame = cv2.warpAffine(frame,rotation_matrix,(cols,rows))
    combined = np.hstack((frame,rotated_frame))
    return combined


if __name__ == "__main__":
    title = "Rotate"
    Cameo(filter=rotate, title=title).run()
