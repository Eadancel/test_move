import pygame
import os
from settings import *
from map.tiledMap import TiledMap
from map.map import Map
from people.people import People
from people.worker import Worker
from people.customer import Customer
from collections import deque
from debug import debug
from utils.camera import CameraGroup
PATH_maps = 'game_assets'

class Level():
    """ This is the class that makes the changes that you want to display. You would add most of your changes here.

    """
    def __init__(self, pathMap):

        self.displayRunning = True
        self.display_surface = pygame.display.get_surface()
        self.pathMap = pathMap
        self.bkgmap = TiledMap(os.path.join(PATH_maps,self.pathMap))
        self.map_img = self.bkgmap.make_map()
        self.map = Map(self.bkgmap)
        self.info=""
        self.paused = False
        self.all_sprites = CameraGroup(self.map_img)
        self.peoples = []
        self.tasks = {}
        self.objects = deque([])
        self.tasks_doing = deque([])
    def run(self,dt):
        if not self.paused:
            self.update(dt)       
            self.all_sprites.update(self, dt)
            self.all_sprites.custom_draw()
        else:
            debug("PAUSED")
        self.info = f"People: {len(self.peoples)} Task Cleaning: {len(self.tasks.get('staff_resting',{}))} ZoneGame:{len(self.tasks.get('gambling',{}))} Objects: {len(self.objects)}" 
    def input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.paused = not self.paused
            if event.key ==pygame.K_g:
                self.all_sprites.target_idx-=1
            if event.key == pygame.K_h:
                self.all_sprites.target_idx+=1
        if event.type == pygame.MOUSEWHEEL:
            self.all_sprites.zoom_scale +=event.y * 0.03 
        
    def update(self, dt):
        pass
    def loadMap(self):
        #self.map_rect = self.map_img.get_rect()
        self.display_surface.blit(self.map_img,(0,0))

    def addTask(self, task):
        if task.need in self.tasks:
            self.tasks[task.need].append(task)
        else:
            self.tasks[task.need] = deque([task])
    
    def addObject(self, obj):
        self.objects.append(obj)
        if obj.task: self.addTask(obj.task)

    def removeObj(self, obj):
        self.objects.remove(obj)
        obj.kill()

    def getTaskbyNeed(self, need):
        if need in self.tasks:
            if len(self.tasks[need])>0:
                return self.tasks[need].popleft()
            else:
                return None
        else:
            return None

    def addObjectAt(self, obj):
        if self.map.isWalkable(obj.x,obj.y):
            self.addObject(obj)
        else:
            print("not walkable {} {}".format(obj.x,obj.y))
    
    def getRelativeMousePos(self):
        pos = pygame.mouse.get_pos()
        return self.all_sprites.relaPosZoom(pos)


class LabelManager():
    def __init__(self):
        self.labelCustomer = pygame.font.Font(None, 12)
        self.labelTitle = pygame.font.Font(None, 20)
        self.labelMini = pygame.font.Font(None, 20)


# Worker(30,9,"Worker 1",self,self.lm.labelCustomer), 
# Worker(37,15,"Worker 2",self,lm.labelCustomer),
# Worker(6,4,"Worker 3",self,label_font), 
# Worker(1,4,"Worker 4",self,label_font),
# Worker(1,4,"Worker 5",self,label_font),
# Worker(1,4,"Worker 6",self,label_font),
# Customer(36,10,f"Customer Test",self,label_font),
# Customer(36,12,f"Customer Test",self,label_font),


    
