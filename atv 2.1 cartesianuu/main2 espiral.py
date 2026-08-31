from turtle import *

#ESPIRAL EXP

t = Turtle() 
t.shape ("turtle")



t.pu()
t.goto(200, -200)
t.pd()

t.fd(20)
t.rt(90)

t.fd(40)
t.rt(90)

t.fd(60)
t.rt(90)

t.fd(80)
t.rt(90)

t.fd(100)
t.rt(90)

t.fd(120)
t.rt(90)

t.fd(140)
t.rt(90)

# t.fd(90)
# t.rt(90)

# t.fd(100)


t.end_fill()

mainloop()