import cv2
img = cv2.imread("image.jpg")
hist = cv2.calcHist([img],[0],None,[256],[0,256])
print(hist.shape)