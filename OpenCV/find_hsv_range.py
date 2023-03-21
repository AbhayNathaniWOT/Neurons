import cv2
import numpy as np


color_range_lower = np.uint8([[[234, 130, 130]]])
color_range_upper = np.uint8([[[150, 70, 70]]])

hsv_range_upper = cv2.cvtColor(color_range_upper,cv2.COLOR_BGR2HSV)
hsv_range_lower = cv2.cvtColor(color_range_lower,cv2.COLOR_BGR2HSV)

print("HSV Lower range:",hsv_range_lower)
print("HSV Upper range:",hsv_range_upper)

print([i for i in dir(cv2) if i.startswith("THRESH")])
a = np.array([[1,2],[1,2],[1,2]])
b = np.ones((1,a.shape[1]))
a = np.concatenate((a,b))
print(a)
