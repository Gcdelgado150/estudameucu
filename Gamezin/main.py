"""
http://howtomakeanrpg.com/a/how-to-make-an-rpg-stats.html
"""
import numpy as np
from item import Item
from bag import *
from inventory import *
from player import *
from missions import Missions

P = Player()
I = Item("Shoes", name="Spear{}".format(0))

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

if __name__ == "__main__":
    print("Lets start")
    test_gain_exp_and_level()