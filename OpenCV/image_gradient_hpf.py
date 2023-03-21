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
        cv2.createTrackbar("Kernal Size", title, 0, 15, slider_callback)
        cv2.createTrackbar("Derivative Order", title, 0, 5, slider_callback)


def morpho_transformations(frame):
    try:

        kernel_size = cv2.getTrackbarPos(
            'Kernal Size', title)*2+1
        order = cv2.getTrackbarPos(
            'Derivative Order', title)
        if order == 0:
            order = 1

    except:
        kernel_size = 1
    height, width = frame.shape[:2]
    frame = cv2.resize(frame, (int(0.5*width),
                               int(0.5*height)), interpolation=cv2.INTER_CUBIC)
    color = frame.copy()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    
    sobel_dx_frame = cv2.Sobel(frame, cv2.CV_64F, order if order<kernel_size else 1, 0, ksize=kernel_size)
    sobel_dy_frame = cv2.Sobel(
        frame, cv2.CV_64F, 0, order if order < kernel_size else 1, ksize=kernel_size)
    
    sobel_frame = cv2.Sobel(frame, cv2.CV_64F,  order if order < kernel_size else 1,
                            order if order < kernel_size else 1, ksize=kernel_size)

    combined_1 = np.hstack(
        (color, sobel_frame, sobel_dx_frame, sobel_dy_frame))
    combined_1 = cv2.putText(combined_1, f"1. Orignial", (30, 30), cv2.FONT_HERSHEY_COMPLEX,
                             0.8, (0, 0, 255), 2, cv2.LINE_AA)
    combined_1 = cv2.putText(combined_1, f"2. Sobel", (350, 30), cv2.FONT_HERSHEY_COMPLEX,
                             0.8, (0, 0, 255), 2, cv2.LINE_AA)
    combined_1 = cv2.putText(combined_1, f"3. Sobel DX", (680, 30), cv2.FONT_HERSHEY_COMPLEX,
                             0.8, (0, 0, 255), 2, cv2.LINE_AA)
    combined_1 = cv2.putText(combined_1, f"4. Sobel DY", (990, 30), cv2.FONT_HERSHEY_COMPLEX,
                             0.8, (0, 0, 255), 2, cv2.LINE_AA)

    laplacian_frame = cv2.Laplacian(frame, cv2.CV_64F, ksize=kernel_size)
    schhr_frame = frame
    if order>2:order=1
    schhr_dx_frame = cv2.Scharr(frame, cv2.CV_64F, 1, 0)
    schhr_dy_frame = cv2.Scharr(frame, cv2.CV_64F, 0, 1)

    combined_2 = np.hstack(
        (laplacian_frame, schhr_frame, schhr_dx_frame, schhr_dy_frame))
    combined_2 = cv2.putText(combined_2, f"5. Laplacian", (30, 30), cv2.FONT_HERSHEY_COMPLEX,
                             0.8, (0, 0, 255), 2, cv2.LINE_AA)
    combined_2 = cv2.putText(combined_2, f"6. Schhr", (350, 30), cv2.FONT_HERSHEY_COMPLEX,
                             0.8, (0, 0, 255), 2, cv2.LINE_AA)
    combined_2 = cv2.putText(combined_2, f"7. Schhr Dx", (680, 30), cv2.FONT_HERSHEY_COMPLEX,
                             0.8, (0, 0, 255), 2, cv2.LINE_AA)
    combined_2 = cv2.putText(combined_2, f"8. Schhr Dy", (990, 30), cv2.FONT_HERSHEY_COMPLEX,
                             0.8, (0, 0, 255), 2, cv2.LINE_AA)

    combined = np.vstack((combined_1, combined_2))

    return combined


def gray(frame): return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


if __name__ == "__main__":
    title = "Blurring"
    Cameo(filter=morpho_transformations, title=title).run()
