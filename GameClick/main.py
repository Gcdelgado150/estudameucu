import cv2
import numpy as np
from player import *

def check_if_inside_rectangle(p1, p2, x, y):
    return 1 if p1[0] < x < p1[1] and p2[0] < y < p2[1] else 0

chr_square = {"CHAR1": [[208, 280], [194, 342]],
              "CHAR2": [[342, 440], [205, 333]],
              "CHAR3": [[525, 615], [178, 343]]}

# Initialize player
P = Player()

def onClick_defineaction(event, x, y, p, q):
    if event == cv2.EVENT_LBUTTONDOWN:
        if check_if_inside_rectangle(chr_square["CHAR1"][0], chr_square["CHAR1"][1], x, y):
            P.clicked()

        elif check_if_inside_rectangle(chr_square["CHAR2"][0], chr_square["CHAR2"][1], x, y):
            P.set_coin_per_click(2)

        elif check_if_inside_rectangle(chr_square["CHAR3"][0], chr_square["CHAR3"][1], x, y):
            P.multiply_coin_per_click(1.1)

def load_screen(window_name="LoadScreen"):
    image_loadscreen = cv2.imread("/home/enacom/TestesVisao/SOURCES/pokemon3d.jpg")
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    earned = P.get_total_coin()

    while 1:
        cv2.setMouseCallback(window_name, on_mouse=onClick_defineaction)
        cv2.imshow(window_name, image_loadscreen)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
        if P.get_total_coin() != earned:
            print(P.get_total_coin())
            earned = P.get_total_coin()

    cv2.destroyAllWindows()

load_screen()