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
        cv2.createTrackbar("Threshold", title, 185, 255, slider_callback)
        cv2.createTrackbar("Kernal Size", title, 10, 100, slider_callback)
        cv2.createTrackbar("Iteration", title, 1, 20, slider_callback)


def morpho_transformations(frame):
    try:

        kernel_size = cv2.getTrackbarPos(
            'Kernal Size', title)
        iteration = cv2.getTrackbarPos(
            'Iteration', title)
        threshold = cv2.getTrackbarPos(
            'Threshold', title)
        if kernel_size == 0:
            kernel_size = 1
        kernel_matrix = np.ones(
            (kernel_size, kernel_size), np.float32)/(kernel_size**2)
    except:
        kernel_matrix = np.ones((5, 5), np.float32)/25

    height, width = frame.shape[:2]
    frame = cv2.resize(frame, (int(0.5*width),
                               int(0.5*height)), interpolation=cv2.INTER_CUBIC)

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    retv, frame = cv2.threshold(frame, threshold, 255, cv2.THRESH_BINARY)
    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    erosion_frame = cv2.erode(frame, kernel_matrix, iterations=iteration)
    dilation_frame = cv2.dilate(frame, kernel_matrix, iterations=iteration)
    opening_frame = cv2.morphologyEx(frame,cv2.MORPH_OPEN,kernel_matrix,iterations=iteration)

    combined_1 = np.hstack(
        (frame, erosion_frame, dilation_frame, opening_frame))
    combined_1 = cv2.putText(combined_1, f"1. Orignial", (30, 30), cv2.FONT_HERSHEY_COMPLEX,
                             0.5, (0, 0, 255), 1, cv2.LINE_AA)
    combined_1 = cv2.putText(combined_1, f"2. Erosion", (350, 30), cv2.FONT_HERSHEY_COMPLEX,
                             0.5, (0, 0, 255), 1, cv2.LINE_AA)
    combined_1 = cv2.putText(combined_1, f"3. Dilation", (680, 30), cv2.FONT_HERSHEY_COMPLEX,
                             0.5, (0, 0, 255), 1, cv2.LINE_AA)
    combined_1 = cv2.putText(combined_1, f"4. Opening", (990, 30), cv2.FONT_HERSHEY_COMPLEX,
                             0.5, (0, 0, 255), 1, cv2.LINE_AA)

    closing_frame = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel_matrix, iterations=iteration)
    morpho_gradient_frame  = cv2.morphologyEx(frame,cv2.MORPH_GRADIENT,kernel_matrix,iterations=iteration)
    top_hat_frame  = cv2.morphologyEx(frame,cv2.MORPH_TOPHAT,kernel_matrix,iterations=iteration)
    black_hat_frame  = cv2.morphologyEx(frame,cv2.MORPH_BLACKHAT,kernel_matrix,iterations=iteration)


    combined_2 = np.hstack(
        (closing_frame, morpho_gradient_frame, top_hat_frame, black_hat_frame))
    combined_2 = cv2.putText(combined_2, f"5. Closing", (30, 30), cv2.FONT_HERSHEY_COMPLEX,
                             0.5, (0, 0, 255), 1, cv2.LINE_AA)
    combined_2 = cv2.putText(combined_2, f"6. Morphological Gradient", (350, 30), cv2.FONT_HERSHEY_COMPLEX,
                             0.5, (0, 0, 255), 1, cv2.LINE_AA)
    combined_2 = cv2.putText(combined_2, f"7. Top Hat", (680, 30), cv2.FONT_HERSHEY_COMPLEX,
                             0.5, (0, 0, 255), 1, cv2.LINE_AA)
    combined_2 = cv2.putText(combined_2, f"8. Black Hat", (990, 30), cv2.FONT_HERSHEY_COMPLEX,
                             0.5, (0, 0, 255), 1, cv2.LINE_AA)

    combined = np.vstack((combined_1, combined_2))

    return combined


if __name__ == "__main__":
    title = "Morphological Transformations"
    Cameo(filter=morpho_transformations, title=title).run()
