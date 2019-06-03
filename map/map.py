import math

from collections import deque
class Map:
    def __init__(self, xGrid, yGrid, walkableTiles):
        self.xGrid = xGrid
        self.yGrid = yGrid
        self.tasks = []
        self.walkableTiles = walkableTiles
    def convertXGridToPX(self, pos):
        return pos*self.xGrid
    def convertYGridToPX(self, pos):
        return pos*self.yGrid

    def convertPXToXGrid(self, px):
        return math.trunc(px/self.xGrid)
    def convertPXToYGrid(self, px):
        return math.trunc(px/self.yGrid)

    def isWalkable(self, x,y):
        return self.walkableTiles[y][x]

    def distance(self, x1,y1,x2,y2):
        return math.trunc(math.sqrt((x1-x2)**2 + (y1-y2)**2)*10)

    def getNeighbourd(self,x1,y1):
        neigh = deque([])
        vector = [(-1,-1),(0,-1),(1,-1),
                  (-1,0),(1,0),
                  (-1,1),(0,1),(1,1) ]
        for x ,y in vector:
            #xc , yc = (x1,y1) + (x,y)
            xc = x1+x
            yc = y1+y

            if self.isWalkable(xc,yc) and xc>0 and yc>0 :
                neigh.append([xc,yc])
        return neigh

    def getNeighDistance(self,x1,y1,x2,y2):
        neighSort = deque([])
        neigh = self.getNeighbourd(x1,y1)
        for x,y in neigh:
            neighSort.append((x,y,self.distance(x,y,x2,y2)))
        return sorted(neighSort,key = lambda celda: celda[2])

    def getWalkablePathFromTo(self,x1,y1,x2,y2):
        path = deque([])
        toReview = deque([])
        toReview.append(self.getNeighDistance(x1,y1,x2,y2))

    def getPathFromTo(self,x1,y1,x2,y2):
        path = deque([])
        print ("distance {},{} to  {},{} : {} ".format(x1,y1,x2,y2,self.distance(x1,y1,x2,y2)))
        print (self.getNeighbourd(x1,y1))
        print (self.getNeighDistance(x1,y1,x2,y2))
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


        return path