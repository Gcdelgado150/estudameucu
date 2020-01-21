import cv2
import numpy as np

def nothing(x):
    pass

# Create a black image, a window
img_ori = cv2.imread("/home/enacom/TestesVisao/SOURCES/pokemon3d.jpg")
img = img_ori.copy()
win_name = "Image"
cv2.namedWindow(win_name)

# create trackbars for color change
cv2.createTrackbar("Element:\n 0: Rect \n 1: Cross \n 2: Ellipse",win_name, 0, 2, nothing)
cv2.createTrackbar('Kernel size:\n 2n +1', win_name, 3, 31,nothing)
cv2.createTrackbar('Iterations', win_name, 0, 7, nothing)
# cv2.createTrackbar('Element:\n 0: Rect \n 1: Cross \n 2: Ellipse','Dilation Demo',0,2,nothing)
# cv2.createTrackbar("Kernel size:\n 2n +1", "Dilation Demo",0,21,nothing)

# create switch for ON/OFF functionality
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, win_name,0, 1, nothing)

while(1):
    cv2.imshow(win_name,img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    # get current positions of four trackbars
    element = cv2.getTrackbarPos("Element:\n 0: Rect \n 1: Cross \n 2: Ellipse",win_name)
    k_size = cv2.getTrackbarPos('Kernel size:\n 2n +1', win_name)
    itera = cv2.getTrackbarPos('Iterations', win_name)
    s = cv2.getTrackbarPos(switch, win_name)

    if s == 1:
        # Apply filter
        filteri = cv2.getStructuringElement(element, (k_size, k_size))
        img = cv2.erode(img_ori, None, filteri, iterations = 1)

cv2.destroyAllWindows()