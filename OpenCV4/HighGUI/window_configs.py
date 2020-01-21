import cv2
import numpy as np

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
if cv2.__version__[0] == "3":
    print(cv2.selectROI(window_name, image[:,:,0], showCrossHair=True))
if cv2.__version__[0] == "4":
    print(cv2.getWindowImageRect(window_name))
    print(cv2.getWindowProperty(window_name))
# cv2.resizeWindow(window_name, 500, 600)
# cv2.moveWindow(window_name, 500, 600)
cv2.imshow(window_name, image)
cv2.waitKey(0)