from operator import truediv
import pygame
import os
import people
from map.task import Task
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
    def __init__(self,x,y,id,map,font):
        super().__init__(x,y,id,People.TYPE_CUSTOMER,map,font)
        self.imgs = []
        self.openForTask=True
        self.money=random.randint(1,5000)+3000
        self.garbage = random.randint(1,5)
        print(f"Init {self.id} Money:{self.money}")
        for i in range(5):
            self.imgs.append([])
            for pi in pathimgs_status[i]:
                self.imgs[i].append(pygame.image.load(os.path.join("game_assets/Tiles",pi)))
        self.intensity = random.randint(1,5) * 10
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
        elif self.current_action["type"]==Action.TYPE_TASKWORK:
            self.status=People.STATUS_WORKING
            

    def draw(self,win):
        super().draw(win)
        # pygame.draw.rect(win, (0,128,0), (self.xGrid, self.yGrid - 22, 25, 5))
        # pygame.draw.rect(win, (255,0,0), (self.xGrid, self.yGrid - 22, int(round(self.needs["thirst"].percent()/4)), 5))
        
        # pygame.draw.rect(win, (0,128,0), (self.xGrid, self.yGrid - 28, 25, 5))
        # pygame.draw.rect(win, (255,0,0), (self.xGrid, self.yGrid - 28, int(round(self.needs["gambling"].percent()/4)), 5))

        self.popup_info.set_text(f"{self.money}")  
        
        if self.money>0:
            offset = 15
            for (k,n) in self.needs.items():
                n.draw(win, self.xGrid, self.yGrid - offset)
                offset+=5
                n.doIncrement(self.intensity)
                task = n.getTask()
                if task is not None:
                    #print(f"solving need {k} Customer :{self.id}")
                    self.popup_status.set_text("solving need...{}".format(k))
                    self.assignTask(task)


    def working(self):  
        if self.money>0:
            value = self.current_action["value"]
            need = self.current_action["need"]
            profit = self.current_action["profit"]
            luck = self.current_action["luck"]
            #cost = random.randint(1,self.current_action["cost"])
            cost = self.current_action["cost"]
            addGarba = self.current_action["addGarba"]


            self.money-=cost
            ganancia = random.choices(profit,luck,k=1)[0] * cost            
            self.money+=ganancia
            self.needs[need].doDecrement(value * (2 if ganancia>0 else 1))
            self.garbage+=random.randint(1,addGarba)

            if ganancia>0 : print(f"Customer {self.id} ganancia:{ganancia} :money {self.money}")
            if self.needs[need].isSolved():
                #self.popup_status.set_text("__IDLE__")  
                self.status=People.STATUS_IDLE
                self.needs[need].status=Need.STATUS_ACTIVE
            else:
                self.status=People.STATUS_WORKING

        if self.money<=0:
            self.status=People.STATUS_IDLE
            self.popup_status.set_text("Leaving...")
            self.assignTask(self.getLeavingTask())

        
    def getLeavingTask(self):
        solution = [{"type":Action.TYPE_GOTO_ZONE,
                     "zone":"out",
                     "canInterrup":False,
                     "drop":False,
                     "velocity":0.5},
                    {"type":Action.TYPE_PEOPLE_STATUS, 
                     "status": People.STATUS_LEAVING}]
        return Task(solution,random.randint(1,20))

    def getDefaultTask(self):
        return Task([{"type":Action.TYPE_GOTO_ZONE,"zone":"walkable","canInterrup":True,"drop":False,"velocity":0.5}],random.randint(1,20))
    def gotGarbage(self):
        if self.garbage>100 :
            self.garbage=0
            return True
        else:
            return False