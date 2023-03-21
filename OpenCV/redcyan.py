from cameo import Cameo
import cv2,numpy as np


def redcyan(frame):
    b,g,r = cv2.split(frame)
    b = cv2.addWeighted(b,0.5,b,0.5,0.0)
    filter_frame = cv2.merge([b,b,r])

    combined = np.hstack((frame,filter_frame))
    return combined
    


if __name__ == "__main__":
    Cameo(filter=redcyan,title="BGR to Red Cyan").run()
