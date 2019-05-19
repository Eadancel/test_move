import pygame
import os
import people
from .people import People
pathimgs = ["tile_0266.png","tile_0293.png","tile_0320.png"]



class Worker (People):
    def __init__(self,x,y,map):
        super().__init__(x,y,People.TYPE_WORKER,map)
        self.imgs = []
        for pi in pathimgs:
            self.imgs.append(pygame.image.load(os.path.join("game_assets\Tiles",pi)))
