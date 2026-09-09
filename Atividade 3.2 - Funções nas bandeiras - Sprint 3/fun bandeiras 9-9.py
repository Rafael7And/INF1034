from turtle import *
from random import randint
from time import sleep


t= Turtle() 

def desenha_retangulo (x,y,larg,alt,color):
    t.pu()
    t.goto(x,y)
    t.pd()

    t.begin_fill()
    t.fillcolor(color)
    for _ in range(2):
        t.fd(larg)
        t.rt(90)
        t.fd(alt)
        t.rt(90)
    t.end_fill()  

def desenha_triangulo(x,y,larg,alt,color):
    t.pu()
    t.goto(x,y)
    t.pd()

    t.begin_fill()
    t.fillcolor(color)
    for cont in range(3):
        

#----------------bandeira italia -------

# def desenha_italia():
#     desenha_retangulo(-150,200,150,300, '#028801')
#     desenha_retangulo(-300,200,150,300, '#F50102')
#     desenha_retangulo(00,200,150,300, '#FAFAFA')

# desenha_italia()
# sleep(2)
# t.clear()

# #----------------bandeira françaa -------
# def desenha_frança():
#     desenha_retangulo(-150,200,150,300, '#002153')
#     desenha_retangulo(-300,200,150,300, '#FAFAFA')
#     desenha_retangulo(000,200,150,300, '#CF0921')

# desenha_frança()
# sleep(5)
# t.clear()
#----------------bandeira sudao -------

def desenha_sudao():
    desenha_retangulo(-200,120,400,80,'red')
    desenha_retangulo(-200,40,400,80, 'white')
    desenha_retangulo (-200,-40,400,80,'black')

desenha_sudao()
sleep(5)
t.clear()


mainloop()








# t.goto (-200,0)

# t.fillcolor ('#F50102')
# t.begin_fill()
# t.rt(90)
# t.fd (100)
# t.right (90)
# t.fd (300)
# t.right (90)
# t.fd (100)
# t.right (90)
# t.fd (300)
# t.end_fill()

# t.pu ()
# t.goto (0,-300)
# t.pd()
# t.lt (90)
# t.forward (200)

# sleep (1)
# t.clear ()

