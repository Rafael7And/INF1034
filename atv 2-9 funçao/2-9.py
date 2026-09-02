from turtle import *
from random import randint


t= Turtle() 
t.shape ("turtle")
#plano cartesiano


# t.pu()
# t.goto(-400, 0)
# t.pd()
# t.goto(400, 0)
# t.stamp()

# t.pu()
# t.goto(0, -400)
# t.pd()
# t.goto(0, 400)
# t.lt(90)
# t.stamp()
# t.rt(90)

# t.pu()
# t.goto(50, 50)
# t.pd()

#1 forma
def desenha_hoct (x,y,lado,cor):
    t.pu()
    t.goto(x, y)
    t.pd()

    t.fillcolor(cor)
    t.begin_fill()
    for _ in range(8):
        t.fd (lado)
        t.lt (45)
    t.end_fill ()

x = randint(100, 200)
y = randint(100, 200)
desenha_hoct (x,y,50, 'purple')

#2 forma #
def desenha_12 (x,y,lado, cor):
    t.pu()
    t.goto(x,y)
    t.pd()
    t.fillcolor(cor)
    t.begin_fill()

    for cont in range(12):
        t.forward (lado)
        t.lt (30)
    t.end_fill ()

x = randint(-99,-25)
y = randint(-150,-10)
desenha_12 (x,y,-50,'blue')

# #3 forma
def desenha_3(x,y,lado,cor):
    t.pu()
    t.goto(x,y)
    t.pd()

    t.fillcolor("red")
    t.begin_fill()

    t.forward (lado)
    t.lt (90)
    t.forward(40)
    t.lt (90)
    t.forward(lado)
    t.lt (90)
    t.forward (40)

    t.end_fill ()
# desenha_3 (100,-200,-90,'red')
x = randint(100, 300)
y = randint(-300, -200)
desenha_3(x, y, -90, 'red')


# #4 forma
def desenha_4 (x,y,lado, cor):
    t.pu()
    t.goto(x,y)
    t.pd()

    t.color (cor)
    t.begin_fill()

    for cont in range(3):
        t.forward(lado)
        t.right(120)

    t.end_fill()
# desenha_4 (-200,200,100,'green')
x = randint (-300,-200)
y = randint (200,300)
desenha_4 (x,y,200, 'green')
mainloop()
