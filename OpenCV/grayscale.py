from cameo import Cameo
import cv2,numpy as np

def BGR2GRAY(frame):
    filter_frame = cv2.cvtColor(cv2.cvtColor(
        frame, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
    combined = np.hstack((frame,filter_frame))
    return combined

if __name__ == "__main__":
    Cameo(filter=BGR2GRAY,title="BGR to GrayScale" ).run()
