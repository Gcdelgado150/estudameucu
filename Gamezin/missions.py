import cv2
from item import Item
from bag import *
from inventory import *
from player import *

# TODO (gcd): create items present in the image
# This will have coordinates?
# If coordinates, it has to change conform Width of new image. (after resize)
# Simple math.

# Idea if bounding box
# : {"item": [ [xmin, xmax], [ymin, ymax] ]}
# Idea if not bounding box
# It can be a dnn to detect each object  (segnet, fastrcnn)
map_mission1 = {"shield1": [[]],
                "shield1": [[]],
                "shield1": [[]],
                "shield1": [[]]}

class Missions():
    def __init__(self):
        self.__level = 1
        self.__base_dir_images = "sources/missions/"
        # New height should be taken from device used
        self.__default_height = 900
        self.__window_name = "Image"
        self.clicked = False
        self.design_mission()

    def _get_level(self):
        return self.__level

    def _upgrade_level(self):
        self.__level += 1

    def resize_correctly(self):
        """Correctly resize image with"""
        # Resize image to new size
        w, h = self.image.shape[:2]
        new_w = int(self.__default_height * float(w/h))

        self.image = cv2.resize(self.image, (self.__default_height, new_w))

    def design_mission(self):
        if self.__level == 1:
            self.mission_lvl1()

    def click_and_crop(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.process_click(x, y)

    def process_click(self, x, y):
        self.clicked = True
        print(x, y)

    def mission_lvl1(self):
        """It will show a photo of armory"""
        print("[GAME] Find a weapon and choose one by clicking on it.")
        self.image = cv2.imread(self.__base_dir_images + "mission1.jpeg")
        self.resize_correctly()

        cv2.namedWindow(self.__window_name)
        cv2.setMouseCallback(self.__window_name, self.click_and_crop)

        while self.clicked == False:
            cv2.imshow(self.__window_name, self.image)
            cv2.waitKey(0)
