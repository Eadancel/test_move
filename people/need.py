import pygame
import random
from map.task import Task
from map.action import Action
class Need():
    STATUS_INACTIVE=0
    STATUS_ACTIVE=1
    def __init__(self):
        self.value = 0
        self.name = "default"
        self.increment = 0
        self.solution = []
        self.threshold = 100
        self.status=Need.STATUS_ACTIVE
        self.start_adding_at=0
        self.adding_sec = 2
    def doIncrement(self, value_add):
        lapsed_secs = (pygame.time.get_ticks()-self.start_adding_at)/1000
        if lapsed_secs > self.adding_sec and self.value< self.threshold and self.status==Need.STATUS_ACTIVE:
            self.start_adding_at = pygame.time.get_ticks() 
            self.value += value_add + self.increment
            #self.value += self.increment
    def doDecrement(self, value_add):
        self.value -= random.randint(1,value_add)
    def getTask(self):
        if self.value>=self.threshold and self.status==Need.STATUS_ACTIVE:    
            self.status=Need.STATUS_INACTIVE     
            return  Task(self.solution,random.randint(1,20))
        else:
            return None
        
    def draw(self, win, x,y):
        pygame.draw.rect(win, (0,128,0), (x, y, 25, 5))
        pygame.draw.rect(win, (255,0,0), (x, y, int(round(self.percent()/4)), 5))

    def isSolved(self):
        pass
    def percent(self):
        return self.value/self.threshold * 100
class NeedThirst(Need):
    def __init__(self):
        super().__init__()
        self.value = 0
        self.name = "Thirst"
        self.increment = 15
        self.adding_sec = 2
        self.solution = [{"type":Action.TYPE_GOTO_ZONE,
                          "zone":"bar",
                          "canInterrup":False,
                          "drop":True,
                          "mode" : "nearest",
                          "velocity":0.7},
                          {"type":Action.TYPE_TASKWORK,
                           "need":"thirst",
                           "cost":10,
                           "profit":[0],
                           "luck":[100],
                           "value":300,
                           "addGarba":15},
                           { "type":Action.TYPE_RELEASE_ZONE,
                            "zone" :"bar"},]
        self.threshold = 1000
    def isSolved(self):
        return self.value<=0
class NeedGambling(Need):
    def __init__(self):
        super().__init__()
        self.value = 0
        self.name = "gambling"
        self.increment = 33
        self.adding_sec = 1
        self.solution = [{"type":Action.TYPE_GOTO_ZONE,
                          "zone":"game",
                          "canInterrup":False,
                          "drop":True,
                          "mode" : "nearest",
                          "velocity":0.7},
                          {"type":Action.TYPE_TASKWORK,
                           "need":"gambling",
                           "cost":100,
                           "profit":[0,1,5,20,50,100],
                           "luck":[90,5,2,1,0.07,0.03],
                           "value":100,
                           "addGarba":5},
                           { "type":Action.TYPE_RELEASE_ZONE,
                            "zone" :"game"},]
        self.threshold = 1000
    def isSolved(self):
        return self.value<=0