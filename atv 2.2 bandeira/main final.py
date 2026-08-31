from turtle import *
from time import sleep

t = Turtle() 

#------------------------bandeira italia O

t.fillcolor ('#028801')
t.begin_fill()
t.fd (100)
t.right (90)
t.fd (300)
t.right (90)
t.fd (100)
t.right (90)
t.fd (300)
t.end_fill()

t.goto (-200,0)

t.fillcolor ('#F50102')
t.begin_fill()
t.rt(90)
t.fd (100)
t.right (90)
t.fd (300)
t.right (90)
t.fd (100)
t.right (90)
t.fd (300)
t.end_fill()

t.pu ()
t.goto (0,-300)
t.pd()
t.lt (90)
t.forward (200)

sleep (1)
t.clear ()

#------------------------ bandeira costa pobre

t.fillcolor ('#001385')
t.begin_fill ()

t.fd (400)
t.rt (90)
t.fd (50)
t.rt (90)
t.fd (400)
t.rt (90)
t.fd (50)
t.end_fill ()


t.pu ()
t.goto (0,-300)
t.pd()

t.fillcolor ('#001385')
t.begin_fill ()

t.rt (90)
t.fd (400)
t.rt (90)
t.fd (50)
t.rt (90)
t.fd (400)
t.rt (90)
t.fd (50)
t.end_fill ()


t.fillcolor ('#DA291C')
t.begin_fill()

t.pu ()
t.goto (0,-250)
t.pendown () 

 
t.forward (150)
t.rt (90)
t.fd (400)
t.rt (90)
t.fd (150)
t.rt (90)
t.fd (400)
t.rt (90)
t.end_fill ()

t.goto (0,-350)
t.fd (350)
t.pu ()
t.goto (400,-350)
t.pd ()
t.fd (350)
sleep (1)
t.clear ()
#------------------------ Guiné - Bissau#####################

t.pu()
t.goto (-200,100)
t.pd()


t.fillcolor('#C81025')
t.begin_fill()

for cont in range(2):
    t.fd(100)
    t.rt(90)
    t.fd(200)
    t.rt(90)

t.end_fill()

t.pu()
t.goto(-180,00)
t.pd()


t.fillcolor("black")
t.begin_fill()

for cont in range(5):
    t.fd(60)
    t.rt(144)

t.end_fill()
t.pu()
t.goto(-157,- 0)
t.pd()


t.fillcolor("black")
t.begin_fill()

for cont in range(5):
    t.fd(14)
    t.rt(72)

t.end_fill()

t.pu()
t.goto(-100,100)
t.pd()


t.fillcolor('#F4CA15')
t.begin_fill()

for cont in range(2):
    t.fd(300)
    t.rt(90)
    t.fd(100)
    t.rt(90)

t.end_fill()

t.pu()
t.goto(-100,0)
t.pd()


t.fillcolor('#009947')
t.begin_fill()

for cont in range(2):
    t.fd(300)
    t.rt(90)
    t.fd(100)
    t.rt(90)

t.end_fill()
sleep (1)
t.clear ()



#------------------------ china

t.pu()
t.goto(-200,120)
t.pd()

# Fundo vermelho
t.color("red")
t.fillcolor("red")
t.begin_fill()

for cont in range(2):
    t.fd(400)
    t.rt(90)
    t.fd(240)
    t.rt(90)

t.end_fill()

# Estrela grande
t.pu()
t.goto(-170,40)
t.pd()

t.color("yellow")
t.fillcolor("yellow")
t.begin_fill()

for cont in range(5):
    t.fd(45)
    t.rt(144)

t.end_fill()


t.pu()
t.goto(-152,40)
t.pd()

t.begin_fill()

for cont in range(5):
    t.fd(10)
    t.rt(72)

t.end_fill()

# Estrela pequena 1
t.pu()
t.goto(-95,85)
t.pd()

t.begin_fill()
for cont in range(5):
    t.fd(18)
    t.rt(144)
t.end_fill()

t.pu()
t.goto(-90,85)
t.pd()

t.begin_fill()
for cont in range(5):
    t.fd(6)
    t.rt(72)
t.end_fill()

# Estrela pequena 2
t.pu()
t.goto(-75,55)
t.pd()

t.begin_fill()
for cont in range(5):
    t.fd(18)
    t.rt(144)
t.end_fill()

t.pu()
t.goto(-70,55)
t.pd()

t.begin_fill()
for cont in range(5):
    t.fd(6)
    t.rt(72)
t.end_fill()

# Estrela pequena 3
t.pu()
t.goto(-75,20)
t.pd()

t.begin_fill()
for cont in range(5):
    t.fd(18)
    t.rt(144)
t.end_fill()

t.pu()
t.goto(-70,20)
t.pd()

t.begin_fill()
for cont in range(5):
    t.fd(6)
    t.rt(72)
t.end_fill()

# Estrela pequena 4
t.pu()
t.goto(-95,-10)
t.pd()

t.begin_fill()
for cont in range(5):
    t.fd(18)
    t.rt(144)
t.end_fill()

t.pu()
t.goto(-90,-10)
t.pd()

t.begin_fill()
for cont in range(5):
    t.fd(6)
    t.rt(72)
t.end_fill()
sleep (1)
t.clear ()
#------------------------ FINLANDIA


t.pu()
t.goto(-200,120)
t.pd()


t.fillcolor("red")
t.begin_fill()

for cont in range(2):
    t.fd(400)
    t.rt(90)
    t.fd(240)
    t.rt(90)

t.end_fill()

# 
t.pu()
t.goto(-100,120)
t.pd()

t.fillcolor("white")
t.begin_fill()

for cont in range(2):
    t.fd(40)
    t.rt(90)
    t.fd(240)
    t.rt(90)

t.end_fill()

t.pu()
t.goto(-200,20)
t.pd()

t.begin_fill()

for cont in range(2):
    t.fd(400)
    t.rt(90)
    t.fd(40)
    t.rt(90)

t.end_fill()


t.pu()
t.goto(-90,120)
t.pd()


t.fillcolor("blue")
t.begin_fill()

for cont in range(2):
    t.fd(20)
    t.rt(90)
    t.fd(240)
    t.rt(90)

t.end_fill()


t.pu()
t.goto(-200,10)
t.pd()

t.begin_fill()

for cont in range(2):
    t.fd(400)
    t.rt(90)
    t.fd(20)
    t.rt(90)

t.end_fill()
sleep (1)
t.clear ()
#------------------------ panama

t.pu()
t.goto(-200,120)
t.pd()

t.color("black")
t.fillcolor("white")
t.begin_fill()

for cont in range(2):
    t.fd(200)
    t.rt(90)
    t.fd(120)
    t.rt(90)

t.end_fill()

t.pu()
t.goto(0,120)
t.pd()

t.fillcolor("red")
t.begin_fill()

for cont in range(2):
    t.fd(200)
    t.rt(90)
    t.fd(120)
    t.rt(90)

t.end_fill()

t.pu()
t.goto(-200,0)
t.pd()

t.fillcolor("blue")
t.begin_fill()

for cont in range(2):
    t.fd(200)
    t.rt(90)
    t.fd(120)
    t.rt(90)

t.end_fill()

t.pu()
t.goto(0,0)
t.pd()

t.fillcolor("white")
t.begin_fill()

for cont in range(2):
    t.fd(200)
    t.rt(90)
    t.fd(120)
    t.rt(90)

t.end_fill()

# Estrela azul
t.pu()
t.goto(-150,50)
t.pd()

t.color("blue")
t.fillcolor("blue")
t.begin_fill()

for cont in range(5):
    t.fd(40)
    t.rt(144)

t.end_fill()

t.pu()
t.goto(-137, 50)  
t.pd()

t.fillcolor("blue")
t.begin_fill()

for cont in range(5):
    t.fd(10)
    t.rt(72)

t.end_fill()

# Estrela vermelha
t.pu()
t.goto(50,-70)
t.pd()

t.color("red")
t.fillcolor("red")
t.begin_fill()

for cont in range(5):
    t.fd(40)
    t.rt(144)

t.end_fill()

t.pu()
t.goto(64, -70) 
t.pd()

t.fillcolor("red")
t.begin_fill()

for cont in range(5):
    t.fd(10)
    t.rt(72)

t.end_fill()
sleep (1)
t.clear ()
# ------------------------ França-250 xp


t.pu()
t.goto(-200,120)
t.pd()

t.color("black")
t.fillcolor("blue")
t.begin_fill()

for cont in range(2):
    t.fd(133)
    t.rt(90)
    t.fd(240)
    t.rt(90)

t.end_fill()

t.pu()
t.goto(-67,120)
t.pd()

t.fillcolor("white")
t.begin_fill()

for cont in range(2):
    t.fd(133)
    t.rt(90)
    t.fd(240)
    t.rt(90)

t.end_fill()


t.pu()
t.goto(66,120)
t.pd()

t.fillcolor("red")
t.begin_fill()

for cont in range(2):
    t.fd(134)
    t.rt(90)
    t.fd(240)
    t.rt(90)

t.end_fill()
sleep (1)
t.clear ()
# ------------------------ Suíça 300 xp

t.pu()
t.goto(-120,120)
t.pd()

t.color("black")
t.fillcolor("red")
t.begin_fill()

for cont in range(4):
    t.fd(240)
    t.rt(90)

t.end_fill()

t.pu()
t.goto(-20,80)
t.pd()

t.fillcolor("white")
t.begin_fill()

for cont in range(2):
    t.fd(40)
    t.rt(90)
    t.fd(160)
    t.rt(90)

t.end_fill()


t.pu()
t.goto(-80,20)
t.pd()

t.begin_fill()

for cont in range(2):
    t.fd(160)
    t.rt(90)
    t.fd(40)
    t.rt(90)

t.end_fill()
sleep (1)
t.clear ()
# ------------------------ Santa Lúcia 350 xp

t.pu()
t.goto(-200,120)
t.pd()

t.color("black")
t.fillcolor("#6EC6FF")
t.begin_fill()

for cont in range(2):
    t.fd(400)
    t.rt(90)
    t.fd(240)
    t.rt(90)

t.end_fill()

t.pu()
t.goto(0,100)
t.pd()

t.fillcolor("white")
t.begin_fill()

t.goto(-70,-100)
t.goto(70,-100)
t.goto(0,100)

t.end_fill()

t.pu()
t.goto(0,80)
t.pd()

t.fillcolor("black")
t.begin_fill()

t.goto(-50,-90)
t.goto(50,-90)
t.goto(0,80)

t.end_fill()

t.pu()
t.goto(0,20)
t.pd()

t.fillcolor("yellow")
t.begin_fill()

t.goto(-35,-90)
t.goto(35,-90)
t.goto(0,20)

t.end_fill()
sleep (1)
t.clear ()
# ------------------------ Botswana 400 xp


t.pu()
t.goto(-200,120)
t.pd()

t.color("black")
t.fillcolor("#75AADB")

t.begin_fill()

for cont in range(2):
    t.fd(400)
    t.rt(90)
    t.fd(240)
    t.rt(90)

t.end_fill()
t.pu()
t.goto(-200,20)
t.pd()

t.fillcolor("white")

t.begin_fill()

for cont in range(2):
    t.fd(400)
    t.rt(90)
    t.fd(15)
    t.rt(90)

t.end_fill()

t.pu()
t.goto(-200,5)
t.pd()

t.fillcolor("black")

t.begin_fill()

for cont in range(2):
    t.fd(400)
    t.rt(90)
    t.fd(50)
    t.rt(90)

t.end_fill()


t.pu()
t.goto(-200,-45)
t.pd()

t.fillcolor("white")

t.begin_fill()

for cont in range(2):
    t.fd(400)
    t.rt(90)
    t.fd(15)
    t.rt(90)

t.end_fill()
sleep (1)
t.clear ()
# ------------------------ Bahamas 450 xp

t.pu()
t.goto(-200,120)
t.pd()

t.color("black")
t.fillcolor("#00ABC9")
t.begin_fill()

for cont in range(2):
    t.fd(400)
    t.rt(90)
    t.fd(80)
    t.rt(90)

t.end_fill()


t.pu()
t.goto(-200,40)
t.pd()

t.fillcolor("#FFD100")
t.begin_fill()

for cont in range(2):
    t.fd(400)
    t.rt(90)
    t.fd(80)
    t.rt(90)

t.end_fill()


t.pu()
t.goto(-200,-40)
t.pd()

t.fillcolor("#00ABC9")
t.begin_fill()

for cont in range(2):
    t.fd(400)
    t.rt(90)
    t.fd(80)
    t.rt(90)

t.end_fill()


t.pu()
t.goto(-200,120)
t.pd()

t.fillcolor("black")
t.begin_fill()

t.goto(-200,-120)
t.goto(-40,0)
t.goto(-200,120)

t.end_fill()
sleep (1)
t.clear ()
# ------------------------ Sudão 5000000000000000000xp


t.pu()
t.goto(-200,120)
t.pd()

t.color("black")
t.fillcolor("red")
t.begin_fill()

for cont in range(2):
    t.fd(400)
    t.rt(90)
    t.fd(80)
    t.rt(90)

t.end_fill()

t.pu()
t.goto(-200,40)
t.pd()

t.fillcolor("white")
t.begin_fill()

for cont in range(2):
    t.fd(400)
    t.rt(90)
    t.fd(80)
    t.rt(90)

t.end_fill()

# Faixa preta
t.pu()
t.goto(-200,-40)
t.pd()

t.fillcolor("black")
t.begin_fill()

for cont in range(2):
    t.fd(400)
    t.rt(90)
    t.fd(80)
    t.rt(90)

t.end_fill()

t.pu()
t.goto(-200,120)
t.pd()

t.fillcolor("green")
t.begin_fill()

t.goto(-200,-120)
t.goto(-40,0)
t.goto(-200,120)

t.end_fill()



sleep (1)
t.clear ()


mainloop()