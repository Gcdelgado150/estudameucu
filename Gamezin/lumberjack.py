import numpy as np
import pyscreenshot as ImageGrab
import cv2
import time
import random
import pickle
import itertools
import os
import pyautogui
import mss

pyautogui.PAUSE = 0.01 # 100 clicks per second
class Movements():
    def __init__(self):
        self.last = "right"
        # Options for TREE position
        self.options = ["right", "left", "any"]
        self.speed = 0.05

    def action(self, action):
        key = self.options[action]
        if key == "right":
            pyautogui.typewrite(['left'], self.speed)
            self.last = "right"
        elif key == "left":
            pyautogui.typewrite(['right'], self.speed)
            self.last = "left"
        elif key == "any" and self.last == "left":
            pyautogui.typewrite(['right'], self.speed)
        elif key == "any" and self.last == "right":
            pyautogui.typewrite(['left'], self.speed)

        time.sleep(0.08)

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


player = Movements()
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

# Screenshot window
X, Y, H, W = 2300, 95, 600, 655

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

def screenshot(debug=False):
    if debug:
        c = 0
        while(True):
            img = np.asarray(sct.grab(monitor))
            img = img[:,:, 0]
            print("{}".format(c), get_state(img))
            cv2.imshow("title", img)
            cv2.imwrite("screenshot/{}.png".format(c), img)
            c += 1
            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                return 0

            time.sleep(0.05)

    img = np.asarray(sct.grab(monitor))

    return img[:,:, 0]

def check_lost(img):
    """Check value for arrow as lost state"""
    return -LOST_PENALTY if img[319, 537] < 200 else DIDNT_LOST_REWARD

def f_pixel(pixel):
    """1 for TREE, 0 for NOTHING"""
    return 1 if pixel < 200 else 0

def get_state(img):
    grid = 100
    first_ = 32
    rightX_coord = 395
    leftX_coord = 223
    state = []

    for i in range(3):
        pixel_left = img[first_+grid*i, leftX_coord]
        state.append(f_pixel(pixel_left))

    for i in range(3):
        pixel_right = img[first_+grid*i, rightX_coord]
        state.append(f_pixel(pixel_right))

    return tuple(state)

def reset_env():
    print("Reset")
    playX = 319
    playY = 537
    pyautogui.moveTo(X+playX, Y+playY)
    pyautogui.click()
    time.sleep(0.3)

def game(EPSILON):
    q_table = get_q_table()
    episode_rewards = []

    for episode in range(TOTAL_EPISODES):
        if episode % SHOW_EVERY == 0:
            print(f"on #{episode}, epsilon is {EPSILON}")
            print(f"{SHOW_EVERY} ep mean: {np.mean(episode_rewards[-SHOW_EVERY:])}")
            show = True
        else:
            show = False

        episode_reward = 0
        img = screenshot()

        if check_lost(img) == -LOST_PENALTY:
            reset_env()
            player.action(1) # Perform a right click at the start

        for i in range(100):
            img = screenshot()

            obs = get_state(img)
            # print("State before action: {}".format(obs))
            if np.random.random() > EPSILON:
                action = np.argmax(q_table[obs]) # GET THE ACTION
            else:
                # print("random move")
                action = np.random.randint(0, 3)

            # Take the action!
            player.action(action)

            img = screenshot()
            reward = check_lost(img)
            new_obs = get_state(img)
            # print("State after action: {}".format(new_obs))

            current_q = q_table[obs][action]
            max_future_q = np.max(q_table[new_obs])

            if reward == DIDNT_LOST_REWARD:
                new_q = reward
            else:
                new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)

            q_table[obs][action] = new_q

            episode_reward += reward
            if reward == -LOST_PENALTY:
                reset_env()

        if not check_lost(img):
            # If we havent lost, we have to wait for it to happens
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

# try:
#     game(EPSILON)
# except KeyboardInterrupt:
#     exit()

def test_verify():
    while 1:
        printscreen = np.array(ImageGrab.grab(bbox=(X, Y, X+H, Y+W)))
        img = cv2.cvtColor(printscreen, cv2.COLOR_RGB2GRAY)

        cv2.imshow("img", img)
        cv2.moveWindow("img", 1300, 0)

        k = cv2.waitKey(33)
        if k == 113:
            cv2.destroyAllWindows()
            break

# test_verify()

# screenshot(True)

import json
jpath = "trees.json"
with open(jpath, "r") as f:
    js = json.load(f)

SUM4TREE = 5540 
def f_pixel2(stream):
    if sum(stream) == SUM4TREE:
        print("Tree")
        return 1
    return 0

  
def game2():
    grid = 100
    first_ = js["posicoes"]["Y"]["third_grid"]
    rightX_coord = js["posicoes"]["X"]["right"]
    leftX_coord = js["posicoes"]["X"]["left"]
    actions = []

    if check_lost(screenshot()) == -LOST_PENALTY:
        reset_env()

    while(True):
        left = []
        right = []
        img = screenshot()
        for i in range(3):
            INICIALY = first_ + grid*i
            left.append(f_pixel2(img[INICIALY:INICIALY + 40 , leftX_coord+50]))

        for i in range(3):
            INICIALY = first_ + grid*i
            right.append(f_pixel2(img[INICIALY:INICIALY + 40, rightX_coord+50]))

        for i in range(3):
            # Get First action
            if left[i]:
                actions.append(1)
                actions.append(1)
            elif right[i]:
                actions.append(0)
                actions.append(0)
            else:
                actions.append(2)
                actions.append(2)

        for i in range(len(actions)):
            player.action(actions[0])
            actions.pop(0)

        if check_lost(screenshot()) == -LOST_PENALTY:
            reset_env()
try:
    game2()
except KeyboardInterrupt:
    exit()

# First grid level
INICIALY = 210
INICIALX = 168



def test_verify2():
    c=0
    while 1:
        printscreen = np.array(ImageGrab.grab(bbox=(X, Y, X+H, Y+W)))
        img = printscreen[:,:,0]
        
        
        crop = img[INICIALY:INICIALY+40, INICIALX+50]
        soma = sum(crop)
        
        print(soma)
        
        cv2.imshow("img", img)
        cv2.imshow("img2", crop)
        cv2.moveWindow("img", 1300, 0)
        cv2.moveWindow("img2", 900, 0)
        
        cv2.imwrite("screenshot/2/{}.png".format(c), img)
        c+=1
        k = cv2.waitKey(33)
        if k == 113:
            cv2.destroyAllWindows()
            break
            
# test_verify2()