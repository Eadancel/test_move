import pygame
import os
import pytmx
from pytmx.util_pygame import load_pygame
from people.people import People
from people.worker import Worker
from people.customer import Customer
from map.task import Task
from map.task import MovetoZoneTask
from map.task import CleanObjectRecoverZone
from map.map import Map
from map.objs.garbage import Garbage
from map.objects import Objects
from display import Display
from collections import deque

def getNewObject(x,y):
    return Garbage(x,y)

class Game:
    def __init__(self):

        self.runDisplay = Display("mapaReducido.tmx")

        self.win = self.runDisplay.displayWindow
        label_font = pygame.font.Font(None, 10)
        self.map = Map(self.runDisplay.map.gameMap.tilewidth,self.runDisplay.map.gameMap.tileheight, self.runDisplay.map.walkableTiles, self.runDisplay.map.zones)
        self.peoples = [Worker(5,2,self.map,label_font), Worker(10,4,self.map,label_font),
                        Worker(6,4,self.map,label_font), Worker(1,4,self.map,label_font),
                        Customer(36,2,self.map,label_font),
                        Customer(36,2,self.map,label_font),
                        Customer(36,2,self.map,label_font),
                        Customer(36,2,self.map,label_font),
                        Customer(36,2,self.map,label_font),
                        Customer(36,2,self.map,label_font)]
        #self.peoples = [Worker(5,2,self.map)]
        self.tasks = deque([])
        self.objects = deque([])
        self.tasks_doing = deque([])
        #self.bg = pygame.image.load(os.path.join("game_assets","bg.png"))

    def run (self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run=False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.addObjectAt(pygame.mouse.get_pos())
            self.draw()
        pygame.quit()

    def draw(self):
        #self.win.blit(self.bg,(0,0))

        #for t in self.tasks_doing:
         #   t.draw(self.win, self.map)

        for p in self.peoples:
            p.draw(self.win)

            if p.type_person == People.TYPE_WORKER and p.openForTask and len(self.tasks)>0 :
                tsk = self.tasks.popleft()
                tsk.status = Task.STATUS_DOING
                p.assignTask(tsk)
            elif p.type_person == People.TYPE_CUSTOMER:
                if p.gotGarbage():
                    if self.map.isWalkable(p.x,p.y):
                        self.addGarbage(p.x,p.y)
                    else:
                        print("not walkable gargabe".format(p.x,p.y))
                #self.tasks_doing.append(tsk)
        for t in self.objects:
            if t.grabbed==False:
                if t.status==Objects.STATUS_DIRTY:
                    t.status=Objects.STATUS_CLEANING
                    self.tasks.append(CleanObjectRecoverZone(t,"garbage_zone"))
                t.draw(self.win, self.map)

        if len(self.tasks_doing)>15:
            self.tasks_doing.popleft()
        self.runDisplay.displayLoop()

    def addGarbage(self, x, y):
        #print("adding garbage{} {}".format(x, y))
        obj=Garbage(x,y)
        self.objects.append(obj)
        self.tasks.append(MovetoZoneTask(obj,"garbage_zone"))

    def addObjectAt(self, pos):
        xGrid = self.map.convertPXToXGrid(pos[0])
        yGrid = self.map.convertPXToYGrid(pos[1])
        if self.map.isWalkable(xGrid,yGrid):
            self.addGarbage(xGrid,yGrid)
        else:
            print("not walkable {} {}".format(xGrid,yGrid))

class CustomerManager():
    def __init__(self):
        self.customers=[Customer(36,2,self.map,label_font),
                        Customer(36,2,self.map,label_font),
                        Customer(36,2,self.map,label_font),
                        Customer(36,2,self.map,label_font),
                        Customer(36,2,self.map,label_font),
                        Customer(36,2,self.map,label_font)]
    def draw(self):
        pass