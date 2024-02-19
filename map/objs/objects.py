import pygame
import os
from map.task import MovetoZoneTaskTakeRelease, MoveWorkObjMoney, MovetoObjWork, MoveConsumeObjMoney
import random


#pathImgs = ["tile_0251.png","tile_0252.png","tile_0253.png"]

class Objects(pygame.sprite.Sprite):
    STATUS_NORMAL = 0
    STATUS_DIRTY = 1
    STATUS_CLEANING = 2
    STATUS_LOCKED = 3

    def __init__(self, x, y, o_type, pathImgs, group):
        super().__init__(group)
        self.x = x
        self.y = y
        self.type = o_type
        self.imgs = []
        self.grabbed = False
        self.visible = True
        self.status=Objects.STATUS_NORMAL
        for pi in pathImgs:
            self.imgs.append(pygame.image.load(os.path.join("game_assets/Tiles",pi)))
    def update (self, level, dt):
        self.image = self.imgs[self.status]
        self.rect = self.image.get_rect(topleft=(level.map.convertXGridToPX(self.x),level.map.convertYGridToPX(self.y)))
    def drawOn(self, win, xGrid, yGrid):
        if self.visible:
            win.blit(self.imgs[self.status], (xGrid, yGrid ))
    def workOnObj(self):
        pass
    

class Garbage(Objects):
    
    def __init__(self,x,y, group):
        super().__init__(x,y,"garbage",["tile_0307.png","tile_0307.png","tile_0307.png"], group)
        self.task = MovetoZoneTaskTakeRelease(self,"garbage","cleaning",Objects.STATUS_DIRTY)


class SlotMachine(Objects):

    def __init__(self,x,y, group):
        super().__init__(x,y,"gambling",["tile_0223.png","tile_0223.png","tile_0223.png"], group)
        
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

    def __init__(self,x,y, group):
        super().__init__(x,y,"garbage",["tile_0333.png","tile_0333.png","tile_0333.png"], group)
        self.task = self.getTask()
    def getTask(self):
        return MovetoObjWork(self,"resting",40)
    
class Drink(Objects):
    def __init__(self,x,y, group):
        super().__init__(x,y,"thirst",["tile_0190.png","tile_0307.png","tile_0307.png"], group)
        self.cost = 100
        self.task = self.getTask()
    def getTask(self):
        return MoveConsumeObjMoney(self,"thirst",40)
    def workOnObj(self):
        ganancia = 0
        return  ganancia - self.cost  