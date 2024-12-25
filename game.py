import sys

import pygame
import json
import pygame_gui
from pygame.locals import K_ESCAPE
from debug import debug
from map.level.restaurante import LevelRestaurante
from pygame_gui.elements import UIButton
from pygame_gui.elements import UITextBox
FPS = 60
WINDOWS_SIZE=(1920,1200)
## "mapaCity.tmx"
class Game:

    def __init__(self):
        pygame.init()
        self.displayWindow = pygame.display.set_mode(WINDOWS_SIZE)
        self.clock = pygame.time.Clock()
        self.level = LevelRestaurante()
        self.ui_manager = pygame_gui.UIManager(WINDOWS_SIZE)

        
        relative_rect = pygame.Rect(0,0,100,40)
        relative_rect.bottomright = (-100,-20)
        self.hello_button = UIButton(relative_rect=relative_rect,
                                             text='Close',
                                             manager=self.ui_manager,
                                             anchors={'right':'right',
                                                    'bottom':'bottom'})
        right_top = pygame.Rect(0,0,200,100)
        right_top.topright = (-200,0) 
        self.label_status = UITextBox(relative_rect=right_top,
                                    html_text="Status",
                                    manager=self.ui_manager,
                                    wrap_to_height = True,
                                    anchors = {'right':'right',
                                               'top':'top'})
        self.UItooltip = UITextBox(relative_rect=right_top,
                                    visible=False,
                                    html_text="Tooltip",
                                    manager=self.ui_manager,
                                    wrap_to_height = True,
                                    anchors = {'right':'right',
                                               'top':'top'})
                                    
    def run(self):
        
        while True:

            dt = self.clock.tick(FPS)/1000.0
            
            self.displayWindow.fill("red")
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if (event.type == pygame.QUIT) or (keys[K_ESCAPE]):
                    pygame.quit()
                    sys.exit()
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.hello_button:
                        pygame.quit()
                        sys.exit()
                self.level.input(event)
                self.ui_manager.process_events(event)

            if (dt < 100 / FPS):  ## in case the window is freezing because is moving (Window behaviour)
                self.level.update(dt)
                if self.level.show_tooltip():
                    mouse_pos = pygame.mouse.get_pos()
                    self.UItooltip.set_position(mouse_pos)
                    self.UItooltip.set_text(self.level.tooltip['html_text'])
                    self.UItooltip.show()
                else:
                    self.UItooltip.hide()
                self.ui_manager.update(dt)
            else:
                print("drop frame")
            
            debug(f"{self.level.getAvailableContSlots('drink_delivery')}")

            self.label_status.set_text(
                "{:.2f}<br> Stage:<br> {}".format(self.clock.get_fps(), json.dumps(self.level.stage,indent=2))
            )
            self.ui_manager.draw_ui(self.displayWindow)
            pygame.display.update()
            #self.clock.tick(FPS)
