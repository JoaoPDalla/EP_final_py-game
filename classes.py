# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import math
import random
from assets import *
from constantes import *

pygame.init()
pygame.mixer.init()
assets = load_assets()

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
        self.ultimo_super = 0
        self.ultimo_area = 0
        self.escudo = False
        self.projetil_som=pygame.mixer.Sound("assets/sound/projectile_sound.wav")
        self.super_som=pygame.mixer.Sound("assets/sound/explosion_sound.wav")
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
            self.projetil_som.play()
            self.ultimo_ataque = agora
            poderes = [assets[F1], assets[F3], assets[F2], assets[F4]]

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
                poderes[tipo]
            )
        return None

    def especial(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_area >= cooldown_especial:
            self.ultimo_area = agora
            self.escudo = True
            return Especial(self)
        return None
    def super(self,projeteis_mago,todos_sprites,alvo):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_super >= cooldown_super:
            self.super_som.play()
            self.ultimo_super = agora
            dx, dy = alvo[0] - self.rect.centerx, alvo[1] - self.rect.centery
            angulo_central = math.atan2(dy, dx)
            abertura_cone = math.radians(60)
            num_projeteis = 3

            for i in range(num_projeteis):
                offset = (i - (num_projeteis - 1) / 2) / (num_projeteis - 1)
                angulo = angulo_central + offset * abertura_cone

                deslocamento = 50
                x_inicial = self.rect.centerx + deslocamento * math.cos(angulo)
                y_inicial = self.rect.centery + deslocamento * math.sin(angulo)
                alvo_x = x_inicial + math.cos(angulo) * 100
                alvo_y = y_inicial + math.sin(angulo) * 100
                proj = Projetil(x_inicial, y_inicial, (alvo_x, alvo_y), assets[F4])
                proj = Projetil(x_inicial, y_inicial, (alvo_x, alvo_y), assets[F2])
                projeteis_mago.add(proj)
                todos_sprites.add(proj)
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
    def __init__(self, x, y, alvo, poder):
        super().__init__()
        self.image = poder
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
        self.image = assets[F3]
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
        
        self.sprites = assets[V1]  # Lista com as imagens de animação
        self.frame = 0
        self.image = self.sprites[self.frame]  # Começa com a primeira imagem
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

        
        # Controle de animação
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 150  # Tempo em ms entre os frames

        self.vida = 3  # Vida inicial
        self.vel = 2
        self.aggro_range = 500
        self.ultimo_ataque_melle = 0
        self.cooldown_movimento = 100
        self.range_melle = 100
        self.v_ocioso = 0.4
        self.var_x = random.choice([-self.v_ocioso, 0, self.v_ocioso])
        self.var_y = random.choice([-self.v_ocioso, 0, self.v_ocioso])
        self.morte = pygame.mixer.Sound("assets/sound/dying_sound.wav")

    def update(self, mago):
        dx = mago.rect.centerx - self.rect.centerx
        dy = mago.rect.centery - self.rect.centery
        distancia = math.hypot(dx, dy)
        
        movendo = False
        
        if distancia <= self.aggro_range and distancia >= self.range_melle:
            angulo = math.atan2(dy, dx)
            self.rect.x += self.vel * math.cos(angulo)
            self.rect.y += self.vel * math.sin(angulo)
            movendo = True
        elif distancia >= self.range_melle:
            if self.cooldown_movimento > 0:
                self.rect.x += self.vel * self.var_x
                self.rect.y += self.vel * self.var_y
                self.cooldown_movimento -= 1
                movendo = False
            else:
                self.var_x = random.choice([-self.v_ocioso, 0, self.v_ocioso])
                self.var_y = random.choice([-self.v_ocioso, 0, self.v_ocioso])
                self.cooldown_movimento = 100
                movendo = True
        
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

        # Atualiza a animação apenas se estiver se movendo
        if movendo:
            self.atualizar_animacao()
        else:
            self.frame = 0
            self.image = self.sprites[self.frame]

    def atualizar_animacao(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame = (self.frame + 1) % len(self.sprites)
            self.image = self.sprites[self.frame]
            self.image = self.sprites[self.frame]
            self.rect = self.image.get_rect(center=self.rect.center)
            self.mask = pygame.mask.from_surface(self.image)

    
    def levar_dano(self, dano):
        self.vida -= dano
        if self.vida <= 0:
            self.morte.play()
            self.kill()

    def ataque_melle(self, mago):
        dx = mago.rect.centerx - self.rect.centerx
        dy = mago.rect.centery - self.rect.centery
        if math.hypot(dx, dy) <= self.range_melle:
            agora = pygame.time.get_ticks()
            if agora - self.ultimo_ataque_melle >= cooldown_ataque_perto:
                self.ultimo_ataque_melle = agora
                return True
        return False


# Classe longo alcance
class longo_alcance(inimigo):
    def __init__(self, x, y):
        super().__init__(x, y)  # Chama o construtor da classe base

        # Sobrescreve sprites e imagem
        self.sprites = assets[V2]  # Lista com imagens de animação de longo alcance
        self.frame = 0
        self.image = self.sprites[self.frame]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

        self.range_ataque = 600
        self.range_perseguicao = 900
        self.timer_movimento_aleatorio = 0
        self.vel = 2
        self.dir_x = random.choice([-1, 0, 1])
        self.dir_y = random.choice([-1, 0, 1])
        self.ultimo_ataque = 0

        # Controle de animação
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 150  # ms entre os frames

    def update(self, mago, projeteis, todos_sprites):
        dx = mago.rect.centerx - self.rect.centerx
        dy = mago.rect.centery - self.rect.centery
        distancia = math.hypot(dx, dy)

        movendo = True

        if distancia <= self.range_ataque:
            agora = pygame.time.get_ticks()
            if agora - self.ultimo_ataque >= cooldown_inim_longe:
                self.ultimo_ataque = agora
                angulo = math.atan2(dy, dx)

                # Calcula posição inicial com deslocamento
                deslocamento = 50
                x_inicial = self.rect.centerx + deslocamento * math.cos(angulo)
                y_inicial = self.rect.centery + deslocamento * math.sin(angulo)

                proj = Projetil(x_inicial, y_inicial, mago.rect.center, assets[F3])
                projeteis.add(proj)
                todos_sprites.add(proj)
        elif distancia <= self.range_perseguicao:
            angulo = math.atan2(dy, dx)
            self.rect.x += self.vel * math.cos(angulo)
            self.rect.y += self.vel * math.sin(angulo)
            movendo = True
        else:
            self.timer_movimento_aleatorio -= 1
            if self.timer_movimento_aleatorio <= 0:
                self.dir_x = random.choice([-1, 0, 1])
                self.dir_y = random.choice([-1, 0, 1])
                self.timer_movimento_aleatorio = random.randint(30, 60)
            self.rect.x += self.dir_x
            self.rect.y += self.dir_y
            if self.dir_x != 0 or self.dir_y != 0:
                movendo = True

        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

        # Atualiza a animação apenas se estiver se movendo
        if movendo:
            self.atualizar_animacao()
        else:
            self.frame = 0
            self.image = self.sprites[self.frame]
            self.mask = pygame.mask.from_surface(self.image)

    def atualizar_animacao(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame = (self.frame + 1) % len(self.sprites)
            self.image = self.sprites[self.frame]
            self.rect = self.image.get_rect(center=self.rect.center)
            self.mask = pygame.mask.from_surface(self.image)


# Classe Dragao Inimigo com vida
class DragaoInimigo(inimigo):
    def __init__(self, x, y):
        super().__init__(x, y)

        # Sprites de animação
        self.sprites_parado = assets[BOSSP]
        self.sprites_andando = assets[BOSSP]
        self.sprites_atacando = assets[BOSSA]
        self.sprites_dano = assets[BOSSD]

        self.estado = 'parado'
        self.frame_index = 0
        self.anim_timer = 0
        self.anim_delay = 150

        self.dano_timer = 0
        self.tempo_dano = 500  # 0.5 segundo de animação de dano

        self.image = self.sprites_parado[0]

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Define uma hitbox menor para colisão
        self.hitbox = self.rect.inflate(-400, -560) 

        self.range_ataque = 500
        self.range_perseguicao = 800
        self.vida = 10
        self.vel = 1.5
        self.ultimo_ataque = 0
        self.movimento_aleatorio = 0
        self.dir_x = random.choice([-1, 0, 1])
        self.dir_y = random.choice([-1, 0, 1])
        self.morte=pygame.mixer.Sound("assets/sound/explosion_sound.wav")
    def atualizar_animacao(self):
        agora = pygame.time.get_ticks()
        if agora - self.anim_timer >= self.anim_delay:
            self.anim_timer = agora
            self.frame_index = (self.frame_index + 1) % 8  # 8 sprites

            if self.estado == 'parado':
                self.image = self.sprites_parado[self.frame_index]
            elif self.estado == 'andando':
                self.image = self.sprites_parado[self.frame_index]
            elif self.estado == 'atacando':
                self.image = self.sprites_atacando[self.frame_index]
            elif self.estado == 'dano':
                self.image = self.sprites_dano[self.frame_index]

    def update(self, jogador):
        # Atualiza animação
        self.atualizar_animacao()

        # Lógica de dano
        if self.estado == 'dano':
            if pygame.time.get_ticks() - self.dano_timer > self.tempo_dano:
                self.estado = 'parado'

        # Exemplo simples de movimentação
        distancia = math.hypot(jogador.rect.centerx - self.rect.centerx, jogador.rect.centery - self.rect.centery)
        if distancia <= self.range_perseguicao:
            self.estado = 'andando'
            if distancia <= self.range_ataque:
                self.estado = 'atacando'
                # Aqui pode colocar lógica de ataque real

        # Movimentação simples aleatória
        if self.estado == 'andando':
            self.rect.x += self.dir_x * self.vel
            self.rect.y += self.dir_y * self.vel
        self.hitbox.center = self.rect.center 


    def update_animacao(self):
        agora = pygame.time.get_ticks()

        if self.estado == 'dano':
            if agora - self.dano_timer >= self.tempo_dano:
                self.estado = 'parado'  # ou andava antes, pode ajustar
                self.frame_index = 0
        else:
            if agora - self.anim_timer > self.anim_delay:
                self.anim_timer = agora
                self.frame_index = (self.frame_index + 1) % len(self.sprites_estado())

        self.image = self.sprites_estado()[self.frame_index]
        self.hitbox.center = self.rect.center

    def sprites_estado(self):
        if self.estado == 'andando':
            return self.sprites_parado
        elif self.estado == 'atacando':
            return self.sprites_atacando
        elif self.estado == 'dano':
            return self.sprites_dano
        else:
            return self.sprites_parado

    def sofrer_dano(self, dano):
        self.vida -= dano
        self.estado = 'dano'
        self.frame_index = 0
        self.dano_timer = pygame.time.get_ticks()
        if self.vida <= 0:
            self.morte.play()
            self.kill()

    def update(self, mago, projeteis, todos_sprites):
        if self.estado != 'dano':
            dx = mago.rect.centerx - self.rect.centerx
            dy = mago.rect.centery - self.rect.centery
            distancia = math.hypot(dx, dy)

            if distancia <= self.range_ataque:
                self.estado = 'atacando'
                agora = pygame.time.get_ticks()
                if agora - self.ultimo_ataque >= cooldown_dragao:
                    self.ultimo_ataque = agora
                    angulo_central = math.atan2(dy, dx)
                    abertura_cone = math.radians(60)
                    num_projeteis = 7

                    for i in range(num_projeteis):
                        offset = (i - (num_projeteis - 1) / 2) / (num_projeteis - 1)
                        angulo = angulo_central + offset * abertura_cone

                        deslocamento = 50
                        x_inicial = self.rect.centerx + deslocamento * math.cos(angulo)
                        y_inicial = self.rect.centery + deslocamento * math.sin(angulo)

                        proj = ProjetilFogo(x_inicial, y_inicial, angulo)
                        projeteis.add(proj)
                        todos_sprites.add(proj)

            elif distancia <= self.range_perseguicao:
                self.estado = 'andando'
                angulo = math.atan2(dy, dx)
                self.rect.x += self.vel * math.cos(angulo)
                self.rect.y += self.vel * math.sin(angulo)
            else:
                self.estado = 'andando'
                self.movimento_aleatorio -= 1
                if self.movimento_aleatorio <= 0:
                    self.dir_x = random.choice([-1, 0, 1])
                    self.dir_y = random.choice([-1, 0, 1])
                    self.movimento_aleatorio = random.randint(30, 60)
                self.rect.x += self.dir_x * self.vel
                self.rect.y += self.dir_y * self.vel

            if self.dir_x == 0 and self.dir_y == 0 and distancia > self.range_ataque:
                self.estado = 'parado'

            self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

        self.update_animacao()

#Classe da poção de vida
class pocao_vida(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = assets[POCAO]
        self.rect = self.image.get_rect(center=(x, y))
