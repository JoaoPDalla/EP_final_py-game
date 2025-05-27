import pygame
from constantes import WIDTH,HEIGHT
import os
# ----- Gera tela principal
TELA = pygame.display.set_mode((WIDTH, HEIGHT))  # Modo fullscreen

INICIO = 'inicio'
VILA = 'vila'
VILA_DRAGAO = 'vila_dragao'
VILA_DESTRUIDA = 'vila_destruida'
VIDA = 'Vida'
BTUTORIAL = 'Tela Tutorial'
BDUNGEON = 'Mapa base dungeon'
RBE_ANM = 'Raposa base esquerdo'

def load_assets():
    assets = {}
    assets[INICIO] = pygame.transform.scale(pygame.image.load("assets/img/Tela_inicial.jpg"), (WIDTH, HEIGHT))
    assets[VILA] = pygame.transform.scale(pygame.image.load("assets/img/vila.png"), (WIDTH, HEIGHT))
    assets[VILA_DRAGAO] = pygame.transform.scale(pygame.image.load("assets/img/vila_dragao.png"), (WIDTH, HEIGHT))
    assets[VILA_DESTRUIDA] = pygame.transform.scale(pygame.image.load("assets/img/dragão_destruindo.png"), (WIDTH, HEIGHT))
    assets[VIDA] = pygame.transform.scale(pygame.image.load("assets/img/ChatGPT_Image_24_de_mai._de_2025__15_00_52-removebg-preview.png"), (WIDTH, HEIGHT))
    assets[BTUTORIAL] = pygame.transform.scale(pygame.image.load("assets/img/Mapa Tutorial.png"), (WIDTH, HEIGHT))
    assets[BDUNGEON] = pygame.transform.scale(pygame.image.load("assets/img/dangeon.png"), (WIDTH, HEIGHT))
    rbe = []
    
    for i in range(1,10):
        # Os arquivos de animação são numerados de 00 a 08
        filename = os.path.join('assets/img/Raposinha base _ lado esquerdo{}.png.png'.format(i))
        img = pygame.image.load(filename).convert_alpha()
        img = pygame.transform.scale(img, (90, 120))
        rbe.append(img)
    assets[RBE_ANM] = rbe
    return assets

