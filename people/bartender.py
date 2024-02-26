import random
import pygame, os
from map.task import WanderTask
from people.need import NeedCleaning
from people.people import People

from people.worker import Worker
    # ANIMA_MOVING_STAY = 0
    # ANIMA_MOVING_UP = 1
    # ANIMA_MOVING_DOWN = 2
    # ANIMA_MOVING_LEFT = 3
    # ANIMA_MOVING_RIGHT = 4
    # chars are 2 tiles tall
    # each frame is a (topleft corner, frame size)


img_matrix = {  People.ANIMA_MOVING_STAY:    [(288+i*16,32,16,32) for i in range(6)],
                People.ANIMA_MOVING_UP:      [(96+i*16,64,16,32) for i in range(6)],
                People.ANIMA_MOVING_DOWN:    [(288+i*16,64,16,32) for i in range(6)],
                People.ANIMA_MOVING_LEFT:    [(192+i*16,64,16,32) for i in range(6)],
                People.ANIMA_MOVING_RIGHT:   [(0+i*16,64,16,32) for i in range(6)],
                People.ANIMA_WORKING:        [(0+i*16,224,16,32) for i in range(12)]}

class Bartender(Worker):
    def __init__(self,x,y,id,level):
        super().__init__(x,y,id,level)
        img_tileset = os.path.join("game_assets",f"hotel/characters/bartender_{random.randint(1,3)}.png")
        self.load_img_ani(img_matrix, img_tileset)
        #self.needs['cleaning']=NeedCleaning()

    def getDefaultTask(self):
        return WanderTask("bar")
