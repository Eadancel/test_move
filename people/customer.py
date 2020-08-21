import pygame
import os
import people
from map.task import Task
from map.action import Action
from .people import People
import random
    # DIREC_MOVING_STAY = 0
    # DIREC_MOVING_UP = 1
    # DIREC_MOVING_DOWN = 2
    # DIREC_MOVING_LEFT = 3
    # DIREC_MOVING_RIGHT = 4
pathimgs_status = (["tile_0186.png"],
                   ["tile_0214.png","tile_0187.png","tile_0241.png"],
                   ["tile_0213.png","tile_0186.png","tile_0240.png"],
                   ["tile_0212.png","tile_0185.png","tile_0239.png"],
                   ["tile_0215.png","tile_0188.png","tile_0242.png"])

class Customer (People):
    def __init__(self,x,y,map):
        super().__init__(x,y,People.TYPE_CUSTOMER,map)
        self.imgs = []
        self.openForTask=True

        for i in range(5):
            self.imgs.append([])
            for pi in pathimgs_status[i]:
                self.imgs[i].append(pygame.image.load(os.path.join("game_assets/Tiles",pi)))

    def getNextTask(self):
        super().getNextTask()
        if self.current_action["type"]==Action.TYPE_TAKE_OBJ:
            self.obj=self.current_action["obj"]
            self.obj.grabbed=True
        elif self.current_action["type"]==Action.TYPE_RELEASE_OBJ:
            self.obj.grabbed=False
            self.obj=None
        #print(self.currentPath)

    def working(self):
        self.currentTask.workingOn(self.working_force)
        if self.currentTask.status == Task.STATUS_DONE:
            self.status=People.STATUS_IDLE
        else:
            self.status=People.STATUS_WORKING
    def getDefaultTask(self):
        return Task([{"type":Action.TYPE_GOTO_ZONE,"zone":"walkable","canInterrup":True,"drop":False,"velocity":0.7}],random.randint(1,20))
    def gotGarbage(self):
        return random.randint(0,5000)<10