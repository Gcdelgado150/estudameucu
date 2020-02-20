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
import pytesseract

def get_json():
    jpath = "train.json"
    with open(jpath, "r") as f:
        js = json.load(f)
    return js

js = get_json()

# Monitor configs
monitor_number = 1

EPSILON = js["general"]["EPSILON"]
EPS_DECAY = js["general"]["EPS_DECAY"]
LEARNING_RATE = js["general"]["LEARNING_RATE"]
DISCOUNT = js["general"]["DISCOUNT"]
N_ACTIONS = js["general"]["N_ACTIONS"]
N_PREVIOUS_ACTIONS = js["general"]["N_PREVIOUS_ACTIONS"]
N_STATES = js["general"]["N_STATES"]

# Constants
TOTAL_EPISODES = (2**N_STATES)*100
SHOW_EVERY = 500
MAX_ACTIONS = 100

# Rewards
MAX_REWARD = js["rewards"]["MAX_REWARD"]
# The punish has to be greater than the total amount that it could do in a episode
LOST_PUNISH = -(js["rewards"]["LOST_PUNISH_multipler"]*MAX_ACTIONS)

# Map configurations
X = js["map_configs"]["X"]
Y = js["map_configs"]["Y"]
H = js["map_configs"]["H"]
W = js["map_configs"]["W"]
LOSTY = js["map_configs"]["LOSTY"]
LOSTX = js["map_configs"]["LOSTX"]

# Tree configs
SUM4TREE = js["tree_configs"]["SUM4TREE"]
leftX_coord = js["tree_configs"]["X"]
rightX_coord = leftX_coord + 170
firstY = js["tree_configs"]["Y"]
grid = js["tree_configs"]["VERTICAL_GRID"]
hs = js["tree_configs"]["horizontal_size"]
vs = js["tree_configs"]["vertical_size"]
ts_config = ("-l eng --psm 10 --oem 3 -c tessedit_char_whitelist=0123456789")
# Loops elapsed for the actions
TIMESTAMP = 10

# Configure sleep time for after-move, and the decay-rate
# As time passes by, the movements have to be faster
# This decay is configured so that after 10k interactions
# It will approximate to 0

sleep_decay = 0.9996

q_table_name = "q_table_lumber.pickle"

def increase_vec(listA, vec):
    perm = itertools.permutations(listA)
    for i in list(perm):
        vec.append(i)

    return vec

class Lumber():
    def __init__(self):
        self.frame_counter = -1
        self.times = 0
        self.click_speed = 0.001
        self.last_moves = ["Right"]*N_PREVIOUS_ACTIONS

        # Monitor configurations
        self.sct = mss.mss()
        mon = self.sct.monitors[monitor_number]

        self.monitor = {
            "top": mon["top"] + 100,  # 100px from the top
            "left": mon["left"] + 375,  # 100px from the left
            "width": 600,
            "height": 650,
            "mon": monitor_number,
        }
        self.get_env()
        # Player configurations
        # Score is based on time
        self.score = 0
        self.max_score = 0
        self.actions = ["Left", "Right"]
        self.q_table = self.get_q_table()

    def generate_q_table(self):
        """
        States / Actions
        3 TREE POSITIONS AT LEFT : 0 for not tree - 1 for tree
        3 TREE POSITIONS AT RIGHT: 0 for not tree - 1 for tree
        4 FOR LAST 4 MOVEMENTS : 0 for LEFT - 1 for RIGHT
        """
        N_TREE_POSITIONS = 6
        vec = []
        for i in range(N_TREE_POSITIONS+N_PREVIOUS_ACTIONS+1):
            new_vec = [0]*(N_TREE_POSITIONS+N_PREVIOUS_ACTIONS-i) + [1]*(i)
            vec = increase_vec(new_vec, vec)
        vec = list(set(vec))

        # All posibles combinations are:
        q_table = {}
        for i in range(len(vec)):
            t = tuple(vec[i])
            q_table[t] = [int(np.random.uniform(-10, 2)) for i in range(N_ACTIONS)]

        return q_table

    def get_q_table(self):
        start_q_table = q_table_name
        if os.path.exists(start_q_table):
            with open(start_q_table, "rb") as f:
                q_table = pickle.load(f)
            print("Loaded q_table...")
            time.sleep(1)
        else:
            q_table = self.generate_q_table()
            print("Generated q_table...")
            time.sleep(1)

        return q_table
    
    def save_q_table(self):
        with open(q_table_name, "wb") as f:
            pickle.dump(self.q_table, f)
        f.close()
    
    def restart_env(self):
        self.score = 0
        self.frame_counter = -1
        self.times = 0
        self.last_moves = ["Right"]*N_PREVIOUS_ACTIONS
        
        # Get score and compare it to max_score
        try:
            roi = self.img[140:180, 240:305]
            tesse = pytesseract.image_to_string(roi, config=ts_config)
            max_score = int(tesse)
            if max_score > self.max_score:
                self.max_score = max_score
                print("New max score: ", self.max_score)
        except ValueError:
            print(".. ", tesse)
        
        pyautogui.moveTo(X+LOSTX, Y+LOSTY)
        pyautogui.click()

    def get_env(self):
        start = time.time()
        self.frame_counter += 1
        self.img = np.asarray(self.sct.grab(self.monitor))[:,:, 0]
        end = time.time()
        self.times += (end-start)
        self.fps = self.frame_counter/self.times

    def get_just_env(self):
        self.img = np.asarray(self.sct.grab(self.monitor))[:,:, 0]
        return self.img

    def get_action(self, obs):
        if np.random.random() > EPSILON:
            action = np.argmax(self.q_table[obs]) # GET THE ACTION
        else:
            action = np.random.randint(0, N_ACTIONS)

        return action

    def move(self, idx_act, sleep):
        action = self.actions[idx_act]
        if action == "Right":
            pyautogui.typewrite(['Right'], self.click_speed)
            self.last_moves.pop(0)
            self.last_moves.append("Right")
            # print(self.last_moves[-1])
        elif action == "Left":
            pyautogui.typewrite(['Left'], self.click_speed)
            self.last_moves.pop(0)
            self.last_moves.append("Left")
            # print(self.last_moves[-1])

        time.sleep(sleep)

    def get_obs(self):
        state = []
        for i in range(3):
            pixel_left = self.img[firstY+grid*i:firstY+grid*i+vs, leftX_coord+int(hs/2)]
            state.append(Lumber.f_stream(pixel_left))

        for i in range(3):
            pixel_right = self.img[firstY+grid*i:firstY+grid*i+vs, rightX_coord+int(hs/2)]
            state.append(Lumber.f_stream(pixel_right))

        for i in range(N_PREVIOUS_ACTIONS):
            state.append(0 if self.last_moves[i] == "Left" else 1)

        return tuple(state)

    def get_reward(self):
        self.get_just_env()
        return self.check_lost()

    def check_lost(self):
        """Check value for arrow as lost state"""
        return LOST_PUNISH if self.img[LOSTY, LOSTX] < 200 else MAX_REWARD

    @staticmethod
    def f_stream(stream):
        return 1 if sum(stream) == SUM4TREE else 0

    @staticmethod
    def increase_vec(listA, vec):
        perm = itertools.permutations(listA)
        for i in list(perm):
            vec.append(i)

        return vec

def game(EPSILON):
    L = Lumber()
    sleep_time = 0.5
    episode_rewards = []
    
    for episode in range(TOTAL_EPISODES):
        episode_reward = 0
        L.get_env()

        if episode+1 % SHOW_EVERY == 0:
            os.system("clear")
            print("FPS: ", L.fps)
            print(f"on #{episode}, epsilon is {EPSILON}")
            print(f"{SHOW_EVERY} ep mean: {np.mean(episode_rewards[-SHOW_EVERY:])}")

        for i in range(MAX_ACTIONS):
            L.get_env()
            if i % TIMESTAMP == 0: # Take the action if TIMESTAMP has passed
                # Get the observation, get and execute the action for that obs
                obs = L.get_obs()
                action = L.get_action(obs)
                L.move(action, sleep=sleep_time)

                # In this we printscreen again
                reward = L.get_reward()
                new_obs = L.get_obs()

                current_q = L.q_table[obs][action]
                max_future_q = np.max(L.q_table[new_obs])

                if reward == MAX_REWARD:
                    new_q = reward
                else:
                    new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)

                L.q_table[obs][action] = new_q
                episode_reward += reward

                if L.check_lost() == LOST_PUNISH:
                    L.save_q_table()
                    break

        if not L.check_lost():
            # Rare condition where at the end of the loop we did not lost yet.
            time.sleep(5)

        episode_rewards.append(episode_reward)
        EPSILON *= EPS_DECAY
        sleep_time *= sleep_decay
        L.restart_env()

    moving_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY,))/SHOW_EVERY, mode='valid')

    plt.plot([i for i in range(len(moving_avg))], moving_avg)
    plt.ylabel(f"Reward {SHOW_EVERY}ma")
    plt.xlabel("episode #")
    plt.savefig("Lumber_episodes.png")

    L.save_q_table()

# game(EPSILON)

def get_only_states():
    L = Lumber()
    c = 0
    
    while True:
        L.get_env()
        obs = L.get_obs()
        action = L.get_action(obs)
        print(obs, action)
        
        cv2.imshow("image", L.img)
        cv2.imwrite("screenshots/{}-{}-{}.png".format(c, obs, action), L.img)
#         cv2.waitKey(0)
        time.sleep(1)
        c += 1

get_only_states()