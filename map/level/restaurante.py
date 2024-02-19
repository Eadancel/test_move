

import pygame
from map.level.level import Level, LabelManager
from map.objs.objects import Objects, Garbage, Sofa, SlotMachine, Drink
from map.task import CleanObjectRecoverZone
from people.people import *
from people.customer import Customer
from people.worker import Worker
from settings import *
import random

CREATE_NEW_CUSTOMER = False

class LevelRestaurante(Level):
    teAddCustomer = pygame.USEREVENT+1
    teCheckingGarbage = pygame.USEREVENT+2
    def __init__(self):
        super().__init__(maps_tmx['restaurante'])
        self.lm = LabelManager()
                
        self.setup()


    def setup(self):
        self.num_customer=0
        self.addWorker(30,9,"Worker 1")
        #self.addWorker(37,15,"Worker 2")
        #self.addCustomer(32,10)
        pygame.time.set_timer(LevelRestaurante.teAddCustomer, 5000)
        pygame.time.set_timer(LevelRestaurante.teCheckingGarbage, 1000)
        self.addObject(Sofa(38, 10, self.all_sprites))
        self.addObject(Sofa(42, 15, self.all_sprites))
        self.addObject(Garbage(52, 10, self.all_sprites))
        self.addObject(SlotMachine(41,13, self.all_sprites))
        self.addObject(SlotMachine(43,13, self.all_sprites))
        self.addObject(SlotMachine(45,13, self.all_sprites))
        self.addObject(SlotMachine(41,18, self.all_sprites))
        self.addObject(SlotMachine(43,18, self.all_sprites))
        self.addObject(SlotMachine(45,18, self.all_sprites))
        self.addObject(Drink(52,19, self.all_sprites))


    def input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                xGrid = self.map.convertPXToXGrid(pos[0])
                yGrid = self.map.convertPXToYGrid(pos[1])
                print(f"adding at {xGrid},{yGrid}")
                self.addObject(Drink(xGrid, yGrid, self.all_sprites))
        elif event.type == LevelRestaurante.teAddCustomer:
            if random.randint(1,10)>2 and len(self.peoples)<50 and CREATE_NEW_CUSTOMER:
                self.addCustomer(32,10)
                
        elif event.type == LevelRestaurante.teCheckingGarbage:
            for p in self.peoples:
                if p.type_person == People.TYPE_CUSTOMER:
                    if p.gotGarbage():
                        if self.map.isWalkable(p.x,p.y):
                            #self.addGarbage(p.x,p.y)
                            self.addObject(Garbage(p.x, p.y+1, self.all_sprites))
                        else:
                            print("not walkable gargabe".format(p.x,p.y))
    def update(self, dt):
 
        for t in self.objects:
            if t.grabbed==False:
                if t.status==Objects.STATUS_DIRTY:
                    t.status=Objects.STATUS_CLEANING
                    self.addTask(CleanObjectRecoverZone(t,"garbage"))

        for p in self.peoples:
            if p.status == People.STATUS_LEAVING:
                #print(f"removing customer {p.id}")
                self.peoples.remove(p)    

    def addWorker(self,x,y, id):
        self.peoples.append(Worker(x,y, id,self))
    
    def addCustomer(self,x,y):
        self.num_customer+=1
        self.peoples.append(Customer(x,y,f"Customer {self.num_customer}",self))
    
    def turnIntoGarbage(self, obj):
        self.addObject(Garbage(obj.x,obj.y))
        self.removeObj(obj)