# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import math
import random
from assets import *
from constantes import *

pygame.init()
pygame.mixer.init()

# Classe do Mago
class Mago(pygame.sprite.Sprite):
    def __init__(self, x, y, assets):
        super().__init__()

        self.sprites = assets[RBE_ANM]  # Lista com as imagens de animação
        self.frame = 0
        self.image = self.sprites[self.frame]  # Começa com a primeira imagem
        self.rect = self.image.get_rect(topleft=(x, y))

        self.vel = 8
        self.ultimo_ataque = 0
        self.ultimo_area = 0
        self.escudo = False

        self.animation_timer = 0
        self.animation_speed = 100  # milissegundos entre troca de sprite

    def verifica_escudo(self):
        if self.escudo:
            agora = pygame.time.get_ticks()
            if agora - self.ultimo_area > duracao_escudo:
                self.escudo = False
                return self.escudo
            return self.escudo
        return self.escudo

    def mover(self, teclas, dt):
        moving = False
        if teclas[pygame.K_w]:
            self.rect.y -= self.vel
            moving = True
        if teclas[pygame.K_s]:
            self.rect.y += self.vel
            moving = True
        if teclas[pygame.K_a]:
            self.rect.x -= self.vel
            moving = True
        if teclas[pygame.K_d]:
            self.rect.x += self.vel
            moving = True

        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

        # Atualiza a animação só se estiver se movendo
        if moving:
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.frame = (self.frame + 1) % len(self.sprites)
                self.image = self.sprites[self.frame]
        else:
            self.frame = 0
            self.image = self.sprites[self.frame]

    def atacar(self, tipo, alvo):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_ataque >= cooldown_magia_bas:
            self.ultimo_ataque = agora
            cores = [VERMELHO, VERDE, AMARELO, BRANCO]

            dx, dy = alvo[0] - self.rect.centerx, alvo[1] - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist == 0:
                dist = 1
            offset_x = (dx / dist) * 50
            offset_y = (dy / dist) * 50

            return Projetil(
                self.rect.centerx + offset_x,
                self.rect.centery + offset_y,
                alvo,
                cores[tipo]
            )
        return None

    def especial(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_area >= cooldown_especial:
            self.ultimo_area = agora
            self.escudo = True
            return Especial(self)
        return None
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
        if pygame.time.get_ticks() - self.tempo_criacao > duracao_escudo:
            self.kill()



# Classe Projetil
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

# Classe para projéteis específicos do Dragão
class ProjetilFogo(pygame.sprite.Sprite):
    def __init__(self, x, y, angulo):
        super().__init__()
        self.image = pygame.Surface((20, 10))
        self.image.fill((255, 100, 0))  # Cor laranja para projéteis de fogo
        self.rect = self.image.get_rect(center=(x, y))
        self.vel = 6

        # Calcula deslocamento inicial baseado no ângulo
        deslocamento = 50  # 50 pixels fora do inimigo
        self.rect.x += deslocamento * math.cos(angulo)
        self.rect.y += deslocamento * math.sin(angulo)

        self.vx = self.vel * math.cos(angulo)
        self.vy = self.vel * math.sin(angulo)

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if (self.rect.right < 0 or self.rect.left > WIDTH or
            self.rect.bottom < 0 or self.rect.top > HEIGHT):
            self.kill()

# Classe base para inimigos
class inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(VERMELHO)
        self.rect = self.image.get_rect(center=(x, y))
        self.vida = 3  # Vida inicial
        self.vel = 2
        self.aggro_range = 500
        self.ultimo_ataque_melle = 0
        self.cooldown_movimento = 100
        self.range_melle = 100
        self.v_ocioso = 0.4
        self.var_x = random.choice([-self.v_ocioso, 0, self.v_ocioso])
        self.var_y = random.choice([-self.v_ocioso, 0, self.v_ocioso])

    def update(self, mago):
        dx = mago.rect.centerx - self.rect.centerx
        dy = mago.rect.centery - self.rect.centery
        if math.hypot(dx, dy) <= self.aggro_range and math.hypot(dx,dy) >= self.range_melle:
            angulo = math.atan2(dy, dx)
            self.rect.x += self.vel * math.cos(angulo)
            self.rect.y += self.vel * math.sin(angulo)
        elif math.hypot(dx,dy) >= self.range_melle:
            if self.cooldown_movimento > 0:
                self.rect.x += self.vel * self.var_x
                self.rect.y += self.vel * self.var_y
                self.cooldown_movimento -= 1
            else:
                self.var_x = random.choice([-self.v_ocioso, 0, self.v_ocioso])
                self.var_y = random.choice([-self.v_ocioso, 0, self.v_ocioso])
                self.cooldown_movimento = 100
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))
    
    def levar_dano(self, dano):
        self.vida -= dano
        if self.vida <= 0:
            self.kill()
    def ataque_melle(self,mago):
        dx = mago.rect.centerx - self.rect.centerx
        dy = mago.rect.centery - self.rect.centery
        if math.hypot(dx,dy) <= self.range_melle:
            agora = pygame.time.get_ticks()
            if agora-self.ultimo_ataque_melle >= cooldown_ataque_perto:
                self.ultimo_ataque_melle = agora
                return True
        return False

# Classe longo alcance
class longo_alcance(inimigo):
    def __init__(self, x, y):
        super().__init__(x, y)  # Chama o construtor da classe base
        self.image = pygame.Surface((30, 30))
        self.image.fill(VERMELHO)
        self.range_ataque = 600
        self.range_perseguicao = 900
        self.timer_movimento_aleatorio = 0
        self.vel = 2
        self.dir_x = random.choice([-1, 0, 1])
        self.dir_y = random.choice([-1, 0, 1])
        self.ultimo_ataque = 0

    def update(self, mago, projeteis, todos_sprites):
        dx = mago.rect.centerx - self.rect.centerx
        dy = mago.rect.centery - self.rect.centery
        distancia = math.hypot(dx, dy)
        if distancia <= self.range_ataque:
            agora = pygame.time.get_ticks()
            if agora - self.ultimo_ataque >= cooldown_inim_longe:
                self.ultimo_ataque = agora
                angulo = math.atan2(dy, dx)

                # Calcula posição inicial com deslocamento de 50 pixels
                deslocamento = 50
                x_inicial = self.rect.centerx + deslocamento * math.cos(angulo)
                y_inicial = self.rect.centery + deslocamento * math.sin(angulo)

                proj = Projetil(x_inicial, y_inicial, mago.rect.center, ROXO)
                projeteis.add(proj)
                todos_sprites.add(proj)
        elif distancia <= self.range_perseguicao:
            angulo = math.atan2(dy, dx)
            self.rect.x += self.vel * math.cos(angulo)
            self.rect.y += self.vel * math.sin(angulo)
        else:
            self.timer_movimento_aleatorio -= 1
            if self.timer_movimento_aleatorio <= 0:
                self.dir_x = random.choice([-1, 0, 1])
                self.dir_y = random.choice([-1, 0, 1])
                self.timer_movimento_aleatorio = random.randint(30, 60)
            self.rect.x += self.dir_x
            self.rect.y += self.dir_y
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

# Classe Dragao Inimigo com vida
class DragaoInimigo(inimigo):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 100))  # Rosa avermelhado para o dragão
        self.range_ataque = 500
        self.range_perseguicao = 800
        self.vida = 10  # Vida inicial maior para o dragão
        self.vel = 1.5
        self.ultimo_ataque = 0
        self.movimento_aleatorio = 0
        self.dir_x = random.choice([-1, 0, 1])
        self.dir_y = random.choice([-1, 0, 1])

    def update(self, mago, projeteis, todos_sprites):
        dx = mago.rect.centerx - self.rect.centerx
        dy = mago.rect.centery - self.rect.centery
        distancia = math.hypot(dx, dy)
        if distancia <= self.range_ataque:
            agora = pygame.time.get_ticks()
            if agora - self.ultimo_ataque >= cooldown_dragao:
                self.ultimo_ataque = agora
                angulo_central = math.atan2(dy, dx)
                abertura_cone = math.radians(60)  # Cone de disparo de 60 graus
                num_projeteis = 7

                for i in range(num_projeteis):
                    offset = (i - (num_projeteis - 1) / 2) / (num_projeteis - 1)
                    angulo = angulo_central + offset * abertura_cone

                    # Calcula posição inicial do projétil, com deslocamento de 50 pixels
                    deslocamento = 50
                    x_inicial = self.rect.centerx + deslocamento * math.cos(angulo)
                    y_inicial = self.rect.centery + deslocamento * math.sin(angulo)

                    proj = ProjetilFogo(x_inicial, y_inicial, angulo)
                    projeteis.add(proj)
                    todos_sprites.add(proj)
        elif distancia <= self.range_perseguicao:
            angulo = math.atan2(dy, dx)
            self.rect.x += self.vel * math.cos(angulo)
            self.rect.y += self.vel * math.sin(angulo)
        else:
            self.movimento_aleatorio -= 1
            if self.movimento_aleatorio <= 0:
                self.dir_x = random.choice([-1, 0, 1])
                self.dir_y = random.choice([-1, 0, 1])
                self.movimento_aleatorio = random.randint(30, 60)
            self.rect.x += self.dir_x * self.vel
            self.rect.y += self.dir_y * self.vel
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))
class pocao_vida(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.Surface((20,20))
        self.image.fill((255,0,150))
        self.rect = self.image.get_rect(center=(x, y))
