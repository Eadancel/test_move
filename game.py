import pygame
import os
import pytmx
from pytmx.util_pygame import load_pygame
from people.people import People
from people.worker import Worker
from people.customer import Customer
from map.task import Task
from map.task import CleanObjectRecoverZone
from map.map import Map 
from map.objs.objects import Objects, Garbage, Sofa, SlotMachine, Drink
from display import Display
from collections import deque
from ui.ui import Label
import random

CREATE_NEW_CUSTOMER = True
PATH_maps = 'game_assets'
## "mapaCity.tmx"
class Game:
    teAddCustomer = pygame.USEREVENT+1
    teCheckingGarbage = pygame.USEREVENT+2
    def __init__(self):

        self.runDisplay = Display(os.path.join(PATH_maps,"hotel/Restaurante.tmx"))

        self.win = self.runDisplay.displayWindow
        self.lbM = LabelManager()
        label_font = self.lbM.labelCustomer
        
        self.map = Map(self.runDisplay)
        
        self.peoples = [Worker(30,9,"Worker 1",self,label_font), 
                        Worker(37,15,"Worker 2",self,label_font),
                        # Worker(6,4,"Worker 3",self,label_font), 
                        # Worker(1,4,"Worker 4",self,label_font),
                        # Worker(1,4,"Worker 5",self,label_font),
                        # Worker(1,4,"Worker 6",self,label_font),
                        # Customer(36,10,f"Customer Test",self,label_font),
                        # Customer(36,12,f"Customer Test",self,label_font),
                        ]
        #self.peoples = [Worker(5,2,self.map)]
        self.tasks = {}
        self.objects = deque([])
        self.tasks_doing = deque([])
        
        pygame.time.set_timer(Game.teAddCustomer, 5000)
        pygame.time.set_timer(Game.teCheckingGarbage, 1000)
        self.addObject(Sofa(38, 10))
        self.addObject(Sofa(42, 15))
        self.addObject(Garbage(45, 15))
        self.addObject(SlotMachine(41,13))
        self.addObject(SlotMachine(43,13))
        self.addObject(SlotMachine(45,13))
        self.addObject(SlotMachine(41,18))
        self.addObject(SlotMachine(43,18))
        self.addObject(SlotMachine(45,18))
        self.addObject(Drink(52,19))
        self.num_customer=0
    def run (self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("peoples :{}".format(len(self.peoples)))
                    run=False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    xGrid = self.map.convertPXToXGrid(pos[0])
                    yGrid = self.map.convertPXToYGrid(pos[1])
                    print(f"adding at {xGrid},{yGrid}")
                    self.addObject(Drink(xGrid, yGrid))
                elif event.type == Game.teAddCustomer:
                    if random.randint(1,10)>2 and len(self.peoples)<50 and CREATE_NEW_CUSTOMER:
                        self.num_customer+=1
                        self.peoples.append(Customer(32,10,f"Customer {self.num_customer}",self,self.lbM.labelCustomer))
                elif event.type == Game.teCheckingGarbage:
                    for p in self.peoples:
                        if p.type_person == People.TYPE_CUSTOMER:
                            if p.gotGarbage():
                                if self.map.isWalkable(p.x,p.y):
                                    #self.addGarbage(p.x,p.y)
                                    self.addObject(Garbage(p.x, p.y+1))
                                else:
                                    print("not walkable gargabe".format(p.x,p.y))
                            
            self.draw()
        pygame.quit()

    def draw(self):
        #self.win.blit(self.bg,(0,0))

        #for t in self.tasks_doing:
         #   t.draw(self.win, self.map)
        for t in self.objects:
            if t.grabbed==False:
                if t.status==Objects.STATUS_DIRTY:
                    t.status=Objects.STATUS_CLEANING
                    self.addTask(CleanObjectRecoverZone(t,"garbage"))
                t.draw(self.win, self.map)

        for p in self.peoples:
            p.draw(self.win)

            # if p.type_person == People.TYPE_WORKER and p.openForTask and len(self.tasks)>0 :
            #     tsk = self.tasks.popleft()
            #     tsk.status = Task.STATUS_DOING
            #     p.assignTask(tsk)
            
                #self.tasks_doing.append(tsk)
            if p.status == People.STATUS_LEAVING:
                #print(f"removing customer {p.id}")
                self.peoples.remove(p)


        if len(self.tasks_doing)>15:
            self.tasks_doing.popleft()
        
        self.runDisplay.info = f"People: {len(self.peoples)} Task Cleaning: {len(self.tasks.get('resting',{}))} ZoneGame:{len(self.tasks.get('gambling',{}))} Objects: {len(self.objects)}" 
        
        self.runDisplay.displayLoop()

    def addObject(self, obj):
        self.objects.append(obj)
        self.addTask(obj.task)
    
    def turnIntoGarbage(self, obj):
        self.addObject(Garbage(obj.x,obj.y))
        self.removeObj(obj)

    def removeObj(self, obj):
        self.objects.remove(obj)

    def getTaskbyNeed(self, need):
        if need in self.tasks:
            if len(self.tasks[need])>0:
                return self.tasks[need].popleft()
            else:
                return None
        else:
            return None

    def addTask(self, task):
        if task.need in self.tasks:
            self.tasks[task.need].append(task)
        else:
            self.tasks[task.need] = deque([task])

    def addObjectAt(self, obj):
        if self.map.isWalkable(obj.x,obj.y):
            self.addObject(obj)
        else:
            print("not walkable {} {}".format(obj.x,obj.y))

class LabelManager():
    def __init__(self):
        self.labelCustomer = pygame.font.Font(None, 12)
        self.labelTitle = pygame.font.Font(None, 20)