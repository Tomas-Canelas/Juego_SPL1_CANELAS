import pygame
import sys
import random

from config import *
from personaje import Personaje
from enemigo import Enemy
from plataforma import Platform
import json

class Game:
    def __init__(self) -> None:
        pygame.init()

        self.reloj = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("My game")
        self.fondo = pygame.transform.scale(pygame.image.load(".\\assets\images\\fondo_medieval.jpg").convert(), SCREEN_SIZE)
        
        self.sprites = pygame.sprite.Group()
        self.enemigos = pygame.sprite.Group()
        self.plataformas = pygame.sprite.Group()
        self.plataformas_creadas = False
        
        
        self.personaje = Personaje(SCREEN_MID_BOTTOM, self.plataformas)
        self.sprites.add(self.personaje)
        
        self.player = 0
        self.score = 0
        self.is_playing = False
        self.is_game_over = False
        self.is_win = False
        self.is_running = False
        
        self.level_1 = False
        self.level_2 = False
        self.supevivencia = False
        self.flag = True
        
        #Botones
        self.boton_restart_rect = pygame.Rect(200, 450, 200, 50)
        self.boton_salir_rect = pygame.Rect(600, 450, 200, 50)
        self.boton_nivel_1_rect = pygame.Rect(200, 400, 200, 50)
        self.boton_nivel_2_rect = pygame.Rect(600, 400, 200, 50)
        self.boton_supervivencia_rect = pygame.Rect(340, 300, 350, 50)
        
        self.fuente = pygame.font.SysFont("century", SIZE_FONT)
        
    def run(self):
        self.is_running = True
        
        while self.is_running:
            self.reloj.tick(FPS)
            self.handler_events()
            if self.is_playing:
                self.update()
            self.render()

    def handler_events(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if self.boton_nivel_1_rect.collidepoint(evento.pos):
                    self.is_playing = True
                    self.level_1 = True
                elif self.boton_nivel_2_rect.collidepoint(evento.pos):
                    self.is_playing = True
                    self.level_2 = True
                elif self.boton_supervivencia_rect.collidepoint(evento.pos):
                    self.is_playing = True
                    self.supevivencia = True
                elif self.boton_restart_rect.collidepoint(evento.pos):
                    self.guardar_puntaje()
                    self.restart_game()
                elif self.boton_salir_rect.collidepoint(evento.pos):
                    self.guardar_puntaje()
                    self.exit()
                
    def update(self):
        self.levels()

        self.detectar_colisiones()
        self.kill_elements_out_screen()
        self.sprites.update()
        self.sprites.add(self.personaje.arco.arrows)
        
    def render(self):
        if self.is_game_over:
            self.show_game_over_screen()
        elif self.is_playing:
            self.screen.blit(self.fondo, ORIGIN)
            self.scoring()
            self.sprites.draw(self.screen)
        elif self.is_win:
            self.show_win_screen()
        else:
            self.home_screen()
            
        pygame.display.flip()
        
    def crear_enemigos(self, speed_enemy):
        if len(self.enemigos) == 0:
            for i in range(MAX_ENEMYS):
                right = random.randint(0, 1)

                if right:
                    x = random.randrange(-500, 0)
                    pos = (x, HEIGHT)
                else:
                    x = random.randrange(WIDTH, WIDTH + 500)
                    pos = (x, HEIGHT)
                    
                
                enemigo = Enemy(pos, right, speed_enemy)
                self.enemigos.add(enemigo)
                self.sprites.add(enemigo)

    def crear_plataformas(self):
        if not self.plataformas_creadas:
            self.plataformas_creadas = True
            self.plataforma = Platform((300, 500), ".\\assets\images\plataforma.png")
            self.plataforma2 = Platform((700, 360), ".\\assets\images\plataforma.png")
            self.sprites.add(self.plataforma, self.plataforma2)
            self.plataformas.add(self.plataforma, self.plataforma2)

    def stop_sprites(self):
        for sprite in self.sprites:
            sprite.stop()

    def detectar_colisiones(self):
        
        #Verificando si las flechas chocan con los enemigos
        for arrow in self.personaje.arco.arrows:
            lista = pygame.sprite.spritecollide(arrow, self.enemigos, True)
            if len(lista) != 0:
                arrow.kill()
                # self.personaje.arco.max_arrows -= 1
                self.score += len(lista) * 100

        #Verificando si el personaje choca con un enemigo
        lista = pygame.sprite.spritecollide(self.personaje, self.enemigos, False)
        if len(lista) != 0:
            self.game_over()

    def kill_elements_out_screen(self):
        for enemigo in self.enemigos:
            if enemigo.rect.left >= WIDTH + 500 or enemigo.rect.right <= -500:
                enemigo.kill()
                
        for arrow in self.personaje.arco.arrows:
            if arrow.rect.right <= 0 or arrow.rect.left >= WIDTH:
                arrow.kill()
                # self.personaje.arco.max_arrows -= 1

    def game_over(self):
        self.stop_sprites()
        self.is_game_over = True
        self.is_playing = False

    def exit(self):
        self.is_running = False
    
    def show_game_over_screen(self):
        fondo_game_over = pygame.transform.scale(pygame.image.load(".\\assets\images\game_over.jpg").convert(), SCREEN_SIZE)
        self.screen.blit(fondo_game_over, ORIGIN)
        
        self.scoring()
        
        pygame.draw.rect(self.screen, ROJO, self.boton_salir_rect)
        texto_salir = self.fuente.render("SALIR", True, NEGRO)
        pos_salir = texto_salir.get_rect(center= self.boton_salir_rect.center)
        self.screen.blit(texto_salir, pos_salir)
        
        pygame.draw.rect(self.screen, VERDE, self.boton_restart_rect)
        texto_restart = self.fuente.render("RESTART", True, NEGRO)
        pos_restart = texto_restart.get_rect(center= self.boton_restart_rect.center)
        self.screen.blit(texto_restart, pos_restart)
        
    def restart_game(self):
        self.is_game_over = False
        self.is_win = False
        self.score = 0
        self.personaje.rect.midbottom = SCREEN_MID_BOTTOM
        
        self.level_1 = False
        self.level_2 = False
        self.supevivencia = False
        self.flag = True
        
        self.plataformas_creadas = False
        self.sprites.empty()
        self.enemigos.empty()
        self.personaje.arco.arrows.empty()
        
        self.sprites.add(self.personaje)

    def home_screen(self):
        fondo_home_screen = pygame.transform.scale(pygame.image.load(".\\assets\images\\fondo_medieval.jpg").convert(), SCREEN_SIZE)
        self.screen.blit(fondo_home_screen, ORIGIN)
        
        texto_titulo = self.fuente.render("BATALLA MEDIEVAL", True, BLANCO)
        pos_titulo = texto_titulo.get_rect(center= (500, 100))
        self.screen.blit(texto_titulo, pos_titulo)
        
        
        pygame.draw.rect(self.screen, VERDE, self.boton_nivel_1_rect)
        texto_level_1 = self.fuente.render("FACIL", True, NEGRO)
        pos_level_1 = texto_level_1.get_rect(center= self.boton_nivel_1_rect.center)
        self.screen.blit(texto_level_1, pos_level_1)
        
        pygame.draw.rect(self.screen, ROJO, self.boton_nivel_2_rect)
        texto_level_2 = self.fuente.render("DIFICIL", True, NEGRO)
        pos_level_2 = texto_level_2.get_rect(center= self.boton_nivel_2_rect.center)
        self.screen.blit(texto_level_2, pos_level_2)

        pygame.draw.rect(self.screen, AMARILLO, self.boton_supervivencia_rect)
        texto_supervivencia = self.fuente.render("SUPERVIVENCIA", True, NEGRO)
        pos_supervivencia = texto_supervivencia.get_rect(center= self.boton_supervivencia_rect.center)
        self.screen.blit(texto_supervivencia, pos_supervivencia)

    def win(self, puntaje_win: int):
        if self.score >= puntaje_win:
            self.stop_sprites()
            self.is_playing = False
            self.is_win = True

    def show_win_screen(self):
        self.screen.fill(NEGRO)
        win = pygame.transform.scale(pygame.image.load(".\\assets\images\VICTORY.png").convert(), (600,300))
        self.screen.blit(win, (200, 100))
        
        pygame.draw.rect(self.screen, ROJO, self.boton_salir_rect)
        texto_salir = self.fuente.render("SALIR", True, NEGRO)
        pos_salir = texto_salir.get_rect(center= self.boton_salir_rect.center)
        self.screen.blit(texto_salir, pos_salir)
        
        pygame.draw.rect(self.screen, VERDE, self.boton_restart_rect)
        texto_restart = self.fuente.render("RESTART", True, NEGRO)
        pos_restart = texto_restart.get_rect(center= self.boton_restart_rect.center)
        self.screen.blit(texto_restart, pos_restart)
    
    def levels(self):
        if self.level_1:
            speed_enemy = SPEED_ENEMY
            self.win(1000)
        elif self.level_2:
            speed_enemy = SPEED_ENEMY + 3
            self.crear_plataformas()
            self.win(3000)
        elif self.supevivencia:
            speed_enemy = SPEED_ENEMY + 2
            self.crear_plataformas()
        self.crear_enemigos(speed_enemy)
    
    def scoring(self):
        puntaje = self.fuente.render(f"  SCORE: {self.score}", True , BLANCO)
        pos_puntaje = puntaje.get_rect()
        self.screen.blit(puntaje, pos_puntaje)
        
    def guardar_puntaje(self):
        self.player += 1
        if self.level_1:
            path = ".\puntajes\puntajes_level_1.json"
        elif self.level_2:
            path = ".\puntajes\puntajes_level_2.json"
        elif self.supevivencia:
            path = ".\puntajes\puntajes_supervivencia.json"
            
        with open(path, "a") as file:
            json.dump({"Nombre": f"player{self.player}", "Score": self.score}, file, indent=2)
            