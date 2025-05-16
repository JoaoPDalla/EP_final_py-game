import pygame
from constantes import HEIGHT,WIDTH
pygame.init()
pygame.mixer.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Fox_Tower')
window.fill((0, 0, 0))  # Preenche com a cor branca


assets = {}
assets['personagem'] = pygame.image.load('assets/img/').convert