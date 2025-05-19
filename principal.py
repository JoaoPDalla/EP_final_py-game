# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
pygame.init()
pygame.mixer.init()  # Inicializa especificamente o módulo de áudio
from constantes import *
from classes import *
from assets import load_assets, INICIO

assets = load_assets()

# ----- Gera tela principal
TELA = pygame.display.set_mode((WIDTH, HEIGHT))  # Modo fullscreen
pygame.display.set_caption('Fox_Tower')
# ----- Inicia estruturas de dados
DONE = 0
TELA_INICIAL = 1  # Usar constantes para representar estados
APRESENTACAO = 2
TUTORIAL = 3
MORRENDO = 4
estado = TELA_INICIAL  # Define estado inicial do jogo

tempo_apresentacao = pygame.time.get_ticks() # contador da Cutscene inicial
relogio = pygame.time.Clock()
mago = Mago(WIDTH//2, HEIGHT//2)
todos_sprites = pygame.sprite.Group(mago)
projeteis = pygame.sprite.Group()

# ===== Loop principal =====
while estado != DONE:
    relogio.tick(FPS)

    # ----- Trata eventos
    for evento in pygame.event.get():
        # Só verifica o teclado se está no estado de jogo
        if evento.type == pygame.QUIT:
            estado = DONE 
        # Tela inicial
        if estado == TELA_INICIAL:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    estado = DONE
                else:
                    # Qualquer tecla inicia o jogo
                    estado = APRESENTACAO    
        # Cutscene inicial            
        elif estado == APRESENTACAO:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    estado = DONE
                else:
                    # Qualquer tecla inicia o jogo
                    estado = TUTORIAL
        elif estado == TUTORIAL:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button in [1, 3]:  
                    tipo = evento.button - 1 if evento.button == 1 else 2  # botão esquerdo: 0, direito: 2
                    proj = mago.atacar(tipo, pygame.mouse.get_pos())
                    if proj:
                        todos_sprites.add(proj)
                        projeteis.add(proj)
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    proj = mago.atacar(3, pygame.mouse.get_pos())
                    if proj:
                        todos_sprites.add(proj)
                        projeteis.add(proj)
                if evento.key == pygame.K_c:
                    area = mago.especial()
                    if area:
                        todos_sprites.add(area)

    # ----- Atualiza estado do jogo
    # Atualização da tela inicial
    if estado == TELA_INICIAL:
        TELA.blit(assets[INICIO], (0, 0))

    teclas = pygame.key.get_pressed()
    mago.mover(teclas)

    todos_sprites.update()

    TELA.fill((0, 0, 0))
    todos_sprites.draw(TELA)
    pygame.display.flip()

pygame.quit()