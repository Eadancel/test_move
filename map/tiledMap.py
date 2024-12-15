from collections import deque
from typing import List
import ast
import pygame
import pytmx


class TiledMap:
    """This is creating the surface on which you make the draw updates"""

    walkableTiles = []
    zones = dict()

    def __init__(self, pathMap):
        self.gameMap = pytmx.load_pygame(pathMap, pixelalpha=True)
        self.xGridSize = self.gameMap.width
        self.yGridSize = self.gameMap.height
        self.tilewidth = self.gameMap.tilewidth
        self.tileheight = self.gameMap.tileheight
        self.mapwidth = self.gameMap.tilewidth * self.gameMap.width
        self.mapheight = self.gameMap.tileheight * self.gameMap.height
        self.objs_layer = {}

    def render(self, surface):
        for layer in self.gameMap.layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                if layer.visible:
                    for x, y, gid in layer:
                        if (layer.name == "chars") & (gid > 0):
                            print(f"{gid=}")
                        tile = self.gameMap.get_tile_image_by_gid(gid)
                        if tile:
                            surface.blit(tile,(x * self.gameMap.tilewidth, y * self.gameMap.tileheight))
            if isinstance(layer,pytmx.TiledObjectGroup):
                objs= []
                for obj in layer:
                    offset = ast.literal_eval(str(obj.properties.get("offset","(0,0)")))if str(obj.properties.get("offset")) else (0,0)
                    offset_prod = ast.literal_eval(str(obj.properties.get("offset_prod","(0,0)")))if str(obj.properties.get("offset_prod"))else (0,0)
                    pos_in =  ast.literal_eval(obj.properties.get("spot_in","(0,0)")) if str(obj.properties.get("spot_in"))!="" else (0,0)
                    pos_out = ast.literal_eval(obj.properties.get("spot_out","(0,0)"))if str(obj.properties.get("spot_out"))!="" else(0,0)

                    objs.append({
                        "name" : obj.name,
                        "type" : obj.type,
                        "drawOn" : (obj.x,obj.y),
                        "stGridx" : self.convertPXToXGrid(obj.x),
                        "stGridy" : self.convertPXToXGrid(obj.y),
                        "endGridx" : self.convertPXToXGrid(obj.x+obj.width),
                        "endGridy" : self.convertPXToXGrid(obj.y+obj.height),
                        "image"   : obj.image,
                        "properties" : obj.properties,
                        "offset" : offset,
                        "offset_prod" : offset_prod,
                        "pos_in" : pos_in,
                        "pos_out" : pos_out,

                    })
                self.objs_layer[layer.name]=objs
    def get_objs_by_layer(self, layer_name):
        layer=self.gameMap.get_layer_by_name(layer_name)
        return layer

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
