from map.task import MovetoObjWork
from map.objs.objects import Objects


pathImgs = ["tile_0333.png","tile_0333.png","tile_033.png"]


class Sofa(Objects):

    def __init__(self,x,y):
        super().__init__(x,y,"garbage",pathImgs)
        self.task = MovetoObjWork(self,"resting")