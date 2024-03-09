from collections import deque

import pygame
import pytmx


class TiledMap:
    """This is creating the surface on which you make the draw updates"""

    walkableTiles = []
    zones = dict()

    def __init__(self, pathMap):
        self.gameMap = pytmx.load_pygame(pathMap, pixelalpha=True)
        self.mapwidth = self.gameMap.tilewidth * self.gameMap.width
        self.mapheight = self.gameMap.tileheight * self.gameMap.height

        self.walkableTiles = [
            [0 for col in range(self.gameMap.width)]
            for row in range(self.gameMap.height)
        ]

    def render(self, surface):
        for layer in self.gameMap.layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                if layer.visible:
                    for x, y, gid in layer:
                        if (layer.name == "chars") & (gid > 0):
                            print(f"{gid=}")
                        tile = self.gameMap.get_tile_image_by_gid(gid)
                        if tile:
                            surface.blit(
                                tile,
                                (
                                    x * self.gameMap.tilewidth,
                                    y * self.gameMap.tileheight,
                                ),
                            )
                # else:
                #     self.zones[layer.name]=deque([])
                #     for x, y, gid in layer:
                #         if gid!=0:
                #             self.zones[layer.name].append((x,y))

        for obj in self.gameMap.get_layer_by_name("walkable_path") + self.gameMap.get_layer_by_name("zones"):
            (xGrid_st, yGrid_st) = (
                self.convertPXToXGrid(obj.x),
                self.convertPXToYGrid(obj.y),
            )
            (xGrid_end, yGrid_end) = (
                self.convertPXToXGrid(obj.x + obj.width),
                self.convertPXToYGrid(obj.y + obj.height),
            )
            for iX in range(xGrid_st, xGrid_end):
                for iY in range(yGrid_st, yGrid_end):
                    if obj.type == "walkable_path":
                        self.walkableTiles[iY][iX] = 1
                    if obj.type not in self.zones.keys():
                        self.zones[obj.type] = deque([])
                    self.zones[obj.type].append((iX, iY))
                    # { pos : (), in:(), out:()}
                    # or
                    # offset[obj.type] = {in:(), out:()}

        print("h{} w{}".format(len(self.walkableTiles), len(self.walkableTiles[0])))
        # print(self.walkableTiles)

    def get_tile_from_img(self, pos: tuple, img):
        x = pos[0]
        y = pos[1]

        gid = self.gameMap.register_gid(gid)
        return self.gameMap.get_tile_image_by_gid(gid)

    def make_map(self):
        mapSurface = pygame.Surface((self.mapwidth, self.mapheight))
        self.render(mapSurface)
        return mapSurface

    def convertPXToXGrid(self, px):
        return int(px // self.gameMap.tilewidth)

    def convertPXToYGrid(self, px):
        return int(px // self.gameMap.tileheight)
