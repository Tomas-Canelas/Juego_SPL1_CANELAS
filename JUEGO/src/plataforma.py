import pygame
from config import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, start_pos: tuple, path_image: str):
        super().__init__()
        
        
        self.image = pygame.transform.scale(pygame.image.load(path_image).convert_alpha(), SIZE_PLATFORM)
        self.rect = self.image.get_rect()

        self.rect.midbottom = start_pos

        self.velocidad_y = 0


    def update(self):
        pass
        
    def stop(self):
        self.velocidad_y = 0