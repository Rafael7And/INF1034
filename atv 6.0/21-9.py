
#pip install pygame -no terminal
from pygame import *

init()

screen = display.set_mode ((800,600))
fonte = font.Font("tngani.ttf", 30)
gandalf = image.load("gandalfvsbalrog.png")
gandalf = transform.scale(gandalf, (200, 200))
mixer.init()
# mixer.music.load("you-shall-not-pass_1.mp3")
# mixer.music.play(-1)
mixer.Sound.play ('you-shall-not-pass_1.mp3')


nuvemVai = 500
nuvemVai2 = 200

balrog = image.load("balrog.png")
balrog = transform.scale(balrog, (300,300))

clock = time.Clock() #


running = True
while running == True:
    clock.tick(60) #fixar o frame , o valor de 60 fps

    for ev in event.get():
        if ev.type == QUIT:
            running = False

        #açao INSTANTANIA
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1 :
                you-shall-not-pass_1.mp3.play()
            elif event.button == 3
                you-shall-not-pass_1.mp3.play()

    #seção para movimentos e simulação fisica
    dt = clock.get_time ()/1000
    keys = key.get_pressed() #se o mouse mexer aumenta a velocidade no teclado
    
    if keys [K_RIGHT]: # movimenta setinha do teclado
        nuvemVai = nuvemVai + 10 * dt
        nuvemVai2 = nuvemVai2 + 10 * dt
    elif keys [K_LEFT]:
        nuvemVai = nuvemVai - 10 * dt
        nuvemVai2 = nuvemVai2 - 10 * dt



    mouse_x, mouse_y = mouse.get_pos()
    #print(mouse_x,mouse_y) #para ver a localização do mouse

    # if nuvemVai > 800:
    #     nuvemVai = 0

    # nuvemVai2 = nuvemVai2 + 10 * dt
    # if nuvemVai2 > 800:
    #     nuvemVai2 = 0

    
    #seção para desenho na tela
    screen.fill("#CBE8F7") #desenhar os elementos na tela , 'screen.fill(#cor)'
    draw.rect(screen,"#60811B", (0,500,800,100)) #x,y,larg altura > GRAMA
    draw.line(screen, "#FFF251", (80,40), (120,10), 8)    # cima direita
    draw.line(screen, "#FFF251", (100,80), (150,80), 8)   # direita
    draw.line(screen, "#FFF251", (80,120), (120,150), 8)  # baixo-di
    draw.line(screen, "#FFF251", (40,0), (40,220), 8)   # baixo
    draw.circle(screen,'#fff251', (mouse_x,mouse_y),100) #raio do circulo) # SOL
    draw.polygon(screen, "#F2883B", ((20,300), (220,300), (120,220)))  # telhado
    draw.rect(screen,"#74716D", (20,300,200,200)) #casa
    draw.rect(screen,"#3B0775", (50,420,50,80)) #porta
    draw.circle(screen, "#000000", (65,460), 4)  # macça da porta
    draw.rect(screen, "#311E02", (350,360,40,140)) #arvore 
    draw.circle(screen, "#058316", (370,320),60)  #arvore   
    draw.circle(screen, "#D51616", (370,370),5)#maça da arvore
    draw.circle(screen, "#D51616", (380,340),5)#maça da arvore
    draw.circle(screen, "#D51616", (350,300),5)#maça da arvore
    draw.circle(screen, "#D51616", (389,310),5)#maça da arvore
    draw.circle(screen, "#D51616", (365,290),5)#maça da arvore
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
    
    screen.blit(gandalf, (560, 320)) #image of gandalf
    screen.blit(balrog, (320, 300)) #image of balrog



    display.update()














