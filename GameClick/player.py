class Player():
    def __init__(self):
        super().__init__()
        self.__coin_per_click = 1
        self.__total_clicks = 0
        self.__total_coin = 0

    def get_coin_per_click(self):
        return self.__coin_per_click

    def get_total_clicks(self):
        return self.__total_clicks

    def get_total_coin(self):
        return self.__total_coin

    def set_coin_per_click(self, value):
        if value > self.__coin_per_click:
            print("Clicks earn more!")
            self.__coin_per_click = value

    def multiply_coin_per_click(self, multiplier):
        print("Coins per click multiplied by {}!".format(multiplier-1))
        self.__coin_per_click *= multiplier

    def clicked(self):
        print("Clicked!!")
        self.__total_clicks += 1
        self.__total_coin += self.__coin_per_click
