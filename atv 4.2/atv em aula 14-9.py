from turtle import *

def soma_10(x):
    return x + 10

t = Turtle()
t.speed(0)

# Plano cartesiano

# Eixo dos X
t.pu()
t.goto(-300, 0)
t.pd()
t.goto(300, 0)
t.stamp()

# Eixo dos Y
t.pu()
t.goto(0, -300)
t.pd()
t.goto(0, 300)
t.lt(90)
t.stamp()





mainloop()