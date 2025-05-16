import pygame
from constantes import HEIGHT,WIDTH
from imagens import assets

pygame.init()
pygame.mixer.init()

#Grupos da classe sem organização necessária
groups = pygame.sprite.Group
all_power1 = pygame.sprite.Group
all_power2 = pygame.sprite.Group
all_power3 = pygame.sprite.Group
groups['all_power1'] = all_power1
groups['all_power2'] = all_power2
groups['all_power3'] = all_power3

#Corpo do personagem
class Mago:
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.image = assets['personagem']
        self.rect = self.image.get_rect()
        self.rect.bottom = HEIGHT-10
        self.rect.centerx = WIDTH/2
        self.speedx = 0
        self.speedy = 0

        # self.last_shot =pygame.time.get_ticks
        # self.shoot_tickets = 500

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Mantem dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    def power1(self):
        #temporariamente emcima do personagem
        new_power1 = power1(self.assets, self.rect.top, self.rect.centerx)
        self.groups['all_sprites'].add(new_power1)
        self.groups['all_power1'].add(new_power1)
    def power2(self):
        #temporariamente emcima do personagem
        new_power2 = power2(self.assets, self.rect.top, self.rect.centerx)
        self.groups['all_sprites'].add(new_power2)
        self.groups['all_power2'].add(new_power2)
    def power3(self):
        #temporariamente emcima do personagem
        new_power3 = power3(self.assets, self.rect.top, self.rect.centerx)
        self.groups['all_sprites'].add(new_power3)
        self.groups['all_power3'].add(new_power3)
#classes dos poderes sem nenhuma aprofundação ainda
class power1:
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
class power2:
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
class power3:
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
