from turtle import *




t= Turtle() 
t.shape ("turtle")

t.pu()
t.goto(-400, 0)
t.pd()
t.goto(400, 0)
t.stamp()

t.pu()
t.goto(0, -400)
t.pd()
t.goto(0, 400)
t.lt(90)
t.stamp()
t.rt(90)

t.pu()
t.goto(50, 50)
t.pd()

t.color("yellow")
t.fillcolor("purple")
t.begin_fill()

for cont in range(8):
    t.forward (50)
    t.lt (45)
t.end_fill ()

t.pu()
t.goto(-100,-75)
t.pd()

t.color("red")
t.fillcolor("blue")
t.begin_fill()

for cont in range(12):
    t.forward (-50)
    t.lt (30)
t.end_fill ()

t.pu()
t.goto(100,-200)
t.pd()

t.color("yellow")
t.fillcolor("red")
t.begin_fill()


t.forward (-90)
t.lt (90)
t.forward(40)
t.lt (90)
t.forward(-90)
t.lt (90)
t.forward (40)

t.end_fill ()

t.pu()
t.goto(-200,200)
t.pd()

t.color ("green")
var_color = textinput("Escolha da cor", "Digite a cor da próxima forma geométrica:")
t.begin_fill()

for cont in range(3):
    t.forward(100)
    t.right(120)

t.end_fill()




mainloop()