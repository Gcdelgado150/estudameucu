import cv2
import numpy as np
from random import randrange
import matplotlib.pyplot as plt

def value_from_action(action):
  color_for_action1 = [a for a in range(50)]
  color_for_action2 = [a for a in range(51,101)]
  color_for_action3 = [a for a in range(102,152)]
  color_for_action4 = [a for a in range(153,203)]
  color_for_action5 = [a for a in range(204,254)]
  rando = randrange(50)
  
  if action == 1:
    return color_for_action1[rando]
  elif action == 2:
    return color_for_action2[rando]
  elif action == 3:
    return color_for_action3[rando]
  elif action == 4:
    return color_for_action4[rando]
  elif action == 5:
    return color_for_action5[rando]
  

def find_stats(your_status, enemy_status):
  if your_status[0] == enemy_status[0]:
    ls = "Same Life "
  elif your_status[0] > enemy_status[0]:
    ls = "Greater Life "
  else:
    ls = "Lower Life "
    
  if your_status[1] == enemy_status[1]:
    la = "Same Atk "
  elif your_status[1] > enemy_status[1]:
    la = "Greater Atk "
  else:
    la = "Lower Atk "
    
  if your_status[2] == enemy_status[2]:
    ld = "Same Def "
  elif your_status[2] > enemy_status[2]:
    ld = "Greater Def "
  else:
    ld = "Lower Def "
    
  if your_status[3] == enemy_status[3]:
    lf = "Same Focus "
  elif your_status[3] > enemy_status[3]:
    lf = "Greater Focus "
  else:
    lf = "Lower Focus "
    
  if your_status[4] == enemy_status[4]:
    le = "Same Evasion"
  elif your_status[4] > enemy_status[4]:
    le = "Greater Evasion"
  else:
    le = "Lower Evasion"
    
    
  comparison = ls + la + ld + lf + le
  color = all_states.index(comparison)
  
  return color # is a int from 0 to 240
  
  
States_for_life = ["Same Life ", "Greater Life ", "Lower Life "]
States_for_atk  = ["Same Atk ", "Greater Atk ", "Lower Atk "]
States_for_def  = ["Same Def ", "Greater Def ", "Lower Def "]
States_for_focus  = ["Same Focus ", "Greater Focus ", "Lower Focus "]
States_for_evasion  = ["Same Evasion", "Greater Evasion", "Lower Evasion"]
all_states = []

for a in range(3):
  for b in range(3):
    for c in range(3):
      for d in range(3):
        for e in range(3):
          all_states.append(States_for_life[a] + States_for_atk[b]+ States_for_def[c]+ States_for_focus[d]+ States_for_evasion[e])
		  

		  
B_stats = [100,10,10,10,10]
B1_stats = [100,10,10,10,10]

rounds = 100
dimensions1 = int(np.ceil(rounds/2))
dimensions2 = int(np.floor(rounds/2))

img2 = np.zeros([dimensions1,dimensions2,3],dtype=np.uint8)

# First 5 rows are specified previously depending on which player have started
first_player = False
for i in range(dimensions1):    # for every col:
  for j in range(dimensions2):
    if j < 5:
      if first_player:
        img2[i,j] = [255, 255, 255] # set the colour accordingly
      else:
        img2[i,j] = [0, 0, 0] # set the colour accordingly
    else:
      action = randrange(5) + 1
      img2[i,j] = [255, value_from_action(action), find_stats(B_stats, B1_stats)] # set the colour accordingly

      
plt.imshow(img2)
plt.show()


from abc import ABC, abstractmethod
import random

class BaseCreature(ABC):
  def __init__(self, name, atk, defense, life, focus, evasion):
      self.max_life = 100
      self.__name = name
      self.atk = atk
      self.defense = defense
      self.life = life
      self.focus = focus
      self.evasion = evasion

  def get_stats(self):
    return (self.life, self.atk, self.defense, self.focus, self.evasion)
  
  def get_life(self):
      return self.life

  def get_name(self):
      return self.__name

  def show_life(self):
      print(self.__name + " life is " + str(self.life))

  def show_name(self):
      print(self.__name)

  def define_action(self):
      # between 5 actions
      # atack, defense, focus, heal, increase_atk
      actions_amount = 5
      self.action = random.randint(1, actions_amount)
      
      return self.action

  def take_dmg(self, value):
      evade = random.randrange(100)/100

      if evade > self.evasion:
#           print("Damage taken: " + str(value-self.defense))
          if value-self.defense > 0:
              self.life = self.life - (value-self.defense)

  def deal_dmg(self, enemy):
      if isinstance(enemy, BaseCreature):
#           print(self.__name + " choose to deal damage!({})".format(self.atk-enemy.defense))
          enemy.take_dmg(self.atk)

  def increase_defense(self):
#       print(self.__name + " choose to increase the defense! ({})".format(self.defense*1.05))
      self.defense = self.defense*1.05

  def increase_focus(self):
      if self.evasion < 0.7:
#           print(self.__name + " choose to increase the focus!({})".format(self.evasion*1.05))
          self.evasion = self.evasion*1.05

  def increase_atk(self):
#       print(self.__name + " choose to increase the attack!({})".format(self.atk*1.05))
      self.atk = self.atk*1.05

  def heal(self):
      # base heal = 2
      heal = 2
      if self.life < self.max_life:
#           print(self.__name + " choose to heal!({})".format(self.life + heal))
          self.life = self.life + heal

  def act(self, enemy):
      if self.action == 1:
          self.deal_dmg(enemy)
      elif self.action == 2:
          self.increase_defense()
      elif self.action == 3:
          self.increase_focus()
      elif self.action == 4:
          self.heal()
      elif self.action == 5:
          self.increase_atk()
      else:
          print("Action choosed not avaiable")

          
          
class Behemoot(BaseCreature):
  def __init_(self, name, atk, defense, life, focus, evasion):
    self.__name = name
    super().__init__(name, atk, defense, life, focus, evasion)
	
	
for it in range(100):
  B = Behemoot("B", atk=10, defense=10, life=100, focus=10, evasion=0.5)
  B1 = Behemoot("B1", atk=10, defense=10, life=100, focus=10, evasion=0.5)


  B_action_history = []
  B_stats_history = []

  B1_action_history = []
  B1_stats_history = []

  rounds = 0

  while (B.get_life() > 0 and B1.get_life() > 0):
    B_action_history.append(B.define_action())
    B_stats_history.append(B.get_stats())
    B1_action_history.append(B1.define_action())
    B1_stats_history.append(B1.get_stats())

    B.act(B1)
    B1.act(B)

  #   B.show_life()
  #   B1.show_life()

    rounds = rounds + 1

  B1_wins = False
  B_wins = False

  if B.get_life() > B1.get_life():
    B_wins = True
    print(B.get_name() + " wins!")
  else:
    B1_wins = True
    print(B1.get_name() + " wins!")
	
path_win = "winner/"
path_los = "loser/"

# Image for B (first)
dimensions1 = int(np.ceil(np.sqrt(rounds)))
dimensions2 = int(np.floor(np.sqrt(rounds)))

img2 = np.zeros([dimensions1,dimensions2,3],dtype=np.uint8)

# First 5 rows are specified previously depending on which player have started
first_player = True
count = 0

for i in range(dimensions1):    # for every col:
  for j in range(dimensions2):
    if j < 2:
      if first_player:
        img2[i,j] = [255, 255, 255] # set the colour accordingly
      else:
        img2[i,j] = [0, 0, 0] # set the colour accordingly
    else:
      img2[i,j] = [255, value_from_action(B_action_history[count]), find_stats(B_stats_history[count], B1_stats_history[count])] # set the colour accordingly
      count = count + 1

if B_wins:
  b_path = path_win + "B_{}.png".format(str(it))
else:
  b_path = path + "B_{}.png".format(str(it))

plt.savefig(b_path)

# Image for B (second)
dimensions1 = int(np.ceil(np.sqrt(rounds)))
dimensions2 = int(np.floor(np.sqrt(rounds)))

img2 = np.zeros([dimensions1,dimensions2,3],dtype=np.uint8)

# First 5 rows are specified previously depending on which player have started
first_player = False
count = 0

for i in range(dimensions1):    # for every col:
  for j in range(dimensions2):
    if j < 2:
      if first_player:
        img2[i,j] = [255, 255, 255] # set the colour accordingly
      else:
        img2[i,j] = [0, 0, 0] # set the colour accordingly
    else:
      img2[i,j] = [255, value_from_action(B1_action_history[count]), find_stats(B1_stats_history[count], B_stats_history[count])] # set the colour accordingly
      count = count + 1

if B1_wins:
  b1_path = path_win + "B1_{}.png".format(str(it))
else:
  b1_path = path + "B1_{}.png".format(str(it))

plt.imshow()
plt.savefig(b1_path)