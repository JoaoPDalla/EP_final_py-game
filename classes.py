# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
from constantes import *
import math
import random

pygame.init()
pygame.mixer.init()

#Grupos da classe sem organização necessária
#Tirei depois fazer :0

#Corpo do personagem
class Mago(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40,60))
        self.image.fill(AZUL)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel = 5
        self.ultimo_ataque = 0
        self.ultimo_area = 0

    def mover(self, teclas):
        if teclas[pygame.K_w]:
            self.rect.y -= self.vel
        if teclas[pygame.K_s]:
            self.rect.y += self.vel
        if teclas[pygame.K_a]:
            self.rect.x -= self.vel
        if teclas[pygame.K_d]:
            self.rect.x += self.vel

        # Limita o movimento à tela
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def atacar(self, tipo, alvo):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_ataque >= cooldown_magia_bas:
            self.ultimo_ataque = agora
            cores = [VERMELHO, VERDE, AMARELO, BRANCO]
            return Projetil(self.rect.centerx, self.rect.centery, alvo, cores[tipo])
        return None

    def especial(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_area >= cooldown_especial:
            self.ultimo_area = agora
            return Especial(self)
        return None
#classes dos poderes sem nenhuma aprofundação ainda
class Projetil(pygame.sprite.Sprite):
    def __init__(self, x, y, alvo, cor):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(cor)
        self.rect = self.image.get_rect(center=(x, y))

        dx, dy = alvo[0] - x, alvo[1] - y
        dist = math.hypot(dx, dy)
        self.vel = 10
        self.vx = dx / dist * self.vel
        self.vy = dy / dist * self.vel

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if (self.rect.right < 0 or self.rect.left > WIDTH or
                self.rect.bottom < 0 or self.rect.top > HEIGHT):
            self.kill()

# Classe para ataque em área
class Especial(pygame.sprite.Sprite):
    def __init__(self, mago):
        super().__init__()
        self.image = pygame.Surface((150, 150), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (160, 32, 240, 100), (75, 75), 75)
        self.rect = self.image.get_rect(center=mago.rect.center)
        self.mago = mago
        self.tempo_criacao = pygame.time.get_ticks()

    def update(self):
        self.rect.center = self.mago.rect.center
        if pygame.time.get_ticks() - self.tempo_criacao > 300:
            self.kill()
class longo_alcance(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.Surface((30,30))
        self.image.fill(VERMELHO)
        self.rect = self.image.get_rect(center=(x, y))
        self.range_ataque = 600
        self.range_perseguicao = 900
        self.random_move_timer = 0
        self.vel = 2
        self.dir_x = random.choice([-1, 0, 1])
        self.dir_y = random.choice([-1, 0, 1])
        self.ultimo_ataque = 0
    def update(self, mago, projeteis,todos_sprites):
        #calcula distancia do inimigo pro mago
        dx = mago.rect.centerx - self.rect.centerx
        dy = mago.rect.centery - self.rect.centery
        distancia = math.hypot(dx, dy)
        #testa se o mago está na distancia de ataque do inimigo
        if distancia <= self.range_ataque:
            agora = pygame.time.get_ticks()
            #testa o cooldown e faz o disparo
            if agora - self.ultimo_ataque >= cooldown_inim_longe:
                self.ultimo_ataque = agora
                proj = Projetil(self.rect.centerx,self.rect.centery,mago.rect.center, ROXO)
                projeteis.add(proj)
                todos_sprites.add(proj)
        #testa se o mago ta dentro do range de perseguição e começa a persegui-lo
        elif distancia <= self.range_perseguicao:
            anglo = math.atan2(dy,dx)
            self.rect.x += self.vel * math.cos(anglo)
            self.rect.y += self.vel * math.sin(anglo)
        #caso fora dos dois range faz movimentos aleatorios
        else:
            self.random_move_timer -=1
            if self.random_move_timer <= 0:
                self.dir_x = random.choice([-1,0,1])
                self.dir_y = random.choice([-1,0,1])
                self.random_move_timer = random.randint(30,60)
            self.rect.x += self.dir_x
            self.rect.y += self.dir_y
        #limite da tela
        self.rect.clamp_ip(pygame.Rect(0,0,WIDTH,HEIGHT))
            
