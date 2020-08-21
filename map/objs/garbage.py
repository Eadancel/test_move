from map.task import Task
from map.action import Action
from map.objects import Objects
import random

pathImgs = ["tile_0251.png","tile_0252.png","tile_0253.png"]


class Garbage(Objects):

    def __init__(self,x,y):
        super().__init__(x,y,pathImgs)
        solution = [
           { "type":Action.TYPE_GOTO_X_Y,
                "x"   :x,
                "y"   :y},
           {  "type":Action.TYPE_TAKE_OBJ,
              "obj":self},

           { "type":Action.TYPE_GOTO_ZONE,
             "zone" :"garbage_zone",
             "drop" : True
             },
            {  "type":Action.TYPE_RELEASE_OBJ
            }
        ]
        self.task = Task(solution,random.randint(1,20))
