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
pathimgs_status = (["tile_0267.png"],
                   ["tile_0268.png","tile_0295.png","tile_0322.png"],
                   ["tile_0267.png","tile_0294.png","tile_0321.png"],
                   ["tile_0266.png","tile_0293.png","tile_0320.png"],
                   ["tile_0269.png","tile_0296.png","tile_0323.png"])

class Worker (People):
    def __init__(self,x,y,map, font):
        super().__init__(x,y,People.TYPE_WORKER,map,font)
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
        elif self.current_action["type"]==Action.TYPE_MAKE_VISIBLE:
            
            self.current_action["obj"].visible = self.current_action["visible"]
            self.obj=None
        
        #print(self.currentPath)

    def working(self):
        self.currentTask.workingOn(self.working_force)
        if self.currentTask.status == Task.STATUS_DONE:
            self.status=People.STATUS_IDLE
        else:
            self.status=People.STATUS_WORKING
    def getDefaultTask(self):
        return Task([{"type":Action.TYPE_GOTO_ZONE,"zone":"rest_zone","canInterrup":True,"drop":False,"velocity":0.5}],random.randint(1,20))