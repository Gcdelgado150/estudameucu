from item import Item

class Bag():
    def __init__(self):
        """Set bag limit and create initial empty bag"""
        self.bag_limit = 20
        self.bag = [None]*self.bag_limit

    def _get_an_item__(self, i):
        return self.bag[i]

    def _drop_an_item(self, idx):
        """Drop item idx from bag"""
        print("Item {} removed!".format(self.bag[idx]._get_name()))
        item = self.bag[idx]
        item._change_status("Dropped")
        self.bag[idx] = None

    def _equip_an_item(self, i):
        """Select item by his index in Bag,
           Change status of item to Inventory
           Remove item from bag"""
        item = self.bag[i]
        item._change_status("Inventory")
        self.bag[i] = None

    def _add_an_item(self, i, item):
        """Change status of item to Bag
           Add item to position i in Bag"""
        item._change_status("Bag")
        self.bag[i] = item

    def _get_content(self):
        return self.bag

    def _not_full(self):
        for i in range(len(self.bag)):
            if self.bag[i] is None:
                return 1
        print("Sorry, your bag is full!")
        return 0 # Full bag

    def _get_first_slot(self):
        for i in range(len(self.bag)):
            if self.bag[i] is None:
                return i
        return -1 # Some error