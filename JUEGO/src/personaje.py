import pygame
from config import *
from arrow import Arrow
from arco import Arco

class Personaje(pygame.sprite.Sprite):
    def __init__(self, midBottom: tuple, plataformas: pygame.sprite.Group):
        super().__init__()
        
        self.indice = 0
        self.dict_key = "Idle left"

        self.animaciones = self.get_animations()
        self.image = self.animaciones[self.dict_key][self.indice]
        self.rect = self.image.get_rect()
        self.rect.midbottom = midBottom
        
        
        self.velocidad_x = 0
        self.velocidad_y = 0

        self.left = False
        self.saltando = False
        self.inplatform = False
        
        self.plataformas = plataformas
        
        self.altura_salto = ALTURA_SALTO
        self.gravedad = GRAVEDAD
        self.delay_animacion = 0

        self.arco = Arco(MAX_ARROWS, ".\\assets\sounds\Tiro_con_arco.mp3")
        self.disparando = False
        
        

        
    def update(self):
        self.mover_personaje()
        self.jump()
        self.animations()
        
    def stop(self):
        self.velocidad_x = 0
        self.velocidad_y = 0
    
    def mover_personaje(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.x - SPEED_CHARACTER > 0:
            self.velocidad_x = -SPEED_CHARACTER
            self.rect.x += self.velocidad_x
        elif keys[pygame.K_RIGHT] and self.rect.x + SPEED_CHARACTER + self.rect.width < WIDTH:
            self.velocidad_x = SPEED_CHARACTER
            self.rect.x += self.velocidad_x
        else:
            self.velocidad_x = 0
        if keys[pygame.K_UP] and not self.saltando:
            self.saltando = True
            self.inplatform = False
            self.velocidad_y = self.altura_salto
                                    
        if keys[pygame.K_SPACE]:
            if not self.disparando:  # Disparar solo si no se está disparando actualmente
                self.disparar_arco()
                self.disparando = True
        else:
            self.disparando = False
            
    def jump(self):
        if self.saltando:
            self.rect.y += self.velocidad_y  
            self.velocidad_y += self.gravedad  
            #Verificando si el personaje salta arriba de una plataforma
            for plataforma in self.plataformas:
                if self.rect.bottom == plataforma.rect.top and self.velocidad_y > 0 and self.rect.midbottom > plataforma.rect.topleft and self.rect.midbottom < plataforma.rect.topright:
                    self.inplatform = True
            if self.rect.bottom >= HEIGHT or self.inplatform:
                self.velocidad_y = 0  
                self.saltando = False
                
        
    def get_animations(self):
        animations = {
                    "Attack right": 
                        (pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Attack\\5_ATTACK_000.png").convert_alpha(), SIZE_CHARACTER), 
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Attack\\5_ATTACK_003.png").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Attack\\5_ATTACK_005.png").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Attack\\5_ATTACK_007.png").convert_alpha(), SIZE_CHARACTER)), 
                    "Die right": 
                        (pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Die\\7_DIE_000.png").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Die\\7_DIE_003.png").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Die\\7_DIE_005.png").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Die\\7_DIE_007.png").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Die\\7_DIE_009.png").convert_alpha(), SIZE_CHARACTER)), 
                    "Idle right": 
                        (pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Idle\\1_IDLE_000.png ").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Idle\\1_IDLE_001.png ").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Idle\\1_IDLE_002.png ").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Idle\\1_IDLE_003.png ").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Idle\\1_IDLE_004.png ").convert_alpha(), SIZE_CHARACTER)), 
                    "Jump right": 
                        (pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Jump\\4_JUMP_000.png ").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Jump\\4_JUMP_001.png ").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Jump\\4_JUMP_002.png ").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Jump\\4_JUMP_003.png ").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Jump\\4_JUMP_004.png ").convert_alpha(), SIZE_CHARACTER)), 
                    "Walk right": 
                        (pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Walk\\3_RUN_000.png ").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Walk\\3_RUN_001.png ").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Walk\\3_RUN_002.png ").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Walk\\3_RUN_003.png ").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Walk\\3_RUN_004.png ").convert_alpha(), SIZE_CHARACTER)),
                    "Attack left": 
                        (pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Attack\\5_ATTACK_LEFT_000.png").convert_alpha(), SIZE_CHARACTER), 
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Attack\\5_ATTACK_LEFT_003.png").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Attack\\5_ATTACK_LEFT_005.png").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Attack\\5_ATTACK_LEFT_007.png").convert_alpha(), SIZE_CHARACTER)), 
                    "Die left": 
                        (pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Die\\7_DIE_LEFT_000.png").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Die\\7_DIE_LEFT_003.png").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Die\\7_DIE_LEFT_005.png").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Die\\7_DIE_LEFT_007.png").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Die\\7_DIE_LEFT_009.png").convert_alpha(), SIZE_CHARACTER)), 
                    "Idle left": 
                        (pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Idle\\1_IDLE_LEFT_000.png ").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Idle\\1_IDLE_LEFT_001.png ").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Idle\\1_IDLE_LEFT_002.png ").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Idle\\1_IDLE_LEFT_003.png ").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Idle\\1_IDLE_LEFT_004.png ").convert_alpha(), SIZE_CHARACTER)), 
                    "Jump left": 
                        (pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Jump\\4_JUMP_LEFT_000.png ").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Jump\\4_JUMP_LEFT_001.png ").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Jump\\4_JUMP_LEFT_002.png ").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Jump\\4_JUMP_LEFT_003.png ").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Jump\\4_JUMP_LEFT_004.png ").convert_alpha(), SIZE_CHARACTER)), 
                    "Walk left": 
                        (pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Walk\\3_RUN_LEFT_000.png ").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Walk\\3_RUN_LEFT_001.png ").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Walk\\3_RUN_LEFT_002.png ").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Walk\\3_RUN_LEFT_003.png ").convert_alpha(), SIZE_CHARACTER),
                        pygame.transform.scale(pygame.image.load(".\\assets\images\warrior_woman_03\Walk\\3_RUN_LEFT_004.png ").convert_alpha(), SIZE_CHARACTER))
                    }

        return animations
    
    def animations(self):
        if self.velocidad_x < 0:                    #Izquierda
            self.left = True
            if self.saltando:
                self.dict_key = "Jump left"
            else:
                self.dict_key = "Walk left"
                
        elif self.velocidad_x > 0:                 #Derecha
            self.left = False
            if self.saltando:
                self.dict_key = "Jump right"
            else:
                self.dict_key = "Walk right"
                
        elif self.velocidad_x == 0 and not self.saltando:   #Quieto
            if self.left:
                self.dict_key = "Idle left"
            else:
                self.dict_key = "Idle right"

        self.delay_animacion += 1
        if self.delay_animacion >= DELAY_ANIMACION:
            self.delay_animacion = 0
            self.indice += 1
            if self.indice >= 4:
                self.indice = 0
            self.image = self.animaciones[self.dict_key][self.indice]
        
    def disparar_arco(self):
        if not self.disparando and len(self.arco.arrows) <= self.arco.max_arrows:
            if self.left:
                path_image = ".\\assets\images\\flecha_left.png"
            else:
                path_image = ".\\assets\images\\flecha_right.png"
                
            arrow = Arrow(self, path_image)
            # self.arco.sound_shot.play()
            self.arco.arrows.add(arrow)
