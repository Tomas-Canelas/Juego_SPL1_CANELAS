import pygame
from config import *
from arrow import Arrow

class Arco:
    def __init__(self, max_arrows: int, path_sound: str):
        self.max_arrows = max_arrows
        # self.sound_shot = pygame.mixer.Sound(path_sound)
        self.arrows = pygame.sprite.Group()
        
        
