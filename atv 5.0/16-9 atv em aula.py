
from pygame import *

init()
screen = display.set_mode ((800,600))

running = True
while running == True:
    for ev in event.get():
        if ev.type == QUIT:
            running = False

    screen.fill("#CBE8F7") #desenhar os elementos na tela , 'screen.fill(#cor)'
    draw.rect(screen,"#60811B", (0,500,800,100)) #x,y,larg altura > GRAMA
    draw.line(screen,'fff251',)
    draw.circle(screen,'#fff251', (100,100),150) #raio do circulo) # SOL
    draw.polygon(screen, "#F2883B", ((400, 300), (450, 300), (425, 250))) #telhado



    display.update()







