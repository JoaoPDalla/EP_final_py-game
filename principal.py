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
INSTR = 7
N1 = 5
N2=6
estado = TELA_INICIAL  # Define estado inicial do jogo
barradevida = 15
qntd_pocoes = 0
assets = load_assets()
# Redimensiona o ícone de vida para pequeno
VIDA_PEQUENA = pygame.transform.scale(assets[VIDA], (60, 60))  # Ajuste o tamanho se quiser
tempo_apresentacao = pygame.time.get_ticks()  # contador da Cutscene inicial
relogio = pygame.time.Clock()

#Cria o personagem principal e os grupos necessários
mago = Mago(0, HEIGHT // 2 - 30, assets)
todos_sprites = pygame.sprite.Group(mago)
projeteis_mago = pygame.sprite.Group()
projeteis = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
enemys = pygame.sprite.Group()
esculdito = pygame.sprite.Group()
pocs = pygame.sprite.Group()
boss = pygame.sprite.Group()
pode_mudar = False

#Funções para otimização do código
def reposicionar_mago(mago, posicao='esquerda'):
    """Reposiciona o mago dependendo do lado desejado."""
    if posicao == 'esquerda':
        mago.rect.topleft = (0, HEIGHT // 2 - mago.rect.height // 2)
    elif posicao == 'direita':
        mago.rect.topright = (WIDTH, HEIGHT // 2 - mago.rect.height // 2)
    elif posicao == 'topo':
        mago.rect.midtop = (WIDTH // 2, 0)
    elif posicao == 'baixo':
        mago.rect.midbottom = (WIDTH // 2, HEIGHT)
    elif isinstance(posicao, tuple):  # Se quiser passar coordenadas específicas
        mago.rect.topleft = posicao
def atualizar():
        #adota variaveis como globais
        global barradevida, ultimo_ataque_perto,qntd_pocoes
        
        #Realiza os movimentos do mago
        teclas = pygame.key.get_pressed()
        mago.mover(teclas,dt)
        #Da update nos inimigos e nos objetos e os desenha na tela
        for enemy in enemys:
            enemy.update(mago)
        todos_sprites.update()
        for mige in boss:
            mige.update(mago,projeteis,todos_sprites)
        for inimiga in inimigos:
            inimiga.update(mago, projeteis, todos_sprites)
        enemys.draw(TELA)
        boss.draw(TELA)
        todos_sprites.draw(TELA)
        inimigos.draw(TELA)
        # Verifica colisão entre mago e poção
        coleta_pocao = pygame.sprite.spritecollide(mago,pocs,True)
        if len(coleta_pocao) > 0:
            qntd_pocoes +=1
        # Verifica colisão entre mago e projéteis
        dano_mago = pygame.sprite.spritecollide(mago, projeteis, True)
        if len(dano_mago) > 0 and mago.verifica_escudo() == False:
            barradevida -= 1
        # Verifica colisão corpo a corpo entre mago e inimigos
        colisao_com_inimigos = pygame.sprite.spritecollide(mago, inimigos, False)
        for enemy in enemys:
            if enemy.ataque_melle(mago):
                if not mago.verifica_escudo():
                    barradevida -=1
        if len(colisao_com_inimigos) > 0 and mago.verifica_escudo() == False:
            now = pygame.time.get_ticks()
            if now - ultimo_ataque_perto > cooldown_ataque_perto:
                ultimo_ataque_perto = pygame.time.get_ticks()
                barradevida -= 1  # Reduz vida do mago
        # Verifica colisão entre projéteis e inimigos
        for proj in projeteis_mago:
            inimigos_atacados = pygame.sprite.spritecollide(proj, inimigos, False)
            for inimige in inimigos_atacados:
                inimige.levar_dano(1)  # Aplica 1 de dano
                proj.kill()
            
            enemys_atacados = pygame.sprite.spritecollide(proj, enemys, False)
            for enemy in enemys_atacados:
                enemy.levar_dano(1)  # Aplica 1 de dano
                proj.kill()
            for mageee in boss:
                if mageee.hitbox.colliderect(proj.rect):
                    mageee.levar_dano(1)
                    proj.kill()
        # Desenhando as vidas no canto superior esquerdo
        for i in range(barradevida):
            pos_x = 10 + i * (VIDA_PEQUENA.get_width() + 5)  # Espaçamento entre os corações
            pos_y = 10  # Canto superior
            TELA.blit(VIDA_PEQUENA, (pos_x, pos_y))


# ===== Loop principal =====
while estado != DONE:
    relogio.tick(FPS)
    dt = 120
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
                    estado = INSTR
        elif estado == INSTR:
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
            #Adiciona os inimigos do tutorial em posições fixas
            if Primeira_fase == False:
                if rooms==4:
                    for i in range(1):
                        inimigos.add(longo_alcance(1000, 500))
                    for i in range(1):
                        enemys.add(inimigo(600, 600))
                    for i in range(1):
                        p = pocao_vida(500,500)
                        pocs.add(p)
                        todos_sprites.add(p)
                    pygame.mixer.music.stop
                    pygame.mixer.music.unload
                    pygame.mixer.music.load("assets/sound/field_music.mp3")
                    pygame.mixer.music.set_volume(0.4)
                    pygame.mixer.music.play(loops=-1)
                    Primeira_fase = True
                elif rooms==3:
                    if Primeira_fase == False:
                        for i in range(1):
                            i1 = inimigo(400,500)
                            i2 = inimigo(400,400)
                            i3 = inimigo(400,600)
                            enemys.add(i1,i2,i3)
                        Primeira_fase=True   
                elif rooms==2:
                    if Primeira_fase==False:
                        for i in range(1):
                            l1 = longo_alcance(800,700)
                            l2 = longo_alcance(950,840)
                            l3 = longo_alcance(982,450)
                            l4 = longo_alcance(723,354)
                            l5 = longo_alcance(943,843)
                            inimigos.add(l1,l2,l3,l4,l5)
                        Primeira_fase=True
                elif rooms==1:
                    if Primeira_fase == False:
                        for i in range(1):
                            i1 = inimigo(400,500)
                            i2 = inimigo(400,400)
                            i3 = inimigo(400,600)
                            enemys.add(i1,i2,i3)
                        for i in range(1):
                            l1 = longo_alcance(800,700)
                            l2 = longo_alcance(950,840)
                            l3 = longo_alcance(982,450)
                            l4 = longo_alcance(723,354)
                            l5 = longo_alcance(943,843)
                            inimigos.add(l1,l2,l3,l4,l5)
                        Primeira_fase=True
            #Realiza as ações do personagem como ataque ou uso de consumiveis
            if evento.type == pygame.MOUSEBUTTONDOWN:
                #Ataque base
                if evento.button in [1, 3]:
                    tipo = evento.button - 1 if evento.button == 1 else 2
                    proj = mago.atacar(tipo, pygame.mouse.get_pos())
                    if proj:
                        todos_sprites.add(proj)
                        projeteis_mago.add(proj)
            if evento.type == pygame.KEYDOWN:
                #Ataque do espaço
                if evento.key == pygame.K_SPACE:
                    proj = mago.super(projeteis_mago,todos_sprites,pygame.mouse.get_pos())
                    if proj:
                        todos_sprites.add(proj)
                        projeteis_mago.add(proj)
                #Escudo de proteção
                if evento.key == pygame.K_c:
                    area = mago.especial()
                    if area:
                        todos_sprites.add(area)
                        esculdito.add(area)
                #Uso da poção de cura
                if evento.key == pygame.K_g and qntd_pocoes >= 0:
                    qntd_pocoes -= 1
                    barradevida +=1
            #Mudança para a próxima fase
            if mago.rect.right >= WIDTH:
                if len(inimigos) == 0 and len(enemys) == 0:
                    reposicionar_mago(mago, 'esquerda')
                    if rooms>=1:
                        Primeira_fase=False
                        rooms-=1
                    if rooms==0:
                        estado = N1
        #Primeiro nivel da dungeon
        elif estado == N1:
            #Cria os inimigos do 1 nivel da dungeon
            if segunda_fase == False:
                for i in range(1):
                    l1 = longo_alcance(800,700)
                    l2 = longo_alcance(950,840)

                    inimigos.add(l1,l2,l3,l4,l5)
                for i in range(1):
                    i2 = inimigo(400,400)
                    i3 = inimigo(400,600)
                    enemys.add(i1,i2,i3)
                for i in range(1):
                    magao = DragaoInimigo(300,300)
                    boss.add(magao)
                for i in range(1):
                    p = pocao_vida(800,500)
                    pocs.add(p)
                    todos_sprites.add(p)
                segunda_fase = True
                pygame.mixer.music.stop
                pygame.mixer.music.unload
                pygame.mixer.music.load("assets/sound/tower_music.mp3")
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play(loops=-1)
            #Realiza as ações do personagem como ataque ou uso de consumiveis
            if evento.type == pygame.MOUSEBUTTONDOWN:
                #ataque base
                if evento.button in [1, 3]:
                    tipo = evento.button - 1 if evento.button == 1 else 2
                    proj = mago.atacar(tipo, pygame.mouse.get_pos())
                    if proj:
                        todos_sprites.add(proj)
                        projeteis_mago.add(proj)
            if evento.type == pygame.KEYDOWN:
                #Ataque do espaço
                if evento.key == pygame.K_SPACE:
                    proj = mago.super(projeteis_mago,todos_sprites,pygame.mouse.get_pos())
                    if proj:
                        todos_sprites.add(proj)
                        projeteis_mago.add(proj)
                #Uso da poção
                if evento.key == pygame.K_g and qntd_pocoes > 0:
                    qntd_pocoes -= 1
                    barradevida +=1
                #Ativação do Escudo
                if evento.key == pygame.K_c:
                    area = mago.especial()
                    if area:
                        todos_sprites.add(area)
                        esculdito.add(area)

                            
    # ----- Atualiza estado do jogo
    TELA.fill((0, 0, 0))
    if estado == TELA_INICIAL:
        TELA.blit(assets[INICIO], (0, 0))
    elif estado == INSTR:
        TELA.blit(assets[INSTRUCOES],(0,0))
        if pygame.time.get_ticks() - tempo_apresentacao > 5000:
            estado = APRESENTACAO
    elif estado == APRESENTACAO:
        TELA.blit(assets[VILA], (0, 0))
        if pygame.time.get_ticks() - tempo_apresentacao > 10000:
            estado = "img2"
    elif estado == "img2":
        TELA.blit(assets[VILA_DRAGAO], (0, 0))
        if pygame.time.get_ticks() - tempo_apresentacao > 15000:
            estado = "img3"
    elif estado == "img3":
        TELA.blit(assets[VILA_DESTRUIDA], (0, 0))
        if pygame.time.get_ticks() - tempo_apresentacao > 20000:
            estado = TUTORIAL
    
    #Atualiza os inimigos no tutorial
    elif estado == TUTORIAL:
        TELA.blit(assets[BTUTORIAL], (0, 0))
        atualizar()
    
    #Atualiza os inimigos no nivel 1 da dungeon
    elif estado == N1:
        TELA.blit(assets[BDUNGEON], (0, 0))
        atualizar()
    
    # ----- Gera saídas
    pygame.display.update()
# ===== Finalização =====
pygame.quit()