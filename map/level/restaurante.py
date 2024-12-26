import random

import pygame

from map.level.level import LabelManager, Level
from map.objs.objects import (Container, Drink, Garbage, Machine, Objects, SlotMachine,
                              Sofa)
from map.task import CleanObjectRecoverZone, PrepareDrink
from people.bartender import Bartender
from people.cleaner import Cleaner
from people.customer import Customer
from people.people import *
from settings import *

CREATE_NEW_CUSTOMER = True 


class LevelRestaurante(Level):
    teAddCustomer = pygame.USEREVENT + 100
    teCheckingGarbage = pygame.USEREVENT + 200
    
    def __init__(self):
        super().__init__(maps_tmx["restaurante"])
        self.lm = LabelManager()
        self.machines = {}
        self.containers = {}
        self.happiness=100
        self.setup()
        self.pending_tasks=[]
    def setup(self):
        self.num_customer = 0
        self.addWorker(30, 9, "Worker 1")
        self.addWorker(30, 9, "Worker 2")
        self.addWorker(30, 9, "Worker 3")
        self.addBartener(30, 9, "Bartender 1")
        self.addBartener(30, 9, "Bartender 2")
        # self.addCustomer(32,10)
        pygame.time.set_timer(LevelRestaurante.teAddCustomer, 5000)
        pygame.time.set_timer(LevelRestaurante.teCheckingGarbage, 1000)

        # Sofas layer "sofa"
        try:
            for sofa in self.map.get_objs_per_layer("sofas"):
                self.addObject(Sofa(sofa,self.all_sprites))
        except:
            print("Error in Sofa")

        
        # SlotMachine
        try:
            for slot in self.map.get_objs_per_layer("games"):
                self.addObject(SlotMachine(slot, self.all_sprites))
        except:
            print("Error in Games")

        for obj in self.map.get_objs_per_layer("drinks"):

            if obj.get("type") == "machine":
                self.addMachine(Machine(obj, self.all_sprites))
            if obj.get("type") == "container":
                self.addContainer(Container(obj,self.all_sprites))

        # self.addObject(Sofa(42, 15, self.all_sprites))
        self.addObjectOnMap(Garbage(52, 10, self.all_sprites))
        # self.addObject(Drink(52,19, self.all_sprites))

    def addMachine(self,machine ):
        if machine.machine_type in self.machines:
            self.machines[machine.machine_type].append(machine)
        else:
            self.machines[machine.machine_type] = []
            self.machines[machine.machine_type].append(machine)

    def addContainer(self,container):
        if container.container_type in self.containers:
            self.containers[container.container_type].append(container)
        else:
            self.containers[container.container_type] = []
            self.containers[container.container_type].append(container)

    def getAvailableMachine(self, machine_type):
        #print(self.machines)

        for m in self.machines.get(machine_type, []):
            if m.available:
                return m
        return None

    def getAvailableContainer(self, container_type):

        for c in self.containers.get(container_type, []):
            if c.checkAvailableSlot():
                return c
        return None

    def getAvailableContSlots(self,container_type):
        l = ""
        for c in self.containers.get(container_type, []):
            l = l + f" {len(c.objs)}"

        return l

    def input(self, event):
        LEFT = 1
        MIDDLE = 2
        RIGHT = 3
        super().input(event)
        if event.type == pygame.MOUSEBUTTONUP and event.button == MIDDLE:
            pos = pygame.mouse.get_pos()
            relative_pos = self.all_sprites.relaPosZoom(pos)
            print(f"{relative_pos=}")
            xGrid = self.map.convertPXToXGrid(relative_pos[0])
            yGrid = self.map.convertPXToYGrid(relative_pos[1])
            print(f"adding at {xGrid},{yGrid}    {pos=}  {relative_pos=}")
            if self.map.isWalkable(xGrid, yGrid):
                self.addObjectOnMap(Garbage(xGrid, yGrid, self.all_sprites))
        elif event.type == pygame.MOUSEBUTTONUP and event.button == RIGHT:
            pos = pygame.mouse.get_pos()
            relative_pos = self.all_sprites.relaPosZoom(pos)
            print(f"{relative_pos=}")
            xGrid = self.map.convertPXToXGrid(relative_pos[0])
            yGrid = self.map.convertPXToYGrid(relative_pos[1])
            print(f"adding OrderDrink at {xGrid},{yGrid}    {pos=}  {relative_pos=}")
            self.createOrderDrink((xGrid, yGrid), random.choice(["coffee","drink"]))
        elif event.type == LevelRestaurante.teAddCustomer:
            if (
                random.randint(0, 10) < self.happiness  ## customer rate based on restaurante happiness
                and len(self.peoples) < 50
                and CREATE_NEW_CUSTOMER
            ):
                self.addCustomer(32, 10)

        elif event.type == LevelRestaurante.teCheckingGarbage:
            for p in self.peoples:
                if p.type_person == People.TYPE_CUSTOMER:
                    if p.gotGarbage():
                        if self.map.isWalkable(p.x, p.y):
                            # self.addGarbage(p.x,p.y)
                            print(f"adding customer garbagfe at {p.x},{p.y+1} ")
                            self.addObjectOnMap(Garbage(p.x, p.y + 1, self.all_sprites))
                        else:
                            print("not walkable gargabe {} {}".format(p.x, p.y))

    def update(self, dt):
        super().update(dt)
        self.checkPendingOrders()
        #Processing People
        sum_frust=0
        i=0
        for p in self.peoples:
            if isinstance(p, Customer):
                sum_frust += p.happiness
                i+=1
                if p.status == People.STATUS_LEAVING:
                    print(f"removing customer {p.id}")
                    self.peoples.remove(p)
                    p.kill()
            if p.get_rect().collidepoint(pygame.mouse.get_pos()):
                self.tooltip['visible']=True
                self.tooltip['html_text']=p.get_tooltip()
                self.tooltip['rect'] = p.get_rect()
        self.happiness = sum_frust/i if i>0 else 100
        self.stage['happy avg'] = f"{self.happiness:.2f}"
        self.stage['num customer'] = i
        #Processing Machines
        self.stage['MoneySlot']=0

        slot_stage=[]
        for m in self.objects:
            if isinstance(m,SlotMachine):
                self.stage['MoneySlot']+=m.stage['money']
                slot_stage.append(m.get_stage())

            if m.get_rect().collidepoint(pygame.mouse.get_pos()):
                self.tooltip['visible']=True
                self.tooltip['html_text']=m.get_tooltip()
                self.tooltip['rect'] = m.get_rect()

        #self.stage["Slots_stage"] = slot_stage
    def addWorker(self, x, y, id):
        self.peoples.append(Cleaner(x, y, id, self))

    def addBartener(self, x, y, id):
        self.peoples.append(Bartender(x, y, id, self))

    def addCustomer(self, x, y):
        self.num_customer += 1
        self.peoples.append(Customer(x, y, f"Customer {self.num_customer}", self))

    def turnIntoGarbage(self, obj):
        print(f"turning into garbage {obj.x=} {obj.y=}")
        self.addObjectOnMap(Garbage(obj.x, obj.y, self.all_sprites))
        self.removeObj(obj)

    def createOrderDrink(self, serveOn, type):

        self.pending_tasks.append((type,serveOn))

    def checkPendingOrders(self):

        for type,serveOn in self.pending_tasks:
            machine = self.getAvailableMachine(type)
            cont_delivery = self.getAvailableContainer("drink_delivery")
            cont_serveOn = self.getAvailableContainer("drink_serveOn")

            if machine:
                if cont_delivery:
                    if cont_serveOn :
                        print("preparing drink")
                        self.addTask(
                            PrepareDrink(machine, "prepare_drink", 25, cont_delivery, cont_serveOn)
                        )
                        self.pending_tasks.remove((type,serveOn))
