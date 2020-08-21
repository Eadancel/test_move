import pygame
import pytmx
from collections import deque

class TiledMap():
    """ This is creating the surface on which you make the draw updates """
    walkableTiles = []
    zones = dict()
    def __init__(self, pathMap):
        self.gameMap = pytmx.load_pygame(pathMap, pixelalpha=True)
        self.mapwidth = self.gameMap.tilewidth * self.gameMap.width
        self.mapheight = self.gameMap.tileheight * self.gameMap.height

    def render(self, surface):
        for layer in self.gameMap.layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                if layer.visible :
                    for x, y, gid in layer:
                        tile = self.gameMap.get_tile_image_by_gid(gid)
                        if tile:
                            surface.blit(tile, (x * self.gameMap.tilewidth, y * self.gameMap.tileheight))
                else:
                    if layer.name=="walkable":
                        #self.walkableTiles=[[False]*self.gameMap.width]*self.gameMap.height
                        self.walkableTiles= [[] for i in range(self.gameMap.height)]

                        for x, y, gid in layer:
                            self.walkableTiles[y].append(gid)

                    self.zones[layer.name]=deque([])
                    for x, y, gid in layer:
                        if gid!=0:
                            self.zones[layer.name].append((x,y))
        print("w{} h{}".format(len(self.walkableTiles), len(self.walkableTiles[0])))
        #print(self.zones)
    def make_map(self):
        mapSurface = pygame.Surface((self.mapwidth, self.mapheight))
        self.render(mapSurface)
        return mapSurface