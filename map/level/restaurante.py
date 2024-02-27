

import pygame
from map.level.level import Level, LabelManager
from map.objs.objects import Machine, Objects, Garbage, Sofa, SlotMachine, Drink
from map.task import CleanObjectRecoverZone, PrepareDrink
from people.bartender import Bartender
from people.cleaner import Cleaner
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
        self.machines = {}
        self.setup()


    def setup(self):
        self.num_customer=0
        self.addWorker(30,9,"Worker 1")
        self.addWorker(30,9,"Worker 2")
        self.addWorker(30,9,"Worker 3")
        self.addBartener(30,9, "Bartender 1")
        #self.addCustomer(32,10)
        pygame.time.set_timer(LevelRestaurante.teAddCustomer, 5000)
        pygame.time.set_timer(LevelRestaurante.teCheckingGarbage, 1000)

        #Sofas layer "sofa"
        try:
            for obj in self.bkgmap.gameMap.get_layer_by_name("sofas"):
                #print(dir(obj))
                xGrid = self.map.convertPXToXGrid(obj.x)
                yGrid = self.map.convertPXToYGrid(obj.y)
                self.addObject(Sofa(xGrid,yGrid, self.all_sprites,[obj.image], obj.type))
        except:
            print("Error in Sofa")
        try:
            for obj in self.bkgmap.gameMap.get_layer_by_name("games"):
                xGrid = self.map.convertPXToXGrid(obj.x)
                yGrid = self.map.convertPXToYGrid(obj.y)
                self.addObject(SlotMachine(xGrid,yGrid, self.all_sprites,[obj.image]))
        except:
            print("Error in Games")


        for obj in self.bkgmap.gameMap.get_layer_by_name("drinks"):
            if obj.type=='machine':
                machine = Machine(0,0,self.all_sprites,[obj.image],obj.type, obj.name,(obj.x, obj.y))
                #self.machines[machine.machine_type] = machine
                self.addMachine(machine)

        #self.addObject(Sofa(42, 15, self.all_sprites))
        self.addObject(Garbage(52, 10, self.all_sprites))
        #self.addObject(Drink(52,19, self.all_sprites))


    def addMachine(self, machine):
        if machine.machine_type in self.machines:
            self.machines[machine.machine_type].append(machine)
        else:
            self.machines[machine.machine_type] = []
            self.machines[machine.machine_type].append(machine)

    def getAvailableMachine(self, machine_type):
        print(self.machines)

        for m in self.machines.get(machine_type, []):
            if m.available: return m
        return None
    def input(self, event):
        LEFT = 1
        MIDDLE = 2
        RIGHT = 3
        super().input(event)
        if event.type == pygame.MOUSEBUTTONUP and event.button == MIDDLE :
                pos = pygame.mouse.get_pos()
                relative_pos = self.all_sprites.relaPosZoom(pos)
                print (f"{relative_pos=}")
                xGrid = self.map.convertPXToXGrid(relative_pos[0])
                yGrid = self.map.convertPXToYGrid(relative_pos[1])
                print(f"adding at {xGrid},{yGrid}    {pos=}  {relative_pos=}")
                if self.map.isWalkable(xGrid,yGrid):
                    self.addObject(Garbage(xGrid, yGrid, self.all_sprites))
        elif event.type == pygame.MOUSEBUTTONUP and event.button == RIGHT :
                pos = pygame.mouse.get_pos()
                relative_pos = self.all_sprites.relaPosZoom(pos)
                print (f"{relative_pos=}")
                xGrid = self.map.convertPXToXGrid(relative_pos[0])
                yGrid = self.map.convertPXToYGrid(relative_pos[1])
                print(f"adding OrderDrink at {xGrid},{yGrid}    {pos=}  {relative_pos=}")
                self.createOrderDrink((xGrid,yGrid))
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
 
        # for t in self.objects:
        #     if t.grabbed==False:
        #         if t.status==Objects.STATUS_DIRTY:
        #             t.status=Objects.STATUS_CLEANING
        #             #self.addTask(CleanObjectRecoverZone(t,"garbage"))

        for p in self.peoples:
            if p.status == People.STATUS_LEAVING:
                print(f"removing customer {p.id}")
                self.peoples.remove(p)
                p.kill()

    def addWorker(self,x,y, id):
        self.peoples.append(Cleaner(x,y, id,self))
    
    def addBartener(self,x,y, id):
        self.peoples.append(Bartender(x,y, id,self))
    
    def addCustomer(self,x,y):
        self.num_customer+=1
        self.peoples.append(Customer(x,y,f"Customer {self.num_customer}",self))
    
    def turnIntoGarbage(self, obj):
        self.addObject(Garbage(obj.x,obj.y, self.all_sprites))
        self.removeObj(obj)
    
    def createOrderDrink(self,pos):
        #create new zone:
        newZone="Order 1"
        if newZone not in self.map.zones.keys():
                self.map.zones[newZone]=deque([])
                self.map.zones[newZone].append(pos)
        self.addTask(PrepareDrink("coffee","prepare_drink",50,"drink_delivery",newZone, Drink.STATUS_READY))
        