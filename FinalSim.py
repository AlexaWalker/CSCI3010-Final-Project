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
        #random start position
        self.x = rand.randint(0, 620)
        self.y = rand.randint(0, 350)

        #random starting velocity
        self.velocity = np.array((rand.randint(2, 5), rand.randint(2, 5)))
        self.tot_vel = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)

        self.state = [self.x, self.y, self.velocity[0], self.velocity[1]] #x_pos, y_pos, x_vel, y_vel
        self.dt = 1.0
        self.t = 0
        self.mass = 90 #kg
        self.radius = 7

        self.solver = ode(self.f)
        self.solver.set_integrator('dop853')
        self.solver.set_initial_value(self.state, self.t)

    def draw(self, bg, colour):
        pygame.draw.circle(bg, colour, (self.x, self.y), self.radius)

    def f(self, p2):
        v =  ((self.mass-p2.mass)/(self.mass+p2.mass))*self.tot_vel+((2*p2.mass)/(self.mass+p2.mass))*p2.tot_vel
        theta = math.atan((p2.state[1]-self.state[1])/(p2.state[0]-self.state[0]))
        vx = v*math.cos(theta)
        vy = v*math.sin(theta)
        x = self.state[0] + vx 
        y = self.state[1] + vy
        return[x, y, vx, vy]
    
    def update(self, p2): 
        new_state = self.solver.integrate(self.t + self.dt)

        if not self.check_collision(new_state):
            self.state = new_state
            self.t += self.t

            #skating motion
            self.state[0] += self.state[2]
            self.state[1] += self.state[3]

            if self.x - self.radius < 0:
                self.x = self.radius
                self.state[2] = rand.randint(2, 5)
                self.state[3] = rand.randint(0, 5)
                self.state[3] *= -1

            elif self.state[0] + self.radius >= WIDTH:
                self.state[0] = WIDTH - self.radius
                self.state[2] = rand.randint(2, 5)
                self.state[3] = rand.randint(0, 5)
                self.state[2] *= -1

            if self.state[1] - self.radius < 0:
                self.state[1] = 0 + self.radius
                self.state[2] = rand.randint(0, 5)
                self.state[3] = rand.randint(2, 5)
                self.state[2] *= -1

            elif self.state[1] + self.radius >= HEIGHT:
                self.state[1] = HEIGHT - self.radius
                self.state[2] = rand.randint(0, 5)
                self.state[3] = rand.randint(2, 5)
                self.state[3] *= -1

            self.tot_vel = math.sqrt(self.state[1]**2 + self.state[3]**2)

        else:
            state_after_collision, collision_time = self.collide(new_state, p2, self.t+self.dt)
            self.state = state_after_collision
            self.t = collision_time
            self.solver.set_intial_value(self.state, self.t)


    def check_collision(self, state, p2):
        return (math.sqrt((p2.state[0]-state[0])**2+(p2.state[1]-state[1])**2)<=self.radius+p2.radius)
        
    def collide(self, state, p2, time):
        pass
            

    def close_pass(self, p2):
        return (math.sqrt((p2.state[0]-self.state[0])**2+(p2.state[1]-self.state[1])**2)<=self.radius+p2.radius+10)


    def stay_in_area(self, x_min, x_max, y_min, y_max):
        if self.x - self.radius < x_min:
            self.x = self.radius
            self.state[2] = 2
            self.state[3] = 2
            self.state[3] *= -1

        elif self.state[0] + self.radius >= x_max:
            self.state[0] = WIDTH - self.radius
            self.state[2] = rand.randint(2, 5)
            self.state[3] = rand.randint(0, 5)
            self.state[2] *= -1

        if self.state[1] - self.radius < y_min:
            self.state[1] = 0 + self.radius
            self.state[2] = rand.randint(0, 5)
            self.state[3] = rand.randint(2, 5)
            self.state[2] *= -1

        elif self.state[1] + self.radius >= y_max:
            self.state[1] = HEIGHT - self.radius
            self.state[2] = rand.randint(0, 5)
            self.state[3] = rand.randint(2, 5)
            self.state[3] *= -1
        
        self.tot_vel = math.sqrt(self.state[2]**2 + self.state[3]**2)

    def fight(self, p2):
        fight_area_x_min = self.x - 20
        fight_area_x_max = self.x + 20
        fight_area_y_min = self.y - 20
        fight_area_y_max = self.y + 20

        self.stay_in_area(fight_area_x_min, fight_area_x_max, fight_area_y_min, fight_area_y_max)
        if self.check_collision(p2):
            self.collide(p2, self.t)
        else:
            pass


    def track(self, p1, p2):
        if(self.close_pass(p2)):
            self.fight(p2)

        

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

        player1.update(player2)
        player2.update(player1)
        player1.track(player2)
        player1.check_collision(player2)
        screen.blit(bg, (0,0))
        player1.draw(screen, VGKGOLD)
        player2.draw(screen, TORBLUE)

        pygame.display.update()



Main()