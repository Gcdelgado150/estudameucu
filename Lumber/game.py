import pygame
import random
import os
import time
import neat
# import visualize
import pickle

WIN_WIDTH = 600
WIN_HEIGHT = 800
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("LumberJack")
STAT_FONT = pygame.font.SysFont("comicsans", 50)
END_FONT = pygame.font.SysFont("comicsans", 70)

gen = 0

bg_img = pygame.transform.scale(pygame.image.load("imgs/bg.png").convert_alpha(), (WIN_WIDTH, WIN_HEIGHT))
lumber_images = pygame.transform.scale2x(pygame.image.load("imgs/lumber.png"))
tree_img = pygame.transform.scale2x(pygame.image.load("imgs/lumber.png"))
base_img = pygame.transform.scale2x(pygame.image.load("imgs/base.png").convert_alpha(), ())
class Lumber:
    def __init__(self, x, y, move=250):
        self.x = x # X position have only to options
        self.max_x = x
        self.y = y # Y position will always be equal
        self.move = move

    def move(self):
        """ Move is determine its sprites even when it does not change pos"""
        pass

    def switch(self):
        if self.x == self.max_x:
            self.x -= self.move
        elif self.x == self.max_x - self.move:
            self.x += self.mov

    def draw(self):
        pass

    def get_mask(self):
        pass

class Tree():
    """Tree object"""
    GAP = 200
    VEL = 5

    def __init__(self, y):
        self.y = y
        self.HEIGHT = 0

        # Top and bottom of the tree
        self.top = 0
        self.bottom = 0

        self.TREE_LEFT = pygame.transform.flip(tree_img, True, False)
        self.TREE_RIGHT = tree_img

        self.passed = False

    def move(self):
        self.y -= self.VEL

    def draw(self, win):
        i = random.randint(0, 1)

        if i:# Draw left
            win.blit(self.PIPE_TOP, (self.x, self.top))
        else:
            # Draw right
            win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, lumber, win):
        pass

class Base:
    """This base will move slowly"""
    VEL = 5
    HEIGHT = base_img.get_height()
    IMG = base_img

    def __init__(self, x):
        self.x = x
        self.y1 = 0
        self.y2 = self.HEIGHT

    def move(self):
        self.y1 -= self.VEL
        self.y2 -= self.VEL

        if self.y1 + self.HEIGHT < 0:
            self.y1 = self.y2 + self.WIDTH

        if self.y2 + self.HEIGHT < 0:
            self.y2 = self.y1 + self.HEIGHT

    def draw(self, win):
        win.blit(self.IMG, (self.y1, self.x))
        win.blit(self.IMG, (self.y2, self.x))

def eval_genomes(genomes, config):
    global WIN, gen
    win = WIN
    gen += 1

    nets = []
    Lumbers = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0 # start with fit 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        Lumbers.append(Lumber(400, 500))
        ge.append(genome)

    base = Base()
    trees = [Tree(20)]
    score = 0

    clock = pygame.time.Clock()
    run = True

    while run and len(Lumber) > 0:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        # Determine which Tree to use for neural netwroks

        # Initialize every lumber and give it 0.1 fit for each frame alive
        for x, lumber in enumerate(Lumbers):
            ge[x].fitness += 0.1
            lumber.move()

            # send lumber location, bottom tree location
            output = nets[Lumbers.index(lumber)].activate((lumber.y, abs(lumber.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                lumber.switch()

        base.move()

        rem = []
        add_tree = False
        for tree in trees:
            tree.move()

        

def run():
    config_file = "config-feedforward.txt"
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter())
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 50)
    print('\nBest genome:\n{!s}'.format(winner))