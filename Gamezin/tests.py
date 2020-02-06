"""
http://howtomakeanrpg.com/a/how-to-make-an-rpg-stats.html
"""
import numpy as np
from item import Item
from bag import *
from inventory import *
from player import *
from missions import Missions
import cv2

P = Player()
I = Item("Shoes", name="Spear{}".format(0))

def nothing(x):
    pass

def test_grab_and_equip():
    print("[Grab item from floor]")
    P._grab_item(I)
    print("INVENTORY: ", P.INVENTORY._get_content())
    print("BAG: ", P.BAG._get_content())
    print("[Equip item from bag to inventory]")
    P._equip_item(0)
    print("INVENTORY: ", P.INVENTORY._get_content())
    print("BAG: ", P.BAG._get_content())

def test_gain_exp_and_level():
    print(P._get_exp())
    print(P._get_level())
    P.gain_exp(10)
    print(P._get_exp())
    print(P._get_level())
    P.gain_exp(10)
    print(P._get_exp())
    print(P._get_level())

def test_drop_item():
    P._grab_item(I)
    P._dispose_item_from_bag(0)

def test_mission():
    m = Missions()

def test_item_erode():
    # print("Will give the player an item that allows him to erode image")
    # print("Improvements on this item may be:")
    # print("Increasing kernel_size, increasing number of iterations and changing kernel type")

    I = Item(classe="Primary", name="Eraser+2")
    P._grab_item(I)
    P._equip_item(0)

    # Get item attributes
    kernel_types = P._get_inventory()["Primary"].attributes[0]
    kernel_size = P._get_inventory()["Primary"].attributes[1]
    kernel_iteration = P._get_inventory()["Primary"].attributes[2]

    image = cv2.imread("/home/enacom/TestesVisao/SOURCES/pokemon3d.jpg")
    window_name = "Test"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.createTrackbar("Erode", window_name, 1, kernel_size, nothing)

    img = image.copy()
    while(1):
        cv2.imshow(window_name, img)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

        # get current positions of four trackbars
        ksize = cv2.getTrackbarPos("Erode", window_name)
        filteri = cv2.getStructuringElement(kernel_types[0], (ksize, ksize))
        img = cv2.erode(image, None, filteri, iterations = kernel_iteration)

if __name__ == "__main__":
    print("Lets start")
    test_item_erode()