from websocket import create_connection
import json
import requests


def websocket():
    header = {
        
        "Host": "nodeprod-06.globalgames.io:32000",
        "Connection": "Upgrade",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Upgrade": "websocket",
        "Origin": "https://gg-production.globalgames.io",
        "Sec-WebSocket-Version": "13",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Sec-WebSocket-Key": "n9nusYhz+xCWIF1y0J8BfA==",
        "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits"

    }


    URL = f"wss://socketgames-kube.evoplay.games/listener-goblinrun/416/447/websocket"

    ws = create_connection(URL)

    ws.send(json.dumps([json.dumps(header)]))

    cont = 0
    ultimo_result = ''
    ultimo_valor_armazenado = ''

    while True:

            ultimo_result = ws.recv()

            if 'crash' in ultimo_result:
                try:
                    print(str(json.loads(ultimo_result)['data']['multiplier']))
                except:
                    pass

            ultimo_valor_armazenado = ultimo_result



def creat_user():
    url = f"https://stelar-affiliate.estrelabet.com/user"

    payload = {
        "firstName": "Victor",
        "lastName": "Rodrigues",
        "email": "victor.o.rodrigues11@gmail.com",
        "password": "Fordbracom2022"
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.text)


def authenticate():
    url = f"https://stelar-affiliate.estrelabet.com/auth"

    payload = {

        "email": "Fordbracom2022",
        "password": "Fordbracom2022"
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, json=payload, headers=headers)
    token = response.json()["data"]["bearerToken"]
    return token


def rounds(token):
    url = "https://stelar-affiliate.estrelabet.com/round"

    headers = {
        'Authorization': f'Bearer {token}'
              }

    response = requests.get(url, headers=headers)
    data = response.json()
    dados = []
    dados = data["data"]
    resultados = []
    dados.reverse()
    dados = dados[0:30]
    for i in dados:
        resultados.append(i["multiplier"])
        
    return resultados[0:20]

#creat_user()
token = authenticate()
check_results = []

while True:
    results = rounds(token)
    if check_results != results:
        check_results = results
        print(results)

    print(111)
    websocket(token)




