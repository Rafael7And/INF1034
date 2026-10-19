

lista_nums = [
    100,120,130,120,150,100,160,200,190,110,115,125,135,170,130
]

maior_num = max(lista_nums)
menor_num = min(lista_nums)

qnt_faixas = 7
almplitude = maior_num - menor_num
tam_faixa =almplitude // qnt_faixas

print (maior_num,menor_num,almplitude,tam_faixa)

lista_qnt_por_faixa = [0] * qnt_faixas


for i in range(len(lista_nums)):
    #if lista_nums[i] == maior_num:

    for j in range (len(lista_qnt_por_faixa)):
        lim_inf = menor_num + tam_faixa * j 
        lim_sup = lim_inf + tam_faixa
        # print(lim_inf, lim_sup, lista_nums)
    if lim_inf <= lista_nums [i] < lim_sup:
        lista_qnt_por_faixa [j] += 1
        break

print(lim_inf,lim_sup, lista_nums )



# 
# lista_nums = [
#     100, 120, 130, 120, 150, 100, 160, 200,
#     190, 110, 115, 125, 135, 170, 130
# ]

# maior_num = max(lista_nums)
# menor_num = min(lista_nums)

# qnt_faixas = 5
# amplitude = maior_num - menor_num
# tam_faixa = amplitude // qnt_faixas

# print(maior_num, menor_num, amplitude, tam_faixa)

# lista_qnt_por_faixa = [0] * qnt_faixas

# for i in range(len(lista_nums)):
#     for j in range(len(lista_qnt_por_faixa)):
#         lim_inf = menor_num + tam_faixa * j
#         lim_sup = lim_inf + tam_faixa

#         if lim_inf <= lista_nums[i] < lim_sup:
#             lista_qnt_por_faixa[j] += 1
#             break

# print(lista_qnt_por_faixa)
# 