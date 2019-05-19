import pygame
import os
import people
from .people import People
    # DIREC_MOVING_STAY = 0
    # DIREC_MOVING_UP = 1
    # DIREC_MOVING_DOWN = 2
    # DIREC_MOVING_LEFT = 3
    # DIREC_MOVING_RIGHT = 4
pathimgs_status = (["tile_0266.png","tile_0293.png","tile_0320.png"],
                   ["tile_0266.png","tile_0293.png","tile_0320.png"],
                   ["tile_0266.png","tile_0293.png","tile_0320.png"],
                   ["tile_0266.png","tile_0293.png","tile_0320.png"],
                   ["tile_0266.png","tile_0293.png","tile_0320.png"])




class Worker (People):
    def __init__(self,x,y,map):
        super().__init__(x,y,People.TYPE_WORKER,map)
        self.imgs = []            
        for pi in pathimgs_status[self.direcMoving]:
            self.imgs.append(pygame.image.load(os.path.join("game_assets\Tiles",pi)))
