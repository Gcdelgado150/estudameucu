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


monitor_number = 1
sct = mss.mss()
mon = sct.monitors[monitor_number]

monitor = {
    "top": mon["top"] + 100,  # 100px from the top
    "left": mon["left"] + 375,  # 100px from the left
    "width": 600,
    "height": 650,
    "mon": monitor_number,
}

# Constants
TOTAL_EPISODES = 35000
N_ACTIONS = 3
EPSILON = 0.8
EPS_DECAY = 0.9998
LEARNING_RATE = 0.1
DISCOUNT = 0.95
SHOW_EVERY = 1000

LOST_PENALTY = 30
DIDNT_LOST_REWARD = 1
MAX_POINTS = 1000

def get_json():
    jpath = "trees.json"
    with open(jpath, "r") as f:
        js = json.load(f)
    return js

js = get_json()

# Map configurations
X, Y, H, W = 2300, 95, 600, 655
LOSTY, LOSTX = 537, 319
SUM4TREE = 4170
leftX_coord = js["posicoes"]["X"]["left"]
rightX_coord = leftX_coord + 170
firstY = js["posicoes"]["Y"]["third_grid"]
grid = 100

# Q_Table configurations
def increase_vec(listA, vec):
    perm = itertools.permutations(listA)
    for i in list(perm):
        vec.append(i)

    return vec

def create_q_table():
    vec = []

    vec = increase_vec([0,0,0,0,0,0], vec)
    vec = increase_vec([0,0,0,0,0,1], vec)
    vec = increase_vec([0,0,0,0,1,1], vec)
    vec = increase_vec([0,0,0,1,1,1], vec)
    vec = increase_vec([0,0,1,1,1,1], vec)
    vec = increase_vec([0,1,1,1,1,1], vec)
    vec = increase_vec([1,1,1,1,1,1], vec)
    vec = list(set(vec))

    # All posibles combinations are:
    q_table = {}
    for i in range(len(vec)):
        t = tuple(vec[i])
        q_table[t] = [np.random.uniform(-5, 0) for i in range(N_ACTIONS)]

    return q_table

def get_q_table():
    start_q_table = "q_table.pickle"
    if os.path.exists(start_q_table):
        with open(start_q_table, "rb") as f:
            q_table = pickle.load(f)
    else:
        q_table = create_q_table()

    return q_table

def save_q_table(q_table):
    start_q_table = "q_table.pickle"
    with open(start_q_table, "wb") as f:
        pickle.dump(q_table, f)
    f.close()

def format_pixel(pixel):
    pixel = -pixel if pixel < 0 else pixel
    pixel = 255 if pixel > 255 else pixel
    return int(pixel)

def get_table_grid(q_table):
    gridd = np.zeros((8,8,3))

    states = []
    for key, value in q_table.items():
        states.append([format_pixel(x*10) for x in value])

    c = 0
    for i in range(gridd.shape[0]):
        for j in range(gridd.shape[1]):
            gridd[i][j][:] = states[c]
            c += 1
    return gridd

pyautogui.PAUSE = 0.01 # 100 clicks per second
class Movements():
    def __init__(self):
        self.last = "right"
        # Options for TREE position
        self.options = ["right", "left", "any"]

    def action(self, action, sleep=0.2, speed=0.1):
        key = self.options[action]
        if key == "right":
            pyautogui.typewrite(['left'], speed)
            self.last = "right"
        elif key == "left":
            pyautogui.typewrite(['right'], speed)
            self.last = "left"
        elif key == "any" and self.last == "left":
            pyautogui.typewrite(['right'], speed)
        elif key == "any" and self.last == "right":
            pyautogui.typewrite(['left'], speed)

        # time.sleep(sleep)

player = Movements()

def screenshot(debug=False):
    img = np.asarray(sct.grab(monitor))
    return img[:,:, 0]

def f_stream(stream):
    return 1 if sum(stream) == SUM4TREE else 0

def get_state(img):
    state = []
    for i in range(3):
        pixel_left = img[firstY+grid*i:firstY+grid*i+40, leftX_coord+50]
        state.append(f_stream(pixel_left))

    for i in range(3):
        pixel_right = img[firstY+grid*i:firstY+grid*i+40, rightX_coord+50]
        state.append(f_stream(pixel_right))

    return tuple(state)

def check_lost(img):
    """Check value for arrow as lost state"""
    return -LOST_PENALTY if img[LOSTY, LOSTX] < 200 else DIDNT_LOST_REWARD

def reset_env():
    # print("Reset")
    pyautogui.moveTo(X+LOSTX, Y+LOSTY)
    pyautogui.click()
    time.sleep(0.3)

def game(EPSILON):
    q_table = get_q_table()
    episode_rewards = []

    for episode in range(TOTAL_EPISODES):
        print(episode, "/", TOTAL_EPISODES)
        if episode % SHOW_EVERY == 0:
            print(f"on #{episode}, epsilon is {EPSILON}")
            print(f"{SHOW_EVERY} ep mean: {np.mean(episode_rewards[-SHOW_EVERY:])}")
            cv2.imwrite("{}.png".format(episode), get_table_grid(q_table))

        episode_reward = 0
        img = screenshot()

        if check_lost(img) == -LOST_PENALTY:
            reset_env()
            player.action(1) # Perform a right click at the start

        start = time.time()
        for i in range(100):
            img = screenshot()
            obs = get_state(img)

            if np.random.random() > EPSILON:
                action = np.argmax(q_table[obs]) # GET THE ACTION
            else:
                print("random move")
                action = np.random.randint(0, 3)

            # Take the action!
            player.action(action, 0.5)

            # After the minisleep, lets check the update in environment
            # (PROBABLY THIS THING HASN'T CHANGE - because it is not enough time)
            # THE NEXT ACTION SHOULD BE BASED ON AROUND 3 STEPS LATER
            # ENOUGH TIME FOR ENVIRONMENT TO SETTLE DOWN
            img = screenshot()
            reward = check_lost(img)
            new_obs = get_state(img)

            current_q = q_table[obs][action]
            max_future_q = np.max(q_table[new_obs])

            # print((time.time() - start)*100)
            if reward == DIDNT_LOST_REWARD:
                new_q = reward
            else:
                new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)

            q_table[obs][action] = new_q

            episode_reward += reward
            if reward == -LOST_PENALTY:
                start = time.time()
                save_q_table(q_table)
                reset_env()

        if not check_lost(img):
            time.sleep(5)

        reset_env()
        episode_rewards.append(episode_reward)
        EPSILON *= EPS_DECAY
        save_q_table(q_table)

    moving_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY,))/SHOW_EVERY, mode='valid')

    plt.plot([i for i in range(len(moving_avg))], moving_avg)
    plt.ylabel(f"Reward {SHOW_EVERY}ma")
    plt.xlabel("episode #")
    plt.show()

    save_q_table(q_table)

try:
    game(EPSILON)
except KeyboardInterrupt:
    exit()