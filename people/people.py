
import pygame

from collections import deque
class People:
    imgs = []
    TYPE_WORKER = 1
    TYPE_PEDESTRIAN = 2

    STATUS_IDLE = 0
    STATUS_GOINGTO = 1
    STATUS_WORKING = 2
    def __init__(self, x, y, type_person,map):
        self.x = x
        self.y = y
        self.map = map
        self.xGrid = self.map.convertXGridToPX(x)
        self.yGrid = self.map.convertYGridToPX(y)
        self.animation_count = 0
        self.tasks = deque([])
        self.img = None
        self.type_person = type_person
        self.status = People.STATUS_IDLE
        self.currentTask = None
        self.currentPath = deque([])
        self.nextPos = None
        self.velocity = 100
    def draw(self, win):
        """
        draw the people
        """
        
        self.img = self.imgs[self.animation_count]
        self.animation_count += 1
        
        if self.animation_count >= len(self.imgs):
            self.animation_count = 0 
        win.blit(self.img, (self.xGrid, self.yGrid))
        self.do()

    def assignTask(self, tsk):
        print ("adding task")
        self.tasks.append(tsk)
    def do(self):
        if self.status == People.STATUS_IDLE and len(self.tasks)>0:
            self.getNextTask()
        elif  self.status == People.STATUS_GOINGTO:
            self.move()
        elif  self.status == People.STATUS_WORKING:
            self.working()
    def getNextTask(self):
        self.currentTask = self.tasks.popleft()
        self.status = People.STATUS_GOINGTO
        self.currentPath = self.map.getPathFromTo(self.x, self.y, self.currentTask.x, self.currentTask.y)
    def move(self):
        if len(self.currentPath)>0 and self.nextPos==None:
            self.nextPos=self.currentPath.popleft()
        if self.nextPos!=None :
            self.moveTo()
        else:
            self.status = People.STATUS_IDLE
        
    def working(self):
        pass
    def moveTo(self):
        nextXGrid = self.map.convertXGridToPX(self.nextPos[0])
        nextYGrid = self.map.convertYGridToPX(self.nextPos[1])
        # print("moving to {} {} - {} {}".format(nextXGrid,nextYGrid,self.nextPos[0],self.nextPos[1]))
        # print("on position {} {}".format(self.xGrid,self.yGrid))
        
        if self.x<self.nextPos[0]:
            self.xGrid+=self.velocity/100
        elif self.x>self.nextPos[0]:
            self.xGrid-=self.velocity/100
        if abs(self.xGrid-nextXGrid)<2:
            self.x=self.nextPos[0]
            self.xGrid=nextXGrid

        if self.y<self.nextPos[1]:
            self.yGrid+=self.velocity/100
        elif self.y<self.nextPos[1]:
            self.yGrid-=self.velocity/100
        if abs(self.yGrid-nextYGrid)<2:
            self.y=self.nextPos[1]
            self.yGrid=nextYGrid
        
        if self.x==self.nextPos[0] and self.y==self.nextPos[1]:
            self.nextPos=None
        
        

