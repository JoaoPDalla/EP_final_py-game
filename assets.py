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
BOSSP = 'Vilão parado'
BOSSA = 'Vilão atacando'
BOSSD = 'Vilão levando dano'
POCAO = 'Cura'
PRJS= 'som do projétil'
F1 = 'Poder 1'
F2 = 'poder 2'
V1 = 'Vilão 1'
INSTRUCOES = 'instrucoes'
DRINK=pygame.mixer.Sound("assets/sound/gulp_sound.wav")
OVER = 'Over'
def cortar_spritesheet(sheet, largura, altura, linhas, colunas):
    frames = []
    for linha in range(linhas):
        for coluna in range(colunas):
            x = coluna * largura
            y = linha * altura
            frame = sheet.subsurface(pygame.Rect(x, y, largura, altura))
            frame = pygame.transform.scale(frame, (620, 740))
            frames.append(frame)
    return frames

def cortar_spritesheet2(sheet, linhas, colunas,diminuir):
    largura_total, altura_total = sheet.get_size()
    largura = largura_total // colunas
    altura = altura_total // linhas
    frames = []
    for linha in range(linhas):
        for coluna in range(colunas):
            x = coluna * largura
            y = linha * altura
            frame = sheet.subsurface(pygame.Rect(x, y, largura, altura))
            if diminuir == True:
                frame = pygame.transform.scale(frame, (largura/9, altura/9))
            elif diminuir == 'A':
                frame = pygame.transform.scale(frame, (220, 340))
            frames.append(frame)
            
    return frames




def load_assets():
    assets = {}
    assets[INICIO] = pygame.transform.scale(pygame.image.load("assets/img/Tela_inicial.jpg"), (WIDTH, HEIGHT))
    assets[VILA] = pygame.transform.scale(pygame.image.load("assets/img/vila.png"), (WIDTH, HEIGHT))
    assets[VILA_DRAGAO] = pygame.transform.scale(pygame.image.load("assets/img/vila_dragao.png"), (WIDTH, HEIGHT))
    assets[VILA_DESTRUIDA] = pygame.transform.scale(pygame.image.load("assets/img/dragão_destruindo.png"), (WIDTH, HEIGHT))
    assets[VIDA] = pygame.transform.scale(pygame.image.load("assets/img/ChatGPT_Image_24_de_mai._de_2025__15_00_52-removebg-preview.png"), (WIDTH, HEIGHT))
    assets[BTUTORIAL] = pygame.transform.scale(pygame.image.load("assets/img/Mapa Tutorial.png"), (WIDTH, HEIGHT))
    assets[BDUNGEON] = pygame.transform.scale(pygame.image.load("assets/img/dangeon.png"), (WIDTH, HEIGHT))
    assets[INSTRUCOES] = pygame.transform.scale(pygame.image.load("assets/img/intrucoes.png"), (WIDTH, HEIGHT))
    assets[OVER] = pygame.transform.scale(pygame.image.load("assets/img/Derrota.png"), (WIDTH, HEIGHT))
    assets[PRJS]=pygame.mixer.Sound("assets/sound/projectile_sound.wav")
    rbe = []
    
    for i in range(1,10):
        # Os arquivos de animação são numerados de 00 a 08
        filename = os.path.join('assets/img/Raposinha base _ lado esquerdo{}.png.png'.format(i))
        img = pygame.image.load(filename).convert_alpha()
        img = pygame.transform.scale(img, (90, 120))
        rbe.append(img)
    assets[RBE_ANM] = rbe

    bossp = pygame.image.load('assets/img/Idle.png').convert_alpha()
    assets[BOSSP] = cortar_spritesheet(bossp, 250, 250, 1, 8)

    bossa = pygame.image.load('assets/img/Attack2.png').convert_alpha()
    assets[BOSSA] = cortar_spritesheet(bossa, 250, 250, 1, 8)

    bossd = pygame.image.load('assets/img/Attack2.png').convert_alpha()
    assets[BOSSD] = cortar_spritesheet(bossd, 250, 250, 1, 8)

    assets[POCAO] = pygame.transform.scale(pygame.image.load("assets/img/cura.png"), (40, 40)).convert_alpha()

    rbe = pygame.image.load('assets/img/Raposinha fogo _ lado esquerdo.png').convert_alpha()
    assets[RBE_ANM] = cortar_spritesheet2(rbe, 5, 2,True)

    assets[F1] = pygame.transform.scale(pygame.image.load("assets/img/f1.png"), (40, 40))
    assets[F2] = pygame.transform.scale(pygame.image.load("assets/img/f2.png"), (40, 40))

    v1 = pygame.image.load('assets/img/vp.png').convert_alpha()
    assets[V1] = cortar_spritesheet2(v1, 4, 4,'A')

    
    return assets

