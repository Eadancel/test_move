import pygame
from map.tiledMap import TiledMap

class Display():
    """ This is the class that makes the changes that you want to display. You would add most of your changes here.

    """
    def __init__(self, pathMap):

        self.displayRunning = True
        pygame.init()
        self.displayWindow = pygame.display.set_mode((640*2, 320*2))
        self.clock = pygame.time.Clock()
        self.pathMap = pathMap
        self.map = TiledMap(self.pathMap)
        self.map_img = self.map.make_map()
        #print(self.map.walkableTiles)

    def update(self):

        pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        pygame.display.update()

    def loadMap(self):
        #self.map_rect = self.map_img.get_rect()
        self.displayWindow.blit(self.map_img,(0,0))

    def displayLoop(self):

        self.clock.tick(60)
        self.update()
        self.loadMap()