import os
import json
import mss
import numpy as np
import pyautogui
import time
import cv2
import itertools
import pickle
import random
import matplotlib.pyplot as plt

# Train Constants
map_dims = (30, 10)
TOTAL_EPISODES = (map_dims[0]*map_dims[1])**2
MAX_ACTIONS = 1000
SHOW_EVERY = 100
EPSILON = 0.8
EPS_DECAY = 0.9998
LEARNING_RATE = 0.1
DISCOUNT = 0.95

N_ACTIONS = 4

# Rewards
NOT_EARNED = -5 # Random move/not earnfull move
MAX_REWARD = 100 # Food gather
NOT_MOVED = -50 # Border crash

q_table_name = "q_table_C3.pickle"

class Field():
    def __init__(self, map_dims=(3,3)):
        # Definitions
        self.map_dims = map_dims
        self.actions = [0,1,2,3]
        self.q_table = self.get_q_table()
        
        # Positions
        self.player_pos = (0,0)
        self.previous_player_pos = self.player_pos
        self.food_pos = self.get_food_pos()
        
        # Variables
        self.movements = 0
        self.score = 0
        self.max_score = 0
        self.max_eps = 0

    def restart(self, eps):
        self.player_pos = (0,0)
        self.previous_player_pos = self.player_pos
        self.movements = 0
        self.food_pos = self.get_food_pos()
        
        self.score = 0
        self.render(eps, True)
    
    def get_food_pos(self):
        while True:
            i = random.randint(0, self.map_dims[0]-1)
            j = random.randint(0, self.map_dims[1]-1)

            if (i, j) != self.player_pos:
                return (i, j)
    
    def check_move(self, newX, newY):
        if newX < 0 or newY < 0:
            return self.player_pos
        if newX > self.map_dims[0]-1 or newY > self.map_dims[1]-1:
            return self.player_pos
        return newX, newY
    
    def move(self, action):
        self.movements += 1
        if action == self.actions[0]:
            self.previous_player_pos = self.player_pos
            self.player_pos = self.check_move(self.player_pos[0] - 1, self.player_pos[1])
        elif action == self.actions[1]:
            self.previous_player_pos = self.player_pos
            self.player_pos = self.check_move(self.player_pos[0], self.player_pos[1]+1)
        elif action == self.actions[2]:
            self.previous_player_pos = self.player_pos
            self.player_pos = self.check_move(self.player_pos[0] + 1, self.player_pos[1])
        elif action == self.actions[3]:
            self.previous_player_pos = self.player_pos
            self.player_pos = self.check_move(self.player_pos[0], self.player_pos[1]-1)
    
    def define_char(self, i, j):
        if self.player_pos == (i, j):
            return "P"
        if self.food_pos == (i, j):
            return "F"
        return "*"
    
    def render(self, eps, show=False):
        if self.player_pos == self.food_pos:
            self.score += 1
            self.food_pos = self.get_food_pos()

        os.system("clear")
        print(eps, "/", TOTAL_EPISODES)
        if show:
            print("_"*self.map_dims[0])
            for j in range(self.map_dims[1]-1, -1, -1):
                ch = ""
                for i in range(self.map_dims[0]):
                    ch += self.define_char(i, j)
                print(ch + "\n")
            print("_"*self.map_dims[0])
        print("Moves: {}".format(self.movements))
        print("Score: {}".format(self.score))

        if self.score >= self.max_score:
            self.max_score = self.score
            self.max_eps = eps

        print("Max score: {} at the {} episode".format(self.max_score, self.max_eps))

    def get_reward(self):
        if self.player_pos == self.food_pos:
            return MAX_REWARD
        elif self.player_pos == self.previous_player_pos:
            return NOT_MOVED
        else:
            return NOT_EARNED
        
    def generate_q_table(self):
        # The states will be (i, j) position of player and (i, j) pos of food
        p_p = [(i, j) for i in range(self.map_dims[0]) for j in range(self.map_dims[1])]

        vec_all = []
        # For each p pos we can have pos of food
        for p in p_p:
            for i in range(self.map_dims[0]):
                for j in range(self.map_dims[1]):
                    vec_all.append((p[0], p[1], i, j))

        q_table = {}
        for i in range(len(vec_all)):
            t = tuple(vec_all[i])
            q_table[t] = [np.random.uniform(-5, 0) for i in range(N_ACTIONS)]

        return q_table
    
    def get_q_table(self):
        start_q_table = q_table_name
        if os.path.exists(start_q_table):
            print("Loaded q_table...")
            time.sleep(1)
            with open(start_q_table, "rb") as f:
                q_table = pickle.load(f)
        else:
            print("Random q_table starts...")
            time.sleep(1)
            q_table = self.generate_q_table()

        return q_table
    
    def get_obs(self):
        return self.player_pos[0], self.player_pos[1], self.food_pos[0], self.food_pos[1]
       
def save_q_table(q_table):
    start_q_table = q_table_name
    with open(start_q_table, "wb") as f:
        pickle.dump(q_table, f)
    f.close()

# def format_pixel(pixel):
#     pixel = -pixel if pixel < 0 else pixel
#     pixel = 255 if pixel > 255 else pixel
#     return int(pixel)

# def get_table_grid(q_table):
#     gridd = np.zeros((8,8,3))

#     states = []
#     for key, value in q_table.items():
#         states.append([format_pixel(x*10) for x in value])

#     c = 0
#     for i in range(gridd.shape[0]):
#         for j in range(gridd.shape[1]):
#             gridd[i][j][:] = states[c]
#             c += 1
#     return gridd

def game(EPSILON):
    F = Field(map_dims)
    episode_rewards = []
    show_conf = True

    for episode in range(TOTAL_EPISODES):
        episode_reward = 0
        if episode > 0.9*TOTAL_EPISODES:
            show_conf = True
        
        F.render(episode, show=show_conf)
        
        for i in range(MAX_ACTIONS):
            obs = F.get_obs()

            if np.random.random() > EPSILON:
                action = np.argmax(F.q_table[obs]) # GET THE ACTION
            else:
                action = np.random.randint(0, 3)

            # Take the action!
            F.move(action)
            reward = F.get_reward()
            F.render(episode, show=show_conf)
            
            new_obs = F.get_obs()
            current_q = F.q_table[obs][action]
            max_future_q = np.max(F.q_table[new_obs])

            if reward == MAX_REWARD:
                new_q = reward
            else:
                new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)

            F.q_table[obs][action] = new_q
            episode_reward += reward
        
        print("Score: {}, Rewards: {}".format(F.score, episode_reward))
        F.restart(episode)
        episode_rewards.append(episode_reward)
        EPSILON *= EPS_DECAY
        
        if episode % SHOW_EVERY == 0:
            save_q_table(F.q_table)

    moving_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY,))/SHOW_EVERY, mode='valid')
    
    print("Max score achieved: {} at the {} episode".format(max(F.all_scores), np.argmax(F.all_scores)))
    plt.plot([i for i in range(len(moving_avg))], moving_avg)
    plt.ylabel(f"Reward {SHOW_EVERY}ma")
    plt.xlabel("episode #")
    plt.show()

    save_q_table(F.q_table)

try:
    game(EPSILON)
except KeyboardInterrupt:
    exit()
