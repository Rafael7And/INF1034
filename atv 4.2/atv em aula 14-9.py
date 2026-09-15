from turtle import *
from time import sleep
#site para ver o grafico https://www.geogebra.org/calculator


def raiz(x):
    return x**0.5

t = Turtle()
t.speed(0)

#plano cartesiano
def plano_cartesiano():
    t.color ('black')
    t.pu()
    t.goto(-400,0)
    t.pd()
    t.goto(400,0)
    t.stamp()

    t.pu()
    t.goto(0,-400)
    t.pd()
    t.goto(0,400)
    t.lt(90)
    t.stamp()
    t.rt(90)
plano_cartesiano()

######

# t.color("red")
# t.pu()
# t.goto(-100, soma_10(-100))
# t.pd()
# t.goto(100, soma_10(100))

# # O range vai do primeiro valor até o último -1
# print(list(range(-100, 100)))

# for x in range(-100, 100):
#     print(x)

# t.color("blue")
# t.pu()
# t.goto(-200, soma_10(-200))
# t.pd()
# for x in range(-99, 101):
#     t.goto(2 * x, soma_10(2*x))


###############  - y = √x

plano_cartesiano()
t.color("blue")
t.pu()
t.goto(0, raiz(0)*20)
t.pd()

for x in range(1, 101):
    t.goto(x*2, raiz(x)*20)

sleep(3)
t.clear()
# ---------------- y = 1/x -************
def inversa(x):
    return 1/x

plano_cartesiano()
t.color("red")

# Parte negativa
t.pu()
t.goto(-200, inversa(-100)*100)
t.pd()

for x in range(-99, 0):
    t.goto(x*2, inversa(x)*100)

# Parte positiva
t.pu()
t.goto(2, inversa(1)*100)
t.pd()

for x in range(1, 101):
    t.goto(x*2, inversa(x)*100)

sleep(3)
t.clear()
# ---------------- y = 2^x #############################

def potencia(x):
    return 2**x

plano_cartesiano()
t.color("red")
t.pu()
t.goto(-20, potencia(-10))
t.pd()

for x in range(-9, 9):
    t.goto(x*20, potencia(x))

sleep(3)
t.clear()

# ---------------- y = 5 - x² ############################
def parabola1(x):
    return 5 - x**2

plano_cartesiano()
t.color("red")
t.pu()
t.goto(-200, parabola1(-10)*20)
t.pd()

for x in range(-9, 11):
    t.goto(x*20, parabola1(x)*20)

sleep(3)
t.clear()


# ---------------- y = x² - 5x + 6 ----------------

def parabola2(x):
    return x**2 - 5*x + 6

plano_cartesiano()
t.color("red")

t.pu()
t.goto(-100, parabola2(-5)*10)
t.pd()

for x in range(-4,11):
    t.goto(x*20, parabola2(x)*10)

sleep(3)
t.clear()

# ---------------- y = x³ - x² - x + 1 -#####################
def cubica(x):
    return x**3 - x**2 - x + 1

plano_cartesiano()
t.color("red")
t.pu()
t.goto(-100, cubica(-5))
t.pd()

for x in range(-4, 6):
    t.goto(x*20, cubica(x))

sleep(3)
t.clear()










mainloop()