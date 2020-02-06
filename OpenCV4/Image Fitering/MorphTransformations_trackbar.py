import cv2
import numpy as np
import os
import sys

def nothing(x): pass

# Create a black image, a window
img_ori = cv2.imread("/home/enacom/TestesVisao/SOURCES/pokemon3d.jpg")
img = img_ori.copy()

win_name = "Image"
cv2.namedWindow(win_name)

# create trackbars for color change
cv2.createTrackbar("Element:\n 0: Rect \n 1: Cross \n 2: Ellipse", win_name, 0, 2, nothing)
cv2.createTrackbar('Kernel size:\n 2n +1', win_name, 3, 31, nothing)
cv2.createTrackbar('Iterations', win_name, 0, 7, nothing)

while(1):
    # Get values from TrackbarPos
    element = cv2.getTrackbarPos("Element:\n 0: Rect \n 1: Cross \n 2: Ellipse", win_name)
    k_size = cv2.getTrackbarPos('Kernel size:\n 2n +1', win_name)
    itera = cv2.getTrackbarPos('Iterations', win_name)

    # Apply filter
    try:
        filteri = cv2.getStructuringElement(element, (k_size, k_size))
        img = cv2.erode(img_ori, None, filteri, iterations = itera)
    except:
        os.system("clear")

    cv2.imshow(win_name, img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()