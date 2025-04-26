import requests
import json
import ast

url = 'https://blaze.com/api/crash_games/recent'

lista_resultados = []

historico_resultados = requests.get(url).json()

for crash in reversed(historico_resultados):
    vela = crash["crash_point"]
    if vela == 0:
        vela = 1.00
    
    lista_resultados.append(vela)


print(lista_resultados)
