#usar a tabela ASC
from pygame import *
from casinha import casa



def valida_email(email):
    print("Final do email:", repr(email[-8:]))
    return email [-8:] == '@puc.com'

# print(valida_email("uzumakigondor@puc.com"))

def verifica_maiucu (senha):
    for char in senha:
        if 'A' <=  char <= 'Z':
            return True
    return False

def verifica_Minuscu (senha):
    for char in senha:
        if 'a' <= char <='z':
            return True
    return False

def verifica_numero (senha):
    for numerus in senha:
        if '0' <= numerus <='9':
            return True
    return False

# print (verifica_maiucu('Aff@156'))
# print (verifica_Minuscu('rigDADAjg'))
# print (verifica_numero('fwf456'))

def valida_senha (senha):
    possui8Tam = len(senha) >= 8
    possuiMaiucu = verifica_maiucu (senha)
    possuiMinuscu = verifica_Minuscu (senha)
    possuiNum = verifica_numero (senha)
    
    return  possui8Tam and possuiMaiucu and possuiNum and possuiMinuscu

# print("\nTestando a 'valida_senha':")
# print(valida_senha("ABc@1234"))
# print(valida_senha("BFSA@1234"))
# print(valida_senha("dsfsef@1234"))
# print(valida_senha("dkfmcef@ajgf"))
# print(valida_senha("Def@123"))
# print (valida_senha("FFF@1dd5615"))


# cripto
def criptografa_cesar (senha):
    novaSenha = ""
    for char in senha:
        if 'a' <= char <= 'z':
            posCharOrig= ord(char) - ord('a') #ord + o carachter ver a ordem dele na TABELA ASC
            novaPosi = (posCharOrig +3) %26 + ord ('a')
            charCript = chr (novaPosi)
            novaSenha += charCript
        elif 'A' <= char <= 'Z':
            posCharOrig= ord(char) - ord('A') #ord + o carachter ver a ordem dele na TABELA ASC
            novaPosi = (posCharOrig +3) %26 + ord ('A')
            charCript = chr (novaPosi)
            novaSenha += charCript
        else:
             novaSenha += char
    return novaSenha


#usando a carta DE REVERSO NA CRIPTOGRAFIA DO CEZINHHA DO PNEU

def descriptografa_cesar(senha):
    novaSenha = ""

    for char in senha:
        if 'a' <= char <= 'z':
            posCharOrig = ord(char) - ord('a')
            novaPosi = (posCharOrig - 3) % 26 + ord('a')
            charCript = chr(novaPosi)
            novaSenha += charCript

        elif 'A' <= char <= 'Z':
            posCharOrig = ord(char) - ord('A')
            novaPosi = (posCharOrig - 3) % 26 + ord('A')
            charCript = chr(novaPosi)
            novaSenha += charCript

        else:
            novaSenha += char

    return novaSenha

# print (criptografa_cesar('fihgi@HH4565654UJIOF'))
# para descri é so diminuir, ao inves de ser + usa o -



init()

screen = display.set_mode((800, 600))
fonte = font.Font("tngani.ttf", 30)

email = ""
senha = ""
campo = 1
mensagem = ""
loginValido = False
rodando = True

while rodando:

    for ev in event.get():

        if ev.type == QUIT:
            rodando = False

        if ev.type == KEYDOWN:

            if ev.key == K_BACKSPACE:
                if campo == 1:
                    email = email[:-1]
                else:
                    senha = senha[:-1]

            elif ev.key == K_RETURN:
                if campo == 1:
                    campo = 2
                else:
                    print("Email digitado:", email)
                    print("Email valido:", valida_email(email))
                    print("Senha digitada:", senha)
                    print("Senha valida:", valida_senha(senha))

                    if valida_email(email) and valida_senha(senha):
                        print(criptografa_cesar(senha))
                        loginValido = True
                        rodando = False
                    else:
                        mensagem = "Dados errados!"

            else:
                if campo == 1:
                    email = email + ev.unicode
                else:
                    senha = senha + ev.unicode

    screen.fill("#5DA2C4")

    texto = fonte.render("KHAZAD - DUM", True, "black")
    screen.blit(texto, (330, 80))

    texto = fonte.render("E-mail: " + email, True, "black")
    screen.blit(texto, (100, 180))

    texto = fonte.render("Digite, amigo e entre : " + "*" * len(senha), True, "black")
    screen.blit(texto, (100, 280))

    texto = fonte.render(mensagem, True, "red")
    screen.blit(texto, (100, 400))

    display.update()

if loginValido:
    casa()

quit()