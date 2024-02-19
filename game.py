import pygame
import os, sys
import pytmx
from pytmx.util_pygame import load_pygame
from people.people import People
from people.worker import Worker
from people.customer import Customer
from map.task import Task
from map.task import CleanObjectRecoverZone
from map.map import Map 
from map.objs.objects import Objects, Garbage, Sofa, SlotMachine, Drink
from map.level.restaurante import LevelRestaurante
from collections import deque
from ui.ui import Label
import random
FPS = 120


## "mapaCity.tmx"
class Game:
    teAddCustomer = pygame.USEREVENT+1
    teCheckingGarbage = pygame.USEREVENT+2
    def __init__(self):
        pygame.init()
        self.displayWindow = pygame.display.set_mode((640*2, 320*2))
        self.clock = pygame.time.Clock()
        self.level = LevelRestaurante()

    def run (self):

        while True:
            dt = self.clock.tick(FPS) /1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    self.level.input(event)
            if dt <  2*1/FPS:    ## in case the window is freezing because is moving (Window behaviour)
                self.level.run(dt)         
            pygame.display.set_caption("{:.2f}  Info {}".format(self.clock.get_fps(), self.level.info))
            pygame.display.update()

                   

        



    



