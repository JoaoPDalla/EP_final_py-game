# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random
from constantes import *
import math

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
        if agora - self.ultimo_ataque >= COOLDOWN_MS:
            self.ultimo_ataque = agora
            cores = [VERMELHO, VERDE, AMARELO, BRANCO]
            return Projetil(self.rect.centerx, self.rect.centery, alvo, cores[tipo])
        return None

    def especial(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_area >= COOLDOWN_MS_Ataque_area:
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

class inimigo(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image =pygame.Surface((40,60))
        self.image.fill(VERMELHO)
        self.rect = self.image.get_rect(center=(x, y))
        self.vel=2
        self.attack_range=400

    def update(self,mago):
        dx=mago.rect.centerx-self.rect.centerx
        dy=mago.rect.centery-self.rect.centery
        if math.hypot(dx,dy)<=self.attack_range:
            angulo = math.atan2(dy, dx)
            self.rect.x += self.vel * math.cos(angulo)
            self.rect.y += self.vel * math.sin(angulo)
        else:
            var_x=random.randint(-5,5)
            var_y=random.randint(-5,5)
            self.rect.x+=self.vel*var_x
            self.rect.y+=self.vel*var_y

        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))