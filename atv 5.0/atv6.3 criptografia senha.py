#usar a tabela ASC


def valida_email(email):
    return email [-8:] == '@puc.com'

print(valida_email("uzumakigondor@puc.com"))

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

print (verifica_maiucu('Aff@156'))
print (verifica_Minuscu('rigjejg'))
print (verifica_numero('fwf456'))

def valida_senha (senha):
    possui8Tam = len(senha) >= 8
    possuiMaiucu = verifica_maiucu (senha)
    possuiMinuscu = verifica_Minuscu (senha)
    possuiNum = verifica_numero (senha)
    
    return  possui8Tam and possuiMaiucu and possuiNum and possuiMinuscu

print("\nTestando a 'valida_senha':")
print(valida_senha("ABc@1234"))
print(valida_senha("BFSA@1234"))
print(valida_senha("dsfsef@1234"))
print(valida_senha("dkfmcef@ajgf"))
print(valida_senha("Def@123"))
print (valida_senha("FFF@1dd5615"))


# cripto
def criptografa_cesar (senha):
    novaSenha = ""
    for char in senha:
        if 'a' < char <= 'z':
            posCharOrig= ord(char) - ord('a') #ord + o carachter ver a ordem dele na TABELA ASC
            novaPosi = (posCharOrig +3) %26 + ord ('a')
            charCript = chr (novaPosi)
            novaSenha += charCript
        elif 'A' < char <= 'Z':
            posCharOrig= ord(char) - ord('A') #ord + o carachter ver a ordem dele na TABELA ASC
            novaPosi = (posCharOrig +3) %26 + ord ('A')
            charCript = chr (novaPosi)
            novaSenha += charCript
        else:
             novaSenha += char
    return novaSenha



print (criptografa_cesar('fihgi@HH4565654UJIOF'))
# para descri é so diminuir, ao inves de ser + usa o -




