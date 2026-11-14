"""
Fuga Hipotética — motor base 

Controles:
  ← →      andar
  Espaço   pular (segurar = pulo mais alto)
  ↓        abaixar
  Z        soco (também quebra blocos 'B')
  X        poder (projétil)
  R        reiniciar (game over / vitória)
  Esc      sair
"""
import os
import glob
import random
import pygame

# ---------------- CONFIGURAÇÕES ----------------
LARGURA, ALTURA = 960, 528
TILE = 48
FPS = 60
GRAVIDADE = 0.6
VEL_MAX_QUEDA = 14
VEL_ANDAR = 4.5
FORCA_PULO = 13.5
ALTURA_SPRITE = 64          # altura final dos sprites do jogador na tela
PASTA = os.path.dirname(os.path.abspath(__file__))

# Legenda do mapa:
#   '#' chão/parede    'B' bloco quebrável (soco)
#   'P' início         'E' inimigo         'V' van (fim da fase)
FASES = [
    {
        "nome": "Fase 1 - Rio de Janeiro",
        "cores": {"ceu": (120, 190, 240), "predios": (90, 150, 200),
                  "chao": (214, 184, 120), "bloco": (230, 130, 60)},
        "mapa": [
            "",
            "",
            "",
            "",
            "                      BBB",
            "                                       ###",
            "             BB",
            "                                ##",
            "    P              E      ##            E      E      B          V",
            "##############   ###########   ##################   #######################",
            "##############   ###########   ##################   #######################",
        ],
    },
    {
        "nome": "Fase 2 - São Paulo",
        "cores": {"ceu": (165, 170, 180), "predios": (120, 125, 135),
                  "chao": (110, 110, 115), "bloco": (180, 90, 70)},
        "mapa": [
            "",
            "",
            "",
            "                                   BBBB",
            "                  ###                          ###",
            "                                                        BB",
            "          BB              ##",
            "                     E               ##",
            "    P         E           ##    E        E          E      B     V",
            "##########   ###########  ###  ###########   ##########  ###################",
            "##########   ###########  ###  ###########   ##########  ###################",
        ],
    },
    {
        "nome": "Fase 3 - Curitiba",
        "cores": {"ceu": (150, 175, 200), "predios": (70, 110, 80),
                  "chao": (95, 120, 85), "bloco": (140, 100, 70)},
        "mapa": [
            "",
            "",
            "",
            "                                              BBB",
            "                ##               ###",
            "                                                       ##",
            "         BB             ###",
            "                                        ##",
            "    P          E    E          E  E            E     E     B       V",
            "#########   #########   ###########   ##########   ############################",
            "#########   #########   ###########   ##########   ############################",
        ],
    },
]


# ---------------- UTILITÁRIOS ----------------
def mover_com_colisao(ent, solidos):
    """Move ent (precisa de rect, vx, vy) colidindo com os sólidos.
    Retorna (no_chao, bateu_na_parede)."""
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


def carregar_animacoes():
    """Procura imagens em assets/jogador/<estado>_<n>.png (PNG com fundo transparente).
    Ex.: parado_0.png, andar_0.png ... andar_5.png, pulo_0.png, abaixar_0.png, soco_0.png
    Se não achar nada, o jogador é desenhado como retângulo."""
    brutos = {}
    for estado in ("parado", "andar", "pulo", "abaixar", "soco"):
        arquivos = glob.glob(os.path.join(PASTA, "assets", "jogador", f"{estado}_*.png"))
        arquivos.sort(key=lambda a: int(os.path.splitext(a)[0].rsplit("_", 1)[1]))
        if arquivos:
            brutos[estado] = [pygame.image.load(a).convert_alpha() for a in arquivos]
    if not brutos:
        return {}
    # mesma escala para todos os quadros (o abaixado continua menor que o em pé)
    ref = brutos.get("parado", next(iter(brutos.values())))[0]
    fator = ALTURA_SPRITE / ref.get_height()
    return {
        e: [pygame.transform.smoothscale(
                img, (int(img.get_width() * fator), int(img.get_height() * fator)))
            for img in quadros]
        for e, quadros in brutos.items()
    }


# ---------------- ENTIDADES ----------------
class Bloco:
    def __init__(self, x, y, tipo):
        self.rect = pygame.Rect(x, y, TILE, TILE)
        self.tipo = tipo  # '#' fixo, 'B' quebrável


class Jogador:
    LARG, ALT, ALT_ABAIXADO = 30, 58, 36

    def __init__(self, anims):
        self.anims = anims
        self.vidas = 3
        self.inicio = (0, 0)

    def reiniciar(self):
        x, base = self.inicio
        self.rect = pygame.Rect(x, base - self.ALT, self.LARG, self.ALT)
        self.vx = self.vy = 0
        self.no_chao = False
        self.abaixado = False
        self.direcao = 1
        self.soco = 0            # frames restantes da animação de soco
        self.recarga_poder = 0
        self.invencivel = 60
        self.tempo_anim = 0

    def pular(self):
        if self.no_chao and not self.abaixado:
            self.vy = -FORCA_PULO

    def soltar_pulo(self):
        if self.vy < -4:         # soltar cedo = pulo mais baixo
            self.vy = -4

    def socar(self):
        if self.soco == 0:
            self.soco = 18

    def atualizar(self, teclas, solidos):
        # abaixar (só no chão; só levanta se houver espaço)
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

        self.vy = min(self.vy + GRAVIDADE, VEL_MAX_QUEDA)
        self.no_chao, _ = mover_com_colisao(self, solidos)

        self.soco = max(0, self.soco - 1)
        self.recarga_poder = max(0, self.recarga_poder - 1)
        self.invencivel = max(0, self.invencivel - 1)
        self.tempo_anim += 1

    def caixa_soco(self):
        if self.soco <= 8:       # só os primeiros frames do soco acertam
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
        if self.vx != 0:
            return "andar"
        return "parado"

    def desenhar(self, tela, cam_x):
        if self.invencivel and (self.invencivel // 4) % 2:
            return  # pisca quando invencível
        quadros = self.anims.get(self.estado()) or self.anims.get("parado")
        if quadros:
            img = quadros[(self.tempo_anim // 6) % len(quadros)]
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


class Inimigo:
    """Inimigo genérico: patrulha e vira em paredes/beiradas.
    Troque o desenho e o efeito em 'atingir' pelo que quiser."""
    LARG, ALT = 34, 44

    def __init__(self, x, base):
        self.rect = pygame.Rect(x, base - self.ALT, self.LARG, self.ALT)
        self.vx, self.vy = -1.5, 0
        self.ativo = True        # False = não causa dano

    def atingir(self, ataque):
        """ataque: 'soco', 'poder' ou 'pisao'. Aqui entra o efeito de cada arma."""
        self.ativo = False

    def atualizar(self, solidos):
        if not self.ativo:
            return
        self.vy = min(self.vy + GRAVIDADE, VEL_MAX_QUEDA)
        no_chao, bateu = mover_com_colisao(self, solidos)
        if bateu:
            self.vx *= -1
        elif no_chao:
            fx = self.rect.right + 2 if self.vx > 0 else self.rect.left - 3
            pe = pygame.Rect(fx, self.rect.bottom + 2, 1, 1)
            if not any(pe.colliderect(b.rect) for b in solidos):
                self.vx *= -1

    def desenhar(self, tela, cam_x):
        r = self.rect.move(-cam_x, 0)
        pygame.draw.rect(tela, (200, 50, 50), r, border_radius=8)
        d = 1 if self.vx > 0 else -1
        for dx in (-6, 6):
            pygame.draw.circle(tela, (255, 255, 255), (r.centerx + dx + 3 * d, r.top + 14), 5)
            pygame.draw.circle(tela, (0, 0, 0), (r.centerx + dx + 5 * d, r.top + 14), 2)


class Projetil:
    def __init__(self, x, y, direcao):
        self.rect = pygame.Rect(0, 0, 16, 10)
        self.rect.center = (x, y)
        self.vx = 9 * direcao
        self.vida = 70

    def atualizar(self, solidos):
        self.rect.x += self.vx
        self.vida -= 1
        if any(self.rect.colliderect(b.rect) for b in solidos):
            self.vida = 0

    def desenhar(self, tela, cam_x):
        pygame.draw.ellipse(tela, (255, 230, 60), self.rect.move(-cam_x, 0))


# ---------------- FASE ----------------
def carregar_fase(indice, jogador):
    fase = FASES[indice]
    blocos, inimigos, van = [], [], None
    for lin, linha in enumerate(fase["mapa"]):
        for col, c in enumerate(linha):
            x, y = col * TILE, lin * TILE
            if c in "#B":
                blocos.append(Bloco(x, y, c))
            elif c == "P":
                jogador.inicio = (x + 9, y + TILE)
            elif c == "E":
                inimigos.append(Inimigo(x + 7, y + TILE))
            elif c == "V":
                van = pygame.Rect(x, y + TILE - 64, 110, 64)
    jogador.reiniciar()
    largura = max(len(l) for l in fase["mapa"]) * TILE
    rnd = random.Random(indice)  # prédios do fundo (sempre iguais na mesma fase)
    predios = [(i * 70, rnd.randint(120, 300), rnd.randint(50, 80))
               for i in range(largura // 70 // 2 + LARGURA // 70 + 2)]
    return {"fase": fase, "blocos": blocos, "inimigos": inimigos, "van": van,
            "largura": largura, "predios": predios, "projeteis": [], "aviso": 120}


def desenhar_van(tela, van, cam_x):
    r = van.move(-cam_x, 0)
    pygame.draw.rect(tela, (240, 240, 240), r, border_radius=10)
    pygame.draw.rect(tela, (120, 180, 220), (r.x + 10, r.y + 10, 30, 20))
    pygame.draw.rect(tela, (120, 180, 220), (r.x + 50, r.y + 10, 30, 20))
    pygame.draw.rect(tela, (120, 180, 220), (r.right - 22, r.y + 10, 16, 24))
    for wx in (r.x + 22, r.right - 22):
        pygame.draw.circle(tela, (30, 30, 30), (wx, r.bottom), 11)


def desenhar_cenario(tela, nivel, cam_x):
    cores = nivel["fase"]["cores"]
    tela.fill(cores["ceu"])
    for x, h, w in nivel["predios"]:   # parallax: anda a 40% da câmera
        px = x - cam_x * 0.4
        if -w < px < LARGURA:
            pygame.draw.rect(tela, cores["predios"], (px, ALTURA - h - TILE, w, h))
    for b in nivel["blocos"]:
        r = b.rect.move(-cam_x, 0)
        if r.right < 0 or r.left > LARGURA:
            continue
        cor = cores["chao"] if b.tipo == "#" else cores["bloco"]
        pygame.draw.rect(tela, cor, r)
        pygame.draw.rect(tela, (0, 0, 0), r, 1)


def texto_central(tela, fonte, msg, y, cor=(255, 255, 255)):
    s = fonte.render(msg, True, cor)
    sombra = fonte.render(msg, True, (0, 0, 0))
    x = LARGURA // 2 - s.get_width() // 2
    tela.blit(sombra, (x + 2, y + 2))
    tela.blit(s, (x, y))


# ---------------- LOOP PRINCIPAL ----------------
def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Fuga Hipotética")
    relogio = pygame.time.Clock()
    fonte = pygame.font.Font(None, 36)
    fonte_grande = pygame.font.Font(None, 72)

    jogador = Jogador(carregar_animacoes())
    indice = 0
    nivel = carregar_fase(indice, jogador)
    estado = "jogando"  # 'jogando', 'game_over', 'vitoria'

    rodando = True
    while rodando:
        # ----- eventos -----
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                rodando = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    rodando = False
                elif estado != "jogando" and ev.key == pygame.K_r:
                    jogador.vidas, indice, estado = 3, 0, "jogando"
                    nivel = carregar_fase(indice, jogador)
                elif estado == "jogando":
                    if ev.key == pygame.K_SPACE:
                        jogador.pular()
                    elif ev.key == pygame.K_z:
                        jogador.socar()
                    elif ev.key == pygame.K_x and jogador.recarga_poder == 0:
                        jogador.recarga_poder = 30
                        nivel["projeteis"].append(
                            Projetil(jogador.rect.centerx, jogador.rect.top + 20, jogador.direcao))
            elif ev.type == pygame.KEYUP and ev.key == pygame.K_SPACE:
                jogador.soltar_pulo()

        # ----- lógica -----
        if estado == "jogando":
            blocos = nivel["blocos"]
            jogador.atualizar(pygame.key.get_pressed(), blocos)

            for ini in nivel["inimigos"]:
                ini.atualizar(blocos)
            for p in nivel["projeteis"]:
                p.atualizar(blocos)
                for ini in nivel["inimigos"]:
                    if ini.ativo and p.rect.colliderect(ini.rect):
                        ini.atingir("poder")
                        p.vida = 0
            nivel["projeteis"] = [p for p in nivel["projeteis"] if p.vida > 0]

            caixa = jogador.caixa_soco()
            if caixa:
                for ini in nivel["inimigos"]:
                    if ini.ativo and caixa.colliderect(ini.rect):
                        ini.atingir("soco")
                nivel["blocos"] = [b for b in blocos
                                   if not (b.tipo == "B" and caixa.colliderect(b.rect))]

            perdeu = jogador.rect.top > ALTURA  # caiu no buraco
            for ini in nivel["inimigos"]:
                if ini.ativo and jogador.rect.colliderect(ini.rect):
                    if jogador.vy > 0 and jogador.rect.bottom - ini.rect.top < 16:
                        ini.atingir("pisao")
                        jogador.vy = -8
                    elif not jogador.invencivel:
                        perdeu = True
            # inimigos inativos somem (troque isso se quiser que fiquem no mapa)
            nivel["inimigos"] = [i for i in nivel["inimigos"] if i.ativo]

            if perdeu:
                jogador.vidas -= 1
                if jogador.vidas <= 0:
                    estado = "game_over"
                else:
                    jogador.reiniciar()

            if nivel["van"] and jogador.rect.colliderect(nivel["van"]):
                # TODO: chefe antes da van
                indice += 1
                if indice >= len(FASES):
                    estado = "vitoria"
                else:
                    nivel = carregar_fase(indice, jogador)

            nivel["aviso"] = max(0, nivel["aviso"] - 1)

        # ----- desenho -----
        cam_x = max(0, min(jogador.rect.centerx - LARGURA // 3, nivel["largura"] - LARGURA))
        desenhar_cenario(tela, nivel, cam_x)
        if nivel["van"]:
            desenhar_van(tela, nivel["van"], cam_x)
        for ini in nivel["inimigos"]:
            ini.desenhar(tela, cam_x)
        for p in nivel["projeteis"]:
            p.desenhar(tela, cam_x)
        jogador.desenhar(tela, cam_x)

        tela.blit(fonte.render(f"Vidas: {jogador.vidas}", True, (0, 0, 0)), (16, 12))
        tela.blit(fonte.render(nivel["fase"]["nome"], True, (0, 0, 0)), (16, 40))
        if nivel["aviso"]:
            texto_central(tela, fonte_grande, nivel["fase"]["nome"], 160)
        if estado == "game_over":
            texto_central(tela, fonte_grande, "GAME OVER", 180, (255, 80, 80))
            texto_central(tela, fonte, "R para recomeçar", 250)
        elif estado == "vitoria":
            texto_central(tela, fonte_grande, "VOCÊ ESCAPOU!", 180, (255, 230, 60))
            texto_central(tela, fonte, "R para jogar de novo", 250)

        pygame.display.flip()
        relogio.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()