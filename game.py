import sys
import time

import pygame
from pygame.locals import K_ESCAPE
from debug import debug
from map.level.restaurante import LevelRestaurante

FPS = 600


## "mapaCity.tmx"
class Game:
    teAddCustomer = pygame.USEREVENT + 1
    teCheckingGarbage = pygame.USEREVENT + 2

    def __init__(self):
        pygame.init()
        self.displayWindow = pygame.display.set_mode((1280, 640))
        self.clock = pygame.time.Clock()
        self.level = LevelRestaurante()

    def run(self):
        previous_time = time.time()
        while True:

            dt = time.time() - previous_time
            previous_time = time.time()
            self.displayWindow.fill("black")
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if (event.type == pygame.QUIT) or (keys[K_ESCAPE]):
                    pygame.quit()
                    sys.exit()
                else:
                    self.level.input(event)

            if (dt < 100 / FPS):  ## in case the window is freezing because is moving (Window behaviour)
                self.level.update(dt)
            else:
                print("drop frame")
            posMS = pygame.mouse.get_pos()
            debug(f"{self.level.getAvailableContSlots('drink_delivery')}")
            pygame.display.set_caption(
                "{:.2f}  Info {}".format(self.clock.get_fps(), self.level.info)
            )
            pygame.display.update()
            self.clock.tick(FPS)
