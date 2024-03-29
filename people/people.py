
from typing import Dict
import pygame
import math
from collections import deque
from map.action import Action
from people.need import Need
from ui.ui import Label
from utils.utils import Animation, extractTilesfromImage

from debug import debug
class People(pygame.sprite.Sprite):
    imgs = []
    TYPE_WORKER = 1
    TYPE_CUSTOMER = 2

    STATUS_IDLE = 0
    STATUS_GOINGTO = 1
    STATUS_WORKING = 2
    STATUS_LEAVING = 3
    STATUS_DESCRIP = ['IDLE','GOINGTO','WORKING','LEAVING']  ## GOING TO hidden

    ANIMA_MOVING_STAY = 0
    ANIMA_MOVING_UP = 1
    ANIMA_MOVING_DOWN = 2
    ANIMA_MOVING_LEFT = 3
    ANIMA_MOVING_RIGHT = 4
    ANIMA_WORKING = 5

    FRAME_DURATION = 10

    def __init__(self, x, y, id, type_person,level):
        super().__init__(level.all_sprites)
        self.x = x
        self.y = y
        self.id = id
        self.game = level
        self.map = level.map
        self.zLevel = 0
        self.xGrid = self.map.convertXGridToPX(x)
        self.yGrid = self.map.convertYGridToPX(y)
        self.visible = True
        self.pos = pygame.math.Vector2(self.xGrid, self.yGrid)
        self.animation_count = 0
        self.tasks = deque([])
        self.animations = {}
        self.type_person = type_person
        self.status = People.STATUS_IDLE
        self.currentTask = None
        self.currentPath = deque([])
        self.nextPos = None
        self.velocity = 50
        self.velocity_modif = 1
        self.working_force = 100
        self.direcMoving = People.ANIMA_MOVING_STAY
        self.obj=None
        self.default_Task = None
        self.popup_status = Label(level.lm.labelCustomer, "", pygame.Color("black"), (self.xGrid-8, self.yGrid-10), "midleft")
        self.popup_info = Label(level.lm.labelCustomer, "", pygame.Color("black"), (self.xGrid-8, self.yGrid-10), "midleft")
        self.start_working_at=0
        self.intensity = 0
        self.needs:Dict[str, Need] = {}
            

    def load_img_ani(self,img_matrix, tileset_fn):
        self.tileset = pygame.image.load(tileset_fn)
        self.animations = {k: Animation(extractTilesfromImage(self.tileset,v),self.FRAME_DURATION,True) for k, v in img_matrix.items()}

    def update(self,level,dt):
        """
        draw the people   self.direcMoving
        """
        self.animations[self.direcMoving].update(dt)

        self.do(dt)

        self.image = self.animations[self.direcMoving].img()
        self.rect = self.image.get_rect(topleft=(round(self.xGrid), round(self.yGrid)-1))
        #win.blit(self.img, (self.xGrid, self.yGrid - self.map.xGrid))
        ##win.blit(self.img[1], (self.xGrid, self.yGrid))

        if self.obj!=None:
            self.obj.rect = self.obj.image.get_rect(topleft=(round(self.xGrid), round(self.yGrid+2)))
            #self.obj.drawOn(self.image,0, 16)
        if self.popup_status is not None:
            self.popup_status.set_position((0, 20), "midleft")
            #self.popup_status.draw(win)
        if self.popup_info is not None:
            self.rect.height +=10
            self.popup_info.set_position((0, 20), "midleft")
            self.popup_info.draw(self.image)
        offset = 0
        self.rect.height +=5*len(self.needs)+5
        self.rect.y-=5*len(self.needs)+5
        for (k,n) in self.needs.items():
            
            n.draw(self.image,0, offset)
            offset+=5
            n.doIncrement(self.intensity)             
            if n.check():
                task = n.solve(self.game)
                if task!=None : 
                    self.popup_status.set_text("solving need...{}".format(k))
                    self.assignTask(task)

    def do(self, dt):
        self.popup_status.set_text(f"{self.STATUS_DESCRIP[self.status]}")
        if self.status == People.STATUS_IDLE or (self.openForTask and len(self.tasks)>0):
            self.getNextTask()
        elif  self.status == People.STATUS_GOINGTO:
            self.move(dt)
        elif  self.status == People.STATUS_WORKING:

            lapsed_secs = (pygame.time.get_ticks()-self.start_working_at)/1000
            need = self.currentTask.need

            if lapsed_secs > 1 :      ## keep as 1 sec instead self.needs[need].adding_sec
                self.direcMoving = People.ANIMA_WORKING
                self.start_working_at = pygame.time.get_ticks() 
                self.working()
        elif  self.status == People.STATUS_LEAVING:
            pass

    def assignTask(self, tsk):
        if tsk is not None:
            self.tasks.append(tsk)

    def move(self, dt):
        #print(self.currentPath)
        if len(self.currentPath)>0 and self.nextPos==None:
            self.nextPos=tuple(self.currentPath.pop(0))
        if self.nextPos!=None :
            self.moveTo(dt)
        else:
            self.status = People.STATUS_IDLE

    def moveTo(self,dt):
        veloc = self.velocity + 50*self.velocity_modif
        #print(self.nextPos)
        nextXGrid = self.map.convertXGridToPX(self.nextPos[0])
        nextYGrid = self.map.convertYGridToPX(self.nextPos[1])
        
        direction = pygame.math.Vector2()

        if self.y<self.nextPos[1]:
            self.direcMoving = People.ANIMA_MOVING_DOWN
            direction.y=1
        elif self.y>self.nextPos[1]:
            self.direcMoving = People.ANIMA_MOVING_UP
            direction.y=-1
        else:
            direction.y=0

        if self.x<self.nextPos[0]:
            direction.x=1
            self.direcMoving = People.ANIMA_MOVING_RIGHT
        elif self.x>self.nextPos[0]:
            direction.x=-1
            self.direcMoving = People.ANIMA_MOVING_LEFT
        else:
            direction.x=0
        
        if direction.magnitude()>0 : direction = direction.normalize()

        
        self.xGrid += (direction.x * veloc * dt)
        self.yGrid += (direction.y * veloc * dt)


        # self.xGrid = round(self.pos.x)
        # self.yGrid = round(self.pos.y)

        if abs(self.yGrid-nextYGrid)<2:
             self.y=self.nextPos[1]
             self.yGrid=nextYGrid
        if abs(self.xGrid-nextXGrid)<2:
             self.x=self.nextPos[0]
             self.xGrid=nextXGrid
        #moving_xGrid = self.map.convertPXToXGrid(self.xGrid)
        #moving_yGrid = self.map.convertPXToYGrid(self.yGrid)
        
        if self.x==self.nextPos[0] and self.y==self.nextPos[1]:
            self.nextPos=None
        if self.obj!=None:
            self.obj.x=self.x
            self.obj.y=self.y

    def getNextTask(self):
        if (self.currentTask==None or len(self.currentTask.solution)<=0):
            if len(self.tasks)>0 :

                self.currentTask = self.tasks.popleft()
            else:
                self.currentTask = self.getDefaultTask()
           #     return
        self.current_action = self.currentTask.solution.popleft()

        if "canInterrup" in self.current_action:
            self.openForTask=self.current_action["canInterrup"]
        else:
            self.openForTask=False  

        if "velocity" in self.current_action:
            self.velocity_modif=self.current_action["velocity"]
        else:
            self.velocity_modif=1

        {
            Action.TYPE_GOTO_X_Y: self.do_GOTO_X_Y,
            Action.TYPE_GOTO_ZONE: self.do_GOTO_ZONE,
            Action.TYPE_SET_STATUS: self.do_SET_STATUS,
            Action.TYPE_PEOPLE_STATUS: self.do_PEOPLE_STATUS,
            Action.TYPE_RESTORE: self.do_RESTORE,
            Action.TYPE_RELEASE_ZONE: self.do_RELEASE_ZONE,
            Action.TYPE_RESTORE_TASK: self.do_RESTORE_TASK,
            Action.TYPE_TURN_INTO_GARBAGE : self.do_TURN_INTO_GARBAGE,
            Action.TYPE_LIFT_OBJ : self.do_LIFT_OBJ,
            Action.TYPE_PUTDOWN_OBJ : self.do_PUTDOWN_OBJ,
            Action.TYPE_GOTO_OBJ : self.do_GOTO_OBJ,
            Action.TYPE_GOTO_CONTAINER: self.do_GOTO_CONTAINER,
            Action.TYPE_ADDOBJ_CONTAINER: self.do_ADDOBJ_CONTAINER,
            Action.TYPE_DELOBJ_CONTAINER: self.do_DELOBJ_CONTAINER,

        }.get(self.current_action["type"],self.do_INTERNAL)()


    def do_LIFT_OBJ(self):
        self.current_action["obj"].zLevel = self.zLevel+1
    def do_PUTDOWN_OBJ(self):
        self.current_action["obj"].zLevel = self.zLevel
    def do_INTERNAL(self):
        pass
    
    def do_GOTO_OBJ(self):
        pos=self.current_action["obj"].getSpot()
        self.status = People.STATUS_GOINGTO
        print(f"{self.x, self.y, pos[0], pos[1]}")
        self.currentPath = self.map.getWalkablePathFromToGrid(self.x, self.y, pos[0], pos[1]) 
        #print(f"{self.currentPath}")
        
    def do_GOTO_CONTAINER(self):
        if self.current_action["spot"]=='in':
            pos=self.current_action["container"].pos_in
        else:
            pos=self.current_action["container"].pos_out
        self.status = People.STATUS_GOINGTO
        print(f"{self.x, self.y, pos[0], pos[1]}")
        self.currentPath = self.map.getWalkablePathFromToGrid(self.x, self.y, pos[0], pos[1]) 
    def do_ADDOBJ_CONTAINER(self):
        self.current_action["container"].addObj(self.current_action["obj"])

    def do_DELOBJ_CONTAINER(self):
        self.current_action["container"].removeObj(self.current_action["obj"])
        
    def do_GOTO_X_Y(self):
        self.status = People.STATUS_GOINGTO
        self.currentPath = self.map.getWalkablePathFromToGrid(self.x, self.y, self.current_action["x"], self.current_action["y"])     
    
    def do_GOTO_ZONE(self):
        self.status = People.STATUS_GOINGTO
        zone = self.current_action["zone"]
        if "mode" in self.current_action and self.current_action["mode"]=="nearest":
            #if zone=='game' : print(f"locking zone {zone} id:{self.id}")
            (x_zone,y_zone)=self.map.getNearestSpotOnZone(zone,self.x, self.y, self.current_action["drop"])
        else:
            (x_zone,y_zone)=self.map.getEmptySpotOnZone(zone, self.current_action["drop"])

        if x_zone>=0 and y_zone>=0:
            self.currentPath = self.map.getWalkablePathFromToGrid(self.x, self.y, x_zone, y_zone)
        else:
            print("Zone FULL {} {} {}".format(x_zone,y_zone,self.current_action["zone"] ))

    def do_SET_STATUS(self):
        self.current_action["obj"].status = self.current_action["status"]
        self.do_RESTORE_TASK()    ## change status and trigger task

    def do_PEOPLE_STATUS(self):
        self.status = self.current_action["status"]     
    
    def do_RESTORE(self):
        self.map.restoreSpotZone(self.current_action["x"],self.current_action["y"],self.current_action["zone"])
    
    def do_RELEASE_ZONE(self):
        zone = self.current_action["zone"]
        #if zone=='game' : print(f"releasing zone {zone} id:{self.id}")
        self.map.restoreSpotZone(self.x,self.y,zone)

    def do_RESTORE_TASK(self):
        self.game.addTask(self.current_action["obj"].getTask())
    
    def do_TURN_INTO_GARBAGE(self):
        self.game.turnIntoGarbage(self.current_action["obj"])
