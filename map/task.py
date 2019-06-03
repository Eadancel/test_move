import pygame
import os
#from people.people import People


pathImgs = ["tile_0251.png","tile_0252.png","tile_0253.png"]

class Task:
    STATUS_TODO = 0
    STATUS_DOING = 1
    STATUS_DONE = 2
    def __init__(self, x, y, duration):
        self.x = x
        self.y = y
        self.duration = duration
        self.status = Task.STATUS_TODO
        self.imgs = []
        for pi in pathImgs:
            self.imgs.append(pygame.image.load(os.path.join("game_assets/Tiles",pi)))
    def draw(self, win, map):
        win.blit(self.imgs[self.status], (map.convertXGridToPX(self.x), map.convertYGridToPX(self.y)))

    def workingOn(self, workingForce):
        self.duration-=workingForce/100
        if self.duration<=0:
            self.status=Task.STATUS_DONE
        else:
            self.status=Task.STATUS_DOING


