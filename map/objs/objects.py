import os
import random
from debug import debug
from ui.ui import Label
import pygame

from map.task import (CleanObjectRecoverZone, MoveConsumeObjMoney, MoveObjToContainer,
                      MovetoObjWorkOffset, MovetoZoneTaskTakeRelease,MoveObjFromContainerToContainer,
                      MoveWorkObjMoney)

# pathImgs = ["tile_0251.png","tile_0252.png","tile_0253.png"]


class Objects(pygame.sprite.Sprite):
    STATUS_NORMAL = 0
    STATUS_DIRTY = 1
    STATUS_CLEANING = 2
    STATUS_LOCKED = 3
    STATUS_TO_DELIVERY = 4
    STATUS_TOBE_SERVED = 5
    STATUS_READY = 6

    def __init__(self, x, y, o_type, pathImgs, group,drawOn=(0,0)):
        super().__init__(group)
        self.x = x
        self.y = y
        self.drawOn = drawOn
        self.zLevel = 0
        self.type = o_type
        self.imgs = []
        self.grabbed = False
        self.visible = True
        self.status = Objects.STATUS_NORMAL
        for pi in pathImgs:
            self.imgs.append(pygame.image.load(os.path.join("game_assets", pi)))

    def update(self,level:None, dt:None):

        if not self.grabbed:
            self.image = self.imgs[self.status]
            self.rect = self.image.get_rect(
                topleft=(
                    self.drawOn
                )
            )

    def drawOn(self, win, xGrid, yGrid):
        win.blit(self.imgs[self.status], (xGrid, yGrid))

    def workOnObj(self):
        pass

    def getCurrentZone(self):
        return None

class Container(Objects):
    def __init__(self,obj,group):
        super().__init__(obj.get("stGridx"), obj.get("stGridy"), obj.get("type"), [], group,obj.get("drawOn"))
        self.objs = []
        self.limit_obj = 1
        self.status = Objects.STATUS_NORMAL
        self.container_type = obj.get("name")
        self.imgs = [obj.get("image")]
        self.pos_in = obj.get("pos_in")  # position where Persons need to go to insert new obj to container
        self.pos_out = obj.get("pos_out") #  position where Persons need to go to take a new obj to container
    def checkAvailableSlot(self):
        return self.limit_obj-len(self.objs)>=1

    def addObj (self, obj):
        if  self.checkAvailableSlot(): 
            self.objs.append(obj)
            return obj
        else:
            return None

    def removeObj(self, obj):
        print(f"remove {obj}")
        self.objs.remove(obj)
    
    def update(self,level, dt):
        super().update(level, dt)
        offset=0
        for o in self.objs:
            o.zLevel = self.zLevel+1
            o.rect = o.image.get_rect(topleft=(
                level.map.convertXGridToPX(self.x+offset),
                level.map.convertYGridToPX(self.y+offset+15),
            ))
            offset+=3



class Garbage(Objects):

    def __init__(self, x, y, group):
        super().__init__(
            x, y, "garbage", 
            ["Tiles/tile_0307.png", "Tiles/tile_0307.png", "Tiles/tile_0307.png"], 
            group
        )
        self.update(None, None)
        self.task = self.getTask()

    # def update(self):
    #     if not self.grabbed:
    #         self.image = self.imgs[self.status]
    #         self.rect = self.image.get_rect(
    #             topleft=(self.drawOn)
    #         )

    def getTask(self):
        if self.status == Drink.STATUS_NORMAL:
            return MovetoZoneTaskTakeRelease(
                self, "garbage", "cleaning", Objects.STATUS_DIRTY
            )
        elif self.status == Objects.STATUS_DIRTY:
            return CleanObjectRecoverZone(self, "garbage")
        else:
            print("NO STATUS FOUND")


class SlotMachine(Objects):

    def __init__(self,obj, group):
        super().__init__(obj.get("stGridx"), obj.get("stGridy"), "gambling", [], group,obj.get("drawOn"))
        self.imgs = [obj.get("image")]
        self.cost = 100
        self.profit = [0, 1, 5, 20, 50, 100]
        self.luck = [90, 5, 2, 1, 0.07, 0.03]
        self.task = self.getTask()

    def getTask(self):
        return MoveWorkObjMoney(self, "gambling", 20)

    def workOnObj(self):
        profit = self.profit
        luck = self.luck
        cost = self.cost
        ganancia = random.choices(profit, luck, k=1)[0] * cost
        if ganancia > 0:
            print(f"{ganancia=}")
        return ganancia - cost


class Machine(Objects):
    def __init__(self, obj, group):
        super().__init__(obj.get("stGridx"), obj.get("stGridy"), obj.get("type"), [], group,obj.get("drawOn"))
        self.available = True
        self.machine_type = obj.get("name")
        self.imgs = [obj.get("image")]
        self.task = self.getTask()
        self.offset_prod = obj.get("offset_prod")
        self.offset = obj.get("offset")
    def getTask(self):
        return None

    # def update(self, level, dt):
        # if not self.grabbed:
        #     self.image = self.imgs[self.status]
        #     self.rect = self.image.get_rect(topleft=(self.pos))

    def getSpot(self):
        return (self.x + self.offset[0], self.y+self.offset[1])

    def getNewObj(self, group, delivery, serveOn):
        return Drink(self.x+self.offset_prod[0], self.y+self.offset_prod[1],self.machine_type, group, delivery, serveOn)


class Sofa(Objects):

    def __init__(self,obj, group):
        super().__init__(obj.get("stGridx"), obj.get("stGridy"),obj.get("type"), [], group,obj.get("drawOn"))
        self.imgs = [obj.get("image")]
        self.task = self.getTask()

    def getTask(self):
        return MovetoObjWorkOffset(self, self.type, 40, (0, 1))


class Drink(Objects):
    idx_img_type = {
        "coffee" : 2,
        "drink"  : 0
    }
    def __init__(self, x, y, type, group, delivery_zone, serveOn):
        super().__init__(
            x,
            y,
            "thirst",
            [
                "hotel/objs/bar/drink_1.png",
                "hotel/objs/bar/drink_2.png",
                "hotel/objs/bar/drink_3.png",
            ],
            group,
            (0,0)
        )
        self.status = Drink.STATUS_TO_DELIVERY
        self.cost = 100
        self.serveOn = serveOn
        self.delivery_zone = delivery_zone
        self.type = type
        self.task = self.getTask()
        self.image = self.imgs[Drink.idx_img_type[self.type]]
        self.rect = self.image.get_rect(topleft=(0, 0))

    def getTask(self):
        ###  to Delivery : from Machine to Deliveryzone
        ###  to Servive  : from DeliveryZone to TableSpot (ServeOn)
        ###  Ready to be consumer : Task for customer to consume the obj
        if self.status == Drink.STATUS_TO_DELIVERY:
            return MoveObjToContainer(
                self, self.delivery_zone, "serving", Drink.STATUS_TOBE_SERVED
            )
        elif self.status == Drink.STATUS_TOBE_SERVED:
            return MoveObjFromContainerToContainer(
                self, self.delivery_zone, self.serveOn, "serving", Drink.STATUS_READY
            )
        elif self.status == Drink.STATUS_READY:
            return MoveConsumeObjMoney(self, "thirst", 40)

    def workOnObj(self):
        ganancia = 0
        return ganancia - self.cost

    def update(self, level, dt):
        if not self.grabbed:
            self.image = self.imgs[Drink.idx_img_type[self.type]]
            self.rect = self.image.get_rect(
                topleft=(
                    level.map.convertXGridToPX(self.x)+4,
                    level.map.convertYGridToPX(self.y),
                )
            )

    def getCurrentZone(self):
        ## STATUS_NORMAL = 0
        ## STATUS_DIRTY = 1
        ##  STATUS_CLEANING = 2
        ##  STATUS_LOCKED = 3
        ##  STATUS_TO_DELIVERY = 4
        ##  STATUS_TOBE_SERVED = 5
        ##  STATUS_READY = 6
        zones = [None for _ in range(7)]
        zones[Drink.STATUS_TO_DELIVERY] = None
        zones[Drink.STATUS_TOBE_SERVED] = self.delivery_zone
        zones[Drink.STATUS_READY] = self.serveOn
        return zones[self.status]
