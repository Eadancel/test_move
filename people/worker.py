import pygame
import os
import people
from map.task import Task, WanderTask
from map.action import Action
from .people import People
from people.need import Need, NeedCleaning, NeedResting
import random
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



class Worker (People):
    def __init__(self,x,y,id,level):
        super().__init__(x,y,id,People.TYPE_WORKER,level)
        self.imgs = []
        self.openForTask=True
        img_tileset = os.path.join("game_assets",f"hotel/characters/worker_{random.randint(1,3)}.png")
        self.load_img_ani(img_matrix, img_tileset)
        self.intensity = random.randint(1,5)
        #self.needs = {}
        self.needs = {"cleaning": NeedCleaning(), "resting": NeedResting(random.randint(1,10))}

    def getNextTask(self):
        super().getNextTask()
        if self.current_action["type"]==Action.TYPE_TAKE_OBJ:
            self.obj=self.current_action["obj"]
            self.obj.grabbed=True
        elif self.current_action["type"]==Action.TYPE_RELEASE_OBJ:
            self.obj.grabbed=False
            self.obj=None
        elif self.current_action["type"]==Action.TYPE_MAKE_VISIBLE:           
            self.game.removeObj(self.current_action["obj"])
            self.obj=None

        elif self.current_action["type"] in (Action.TYPE_TASKWORK, Action.TYPE_TASKWORK_OBJ):
            self.status=People.STATUS_WORKING
        
        #print(self.currentPath)

    def working(self):
        value = self.current_action['value']
        need = self.currentTask.need
        self.needs[need].doDecrement(value)
        
        if self.needs[need].isSolved():
                self.status=People.STATUS_IDLE
                self.needs[need].status=Need.STATUS_ACTIVE
        else:
                self.status=People.STATUS_WORKING

    def getDefaultTask(self):
        return WanderTask("walkable_path")