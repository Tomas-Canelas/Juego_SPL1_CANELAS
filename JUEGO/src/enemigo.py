import pygame
from config import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, start_pos: tuple, right: bool, speed_enemy: int):
        super().__init__()
        
        self.right = right
        self.indice = 0
        self.animaciones = self.get_animations()
        self.image = self.animaciones[right][self.indice]
        self.rect = self.image.get_rect()

        self.rect.midbottom = start_pos

        self.velocidad_x = speed_enemy
        
        self.delay_animacion = 0



    def update(self):
        if self.right:
            self.rect.x += self.velocidad_x
        else:
            self.rect.x -= self.velocidad_x
        self.animations()
        
    def stop(self):
        self.velocidad_x = 0


    def get_animations(self):
        animations = (
                        (pygame.transform.scale(pygame.image.load(".\\assets\images\enemy_01\WALK_LEFT_000.png").convert_alpha(), SIZE_ENEMY),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\enemy_01\WALK_LEFT_001.png").convert_alpha(), SIZE_ENEMY),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\enemy_01\WALK_LEFT_002.png").convert_alpha(), SIZE_ENEMY),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\enemy_01\WALK_LEFT_003.png").convert_alpha(), SIZE_ENEMY),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\enemy_01\WALK_LEFT_004.png").convert_alpha(), SIZE_ENEMY),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\enemy_01\WALK_LEFT_005.png").convert_alpha(), SIZE_ENEMY),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\enemy_01\WALK_LEFT_006.png").convert_alpha(), SIZE_ENEMY)),
                        (pygame.transform.scale(pygame.image.load(".\\assets\images\enemy_01\WALK_000.png").convert_alpha(), SIZE_ENEMY),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\enemy_01\WALK_001.png").convert_alpha(), SIZE_ENEMY),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\enemy_01\WALK_002.png").convert_alpha(), SIZE_ENEMY),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\enemy_01\WALK_003.png").convert_alpha(), SIZE_ENEMY),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\enemy_01\WALK_004.png").convert_alpha(), SIZE_ENEMY),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\enemy_01\WALK_005.png").convert_alpha(), SIZE_ENEMY),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\enemy_01\WALK_006.png").convert_alpha(), SIZE_ENEMY))
                    )
        
        return animations
    
    def animations(self):
        self.delay_animacion += 1
        if self.delay_animacion >= DELAY_ANIMACION:
            self.delay_animacion = 0
            self.indice += 1
            if self.indice >= 4:
                self.indice = 0
            self.image = self.animaciones[self.right][self.indice]