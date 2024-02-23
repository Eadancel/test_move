import pygame
import os, sys, time
from debug import debug

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
        previous_time = time.time()
        while True:
            
            dt = time.time() - previous_time
            previous_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    self.level.input(event)
            
            if dt <  100/FPS:    ## in case the window is freezing because is moving (Window behaviour)
                self.level.run(dt)   
            else:
                print("drop frame")
            zoom= self.level.all_sprites.zoom_scale
            offset = self.level.all_sprites.offset
            debug(f"{zoom=} {offset=}")      
            pygame.display.set_caption("{:.2f}  Info {}".format(self.clock.get_fps(), self.level.info))
            pygame.display.update()
            self.clock.tick(FPS)

                   

        



    



