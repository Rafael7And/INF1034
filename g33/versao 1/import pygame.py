import pygame

pygame.init()
tela = pygame.display.set_mode((960, 528))   # largura x altura em pixels
pygame.display.set_caption("Fuga Hipotética")
relogio = pygame.time.Clock()

x = 100  # posição de um quadrado de teste

rodando = True
while rodando:
    # 1) ler eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:   # clicou no X da janela
            rodando = False

    # 2) atualizar
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_RIGHT]:
        x += 4
    if teclas[pygame.K_LEFT]:
        x -= 4

    # 3) desenhar
    tela.fill((120, 190, 240))                              # céu
    pygame.draw.rect(tela, (200, 50, 50), (x, 400, 40, 60))  # quadrado
    pygame.display.flip()                                   # mostra o quadro

    relogio.tick(60)  # limita a 60 quadros por segundo

pygame.quit()