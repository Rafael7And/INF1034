from turtle import *

#sobbre recursao(iôiÔ)
# def mostrar_subtrings_for(string):
#     for i in  range(len(string)): # poderia usar o while ate ficar fazia 

#         print (string)
#         string = string [:-1]

# #de outro jeito
# def mostra_substrings_while (string):
#     while len(string) !=0:
#         print (string)
#         string = string [:-1]

# def mostra_substrings(string):
#     if string == '':
#         print('cheguei no caso base!')
#         return
#     print(f'chamando a função para {string}')
#     mostra_substrings(string[:-1])
#     print(f'retornando a função para {string}')
#     return

# mostrar_subtrings_for('abacaxi')
# mostra_substrings_while('abacate')
# mostra_substrings('morango')

# ------------------------ facil


# t = Turtle()
# t.speed(3)

# # 1 triângulo
# for i in range(3):
#     t.forward(100)
#     t.left(120)


# t.penup()
# t.goto(150, 0)
# t.pendown()

# #  triângulo 2
# for i in range(3):
#     t.forward(70)
#     t.left(120)


# t.penup()
# t.goto(260, 0)
# t.pendown()

# #  triângulo 3
# for i in range(3):
#     t.forward(40)
#     t.left(120)

# done()

# ---------------- facil 2

# # raios
# t = Turtle()
# t.speed(3)
# for i in range(8):
#     t.penup()
#     t.goto(0, 0)
#     t.pendown()

#     t.forward(70)
#     t.backward(70)
#     t.right(45)

# done()

#----------------- MEDIO 1

# t = Turtle()
# t.speed(5)

# def circulos(raio):
#     if raio <= 0:
#         return

#     t.penup()
#     t.goto(0, -raio)
#     t.pendown()
#     t.circle(raio)

#     circulos(raio - 10)

# circulos(80)

# done()


# ------------dificil
t = Turtle()
t.speed(0)

def bracos(tamanho, nivel, angulo):
    if nivel == 0:
        return

    t.forward(tamanho)
    posicao = t.position()
    direcao = t.heading()

    t.left(angulo)
    bracos(tamanho / 2, nivel - 1, angulo)
    t.goto(posicao)
    t.setheading(direcao)

    t.right(angulo)
    bracos(tamanho / 2, nivel - 1, angulo)
    t.goto(posicao)
    t.setheading(direcao)

    t.right(angulo)
    bracos(tamanho / 2, nivel - 1, angulo)
    t.goto(posicao)
    t.setheading(direcao)

bracos(80, 5, 40)

done()
