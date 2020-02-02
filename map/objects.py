import pygame
import os
from collections import deque
#from people.people import People


#pathImgs = ["tile_0251.png","tile_0252.png","tile_0253.png"]

class Objects:

    def __init__(self, x, y, pathImgs):
        self.x = x
        self.y = y

        self.imgs = []
        self.grabbed = False
        for pi in pathImgs:
            self.imgs.append(pygame.image.load(os.path.join("game_assets/Tiles",pi)))
    def draw(self, win, map):
        win.blit(self.imgs[self.status], (map.convertXGridToPX(self.x), map.convertYGridToPX(self.y)))
    def drawOn(self, win, xGrid, yGrid):
        win.blit(self.imgs[self.status], (xGrid, yGrid ))



