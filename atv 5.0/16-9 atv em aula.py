#pip install pygame -no terminal
from pygame import *

init()

screen = display.set_mode ((800,600))
fonte = font.Font("tngani.ttf", 30)
gandalf = image.load("gandalfvsbalrog.png")
gandalf = transform.scale(gandalf, (200, 200))
mixer.init()
mixer.music.load("you-shall-not-pass_1.mp3")
mixer.music.play(-1)

nuvemVai = 500
nuvemVai2 = 200

balrog = image.load("balrog.png")
balrog = transform.scale(balrog, (300,300))

x_gandalf = 800
x_balrog = 950

running = True
while running == True:
    for ev in event.get():
        if ev.type == QUIT:
            running = False

    screen.fill("#CBE8F7") #desenhar os elementos na tela , 'screen.fill(#cor)'
    draw.rect(screen,"#60811B", (0,500,800,100)) #x,y,larg altura > GRAMA
    draw.line(screen, "#FFF251", (80,40), (120,10), 8)    # cima direita
    draw.line(screen, "#FFF251", (100,80), (150,80), 8)   # direita
    draw.line(screen, "#FFF251", (80,120), (120,150), 8)  # baixo-di
    draw.line(screen, "#FFF251", (40,0), (40,220), 8)   # baixo
    draw.circle(screen,'#fff251', (0,80),100) #raio do circulo) # SOL
    draw.polygon(screen, "#F2883B", ((20,300), (220,300), (120,220)))  # telhado
    draw.rect(screen,"#74716D", (20,300,200,200)) #casa
    draw.rect(screen,"#3B0775", (50,420,50,80)) #porta
    draw.circle(screen, "#000000", (65,460), 4)  # macça da porta
    draw.rect(screen, "#311E02", (350,360,40,140)) #arvore 
    draw.circle(screen, "#058316", (370,320),60)  #arvore   
    draw.circle(screen, "#D51616", (370,370),5)
    draw.circle(screen, "#D51616", (380,340),5)
    draw.circle(screen, "#D51616", (350,300),5)
    draw.circle(screen, "#D51616", (389,310),5)
    draw.circle(screen, "#D51616", (365,290),5)
    draw.circle(screen, "#D51616", (340,350),5) #maça da arvore
    draw.circle(screen, "#FBF7F7", (nuvemVai,80),35) #nuvem 1
    draw.circle(screen, "#FBF7F7", (nuvemVai + 40,80),35) #nuvem 1
    draw.circle(screen, "#FBF7F7", (nuvemVai + 80,80),35) #nuvem 1
    draw.circle(screen, "#FBF7F7", (nuvemVai + 120,80),35) #nuvem 1
    draw.circle(screen, "#FBF7F7", (nuvemVai2,200),35) #nuvem 2
    draw.circle(screen, "#FBF7F7", (nuvemVai2 + 40,200),35) #nuvem 2
    draw.circle(screen, "#FBF7F7", (nuvemVai2 + 80,200),35) #nuvem 2
    draw.circle(screen, "#FBF7F7", (nuvemVai2 + 120,200),35) #nuvem 2
    draw.rect(screen, "#1339A1", (80,320,40,35)) #janlaum cima
    draw.rect(screen, "#1339A1", (120,320,40,35)) #janlaum cima
    draw.rect(screen, "#1339A1", (140,410,40,35)) #janela baixo

    #shall you not pass
    texto = fonte.render("shall you not pass?", True, "black")
    screen.blit(texto, (300,110))
    
    screen.blit(gandalf, (x_gandalf, 320)) #image of gandalf
    screen.blit(balrog, (x_balrog, 300)) #image of balrog

    x_gandalf += 1
    x_balrog += 1

    if x_gandalf > 800:
        x_gandalf = -120

    if x_balrog > 800:
        x_balrog = -260

    nuvemVai += 1
    if nuvemVai > 800:
        nuvemVai = 0

    nuvemVai2 += 1
    if nuvemVai2 > 800:
        nuvemVai2 = 0

    display.update()
