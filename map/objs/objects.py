import pygame
import os
from map.task import MovetoZoneTaskTakeRelease, MoveWorkObjMoney, MovetoObjWork, MoveConsumeObjMoney
import random


#pathImgs = ["tile_0251.png","tile_0252.png","tile_0253.png"]

class Objects:
    STATUS_NORMAL = 0
    STATUS_DIRTY = 1
    STATUS_CLEANING = 2
    STATUS_LOCKED = 3

    def __init__(self, x, y, o_type, pathImgs):
        self.x = x
        self.y = y
        self.type = o_type
        self.imgs = []
        self.grabbed = False
        self.visible = True
        self.status=Objects.STATUS_NORMAL
        for pi in pathImgs:
            self.imgs.append(pygame.image.load(os.path.join("game_assets/Tiles",pi)))
    def draw(self, win, map):
        if self.visible:
            win.blit(self.imgs[self.status], (map.convertXGridToPX(self.x), map.convertYGridToPX(self.y)))
    def drawOn(self, win, xGrid, yGrid):
        if self.visible:
            win.blit(self.imgs[self.status], (xGrid, yGrid ))
    def workOnObj(self):
        pass
    

class Garbage(Objects):
    
    def __init__(self,x,y):
        super().__init__(x,y,"garbage",["tile_0307.png","tile_0307.png","tile_0307.png"])
        self.task = MovetoZoneTaskTakeRelease(self,"garbage","cleaning",Objects.STATUS_DIRTY)


class SlotMachine(Objects):

    def __init__(self,x,y):
        super().__init__(x,y,"gambling",["tile_0223.png","tile_0223.png","tile_0223.png"])
        
        self.cost = 100
        self.profit = [0,1,5,20,50,100]
        self.luck = [90,5,2,1,0.07,0.03]
        self.task = self.getTask()
    def getTask(self):
        return MoveWorkObjMoney(self,"gambling",20 )
    
    def workOnObj(self):
        profit = self.profit
        luck = self.luck
        cost = self.cost
        ganancia = random.choices(profit,luck,k=1)[0] * cost
        if ganancia>0 :  print(f"{ganancia=}") 
        return  ganancia - cost  

class Sofa(Objects):

    def __init__(self,x,y):
        super().__init__(x,y,"garbage",["tile_0333.png","tile_0333.png","tile_0333.png"])
        self.task = self.getTask()
    def getTask(self):
        return MovetoObjWork(self,"resting",40)
    
class Drink(Objects):
    def __init__(self,x,y):
        super().__init__(x,y,"thirst",["tile_0190.png","tile_0307.png","tile_0307.png"])
        self.cost = 100
        self.task = self.getTask()
    def getTask(self):
        return MoveConsumeObjMoney(self,"thirst",40)
    def workOnObj(self):
        ganancia = 0
        return  ganancia - self.cost  