import numpy as np

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