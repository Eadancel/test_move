import pygame
import os
#from people.people import People
from collections import deque
from map.action import Action
from map.objects import Objects
import random

class Task:
    STATUS_TODO = 0
    STATUS_DOING = 1
    STATUS_DONE = 2
    def __init__(self,solution, duration):
        self.duration = duration
        self.solution = deque(solution)
        self.status = Task.STATUS_TODO

    def workingOn(self, workingForce):
        self.duration-=workingForce/100
        if self.duration<=0:
            self.status=Task.STATUS_DONE
        else:
            self.status=Task.STATUS_DOING


class MovetoZoneTask(Task):
    def __init__(self, obj, zone):
        super().__init__([],random.randint(1,20))
        self.solution = deque([
            { "type":Action.TYPE_GOTO_X_Y,
              "x"   :obj.x,
              "velocity" :1.1,
              "y"   :obj.y},

            { "type":Action.TYPE_TAKE_OBJ,
              "obj" :obj},

            { "type":Action.TYPE_GOTO_ZONE,
              "zone" :zone,
              "velocity" :1.1,
              "drop" : True},

            { "type":Action.TYPE_RELEASE_OBJ},

            { "type":Action.TYPE_SET_STATUS,
              "obj" :obj,
              "status":Objects.STATUS_DIRTY},
        ])
class CleanObjectRecoverZone(Task):
    def __init__(self, obj, zone):
        super().__init__([],random.randint(1,20))
        self.solution = deque([
            { "type":Action.TYPE_GOTO_X_Y,
              "x"   :obj.x,
              "y"   :obj.y},

            { "type":Action.TYPE_MAKE_VISIBLE,
              "obj" : obj,
              "visible" : False},

            { "type":Action.TYPE_RESTORE,
              "zone" :zone,
              "x"   :obj.x,
              "y"   :obj.y},

        ])