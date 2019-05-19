import math
from collections import deque
class Map:
    def __init__(self, xGrid, yGrid):
        self.xGrid = xGrid
        self.yGrid = yGrid
        self.tasks = []

    def convertXGridToPX(self, pos):
        return pos*self.xGrid
    def convertYGridToPX(self, pos):
        return pos*self.yGrid
    
    def convertPXToXGrid(self, px):
        return math.trunc(px/self.xGrid)
    def convertPXToYGrid(self, px):
        return math.trunc(px/self.yGrid)

    def getPathFromTo(self,x1,y1,x2,y2):
        path = deque([])
        
        stepx=0
        stepy=0
        while x1!=x2 or y1!=y2:
            if x1>x2:
                x1 -=1
            elif x1<x2:
                x1 +=1
            if y1>y2:
                y1 -=1
            elif y1<y2:
                y1 +=1
            path.append([x1,y1])

        #print (path)
        return path