import pygame
import os
import people
from map.task import Task, WanderTask
from map.action import Action
from .people import People
from people.need import Need, NeedCleaning, NeedResting
import random






class Worker (People):
    def __init__(self,x,y,id,level):
        super().__init__(x,y,id,People.TYPE_WORKER,level)
        self.imgs = []
        self.openForTask=True

        self.intensity = random.randint(1,5)
        #self.needs = {}
        self.needs = { "staff_resting": NeedResting(random.randint(1,10))}

    def getNextTask(self):
        super().getNextTask()
        if self.current_action["type"]==Action.TYPE_TAKE_OBJ:
            self.obj=self.current_action["obj"]
            self.obj.grabbed=True
            #self.obj.visible = False
        elif self.current_action["type"]==Action.TYPE_RELEASE_OBJ:
            self.obj.grabbed=False
            #self.obj.visible = True
            self.obj=None
        elif self.current_action["type"]==Action.TYPE_MAKE_VISIBLE:           
            self.game.removeObj(self.current_action["obj"])
            self.obj=None

        elif self.current_action["type"] in (Action.TYPE_TASKWORK, Action.TYPE_TASKWORK_OBJ):
            self.status=People.STATUS_WORKING
        
        #print(self.currentPath)

    def working(self):
        value = self.current_action['value']
        need = self.currentTask.need
        self.needs[need].doDecrement(value)
        
        if self.needs[need].isSolved():
                self.status=People.STATUS_IDLE
                self.needs[need].status=Need.STATUS_ACTIVE
        else:
                self.status=People.STATUS_WORKING

    def getDefaultTask(self):
        return WanderTask("walkable_path")