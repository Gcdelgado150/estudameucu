import pygame

pygame.init()
WIN_WIDTH = 600
WIN_HEIGHT = 800
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
done = False
is_blue = True

x = 370
initial_x = x
y = 500
move = 250

base_img = pygame.transform.scale(pygame.image.load("imgs/base.png").convert_alpha(), (50, 500))
bg_img = pygame.transform.scale(pygame.image.load("imgs/bg.png").convert_alpha(), (WIN_WIDTH, WIN_HEIGHT))
lumber_images = pygame.transform.scale(pygame.image.load("imgs/lumber.png"), (100, 120))

class Base:
    """This base will move slowly"""
    VEL = 5
    HEIGHT = base_img.get_height() - 50
    IMG = base_img

    def __init__(self, x):
        self.x = x
        self.y1 = 0
        self.y2 = self.HEIGHT

    def move(self):
        self.y1 += self.VEL
        self.y2 += self.VEL

        if self.y1 - self.HEIGHT > self.HEIGHT:
            self.y1 = self.y2 - self.HEIGHT

        if self.y2 - self.HEIGHT > self.HEIGHT:
            self.y2 = self.y1 - self.HEIGHT

    def draw(self, win):
        win.blit(self.IMG, (self.x, self.y1))
        win.blit(self.IMG, (self.x, self.y2)) 
        
clock = pygame.time.Clock()
base = Base(275)
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_blue = not is_blue

    pressed = pygame.key.get_pressed()
    
    if pressed[pygame.K_LEFT] and x == initial_x: 
        x -= move
    if pressed[pygame.K_RIGHT] and x == initial_x - move: 
        x += move

    screen.blit(bg_img, (0,0))
    screen.blit(lumber_images, (x, y))
    base.move()
    base.draw(screen)
    
    
    pygame.display.flip()
    clock.tick(60)