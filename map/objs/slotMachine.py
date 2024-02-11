from map.task import PlayingLuck
from map.objs.objects import Objects


pathImgs = ["tile_0223.png","tile_0223.png","tile_0223.png"]


class SlotMachine(Objects):

    def __init__(self,x,y):
        super().__init__(x,y,pathImgs)
        self.task = PlayingLuck(self)
        self.locked = False
        self.cost = 100
        self.profit = [0,1,5,20,50,100]
        self.luck = [90,5,2,1,0.07,0.03]
