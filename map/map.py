import math

from collections import deque
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

class Map:
    def __init__(self, xGrid, yGrid, walkableTiles, zones):
        self.xGrid = xGrid
        self.yGrid = yGrid
        self.tasks = []
        self.walkableTiles = walkableTiles
        self.zones = zones

    def convertXGridToPX(self, pos):
        return pos*self.xGrid
    def convertYGridToPX(self, pos):
        return pos*self.yGrid

    def convertPXToXGrid(self, px):
        return math.trunc(px/self.xGrid)
    def convertPXToYGrid(self, px):
        return math.trunc(px/self.yGrid)
    def getEmptySpotOnZone(self,zone):
        if len(self.zones[zone])>0:
            return self.zones[zone].popleft()
        else:
            return (0,0)
    def isWalkable(self, x,y):
        #print("checking {} {}".format(x,y))
        return self.walkableTiles[y][x]

    def distance(self, x1,y1,x2,y2):
        return math.trunc(math.sqrt(((x1-x2)**2) + (y1-y2)**2))

    def distancePos(self, pos1, pos2):
        return self.distance ( pos1[0],pos1[1], pos2[0], pos2[1])

    def getNeighbourd(self,current_node):
        neigh = []
        vector = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for x ,y in vector:
            #xc , yc = (x1,y1) + (x,y)
            xc = current_node.position[0]+x
            yc = current_node.position[1]+y

            if  xc>0 and yc>0 and xc<40 and yc<20 and self.isWalkable(xc,yc):
                new_node = Node(current_node, (xc,yc))
                neigh.append(new_node)

        return neigh
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
    def getWalkablePathFromTo(self,x1,y1,x2,y2):
        start = (x1,y1)
        end = (x2,y2)
        print ("path from {} {}".format(start,end))
        start_node=Node(None, start)
        start_node.g = start_node.h = start_node.f = 0

        end_node=Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        open_list = []
        closed_list = []

        open_list.append(start_node)
        while len(open_list)>0:
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f<current_node.f:
                    current_node = item
                    current_index = index
            print ("index {} pos {} f{} g{} h{}".format(current_index,current_node.position, current_node.f, current_node.g , current_node.h))
            open_list.pop(current_index)
            closed_list.append(current_node)
            print ("largo {}".format(len(open_list)))

            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    print ("pos {} f{} g{} h{}".format(current.position, current.f, current.g , current.h))
                    path.append(current.position)
                    current = current.parent
                return path[::-1]

            children = self.getNeighbourd(current_node)

            for child in children:
                # for closed_child in closed_list:
                #     if child == closed_child:
                #         continue
                if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                    continue

                child.g = current_node.g + 1
                child.h = self.distancePos(current_node.position, end_node.position)
                child.f = child.g + child.h

                # for open_node in open_list:
                #     if child==open_node and child.g > open_node.g:
                #         continue
                if len([open_node for open_node in open_list if child == open_node and child.g > open_node.g]) > 0:
                    continue

                open_list.append(child)


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