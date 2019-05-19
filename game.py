import pygame
import os
from people.people import People
from people.worker import Worker
from map.task import Task
from map.map import Map
from collections import deque

class Game:
    def __init__(self):
        self.width = 960
        self.height = 480
        self.map = Map(16,16)
        self.win = pygame.display.set_mode((self.width, self.height))
        self.peoples = [Worker(5,2,self.map), Worker(10,4,self.map)] 
        self.tasks = deque([])
        self.bg = pygame.image.load(os.path.join("game_assets","bg.png"))
        
    def run (self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run=False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.addTaskAt(pygame.mouse.get_pos())
            self.draw()
        pygame.quit()

    def draw(self):
        self.win.blit(self.bg,(0,0))
        for p in self.peoples:
            p.draw(self.win)
            if p.type_person == People.TYPE_WORKER and p.status == People.STATUS_IDLE and len(self.tasks)>0 :
                p.assignTask(self.tasks.popleft())
        for t in self.tasks:
            t.draw(self.win, self.map)
        pygame.display.update()

    def addTaskAt(self, pos):
        xGrid = self.map.convertPXToXGrid(pos[0])
        yGrid = self.map.convertPXToYGrid(pos[1])
        self.tasks.append(Task(xGrid, yGrid,20))
        print("{} {}".format(xGrid, yGrid ))