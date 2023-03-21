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



def slider_callback(s):pass

class Cameo(Cameo_Base):
    def __init__(self, filter, title) -> None:
        super().__init__(filter, title)

    def Keypress_Events(self, keycode):
        print("Key_pressed", keycode)
    
    def loop_Events(self, title):
        self._windowManager.apply_filter = object_tracking
    
    def window_changes(self, title):
        cv2.createTrackbar("h_u", title, 0, 180, slider_callback)
        cv2.createTrackbar("h_l", title, 0, 180, slider_callback)
        cv2.createTrackbar("s_u", title, 0, 255, slider_callback)
        cv2.createTrackbar("s_l", title, 0, 255, slider_callback)
        cv2.createTrackbar("v_u", title, 0, 255, slider_callback)
        cv2.createTrackbar("v_l", title, 0, 255, slider_callback)
        








def object_tracking(frame):
    try:    
        h_l, s_l, v_l = cv2.getTrackbarPos('h_l', title),cv2.getTrackbarPos('s_l', title),cv2.getTrackbarPos('v_l', title)

        h_u, s_u, v_u  = cv2.getTrackbarPos('h_u', title),cv2.getTrackbarPos('s_u', title),cv2.getTrackbarPos('v_u', title)
        
        color_range_lower = np.array([h_l,s_l,v_l])
        color_range_upper = np.array([h_u,s_u, v_u])
    except:
        color_range_lower = np.array([0, 0, 0])
        color_range_upper = np.array([180, 255, 50])
    frame = cv2.resize(frame,(frame.shape[1]-200,frame.shape[0]-200))
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Create a mask to seprate the give range of colors
    mask = cv2.inRange(hsv_frame, color_range_lower, color_range_upper)
    
    # Using Bitwise-AND on mask and Image
    # Thus, selected colors will be multiplied by 1 in the mask else 0
    # Thus, interest color segmented
    segmented = cv2.bitwise_and(frame,frame,mask=mask)

    # Convert to BGR to stack and show (no special purpose)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    
    # Stacking Results
    combined1 = np.hstack((frame,hsv_frame))
    combined2 = np.hstack((mask,segmented))
    combined = np.vstack((combined1,combined2))
    
    return combined


if __name__ == "__main__":
    title = "BGR to GrayScale"
    Cameo(filter=object_tracking, title=title).run()
