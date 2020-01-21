import numpy as np
import random
from random import randint, choice
import subprocess
import platform
import time

class MapGrid:
    def __init__(self, width, height, pw=.02, pr=.01, pf=.02):
        self.dimensions = (width, height)
        self.grid = np.ones((self.dimensions[0], self.dimensions[1], 3), np.uint8)

        self.amount_of_wood = self.dimensions[0]*self.dimensions[1]*pw
        self.amount_of_rock = self.dimensions[0]*self.dimensions[1]*pr
        self.amount_of_food = self.dimensions[0]*self.dimensions[1]*pf
        self.actual_wood = self.amount_of_wood
        self.actual_rock = self.amount_of_rock
        self.actual_food = self.amount_of_food

        self.allocated_positions = []
        self.allocated_wood = self.alocate_wood()
        self.allocated_rock = self.alocate_rock()
        self.allocated_food = self.alocate_food()

        self.start = self.define_start_point()
        self.player = self.start

        self.draw_grid()

    def check_if_player_out(self):
        if self.player[0][0] < 0 or self.player[0][0] > self.dimensions[0]:
            return 0
        if self.player[0][1] < 0 or self.player[0][1] > self.dimensions[1]:
            return 0
        else:
            return 1

    def define_start_point(self):
        while 1:
            x = random.randint(0, self.dimensions[0])
            y = random.randint(0, self.dimensions[1])
            if (x, y) not in self.allocated_positions:
                if self.check_if_border(x, y):
                    return [(x, y)]

    def alocate_wood(self):
        allocated_wood = []
        while self.actual_wood >= 0:
            x = random.randint(0, self.dimensions[0])
            y = random.randint(0, self.dimensions[1])

            if self.check_position(x, y):
                print("Alocated wood in ", x, y)
                self.allocated_positions.append((x,y))
                allocated_wood.append((x,y))
                self.actual_wood -= 1
        return allocated_wood

    def alocate_rock(self):
        allocated_rock = []
        while self.actual_rock >= 0:
            x = random.randint(0, self.dimensions[0])
            y = random.randint(0, self.dimensions[1])

            if self.check_position(x, y):
                print("Alocated rock in ", x, y)
                self.allocated_positions.append((x,y))
                allocated_rock.append((x,y))
                self.actual_rock -= 1
        return allocated_rock

    def alocate_food(self):
        allocated_food = []
        while self.actual_food >= 0:
            x = random.randint(0, self.dimensions[0])
            y = random.randint(0, self.dimensions[1])

            if self.check_position(x, y):
                print("Alocated food in ", x, y)
                self.allocated_positions.append((x,y))
                allocated_food.append((x,y))
                self.actual_food -= 1
        return allocated_food

    def move_player(self, d):
        x = self.player[0][0]
        y = self.player[0][1]
        pos = None

        if d == 'r':
            pos = [(x + 1, y)]
        if d == 'l':
            pos = [(x - 1, y)]
        if d == 'u':
            print("Sobe")
            pos = [(x, y - 1)]
        if d == 'd':
            pos = [(x, y + 1)]

        self.player = pos
        # if pos not in self.walls:
        #     self.player = pos

        # if pos == self.goal:
        #     print("You made it to the end!")

    def check_position(self, x, y):
        return 1 if (x, y) not in self.allocated_positions else 0

    def draw_grid(self, width=2):
        for y in range(self.dimensions[1]-1):
            for x in range(self.dimensions[0]-1):

                if (x, y) in self.allocated_wood: # BROWN
                    symbol = [0, 25, 51]
                elif (x, y) in self.allocated_rock: # CINZA
                    symbol = [128, 128, 128]
                elif (x, y) in self.allocated_food: # RED
                    symbol = [0, 0, 255]
                elif (x, y) in self.player: # BLUE
                    symbol = [255, 0, 0]
                else:
                    symbol = [0, 0, 0]
                self.grid[x, y] = symbol

        cv2.imshow("grid", self.grid)

    def check_if_border(self, x, y):
        if x == 0 or x == self.dimensions[0]:
            return 1
        if y == 0 or y == self.dimensions[1]:
            return 1

        return 0


# def clear():
#     subprocess.Popen("cls" if platform.system() == "Windows" else "clear", shell=True)
#     time.sleep(.01)

import os
import time
import cv2

def main():
    g = MapGrid(20, 20)
    ran = ["r", "l", "u", "d"]

    while g.check_if_player_out():
        time.sleep(0.2)
        key = ran[random.randint(0, len(ran)-1)]
        g.move_player(key)
        os.system("clear")
        g.draw_grid()

if __name__ == '__main__':
    main()