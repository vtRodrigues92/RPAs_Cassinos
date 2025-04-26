import requests
import json
import time
from websocket import create_connection
    

def logar():
    global header
    global usuario
    global senha


    ''' Inserindo login e senha '''
    ''' Lendo o arquivo txt config-mensagens '''
    #txt = open("canais.txt", "r", encoding="utf-8")
    #mensagem_login = txt.readlines()
    #usuario = mensagem_login[2].replace('\n','').split('= ')[1] 
    #senha = mensagem_login[3].replace('\n','').split('= ')[1]

    usuario = 'MuriloR1895'
    senha = 'flamengo77'


    URL = 'https://backoffice.mesk.bet/api/auth/login'

    header = {
    'Content-Type': 'application/json'
    }

    payload = {"email":usuario,
               "password":senha}
    
    token = requests.post(URL, headers=header, json=payload).json()['token']

    return token


def puxar_dados_acesso(token_autorizacao):
    global username

    header = {
                'Content-Type': 'application/json',
                "authorization": f"bearer {token_autorizacao}"
                }
    
    payload = {"email":usuario,
               "password":senha
               }
    

    URL = 'https://backoffice.mesk.bet/api/auth/me'

    uuid_usuário = requests.post(URL, headers=header, json=payload).json()['player']['uuid']
    username = requests.post(URL, headers=header, json=payload).json()['username']

    return uuid_usuário, username


def acessar_game(uuid_usuário):

    #LOCATION PRAGMATICPLAY
    URL_FORNECEDOR = f'https://pi.njoybingo.com/game.do?token={uuid_usuário}&pn=meskbet&lang=pt&game=EVOLUTION-roulette-7x0b1tgh7agmf6hv&type=CHARGED'
    location = requests.get(URL_FORNECEDOR, allow_redirects=False).headers.get('location')
    
    #SEGUNDO LOCATION
    EVOSESSIONID = requests.get(location, cookies={"EVOSESSIONID": ""},allow_redirects=False).cookies._cookies['wac.evo-games.com']['/']['EVOSESSIONID'].value
    
    return EVOSESSIONID


def processo_pegar_jsessionid():
        global token_autorizacao, uuid_usuário, username, jsession_id

        token_autorizacao = logar()
        uuid_usuário, username = puxar_dados_acesso(token_autorizacao)
        EVOSESSIONID = acessar_game(uuid_usuário)

        return EVOSESSIONID



def conectar_websocket(EVOSESSIONID):
    global URL
    global ws
    global cont
    global ultimo_result
    global ultimo_valor_armazenado


    header = {
      
    "Host": "wac.evo-games.com",
    "Connection": "Upgrade",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Upgrade": "websocket",
    "Origin": "https://wac.evo-games.com",
    "Sec-WebSocket-Version": "13",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cookie": f"cdn=https://static.egcdn.com; lang=bp; locale=pt-BR; EVOSESSIONID={EVOSESSIONID}",
    "Sec-WebSocket-Key": "/zq4yO2qA5boRFM7PJzHZw==",
    "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits"

    }


    URL = f'wss://wac.evo-games.com/public/roulette/player/game/7x0b1tgh7agmf6hv/socket?messageFormat=json&instance=slnjqn-q46vrmxdeigoqaco-7x0b1tgh7agmf6hv&tableConfig=&EVOSESSIONID={EVOSESSIONID}&client_version=6.20230525.64718.25696-1e87816ab7'
    
    ws = create_connection(URL)

    ws.send(json.dumps([json.dumps(header)]))

    cont = 0
    ultimo_result = ''
    ultimo_valor_armazenado = ''



if __name__=='__main__':

        EVOSESSIONID = processo_pegar_jsessionid()
        conectar_websocket(EVOSESSIONID)
        lista_resultados = []

        while True:
            try:

                ultimo_result = ws.recv()
                
                if 'roulette.winSpots' in ultimo_result:
                    try:

                        ultimo_resultado = json.loads(ultimo_result)['args']['code']
                        lista_resultados.append(ultimo_resultado)
                        print(lista_resultados)
                        
                    except:
                        ultimo_valor_armazenado = ultimo_result
                        continue
                else:
                    ultimo_valor_armazenado = ultimo_result
                    continue
            
            except:continue
