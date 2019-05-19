
import pygame

class People:
    imgs = []
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.animation_count = 0
        self.path = []
        self.img = None
    def draw(self, win)
        """
        draw the peopl
        """
        self.animation_count += 1
        self.img = self.imgs[self.animation_count]
        if self.animation_count > len(self.imgs):
            self.animation_count = 0 
        win.blit(self.img, (self.x, self.y))
        self.move()
    def move():
        pass
