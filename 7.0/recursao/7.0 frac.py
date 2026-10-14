



#sobbre recursao(iôiÔ)
def mostrar_subtrings_for(string):
    for i in  range(len(string)): # poderia usar o while ate ficar fazia 

        print (string)
        string = string [:-1]

#de outro jeito
def mostra_substrings_while (string):
    while len(string) !=0:
        print (string)
        string = string [:-1]

def mostra_substrings(string):
    if string == '':
        print('cheguei no caso base!')
        return
    print(f'chamando a função para {string}')
    mostra_substrings(string[:-1])
    print(f'retornando a função para {string}')
    return

mostrar_subtrings_for('abacaxi')
mostra_substrings_while('abacate')
mostra_substrings('morango')


