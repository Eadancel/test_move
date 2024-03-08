import os
import random
import sys
import time

import pygame

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
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    self.level.input(event)

            if (
                dt < 100 / FPS
            ):  ## in case the window is freezing because is moving (Window behaviour)
                self.level.run(dt)
            else:
                print("drop frame")
            posMS = pygame.mouse.get_pos()
            debug(
                f"{self.level.getRelativeMousePos()} {posMS=} Zoom:{self.level.all_sprites.zoom_scale} offsetScaled{self.level.all_sprites.scaled_rect.topleft} Internal{self.level.all_sprites.internal_offset}"
            )
            pygame.display.set_caption(
                "{:.2f}  Info {}".format(self.clock.get_fps(), self.level.info)
            )
            pygame.display.update()
            self.clock.tick(FPS)
