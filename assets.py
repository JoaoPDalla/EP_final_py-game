import pygame
from constantes import WIDTH,HEIGHT

INICIO = 'inicio'
VILA = 'vila'
VILA_DRAGAO = 'vila_dragao'
VILA_DESTRUIDA = 'vila_destruida'

def load_assets():
    assets = {}
    assets[INICIO] = pygame.transform.scale(pygame.image.load("assets/img/Tela_inicial.jpg"), (WIDTH, HEIGHT))
    assets[VILA] = pygame.transform.scale(pygame.image.load("assets/img/vila.png"), (WIDTH, HEIGHT))
    assets[VILA_DRAGAO] = pygame.transform.scale(pygame.image.load("assets/img/vila_dragao.png"), (WIDTH, HEIGHT))
    assets[VILA_DESTRUIDA] = pygame.transform.scale(pygame.image.load("assets/img/dragão_destruindo.png"), (WIDTH, HEIGHT))

    return assets

