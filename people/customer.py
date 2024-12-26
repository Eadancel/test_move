from operator import truediv
import pygame
import os
import people
from map.task import Task, LeavingGameTask, WanderTask
from map.action import Action
from .people import People
import random
from people.need import Need, NeedGambling, NeedRestCustomer, NeedThirst
    # DIREC_MOVING_STAY = 0
    # DIREC_MOVING_UP = 1
    # DIREC_MOVING_DOWN = 2
    # DIREC_MOVING_LEFT = 3
    # DIREC_MOVING_RIGHT = 4
img_matrix = {  People.ANIMA_MOVING_STAY:    [(288+i*16,32,16,32) for i in range(6)],
                People.ANIMA_MOVING_UP:      [(96+i*16,64,16,32) for i in range(6)],
                People.ANIMA_MOVING_DOWN:    [(288+i*16,64,16,32) for i in range(6)],
                People.ANIMA_MOVING_LEFT:    [(192+i*16,64,16,32) for i in range(6)],
                People.ANIMA_MOVING_RIGHT:   [(0+i*16,64,16,32) for i in range(6)],
                People.ANIMA_WORKING:        [(0+i*16,224,16,32) for i in range(12)]}


class Customer (People):
    def __init__(self,x,y,id,level):
        super().__init__(x,y,id,People.TYPE_CUSTOMER,level)
        self.imgs = []
        self.happiness = 100
        self.openForTask=True
        self.money=random.randint(1,5000)#+3000
        self.garbage = random.randint(1,5)
        self.intensity = random.randint(1,5)
        print(f"Init {self.id} Money:{self.money} Intensity:{self.intensity}" )
        img_tileset = os.path.join("game_assets",f"hotel/characters/customer_{random.randint(1,3)}.png")
        self.load_img_ani(img_matrix,img_tileset)
        
        self.needs = {"thirst": NeedThirst(), 
                      "gambling": NeedGambling(),
                      "customer_resting" : NeedRestCustomer(random.randint(1,15))}

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
        
        #if self.money>0:

    def calc_happynes_add(self, ganancia, need):
        ## TODO Calculation of the frustration changes based on the ganacia compare with the current money
        ## TODO If the amount earn is bigger than current money more happiness is gain.
        ## the level can be influended by the un-solved needs.
        ## Buying things is providing Happyness gain spending money 


        return need.dopamine() * self.intensity

    def working(self): 
        value = self.current_action["value"]
        need = self.current_action["need"]
        addGarba = self.current_action.get("addGarba",1)
        ganancia=0
        if self.needs[need].needsMoney:
            if self.money>0 and self.happiness>0:
                if self.current_action["type"]==Action.TYPE_TASKWORK_OBJ:
                    ganancia = self.current_action["obj"].workOnObj()            
                    self.money+=ganancia
            else:
                self.status=People.STATUS_IDLE
                self.assignTask(self.getLeavingTask())
                return
        else:
            ganancia=1

        self.needs[need].doDecrement(value * (2 if ganancia>0 else 1))
        self.garbage+=random.randint(1,addGarba)

        if self.needs[need].isSolved():
            self.status=People.STATUS_IDLE
            self.needs[need].status=Need.STATUS_ACTIVE
        else:
            self.status=People.STATUS_WORKING
        if self.money>0: ## Avoid DIV by zero
            happy_incre =self.needs[need].dopamine()* ganancia / self.money * self.intensity
        else:
            happy_incre =1
        print(f"{happy_incre=}  Customer : {self.id}")
        self.happiness+= happy_incre       
        self.stage['working on:']=need
        self.stage['money']=self.money
        self.stage['garbage']=self.garbage
        self.stage['happiness']=f"{self.happiness:.2f}"
        
    def getLeavingTask(self):
        return LeavingGameTask("out")

    def getDefaultTask(self):
        return WanderTask("walkable_path")
    def gotGarbage(self):
        if self.garbage>100 :
            self.garbage=0
            return True
        else:
            return False
