import requests
import json
import time


    
def logar():
    global header
    global usuario
    global senha


    ''' Inserindo login e senha '''
    ''' Lendo o arquivo txt config-mensagens '''
    txt = open("canais.txt", "r", encoding="utf-8")
    mensagem_login = txt.readlines()
    usuario = mensagem_login[2].replace('\n','').split('= ')[1] 
    senha = mensagem_login[3].replace('\n','').split('= ')[1]


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
    URL_FORNECEDOR = f'https://pi.njoybingo.com/game.do?token={uuid_usuário}&pn=meskbet&lang=pt&game=PRPLAY-1301&type=CHARGED'
    location = requests.get(URL_FORNECEDOR, allow_redirects=False).headers.get('location')
    
    #SEGUNDO LOCATION
    location2 = requests.get(location, allow_redirects=False).headers.get('location')
    

    header = {
    "Content-Type": "application/json",
    "referer": "https://mesk.bet/"
    }

    #Usando o Token gerado pelo FORNECEDOR para Acessar o GAME e pegar o TOKEN para ter acesso aos dados do GAME
    #URL_GAME = f'https://wac.paconassa.com/?game=LUVASG&token={token_fornecedor}&pn=meskbet&lang=pt&type=CHARGED'
    jsession_id = requests.get(location2, allow_redirects=False).headers.get('location').split('JSESSIONID=')[1].split('&')[0]

    return jsession_id


def processo_pegar_jsessionid():
        global token_autorizacao, uuid_usuário, username, jsession_id

        token_autorizacao = logar()
        uuid_usuário, username = puxar_dados_acesso(token_autorizacao)
        jsession_id = acessar_game(uuid_usuário)



if __name__=='__main__':

        processo_pegar_jsessionid()
        ult_resultado = 0

        while True:
                try:
                        url_spaceman = f'https://gs9.pragmaticplaylive.net/api/ui/statisticHistory?tableId=spacemanyxe123nh&numberOfGames=500&JSESSIONID={jsession_id}&game_mode=lobby_desktop'
                        session = requests.session()
                        response = session.get(url_spaceman)
                        historico_velas = json.loads(response.content)
                        resultado = historico_velas["history"][0]["gameResult"]

                        if resultado != ult_resultado:
                                resultado = historico_velas["history"][0]["gameResult"]
                                print(resultado)
                                ult_resultado = resultado

                        time.sleep(2)
                
                except:
                        processo_pegar_jsessionid()

