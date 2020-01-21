import numpy as np
from item import Item
from bag import *
from inventory import *
from player import *
from missions import Missions
import cv2

FULLSCREEN = False
sex_square = {"MALE" : [[100, 200],[400, 500]],
              "FEMALE": [[300, 400],[400, 500]]}

chr_square = {"CHAR1" : [[100, 200],[100, 200]],
              "CHAR2":  [[300, 400],[300, 400]],
              "CHAR3":  [[100, 200],[300, 400]],
              "CHAR4":  [[300, 400],[300, 400]]}

# Initialize player
P = Player()

def check_if_inside_rectangle(p1, p2, x, y):
    if p1[0] < x < p1[1] and p2[0] < y < p2[1]:
        return 1
    else:
        return 0

def onClick_definesex(event, x, y, p, q):
    if event == cv2.EVENT_LBUTTONDOWN:
        if check_if_inside_rectangle(sex_square["MALE"][0], sex_square["MALE"][1], x, y):
            P._change_sex("MALE")
        elif check_if_inside_rectangle(sex_square["FEMALE"][0], sex_square["FEMALE"][1], x, y):
            P._change_sex("FEMALE")

def onClick_definechar(event, x, y, p, q):
    if event == cv2.EVENT_LBUTTONDOWN:
        if check_if_inside_rectangle(chr_square["CHAR1"][0], chr_square["CHAR1"][1], x, y):
            P._change_sex("CHAR1")

        elif check_if_inside_rectangle(chr_square["CHAR2"][0], chr_square["CHAR2"][1], x, y):
            P._change_sex("CHAR2")

        elif check_if_inside_rectangle(chr_square["CHAR3"][0], chr_square["CHAR3"][1], x, y):
            P._change_sex("CHAR3")

        elif check_if_inside_rectangle(chr_square["CHAR4"][0], chr_square["CHAR4"][1], x, y):
            P._change_sex("CHAR4")


def load_screen(window_name="LoadScreen"):
    image_loadscreen = cv2.imread("/home/enacom/TestesVisao/SOURCES/pokemon3d.jpg")
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    if FULLSCREEN:
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while P._get_sex() is None:
        cv2.setMouseCallback(window_name, on_mouse=onClick_definesex)
        cv2.imshow(window_name, image_loadscreen)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()

def start_game():
    window_name_startgame = "StartGame"
    cv2.namedWindow(window_name_startgame, cv2.WINDOW_NORMAL)
    if FULLSCREEN:
        cv2.setWindowProperty(window_name_startgame,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

    # Come back sex, to test
    P._change_sex(None)
    while P._get_sex() is None:
        cv2.setMouseCallback(window_name_startgame, on_mouse=onClick_definesex)
        cv2.imshow(window_name_startgame, image_startgame)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

    # After end game
    cv2.destroyAllWindows()


image_startgame = cv2.imread("/home/enacom/TestesVisao/SOURCES/example_01.png")
# image_loadscreen = cv2.imread("/home/enacom/TestesVisao/SOURCES/pokemon3d.jpg")

load_screen()
start_game()
