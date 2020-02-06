import cv2
import numpy as np

POSITIONING_VALUES = {"SQUIRTLE": [[208, 280], [194, 342]], 
                      "BULBA": [[342, 440], [205, 333]], 
                      "CHAR": [[525, 615], [178, 343]]}

def onMouse_event(event, x, y, p, q):
    # print(event, x, y, p, q)
    if event == MOUSE_EVENT_TYPES[1]:
        # Maybe this can trigger contour find, to find what object did we clicked.
        if POSITIONING_VALUES["SQUIRTLE"][0][0] < x < POSITIONING_VALUES["SQUIRTLE"][0][1] and POSITIONING_VALUES["SQUIRTLE"][1][0] < y< POSITIONING_VALUES["SQUIRTLE"][1][1]:
            print("Squirtle")
        if POSITIONING_VALUES["BULBA"][0][0] < x < POSITIONING_VALUES["BULBA"][0][1] and POSITIONING_VALUES["BULBA"][1][0] < y< POSITIONING_VALUES["BULBA"][1][1]:
            print("Bulba")
        if POSITIONING_VALUES["CHAR"][0][0] < x < POSITIONING_VALUES["CHAR"][0][1] and POSITIONING_VALUES["CHAR"][1][0] < y< POSITIONING_VALUES["CHAR"][1][1]:
            print("Char")
        
def nothing(x):
    pass

MOUSE_EVENT_FLAGS = [cv2.EVENT_FLAG_LBUTTON, 
                     cv2.EVENT_FLAG_RBUTTON,
                     cv2.EVENT_FLAG_MBUTTON,
                     cv2.EVENT_FLAG_CTRLKEY,
                     cv2.EVENT_FLAG_SHIFTKEY,
                     cv2.EVENT_FLAG_ALTKEY
                    ]

MOUSE_EVENT_TYPES = [cv2.EVENT_MOUSEMOVE,
                     cv2.EVENT_LBUTTONDOWN,
                     cv2.EVENT_RBUTTONDOWN,
                     cv2.EVENT_MBUTTONDOWN,
                     cv2.EVENT_LBUTTONUP,
                     cv2.EVENT_RBUTTONUP,
                     cv2.EVENT_MBUTTONUP,
                     cv2.EVENT_LBUTTONDBLCLK,
                     cv2.EVENT_RBUTTONDBLCLK,
                     cv2.EVENT_MBUTTONDBLCLK,
                     cv2.EVENT_MOUSEWHEEL,
                     cv2.EVENT_MOUSEHWHEEL]

QT_BUTTON_TYPES = [cv2.QT_PUSH_BUTTON, 
                   cv2.QT_CHECKBOX, 
                   cv2.QT_RADIOBOX, 
                   cv2.QT_NEW_BUTTONBAR]

QT_FONT_STYLES = [cv2.QT_STYLE_NORMAL,
                  cv2.QT_STYLE_ITALIC,
                  cv2.QT_STYLE_OBLIQUE]
QT_FONT_WEIGHTS = [cv2.QT_FONT_LIGHT, 
                   cv2.QT_FONT_NORMAL, 
                   cv2.QT_FONT_DEMIBOLD, 
                   cv2.QT_FONT_BOLD, 
                   cv2.QT_FONT_BLACK]

WINDOW_FLAGS = [cv2.WINDOW_NORMAL, cv2.WINDOW_AUTOSIZE,
                cv2.WINDOW_OPENGL, cv2.WINDOW_FULLSCREEN, 
                cv2.WINDOW_FREERATIO, cv2.WINDOW_KEEPRATIO,
                cv2.WINDOW_GUI_EXPANDED, cv2.WINDOW_GUI_NORMAL]

WINDOW_PROPERTY_FLAGS = [cv2.WND_PROP_FULLSCREEN, 
                         cv2.WND_PROP_AUTOSIZE, 
                         cv2.WND_PROP_ASPECT_RATIO,
                         cv2.WND_PROP_OPENGL,
                         cv2.WND_PROP_VISIBLE]

image = cv2.imread("/home/enacom/TestesVisao/SOURCES/pokemon3d.jpg")
window_name = "image"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

## Create ButtonCallback
# cv2.ButtonCallback(state)
## Callback function for a button created by cv::createButton.
## State (-1 for a push button, 0 for check, 1 for radio button)

## Create MouseCallback
# cv2.MouseCallback(event, x, y, flags)
cv2.setMouseCallback(window_name, on_mouse=onMouse_event)
## Callback function for mouse events see cv::setMouseCallback.
## event (one of the [MOUSE_EVENT_TYPES]
## x, y (x-coord and y-coord of the mouse event)
## flags (one of the [MOUSE_EVENT_FLAGS]

## Create TrackbarCallback
## Callback function for Trackbar see cv::createTrackbar
cv2.createTrackbar("Size \n 2n +1", window_name, 3, 7, nothing)
cv2.createTrackbar("Erode", window_name, 0, 3, nothing)
cv2.createTrackbar("Dilate", window_name, 0, 3, nothing)

img = image.copy()
while(1):
    cv2.imshow(window_name, img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    # get current positions of four trackbars
    ksize = cv2.getTrackbarPos("Size \n 2n +1", window_name)
    it_erode = cv2.getTrackbarPos("Erode", window_name)
    it_dilate = cv2.getTrackbarPos("Dilate", window_name)
    
    filteri = cv2.getStructuringElement(0, (ksize, ksize))
    img = cv2.erode(image, None, filteri, iterations = it_erode)
    img = cv2.dilate(img, None, filteri, iterations = it_dilate)

cv2.destroyAllWindows()
print("ok")