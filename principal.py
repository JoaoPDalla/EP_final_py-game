import pygame

from constantes import *
from classes import *

relogio = pygame.time.Clock()
TELA = pygame.display.set_mode((HEIGHT, WIDTH))

relogio = pygame.time.Clock()
mago = Mago(WIDTH//2, HEIGHT//2)
todos_sprites = pygame.sprite.Group(mago)
projeteis = pygame.sprite.Group()

# Loop principal
rodando = True
while rodando:
    relogio.tick(FPS)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
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

    teclas = pygame.key.get_pressed()
    mago.mover(teclas)

    todos_sprites.update()

    TELA.fill((30, 30, 30))
    todos_sprites.draw(TELA)
    pygame.display.flip()

pygame.quit()