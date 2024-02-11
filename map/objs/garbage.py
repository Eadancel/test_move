from map.task import MovetoZoneTaskTakeRelease
from map.objs.objects import Objects





class Garbage(Objects):

    def __init__(self,x,y):
        super().__init__(x,y,"garbage",pathImgs)
        self.task = MovetoZoneTaskTakeRelease(self,"garbage_zone","cleaning")