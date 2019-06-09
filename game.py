import pygame
import os
import pytmx
from pytmx.util_pygame import load_pygame
from people.people import People
from people.worker import Worker
from map.task import Task
from map.map import Map
from display import Display
from collections import deque

class Game:
    def __init__(self):

        self.runDisplay = Display("mapaReducido.tmx")

        self.win = self.runDisplay.displayWindow

        self.map = Map(self.runDisplay.map.gameMap.tilewidth,self.runDisplay.map.gameMap.tileheight, self.runDisplay.map.walkableTiles)
        self.peoples = [Worker(5,2,self.map), Worker(10,4,self.map),Worker(6,4,self.map), Worker(1,4,self.map)]
        self.tasks = deque([])
        self.tasks_doing = deque([])
        #self.bg = pygame.image.load(os.path.join("game_assets","bg.png"))

    def run (self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run=False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.addTaskAt(pygame.mouse.get_pos())
            self.draw()
        pygame.quit()

    def draw(self):
        #self.win.blit(self.bg,(0,0))
        for t in self.tasks:
            t.draw(self.win, self.map)
        for t in self.tasks_doing:
            t.draw(self.win, self.map)
        for p in self.peoples:
            p.draw(self.win)
            if p.type_person == People.TYPE_WORKER and p.status == People.STATUS_IDLE and len(self.tasks)>0 :
                tsk = self.tasks.popleft()
                tsk.status = Task.STATUS_DOING
                p.assignTask(tsk)
                self.tasks_doing.append(tsk)
        if len(self.tasks_doing)>15:
            self.tasks_doing.popleft()
        self.runDisplay.displayLoop()

    def addTaskAt(self, pos):
        xGrid = self.map.convertPXToXGrid(pos[0])
        yGrid = self.map.convertPXToYGrid(pos[1])
        if self.map.isWalkable(xGrid,yGrid):
            self.tasks.append(Task(xGrid, yGrid,20))
            #print("{} {}".format(xGrid, yGrid ))
        else:
            print("not walkable {} {}".format(xGrid,yGrid))
