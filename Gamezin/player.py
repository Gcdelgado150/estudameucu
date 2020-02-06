from bag import *
from inventory import *

class Configurations():
    """For now configurating experience_map
    (amount of experience for each level)
    """
    def __init__(self):
        """Set initial exp (for upgrading to level 2)
        Set multitplier logic to experience map
        Generate experience map"""
        self.initial_exp = 10
        self.multiplier = [1.5]*30 + [1.3]*30 + [1.18]*30 + [1.06]*9
        self.map_exp = self.generate_map()
        super().__init__()

    def generate_map(self):
        """For each value in multiplier, grab last value in map and
        update to new value, generating a whole map"""
        map_exp = {}
        for i in range(len(self.multiplier)):
            if i == 0:
                map_exp[str(i+2)] = int(self.multiplier[i]*self.initial_exp)
            else:
                map_exp[str(i+2)] = int(self.multiplier[i]*map_exp[str(i+1)])

        return map_exp

    def get_mult(self):
        return self.multiplier

    def get_map(self):
        return self.map_exp

cfx = Configurations()

class Player():
    def __init__(self):
        self.BAG = Bag()
        self.INVENTORY = Inventory()
        self.__sex = None
        self.__LEVEL = 1
        self.__EXPERIENCE = 0

        self.__char = None
        self.__name = None

        # TODO (gcd) add current and total hp
        # TODO (gcd) add stats (str, car, speed, int)

    def _get_sex(self):
        return self.__sex

    def _get_bag(self):
        return self.BAG._get_content()

    def _get_inventory(self):
        return self.INVENTORY._get_content()

    def _get_level(self):
        return self.__LEVEL

    def _get_exp(self):
        return self.__EXPERIENCE

    def _get_char(self):
        return self.__char

    def _get_name(self):
        return self.__name

    def _change_sex(self, value):
        self.__sex = value

    def _change_char(self, image):
        self.__char = image

    def _change_name(self, name):
        self.__name = name

    def __check_if_equip_possible(self, i):
        if isinstance(i, Item) and self.BAG._not_full():
            return 1
        else:
            return 0

    def _grab_item(self, i):
        """Grab item from ground and add it to bag

        Args:
            i (item.class): the item found
        """
        if self.__check_if_equip_possible(i):
            self.BAG._add_an_item(self.BAG._get_first_slot(), i)
            i._change_status("Bag")

    def _dispose_item_from_bag(self, idx):
        """dispose item idx in bag
        Args:
            idx (int): the index of item wanted.
        """
        if isinstance(self.BAG._get_an_item__(idx), Item):
            self.BAG._drop_an_item(idx)
        else:
            print("There is no item in this slot!")

    def _equip_item(self, idx):
        """Equip the item idx to inventory
        Args:
            idx (int): the index of item chosed.
        """
        if isinstance(self.BAG._get_an_item__(idx), Item):
            i = self.BAG._get_an_item__(idx)
            # If possible, add to inventory
            r = self.INVENTORY._equip_an_item(i)
            # If needed, remove from bag
            if r:
                self.BAG._equip_an_item(idx)

    def define_level(self):
        """After some exp gained, check and upgrade level"""
        # get from exp gained and compare it to map
        old_lvl = self.__LEVEL
        for k, value in cfx.get_map().items():
            if value < self.__EXPERIENCE:
                self.__LEVEL = int(k)

        if old_lvl != self.__LEVEL:
            print("Subiu de LVL! {}->{}".format(old_lvl, self.__LEVEL) )

    def gain_exp(self, value):
        """Gain specific value of experience and check level"""
        if type(value) != int or value < 0:
            raise ValueError("Experience value inconsistent. Must be a positive integer")

        self.__EXPERIENCE += value
        self.define_level()