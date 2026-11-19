
import pygame
from pygame.locals import QUIT, KEYDOWN
pygame.init()

# 1 JANELA+++++

LARGURA, ALTURA = 960, 528
tela = pygame.display.set_mode((LARGURA, ALTURA))   # largura x altura  pixels
pygame.display.set_caption("A FUGA")
relogio = pygame.time.Clock()                       # controla a velocidade do jogo (FPS)
fonte = pygame.font.Font(None, 28)


CHAO = 432          # y (altura na tela) 
VEL_ANDAR = 5    #pixels que o personagem anda por quadro
GRAVIDADE = 0.8      #velocidade vertical aumenta por quadro
FORCA_PULO = 15    #velocidade para cima no começo do pulo
LARGURA_JOGADOR = 30
ALTURA_EM_PE = 57
ALTURA_ABAIXADO = 32
DURACAO_SOCO = 22   

###########3) "estado" do personagem

x = 100               # posição horizontal (lado esquerdo do personagem)
pe = CHAO             # posição vertical dos PÉS (usar os pés facilita agachar)
vel_y = 0             # velocidade vertical: negativo = subindo, positivo = descendo
no_chao = True        # está tocando o chão?
abaixado = False
direcao = 1           # 1 = olhando para a direita, -1 = para a esquerda
soco_tempo = 0        # quadros que faltam para o soco acabar (0 = sem soco)
soco_acertou = False  # o soco atual já acertou o alvo? (evita contar duas vezes)

# teste  para ver o soco funcionando >> mobs futuros
alvo = pygame.Rect(600, CHAO - 60, 40, 60)
alvo_piscar = 0
pontos = 0

