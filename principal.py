# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
pygame.init()
pygame.mixer.init()  # Inicializa especificamente o módulo de áudio
from constantes import *
from classes import *
from assets import *
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
barradevida = 15
assets = load_assets()
# Redimensiona o ícone de vida para pequeno
VIDA_PEQUENA = pygame.transform.scale(assets[VIDA], (60, 60))  # Ajuste o tamanho se quiser
tempo_apresentacao = pygame.time.get_ticks()  # contador da Cutscene inicial
relogio = pygame.time.Clock()
mago = Mago(WIDTH // 2, HEIGHT // 2)
enemy = inimigo(WIDTH // 2, HEIGHT // 2)
inim_longo = longo_alcance(100, 100)
dragao = DragaoInimigo(300, 300)
todos_sprites = pygame.sprite.Group(mago)
projeteis_mago = pygame.sprite.Group()
projeteis = pygame.sprite.Group()
inimigos = pygame.sprite.Group(inim_longo, dragao)
enemys = pygame.sprite.Group(enemy)
esculdito = pygame.sprite.Group()
# ===== Loop principal =====
while estado != DONE:
    relogio.tick(FPS)
    # ----- Trata eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            estado = DONE
        # Tela inicial
        if estado == TELA_INICIAL:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    estado = DONE
                else:
                    estado = APRESENTACAO
        # Cutscene inicial
        elif estado == APRESENTACAO:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    estado = DONE
                elif evento.key == pygame.K_RETURN:
                    estado = TUTORIAL
        # Tutorial
        elif estado == TUTORIAL:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button in [1, 3]:
                    tipo = evento.button - 1 if evento.button == 1 else 2
                    proj = mago.atacar(tipo, pygame.mouse.get_pos())
                    if proj:
                        todos_sprites.add(proj)
                        projeteis_mago.add(proj)
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    proj = mago.atacar(3, pygame.mouse.get_pos())
                    if proj:
                        todos_sprites.add(proj)
                        projeteis_mago.add(proj)
                if evento.key == pygame.K_c:
                    area = mago.especial()
                    if area:
                        todos_sprites.add(area)
                        esculdito.add(area)
                        
    # ----- Atualiza estado do jogo
    TELA.fill((0, 0, 0))
    if estado == TELA_INICIAL:
        TELA.blit(assets[INICIO], (0, 0))
    
    elif estado == APRESENTACAO:
        TELA.blit(assets[VILA], (0, 0))
        if pygame.time.get_ticks() - tempo_apresentacao > 5000:
            estado = "img2"
    elif estado == "img2":
        TELA.blit(assets[VILA_DRAGAO], (0, 0))
        if pygame.time.get_ticks() - tempo_apresentacao > 10000:
            estado = "img3"
    elif estado == "img3":
        TELA.blit(assets[VILA_DESTRUIDA], (0, 0))
        if pygame.time.get_ticks() - tempo_apresentacao > 15000:
            estado = TUTORIAL
    
    elif estado == TUTORIAL:
        TELA.blit(assets[BTUTORIAL], (0, 0))
        teclas = pygame.key.get_pressed()
        mago.mover(teclas)
        enemy.update(mago)
        enemys.draw(TELA)
        todos_sprites.update()
        for inimiga in inimigos:
            inimiga.update(mago, projeteis, todos_sprites)
        todos_sprites.draw(TELA)
        inimigos.draw(TELA)
        # Verifica colisão entre o escudo
        if mago.verifica_escudo() == True:
            for escudo in esculdito:
                projeteis_bloqueados = pygame.sprite.spritecollide(escudo,projeteis,True)
        # Verifica colisão entre mago e projéteis
        dano_mago = pygame.sprite.spritecollide(mago, projeteis, True)
        if len(dano_mago) > 0 and mago.verifica_escudo() == False:
            barradevida -= 1
        # Verifica colisão corpo a corpo entre mago e inimigos
        colisao_com_inimigos = pygame.sprite.spritecollide(mago, inimigos, False)
        colisao_com_enemys = pygame.sprite.spritecollide(mago, enemys, False)
        if len(colisao_com_inimigos) > 0 or len(colisao_com_enemys) > 0 and mago.verifica_escudo() == False:
            now = pygame.time.get_ticks()
            if now - ultimo_ataque_perto > cooldown_ataque_perto:
                ultimo_ataque_perto = pygame.time.get_ticks()
                barradevida -= 1  # Reduz vida do mago
        # Verifica colisão entre projéteis e inimigos
        for proj in projeteis_mago:
            inimigos_atacados = pygame.sprite.spritecollide(proj, inimigos, False)
            for inimigo in inimigos_atacados:
                inimigo.levar_dano(1)  # Aplica 1 de dano
                proj.kill()
            
            enemys_atacados = pygame.sprite.spritecollide(proj, enemys, False)
            for enemy in enemys_atacados:
                enemy.levar_dano(1)  # Aplica 1 de dano
                proj.kill()
        # Desenhando as vidas no canto superior esquerdo
        for i in range(barradevida):
            pos_x = 10 + i * (VIDA_PEQUENA.get_width() + 5)  # Espaçamento entre os corações
            pos_y = 10  # Canto superior
            TELA.blit(VIDA_PEQUENA, (pos_x, pos_y))
    
    # ----- Gera saídas
    pygame.display.update()
# ===== Finalização =====
pygame.quit()