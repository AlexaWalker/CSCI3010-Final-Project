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

#dimensions
WIDTH = 620
HEIGHT = 350


class Player():
    def __init__(self):
        self.x = rand.randint(0, 620)
        self.y = rand.randint(0, 350)
        self.velocity = np.array((rand.randint(2, 5), rand.randint(2, 5)))
        self.tot_vel = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
        self.state = [self.x, self.y, self.velocity[0], self.velocity[1]] #x_pos, y_pos, x_vel, y_vel
        self.dt = 1.0
        self.t = 0
        self.mass = 200
        self.radius = 7

        self.solver = ode(self.f)
        self.solver.set_integrator('dop853')
        self.solver.set_initial_value(self.state, self.t)

    def draw(self, bg, colour):
        pygame.draw.circle(bg, colour, (self.x, self.y), self.radius)

    def f(self, t, x, y, p2):
        self.mass, p2.mass = self.mass, p2.mass
        M = self.mass + p2.mass
        r1, r2 = self.radius, p2.radius
        d = np.linalg.norm(r1 - r2)**2
        v1, v2 = self.tot_velocity, p2.tot_velocity
        u1 = v1 - 2*p2.mass / M * np.dot(v1-v2, r1-r2) / d * (r1 - r2)
        u2 = v2 - 2*self.mass / M * np.dot(v2-v1, r2-r1) / d * (r2 - r1)
        self.v = u1
        p2.v = u2
        return[]
    
    def update(self, p2): 
        new_state = self.solver.integrate(self.t + self.dt)

        if not self.check_collision(new_state):
            self.state = new_state
            self.t += self.t

            #skating motion
            self.x += self.velocity[0]
            self.y += self.velocity[1]

            if self.x - self.radius < 0:
                self.x = self.radius
                self.velocity[0] = rand.randint(2, 5)
                self.velocity[1] = rand.randint(0, 5)
                self.velocity[1] *= -1

            elif self.x + self.radius >= WIDTH:
                self.x = WIDTH - self.radius
                self.velocity[0] = rand.randint(2, 5)
                self.velocity[1] = rand.randint(0, 5)
                self.velocity[0] *= -1

            if self.y - self.radius < 0:
                self.y = 0 + self.radius
                self.velocity[0] = rand.randint(0, 5)
                self.velocity[1] = rand.randint(2, 5)
                self.velocity[0] *= -1

            elif self.y + self.radius >= HEIGHT:
                self.y = HEIGHT - self.radius
                self.velocity[0] = rand.randint(0, 5)
                self.velocity[1] = rand.randint(2, 5)
                self.velocity[1] *= -1

            self.tot_vel = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)

        else:
            state_after_collision, collision_time = self.collide(new_state, p2, self.t+self.dt)
            self.state = state_after_collision
            self.t = collision_time
            self.solver.set_intial_value(self.state, self.t)


        def check_collision(self, state, p2):
            return (math.sqrt((p2.state[0]-state[0])**2+(p2.state[1]-state[1])**2)<=self.radius+p2.radius)
        
        def collide(self, state, p2, time):
            

def close_pass(p1, p2):
    return (math.sqrt((p2.x-p1.x)**2+(p2.y-p1.y)**2)<=p1.radius+p2.radius+10)


def stay_in_area(p, x_min, x_max, y_min, y_max):
    if p.x - p.radius < x_min:
        p.x = p.radius
        p.velocity[0] = 2
        p.velocity[1] = 2
        p.velocity[1] *= -1

    elif p.x + p.radius >= x_max:
        p.x = WIDTH - p.radius
        p.velocity[0] = rand.randint(2, 5)
        p.velocity[1] = rand.randint(0, 5)
        p.velocity[0] *= -1

    if p.y - p.radius < y_min:
        p.y = 0 + p.radius
        p.velocity[0] = rand.randint(0, 5)
        p.velocity[1] = rand.randint(2, 5)
        p.velocity[0] *= -1

    elif p.y + p.radius >= y_max:
        p.y = HEIGHT - p.radius
        p.velocity[0] = rand.randint(0, 5)
        p.velocity[1] = rand.randint(2, 5)
        p.velocity[1] *= -1

def fight(p1, p2):
    fight_area_x_min = p1.x - 20
    fight_area_x_max = p1.x + 20
    fight_area_y_min = p1.y - 20
    fight_area_y_max = p1.y + 20

    stay_in_area(p1, fight_area_x_min, fight_area_x_max, fight_area_y_min, fight_area_y_max)
    if check_collision(p1, p2):
        collide(p1, p2)
    else:
        pass

def track(p1, p2):
    if(close_pass(p1, p2)):
        fight(p1, p2)
        


def Main():
    clock = pygame.time.Clock()
    pygame.init()

    #background setup
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    bg = pygame.image.load('c:/Users/fredi/OneDrive/Documents/School/Year 5/Simulations and Modelling/Final Project/assets/rink.jpg')
    bg = pygame.transform.scale(bg,(WIDTH,HEIGHT))

    #players setup
    player1 = Player()
    player2 = Player()

    while True:
        clock.tick(30)

        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

        player1.update()
        player2.update()
        track(player1, player2)
        check_collision(player1, player2)
        screen.blit(bg, (0,0))
        player1.draw(screen, VGKGOLD)
        player2.draw(screen, TORBLUE)

        pygame.display.update()



Main()