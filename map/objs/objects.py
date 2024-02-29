import pygame
import os
from map.task import CleanObjectRecoverZone, MovetoObjWorkOffset, MovetoZoneTaskTakeRelease, MoveWorkObjMoney,  MoveConsumeObjMoney
import random


#pathImgs = ["tile_0251.png","tile_0252.png","tile_0253.png"]

class Objects(pygame.sprite.Sprite):
    STATUS_NORMAL = 0
    STATUS_DIRTY = 1
    STATUS_CLEANING = 2
    STATUS_LOCKED = 3
    STATUS_TO_DELIVERY = 4
    STATUS_TOBE_SERVED = 4
    STATUS_READY = 5
    def __init__(self, x, y, o_type, pathImgs, group):
        super().__init__(group)
        self.x = x
        self.y = y
        self.zLevel = 0
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
        win.blit(self.imgs[self.status], (xGrid, yGrid))
    def workOnObj(self):
        pass
    

class Garbage(Objects):
    
    def __init__(self,x,y, group):
        super().__init__(x,y,"garbage",["tile_0307.png","tile_0307.png","tile_0307.png"], group)
        self.task = self.getTask()
    def update (self, level, dt):
        if not self.grabbed: 
            self.image = self.imgs[self.status]
            self.rect = self.image.get_rect(topleft=(level.map.convertXGridToPX(self.x),level.map.convertYGridToPX(self.y)))
    def getTask(self):
        if self.status == Drink.STATUS_NORMAL:
            return MovetoZoneTaskTakeRelease(self,"garbage","cleaning",Objects.STATUS_DIRTY)
        elif self.status == Objects.STATUS_DIRTY:
            return CleanObjectRecoverZone(self,"garbage")
        else:
            print("NO STATUS FOUND")

class SlotMachine(Objects):

    def __init__(self,x,y, group, images):
        super().__init__(x,y,"gambling",[], group)
        self.imgs = images
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

class Machine(Objects):
    def __init__(self,x,y, group, images, type, name, pos):
        super().__init__(x,y,type,[], group)
        self.type=type
        self.available = True
        self.machine_type=name
        self.imgs = images
        self.task = self.getTask()
        self.pos = pos
    def getTask(self):
        return None
    def update (self, level, dt):
        if not self.grabbed: 
            self.image = self.imgs[self.status]
            self.rect = self.image.get_rect(topleft=(self.pos))

    def getSpot(self):
        return (self.x, self.y)
    
    def getNewObj(self, group, delivery,serveOn):
        return Drink(self.x, self.x,self.type, group, delivery,serveOn)

class Sofa(Objects):

    def __init__(self,x,y, group, images, type):
        super().__init__(x,y,type,[], group)
        self.type=type
        self.imgs = images
        self.task = self.getTask()
    def getTask(self):
        return MovetoObjWorkOffset(self,self.type,40,(0,1))
    
class Drink(Objects):
    def __init__(self,x,y,type, group,delivery_zone, serveOn):
        super().__init__(x,y,"thirst",["tile_0190.png","tile_0307.png","tile_0307.png","tile_0307.png","tile_0307.png","tile_0307.png"], group)
        self.status = Drink.STATUS_TO_DELIVERY
        self.cost = 100
        self.serveOn = serveOn
        self.delivery_zone = delivery_zone
        self.type=type
        self.task = self.getTask()
        self.image = self.imgs[self.status]
        self.rect = self.image.get_rect(topleft=(0,0))
    def getTask(self):
        ###  to Delivery : from Machine to Deliveryzone
        ###  to Servive  : from DeliveryZone to TableSpot (ServeOn)
        ###  Ready to be consumer : Task for customer to consume the obj
        if self.status == Drink.STATUS_TO_DELIVERY:
            return MovetoZoneTaskTakeRelease(self,self.delivery_zone,"serving", Drink.STATUS_TOBE_SERVED) 
        elif self.status == Drink.STATUS_TOBE_SERVED:
            return MovetoZoneTaskTakeRelease(self,self.serveOn,"serving", Drink.STATUS_READY) 
        elif self.status == Drink.STATUS_READY:
            return MoveConsumeObjMoney(self,"thirst",40) 
    def workOnObj(self):
        ganancia = 0
        return  ganancia - self.cost  
    

