#usar a tabela ASC


def valida_email(email):
    return email [-8:] == '@puc.com'

def verifica_maiucu (senha):
    for char in senha:
        if 'A' <=  char <= 'Z':
            return True
    return False

def valida_senha (senha):
    possui8Tam = len(senha) >= 8
    possuiMaiucu = verifica_maiucu (senha)
    possuiMinuscu = verifica_Minuscu (senha)
    possuiNum = verifica_NUmebro (senha)
    
    return  possui8Tam and possuiMaiucu

print (valida_senha("FFF@15615"))


# cripto
def criptografa_cesar (senha):
    sovaSenha = " "
    for char in senha:
        if 'a' < char <= 'z':
        posCharOrig= ord(char) - ord('a') #ord + o carachter ver a ordem dele na TABELA ASC
        novaPosi = (posCharOrig +3) %26 + ord ('a')
        charCript = Chr (novaPosi)
        novaSenha += charCript
        elif 'A' < char <= 'Z':
        posCharOrig= ord(char) - ord('A') #ord + o carachter ver a ordem dele na TABELA ASC
        novaPosi = (posCharOrig +3) %26 + ord ('A')
        charCript = Chr (novaPosi)
        novaSenha += charCript
        else:
        novaSenha += char
# para descri é so diminuir, ao inves de ser + usa o -