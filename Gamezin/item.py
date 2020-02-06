import numpy as np
import cv2

elements = [cv2.MORPH_RECT, cv2.MORPH_CROSS, cv2.MORPH_ELLIPSE]

class Item():
    def __init__(self, classe, name):
        """
        Input:
            classe: [Primary, Secondary, (...), Food, Equipment]
            name: Name of the equipment
            status: Equipped, Bag, Dropped, Safe
        """
        self.__item_class = classe
        self.__name = name
        self.__status = ""
        self.attributes = self.get_attributes()

    def _get_name(self):
        return self.__name

    def _get_status(self):
        return self.__status

    def _get_class(self):
        return self.__item_class

    def _change_status(self, status):
        self.__status = status

    def _change_name(self, new_name):
        self.__name = new_name

    def get_attributes(self):
        # This will return:
        # Kernel type, size and amount of iterations possible
        if self.__name == "Eraser":
            # Since lvl 1, only basic
            return [[cv2.MORPH_RECT], 3, 1]
        if self.__name == "Eraser+1":
            # Since lvl 1, only basic
            return [[cv2.MORPH_RECT], 5, 1]
        if self.__name == "Eraser+2":
            # Since lvl 1, only basic
            return [[cv2.MORPH_RECT], 7, 1]
        if self.__name == "Eraser+3":
            # Since lvl 1, only basic
            return [[cv2.MORPH_RECT], 7, 2]