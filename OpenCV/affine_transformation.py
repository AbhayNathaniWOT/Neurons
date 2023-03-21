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
        cv2.createTrackbar("p1_before", title, 0, 300, slider_callback)
        cv2.createTrackbar("p1_after", title, 0, 300, slider_callback)
        cv2.createTrackbar("p2_before", title, 0, 300, slider_callback)
        cv2.createTrackbar("p2_after", title, 0, 300, slider_callback)
        cv2.createTrackbar("p3_before", title, 0, 300, slider_callback)
        cv2.createTrackbar("p3_after", title, 0, 300, slider_callback)


def rotate(frame):
    try:
        

        p1_before, p2_before, p3_before = cv2.getTrackbarPos('p1_before', title), cv2.getTrackbarPos(
            'p2_before', title), cv2.getTrackbarPos('p3_before', title)

        p1_after, p2_after, p3_after = cv2.getTrackbarPos('p1_after', title), cv2.getTrackbarPos(
            'p2_after', title), cv2.getTrackbarPos('p3_after', title)
    except:
        p1_before, p2_before, p3_before = 0,0,0
        p1_after, p2_after, p3_after = 0,0,0

    # Rows and cols
    rows,cols = frame.shape[:2]
    # intial points and points after transformation
    p_before = np.float32([[p1_before,50],[p2_before,50],[p3_before,200]])
    p_after = np.float32([[p1_after,100],[p2_after,50],[p3_after,250]])
    
    transform_matrix = cv2.getAffineTransform(p_before,p_after)
    transformed_frame = cv2.warpAffine(frame,transform_matrix,(cols,rows))
    combined = np.hstack((frame, transformed_frame))
    return combined


if __name__ == "__main__":
    title = "Rotate"
    Cameo(filter=rotate, title=title).run()
