import pygame
import os, sys

from map.level.restaurante import LevelRestaurante
import random
FPS = 600


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

                   

        



    



