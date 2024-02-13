from operator import truediv
import pygame
import os
import people
from map.task import Task, LeavingGameTask, WanderTask
from map.action import Action
from .people import People
import random
from people.need import Need, NeedGambling, NeedThirst
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
    def __init__(self,x,y,id,game,font):
        super().__init__(x,y,id,People.TYPE_CUSTOMER,game,font)
        self.imgs = []
        self.openForTask=True
        self.money=random.randint(1,5000)#+3000
        self.garbage = random.randint(1,5)
        self.intensity = random.randint(1,5)
        print(f"Init {self.id} Money:{self.money} Intensity:{self.intensity}" )
        for i in range(5):
            self.imgs.append([])
            for pi in pathimgs_status[i]:
                self.imgs[i].append(pygame.image.load(os.path.join("game_assets/Tiles",pi)))
        
        self.needs = {"thirst": NeedThirst(), 
                      "gambling": NeedGambling()}

    def getNextTask(self):
        super().getNextTask()
        if self.current_action["type"]==Action.TYPE_TAKE_OBJ:
            self.obj=self.current_action["obj"]
            self.obj.grabbed=True
        elif self.current_action["type"]==Action.TYPE_RELEASE_OBJ:
            self.obj.grabbed=False
            self.obj=None
        elif self.current_action["type"] in (Action.TYPE_TASKWORK, Action.TYPE_TASKWORK_OBJ):
            self.status=People.STATUS_WORKING
            

    def draw(self,win):
        super().draw(win)

        self.popup_info.set_text(f"{self.money}")  
        
        #if self.money>0:



    def working(self): 
        value = self.current_action["value"]
        need = self.current_action["need"]
        addGarba = self.current_action["addGarba"]
        if self.needs[need].needsMoney:
            if self.money>0:
                if self.current_action["type"]==Action.TYPE_TASKWORK_OBJ:
                    ganancia = self.current_action["obj"].workOnObj()            
                    self.money+=ganancia
                    self.needs[need].doDecrement(value * (2 if ganancia>0 else 1))
            else:
                self.status=People.STATUS_IDLE
                self.popup_status.set_text("Leaving...")
                self.assignTask(self.getLeavingTask())
                return

        self.garbage+=random.randint(1,addGarba)

        if self.needs[need].isSolved():
            self.status=People.STATUS_IDLE
            self.needs[need].status=Need.STATUS_ACTIVE
        else:
            self.status=People.STATUS_WORKING
        
    def getLeavingTask(self):
        return LeavingGameTask("out")

    def getDefaultTask(self):
        return WanderTask("walkable")
    def gotGarbage(self):
        if self.garbage>100 :
            self.garbage=0
            return True
        else:
            return False