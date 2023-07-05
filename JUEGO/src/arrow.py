import pygame
from config import *

class Arrow(pygame.sprite.Sprite):
    def __init__(self, personaje, path_image: str):
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load(path_image).convert_alpha(), SIZE_ARROW)
        self.rect = self.image.get_rect()
        
        if personaje.left:
            self.rect.midright = personaje.rect.midleft
            self.velocidad_x = -SPEED_ARROW
        else:
            self.velocidad_x = SPEED_ARROW
            self.rect.midleft = personaje.rect.midright
            

    def update(self):
        self.rect.x += self.velocidad_x

    def stop(self):
        self.velocidad_x = 0

    
