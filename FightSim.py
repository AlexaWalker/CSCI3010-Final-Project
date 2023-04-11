import pygame, sys
from pygame.locals import *
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.integrate import ode
import random as rand

# colours
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
VGKGOLD = (185, 151, 91)
TORBLUE = (0, 32, 91)


class Player(pygame.sprite.Sprite):
    def __init__(self, color, width, height, bg):
        pygame.sprite.Sprite.__init__(self)

        self.pos = pygame.math.Vector2(rand.randint(0, 620), rand.randint(0, 350))
        self.dir = pygame.math.Vector2(1, 0).rotate(rand.randrange(360))

        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.x_speed = 2
        self.radius = 7
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.image.fill(WHITE)
        #cx = self.rect.centerx
        #cy = self.rect.centery
        pygame.draw.circle(bg, color, (self.pos[0], self.pos[1]), self.radius)
        self.rect = self.image.get_rect()
    
    def update(self):
        #pygame.sprite.Sprite.update(self)
        self.rect.x += self.x_speed
        self.pos[0] += self.x_speed
        print("Bruh")

        '''
        if self.pos[0] - self.radius < 0:
            self.pos[0] = self.radius
            self.dir[0] = abs(self.dir[0])
        elif self.pos[0] + self.radius > 400:
            self.pos[0] = 400 - self.radius
            self.dir[0] = -abs(self.dir[0])
        if self.pos[1] - self.radius < 50:
            self.pos[1] = 50 + self.radius
            self.dir[1] = abs(self.dir.y)
        elif self.pos[1] + self.radius > 700:
            self.pos[1] = 700 - self.radius
            self.dir[1] = -abs(self.dir[1]) 

        self.cx = round(self.pos[0])
        self.cy = round(self.pos[1])
        '''


def Main():
    clock = pygame.time.Clock()
    pygame.init()

    #background setup
    width = 620
    height = 350
    screen = pygame.display.set_mode((width,height))
    bg = pygame.image.load('assets/rink.jpg')
    bg = pygame.transform.scale(bg,(width,height))

    #players setup
    player1 = Player(VGKGOLD, 2, 2, bg)
    player2 = Player(TORBLUE, 2, 2, bg)
    my_group = pygame.sprite.Group(player1)
    #my_group = pygame.sprite.Group(player2)

    run = True
    while run:
        clock.tick(30)
        screen.blit(bg,(0,0))

        my_group.update()
        my_group.draw(screen)


        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        pygame.display.update()

        my_group.update()


Main()