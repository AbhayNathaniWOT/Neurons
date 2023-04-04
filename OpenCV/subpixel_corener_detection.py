from cameo import Cameo as Cameo_Base
import cv2
import numpy as np
from utils import add_strip


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
        cv2.createTrackbar("windowsize", title, 2, 100, slider_callback)
        cv2.createTrackbar("blocksize", title, 2, 100, slider_callback)
        cv2.createTrackbar("k", title, 5, 100, slider_callback)
        cv2.createTrackbar("Aperture Size", title, 0, 15, slider_callback)


def subpixel_corner_detector(frame, self):
    try:

        windowsize, blocksize, k, Aperture_size = cv2.getTrackbarPos('windowsize', title),cv2.getTrackbarPos(
            'blocksize', title), cv2.getTrackbarPos('k', title), cv2.getTrackbarPos('Aperture Size', title)*2+1
    except:
        a = 0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray, blocksize, Aperture_size, k/100)
    frame_detected = frame.copy()
    dst = cv2.dilate(dst, None)
    ret,dst = cv2.threshold(dst,0.1*dst.max(),255,0)
    dst = np.uint8(dst)
    
    #find centroids using cv2 connectedComponentsWithStats method
    ret,labels,stats,centroids = cv2.connectedComponentsWithStats(dst)
    
    # define criteria to stop and refine corners
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(gray,np.float32(centroids),(windowsize,windowsize),(-1,-1),criteria)

    res = np.hstack((centroids,corners))
    res = np.int0(res)
    frame_detected[res[:,1],res[:,0]] = [0,0,255]
    frame_detected[res[:, 3], res[:, 2]] = [0,255,0]
    
    
    
    
    combined = np.hstack((frame, frame_detected))
    # add strip to the combined
    combined = add_strip(combined)
    combined = cv2.putText(combined, "Corners Detected", (500, 30), cv2.FONT_HERSHEY_COMPLEX,
                           1, (0, 0, 255), 2, cv2.LINE_AA)

    return combined


if __name__ == "__main__":
    title = "Subpixel Corner Detection"
    Cameo(filter=subpixel_corner_detector, title=title).run()
