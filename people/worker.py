import pygame
import os
import people
from map.task import Task
from map.action import Action
from .people import People
import random
    # DIREC_MOVING_STAY = 0
    # DIREC_MOVING_UP = 1
    # DIREC_MOVING_DOWN = 2
    # DIREC_MOVING_LEFT = 3
    # DIREC_MOVING_RIGHT = 4
pathimgs_status = (["tile_0267.png"],
                   ["tile_0268.png","tile_0295.png","tile_0322.png"],
                   ["tile_0267.png","tile_0294.png","tile_0321.png"],
                   ["tile_0266.png","tile_0293.png","tile_0320.png"],
                   ["tile_0269.png","tile_0296.png","tile_0323.png"])

class Worker (People):
    def __init__(self,x,y,map):
        super().__init__(x,y,People.TYPE_WORKER,map)
        self.imgs = []
        self.openForTask=True
        for i in range(5):
            self.imgs.append([])
            for pi in pathimgs_status[i]:
                self.imgs[i].append(pygame.image.load(os.path.join("game_assets/Tiles",pi)))

    def do(self):
        #print ("tasks:{}".format(len(self.tasks)))
        if self.status == People.STATUS_IDLE or (self.openForTask and len(self.tasks)>0):
            self.getNextTask()
        elif  self.status == People.STATUS_GOINGTO:
            #print(self.openForTask)
            #print ("tasks:{}".format(len(self.tasks)))
            self.move()
        elif  self.status == People.STATUS_WORKING:
            self.working()

    def getNextTask(self):

        if (self.currentTask==None or len(self.currentTask.solution)<=0):
            if len(self.tasks)>0 :
                self.currentTask = self.tasks.popleft()
            else:
                self.assignTask(Task([{"type":Action.TYPE_GOTO_ZONE,"zone":"rest_zone","canInterrup":True,"drop":False,"velocity":0.5}],random.randint(1,20)))
                return
        self.current_action = self.currentTask.solution.popleft()
        if "canInterrup" in self.current_action:
            self.openForTask=self.current_action["canInterrup"]
        else:
            self.openForTask=False

        if "velocity" in self.current_action:
            self.velocity_modif=self.current_action["velocity"]
        else:
            self.velocity_modif=1

        if self.current_action["type"]==Action.TYPE_GOTO_X_Y:
            self.status = People.STATUS_GOINGTO
            self.currentPath = self.map.getWalkablePathFromToGrid(self.x, self.y, self.current_action["x"], self.current_action["y"])

        elif self.current_action["type"]==Action.TYPE_GOTO_ZONE:
            self.status = People.STATUS_GOINGTO
            (x_zone,y_zone)=self.map.getEmptySpotOnZone(self.current_action["zone"], self.current_action["drop"])
            if x_zone>0 and y_zone>0:
                self.currentPath = self.map.getWalkablePathFromToGrid(self.x, self.y, x_zone, y_zone)
            else:
                print("Zone FULL")
        elif self.current_action["type"]==Action.TYPE_TAKE_OBJ:
            self.obj=self.current_action["obj"]
            self.obj.grabbed=True
        elif self.current_action["type"]==Action.TYPE_RELEASE_OBJ:
            self.obj.grabbed=False
            self.obj=None
        #print(self.currentPath)

    def working(self):
        self.currentTask.workingOn(self.working_force)
        if self.currentTask.status == Task.STATUS_DONE:
            self.status=People.STATUS_IDLE
        else:
            self.status=People.STATUS_WORKING