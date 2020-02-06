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

        time.sleep(1)

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
SHOW_EVERY = 3000
LOST_PENALTY = 25
DIDNT_LOST_REWARD = 5
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
    img = np.asarray(sct.grab(monitor))
    if debug:
        cv2.imshow("title", img)
        cv2.waitKey(0)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            return 0
    return img

def check_lost(img):
    """Check value for arrow as lost state"""
    return -LOST_PENALTY if img[318, 542] == 125 else DIDNT_LOST_REWARD

def f_pixel(pixel):
    """0 for TREE, 1 for NOTHING"""
    return 0 if pixel < 200 else 1

def get_state(img):
    grid = 51
    first_ = 45
    rightX_coord = 390
    leftX_coord = 219
    state = []

    for i in range(3):
        pixel_right = img[rightX_coord, first_+grid*i]
        state.append(f_pixel(pixel_right))

    for i in range(3):
        pixel_left = img[leftX_coord, first_+grid*i]
        state.append(f_pixel(pixel_left))

    return tuple(state)

def reset_env():
    playX = 318
    playY = 542
    pyautogui.moveTo(X+playX, Y+playY)
    pyautogui.click()
    time.sleep(0.3)

# TODO: REFACTOR PIXELS, BECAUSE WE CHANGE SCREENSHOT METHOD
def game(EPSILON):
    q_table = get_q_table()
    episode_rewards = []

    for episode in range(TOTAL_EPISODES):
        print("Running {}/{}".format(episode, TOTAL_EPISODES))
        episode_reward = 0
        img = cv2.cvtColor(screenshot(), cv2.COLOR_RGB2GRAY)

        if check_lost(img):
            reset_env()
            player.action(1) # Perform a right click at the start

        for i in range(MAX_POINTS):
            img = cv2.cvtColor(screenshot(), cv2.COLOR_RGB2GRAY)
            cv2.imwrite("screenshots/{}_antes.png".format(i), img)

            obs = get_state(img)
            print("State before action: {}".format(obs))
            if np.random.random() > EPSILON:
                action = np.argmax(q_table[obs]) # GET THE ACTION
            else:
                print("random move")
                action = np.random.randint(0, 3)
            # Take the action!
            player.action(action)

            img = cv2.cvtColor(screenshot(), cv2.COLOR_RGB2GRAY)
            cv2.imwrite("screenshots/{}_depois.png".format(i), img)
            reward = check_lost(img)

            new_obs = get_state(img)
            print("State after action: {}".format(new_obs))
            max_future_q = np.max(q_table[new_obs])
            current_q = q_table[obs][action]

            if reward == DIDNT_LOST_REWARD:
                new_q = reward
            else:
                new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
                reset_env()

            q_table[obs][action] = new_q

            episode_reward += reward
            print(reward)
            if reward == -LOST_PENALTY:
                break

        if not check_lost(img):
            # If we havent lost, we have to wait for it to happens
            time.sleep(5)

        reset_env()
        episode_rewards.append(episode_reward)
        EPSILON *= EPS_DECAY

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