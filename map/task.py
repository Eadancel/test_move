import pygame
import os
#from people.people import People
from collections import deque

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


