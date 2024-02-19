import math

from collections import deque
from random import sample
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


class Map:
    def __init__(self,map):

        self.map = map
        self.xGrid = self.map.gameMap.tilewidth
        self.yGrid = self.map.gameMap.tileheight
        self.tasks = []
        self.walkableTiles = self.map.walkableTiles
        self.zones = self.map.zones

    def convertXGridToPX(self, pos):
        return pos*self.xGrid
    def convertYGridToPX(self, pos):
        return pos*self.yGrid

    def convertPXToXGrid(self, px):
        return math.trunc(px/self.xGrid)
    def convertPXToYGrid(self, px):
        return math.trunc(px/self.yGrid)

    def getNearestSpotOnZone(self,zone,x,y,drop=True):
        if len(self.zones[zone])>0:
            nearspt=sorted(list(self.zones[zone]),key=lambda spot: self.distancePos(spot,(x,y)))[0]
            if drop:
                self.zones[zone].remove(nearspt)
            return nearspt            
        else:
            return (-1,-1)
    def getEmptySpotOnZone(self,zone,drop=True):
        if len(self.zones[zone])>0:
            if drop:
                return self.zones[zone].popleft()
            else:
                return sample(self.zones[zone],1)[0]
        else:
            return (-1,-1)
            
    def restoreSpotZone(self, x,y,zone):
        self.zones[zone].appendleft((x,y))
    def getRandomWalkableSpot(self):
        return sample(self.walkableTiles,1)[0]

    def isWalkable(self, x,y):
        #print("checking {} {}".format(x,y))
        return self.walkableTiles[y][x]

    def distance(self, x1,y1,x2,y2):
        return math.trunc(math.sqrt(((x1-x2)**2) + (y1-y2)**2))

    def distancePos(self, pos1, pos2):
        return self.distance ( pos1[0],pos1[1], pos2[0], pos2[1])

    def getWalkablePathFromToGrid(self,x1,y1,x2,y2):
        self.grid = Grid(matrix=self.walkableTiles)
        start = self.grid.node(x1,y1)
        end = self.grid.node(x2,y2)

        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        path, runs = finder.find_path(start, end, self.grid)

        #print('operations:', runs, 'path length:', len(path))
        #print (path)
        #print(self.grid.grid_str(path=path, start=start, end=end))

        return path