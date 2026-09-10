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
###############  FUNÇAO TRIANGULO
def desenha_triangulo(x1, y1, x2, y2, x3, y3, cor):
    t.pu()
    t.goto(x1, y1)
    t.pd()

    t.fillcolor(cor)
    t.begin_fill()

    t.goto(x2, y2)
    t.goto(x3, y3)
    t.goto(x1, y1)

    t.end_fill()
############################# função estrela(patrick)
def desenha_estrela(x,y,lado,cor):
    t.pu()
    t.goto(x,y)
    t.pd()

    t.color(cor)
    t.fillcolor(cor)
    t.begin_fill()

    for cont in range(5):
        t.fd(lado)
        t.rt(144)

    t.end_fill()



#----------------bandeira italia -------

def desenha_italia():
    desenha_retangulo(-150,200,150,300, '#028801')
    desenha_retangulo(-300,200,150,300, '#F50102')
    desenha_retangulo(00,200,150,300, '#FAFAFA')

desenha_italia()
sleep(2)
t.clear()

# #----------------bandeira françaa -------
def desenha_frança():
    desenha_retangulo(-150,200,150,300, '#002153')
    desenha_retangulo(-300,200,150,300, '#FAFAFA')
    desenha_retangulo(000,200,150,300, '#CF0921')

desenha_frança()
sleep(5)
t.clear()
#----------------bandeira sudao -------


def desenha_sudao():
    desenha_retangulo(-200,120,400,80,"red")
    desenha_retangulo(-200,40,400,80,"white")
    desenha_retangulo(-200,-40,400,80,"black")
    desenha_triangulo(-200,120,-200,-120,-40,0,"green")

desenha_sudao()

sleep(5)
t.clear()
#########----------- bahamas
def desenha_bahamas():
    desenha_retangulo(-200,120,400,80,"#00ABC9")
    desenha_retangulo(-200,40,400,80,"#FFD100")
    desenha_retangulo(-200,-40,400,80,"#00ABC9")

    desenha_triangulo(-200,120,-200,-120,-40,0,"black")
desenha_bahamas()

sleep(5)
t.clear()

######- costa pobre------
def desenha_costa_rica():
    desenha_retangulo(-200,120,400,40,"blue")     
    desenha_retangulo(-200,80,400,40,"white")     
    desenha_retangulo(-200,40,400,80,"red")      
    desenha_retangulo(-200,-40,400,40,"white")    
    desenha_retangulo(-200,-80,400,40,"blue")     

desenha_costa_rica()

sleep(5)
t.clear()


# ---------------- Guiné-Bissau ---------------- chatao esse da estrela

def desenha_guine_bissau():
    desenha_retangulo(-200,120,100,240,"red")
    desenha_retangulo(-100,120,300,120,"yellow")
    desenha_retangulo(-100,0,300,120,"green")
    # Estrela 
    desenha_estrela(-165,30,55,"black")
desenha_guine_bissau()

t.pu()
t.goto(-147,30)
t.pd()

t.fillcolor("black")
t.begin_fill()

for cont in range(5):
    t.fd(18)
    t.rt(72)
t.end_fill ()
sleep(5)
t.clear()

###################FINLANDIA
def desenha_finlandia():
    desenha_retangulo (-200,120,400,240,'white')
    desenha_retangulo(-80,120,60,240,"blue")
    desenha_retangulo(-200,20,400,60,"blue")

desenha_finlandia()
sleep(5)
t.clear()

###################- SUiças
def desenha_suiça():
    desenha_retangulo(-120,120,240,240,'red')
    desenha_retangulo(-20,80,40,160,'white')
    desenha_retangulo(-80,20,160,40,'white')

desenha_suiça()
sleep(5)
t.clear()

######SAnta lucia ---------------

def desenha_santa_lucia():
    desenha_retangulo(-200,120,400,240,"#66B5E3")
    desenha_triangulo(0,100,-80,-100,80,-100,"white")
    desenha_triangulo(0,80,-55,-70,55,-70,"black")
    desenha_triangulo(0,10,-30,-70,30,-70,"gold")

desenha_santa_lucia()
sleep(5)
t.clear()

 # ------------------------ Botswana 400 xp
def desenha_botswana():
    desenha_retangulo(-200,120,400,240,"#75AADB")
    desenha_retangulo(-200,40,400,15,"white")
    desenha_retangulo(-200,25,400,50,"black")
    desenha_retangulo(-200,-25,400,15,"white")
desenha_botswana()
sleep(5)
t.clear()

# ------------------------ Palestina

def desenha_palestina():
    desenha_retangulo(-200,120,400,80,"black")
    desenha_retangulo(-200,40,400,80,"white")
    desenha_retangulo(-200,-40,400,80,"green")
    desenha_triangulo(-200,120,-200,-120,-40,0,"red")
desenha_palestina()
sleep(5)
t.clear()

## ------------------------ Maurício

def desenha_mauricio():
    desenha_retangulo(-200,120,400,60,"red")
    desenha_retangulo(-200,60,400,60,"blue")
    desenha_retangulo(-200,0,400,60,"yellow")
    desenha_retangulo(-200,-60,400,60,"green")
desenha_mauricio()
sleep(5)
t.clear()
mainloop()








################## EXTRA ##################<<<<

opcao =textinput("Bandeiras", "Digite: italia, frança, sudao,Maurício,Palestina,Botswana,SAnta lucia,SUiças, costa pobre,Guiné-Bissau,bahamas,FINLANDIA,")

if opcao == "italia":
    desenha_italia()

elif opcao == "frança":
    desenha_frança()

elif opcao == "Mauricio":
    desenha_mauricio()
elif opcao == "palestina":
    desenha_palestina()
elif opcao == " botswana":
     desenha_botswana()

elif opcao == "santa lucia":
    desenha_santa_lucia()
elif opcao == "suiça":
    desenha_suiça()
elif opcao == "finlandia":
    desenha_finlandia()
elif opcao == "guine bissau":
    desenha_guine_bissau()
elif opcao == "costa rica":
    desenha_costa_rica()
elif opcao == 'bahamas':
    desenha_bahamas()
elif opcao == 'sudao':
    desenha_sudao()


