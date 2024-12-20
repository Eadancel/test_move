import pygame
import random

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
        self.needsMoney = False
    def doIncrement(self, value_add):
        lapsed_secs = (pygame.time.get_ticks()-self.start_adding_at)/1000
        if lapsed_secs > self.adding_sec and self.value< self.threshold and self.status==Need.STATUS_ACTIVE:
            self.start_adding_at = pygame.time.get_ticks() 
            self.value += value_add + self.increment
            #self.value += self.increment
    def doDecrement(self, value_add):
        self.value -= random.randint(1,value_add)
    def solve(self, game): 
        ## Find a available Task to solve the need.  
        task = game.getTaskbyNeed(self.name)
        if task !=None: 
            self.status=Need.STATUS_INACTIVE
        return task
    def checkPreconditions(self):
        return True
    def check(self):
        return  self.value>=self.threshold and self.status==Need.STATUS_ACTIVE
    def draw(self, win, x,y):
        pygame.draw.rect(win, (0,128,0), (x, y, 16, 5))
        pygame.draw.rect(win, (255,0,0), (x, y, int(self.percent()/100 * 16), 5))

    def isSolved(self):
        return self.value<=0
    def percent(self):
        return min(self.value/self.threshold * 100, 100)
    
class NeedThirst(Need):
    def __init__(self):
        super().__init__()
        self.value = 0
        self.name = "thirst"
        self.increment = 5
        self.adding_sec = 2
        self.threshold = 100
        self.needsMoney = True


class NeedGambling(Need):
    def __init__(self):
        super().__init__()
        self.value = 0
        self.name = "gambling"
        self.increment = 20
        self.adding_sec = 2
        self.threshold = 100
        self.needsMoney = True
    
class NeedCleaning(Need):
    def __init__(self):
        super().__init__()
        self.value = 0
        self.name = "cleaning"
        self.increment = 50
        self.adding_sec = 1
        self.threshold = 100

class NeedResting(Need):
    def __init__(self, increment):
        super().__init__()
        self.value = 0
        self.name = "staff_resting"
        self.increment = increment
        self.adding_sec = 5
        self.threshold = 100

class NeedPrepare(Need):
    def __init__(self):
        super().__init__()
        self.value = 0
        self.name = "prepare_drink"
        self.increment = 50
        self.adding_sec = 1
        self.threshold = 100
    

class NeedServing(Need):
    def __init__(self):
        super().__init__()
        self.value = 0
        self.name = "serving"
        self.increment = 50
        self.adding_sec = 1
        self.threshold = 100
    
