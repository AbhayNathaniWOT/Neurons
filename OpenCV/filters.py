import cv2,numpy,utils
# We will be adding filter functions and classes to filters.py

def BGR2GRAY(frame): return cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)



colors = [i for i in dir(cv2) if i.startswith("COLOR_")]
   