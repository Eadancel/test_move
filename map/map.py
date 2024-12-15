import math
import os
from random import sample
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from map.tiledMap import TiledMap

from collections import deque

PATH_maps = 'game_assets'
WALKABLE_LAYER = 'walkable_path'
ZONES_LAYER = 'zones'
class Map:
    def __init__(self,pathMap):

        self.gameMap = TiledMap(os.path.join(PATH_maps,pathMap))
        self.map_img = self.gameMap.make_map()
        self.xGrid = self.gameMap.tilewidth
        self.yGrid = self.gameMap.tileheight
        self.tasks = []
        self.setup_zone()
        self.setup_walkable()

    def setup_walkable(self):
        
        ### Walkable_tiles 
        self.walkableTiles = []
        self.walkableTiles = [
            [0 for _ in range(self.gameMap.xGridSize)]
            for _ in range(self.gameMap.yGridSize)
        ]
        walkable_objs = self.gameMap.objs_layer[WALKABLE_LAYER]
        self.zones[WALKABLE_LAYER] = deque([])
        for wo in walkable_objs:
            for iX in range(wo['stGridx'], wo['endGridx']):
                for iY in range(wo['stGridy'], wo['endGridy']):
                    self.walkableTiles[iY][iX] = 1
                    self.zones[WALKABLE_LAYER].append((iX,iY))
        print("h{} w{}".format(len(self.walkableTiles), len(self.walkableTiles[0])))

    def setup_zone(self):
        ### Zones
        self.zones = {}
        walkable_objs = self.gameMap.objs_layer[ZONES_LAYER]
        for wo in walkable_objs:
            for iX in range(wo['stGridx'], wo['endGridx']):
                for iY in range(wo['stGridy'], wo['endGridy']):
                    if wo['name'] not in self.zones.keys():
                        self.zones[wo['name']] = deque([])
                    self.zones[wo['name']].append((iX, iY))
    
    def get_objs_per_layer(self, layer_name):
        return self.gameMap.objs_layer[layer_name]

    def convertXGridToPX(self, pos):
        return pos*self.xGrid
    def convertYGridToPX(self, pos):
        return pos*self.yGrid

    def convertPXToXGrid(self, px):
        return self.gameMap.convertPXToXGrid(px)
    def convertPXToYGrid(self, px):
        return self.gameMap.convertPXToYGrid(px)
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
        
        if not self.isWalkable(x2,y2):
            print(f"{len(path)=} {path=}")

        return path
