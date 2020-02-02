import pygame
import os
import people
from map.task import Task
from map.action import Action
from .people import People
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
        for i in range(5):
            self.imgs.append([])
            for pi in pathimgs_status[i]:
                self.imgs[i].append(pygame.image.load(os.path.join("game_assets/Tiles",pi)))

    def do(self):
        if self.status == People.STATUS_IDLE:
            self.getNextTask()
        elif  self.status == People.STATUS_GOINGTO:
            self.move()
        elif  self.status == People.STATUS_WORKING:
            self.working()

    def getNextTask(self):
        if (self.currentTask==None or len(self.currentTask.solution)<=0):
            if len(self.tasks)>0 :
                self.currentTask = self.tasks.popleft()
            else:
                return

        action = self.currentTask.solution.popleft()
        if action["type"]==Action.TYPE_GOTO_X_Y:
            self.status = People.STATUS_GOINGTO
            self.currentPath = self.map.getWalkablePathFromToGrid(self.x, self.y, action["x"], action["y"])
        elif action["type"]==Action.TYPE_GOTO_ZONE:
            self.status = People.STATUS_GOINGTO
            (x_zone,y_zone)=self.map.getEmptySpotOnZone(action["zone"])
            if x_zone>0 and y_zone>0:
                self.currentPath = self.map.getWalkablePathFromToGrid(self.x, self.y, x_zone, y_zone)
            else:
                print("Zone FULL")
        elif action["type"]==Action.TYPE_TAKE_OBJ:
            self.obj=action["obj"]
            self.obj.grabbed=True
        elif action["type"]==Action.TYPE_RELEASE_OBJ:
            self.obj.grabbed=False
            self.obj=None
        #print(self.currentPath)

    def working(self):
        self.currentTask.workingOn(self.working_force)
        if self.currentTask.status == Task.STATUS_DONE:
            self.status=People.STATUS_IDLE
        else:
            self.status=People.STATUS_WORKING