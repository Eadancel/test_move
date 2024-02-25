import pygame

from debug import debug
from map.objs.objects import Sofa

class CameraGroup(pygame.sprite.Group):
    def __init__(self, ground_surf):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        #camera offset

        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # box setup
        self.camera_borders = {'left':200, 'right':200, 'top':100, 'bottom':100}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.display_surface.get_size()[0] - (self.camera_borders['left']+ self.camera_borders['right'])
        h = self.display_surface.get_size()[1] - (self.camera_borders['top']+ self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l,t,w,h)

        #ground
        self.target_idx = 0
        self.ground_surf = ground_surf.convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(topleft=(0,0))

        #camera
        self.keyboard_speed = 5

        self.zoom_scale = 1
        self.internal_surf_size = (1440,1440)
        self.internal_surf = pygame.Surface(self.internal_surf_size,pygame.SRCALPHA )
        self.internal_rect = self.internal_surf.get_rect(center = (self.half_w, self.half_h) )
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surf_size)
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w     # 960/2 - 640   
        self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h

    def relaPosZoom(self,pos): # Screen position, translate to pos internal surface for tail calculation
        
        #print (f"{self.offset=} {1 / self.zoom_scale=} {self.scaled_rect.topleft=} {self.internal_offset}")
        relapos = pos
        invertScale = 1 / self.zoom_scale
        offset_zoom = pygame.math.Vector2()
        offset_zoom.x = ((self.scaled_rect.topleft[0]) * invertScale + self.internal_offset.x) * self.zoom_scale
        offset_zoom.y = ((self.scaled_rect.topleft[1]) * invertScale + self.internal_offset.y) * self.zoom_scale

        relapos_x = round((pos[0]   - offset_zoom.x  ) * invertScale - self.offset.x)
        relapos_y = round((pos[1]   - offset_zoom.y   ) * invertScale - self.offset.y)
        #relapos = pos + self.offset
        #print (f"{relapos_x - pos[0]=} {relapos_y - pos[1]=} {offset_zoom=}")
        return ((relapos_x,relapos_y))
    


    def center_target_camera(self, target):

        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def box_target_cames(self, target):

        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom


        self.offset.x= self.camera_rect.left - self.camera_borders['left']
        self.offset.y= self.camera_rect.top - self.camera_borders['top']

    def keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: self.camera_rect.x  += self.keyboard_speed
        if keys[pygame.K_d]: self.camera_rect.x  -= self.keyboard_speed
        if keys[pygame.K_w]: self.camera_rect.y  += self.keyboard_speed
        if keys[pygame.K_s]: self.camera_rect.y  -= self.keyboard_speed 

        self.offset.x= self.camera_rect.left - self.camera_borders['left']
        self.offset.y= self.camera_rect.top - self.camera_borders['top']

    def mouse_grab_control(self):
        state = pygame.mouse.get_pressed()
        if state[2]:
            relaPos = pygame.mouse.get_pos()  # relative pos
            self.camera_rect.center = relaPos
        

        self.offset.x= self.camera_rect.left - self.camera_borders['left']
        self.offset.y= self.camera_rect.top - self.camera_borders['top']

    def zoom_keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]: self.zoom_scale -=0.2
        if keys[pygame.K_e]: self.zoom_scale +=0.2
        if keys[pygame.K_x]: self.zoom_scale =1


    def custom_draw(self):
        # if self.target_idx > 0 :
        #     self.center_target_camera(self.sprites()[self.target_idx-1 % len(self.sprites())])

        #self.center_target_camera(self.sprites()[0])
        self.keyboard_control()
        self.mouse_grab_control()
        self.zoom_keyboard_control()
        self.internal_surf.fill('black')

        #ground
        #self.display_surface.fill('black')
        self.ground_offset  = self.ground_rect.topleft + self.offset + self.internal_offset
        self.internal_surf.blit(self.ground_surf, self.ground_offset)
        
        # elements
        #print("-----")
        for sprite in sorted(self.sprites(), key= lambda sprite: (sprite.zLevel, sprite.rect.bottom)):
            #print(sprite, f"{sprite.rect.bottom=} {sprite.zLevel=}")
            if sprite.visible:
                offset_pos = sprite.rect.topleft + self.offset + self.internal_offset            
                self.internal_surf.blit(sprite.image, offset_pos)

        self.zoom_scale = min(max(self.zoom_scale,0.5),2)

        self.scaled_surf = pygame.transform.smoothscale (self.internal_surf, self.internal_surface_size_vector*self.zoom_scale)
        self.scaled_rect = self.scaled_surf.get_rect(center=(self.half_w,self.half_h) )
        #self.scaled_rect = self.scaled_surf.get_rect(center = pygame.mouse.get_pos() )

        # mx, my = pygame.mouse.get_pos()
        # left   = mx + (maprect.left - mx) * self.zoom_scale
        # right  = mx + (maprect.right - mx) * self.zoom_scale
        # top    = my + (maprect.top - my) * self.zoom_scale
        # bottom = my + (maprect.bottom - my) * self.zoom_scale
        # maprect = pygame.Rect(left, top, right-left, bottom-top)


       
        self.display_surface.blit(self.scaled_surf, self.scaled_rect )