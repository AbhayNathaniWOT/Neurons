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
        cv2.createTrackbar("Kernal Size", title, 10, 100, slider_callback)


def lpf_blurring(frame):
    try:

        kernel_size = cv2.getTrackbarPos(
            'Kernal Size', title)
        if kernel_size == 0:
            kernel_size = 1
        kernel_matrix = np.ones(
            (kernel_size, kernel_size), np.float32)/(kernel_size**2)
    except:
        kernel_matrix = np.ones((5, 5), np.float32)/25

    height, width = frame.shape[:2]
    frame = cv2.resize(frame, (int(0.7*width),
                               int(0.7*height)), interpolation=cv2.INTER_CUBIC)

    blurred_frame = cv2.filter2D(frame, -1, kernel_matrix)
    
    guassian_blur = cv2.GaussianBlur(frame,(kernel_size*2+1,kernel_size*2+1),0)
    median_blur = cv2.medianBlur(frame,kernel_size*2+1)
    combined_1 = np.hstack((frame, blurred_frame))
    combined_1 = cv2.putText(combined_1, f"Averaging - Kernel: {kernel_size}x{kernel_size}", (480, 30), cv2.FONT_HERSHEY_COMPLEX,
                             0.8, (0, 0, 255), 1, cv2.LINE_AA)
    combined_2 = np.hstack((guassian_blur, blurred_frame))
    combined_2 = cv2.putText(combined_2, f"Guassian - {kernel_size*2+1}x{kernel_size*2+1}", (50, 30), cv2.FONT_HERSHEY_COMPLEX,
                             0.8, (0, 0, 255), 1, cv2.LINE_AA)
    combined_2 = cv2.putText(combined_2, f"Median - {kernel_size*2+1}x{kernel_size*2+1}", (480, 30), cv2.FONT_HERSHEY_COMPLEX,
                             0.8, (0, 0, 255), 1, cv2.LINE_AA)
    combined = np.vstack((combined_1, combined_2))

    return combined


if __name__ == "__main__":
    title = "Blurring"
    Cameo(filter=lpf_blurring, title=title).run()
