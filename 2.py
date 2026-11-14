"""
Fuga Hipotética — plataforma 2D em Pygame

Controles:
  ← →      andar
  Espaço   pular (segurar = pulo mais alto)
  ↓        abaixar
  Z        soco (também quebra blocos 'B')
  X        atirar com a arma atual (sem arma = poder básico)
  P        pausar / continuar
  Enter    começar (tela de título)
  R        reiniciar (game over / vitória)
  Esc      sair

Pontuação:
  inimigo derrotado 100 · arma coletada 50 · chefe 1000 · fase concluída 500
  Bandeiras de checkpoint ('!') mudam o ponto de renascimento.

Armas (itens no mapa):
  g  Arma comum      -> inimigo leva carimbo "CANCELADO" e some
  c  Lança-carteira  -> granada em arco; inimigos atingidos viram fumaça
  r  Raio            -> inimigo muda de skin e vai embora (não dá mais dano)
"""
import os
import glob
import math
import random
from collections import deque
import pygame

# ---------------- CONFIGURAÇÕES ----------------
LARGURA, ALTURA = 960, 528
TILE = 48
FPS = 60
GRAVIDADE = 0.6
VEL_MAX_QUEDA = 14
VEL_ANDAR = 4.5
FORCA_PULO = 13.5
ALTURA_SPRITE = 64
PASTA = os.path.dirname(os.path.abspath(__file__))
SKINS_VISUAIS = {}

# munição ao pegar cada arma / recarga entre tiros (frames)
ARMAS = {
    "poder":    {"nome": "Poder",          "municao": None, "recarga": 30},
    "arma":     {"nome": "Arma comum",     "municao": 15,   "recarga": 12},
    "carteira": {"nome": "Lança-carteira", "municao": 5,    "recarga": 40},
    "raio":     {"nome": "Raio",           "municao": 8,    "recarga": 25},
}
DANO_CHEFE = {"soco": 1, "pisao": 1, "poder": 1, "arma": 1, "raio": 2, "carteira": 3}
PONTOS = {"inimigo": 100, "item": 50, "chefe": 1000, "fase": 500}

# Legenda do mapa:
#   '#' chão   'B' bloco quebrável   'P' início   'V' van   'K' chefe   '!' checkpoint
#   'E' burocrata   'S' sapo de toga   'F' panfleteiro   'M' cartazista
#   'g' arma comum  'c' lança-carteira  'r' raio
FASES = [
    {
        "nome": "Fase 1 - Calçadão de Copacabana",
        "tema": "copacabana",
        "chefe": "megafone",
        "cores": {"ceu": (120, 190, 240), "predios": (90, 150, 200),
                  "chao": (214, 184, 120), "bloco": (230, 130, 60)},
        "mapa": [
            "",
            "",
            "",
            "",
            "                      BBB",
            "                                       ###",
            "             BB                             r",
            "          g                      ##                         c",
            "    P              E      ##         S  !     F     M  B              K             V",
            "##############   ###########   ##################   #######################################",
            "##############   ###########   ##################   #######################################",
        ],
    },
    {
        "nome": "Fase 2 - São Paulo",
        "tema": "saopaulo",
        "chefe": "fiscal",
        "cores": {"ceu": (165, 170, 180), "predios": (120, 125, 135),
                  "chao": (110, 110, 115), "bloco": (180, 90, 70)},
        "mapa": [
            "",
            "",
            "",
            "",
            "                                      F r",
            "                                      ####                      c",
            "        g                             ####                    #####",
            "       ###                  B    #### ####             ##",
            "   P   ###            E     B    #### ####   S   !          #   M      E           F   M   ##      K        V",
            "##############   ####################################      #################   ##################################",
            "##############   ####################################      #################   ##################################",
        ],
    },
    {
        "nome": "Fase 3 - Curitiba e a Fronteira",
        "tema": "curitiba",
        "ponte_inicio": 56,   # coluna do mapa onde começa a ponte para a Argentina
        "chefe": "juiz",
        "cores": {"ceu": (150, 175, 200), "predios": (70, 110, 80),
                  "chao": (95, 120, 85), "bloco": (140, 100, 70)},
        "mapa": [
            "",
            "",
            "",
            "",
            "                ##",
            "              BB",                                 
            "         BB             ###   c",
            "        g                                                         r",
            "    P             S   E       !  F            S   E           F  M B                 K             V",
            "###########   ###########   ###########   ###########   ###############################################",
            "###########   ###########   ###########   ###########   ###############################################",
        ],
    },
]

CHEFES = {
    "megafone": {"nome": "GENERAL RACHADINHA", "vida": 12, "cor": (200, 90, 40),
                 "falas": ["ATENÇÃO, POVO!", "EU FALO MAIS ALTO!", "MICROFONE LIGADO!",
                           "ISSO É UM ABSURDO!"]},
    "fiscal":   {"nome": "Fiscal do Pedágio", "vida": 14, "cor": (230, 190, 40),
                 "falas": ["Cadê o comprovante?", "Taxa extra!", "Volte amanhã.",
                           "Carimbo em três vias!"]},
    "juiz":     {"nome": "Juiz da Toga CABEÇA DE OVO", "vida": 16, "cor": (30, 30, 40),
                 "falas": ["ATOS ANTI DEMOCATICOS!", "FAKE NEWS!", "ESTADO DEMOCRÁTICO!",
                           "JURISDISQUES!"]},
}


# ---------------- UTILITÁRIOS ----------------
def mover_com_colisao(ent, solidos):
    """Move ent (rect, vx, vy) colidindo com os sólidos. Retorna (no_chao, bateu_na_parede)."""
    bateu = False
    ent.rect.x += round(ent.vx)
    for b in solidos:
        if ent.rect.colliderect(b.rect):
            if ent.vx > 0:
                ent.rect.right = b.rect.left
            elif ent.vx < 0:
                ent.rect.left = b.rect.right
            bateu = True
    no_chao = False
    ent.rect.y += round(ent.vy)
    for b in solidos:
        if ent.rect.colliderect(b.rect):
            if ent.vy > 0:
                ent.rect.bottom = b.rect.top
                no_chao = True
            elif ent.vy < 0:
                ent.rect.top = b.rect.bottom
            ent.vy = 0
    return no_chao, bateu


# Faixas da folha de animações (x, y, largura, altura) onde ficam os bonecos de cada estado.
# Os quadros são achados automaticamente dentro de cada faixa, da esquerda para a direita.
FAIXAS_FOLHA = {
    "parado":  (12, 18, 492, 180),
    "andar":   (522, 18, 668, 180),
    "pulo":    (12, 492, 684, 196),
    "abaixar": (714, 492, 474, 196),
    "soco":    (12, 1002, 392, 188),   # usa a animação "empurrar"
}


def recortar_quadros_folha(caminho, faixas):
    """Acha cada boneco dentro das faixas da folha e recorta só ele.

    1. O fundo quadriculado claro que encosta na borda da faixa vira transparente.
    2. O que sobra é separado em pedaços (componentes conectados).
    3. Pedaços pequenos (números "01", sombras, moldura) são descartados.
    Cada quadro fica justo no boneco, então dá para alinhar todos pelos pés.
    """
    folha = pygame.image.load(caminho).convert()
    animacoes = {}
    for estado, ret in faixas.items():
        faixa = folha.subsurface(ret).copy()
        w, h = faixa.get_size()
        claro = pygame.mask.from_threshold(faixa, (220, 220, 220), (37, 37, 37))
        fundo = pygame.mask.Mask((w, h))
        borda = ([(x, 0) for x in range(w)] + [(x, h - 1) for x in range(w)] +
                 [(0, y) for y in range(h)] + [(w - 1, y) for y in range(h)])
        for p in borda:
            if claro.get_at(p) and not fundo.get_at(p):
                fundo.draw(claro.connected_component(p), (0, 0))
        fundo.invert()  # agora: 1 = boneco

        pedacos = []
        for comp in fundo.connected_components(minimum=300):
            r = comp.get_bounding_rects()[0]
            if r.h > 60 and r.w > 30:
                pedacos.append((r, comp))
        pedacos.sort(key=lambda p: p[0].x)

        faixa_alfa = faixa.convert_alpha()
        quadros = []
        for r, comp in pedacos:
            img = comp.to_surface(faixa_alfa.copy(), setsurface=faixa_alfa, unsetcolor=(0, 0, 0, 0))
            quadros.append(img.subsurface(r).copy())
        if quadros:
            animacoes[estado] = quadros
    return animacoes


def carregar_animacoes():
    """Carrega animações do projeto ou usa os quadros de exemplo existentes.

    Para adicionar animações próprias, salve PNGs transparentes em
    assets/jogador/<estado>_<n>.png (por exemplo, andar_01.png).
    Enquanto isso, usa Hero_Walk_01 e Hero_Walk_02 da pasta ``do prof``.
    """
    brutos = {}
    for estado in ("parado", "andar", "pulo", "abaixar", "soco"):
        arquivos = glob.glob(os.path.join(PASTA, "assets", "jogador", f"{estado}_*.png"))
        arquivos.sort(key=lambda a: int(os.path.splitext(a)[0].rsplit("_", 1)[1]))
        if arquivos:
            brutos[estado] = [pygame.image.load(a).convert_alpha() for a in arquivos]

    # Usa a folha de animações que está junto deste arquivo em "versao 1".
    if not brutos:
        folhas = glob.glob(os.path.join(PASTA, "WhatsApp Image*.jpeg"))
        if not folhas:
            folhas = glob.glob(os.path.join(PASTA, "versao 1", "WhatsApp Image*.jpeg"))
        if folhas:
            brutos = recortar_quadros_folha(folhas[0], FAIXAS_FOLHA)

    # Fallback para os quadros PNG antigos, se a folha não estiver disponível.
    if not brutos:
        pastas = [os.path.join(PASTA, "do prof"),
                  os.path.join(os.path.dirname(PASTA), "do prof")]
        for pasta_exemplo in pastas:
            caminhos = [os.path.join(pasta_exemplo, f"Hero_Walk_{n:02}.png") for n in (1, 2)]
            quadros = [pygame.image.load(a).convert_alpha() for a in caminhos if os.path.isfile(a)]
            if quadros:
                brutos = {"parado": [quadros[0]], "andar": quadros,
                          "pulo": [quadros[-1]], "abaixar": [quadros[0]],
                          "soco": [quadros[-1]]}
                break

    if not brutos:
        return {}
    base = brutos.get("parado", brutos.get("andar", next(iter(brutos.values()))))[0]
    for estado in ("parado", "andar", "pulo", "abaixar", "soco"):
        if estado not in brutos:
            brutos[estado] = [base]
    ref = brutos.get("parado", next(iter(brutos.values())))[0]
    fator = ALTURA_SPRITE / ref.get_height()
    return {e: [pygame.transform.scale(
                    i, (max(1, int(i.get_width() * fator)), max(1, int(i.get_height() * fator)))) for i in q]
            for e, q in brutos.items()}


def carregar_tiles():
    """Recorta e ajusta os tiles do tileset usado no exercício de plataforma."""
    caminhos = [os.path.join(PASTA, "do prof", "1", "plataform_tileset.png"),
                os.path.join(os.path.dirname(PASTA), "do prof", "1", "plataform_tileset.png")]
    caminho = next((a for a in caminhos if os.path.isfile(a)), None)
    if caminho is None:
        return {}

    folha = pygame.image.load(caminho).convert_alpha()
    tiles = {}
    recortes = {"chao": (0, 0), "subsolo": (0, 64), "bloco": (0, 128)}
    for nome, (x, y) in recortes.items():
        if x + 64 <= folha.get_width() and y + 64 <= folha.get_height():
            original = folha.subsurface((x, y, 64, 64))
            tiles[nome] = pygame.transform.scale(original, (TILE, TILE))
    return tiles


def carregar_skins():
    """Carrega os sprites ilustrados e remove a margem transparente do arquivo."""
    arquivos = {
        "burocrata": ("mob_burocrata.png", 68),
        "sapo": ("mob_sapo_toga.png", 70),
        "panfleteiro": ("mob_panfleteiro.png", 68),
        "cartazista": ("mob_cartazista.png", 106),
        "patriota": ("mob_patriota.png", 106),
        "megafone": ("boss_megafone.png", 124),
        "fiscal": ("boss_fiscal.png", 124),
        "juiz": ("boss_juiz.png", 124),
    }
    skins = {}
    pasta = os.path.join(PASTA, "assets", "skins")
    for nome, (arquivo, altura) in arquivos.items():
        caminho = os.path.join(pasta, arquivo)
        if not os.path.isfile(caminho):
            continue
        imagem = pygame.image.load(caminho).convert_alpha()
        recorte = imagem.get_bounding_rect()
        if recorte.width and recorte.height:
            imagem = imagem.subsurface(recorte).copy()
        largura = max(1, round(imagem.get_width() * altura / imagem.get_height()))
        skins[nome] = pygame.transform.scale(imagem, (largura, altura))
        skins[f"{nome}_esquerda"] = pygame.transform.flip(skins[nome], True, False)
    return skins


def balao(tela, fonte, texto, x, y):
    """Balão de fala centralizado em x, com a base em y."""
    s = fonte.render(texto, True, (0, 0, 0))
    r = s.get_rect(midbottom=(x, y - 8)).inflate(14, 8)
    pygame.draw.rect(tela, (255, 255, 255), r, border_radius=8)
    pygame.draw.rect(tela, (0, 0, 0), r, 2, border_radius=8)
    pygame.draw.polygon(tela, (255, 255, 255), [(x - 6, r.bottom - 2), (x + 6, r.bottom - 2), (x, y)])
    tela.blit(s, s.get_rect(center=r.center))


# ---------------- ENTIDADES ----------------
class Bloco:
    def __init__(self, x, y, tipo):
        self.rect = pygame.Rect(x, y, TILE, TILE)
        self.tipo = tipo


class Item:
    CORES = {"arma": (60, 60, 60), "carteira": (30, 70, 160), "raio": (60, 220, 230)}

    def __init__(self, x, y, tipo):
        self.rect = pygame.Rect(x + 10, y + 10, 28, 28)
        self.tipo = tipo
        self.t = random.random() * 6

    def desenhar(self, tela, cam_x, fonte):
        self.t += 0.08
        r = self.rect.move(-cam_x, round(math.sin(self.t) * 4))
        pygame.draw.rect(tela, (255, 255, 255), r.inflate(6, 6), border_radius=6)
        pygame.draw.rect(tela, self.CORES[self.tipo], r, border_radius=4)
        letra = fonte.render(self.tipo[0].upper(), True, (255, 255, 255))
        tela.blit(letra, letra.get_rect(center=r.center))


class Jogador:
    LARG, ALT, ALT_ABAIXADO = 30, 58, 36

    def __init__(self, anims):
        self.anims = anims
        self.vidas = 3
        self.pontos = 0
        self.inicio = (0, 0)

    def reiniciar(self):
        x, base = self.inicio
        self.rect = pygame.Rect(x, base - self.ALT, self.LARG, self.ALT)
        self.vx = self.vy = 0
        self.no_chao = self.abaixado = False
        self.direcao = 1
        self.soco = self.recarga = 0
        self.invencivel = 90
        self.tempo_anim = 0
        self.arma, self.municao = "poder", None
        self.coyote = self.buffer_pulo = 0   # tolerâncias do pulo (em quadros)
        self.pulou = self.pousou = False     # avisos para som e poeira

    def pegar_arma(self, tipo):
        self.arma, self.municao = tipo, ARMAS[tipo]["municao"]

    def atirar(self):
        """Retorna um Tiro ou None."""
        if self.recarga:
            return None
        self.recarga = ARMAS[self.arma]["recarga"]
        tiro = Tiro(self.arma, self.rect.centerx, self.rect.top + 20, self.direcao)
        if self.municao is not None:
            self.municao -= 1
            if self.municao <= 0:
                self.arma, self.municao = "poder", None
        return tiro

    def pular(self):
        # Só anota o pedido: o pulo acontece em atualizar(). Assim, apertar um
        # pouco antes de pousar ainda vale (o pedido fica guardado por 8 quadros).
        self.buffer_pulo = 8

    def soltar_pulo(self):
        if self.vy < -4:
            self.vy = -4

    def socar(self):
        if self.soco == 0:
            self.soco = 18

    def atualizar(self, teclas, solidos):
        quer = teclas[pygame.K_DOWN] and self.no_chao
        if quer != self.abaixado:
            alt = self.ALT_ABAIXADO if quer else self.ALT
            novo = pygame.Rect(self.rect.x, self.rect.bottom - alt, self.LARG, alt)
            if quer or not any(novo.colliderect(b.rect) for b in solidos):
                self.rect, self.abaixado = novo, quer

        self.vx = 0
        if not self.abaixado:
            if teclas[pygame.K_LEFT]:
                self.vx, self.direcao = -VEL_ANDAR, -1
            if teclas[pygame.K_RIGHT]:
                self.vx, self.direcao = VEL_ANDAR, 1

        # "coyote time": por 6 quadros depois de sair da beirada ainda dá para pular
        self.coyote = 6 if self.no_chao else max(0, self.coyote - 1)
        self.pulou = False
        if self.buffer_pulo:
            self.buffer_pulo -= 1
            if self.coyote and not self.abaixado:
                self.vy = -FORCA_PULO
                self.coyote = self.buffer_pulo = 0
                self.pulou = True

        self.vy = min(self.vy + GRAVIDADE, VEL_MAX_QUEDA)
        estava_no_chao, vel_queda = self.no_chao, self.vy
        self.no_chao, _ = mover_com_colisao(self, solidos)
        self.pousou = self.no_chao and not estava_no_chao and vel_queda > 5
        self.rect.left = max(0, self.rect.left)

        self.soco = max(0, self.soco - 1)
        self.recarga = max(0, self.recarga - 1)
        self.invencivel = max(0, self.invencivel - 1)
        self.tempo_anim += 1

    def caixa_soco(self):
        if self.soco <= 8:
            return None
        w, h = 28, 18
        x = self.rect.right if self.direcao > 0 else self.rect.left - w
        return pygame.Rect(x, self.rect.top + 10, w, h)

    def estado(self):
        if self.soco > 0:
            return "soco"
        if not self.no_chao:
            return "pulo"
        if self.abaixado:
            return "abaixar"
        return "andar" if self.vx else "parado"

    def indice_quadro(self, estado, n):
        """Qual quadro da animação mostrar agora (cada estado tem seu ritmo)."""
        if estado == "pulo" and n >= 5:
            # quadro de acordo com a velocidade vertical: subindo, no topo, descendo
            if self.vy < -4:
                return 2
            if self.vy < 2:
                return 3
            return 4
        if estado == "abaixar":
            return n - 1                                  # fica agachado, sem subir e descer
        if estado == "soco":
            return min(n - 1, (18 - self.soco) * n // 18)  # toca uma vez durante o soco
        if estado == "parado":
            return (self.tempo_anim // 12) % n             # respiração lenta
        return (self.tempo_anim // 6) % n                  # andar

    def desenhar(self, tela, cam_x):
        if self.invencivel and (self.invencivel // 4) % 2:
            return
        estado = self.estado()
        quadros = self.anims.get(estado) or self.anims.get("parado")
        if quadros:
            img = quadros[self.indice_quadro(estado, len(quadros))]
            if self.direcao < 0:
                img = pygame.transform.flip(img, True, False)
            tela.blit(img, img.get_rect(midbottom=(self.rect.centerx - cam_x, self.rect.bottom)))
        else:
            pygame.draw.rect(tela, (40, 60, 140), self.rect.move(-cam_x, 0), border_radius=6)
            olho = (self.rect.centerx - cam_x + 7 * self.direcao, self.rect.top + 12)
            pygame.draw.circle(tela, (255, 255, 255), olho, 4)
            caixa = self.caixa_soco()
            if caixa:
                pygame.draw.rect(tela, (255, 220, 0), caixa.move(-cam_x, 0))


class Tiro:
    """Projétil do jogador. tipo: poder, arma, raio, carteira."""
    def __init__(self, tipo, x, y, direcao):
        self.tipo = tipo
        tam = {"poder": (16, 10), "arma": (10, 4), "raio": (34, 6), "carteira": (14, 18)}[tipo]
        vel = {"poder": 9, "arma": 13, "raio": 15, "carteira": 6}[tipo]
        self.rect = pygame.Rect(0, 0, *tam)
        self.rect.center = (x, y)
        self.vx = vel * direcao
        self.vy = -8 if tipo == "carteira" else 0
        self.vida = 90

    def atualizar(self, solidos):
        self.rect.x += self.vx
        if self.tipo == "carteira":
            self.vy += 0.5
            self.rect.y += round(self.vy)
        self.vida -= 1
        if any(self.rect.colliderect(b.rect) for b in solidos) or self.rect.top > ALTURA:
            self.vida = 0

    def desenhar(self, tela, cam_x):
        r = self.rect.move(-cam_x, 0)
        if self.tipo == "poder":
            pygame.draw.ellipse(tela, (255, 230, 60), r)
        elif self.tipo == "arma":
            pygame.draw.rect(tela, (40, 40, 40), r)
        elif self.tipo == "raio":
            pygame.draw.rect(tela, (60, 220, 230), r, border_radius=3)
            pygame.draw.rect(tela, (255, 255, 255), r.inflate(-10, -4), border_radius=2)
        else:  # carteira de trabalho
            pygame.draw.rect(tela, (30, 70, 160), r, border_radius=2)
            pygame.draw.rect(tela, (230, 200, 80), (r.x + 3, r.y + 4, r.w - 6, 3))


class TiroInimigo:
    """Projétil que machuca o jogador (balão, folheto, palavra, carimbo, onda)."""
    def __init__(self, x, y, vx, vy, texto="", cor=(255, 255, 255), gravidade=0.0, tam=(20, 14)):
        self.rect = pygame.Rect(0, 0, *tam)
        self.rect.center = (x, y)
        self.vx, self.vy, self.g = vx, vy, gravidade
        self.texto, self.cor = texto, cor
        self.vida = 240

    def atualizar(self, solidos):
        self.vy += self.g
        self.rect.x += round(self.vx)
        self.rect.y += round(self.vy)
        self.vida -= 1
        if any(self.rect.colliderect(b.rect) for b in solidos) or self.rect.top > ALTURA:
            self.vida = 0

    def desenhar(self, tela, cam_x, fonte):
        r = self.rect.move(-cam_x, 0)
        pygame.draw.rect(tela, self.cor, r, border_radius=6)
        pygame.draw.rect(tela, (0, 0, 0), r, 2, border_radius=6)
        if self.texto:
            s = fonte.render(self.texto, True, (0, 0, 0))
            tela.blit(s, s.get_rect(center=r.center))


class Explosao:
    def __init__(self, centro, raio=80):
        self.centro, self.raio, self.t = centro, raio, 18

    def desenhar(self, tela, cam_x):
        r = int(self.raio * (1 - self.t / 18) + 10)
        pygame.draw.circle(tela, (255, 200, 60), (self.centro[0] - cam_x, self.centro[1]), r, 4)
        self.t -= 1


class Inimigo:
    """tipos: burocrata (patrulha), sapo de toga (solta frases), panfleteiro (arremessa folhetos), cartazista (solta slogans).
    estado: ativo | cancelado | fumaca | convertido"""
    COR = {"burocrata": (110, 110, 120), "sapo": (60, 160, 70),
           "panfleteiro": (190, 80, 160), "cartazista": (190, 35, 50)}
    LARG, ALT = 34, 44

    def __init__(self, tipo, x, base):
        self.tipo = tipo
        self.rect = pygame.Rect(x, base - self.ALT, self.LARG, self.ALT)
        self.vx = -1.5 if tipo == "burocrata" else 0
        self.vy = 0
        self.estado = "ativo"
        self.timer = random.randint(0, 60)
        self.no_chao = False
        self.pontuado = False  # já rendeu pontos ao jogador?
        self.direcao = -1
        self.anim_tick = 0
        self.attack_anim = 0
        self.attack_warning = 0

    @property
    def perigoso(self):
        return self.estado == "ativo"

    def atingir(self, ataque, jogador_x):
        if self.estado != "ativo":
            return
        if ataque == "arma":
            self.estado, self.timer = "cancelado", 45
        elif ataque == "carteira":
            self.estado, self.timer, self.vx = "fumaca", 28, 0
        elif ataque == "raio":
            self.estado = "convertido"
            self.vx = 3 if self.rect.centerx > jogador_x else -3
            self.direcao = 1 if self.vx > 0 else -1
            self.timer = 240
        else:  # soco, pisão, poder
            self.estado, self.timer = "removido", 0

    def atualizar(self, solidos, jogador, tiros_ini):
        self.anim_tick += 1
        self.attack_anim = max(0, self.attack_anim - 1)
        self.attack_warning = max(0, self.attack_warning - 1)
        self.vy = min(self.vy + GRAVIDADE, VEL_MAX_QUEDA)
        if self.estado in ("cancelado", "convertido", "fumaca"):
            self.timer -= 1
            if self.timer <= 0:
                self.estado = "removido"
            if self.estado in ("cancelado", "fumaca"):
                return
        no_chao, bateu = mover_com_colisao(self, solidos)
        self.no_chao = no_chao
        if self.estado != "ativo":
            return

        self.timer += 1
        dist = jogador.rect.centerx - self.rect.centerx
        self.direcao = 1 if dist > 0 else -1
        if self.tipo == "burocrata":
            if self.timer % 120 == 96 and abs(dist) < 90:
                self.attack_warning = 24
            if self.timer % 120 == 0 and abs(dist) < 90:
                self.attack_anim, self.attack_warning = 18, 0
            if bateu:
                self.vx *= -1
            elif no_chao:
                fx = self.rect.right + 2 if self.vx > 0 else self.rect.left - 3
                if not any(b.rect.collidepoint(fx, self.rect.bottom + 2) for b in solidos):
                    self.vx *= -1
        elif self.tipo == "sapo":
            if no_chao:
                self.vx = 0
                if self.timer % 100 == 0 and abs(dist) < 500:
                    self.vy, self.vx = -9, (2 if dist > 0 else -2)
                if self.timer % 150 == 60 and abs(dist) < 450:
                    self.attack_warning = 15
                if self.timer % 150 == 75 and abs(dist) < 450:
                    d = 1 if dist > 0 else -1
                    frase = random.choice(("INDEFERIDO!", "DATA VENIA!",
                                           "TÁ NOS AUTOS!", "DECISÃO MANTIDA!"))
                    tiros_ini.append(TiroInimigo(self.rect.centerx, self.rect.top + 14, 4 * d, 0,
                                                 frase, (245, 245, 255), tam=(150, 24)))
                    self.attack_anim, self.attack_warning = 18, 0
        elif self.tipo == "panfleteiro":
            if self.timer % 120 == 96 and abs(dist) < 480:
                self.attack_warning = 24
            if self.timer % 120 == 0 and abs(dist) < 480:
                d = 1 if dist > 0 else -1
                tiros_ini.append(TiroInimigo(self.rect.centerx, self.rect.top, 4.5 * d, -7,
                                             "", (255, 250, 200), gravidade=0.35, tam=(16, 12)))
                self.attack_anim, self.attack_warning = 18, 0
        elif self.tipo == "cartazista":
            if self.timer % 135 == 110 and abs(dist) < 480:
                self.attack_warning = 25
            if self.timer % 135 == 0 and abs(dist) < 480:
                d = 1 if dist > 0 else -1
                tiros_ini.append(TiroInimigo(self.rect.centerx, self.rect.top + 14,
                                             4 * d, -0.4, "RECÚA!", (255, 170, 175),
                                             tam=(78, 26)))
                self.attack_anim, self.attack_warning = 18, 0

    def desenhar(self, tela, cam_x, fonte):
        r = self.rect.move(-cam_x, 0)
        if self.estado == "fumaca":
            progresso = 1 - max(0, self.timer) / 28
            nuvem = pygame.Surface((76, 64), pygame.SRCALPHA)
            alpha = max(0, int(175 * (1 - progresso)))
            centro_y = 49 - round(progresso * 24)
            for dx, dy, raio in ((20, 42, 13), (34, 30, 16), (49, 40, 14),
                                 (29, 19, 11), (48, 17, 10)):
                atual = max(3, round(raio * (0.65 + progresso * 0.8)))
                pygame.draw.circle(nuvem, (205, 210, 220, alpha),
                                   (dx, centro_y + dy - 38), atual)
            tela.blit(nuvem, (r.centerx - 38, r.bottom - 55))
            return

        skin = "patriota" if self.estado == "convertido" else self.tipo
        imagem = SKINS_VISUAIS.get(f"{skin}_esquerda") if self.direcao < 0 else None
        imagem = imagem or SKINS_VISUAIS.get(skin)
        if imagem:
            andando = abs(self.vx) > 0.3 or not self.no_chao
            bob = round(abs(math.sin(self.anim_tick * 0.28)) * 2) if andando else round(
                math.sin(self.anim_tick * 0.12))
            pose = imagem
            if self.attack_anim:
                w, h = imagem.get_size()
                pose = pygame.transform.scale(imagem, (round(w * 1.08), round(h * 0.94)))
            elif andando:
                angulo = math.sin(self.anim_tick * 0.32) * 3.5
                pose = pygame.transform.rotate(imagem, angulo)
            destino = pose.get_rect(midbottom=(r.centerx + (self.direcao * 2 if self.attack_anim else 0),
                                               self.rect.bottom - bob))
            tela.blit(pose, destino)
            if self.attack_warning:
                pulso = 13 + (self.attack_warning % 4)
                pygame.draw.circle(tela, (255, 220, 55), (destino.centerx, destino.top + 13), pulso, 2)
                alerta = fonte.render("!", True, (255, 80, 40))
                tela.blit(alerta, alerta.get_rect(midbottom=(destino.centerx, destino.top + 12)))
            if self.estado == "convertido":
                centro_x = destino.left + round(destino.width * 0.72)
                for texto, pos_y in (("ANISTIA", 0.15), ("JÁ!", 0.27)):
                    letras = fonte.render(texto, True, (20, 75, 28))
                    max_w, max_h = round(destino.width * 0.50), round(destino.height * 0.10)
                    fator = min(max_w / letras.get_width(), max_h / letras.get_height())
                    letras = pygame.transform.scale(letras, (max(1, round(letras.get_width() * fator)),
                                                              max(1, round(letras.get_height() * fator))))
                    tela.blit(letras, letras.get_rect(center=(centro_x,
                                                              destino.top + round(destino.height * pos_y))))
            elif self.tipo == "cartazista":
                # Escreve sobre a placa em branco do sprite para manter o slogan legível.
                for texto, pos_y in (("RECÚA", 0.15), ("FASCISTA!", 0.27)):
                    letras = fonte.render(texto, True, (140, 18, 28))
                    max_w, max_h = round(destino.width * 0.52), round(destino.height * 0.10)
                    fator = min(max_w / letras.get_width(), max_h / letras.get_height())
                    letras = pygame.transform.scale(letras, (max(1, round(letras.get_width() * fator)),
                                                              max(1, round(letras.get_height() * fator))))
                    tela.blit(letras, letras.get_rect(center=(destino.centerx,
                                                              destino.top + round(destino.height * pos_y))))
            if self.estado == "cancelado":
                carimbo = pygame.transform.rotate(fonte.render("CANCELADO", True, (220, 0, 0)), 12)
                tela.blit(carimbo, carimbo.get_rect(center=r.center))
            elif self.estado == "passivo":
                tela.blit(fonte.render("zzz", True, (40, 40, 80)), (destino.right - 6, destino.top - 8))
            return

        cor = {"passivo": (150, 180, 220), "convertido": (240, 200, 60)}.get(self.estado,
                                                                           self.COR[self.tipo])
        # Sapato/sombra comum dá uma base visual consistente aos personagens.
        pygame.draw.ellipse(tela, (35, 35, 40), (r.x + 3, r.bottom - 5, r.w - 6, 7))
        if self.tipo == "sapo":
            toga = (32, 32, 38) if self.estado == "ativo" else cor
            # Capa, manto, gola e filete dourado do sapo de toga.
            pygame.draw.polygon(tela, (18, 18, 24), [
                (r.centerx - 10, r.y + 15), (r.centerx + 10, r.y + 15),
                (r.right + 2, r.bottom - 2), (r.left - 2, r.bottom - 2)])
            pygame.draw.polygon(tela, toga, [
                (r.centerx - 9, r.y + 15), (r.centerx + 9, r.y + 15),
                (r.centerx + 15, r.bottom - 2), (r.centerx - 15, r.bottom - 2)])
            pygame.draw.line(tela, (190, 155, 65), (r.left + 4, r.bottom - 7),
                             (r.right - 4, r.bottom - 7), 2)
            # Cabeça de sapo, olhos salientes e gola branca.
            pygame.draw.ellipse(tela, cor, (r.centerx - 14, r.y + 2, 28, 21))
            for dx in (-8, 8):
                pygame.draw.circle(tela, cor, (r.centerx + dx, r.y + 5), 6)
                pygame.draw.circle(tela, (250, 245, 225), (r.centerx + dx, r.y + 5), 3)
                pygame.draw.circle(tela, (20, 20, 20), (r.centerx + dx, r.y + 5), 1)
            pygame.draw.polygon(tela, (235, 235, 225), [
                (r.centerx - 7, r.y + 16), (r.centerx + 7, r.y + 16),
                (r.centerx, r.y + 28)])
            pygame.draw.line(tela, (180, 180, 175), (r.centerx, r.y + 27),
                             (r.centerx, r.bottom - 5), 2)
            pygame.draw.line(tela, (25, 25, 30), (r.centerx - 5, r.y + 14),
                             (r.centerx + 5, r.y + 14), 2)
        elif self.tipo == "burocrata":
            # Terno azul-marinho, camisa, gravata e pasta de documentos.
            pygame.draw.rect(tela, (26, 43, 72), (r.x + 4, r.y + 18, r.w - 8, 22), border_radius=4)
            pygame.draw.rect(tela, (235, 232, 218), (r.centerx - 5, r.y + 18, 10, 15))
            pygame.draw.polygon(tela, (180, 40, 48), [(r.centerx - 2, r.y + 20),
                             (r.centerx + 2, r.y + 20), (r.centerx + 4, r.y + 33),
                             (r.centerx, r.y + 37), (r.centerx - 4, r.y + 33)])
            pygame.draw.line(tela, (17, 25, 40), (r.x + 10, r.bottom - 7),
                             (r.x + 10, r.bottom - 1), 4)
            pygame.draw.line(tela, (17, 25, 40), (r.right - 10, r.bottom - 7),
                             (r.right - 10, r.bottom - 1), 4)
            pygame.draw.ellipse(tela, (225, 174, 132), (r.centerx - 9, r.y + 2, 18, 18))
            pygame.draw.arc(tela, (55, 37, 28), (r.centerx - 10, r.y, 20, 15), 0, math.pi, 4)
            pygame.draw.rect(tela, (125, 76, 40), (r.x - 4, r.y + 25, 9, 12), border_radius=2)
            pygame.draw.line(tela, (220, 185, 110), (r.x - 2, r.y + 28),
                             (r.x + 3, r.y + 28), 1)
        elif self.tipo == "panfleteiro":
            # Jaqueta violeta, boné, bolsa de folhetos e pilha de panfletos.
            pygame.draw.rect(tela, cor, (r.x + 4, r.y + 18, r.w - 8, 22), border_radius=5)
            pygame.draw.line(tela, (245, 220, 245), (r.centerx, r.y + 20),
                             (r.centerx, r.y + 38), 2)
            pygame.draw.ellipse(tela, (225, 172, 130), (r.centerx - 9, r.y + 3, 18, 17))
            pygame.draw.arc(tela, (45, 35, 48), (r.centerx - 10, r.y, 20, 14), 0, math.pi, 4)
            pygame.draw.rect(tela, (75, 45, 95), (r.centerx - 12, r.y + 2, 24, 5), border_radius=2)
            pygame.draw.rect(tela, (95, 57, 42), (r.right - 3, r.y + 22, 9, 15), border_radius=2)
            pygame.draw.rect(tela, (255, 250, 220), (r.right - 1, r.y + 18, 11, 7))
            pygame.draw.line(tela, (40, 35, 45), (r.x + 10, r.bottom - 7),
                             (r.x + 10, r.bottom - 1), 4)
            pygame.draw.line(tela, (40, 35, 45), (r.right - 10, r.bottom - 7),
                             (r.right - 10, r.bottom - 1), 4)
        elif self.tipo == "cartazista":
            # Camiseta vermelha, braços erguidos, tênis e placa de protesto.
            pygame.draw.rect(tela, cor, (r.x + 5, r.y + 17, r.w - 10, r.h - 20), border_radius=5)
            pygame.draw.line(tela, (225, 175, 135), (r.x + 7, r.y + 20),
                             (r.x + 1, r.y + 12), 4)
            pygame.draw.line(tela, (225, 175, 135), (r.right - 7, r.y + 20),
                             (r.right - 1, r.y + 12), 4)
            pygame.draw.line(tela, (35, 35, 40), (r.x + 11, r.bottom - 7),
                             (r.x + 9, r.bottom - 1), 4)
            pygame.draw.line(tela, (35, 35, 40), (r.right - 11, r.bottom - 7),
                             (r.right - 9, r.bottom - 1), 4)
            pygame.draw.circle(tela, (220, 170, 130), (r.centerx, r.y + 10), 9)
            pygame.draw.arc(tela, (45, 30, 25), (r.centerx - 10, r.y, 20, 17), 0, math.pi, 4)
            placa = pygame.Rect(r.centerx - 55, r.y - 39, 110, 38)
            pygame.draw.rect(tela, (245, 240, 220), placa, border_radius=3)
            pygame.draw.rect(tela, (80, 50, 35), placa, 2, border_radius=3)
            linha1 = fonte.render("RECÚA", True, (150, 20, 30))
            linha2 = fonte.render("FASCISTA!", True, (150, 20, 30))
            tela.blit(linha1, linha1.get_rect(center=(placa.centerx, placa.y + 10)))
            tela.blit(linha2, linha2.get_rect(center=(placa.centerx, placa.y + 28)))
        if self.estado == "cancelado":
            s = fonte.render("CANCELADO", True, (220, 0, 0))
            s = pygame.transform.rotate(s, 12)
            tela.blit(s, s.get_rect(center=r.center))
        elif self.estado == "passivo":
            tela.blit(fonte.render("zzz", True, (40, 40, 80)), (r.right - 4, r.top - 14))


class Chefe:
    LARG, ALT = 80, 104

    def __init__(self, tipo, x, base):
        self.tipo = tipo
        dados = CHEFES[tipo]
        self.nome, self.cor, self.falas = dados["nome"], dados["cor"], dados["falas"]
        self.vida = self.vida_max = dados["vida"]
        self.rect = pygame.Rect(x, base - self.ALT, self.LARG, self.ALT)
        self.origem = (x, base)
        self.vx, self.vy = 0, 0
        self.acordado = False
        self.timer = 0
        self.piscar = 0
        self.fala, self.tempo_fala = "", 0
        self.no_chao = True
        self.direcao = -1
        self.anim_tick = 0
        self.attack_anim = 0
        self.telegraph = 0
        self.telegraph_type = None
        self.telegraph_targets = []
        self.telegraph_dir = -1

    def atingir(self, ataque):
        if self.piscar or self.vida <= 0:
            return
        self.vida -= DANO_CHEFE.get(ataque, 1)
        self.piscar = 20

    def falar(self):
        self.fala, self.tempo_fala = random.choice(self.falas), 110

    def atualizar(self, solidos, jogador, tiros_ini):
        dist = jogador.rect.centerx - self.rect.centerx
        if not self.acordado:
            if abs(dist) < 520:
                self.acordado = True
                self.falar()
            return
        self.timer += 1
        self.anim_tick += 1
        self.attack_anim = max(0, self.attack_anim - 1)
        self.piscar = max(0, self.piscar - 1)
        self.tempo_fala = max(0, self.tempo_fala - 1)
        if self.timer % 200 == 0:
            self.falar()
        d = 1 if dist > 0 else -1
        self.direcao = d
        estava_no_ar = not self.no_chao
        self.vy = min(self.vy + GRAVIDADE, VEL_MAX_QUEDA)

        # A contagem regressiva mostra o perigo antes de cada ataque.
        if self.telegraph > 0:
            self.telegraph -= 1
            if self.telegraph == 0:
                self.attack_anim = 28
                if self.telegraph_type == "chuva":
                    for x in self.telegraph_targets:
                        tiros_ini.append(TiroInimigo(x, -20, 0, 2, "BLÁ!", (255, 230, 120),
                                                     gravidade=0.15, tam=(48, 24)))
                elif self.telegraph_type == "linha":
                    tiros_ini.append(TiroInimigo(self.rect.centerx, self.rect.centery,
                                                 6 * self.telegraph_dir, 0, "TAXA!",
                                                 (255, 210, 120), tam=(62, 24)))
                elif self.telegraph_type == "martelo":
                    self.vy, self.vx = -14, 2.5 * self.telegraph_dir
                self.telegraph_type = None

        if self.tipo == "megafone":
            self.vx = 1.2 * d if abs(dist) > 150 else 0
            if self.timer % 120 == 80 and self.telegraph == 0:
                self.telegraph = 40
                self.telegraph_type = "chuva"
                self.telegraph_targets = [jogador.rect.centerx - 72,
                                          jogador.rect.centerx + 72]
        elif self.tipo == "fiscal":
            if self.no_chao:
                self.vx = 0
            if self.timer % 120 == 82 and self.telegraph == 0:
                self.telegraph = 30
                self.telegraph_type = "linha"
                self.telegraph_dir = d
            if self.timer % 150 == 0 and self.no_chao:
                self.vy, self.vx = -12, 3 * d
                self.attack_anim = 20
        elif self.tipo == "juiz":
            if self.no_chao and self.telegraph_type != "martelo" and self.attack_anim == 0:
                self.vx = 0.8 * d
            if self.timer % 150 == 100 and self.no_chao and self.telegraph == 0:
                self.telegraph = 36
                self.telegraph_type = "martelo"
                self.telegraph_dir = d

        self.no_chao, _ = mover_com_colisao(self, solidos)
        if self.rect.top > ALTURA:  # caiu num buraco: volta ao ponto de origem (evita travar a fase)
            x, base = self.origem
            self.rect.update(x, base - self.ALT, self.LARG, self.ALT)
            self.vx = self.vy = 0
            self.falar()
            return
        if self.tipo == "juiz" and estava_no_ar and self.no_chao:  # pancada do martelo
            self.attack_anim = 24
            for v in (-6, 6):
                tiros_ini.append(TiroInimigo(self.rect.centerx, self.rect.bottom - 10, v, 0,
                                             "", (200, 200, 210), tam=(30, 18)))

    def desenhar(self, tela, cam_x, fonte):
        r = self.rect.move(-cam_x, 0)
        imagem = (SKINS_VISUAIS.get(f"{self.tipo}_esquerda") if self.direcao < 0 else None)
        imagem = imagem or SKINS_VISUAIS.get(self.tipo)
        if imagem:
            andando = abs(self.vx) > 0.35 or not self.no_chao
            pose = imagem
            deslocamento_y = round(abs(math.sin(self.anim_tick * 0.22)) * 2) if andando else 0
            if self.telegraph:
                w, h = imagem.get_size()
                pose = pygame.transform.scale(imagem, (round(w * 1.04), round(h * 0.96)))
            elif self.attack_anim:
                w, h = imagem.get_size()
                pose = pygame.transform.scale(imagem, (round(w * 1.12), round(h * 0.90)))
            elif andando:
                pose = pygame.transform.rotate(imagem, math.sin(self.anim_tick * 0.24) * 2.5)
            destino = pose.get_rect(midbottom=(r.centerx + (self.direcao * 3 if self.attack_anim else 0),
                                               self.rect.bottom - deslocamento_y))

            if self.telegraph and self.telegraph_type == "chuva":
                for x in self.telegraph_targets:
                    sx = x - cam_x
                    if -28 <= sx <= LARGURA + 28:
                        faixa = pygame.Surface((26, max(1, Y_CHAO - 100)), pygame.SRCALPHA)
                        faixa.fill((255, 70, 40, 32))
                        tela.blit(faixa, (sx - 13, 100))
                        for yy in range(110, Y_CHAO - 16, 20):
                            pygame.draw.line(tela, (250, 110, 55), (sx, yy), (sx, yy + 8), 2)
                        pygame.draw.circle(tela, (255, 80, 45), (sx, Y_CHAO - 8),
                                           16 + (self.telegraph % 5), 3)
                        marca = fonte.render("BLÁ!", True, (160, 30, 20))
                        tela.blit(marca, marca.get_rect(midbottom=(sx, Y_CHAO - 25)))
            elif self.telegraph and self.telegraph_type == "linha":
                y = destino.centery
                inicio = destino.centerx
                fim = LARGURA if self.telegraph_dir > 0 else 0
                esquerda, largura = min(inicio, fim), abs(fim - inicio)
                faixa = pygame.Surface((max(1, largura), 10), pygame.SRCALPHA)
                faixa.fill((255, 190, 40, 85))
                tela.blit(faixa, (esquerda, y - 5))
                for xx in range(esquerda, esquerda + largura, 28):
                    pygame.draw.line(tela, (245, 75, 35), (xx, y - 8), (xx + 12, y + 8), 3)
                aviso = fonte.render("TAXA!", True, (175, 45, 20))
                tela.blit(aviso, aviso.get_rect(midbottom=(fim - self.telegraph_dir * 8, y - 12)))
            elif self.telegraph and self.telegraph_type == "martelo":
                y = Y_CHAO - 8
                x = destino.centerx
                pygame.draw.line(tela, (245, 80, 45), (x - 76, y), (x + 76, y), 4)
                for dx in (-60, -30, 0, 30, 60):
                    pygame.draw.circle(tela, (255, 205, 60), (x + dx, y),
                                       7 + (self.telegraph % 4), 2)
                aviso = fonte.render("MARTELADA!", True, (165, 35, 25))
                tela.blit(aviso, aviso.get_rect(midbottom=(x, y - 15)))

            tela.blit(pose, destino)
            if self.telegraph:
                alerta = fonte.render("!", True, (255, 75, 35))
                tela.blit(alerta, alerta.get_rect(midbottom=(destino.centerx, destino.top + 15)))
            if self.piscar % 4 >= 2:
                brilho = pygame.Surface(destino.size, pygame.SRCALPHA)
                brilho.fill((255, 255, 255, 105))
                tela.blit(brilho, destino)
            if self.tempo_fala:
                balao(tela, fonte, self.fala, r.centerx, destino.top)
            return

        cor = (255, 255, 255) if self.piscar % 4 >= 2 else self.cor
        pele = (230, 180, 138)
        pygame.draw.ellipse(tela, (35, 35, 40), (r.x + 8, r.bottom - 9, r.w - 16, 12))
        # Pernas e botas deixam a silhueta do chefe mais clara durante a luta.
        calca = (55, 55, 65) if self.tipo != "megafone" else (82, 45, 39)
        pygame.draw.rect(tela, calca, (r.x + 18, r.y + 78, 18, 19), border_radius=4)
        pygame.draw.rect(tela, calca, (r.x + 45, r.y + 78, 18, 19), border_radius=4)
        pygame.draw.rect(tela, (30, 28, 30), (r.x + 14, r.bottom - 10, 27, 11), border_radius=4)
        pygame.draw.rect(tela, (30, 28, 30), (r.x + 40, r.bottom - 10, 27, 11), border_radius=4)

        if self.tipo == "megafone":
            # Terno terracota, camisa clara, gravata e megafone dourado.
            pygame.draw.rect(tela, cor, (r.x + 10, r.y + 38, r.w - 20, 48), border_radius=10)
            pygame.draw.polygon(tela, (245, 238, 215), [(r.centerx - 12, r.y + 39),
                             (r.centerx + 12, r.y + 39), (r.centerx, r.y + 63)])
            pygame.draw.polygon(tela, (170, 35, 42), [(r.centerx - 3, r.y + 48),
                             (r.centerx + 3, r.y + 48), (r.centerx + 6, r.y + 70),
                             (r.centerx, r.y + 76), (r.centerx - 6, r.y + 70)])
            pygame.draw.ellipse(tela, pele, (r.centerx - 19, r.y + 7, 38, 36))
            pygame.draw.arc(tela, (50, 32, 26), (r.centerx - 20, r.y + 2, 40, 22), 0, math.pi, 7)
            pygame.draw.line(tela, (60, 30, 25), (r.centerx - 8, r.y + 27),
                             (r.centerx + 8, r.y + 27), 3)
            pygame.draw.polygon(tela, (230, 175, 50), [
                (r.right - 7, r.y + 48), (r.right + 25, r.y + 37),
                (r.right + 25, r.y + 73), (r.right - 7, r.y + 62)])
            pygame.draw.ellipse(tela, (250, 220, 125), (r.right + 17, r.y + 39, 13, 32), 3)
            pygame.draw.line(tela, pele, (r.right - 4, r.y + 61),
                             (r.right + 13, r.y + 58), 7)
        elif self.tipo == "fiscal":
            # Uniforme verde-oliva, colete amarelo refletivo, quepe e prancheta.
            pygame.draw.rect(tela, (63, 83, 61), (r.x + 10, r.y + 38, r.w - 20, 48), border_radius=9)
            pygame.draw.rect(tela, cor, (r.x + 16, r.y + 42, r.w - 32, 40), border_radius=4)
            pygame.draw.line(tela, (245, 235, 170), (r.x + 17, r.y + 56),
                             (r.right - 17, r.y + 56), 5)
            pygame.draw.line(tela, (245, 235, 170), (r.x + 17, r.y + 71),
                             (r.right - 17, r.y + 71), 4)
            pygame.draw.ellipse(tela, pele, (r.centerx - 18, r.y + 8, 36, 34))
            pygame.draw.rect(tela, (35, 42, 35), (r.x + 18, r.y + 5, r.w - 36, 10), border_radius=3)
            pygame.draw.rect(tela, (35, 42, 35), (r.x + 10, r.y + 13, r.w - 20, 6), border_radius=3)
            pygame.draw.circle(tela, (235, 195, 65), (r.centerx + 15, r.y + 52), 7)
            pygame.draw.circle(tela, (255, 240, 150), (r.centerx + 15, r.y + 52), 3)
            pygame.draw.rect(tela, (130, 83, 45), (r.x - 12, r.y + 47, 22, 34), border_radius=3)
            pygame.draw.rect(tela, (245, 235, 205), (r.x - 9, r.y + 52, 16, 23))
            pygame.draw.line(tela, (90, 70, 50), (r.x - 6, r.y + 58),
                             (r.x + 4, r.y + 58), 2)
        else:  # juiz da toga
            # Toga preta, jabô branco, peruca grisalha e martelo de juiz.
            pygame.draw.polygon(tela, cor, [(r.x + 20, r.y + 37), (r.right - 20, r.y + 37),
                             (r.right - 7, r.bottom - 10), (r.x + 7, r.bottom - 10)])
            pygame.draw.polygon(tela, (235, 232, 220), [(r.centerx - 11, r.y + 38),
                             (r.centerx + 11, r.y + 38), (r.centerx + 6, r.y + 72),
                             (r.centerx, r.y + 78), (r.centerx - 6, r.y + 72)])
            for dx, dy, raio in ((-15, 19, 11), (-7, 11, 10), (5, 11, 10),
                                 (15, 19, 11), (-17, 30, 7), (17, 30, 7)):
                pygame.draw.circle(tela, (190, 190, 195), (r.centerx + dx, r.y + dy), raio)
                pygame.draw.circle(tela, (225, 225, 225), (r.centerx + dx - 2, r.y + dy - 2), 3)
            pygame.draw.ellipse(tela, pele, (r.centerx - 18, r.y + 17, 36, 29))
            pygame.draw.line(tela, (35, 30, 28), (r.centerx - 10, r.y + 32),
                             (r.centerx - 3, r.y + 32), 3)
            pygame.draw.line(tela, (35, 30, 28), (r.centerx + 3, r.y + 32),
                             (r.centerx + 10, r.y + 32), 3)
            pygame.draw.line(tela, (90, 55, 35), (r.right - 8, r.y + 53),
                             (r.right + 13, r.y + 37), 6)
            pygame.draw.rect(tela, (135, 88, 48), (r.right + 5, r.y + 30, 23, 12), border_radius=3)
            pygame.draw.line(tela, (205, 160, 95), (r.right + 8, r.y + 33),
                             (r.right + 25, r.y + 33), 2)

        # Olhos, cinto e pequenos detalhes acompanham o piscar de dano.
        pygame.draw.circle(tela, (255, 255, 255), (r.centerx - 8, r.y + 25), 5)
        pygame.draw.circle(tela, (255, 255, 255), (r.centerx + 8, r.y + 25), 5)
        pygame.draw.circle(tela, (35, 28, 27), (r.centerx - 8, r.y + 25), 2)
        pygame.draw.circle(tela, (35, 28, 27), (r.centerx + 8, r.y + 25), 2)
        if self.tempo_fala:
            balao(tela, fonte, self.fala, r.centerx, r.top)


# ---------------- FASE ----------------
TIPO_INIMIGO = {"E": "burocrata", "S": "sapo", "F": "panfleteiro", "M": "cartazista"}
TIPO_ITEM = {"g": "arma", "c": "carteira", "r": "raio"}


def carregar_fase(indice, jogador):
    fase = FASES[indice]
    nivel = {"fase": fase, "blocos": [], "inimigos": [], "itens": [], "van": None,
             "chefe": None, "tiros": [], "tiros_ini": [], "explosoes": [], "aviso": 120,
             "checkpoints": []}
    for lin, linha in enumerate(fase["mapa"]):
        for col, c in enumerate(linha):
            x, y = col * TILE, lin * TILE
            if c in "#B":
                nivel["blocos"].append(Bloco(x, y, c))
            elif c == "P":
                jogador.inicio = (x + 9, y + TILE)
            elif c in TIPO_INIMIGO:
                nivel["inimigos"].append(Inimigo(TIPO_INIMIGO[c], x + 7, y + TILE))
            elif c in TIPO_ITEM:
                nivel["itens"].append(Item(x, y, TIPO_ITEM[c]))
            elif c == "K":
                nivel["chefe"] = Chefe(fase["chefe"], x, y + TILE)
            elif c == "V":
                nivel["van"] = pygame.Rect(x, y + TILE - 64, 110, 64)
            elif c == "!":
                nivel["checkpoints"].append({"rect": pygame.Rect(x + 18, y - 24, 12, 72),
                                             "ativo": False})
    jogador.reiniciar()
    nivel["largura"] = max(len(l) for l in fase["mapa"]) * TILE
    rnd = random.Random(indice)
    nivel["predios"] = [(i * 70, rnd.randint(120, 300), rnd.randint(50, 80))
                        for i in range(nivel["largura"] // 140 + LARGURA // 70 + 2)]
    return nivel


def desenhar_van(tela, van, cam_x, trancada, fonte):
    r = van.move(-cam_x, 0)
    pygame.draw.rect(tela, (240, 240, 240), r, border_radius=10)
    for wx in (r.x + 10, r.x + 50):
        pygame.draw.rect(tela, (120, 180, 220), (wx, r.y + 10, 30, 20))
    pygame.draw.rect(tela, (120, 180, 220), (r.right - 22, r.y + 10, 16, 24))
    for wx in (r.x + 22, r.right - 22):
        pygame.draw.circle(tela, (30, 30, 30), (wx, r.bottom), 11)
    if trancada:
        s = fonte.render("TRANCADA", True, (200, 0, 0))
        tela.blit(s, s.get_rect(midbottom=(r.centerx, r.top - 4)))


def desenhar_checkpoints(tela, nivel, cam_x):
    for cp in nivel["checkpoints"]:
        r = cp["rect"].move(-cam_x, 0)
        pygame.draw.rect(tela, (80, 80, 80), (r.x, r.y, 4, r.h))  # mastro
        cor = (60, 200, 80) if cp["ativo"] else (200, 60, 60)
        pygame.draw.polygon(tela, cor, [(r.x + 4, r.y), (r.x + 30, r.y + 10), (r.x + 4, r.y + 20)])


# ---------------- CENÁRIO: CALÇADÃO DE COPACABANA ----------------
Y_CHAO = 9 * TILE        # topo da linha de chão dos mapas
Y_HORIZONTE = 250        # onde o céu encontra o mar
Y_AREIA = 360            # onde o mar encontra a areia
_cache_copa = {}


def _superficies_copacabana():
    """Cria (uma vez só) o céu em degradê e o ladrilho do calçadão."""
    if _cache_copa:
        return _cache_copa
    ceu = pygame.Surface((LARGURA, Y_HORIZONTE))
    for y in range(Y_HORIZONTE):
        t = y / Y_HORIZONTE
        ceu.fill((int(70 + 110 * t), int(150 + 70 * t), int(230 + 15 * t)), (0, y, LARGURA, 1))
    _cache_copa["ceu"] = ceu

    # calçadão: faixas onduladas pretas sobre pedra branca.
    # O período da onda é igual a TILE, então os ladrilhos emendam sem costura.
    piso = pygame.Surface((TILE, TILE))
    piso.fill((245, 242, 232))
    for faixa in range(-1, 3):
        base = faixa * TILE / 2 + TILE / 4
        cima = [(x, base + math.sin(2 * math.pi * x / TILE) * TILE / 6) for x in range(TILE + 1)]
        baixo = [(x, y + TILE / 4) for x, y in reversed(cima)]
        pygame.draw.polygon(piso, (30, 30, 30), cima + baixo)
    pygame.draw.line(piso, (200, 195, 180), (0, 0), (TILE, 0), 3)  # meio-fio
    _cache_copa["piso"] = piso

    terra = pygame.Surface((TILE, TILE))
    terra.fill((120, 95, 70))
    for x, y in ((8, 10), (30, 20), (18, 36), (40, 40)):
        pygame.draw.circle(terra, (100, 78, 58), (x, y), 3)
    _cache_copa["terra"] = terra
    return _cache_copa


def _repetir(cam_x, fator, espaco):
    """Posições na tela de objetos que se repetem a cada `espaco` px com parallax `fator`."""
    desloc = (cam_x * fator) % espaco
    x = -desloc - espaco
    while x < LARGURA + espaco:
        yield x
        x += espaco


def desenhar_morros(tela, cam_x):
    """Silhueta de morros no horizonte (bem ao fundo, quase parada)."""
    for x in _repetir(cam_x, 0.08, 900):
        cor = (70, 110, 95)
        pygame.draw.ellipse(tela, cor, (x + 40, Y_HORIZONTE - 60, 320, 140))
        pygame.draw.ellipse(tela, cor, (x + 300, Y_HORIZONTE - 150, 110, 230))   # morro alto e redondo
        pygame.draw.ellipse(tela, cor, (x + 230, Y_HORIZONTE - 80, 120, 140))
        # morro alto e pontudo com o Cristo Redentor no topo
        topo = (x + 690, Y_HORIZONTE - 175)
        pygame.draw.polygon(tela, (60, 100, 85), [(x + 560, Y_HORIZONTE + 2), (x + 650, topo[1] + 30),
                                                  (topo[0] - 14, topo[1] + 4), (topo[0] + 14, topo[1] + 4),
                                                  (x + 740, topo[1] + 40), (x + 830, Y_HORIZONTE + 2)])
        desenhar_cristo(tela, topo)
        pygame.draw.ellipse(tela, (85, 125, 105), (x + 520, Y_HORIZONTE - 60, 420, 120))


def desenhar_cristo(tela, base):
    """Estátua de braços abertos; base = ponto do pé, no alto do morro."""
    bx, by = base
    cor, sombra = (238, 236, 225), (200, 198, 188)
    pygame.draw.rect(tela, sombra, (bx - 6, by - 6, 12, 10))                         # pedestal
    pygame.draw.polygon(tela, cor, [(bx - 6, by - 6), (bx + 6, by - 6),
                                    (bx + 3, by - 34), (bx - 3, by - 34)])           # túnica
    pygame.draw.rect(tela, cor, (bx - 22, by - 34, 44, 5))                           # braços abertos
    pygame.draw.circle(tela, cor, (bx, by - 38), 4)                                  # cabeça
    pygame.draw.line(tela, sombra, (bx, by - 30), (bx, by - 8), 1)                   # dobra da túnica


def desenhar_mar(tela, cam_x, t):
    pygame.draw.rect(tela, (30, 110, 170), (0, Y_HORIZONTE, LARGURA, Y_AREIA - Y_HORIZONTE))
    pygame.draw.rect(tela, (40, 140, 190), (0, Y_HORIZONTE + 40, LARGURA, Y_AREIA - Y_HORIZONTE - 40))
    for i, y in enumerate(range(Y_HORIZONTE + 14, Y_AREIA - 10, 22)):  # cristas das ondas
        fator = 0.15 + 0.05 * i
        for x in _repetir(cam_x, fator, 120):
            dx = x + math.sin(t / 700 + i) * 20
            pygame.draw.arc(tela, (220, 240, 250), (dx, y, 40, 12), 0, math.pi, 2)
    # espuma na beira da praia, indo e vindo
    vai_vem = math.sin(t / 900) * 6
    pygame.draw.rect(tela, (235, 245, 250), (0, Y_AREIA - 6 + vai_vem, LARGURA, 8))


def desenhar_guarda_sol(tela, x, y, cor):
    pygame.draw.line(tela, (90, 70, 50), (x, y), (x, y - 46), 3)
    pygame.draw.polygon(tela, cor, [(x - 32, y - 40), (x, y - 58), (x + 32, y - 40)])
    pygame.draw.line(tela, (255, 255, 255), (x - 16, y - 49), (x + 16, y - 49), 2)


def desenhar_coqueiro(tela, x, y):
    tronco = [(x + i * 3 + math.sin(i / 2) * 2, y - i * 10) for i in range(10)]
    pygame.draw.lines(tela, (130, 90, 50), False, tronco, 7)
    topo = tronco[-1]
    for ang in (-150, -110, -60, -20, 200):
        a = math.radians(ang)
        ponta = (topo[0] + math.cos(a) * 46, topo[1] + math.sin(a) * 22 + 14)
        meio = (topo[0] + math.cos(a) * 24, topo[1] + math.sin(a) * 22 - 4)
        pygame.draw.lines(tela, (40, 140, 60), False, [topo, meio, ponta], 6)
    for dx in (-5, 5):
        pygame.draw.circle(tela, (100, 70, 30), (int(topo[0] + dx), int(topo[1] + 6)), 5)


def desenhar_quiosque(tela, x, y):
    pygame.draw.rect(tela, (250, 250, 245), (x, y - 50, 70, 50))
    pygame.draw.rect(tela, (40, 160, 90), (x - 8, y - 66, 86, 16), border_radius=4)
    pygame.draw.rect(tela, (230, 200, 60), (x + 10, y - 36, 50, 18))


def desenhar_areia(tela, cam_x):
    pygame.draw.rect(tela, (238, 214, 160), (0, Y_AREIA, LARGURA, Y_CHAO - Y_AREIA))
    cores = [(230, 60, 60), (250, 200, 40), (40, 120, 220), (240, 120, 30)]
    for n, x in enumerate(_repetir(cam_x, 0.5, 260)):
        idx = int((cam_x * 0.5 + x) // 260) % len(cores)
        desenhar_guarda_sol(tela, x + 60, Y_AREIA + 50, cores[idx])
        desenhar_guarda_sol(tela, x + 170, Y_AREIA + 40, cores[(idx + 2) % len(cores)])
    for x in _repetir(cam_x, 0.7, 520):
        desenhar_coqueiro(tela, x + 120, Y_CHAO)
        desenhar_quiosque(tela, x + 330, Y_CHAO)


def desenhar_fundo_copacabana(tela, cam_x, nivel=None):
    sup = _superficies_copacabana()
    t = pygame.time.get_ticks()
    tela.blit(sup["ceu"], (0, 0))
    pygame.draw.circle(tela, (255, 235, 150), (LARGURA - 140, 80), 36)  # sol
    desenhar_morros(tela, cam_x)
    desenhar_mar(tela, cam_x, t)
    desenhar_areia(tela, cam_x)
    pygame.draw.rect(tela, (60, 45, 35), (0, Y_CHAO, LARGURA, ALTURA - Y_CHAO))  # fundo dos buracos


# ---------------- CENÁRIO: AVENIDA PAULISTA (SÃO PAULO) ----------------
Y_RUA = 392              # topo do asfalto (atrás da calçada)
CICLO_SP = 1600          # largura das camadas de prédios, que se repetem
_cache_sp = {}


def _camada_predios(semente, alt_min, alt_max, cor, cor_janela):
    """Desenha uma faixa de prédios (com janelas, se cor_janela) numa Surface transparente."""
    rnd = random.Random(semente)
    camada = pygame.Surface((CICLO_SP, Y_RUA), pygame.SRCALPHA)
    x = 0
    while x < CICLO_SP - 40:
        w = min(rnd.randint(60, 130), CICLO_SP - x)
        h = rnd.randint(alt_min, alt_max)
        topo = Y_RUA - h
        pygame.draw.rect(camada, cor, (x, topo, w - 6, h))
        if cor_janela:
            for jy in range(topo + 10, Y_RUA - 14, 18):
                for jx in range(x + 8, x + w - 18, 14):
                    acesa = rnd.random() < 0.2
                    pygame.draw.rect(camada, (250, 220, 120) if acesa else cor_janela, (jx, jy, 7, 10))
        if rnd.random() < 0.3:  # antena no telhado
            pygame.draw.line(camada, cor, (x + w // 2, topo), (x + w // 2, topo - 24), 2)
        x += w
    return camada


def _desenhar_torre_tv(sup, x, base):
    """Torre de transmissão listrada de vermelho e branco."""
    altura = 300
    for i in range(10):
        y0, y1 = base - i * altura // 10, base - (i + 1) * altura // 10
        l0, l1 = 22 - i * 2, 22 - (i + 1) * 2
        cor = (210, 60, 50) if i % 2 == 0 else (235, 235, 235)
        pygame.draw.polygon(sup, cor, [(x - l0, y0), (x + l0, y0), (x + l1, y1), (x - l1, y1)])
    pygame.draw.line(sup, (200, 60, 50), (x, base - altura), (x, base - altura - 40), 3)


def _superficies_sp():
    if _cache_sp:
        return _cache_sp
    ceu = pygame.Surface((LARGURA, Y_RUA))
    for y in range(Y_RUA):
        t = y / Y_RUA
        ceu.fill((int(140 + 55 * t), int(145 + 52 * t), int(158 + 44 * t)), (0, y, LARGURA, 1))
    _cache_sp["ceu"] = ceu

    longe = _camada_predios(7, 140, 300, (150, 156, 170), None)
    _desenhar_torre_tv(longe, 1150, Y_RUA)
    _cache_sp["longe"] = longe
    _cache_sp["meio"] = _camada_predios(21, 90, 230, (95, 100, 115), (70, 75, 90))

    calcada = pygame.Surface((TILE, TILE))  # placas de concreto com detalhe preto
    calcada.fill((178, 178, 172))
    for i in range(0, TILE, TILE // 2):
        pygame.draw.line(calcada, (140, 140, 135), (i, 0), (i, TILE), 2)
        pygame.draw.line(calcada, (140, 140, 135), (0, i), (TILE, i), 2)
    meio = TILE // 2
    pygame.draw.polygon(calcada, (60, 60, 60), [(meio, 8), (TILE - 8, meio), (meio, TILE - 8), (8, meio)])
    pygame.draw.rect(calcada, (120, 120, 118), (0, 0, TILE, 5))  # meio-fio
    _cache_sp["calcada"] = calcada

    subsolo = pygame.Surface((TILE, TILE))
    subsolo.fill((80, 80, 86))
    for x, y in ((9, 12), (32, 22), (18, 38), (40, 40)):
        pygame.draw.circle(subsolo, (66, 66, 72), (x, y), 3)
    _cache_sp["subsolo"] = subsolo

    fachada = pygame.Surface((TILE, TILE))  # concreto com uma janela de vidro
    fachada.fill((150, 150, 156))
    pygame.draw.rect(fachada, (85, 110, 135), (10, 10, TILE - 20, TILE - 20))
    pygame.draw.rect(fachada, (170, 200, 220), (12, 12, 8, TILE - 24))
    pygame.draw.rect(fachada, (110, 110, 116), (0, 0, TILE, TILE), 2)
    _cache_sp["fachada"] = fachada
    return _cache_sp


def desenhar_poste(tela, x, y):
    pygame.draw.line(tela, (50, 50, 55), (x, y), (x, y - 110), 4)
    pygame.draw.line(tela, (50, 50, 55), (x, y - 110), (x + 24, y - 110), 4)
    pygame.draw.circle(tela, (255, 235, 160), (x + 24, y - 104), 6)


def desenhar_arvore(tela, x, y):
    pygame.draw.rect(tela, (90, 65, 45), (x - 4, y - 60, 8, 60))
    for dx, dy, r in ((0, -78, 30), (-22, -62, 22), (22, -62, 22)):
        pygame.draw.circle(tela, (55, 120, 60), (x + dx, y + dy), r)


def desenhar_museu(tela, x, y):
    """Museu vermelho suspenso por dois pórticos, com o vão livre embaixo."""
    vermelho = (200, 40, 40)
    for px in (x, x + 300):
        pygame.draw.rect(tela, vermelho, (px, y - 150, 22, 150))       # pilares
    pygame.draw.rect(tela, vermelho, (x, y - 150, 322, 18))             # viga de cima
    pygame.draw.rect(tela, (60, 65, 75), (x + 22, y - 132, 278, 62))    # caixa de vidro
    for jx in range(x + 30, x + 296, 22):
        pygame.draw.line(tela, (110, 120, 135), (jx, y - 130), (jx, y - 72), 2)
    pygame.draw.rect(tela, vermelho, (x, y - 70, 322, 8))               # viga de baixo


def desenhar_rua(tela, cam_x, t):
    pygame.draw.rect(tela, (62, 62, 68), (0, Y_RUA, LARGURA, Y_CHAO - Y_RUA))
    for x in _repetir(cam_x, 0.9, 80):  # faixa amarela tracejada
        pygame.draw.rect(tela, (230, 200, 60), (x, Y_RUA + 18, 40, 4))
    cores = [(200, 50, 50), (240, 240, 240), (50, 90, 180), (240, 200, 40)]
    pista = LARGURA + 300
    for i, cor in enumerate(cores):  # carros passando
        sentido = 1 if i % 2 == 0 else -1
        x = (i * 330 + sentido * t * 0.12 - cam_x * 0.9) % pista - 150
        y = Y_RUA + (4 if sentido > 0 else 22)
        pygame.draw.rect(tela, cor, (x, y, 70, 14), border_radius=4)
        pygame.draw.rect(tela, cor, (x + 14, y - 10, 38, 12), border_radius=4)
        pygame.draw.rect(tela, (150, 190, 220), (x + 18, y - 8, 30, 8))
        for rx in (x + 14, x + 56):
            pygame.draw.circle(tela, (20, 20, 20), (int(rx), y + 14), 5)


def desenhar_garoa(tela, t):
    for i in range(80):
        x = (i * 131 - t * 0.05) % LARGURA
        y = (i * 57 + t * 0.4) % ALTURA
        pygame.draw.line(tela, (215, 220, 230), (x, y), (x - 3, y + 9), 1)


def desenhar_fundo_saopaulo(tela, cam_x, nivel=None):
    sup = _superficies_sp()
    t = pygame.time.get_ticks()
    tela.blit(sup["ceu"], (0, 0))
    for camada, fator in ((sup["longe"], 0.1), (sup["meio"], 0.3)):
        for x in _repetir(cam_x, fator, CICLO_SP):
            tela.blit(camada, (x, 0))
    for x in _repetir(cam_x, 0.6, 1400):
        desenhar_museu(tela, int(x) + 500, Y_RUA)
    for x in _repetir(cam_x, 0.6, 280):
        desenhar_arvore(tela, int(x) + 60, Y_RUA)
        desenhar_poste(tela, int(x) + 200, Y_RUA)
    desenhar_rua(tela, cam_x, t)
    pygame.draw.rect(tela, (40, 40, 45), (0, Y_CHAO, LARGURA, ALTURA - Y_CHAO))  # fundo dos buracos
    desenhar_garoa(tela, t)


# ---------------- CENÁRIO: CURITIBA E A PONTE DA FRONTEIRA ----------------
# A fase começa num parque de Curitiba e, a partir da coluna "ponte_inicio",
# vira a ponte internacional sobre o rio, que termina na aduana da Argentina.
Y_RIO = 300              # topo da água do rio
_cache_cwb = {}


def _fonte_placa(tamanho):
    chave = ("fonte", tamanho)
    if chave not in _cache_cwb:
        _cache_cwb[chave] = pygame.font.Font(None, tamanho)
    return _cache_cwb[chave]


def _superficies_cwb():
    if "ceu" in _cache_cwb:
        return _cache_cwb
    ceu = pygame.Surface((LARGURA, Y_CHAO))
    for y in range(Y_CHAO):  # céu frio, azul acinzentado
        t = min(1, y / 330)
        ceu.fill((int(120 + 70 * t), int(150 + 55 * t), int(185 + 40 * t)), (0, y, LARGURA, 1))
    _cache_cwb["ceu"] = ceu

    neblina = pygame.Surface((LARGURA, 90), pygame.SRCALPHA)
    for y in range(90):
        neblina.fill((235, 240, 245, int(110 * (1 - abs(y - 45) / 45))), (0, y, LARGURA, 1))
    _cache_cwb["neblina"] = neblina

    def tile(cor_fundo, desenho):
        s = pygame.Surface((TILE, TILE))
        s.fill(cor_fundo)
        desenho(s)
        return s

    def paralelepipedo(s):  # pedras retangulares desencontradas
        for linha, y in enumerate(range(0, TILE, 12)):
            desloc = 0 if linha % 2 == 0 else 12
            for x in range(-desloc, TILE, 24):
                pygame.draw.rect(s, (128, 124, 118), (x + 1, y + 1, 22, 10), border_radius=3)
        pygame.draw.rect(s, (95, 120, 70), (0, 0, TILE, 4))  # beirada de grama

    def terra(s):
        for x, y in ((9, 12), (32, 22), (18, 38), (40, 40)):
            pygame.draw.circle(s, (92, 70, 52), (x, y), 3)

    def pedra(s):  # muro de pedra para plataformas
        for y in range(0, TILE, 16):
            for x in range(-8 if (y // 16) % 2 else 0, TILE, 24):
                pygame.draw.rect(s, (150, 145, 135), (x + 1, y + 1, 22, 14), border_radius=2)

    def pista(s):  # asfalto da ponte
        pygame.draw.rect(s, (200, 200, 195), (0, 0, TILE, 6))      # calçada da ponte
        pygame.draw.rect(s, (230, 200, 60), (6, 26, 24, 4))         # faixa amarela

    def estrutura(s):  # concreto da estrutura da ponte
        pygame.draw.line(s, (120, 120, 118), (0, 8), (TILE, 8), 2)
        for x in (8, 40):
            pygame.draw.circle(s, (115, 115, 112), (x, 30), 3)

    _cache_cwb["chao"] = tile((100, 98, 94), paralelepipedo)
    _cache_cwb["terra"] = tile((110, 85, 62), terra)
    _cache_cwb["pedra"] = tile((115, 110, 102), pedra)
    _cache_cwb["pista"] = tile((70, 70, 74), pista)
    _cache_cwb["estrutura"] = tile((150, 150, 146), estrutura)
    return _cache_cwb


def desenhar_araucaria(tela, x, base, escala, cor):
    """Pinheiro-do-paraná: tronco fino e copa em forma de taça."""
    alt = int(150 * escala)
    topo = base - alt
    pygame.draw.line(tela, (80, 60, 45), (x, base), (x, topo + int(10 * escala)), max(2, int(6 * escala)))
    for i in range(4):  # camadas da copa, mais largas em cima
        larg = int((40 + i * 22) * escala)
        y = topo + int((36 - i * 12) * escala)
        pygame.draw.ellipse(tela, cor, (x - larg // 2, y, larg, int(16 * escala)))
        for lado in (-1, 1):  # galhos subindo até a copa
            pygame.draw.line(tela, (80, 60, 45), (x, y + int(30 * escala)),
                             (x + lado * larg // 3, y + int(8 * escala)), max(1, int(2 * escala)))


def desenhar_estufa(tela, x, base):
    """Estufa de vidro com cúpula, num jardim."""
    vidro, ferro = (215, 235, 240), (250, 250, 250)
    pygame.draw.rect(tela, vidro, (x, base - 70, 240, 70))
    pygame.draw.ellipse(tela, vidro, (x + 70, base - 140, 100, 140))
    pygame.draw.rect(tela, vidro, (x + 70, base - 80, 100, 80))
    for vx in range(x, x + 241, 20):
        pygame.draw.line(tela, ferro, (vx, base - 70), (vx, base), 2)
    for vx in range(x + 80, x + 170, 15):
        pygame.draw.line(tela, ferro, (vx, base - 128), (vx, base - 70), 2)
    pygame.draw.line(tela, ferro, (x, base - 35), (x + 240, base - 35), 2)
    pygame.draw.rect(tela, ferro, (x, base - 70, 240, 70), 2)
    pygame.draw.line(tela, ferro, (x + 120, base - 140), (x + 120, base - 158), 3)
    for i in range(6):  # canteiros de flores na frente
        pygame.draw.circle(tela, ((230, 90, 110), (250, 200, 60))[i % 2], (x + 20 + i * 40, base + 4), 7)


def desenhar_bandeira_brasil(tela, x, y):
    pygame.draw.line(tela, (70, 70, 70), (x, y), (x, y + 90), 3)
    r = pygame.Rect(x + 2, y, 54, 36)
    pygame.draw.rect(tela, (0, 150, 70), r)
    pygame.draw.polygon(tela, (250, 210, 0), [(r.centerx, r.y + 4), (r.right - 5, r.centery),
                                              (r.centerx, r.bottom - 4), (r.x + 5, r.centery)])
    pygame.draw.circle(tela, (30, 60, 150), r.center, 9)


def desenhar_bandeira_argentina(tela, x, y):
    pygame.draw.line(tela, (70, 70, 70), (x, y), (x, y + 90), 3)
    for i, cor in enumerate(((115, 175, 225), (255, 255, 255), (115, 175, 225))):
        pygame.draw.rect(tela, cor, (x + 2, y + i * 12, 54, 12))
    pygame.draw.circle(tela, (245, 190, 40), (x + 29, y + 18), 5)


def desenhar_placa(tela, x, base, linhas, cor=(20, 110, 60)):
    fonte = _fonte_placa(24)
    textos = [fonte.render(l, True, (255, 255, 255)) for l in linhas]
    w = max(t.get_width() for t in textos) + 20
    h = len(textos) * 20 + 12
    caixa = pygame.Rect(x - w // 2, base - 90 - h, w, h)
    for px in (caixa.x + 12, caixa.right - 12):
        pygame.draw.line(tela, (90, 90, 90), (px, caixa.bottom), (px, base), 4)
    pygame.draw.rect(tela, cor, caixa, border_radius=4)
    pygame.draw.rect(tela, (255, 255, 255), caixa.inflate(-6, -6), 2, border_radius=3)
    for i, t in enumerate(textos):
        tela.blit(t, t.get_rect(midtop=(caixa.centerx, caixa.y + 8 + i * 20)))


def desenhar_aduana(tela, x, base):
    """Posto de fronteira com cobertura e cancela."""
    pygame.draw.rect(tela, (235, 230, 220), (x, base - 80, 110, 80))
    pygame.draw.rect(tela, (120, 160, 200), (x + 14, base - 64, 36, 26))
    pygame.draw.rect(tela, (120, 160, 200), (x + 62, base - 64, 36, 26))
    pygame.draw.rect(tela, (70, 70, 80), (x - 20, base - 104, 300, 18))       # cobertura
    pygame.draw.rect(tela, (230, 230, 230), (x + 250, base - 86, 8, 86))      # pilar
    fonte = _fonte_placa(22)
    t = fonte.render("ADUANA", True, (255, 255, 255))
    tela.blit(t, t.get_rect(center=(x + 130, base - 95)))
    pygame.draw.rect(tela, (60, 60, 60), (x + 120, base - 40, 10, 40))        # cancela
    for i in range(5):
        cor = (220, 40, 40) if i % 2 == 0 else (250, 250, 250)
        pygame.draw.rect(tela, cor, (x + 130 + i * 18, base - 38, 18, 7))


def margem_do_rio(nivel):
    """Coluna onde a terra de Curitiba acaba antes da ponte (início da água).
    Procura, da ponte para trás, o último chão '#' da linha 9 do mapa."""
    if "_margem" not in nivel:
        mapa = nivel["fase"]["mapa"]
        linha = mapa[9] if len(mapa) > 9 else ""
        col = nivel["fase"].get("ponte_inicio", 0) - 1
        while col > 0 and (col >= len(linha) or linha[col] != "#"):
            col -= 1
        nivel["_margem"] = col + 1
    return nivel["_margem"]


def _curva_barranco(x0, x1, y0, y1, passos=14):
    """Pontos de uma curva suave (meia senoide) de (x0, y0) até (x1, y1)."""
    return [(x0 + (x1 - x0) * i / passos,
             y0 + (y1 - y0) * (1 - math.cos(math.pi * i / passos)) / 2) for i in range(passos + 1)]


def desenhar_fundo_curitiba(tela, cam_x, nivel=None):
    sup = _superficies_cwb()
    t = pygame.time.get_ticks()
    largura_mapa = nivel["largura"] if nivel else 100 * TILE
    ponte_ini = (nivel["fase"].get("ponte_inicio", 10 ** 6) if nivel else 10 ** 6) * TILE
    # A água aparece a partir da margem, e a encosta começa a descer 4 tiles antes dela.
    margem = (margem_do_rio(nivel) * TILE if nivel and ponte_ini < largura_mapa else 10 ** 7) - cam_x
    encosta = margem - 4 * TILE           # na tela: onde o gramado começa a descer
    grama, barro = (105, 145, 90), (120, 92, 66)

    # --- fundo comum às duas partes (sem emenda no céu)
    tela.blit(sup["ceu"], (0, 0))
    for x in _repetir(cam_x, 0.08, 700):  # serra ao longe
        pygame.draw.ellipse(tela, (115, 140, 150), (x - 60, 200, 520, 200))
        pygame.draw.ellipse(tela, (125, 150, 158), (x + 300, 220, 460, 180))
    pygame.draw.rect(tela, (70, 120, 80), (0, 262, LARGURA, Y_RIO - 262))  # mata ao longe / margem argentina
    for x in _repetir(cam_x, 0.3, 90):
        pygame.draw.circle(tela, (50, 100, 60), (int(x) + 40, 266), 18)
    for x in _repetir(cam_x, 0.25, 130):  # araucárias ao longe, só do lado da cidade
        if x + 90 < encosta + 2 * TILE:
            desenhar_araucaria(tela, int(x) + 50, Y_RIO + 6, 0.6, (45, 85, 70))

    # --- rio (atrás da encosta, então pode começar antes dela)
    if encosta < LARGURA:
        ax = max(0, int(encosta))
        tela.set_clip(pygame.Rect(ax, 0, LARGURA - ax, ALTURA))
        pygame.draw.rect(tela, (70, 120, 140), (0, Y_RIO, LARGURA, ALTURA - Y_RIO))
        for i, y in enumerate(range(Y_RIO + 12, ALTURA, 20)):
            for x in _repetir(cam_x, 0.4 + 0.1 * i, 110):
                dx = x + math.sin(t / 800 + i) * 14
                pygame.draw.line(tela, (130, 175, 190), (dx, y), (dx + 30, y), 2)
        tela.set_clip(None)

    # --- gramado de Curitiba, terminando numa encosta curva até a água
    if encosta > 0:
        pygame.draw.rect(tela, grama, (0, Y_RIO, max(0, encosta) + 1, Y_CHAO - Y_RIO))
        if encosta < LARGURA:
            curva = _curva_barranco(encosta, margem, Y_RIO, Y_CHAO)
            fundo_curva = [(margem, ALTURA), (encosta, ALTURA)]
            pygame.draw.polygon(tela, barro, curva + fundo_curva)                       # barranco
            pygame.draw.polygon(tela, grama, [(x - 16, y) for x, y in curva] + fundo_curva)
        for x in _repetir(cam_x, 0.5, 1300):
            if x + 600 + 260 < encosta:
                desenhar_estufa(tela, int(x) + 600, 400)
        for x in _repetir(cam_x, 0.65, 330):
            if x + 120 + 60 < encosta:   # árvore inteira ou nenhuma (nada cortado ao meio)
                desenhar_araucaria(tela, int(x) + 120, Y_CHAO, 1.0, (35, 95, 55))
        # buracos da cidade: terra escura
        pygame.draw.rect(tela, (45, 38, 32), (0, Y_CHAO, max(0, encosta), ALTURA - Y_CHAO))

    tela.blit(sup["neblina"], (0, 200))

    # --- cabeceira da ponte: pilar dentro d'água e poste de concreto no começo
    if nivel and ponte_ini < largura_mapa:
        px = ponte_ini - cam_x
        if -60 < px < LARGURA + 60:
            pygame.draw.rect(tela, (150, 150, 146), (px - 16, Y_CHAO, 16, ALTURA - Y_CHAO))   # pilar
            pygame.draw.rect(tela, (120, 120, 116), (px - 16, Y_CHAO, 4, ALTURA - Y_CHAO))
            onda = math.sin(t / 300) * 3
            pygame.draw.line(tela, (200, 225, 235), (px - 26, ALTURA - 40 + onda), (px - 16, ALTURA - 40 + onda), 2)
            pygame.draw.rect(tela, (175, 175, 170), (px - 4, Y_CHAO - 56, 14, 56))           # poste da cabeceira
            pygame.draw.rect(tela, (140, 140, 136), (px - 8, Y_CHAO - 60, 22, 6))
            pygame.draw.circle(tela, (255, 235, 160), (px + 3, Y_CHAO - 66), 6)

    # --- objetos da ponte, presos ao mundo (andam junto com o chão)
    if nivel and ponte_ini < largura_mapa:
        meio = (ponte_ini + largura_mapa) // 2
        desenhar_placa(tela, ponte_ini + 70 - cam_x, Y_CHAO, ["PONTE INTERNACIONAL", "ARGENTINA  >"])
        x0 = max(ponte_ini, (cam_x // 24) * 24)
        for wx in range(x0, min(largura_mapa, cam_x + LARGURA + 24), 24):  # guarda-corpo
            brasil = wx < meio
            cores = ((0, 150, 70), (250, 210, 0)) if brasil else ((115, 175, 225), (255, 255, 255))
            cor = cores[(wx // 24) % 2]
            sx = wx - cam_x
            pygame.draw.rect(tela, cor, (sx, Y_CHAO - 34, 6, 34))
            pygame.draw.rect(tela, cor, (sx, Y_CHAO - 36, 24, 5))
        mx = meio - cam_x  # marco da divisa no meio da ponte
        pygame.draw.rect(tela, (240, 240, 240), (mx - 5, Y_CHAO - 60, 10, 60))
        t1 = _fonte_placa(20).render("BRASIL | ARGENTINA", True, (30, 30, 30))
        fundo = t1.get_rect(midbottom=(mx, Y_CHAO - 62)).inflate(10, 6)
        pygame.draw.rect(tela, (245, 245, 235), fundo, border_radius=3)
        tela.blit(t1, t1.get_rect(center=fundo.center))
        desenhar_bandeira_brasil(tela, fundo.left - 70, Y_CHAO - 90)
        desenhar_bandeira_argentina(tela, fundo.right + 12, Y_CHAO - 90)
        van = nivel.get("van")
        if van:
            desenhar_aduana(tela, van.x - 330 - cam_x, Y_CHAO)
            desenhar_placa(tela, van.x - 420 - cam_x, Y_CHAO, ["BIENVENIDOS A", "ARGENTINA"],
                           (60, 120, 190))
            desenhar_bandeira_argentina(tela, van.x - 70 - cam_x, Y_CHAO - 90)



def tile_do_tema(tema, b, nivel=None):
    """Imagem do bloco '#' para fases com tema próprio (ou None para usar o padrão)."""
    if tema == "curitiba":
        sup = _superficies_cwb()
        inicio = (nivel["fase"].get("ponte_inicio", 10 ** 6) if nivel else 10 ** 6) * TILE
        if b.rect.y < Y_CHAO:
            return sup["pedra"]
        if b.rect.x >= inicio:
            return sup["pista"] if b.rect.y == Y_CHAO else sup["estrutura"]
        return sup["chao"] if b.rect.y == Y_CHAO else sup["terra"]
    if tema == "copacabana":
        sup = _superficies_copacabana()
        return sup["piso"] if b.rect.y <= Y_CHAO else sup["terra"]
    if tema == "saopaulo":
        sup = _superficies_sp()
        if b.rect.y < Y_CHAO:
            return sup["fachada"]
        return sup["calcada"] if b.rect.y == Y_CHAO else sup["subsolo"]
    return None


FUNDOS = {"copacabana": desenhar_fundo_copacabana, "saopaulo": desenhar_fundo_saopaulo,
          "curitiba": desenhar_fundo_curitiba}


def desenhar_cenario(tela, nivel, cam_x, tiles):
    cores = nivel["fase"]["cores"]
    tema = nivel["fase"].get("tema")
    if tema in FUNDOS:
        FUNDOS[tema](tela, cam_x, nivel)
    else:
        tela.fill(cores["ceu"])
        for x, h, w in nivel["predios"]:
            px = x - cam_x * 0.4
            if -w < px < LARGURA:
                pygame.draw.rect(tela, cores["predios"], (px, ALTURA - h - TILE, w, h))
    for b in nivel["blocos"]:
        r = b.rect.move(-cam_x, 0)
        if r.right < 0 or r.left > LARGURA:
            continue
        img = tile_do_tema(tema, b, nivel) if b.tipo == "#" else None
        if img:
            tela.blit(img, r)
        elif b.tipo == "B" and "bloco" in tiles:
            tela.blit(tiles["bloco"], r)
        elif b.tipo == "#" and "chao" in tiles:
            tile = tiles["chao"] if b.rect.y <= 9 * TILE else tiles.get("subsolo", tiles["chao"])
            tela.blit(tile, r)
        else:
            pygame.draw.rect(tela, cores["chao"] if b.tipo == "#" else cores["bloco"], r)
            pygame.draw.rect(tela, (0, 0, 0), r, 1)


def texto_central(tela, fonte, msg, y, cor=(255, 255, 255)):
    s, sombra = fonte.render(msg, True, cor), fonte.render(msg, True, (0, 0, 0))
    x = LARGURA // 2 - s.get_width() // 2
    tela.blit(sombra, (x + 2, y + 2))
    tela.blit(s, (x, y))


def escurecer(tela, alfa=150):
    """Camada preta semitransparente por cima de tudo (título, pausa)."""
    veu = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    veu.fill((0, 0, 0, alfa))
    tela.blit(veu, (0, 0))


def desenhar_hud(tela, fonte, fonte_p, jogador, nivel):
    tela.blit(fonte.render(f"Vidas: {jogador.vidas}", True, (0, 0, 0)), (16, 12))
    arma = ARMAS[jogador.arma]["nome"]
    if jogador.municao is not None:
        arma += f" ({jogador.municao})"
    tela.blit(fonte.render(f"Arma: {arma}", True, (0, 0, 0)), (16, 40))
    tela.blit(fonte.render(f"Pontos: {jogador.pontos}", True, (0, 0, 0)), (16, 68))
    chefe = nivel["chefe"]
    if chefe and chefe.acordado:
        w = 300
        x = LARGURA - w - 20
        tela.blit(fonte_p.render(chefe.nome, True, (0, 0, 0)), (x, 12))
        pygame.draw.rect(tela, (60, 0, 0), (x, 34, w, 14))
        pygame.draw.rect(tela, (230, 40, 40), (x, 34, w * max(0, chefe.vida) // chefe.vida_max, 14))
        pygame.draw.rect(tela, (0, 0, 0), (x, 34, w, 14), 2)


# ---------------- LOOP PRINCIPAL ----------------
def main():
    global SKINS_VISUAIS
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Fuga Hipotética")
    relogio = pygame.time.Clock()
    fonte = pygame.font.Font(None, 32)
    fonte_p = pygame.font.Font(None, 24)
    fonte_grande = pygame.font.Font(None, 72)

    tiles = carregar_tiles()
    SKINS_VISUAIS = carregar_skins()
    jogador = Jogador(carregar_animacoes())
    indice = 0
    nivel = carregar_fase(indice, jogador)
    estado = "titulo"

    rodando = True
    while rodando:
        # ----- eventos -----
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                rodando = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    rodando = False
                elif estado == "titulo" and ev.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    estado = "jogando"
                    nivel["aviso"] = 120
                elif estado in ("game_over", "vitoria") and ev.key == pygame.K_r:
                    jogador.vidas, jogador.pontos, indice, estado = 3, 0, 0, "jogando"
                    nivel = carregar_fase(indice, jogador)
                elif ev.key == pygame.K_p and estado in ("jogando", "pausado"):
                    estado = "pausado" if estado == "jogando" else "jogando"
                elif estado == "jogando":
                    if ev.key == pygame.K_SPACE:
                        jogador.pular()
                    elif ev.key == pygame.K_z:
                        jogador.socar()
                    elif ev.key == pygame.K_x:
                        tiro = jogador.atirar()
                        if tiro:
                            nivel["tiros"].append(tiro)
            elif ev.type == pygame.KEYUP and ev.key == pygame.K_SPACE:
                jogador.soltar_pulo()

        # ----- lógica -----
        if estado == "jogando":
            blocos, chefe = nivel["blocos"], nivel["chefe"]
            jogador.atualizar(pygame.key.get_pressed(), blocos)
            jogador.rect.right = min(jogador.rect.right, nivel["largura"])

            for it in nivel["itens"][:]:
                if jogador.rect.colliderect(it.rect):
                    jogador.pegar_arma(it.tipo)
                    jogador.pontos += PONTOS["item"]
                    nivel["itens"].remove(it)

            for cp in nivel["checkpoints"]:
                if not cp["ativo"] and jogador.rect.colliderect(cp["rect"]):
                    cp["ativo"] = True
                    jogador.inicio = (cp["rect"].centerx - jogador.LARG // 2, cp["rect"].bottom)

            for ini in nivel["inimigos"]:
                ini.atualizar(blocos, jogador, nivel["tiros_ini"])
            if chefe:
                chefe.atualizar(blocos, jogador, nivel["tiros_ini"])
            for t in nivel["tiros_ini"]:
                t.atualizar(blocos)

            # tiros do jogador
            for t in nivel["tiros"]:
                t.atualizar(blocos)
                alvos = [i for i in nivel["inimigos"] if i.perigoso and t.rect.colliderect(i.rect)]
                acertou_chefe = chefe and chefe.vida > 0 and t.rect.colliderect(chefe.rect)
                if t.tipo == "carteira" and (alvos or acertou_chefe or t.vida == 0):
                    centro = t.rect.center
                    nivel["explosoes"].append(Explosao(centro))
                    for i in nivel["inimigos"]:
                        if math.dist(centro, i.rect.center) < 90:
                            i.atingir("carteira", jogador.rect.centerx)
                    if chefe and math.dist(centro, chefe.rect.center) < 110:
                        chefe.atingir("carteira")
                    t.vida = 0
                elif alvos:
                    alvos[0].atingir(t.tipo, jogador.rect.centerx)
                    t.vida = 0
                elif acertou_chefe:
                    chefe.atingir(t.tipo)
                    t.vida = 0
            nivel["tiros"] = [t for t in nivel["tiros"] if t.vida > 0]

            # soco
            caixa = jogador.caixa_soco()
            if caixa:
                for ini in nivel["inimigos"]:
                    if ini.perigoso and caixa.colliderect(ini.rect):
                        ini.atingir("soco", jogador.rect.centerx)
                if chefe and caixa.colliderect(chefe.rect):
                    chefe.atingir("soco")
                nivel["blocos"] = [b for b in blocos
                                   if not (b.tipo == "B" and caixa.colliderect(b.rect))]

            # dano no jogador
            perdeu = jogador.rect.top > ALTURA
            for ini in nivel["inimigos"]:
                if ini.perigoso and jogador.rect.colliderect(ini.rect):
                    if jogador.vy > 0 and jogador.rect.bottom - ini.rect.top < 16:
                        ini.atingir("pisao", jogador.rect.centerx)
                        jogador.vy = -8
                    elif not jogador.invencivel:
                        ini.attack_anim = max(ini.attack_anim, 14)
                        perdeu = True
            if chefe and chefe.vida > 0 and jogador.rect.colliderect(chefe.rect):
                if jogador.vy > 0 and jogador.rect.bottom - chefe.rect.top < 18:
                    chefe.atingir("pisao")
                    jogador.vy = -10
                elif not jogador.invencivel:
                    perdeu = True
            for t in nivel["tiros_ini"]:
                if jogador.rect.colliderect(t.rect) and not jogador.invencivel:
                    perdeu, t.vida = True, 0

            for ini in nivel["inimigos"]:
                if not ini.perigoso and not ini.pontuado:
                    ini.pontuado = True
                    jogador.pontos += PONTOS["inimigo"]
            nivel["inimigos"] = [i for i in nivel["inimigos"]
                                 if i.estado != "removido" and i.rect.top < ALTURA]
            nivel["tiros_ini"] = [t for t in nivel["tiros_ini"] if t.vida > 0]
            nivel["explosoes"] = [e for e in nivel["explosoes"] if e.t > 0]
            if chefe and chefe.vida <= 0:
                nivel["chefe"] = None
                nivel["aviso_van"] = 120
                jogador.pontos += PONTOS["chefe"]

            if perdeu:
                jogador.vidas -= 1
                nivel["tiros_ini"].clear()
                if jogador.vidas <= 0:
                    estado = "game_over"
                else:
                    jogador.reiniciar()

            if nivel["van"] and not nivel["chefe"] and jogador.rect.colliderect(nivel["van"]):
                jogador.pontos += PONTOS["fase"]
                indice += 1
                if indice >= len(FASES):
                    estado = "vitoria"
                else:
                    nivel = carregar_fase(indice, jogador)

            nivel["aviso"] = max(0, nivel["aviso"] - 1)
            nivel["aviso_van"] = max(0, nivel.get("aviso_van", 0) - 1)

        # ----- desenho -----
        cam_x = max(0, min(jogador.rect.centerx - LARGURA // 3, nivel["largura"] - LARGURA))
        desenhar_cenario(tela, nivel, cam_x, tiles)
        desenhar_checkpoints(tela, nivel, cam_x)
        if nivel["van"]:
            desenhar_van(tela, nivel["van"], cam_x, nivel["chefe"] is not None, fonte_p)
        for it in nivel["itens"]:
            it.desenhar(tela, cam_x, fonte_p)
        for ini in nivel["inimigos"]:
            ini.desenhar(tela, cam_x, fonte_p)
        if nivel["chefe"]:
            nivel["chefe"].desenhar(tela, cam_x, fonte_p)
        for t in nivel["tiros"]:
            t.desenhar(tela, cam_x)
        for t in nivel["tiros_ini"]:
            t.desenhar(tela, cam_x, fonte_p)
        for e in nivel["explosoes"]:
            e.desenhar(tela, cam_x)
        jogador.desenhar(tela, cam_x)

        if estado == "titulo":
            escurecer(tela)
            texto_central(tela, fonte_grande, "FUGA HIPOTÉTICA", 90, (255, 230, 60))
            linhas = ["← →  andar     ESPAÇO  pular     ↓  abaixar",
                      "Z  soco (quebra blocos)     X  atirar     P  pausar",
                      "Pegue as armas, derrote o chefe e fuja na van!"]
            for n, linha in enumerate(linhas):
                texto_central(tela, fonte, linha, 200 + n * 40)
            if (pygame.time.get_ticks() // 500) % 2:
                texto_central(tela, fonte, "Aperte ENTER para começar", 380, (255, 230, 60))
            pygame.display.flip()
            relogio.tick(FPS)
            continue

        desenhar_hud(tela, fonte, fonte_p, jogador, nivel)
        if nivel["aviso"] and estado != "pausado":
            texto_central(tela, fonte_grande, nivel["fase"]["nome"], 160)
        if nivel.get("aviso_van") and estado != "pausado":
            texto_central(tela, fonte_grande, "VAN LIBERADA!", 160, (255, 230, 60))
        if estado == "pausado":
            escurecer(tela)
            texto_central(tela, fonte_grande, "PAUSADO", 180)
            texto_central(tela, fonte, "P para continuar", 250)
        elif estado == "game_over":
            texto_central(tela, fonte_grande, "GAME OVER", 180, (255, 80, 80))
            texto_central(tela, fonte, f"Pontos: {jogador.pontos}", 240)
            texto_central(tela, fonte, "R para recomeçar", 280)
        elif estado == "vitoria":
            texto_central(tela, fonte_grande, "VOCÊ ESCAPOU!", 180, (255, 230, 60))
            texto_central(tela, fonte, f"Pontos: {jogador.pontos}", 240)
            texto_central(tela, fonte, "R para jogar de novo", 280)

        pygame.display.flip()
        relogio.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
