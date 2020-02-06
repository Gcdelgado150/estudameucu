from item import Item

class Inventory():
    def __init__(self):
        """Item_class: item_name"""
        self.invent = {"Primary": None,
                      "Secondary": None,
                      "Hat": None,
                      "Breastplate": None,
                      "Legs": None,
                      "Shoes": None
                      }

    def _equip_an_item(self, i):
        """Receives the item i from the bag and equip it
        if possible.
        Args:
            i (item.class): An item that should be in the bag

        Returns:
            boolean: True for sucessfully equip
                     False for negative equip"""
        if isinstance(i, Item) and i._get_status() == "Bag":
            item_class = i._get_class()
            if item_class in self.invent:
                self.invent[item_class] = i
                return 1
            else:
                print("[The item class {} does not exists]".format(item_class))
                return 0

    def _get_content(self):
        """Get content of inventory"""
        return self.invent