
import pygame
import math
from map.task import Task
from collections import deque
class People:
    imgs = []
    TYPE_WORKER = 1
    TYPE_PEDESTRIAN = 2

    STATUS_IDLE = 0
    STATUS_GOINGTO = 1
    STATUS_WORKING = 2

    DIREC_MOVING_STAY = 0
    DIREC_MOVING_UP = 1
    DIREC_MOVING_DOWN = 2
    DIREC_MOVING_LEFT = 3
    DIREC_MOVING_RIGHT = 4

    FREQ_ANIMATION = 30

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
        self.velocity = 120
        self.working_force = 100
        self.direcMoving = People.DIREC_MOVING_STAY
        self.obj=None
    def draw(self, win):
        """
        draw the people
        """
        idx = math.trunc( self.animation_count/(People.FREQ_ANIMATION/len(self.imgs[self.direcMoving])))

        self.img = self.imgs[self.direcMoving][idx]
        self.animation_count += 1

        if self.animation_count >=  People.FREQ_ANIMATION - 1:
            self.animation_count = 0

        self.do()
        win.blit(self.img, (self.xGrid, self.yGrid))
        if self.obj!=None:
            self.obj.drawOn(win,self.xGrid-5, self.yGrid)

    def assignTask(self, tsk):
        self.tasks.append(tsk)

    def move(self):
        if len(self.currentPath)>0 and self.nextPos==None:
            self.nextPos=self.currentPath.pop(0)
        if self.nextPos!=None :
            self.moveTo()
        else:
            self.status = People.STATUS_IDLE

    def moveTo(self):
        nextXGrid = self.map.convertXGridToPX(self.nextPos[0])
        nextYGrid = self.map.convertYGridToPX(self.nextPos[1])
        # print("moving to {} {} - {} {}".format(nextXGrid,nextYGrid,self.nextPos[0],self.nextPos[1]))
        # print("on position {} {}".format(self.xGrid,self.yGrid))
        if self.y<self.nextPos[1]:
            self.direcMoving = People.DIREC_MOVING_DOWN
            self.yGrid+=self.velocity/100
        elif self.y>self.nextPos[1]:
            self.direcMoving = People.DIREC_MOVING_UP
            self.yGrid-=self.velocity/100

        if self.x<self.nextPos[0]:
            self.xGrid+=self.velocity/100
            self.direcMoving = People.DIREC_MOVING_RIGHT
        elif self.x>self.nextPos[0]:
            self.direcMoving = People.DIREC_MOVING_LEFT
            self.xGrid-=self.velocity/100


        if abs(self.yGrid-nextYGrid)<2:
            self.y=self.nextPos[1]
            self.yGrid=nextYGrid
        if abs(self.xGrid-nextXGrid)<2:
            self.x=self.nextPos[0]
            self.xGrid=nextXGrid

        if self.x==self.nextPos[0] and self.y==self.nextPos[1]:
            self.direcMoving = People.DIREC_MOVING_STAY
            self.nextPos=None
        if self.obj!=None:
            self.obj.x=self.x
            self.obj.y=self.y



