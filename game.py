import pygame
import os
class Game:
    def __init__(self):
        self.width = 500
        self.height = 300
        self.win = pygame.display.set_mode((self.width, self.height))
        self.peoples = [] 
        self.objects = []
        self.bg = pygame.image.load(os.path.join("game_assets","bg.png"))
        
    def run (self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run=False
            self.draw()
        pygame.quit()

    def draw(self):
        self.win.blit(self.bg,(0,0))
        pygame.display.update()