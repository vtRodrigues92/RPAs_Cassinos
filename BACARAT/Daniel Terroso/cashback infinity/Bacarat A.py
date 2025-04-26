import time
from datetime import datetime, timedelta
import telebot
from telegram.ext import *
from telebot import *
import ast
import os
from websocket import create_connection
import json
import requests
#from fake_useragent import UserAgent
import urllib3
import ssl
import certifi

print()
print('                                #################################################################')
print('                                #####################   BOT BACCARAT   ##########################')
print('                                #################################################################')
print('                                ##################### SEJA BEM VINDO ############################')
print('                                #################################################################')
print('                                ############# DESENVOLVIDO POR VICTOR RODRIGUES #################')
print('                                #################################################################\n')
print('Versão = 1.0.0')
print('Ambiente: Produção\n\n\n')

ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# THREAD PARA ENVIAR POST PARA API DE RESULTADOS
class enviarPostAPIResultados(threading.Thread):
    def __init__(self, winner):
        self.winner = winner
        threading.Thread.__init__(self)
    
    def run(self):
        try:

            url_api_resultados = 'https://fb.hackergames.com.br/call.php'

            payload = {

                        "game": "baccarat-a",
                        "winner":self.winner

                        }

            requests.post(url_api_resultados, headers=headers, json=payload)

            print('Post API Resultados enviado com sucesso.')

        except Exception as e:
            print(e)



# THREAD PARA ENVIAR POST PARA API DE ENTRADAS
class enviarPostAPI(threading.Thread):
    def __init__(self, texto, gale, winner):
        self.texto = texto
        self.gale = gale
        self.winner = winner
        threading.Thread.__init__(self)
    
    def run(self):
        try:
        
            payload = {
                    
                        "content": self.texto,
                        "game": "baccarat-a",
                        "gale":self.gale,
                        "winner":self.winner

                        }

            requests.post(url, headers=headers, json=payload)

            print('Post API Entradas enviado com sucesso.')

        except Exception as e:
            print(e)



# GERA TXT DO PLACAR
def placar():
    global placar_win
    global placar_semGale
    global placar_gale1, placar_gale3, placar_gale4, placar_gale5, placar_gale6, placar_gale7, placar_gale8, placar_gale9, placar_gale10
    global placar_gale2
    global placar_loss
    global placar_geral
    global asserividade
    global data_hoje
    global placar_maior

    data_hoje = datetime.today().strftime('%d-%m-%Y')
    arquivos_placares = os.listdir(r"placar/")

    if f'{data_hoje}.txt' in arquivos_placares:
        # Carregar arquivo de placar
        with open(f"placar/{data_hoje}.txt", 'r') as arquivo:
            try:

                arq_placar = arquivo.readlines()
                placar_win = int(arq_placar[0].split(',')[1])
                placar_semGale = int(arq_placar[1].split(',')[1])
                placar_gale1 = int(arq_placar[2].split(',')[1])
                placar_gale2 = int(arq_placar[3].split(',')[1]) 
                placar_loss = int(arq_placar[4].split(',')[1])
                placar_geral = int(placar_win) + int(placar_loss)
                asserividade = arq_placar[5].split(',')[1]+"%"
                placar_maior = int(arq_placar[6].split(',')[1])
                placar_gale3 = int(arq_placar[7].split(',')[1])
                placar_gale4 = int(arq_placar[8].split(',')[1])
                placar_gale5 = int(arq_placar[9].split(',')[1])
                placar_gale6 = int(arq_placar[10].split(',')[1])
                placar_gale7 = int(arq_placar[11].split(',')[1])
                placar_gale8 = int(arq_placar[12].split(',')[1])
                placar_gale9 = int(arq_placar[13].split(',')[1])
                placar_gale10 = int(arq_placar[14].split(',')[1])
            
            except:
                pass

            
    else:
        # Criar um arquivo com a data atual
        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
            arquivo.write("win,0\nsg,0\ng1,0\ng2,0\nloss,0\nass,0\nmaior,0\ng3,0\ng4,0\ng5,0\ng6,0\ng7,0\ng8,0\ng9,0\ng10,0")

        # Ler o arquivo de placar criado
        with open(f"placar/{data_hoje}.txt", 'r') as arquivo:
            try:

                arq_placar = arquivo.readlines()
                placar_win = int(arq_placar[0].split(',')[1])
                placar_semGale = int(arq_placar[1].split(',')[1])
                placar_gale1 = int(arq_placar[2].split(',')[1])
                placar_gale2 = int(arq_placar[3].split(',')[1])
                placar_loss = int(arq_placar[4].split(',')[1])
                placar_geral = int(placar_win) + int(placar_loss)
                asserividade = arq_placar[5].split(',')[1]+"%"
                placar_maior = int(arq_placar[6].split(',')[1])
                placar_gale3 = int(arq_placar[7].split(',')[1])
                placar_gale4 = int(arq_placar[8].split(',')[1])
                placar_gale5 = int(arq_placar[9].split(',')[1])
                placar_gale6 = int(arq_placar[10].split(',')[1])
                placar_gale7 = int(arq_placar[11].split(',')[1])
                placar_gale8 = int(arq_placar[12].split(',')[1])
                placar_gale9 = int(arq_placar[13].split(',')[1])
                placar_gale10 = int(arq_placar[14].split(',')[1])
            
            
            except:
                pass



# ENVIA PLACAR CANAIS TELEGRAM
def envia_placar():

    try:
        placar()

        ''' Lendo o arquivo txt canais '''
        txt = open("arquivos_txt/canais.txt", "r", encoding="utf-8")
        arquivo = txt.readlines()
        canais = arquivo[12].replace('canais= ','').replace('\n','')
        canais = ast.literal_eval(canais) # Convertendo string em dicionario 

        ''' Enviando mensagem Telegram '''
        try:
            for key, value in canais.items():
                try:
                    globals()[f'placar_{key}'] = bot.send_message(key,\
        "📊 Placar Atual do dia "+data_hoje+":\n\
        =====================\n\
        TOTAL LOSS - "+str(placar_win)+"\n\
        LOSS S/ GALE - "+str(placar_semGale)+"\n\
        LOSS GALE1 - "+str(placar_gale1)+"\n\
        LOSS GALE2 - "+str(placar_gale2)+"\n\
        LOSS GALE3 - "+str(placar_gale3)+"\n\
        LOSS GALE4 - "+str(placar_gale4)+"\n\
        LOSS GALE5 - "+str(placar_gale5)+"\n\
        LOSS GALE6 - "+str(placar_gale6)+"\n\
        LOSS GALE7 - "+str(placar_gale7)+"\n\
        LOSS GALE8 - "+str(placar_gale8)+"\n\
        LOSS GALE9 - "+str(placar_gale9)+"\n\
        LOSS GALE10 - "+str(placar_gale10)+"\n\
        LOSS MAIOR QUE 10 - "+str(placar_maior)+"\n\
        =====================")
        #Variavel Dinâmica
                except:
                    pass

        except:
            pass

    except Exception as a:
        logger.error('Exception ocorrido no ' + repr(a))
        #placar = bot.reply_to(message,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%", reply_markup=markup)
        pass


# VALIDADOR DE DATA
def validaData():
    global data_resultado
    global reladiarioenviado
    global horario_atual

    data_hoje = datetime.today()
    subtrai_dia = timedelta(days=-1)
    data_ontem = data_hoje + subtrai_dia
    data_resultado = data_ontem.strftime('%d/%m/%Y')
    horario_atual = datetime.today().strftime('%H:%M')

    # Condição que zera o placar quando o dia muda
    if horario_atual == '00:00' and reladiarioenviado == 0:
        placar()
        reladiarioenviado +=1

    # Condição que zera o placar quando o dia muda
    if horario_atual == '00:01' and reladiarioenviado == 1:
        reladiarioenviado = 0



def inicio():
    global horario_inicio
    global lista_resultados
    global url
    global headers

    url = "https://fb.hackergames.com.br/firebase.php"
    
    headers = {
    'Content-Type': 'application/json'
    }


    horario_inicio = datetime.now()
    lista_resultados = []

        
def pegar_evosessionid():
    
    while True:

        try:

            #LOGIN
            URL = 'https://cashbackinfinity.com.br/cassino/api/v1/login.php'

            header = {
            'Content-Type': 'application/json',
            "Origin":"https://cash-back-infinity.web.app",
            "Referer":"https://cash-back-infinity.web.app/",
            }

            payload = '{"email":"magnatametodos@gmail.com","password":"10203040","device":"desktop","deviceType":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}'
            
            response = requests.post(URL, headers=header, data=payload, verify=False)
            
            access_token = response.json()['access_token']
            token = response.json()['token']

            print(access_token, token)    

            #### ENTRANDO NO GAME
            #REQUISIÇÃO1 #IFRAME
            URL = 'https://cashbackinfinity.com.br/cassino/api/v1/game.php'

            payload = {"access_token":access_token,
                        "code":"1000012",
                        "token":token
                    }

            header = {
            'Content-Type': 'application/json',
            "Origin":"https://cash-back-infinity.web.app",
            "Referer":"https://cash-back-infinity.web.app/",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            }
            
            response = requests.post(URL, json=payload, headers=header, verify=False)

            iframe = json.loads(response.content)['iframe']
            print(iframe)

            #REQUISIÇÃO2 #LOCATION 1
            URL = iframe

            response = requests.get(URL, allow_redirects=False)

            location_1 = response.headers.get('Location')
            print(location_1)

            #REQUISIÇÃO3 #LOCATION 2
            headers = {
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Cookie":"PHPSESSID=54f53f123608c0f86c541fe22c3fa142; __cf_bm=uzgn_qu4HAihg1qxKLHpowvwCGWWmcZzW2L6vRHxU44-1715897339-1.0.1.1-BJKgHBDOv.LL8pMH0MQWG888N3ZyIM4_MsQPlOxVVTDB9c2.tqrQlOq_q5JiYQ2Fi7RXpr4QHGI7nG3u3KCgTA",
                "Referer":"https://cash-back-infinity.web.app/",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
            }

            response = requests.get(location_1, headers=headers, allow_redirects=False, verify=False)

            location_2 = response.headers.get('Location')
            print(location_2)

            #REQUISIÇÃO4 #EVOSESSID
            URL = location_2
            headers = {
                "authority":"ezugi.evo-games.com",
                "Cookie":"lang=en; locale=en-GB; EVOSESSIONID=rz3ohzd6qdvs2p5cr6baxmuxn43hgprn1768b99ef7cc4a20031b19993667df8e8b96ce99bab48d4f",
                "Referer":"https://cash-back-infinity.web.app/",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            }

            response = requests.get(location_2, headers=headers, allow_redirects=False, verify=False)

            evosessionid = response.headers.get('Set-Cookie').split('; Path=/')[0]

            return evosessionid
        
        except Exception as e:
            print(e)
            time.sleep(10)
            continue


def conectar_websocket(evosessionid):
    global ws
    global cont
    global ultimo_result
    global ultimo_valor_armazenado

    try:

        header = {
        
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "no-cache",
        "Connection": "Upgrade",
        'Cookie':f'lang=en; locale=en-GB; {evosessionid}',
        "Host": "ezugi.evo-games.com",
        "Origin": "https://ezugi.evo-games.com",
        "Pragma":"no-cache",
        "Sec-Websocket-Extensions":"permessage-deflate; client_max_window_bits",
        "Sec-Websocket-Key":"tMKcxpqt9k2L8UoF+Ra9yQ==",
        "Sec-Websocket-Version":"13",
        "Upgrade":"websocket",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

        }

        URL = f'wss://ezugi.evo-games.com/public/baccarat/player/game/oytmvb9m1zysmc44/socket?messageFormat=json&instance=s0z2gx-rz3ohzd6qdvs2p5c-nx7ecktjzywdqwwt&tableConfig=nx7ecktjzywdqwwt&{evosessionid}&client_version=6.20240515.72258.41670-771cf851ea'
        #URL = f'wss://belloatech.evo-games.com/public/bacbo/player/game/BacBo00000000001/socket?messageFormat=json&instance=pe7y9k-rhjuf7mokioplhho-BacBo00000000001&tableConfig=&EVOSESSIONID={evosessionid}&client_version=6.20230823.71249.29885-78ea79aff8'
        #URL = f'wss://tmkybox.evo-games.com/public/bacbo/player/game/BacBo00000000001/socket?messageFormat=json&instance=wauuc5-rm2dykph2d2ahokr-BacBo00000000001&tableConfig=&{evosessionid}&client_version=6.20231117.220451.34739-a84e2ac2a1'
        
        ws = create_connection(URL, verify=False)

        ws.send(json.dumps([json.dumps(header)]))

        cont = 0
        ultimo_result = ''
        ultimo_valor_armazenado = ''

    except Exception as e:
        print('ERRO NA FUNÇÃO CONECTAR WEBSOCKET----', e)


def formata_dados(ultimo_result):
    ''' Convertendo a letra em cor '''
    # Pegando Resultado da rodada no arquivo JSON
    resultado = json.loads(ultimo_result)['args']['result']['winner']
            
    if resultado == 'Player':
        resultado = 'P'
        
    if resultado == 'Banker':
        resultado = 'B'
        
    if resultado == 'Tie':
        resultado = 'T'
        
    return resultado


def coletarDados():
    global evosessionid

    evosessionid = pegar_evosessionid()

    while True:

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass
        
        # Validando o horario para envio do relatório diário
        validaData()


        try:
            # Validando se foi solicitado o stop do BOT
            if parar != 0:
                break
            else:
                pass
            
            # Validando o horario para envio do relatório diário
            validaData()

            # Pegando o histórico de resultados
            try:

                conectar_websocket(evosessionid)

                while True:
                    
                    ultimo_result = ws.recv()

                    if 'baccarat.resolved' in ultimo_result:

                        resultado_atual = formata_dados(ultimo_result)
                        lista_resultados.append(resultado_atual)

                        # Enviando Resultado pra API de Resultados
                        enviarPostAPIResultados('banker' if resultado_atual == 'B' 
                                                        else 'player' if resultado_atual == 'P'
                                                        else 'tie').start()

                        
                        print(datetime.now().strftime('%H:%M'))
                        ''' Chama a função que valida a estratégia para enviar o sinal Telegram '''
                        validaEstrategias(lista_resultados)
                        #Separador
                        print('=' * 100)
                        
                    
                    ultimo_valor_armazenado = ultimo_result  
                                        
                
            except Exception as e:
                print(e)
                evosessionid = pegar_evosessionid()
                continue
                
                
            # Validando se foi solicitado o stop do BOT
            if parar != 0:
                break
            else:
                pass
    
        except Exception as e:
            print(e)
            print('ERRO NO PRIMEIRO TRY DA FUNÇÃO PEGAR DADOS')
            

def validaEstrategias(lista_resultados):
    global estrategias
    global estrategia
    
    for estrategia in estrategias:
        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass
        # Validando o horario para envio do relatório diário
        validaData()

        # Jogo Pausado
        #validarJogoPausado()
        
        sequencia_minima_alerta = len(estrategia)-2
        sequencia_minima_sinal = len(estrategia)-1

        print ('Analisando a Estratégia --> ', estrategia)
        print ('Historico da Mesa --> ', lista_resultados[:sequencia_minima_alerta])

        ''' Verifica se os resultados da mesa batem com a estrategia para enviar o alerta '''
        if estrategia[:sequencia_minima_alerta] == lista_resultados[-sequencia_minima_alerta:]:
            print('IDENTIFICADO O PADRÃO DA ESTRATÉGIA --> ', estrategia)
            print('ENVIAR ALERTA')
            enviarAlertaTelegram()
            time.sleep(1)

            ''' Verifica se a ultima condição bate com a estratégia para enviar sinal Telegram '''
            while True:
                try:
                    #Relatório de Placar
                    validaData()

                    # Validando se foi solicitado o stop do BOT
                    if parar != 0:
                        break
                    else:
                        pass
                    
                    ultimo_result = ws.recv()

                    if 'baccarat.resolved' in ultimo_result:
                        resultado_atual = formata_dados(ultimo_result)
                        lista_resultados.append(resultado_atual)
                        
                        # Enviando Resultado pra API de Resultados
                        enviarPostAPIResultados('banker' if resultado_atual == 'B' 
                                                        else 'player' if resultado_atual == 'P'
                                                        else 'tie').start()


                        if estrategia[:sequencia_minima_sinal] == lista_resultados[-sequencia_minima_sinal:]:
                            print('PADRÃO DA ESTRATÉGIA ', estrategia, ' CONFIRMADO!')
                            print('ENVIANDO SINAL TELEGRAM')
                            enviarSinalTelegram()
                            time.sleep(10)
                            checkSinalEnviado(lista_resultados)
                            break
                            
                        else:
                            print('APAGA SINAL DE ALERTA')
                            apagaAlertaTelegram()
                            break

                    else:
                        ultimo_valor_armazenado = ultimo_result


                except Exception as e:

                    if e.args[0] == 'socket is already closed.':
                        conectar_websocket(evosessionid)
                    
                    else:
                        print(e)
                        evosessionid = pegar_evosessionid()
                        conectar_websocket(evosessionid)
                        continue


def enviarAlertaTelegram():
    global contador_passagem

    ''' Lendo o arquivo txt canais '''
    txt = open(r"arquivos_txt\canais.txt", "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[12].replace('canais= ','').replace('\n','')
    canais = ast.literal_eval(canais) # Convertendo string em dicionario 


    # Enviando POST para a API
    try:
        ''' Lendo o arquivo txt '''
        with open('arquivos_txt\\alerta_api.txt',"r", encoding="utf-8") as arquivo:
            message_alerta = arquivo.read()

        texto = message_alerta
        
        enviarPostAPI(texto, '', '').start()

    except Exception as e:
        print(e)

    ''' Enviando mensagem Telegram '''
    try:
        for key,value in canais.items():
            try:
                ''' Lendo o arquivo txt '''
                with open('arquivos_txt\\alerta.txt',"r", encoding="utf-8") as arquivo:
                    message_alerta = arquivo.read()

                ''' Mensagem '''
                #table_alerta = mensagem_alerta[0].replace('\n','') + '\n' + mensagem_alerta[1].replace('\n','') + '\n' + mensagem_alerta[2].replace('\n','').replace('[SITE_PC]', value[1]) + mensagem_alerta[3].replace('\n','').replace('[SITE_MB]', value[2])
                globals()[f'alerta_{key}'] = bot.send_message(key, message_alerta
                                                                    .replace('[SITE_PC]', value[0])
                                                                    .replace('[SITE_MB]', value[0]), 
                                                              parse_mode='HTML', disable_web_page_preview=True)  #Variavel Dinâmica
            except:
                pass

    except:
        pass

    contador_passagem = 1


def enviarSinalTelegram():
    global table_sinal
    
    ''' Lendo o arquivo txt canais '''
    txt = open(r"arquivos_txt\canais.txt", "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[12].replace('canais= ','').replace('\n','')
    canais = ast.literal_eval(canais) # Convertendo string em dicionario 


    # Enviando POST para a API
    try:
        ''' Lendo o arquivo txt config-mensagens '''
        with open('arquivos_txt\\sinal_api.txt',"r", encoding="utf-8") as arquivo:
            message_sinal = arquivo.read()

        texto = message_sinal\
                    .replace('[COR]', 'ALTERNADO 🟥 🟦 🟥 🟦' if estrategia[-1] == 'alternadoB' else 'ALTERNADO 🟦 🟥 🟦 🟥 ' if estrategia[-1] == 'alternadoP' else '🟩' )\
  
        
        enviarPostAPI(texto, '', '').start()

    except Exception as e:
        print(e)



    ''' Enviando mensagem Telegram '''
    try:
        for key, value in canais.items():
            try:
                ''' Lendo o arquivo txt config-mensagens '''
                with open('arquivos_txt\\sinal.txt',"r", encoding="utf-8") as arquivo:
                    message_sinal = arquivo.read()

                ''' Mensagem '''
                #table_sinal = mensagem_sinal[9].replace('\n','') + '\n' + mensagem_sinal[10].replace('\n','').replace('[LINK_CANAL]',value[0]) + '\n' + mensagem_sinal[11].replace('\n','').replace('[COR]','VERMELHO' if estrategia[-1] == 'C' else 'AZUL' if estrategia[-1] == 'V' else 'AMARELO') + '\n' + mensagem_sinal[12].replace('\n','') + '\n\n' + mensagem_sinal[15].replace('\n','').replace('[SITE_PC]',value[1]) + mensagem_sinal[16].replace('\n','').replace('[SITE_MB]',value[2])
                bot.delete_message(key, globals()[f'alerta_{key}'].message_id)
                globals()[f'sinal_{key}'] = bot.send_message(key, message_sinal
                                                                    .replace('[COR]', 'ALTERNADO 🟥 🟦 🟥 🟦' if estrategia[-1] == 'alternadoB' else 'ALTERNADO 🟦 🟥 🟦 🟥 ' if estrategia[-1] == 'alternadoP' else '🟩' )
                                                                    .replace('[LINK_CANAL]', value[1])
                                                                    .replace('[SITE_PC]', value[0])
                                                                    .replace('[SITE_MB]', value[0])
                                                                    , parse_mode='HTML', disable_web_page_preview=True)
            except:
                pass
    
    except:
        pass



def apagaAlertaTelegram():
    global contador_passagem

    ''' Lendo o arquivo txt canais '''
    txt = open(r"arquivos_txt\canais.txt", "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[12].replace('canais= ','').replace('\n','')
    canais = ast.literal_eval(canais) # Convertendo string em dicionario 


    #Enviando POST para a API
    try:
    
        texto = '🚫 Entrada não confirmada'
        
        enviarPostAPI(texto, '', '').start()

    except Exception as e:
        print(e)



    try:
        for key,value in canais.items():
            try:
                bot.delete_message(key, globals()[f'alerta_{key}'].message_id)
            except:
                pass
    except:
        pass

    contador_passagem = 0



def checkSinalEnviado(lista_resultados_validacao):
    global alerta_free
    global alerta_vip
    global message_canal_free
    global message_canal_vip
    global placar_win
    global placar_semGale
    global placar_gale1
    global placar_gale2
    global placar_gale3, placar_gale4, placar_gale5, placar_gale6, placar_gale7, placar_gale8, placar_gale9, placar_gale10
    global placar_loss
    global resultados_sinais
    global ultimo_horario_resultado
    global validador_sinal
    global stop_loss
    global estrategia
    global contador_passagem
    global lista_resultados
    global table
    global contador_cash
    global placar_maior
    global inicio_alternado

    resultado_valida_sinal = []
    contador_cash = 0
    

    if estrategia[-1] == 'alternadoB':
        resultado_estrategia = 'B'
        inicio_alternado = 'B'
    elif estrategia[-1] == 'alternadoP':
        resultado_estrategia = 'P'
        inicio_alternado = 'P'


    while True:

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass

        # Validando o horario para envio do relatório diário
        validaData()

        try:
           
            ultimo_result = ws.recv()

            if 'baccarat.resolved' in ultimo_result:

                resultado_atual = formata_dados(ultimo_result)

                lista_resultados.append(resultado_atual)

                # Enviando Resultado pra API de Resultados
                enviarPostAPIResultados('banker' if resultado_atual == 'B' 
                                                        else 'player' if resultado_atual == 'P'
                                                        else 'tie').start()

                print(lista_resultados[-1])

                if lista_resultados[-1] == 'P':
                    resultado_valida_sinal.append('🟦')

                if lista_resultados[-1] == 'B':
                    resultado_valida_sinal.append('🟥')
                
                if lista_resultados[-1] == 'E':
                    resultado_valida_sinal.append('🟩')

                #resultado_valida_sinal.append(lista_resultados[-1])
                    
                
                # VALIDANDO WIN OU LOSS
                if lista_resultados[-1] == resultado_estrategia:
                    
                    print('GREEN')
                    print('==================================================')
                    contador_cash+=1
                    
                    ### FUNÇÃO PARA ESTRATEGIA ALTERNADA
    
                    inicio_alternado, resultado_estrategia = estrategia_alterada(inicio_alternado)

                    continue
                
                #CONDIÇÃO SE DER EMPATE E FOR O SEGUNDO EM DIANTE RESULTADO DO SINAL
                #elif lista_resultados[-1] == 'T' and contador_cash != 0:

                #    print('EMPATE!! MANTENHA NA MESMA COR ANTERIOR!')
                #    contador_cash+=1
                    
                    # Enviando POST para a API
                #    try:
                #        ''' Lendo o arquivo txt config-mensagens '''
                #        with open('arquivos_txt/empate_2.txt',"r", encoding="utf-8") as arquivo:
                #            message_empate = arquivo.read()

                #        texto = message_empate

                #        enviarPostAPI(texto).start()

                #    except Exception as e:
                #        print(e)


                    # enviando mensagem empate
                #    try:
                #        ''' Lendo o arquivo txt canais '''
                #        txt = open(r"arquivos_txt/canais.txt", "r", encoding="utf-8")
                #        arquivo = txt.readlines()
                #        canais = arquivo[12].replace('canais= ','').replace('\n','')
                #        canais = ast.literal_eval(canais) # Convertendo string em dicionario 
                       
                #        for key, value in canais.items():
                #            try:
                #                ''' Lendo o arquivo txt config-mensagens '''
                #                with open('arquivos_txt/empate_2.txt',"r", encoding="utf-8") as arquivo:
                #                    message_empate_2 = arquivo.read()

                #                globals()[f'empate_{key}'] = bot.send_message(key, message_empate_2, parse_mode='HTML')

                                #Aguardando 5 segundos
                #                time.sleep(5)

                                #Excluindo mensagem enviada
                #                bot.delete_message(key, globals()[f'empate_{key}'].message_id)

                #                print('Mensagem Excluida')

                #            except:
                #                pass
                        
                #        continue
                
                #    except Exception as e:
                #        print(e)
                #        pass                     

                #CONDIÇÃO SE DER EMPATE
                elif lista_resultados[-1] == 'T': #and contador_cash == 0:
                    
                    print('EMPATE!! AGUARDE O PROXIMO SINAL!')
                    
                    # Enviando POST para a API
                    try:
                        ''' Lendo o arquivo txt config-mensagens '''
                        with open('arquivos_txt/empate.txt',"r", encoding="utf-8") as arquivo:
                            message_empate = arquivo.read()

                        texto = message_empate

                        enviarPostAPI(texto, str(contador_cash), 'tie').start()

                    except Exception as e:
                        print(e)



                    # editando mensagem enviada
                    try:
                        ''' Lendo o arquivo txt canais '''
                        txt = open(r"arquivos_txt/canais.txt", "r", encoding="utf-8")
                        arquivo = txt.readlines()
                        canais = arquivo[12].replace('canais= ','').replace('\n','')
                        canais = ast.literal_eval(canais) # Convertendo string em dicionario 
                       
                        for key, value in canais.items():
                            try:
                                ''' Lendo o arquivo txt config-mensagens '''
                                with open('arquivos_txt/empate.txt',"r", encoding="utf-8") as arquivo:
                                    message_empate = arquivo.read()

                                bot.reply_to(globals()[f'sinal_{key}'], message_empate, parse_mode='HTML')
                            except:
                                pass
                
                    except Exception as e:
                        print(e)
                        pass
                    

                    print('='*100)
                    validador_sinal = 0
                    contador_cash = 0
                    contador_passagem = 0
                    
                    return
                    


                else:

                    # validando o tipo de WIN
                    if contador_cash == 0:
                        print('LOSS SEM GALE')
                        stop_loss.append('win')

                        # Atualizando placar e Alimentando o arquivo txt
                        placar_win +=1
                        placar_semGale +=1
                        placar_geral = placar_win + placar_loss

                        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                            arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}\nmaior,{placar_maior}\ng3,{placar_gale3}\ng4,{placar_gale4}\ng5,{placar_gale5}\ng6,{placar_gale6}\ng7,{placar_gale7}\ng8,{placar_gale8}\ng9,{placar_gale9}\ng10,{placar_gale10}")
                        
                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                        try:
                            # Somando Win na estratégia da lista atual
                            for pe in placar_estrategias:
                                if pe[0] == estrategia:
                                    pe[-12] = int(pe[-12])+1
                        except:
                            pass
                        
                        
                    elif contador_cash == 1:
                        print('LOSS GALE1')
                        stop_loss.append('win')

                        # Atualizando placar e Alimentando o arquivo txt
                        placar_win +=1
                        placar_gale1 +=1
                        placar_geral = placar_win + placar_loss
                        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                            arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}\nmaior,{placar_maior}\ng3,{placar_gale3}\ng4,{placar_gale4}\ng5,{placar_gale5}\ng6,{placar_gale6}\ng7,{placar_gale7}\ng8,{placar_gale8}\ng9,{placar_gale9}\ng10,{placar_gale10}")
                         

                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                        try:
                            # Somando Win na estratégia da lista atual
                            for pe in placar_estrategias:
                                if pe[0] == estrategia:
                                    pe[-11] = int(pe[-11])+1

                        except:
                            pass


                    elif contador_cash == 2:
                        print('LOSS GALE2')
                        stop_loss.append('win')
                        
                        # Atualizando placar e Alimentando o arquivo txt
                        placar_win +=1
                        placar_gale2 +=1
                        placar_geral = placar_win + placar_loss
                        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                            arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}\nmaior,{placar_maior}\ng3,{placar_gale3}\ng4,{placar_gale4}\ng5,{placar_gale5}\ng6,{placar_gale6}\ng7,{placar_gale7}\ng8,{placar_gale8}\ng9,{placar_gale9}\ng10,{placar_gale10}")
                        
                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)
                        
                        try:
                            # Somando Win na estratégia da lista atual
                            for pe in placar_estrategias:
                                    if pe[0] == estrategia:
                                        pe[-10] = int(pe[-10])+1
                        except:
                            pass
                        
                    
                    elif contador_cash == 3:
                        print('LOSS GALE3')
                        stop_loss.append('win')

                        # Atualizando placar e Alimentando o arquivo txt
                        placar_win +=1
                        placar_gale3 +=1
                        placar_geral = placar_win + placar_loss
                        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                            arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}\nmaior,{placar_maior}\ng3,{placar_gale3}\ng4,{placar_gale4}\ng5,{placar_gale5}\ng6,{placar_gale6}\ng7,{placar_gale7}\ng8,{placar_gale8}\ng9,{placar_gale9}\ng10,{placar_gale10}")
                         

                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                        try:
                            # Somando Win na estratégia da lista atual
                            for pe in placar_estrategias:
                                if pe[0] == estrategia:
                                    pe[-9] = int(pe[-9])+1

                        except:
                            pass


                    elif contador_cash == 4:
                        print('LOSS GALE4')
                        stop_loss.append('win')

                        # Atualizando placar e Alimentando o arquivo txt
                        placar_win +=1
                        placar_gale4 +=1
                        placar_geral = placar_win + placar_loss
                        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                            arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}\nmaior,{placar_maior}\ng3,{placar_gale3}\ng4,{placar_gale4}\ng5,{placar_gale5}\ng6,{placar_gale6}\ng7,{placar_gale7}\ng8,{placar_gale8}\ng9,{placar_gale9}\ng10,{placar_gale10}")
                         

                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                        try:
                            # Somando Win na estratégia da lista atual
                            for pe in placar_estrategias:
                                if pe[0] == estrategia:
                                    pe[-8] = int(pe[-8])+1

                        except:
                            pass


                    elif contador_cash == 5:
                        print('LOSS GALE5')
                        stop_loss.append('win')

                        # Atualizando placar e Alimentando o arquivo txt
                        placar_win +=1
                        placar_gale5 +=1
                        placar_geral = placar_win + placar_loss
                        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                            arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}\nmaior,{placar_maior}\ng3,{placar_gale3}\ng4,{placar_gale4}\ng5,{placar_gale5}\ng6,{placar_gale6}\ng7,{placar_gale7}\ng8,{placar_gale8}\ng9,{placar_gale9}\ng10,{placar_gale10}")
                         

                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                        try:
                            # Somando Win na estratégia da lista atual
                            for pe in placar_estrategias:
                                if pe[0] == estrategia:
                                    pe[-7] = int(pe[-7])+1

                        except:
                            pass


                    elif contador_cash == 6:
                        print('LOSS GALE6')
                        stop_loss.append('win')

                        # Atualizando placar e Alimentando o arquivo txt
                        placar_win +=1
                        placar_gale6 +=1
                        placar_geral = placar_win + placar_loss
                        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                            arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}\nmaior,{placar_maior}\ng3,{placar_gale3}\ng4,{placar_gale4}\ng5,{placar_gale5}\ng6,{placar_gale6}\ng7,{placar_gale7}\ng8,{placar_gale8}\ng9,{placar_gale9}\ng10,{placar_gale10}")
                         

                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                        try:
                            # Somando Win na estratégia da lista atual
                            for pe in placar_estrategias:
                                if pe[0] == estrategia:
                                    pe[-6] = int(pe[-6])+1

                        except:
                            pass


                    elif contador_cash == 7:
                        print('LOSS GALE7')
                        stop_loss.append('win')

                        # Atualizando placar e Alimentando o arquivo txt
                        placar_win +=1
                        placar_gale7 +=1
                        placar_geral = placar_win + placar_loss
                        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                            arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}\nmaior,{placar_maior}\ng3,{placar_gale3}\ng4,{placar_gale4}\ng5,{placar_gale5}\ng6,{placar_gale6}\ng7,{placar_gale7}\ng8,{placar_gale8}\ng9,{placar_gale9}\ng10,{placar_gale10}")
                         

                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                        try:
                            # Somando Win na estratégia da lista atual
                            for pe in placar_estrategias:
                                if pe[0] == estrategia:
                                    pe[-5] = int(pe[-5])+1

                        except:
                            pass


                    elif contador_cash == 8:
                        print('LOSS GALE8')
                        stop_loss.append('win')

                        # Atualizando placar e Alimentando o arquivo txt
                        placar_win +=1
                        placar_gale8 +=1
                        placar_geral = placar_win + placar_loss
                        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                            arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}\nmaior,{placar_maior}\ng3,{placar_gale3}\ng4,{placar_gale4}\ng5,{placar_gale5}\ng6,{placar_gale6}\ng7,{placar_gale7}\ng8,{placar_gale8}\ng9,{placar_gale9}\ng10,{placar_gale10}")
                         

                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                        try:
                            # Somando Win na estratégia da lista atual
                            for pe in placar_estrategias:
                                if pe[0] == estrategia:
                                    pe[-4] = int(pe[-4])+1

                        except:
                            pass


                    elif contador_cash == 9:
                        print('LOSS GALE9')
                        stop_loss.append('win')

                        # Atualizando placar e Alimentando o arquivo txt
                        placar_win +=1
                        placar_gale9 +=1
                        placar_geral = placar_win + placar_loss
                        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                            arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}\nmaior,{placar_maior}\ng3,{placar_gale3}\ng4,{placar_gale4}\ng5,{placar_gale5}\ng6,{placar_gale6}\ng7,{placar_gale7}\ng8,{placar_gale8}\ng9,{placar_gale9}\ng10,{placar_gale10}")
                         

                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                        try:
                            # Somando Win na estratégia da lista atual
                            for pe in placar_estrategias:
                                if pe[0] == estrategia:
                                    pe[-3] = int(pe[-3])+1

                        except:
                            pass

                    
                    elif contador_cash == 10:
                        print('LOSS GALE10')
                        stop_loss.append('win')

                        # Atualizando placar e Alimentando o arquivo txt
                        placar_win +=1
                        placar_gale10 +=1
                        placar_geral = placar_win + placar_loss
                        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                            arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}\nmaior,{placar_maior}\ng3,{placar_gale3}\ng4,{placar_gale4}\ng5,{placar_gale5}\ng6,{placar_gale6}\ng7,{placar_gale7}\ng8,{placar_gale8}\ng9,{placar_gale9}\ng10,{placar_gale10}")
                         

                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                        try:
                            # Somando Win na estratégia da lista atual
                            for pe in placar_estrategias:
                                if pe[0] == estrategia:
                                    pe[-2] = int(pe[-2])+1

                        except:
                            pass

                        

                    else:
                        print('LOSS MAIOR QUE 10 GALES')
                        #stop_loss.append('win')

                        # Atualizando placar e Alimentando o arquivo txt
                        placar_win +=1
                        placar_maior +=1
                        placar_geral = placar_win + placar_loss

                        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                            arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}\nmaior,{placar_maior}\ng3,{placar_gale3}\ng4,{placar_gale4}\ng5,{placar_gale5}\ng6,{placar_gale6}\ng7,{placar_gale7}\ng8,{placar_gale8}\ng9,{placar_gale9}\ng10,{placar_gale10}")
                        
                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                        try:
                            # Somando Win na estratégia da lista atual
                            for pe in placar_estrategias:
                                if pe[0] == estrategia:
                                    pe[-1] = int(pe[-1])+1
                        except:
                            pass
                        

                    # editando mensagem enviada
                    try:
                        ''' Lendo o arquivo txt canais '''
                        txt = open(r"arquivos_txt\canais.txt", "r", encoding="utf-8")
                        arquivo = txt.readlines()
                        canais = arquivo[12].replace('canais= ','').replace('\n','')
                        canais = ast.literal_eval(canais) # Convertendo string em dicionario 



                        #Enviando POST para a API
                        try:
                            ''' Lendo o arquivo txt config-mensagens '''
                            with open('arquivos_txt\\red.txt',"r", encoding="utf-8") as arquivo:
                                message_green = arquivo.read()

                            texto = message_green.replace('[GALE]', str(contador_cash))
                            
                            enviarPostAPI(texto, str(contador_cash), 'banker' if lista_resultados[-1] == 'B' 
                                                                            else 'player' if lista_resultados[-1] == 'P'
                                                                            else 'tie').start()

                        except Exception as e:
                            print(e)

                        
                        #Enviando mensagem Telegram
                        for key, value in canais.items():
                            try:
                                ''' Lendo o arquivo txt config-mensagens '''
                                with open('arquivos_txt\\red.txt',"r", encoding="utf-8") as arquivo:
                                    message_green = arquivo.read()

                                bot.reply_to(globals()[f'sinal_{key}'], message_green.replace('[GALE]', str(contador_cash)), parse_mode='HTML')
                            except:
                                pass
                
                    except:
                        pass
                    

                    print('='*100)
                    validador_sinal = 0
                    contador_cash = 0
                    contador_passagem = 0
                    
                    return
                
        except Exception as e:
            if e.args[0] == 'socket is already closed.':
                conectar_websocket(evosessionid)
            
            else:
                print(e)
                evosessionid = pegar_evosessionid()
                conectar_websocket(evosessionid)
                continue



def estrategia_alterada(inicio_alternado):

    try:

        if inicio_alternado == 'B':
            inicio_alternado = 'P'
        
        elif inicio_alternado == 'P':
            inicio_alternado = 'B'


        return inicio_alternado, inicio_alternado
        
    
    except Exception as e:
        print(e)




inicio()
placar()
#pegar_evosessionid()



#________________________________________________________________________________________ TELEGRAM__________________________________________________________________________________#

print('\n\n')
print('############################################ AGUARDANDO COMANDOS ############################################')


# VARIAVEIS
#placar_win = 0
#placar_semGale= 0
#placar_gale1= 0
#placar_gale2= 0
#placar_gale3= 0
#placar_loss = 0
#resultados_sinais = placar_win + placar_loss
estrategias = []
placar_estrategias = []
estrategias_diaria = []
placar_estrategias_diaria = []
contador = 0
contador_passagem = 0
botStatus = 0



# LENDO TXT PARA DEFINIR VARIAVEL DE CANAIS E VALIDAÇÃO DE USUÁRIO
txt = open("arquivos_txt/canais.txt", "r", encoding="utf-8")
arquivo = txt.readlines()
usuario = arquivo[2].split(' ')[1]
senha = arquivo[3].split(' ')[1].split('\n')[0]
CHAVE_API = arquivo[7].split(' ')[1].split('\n')[0]

ids = arquivo[11].split(' ')[1].split('\n')[0]
canais = arquivo[12].split(' ')[1].split('\n')[0].split((','))


bot = telebot.TeleBot(CHAVE_API)



######################################################


global message


def generate_buttons_estrategias(bts_names, markup):
    for button in bts_names:
        markup.add(types.KeyboardButton(button))
    return markup



def pausarBot():
     while True:
        try:
            global parar
            global browser
            parar = 1
            time.sleep(1)
            break

        except:
            continue



@bot.message_handler(commands=['⚙ Cadastrar_Estratégia'])
def cadastrarEstrategia(message):

    global contador_passagem

    if contador_passagem == 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
        markup = markup.add('◀ Voltar', 'ESTRATÉGIAS PADRÕES','NOVA ESTRATÉGIA')

        
        message_tipo_estrategia = bot.reply_to(message, "🤖 Ok! Escolha cadastrar uma nova estratégia ou cadastrar estratégias padrões 👇", reply_markup=markup)
        bot.register_next_step_handler(message_tipo_estrategia, registrarTipoEstrategia)
    

    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_estrategia = bot.reply_to(message, "🤖⛔ Estou validando uma estratégia! Tente novamente em alguns instanstes.", reply_markup=markup)



@bot.message_handler(commands=['🗑 Apagar_Estratégia'])
def apagarEstrategia(message):
    global estrategia
    global estrategias
    global contador_passagem

    print('Excluir estrategia')

    if contador_passagem == 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        #Add to buttons by list with ours generate_buttons function.
        markup_estrategias = generate_buttons_estrategias([''.join(estrategia) for estrategia in estrategias], markup)
        markup_estrategias.add('◀ Voltar')   


        message_excluir_estrategia = bot.reply_to(message, "🤖 Escolha a estratégia a ser excluída 👇", reply_markup=markup_estrategias)
        bot.register_next_step_handler(message_excluir_estrategia, registrarEstrategiaExcluida)
    
    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_excluir_estrategia = bot.reply_to(message, "🤖⛔ Estou validando uma estratégia! Tente novamente em alguns instanstes.", reply_markup=markup)



@bot.message_handler(commands=['📜 Estrategias_Cadastradas'])
def estrategiasCadastradas(message):
    global estrategia
    global estrategias

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    bot.reply_to(message, "🤖 Ok! Listando estratégias", reply_markup=markup)

    for estrategia in estrategias:
        #print(estrategia)
        bot.send_message(message.chat.id, ''.join(estrategia))




@bot.message_handler(commands=['📊 Placar Atual'])
def placar_atual(message):
    global placar
    global resultados_sinais

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    try:
        placar()

        resposta = bot.reply_to(message,\
        "📊 Placar Atual do dia "+data_hoje+":\n\
        =====================\n\
        TOTAL LOSS - "+str(placar_win)+"\n\
        LOSS S/ GALE - "+str(placar_semGale)+"\n\
        LOSS GALE1 - "+str(placar_gale1)+"\n\
        LOSS GALE2 - "+str(placar_gale2)+"\n\
        LOSS GALE3 - "+str(placar_gale3)+"\n\
        LOSS GALE4 - "+str(placar_gale4)+"\n\
        LOSS GALE5 - "+str(placar_gale5)+"\n\
        LOSS GALE6 - "+str(placar_gale6)+"\n\
        LOSS GALE7 - "+str(placar_gale7)+"\n\
        LOSS GALE8 - "+str(placar_gale8)+"\n\
        LOSS GALE9 - "+str(placar_gale9)+"\n\
        LOSS GALE10 - "+str(placar_gale10)+"\n\
        LOSS MAIOR QUE 10 - "+str(placar_maior)+"\n\
        =====================",
        reply_markup=markup)
        
    except Exception as a:
        logger.error('Exception ocorrido no ' + repr(a))
        #placar = bot.reply_to(message,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%", reply_markup=markup)
        pass



@bot.message_handler(commands=['♻ Resetar Resultados'])
def resetarResultados(message):
    global placar_win
    global placar_semGale
    global placar_gale1
    global placar_gale2
    global placar_gale3
    global placar_loss
    global placar
    global resultados_sinais
    global placar_estrategias

    # Resetando placar Geral (placar geral)
    placar_win = 0
    placar_semGale= 0
    placar_gale1= 0
    placar_gale2= 0
    placar_gale3= 0
    placar_loss = 0

    # Resetando placar das estrategias (Gestão)
    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    for pe in placar_estrategias:
        pe[-5], pe[-4], pe[-3], pe[-2], pe[-1] = 0,0,0,0,0
        assertividade = '0%'
    
    message_final = bot.reply_to(message, "🤖♻ Resultados resetados com sucesso ✅", reply_markup=markup)




@bot.message_handler(commands=['📈 Gestão'])
def gestao(message):
    global placar
    global resultados_sinais
    global placar_estrategias

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    
    for pe in placar_estrategias:
        
        total = int(pe[-12]) + int(pe[-11]) + int(pe[-10]) + int(pe[-9]) + int(pe[-8]) + int(pe[-7]) + int(pe[-6]) + int(pe[-5]) + int(pe[-4]) + int(pe[-3]) + int(pe[-2]) + int(pe[-1])
        #soma_win = int(pe[-5]) + int(pe[-4]) + int(pe[-3]) + int(pe[-2])

        bot.send_message(message.chat.id, 
                        
                        f'🧠 {pe[0]}\
                        \n==========================\n\
SG = {pe[-12]}\n\
G1 = {pe[-11]}\n\
G2 = {pe[-10]}\n\
G3 = {pe[-9]}\n\
G4 = {pe[-8]}\n\
G5 = {pe[-7]}\n\
G6 = {pe[-6]}\n\
G7 = {pe[-5]}\n\
G8 = {pe[-4]}\n\
G9 = {pe[-3]}\n\
G10 = {pe[-2]}\n\
MAIOR 10 = {pe[-1]}', reply_markup=markup)
        
        


@bot.message_handler(commands=['🛑 Pausar_bot'])
def pausar(message):
    global botStatus
    global contador_passagem
    global parar

    
    if botStatus == 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Bot já está pausado ", reply_markup=markup)

    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        print('\n\n')
        print('Comando: Parar BOT')
        print('Parando o BOT....\n')
        botStatus = 0
        parar += 1
        #pausarBot()

        print('###################### AGUARDANDO COMANDOS ######################')

        message_final = bot.reply_to(message, "🤖 Ok! Bot pausado 🛑", reply_markup=markup)





@bot.message_handler(commands=['start'])
def start(message):

    if str(message.chat.id) in ids:

        #Add to buttons by list with ours generate_buttons function.
        #markup = generate_buttons(['/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','📊 Placar Atual','❌ Pausar Bot'], markup)
        
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message, "🤖 Bot Baccarat Iniciado! ✅ Escolha uma opção 👇",
                                reply_markup=markup)
        
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(message_opcoes, opcoes)
    
    else:
        message_error = bot.reply_to(message, "🤖 Você não tem permissão para acessar este Bot ❌🚫")





@bot.message_handler()
def opcoes(message_opcoes):

    if message_opcoes.text in ['⚙ Cadastrar Estratégia']:
        print('Cadastrar Estrategia')

        cadastrarEstrategia(message_opcoes)


    if message_opcoes.text in['📜 Estratégias Cadastradas']:
        print('Estrategias Cadastradas')
        estrategiasCadastradas(message_opcoes)


    if message_opcoes.text in ['🗑 Apagar Estratégia']:
        print('Apagar estrategia')
        apagarEstrategia(message_opcoes)



    if message_opcoes.text in ['✅ Ativar Bot']:
        global botStatus
        global placar
        global estrategia
        global stop_loss
        global botStatus
        global reladiarioenviado
        global parar

        print('Ativar Bot')

        if botStatus == 1:

            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖⛔ Bot já está ativado",
                                reply_markup=markup)

        elif estrategias == []:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖⛔ Cadastre no mínimo 1 estratégia antes de iniciar",
                                reply_markup=markup)
        
        else:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

            message_final = bot.reply_to(message_opcoes, "🤖 Ok! Bot Ativado com sucesso! ✅ Em breve receberá sinais nos canais informados no arquivo auxiliar!", reply_markup = markup)
            
            stop_loss = []
            botStatus = 1
            vela_anterior = 0
            reladiarioenviado = 0
            parar = 0
    
            print('######################### ANALISANDO AS ESTRATÉGIAS CADASTRADAS  #########################')
            print()

            coletarDados()
            
    
    if message_opcoes.text in['📊 Placar Atual']:
        print('Placar Atual')
        placar_atual(message_opcoes)



    if message_opcoes.text in ['♻ Resetar Resultados']:
        print('Resetar Resultados')
        resetarResultados(message_opcoes)



    if message_opcoes.text in['📈 Gestão']:
        print('Gestão')
        gestao(message_opcoes)


    if message_opcoes.text in ['🛑 Pausar Bot']:
        print('Pausar Bot')
        pausar(message_opcoes)
    



@bot.message_handler()
def registrarTipoEstrategia(message_tipo_estrategia):
    global resposta_usuario

    if message_tipo_estrategia.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_tipo_estrategia, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        return


    if message_tipo_estrategia.text in ['ESTRATÉGIAS PADRÕES']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')


        estrategias_padroes = ( 
                                ['P','P','alternadoP'],
                                ['B','B','alternadoB'],
                                ['P','B','P','alternadoB'],
                                ['B','P','B','alternadoP'],
                              )
        

        for estrategia_padrao in estrategias_padroes:
            estrategias.append(estrategia_padrao)
            placar_estrategia = [estrategia_padrao]
            placar_estrategia.extend([0,0,0,0,0,0,0,0,0,0,0,0])
            placar_estrategias.append(placar_estrategia)


        message_aposta = bot.reply_to(message_tipo_estrategia, "🤖 Estratégias Cadastradas ✅", reply_markup=markup)


    elif message_tipo_estrategia.text in ['ESTRATÉGIAS PADRÕES B']:

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')


        estrategias_padroes = ( 
                                ['B','B','B','alternadoP'],
                                ['P','P','P','alternadoB'],
                                ['B','P','B','P','B','alternadoP'],
                                ['P','B','P','B','P','alternadoB'],
                              )
        

        for estrategia_padrao in estrategias_padroes:
            estrategias.append(estrategia_padrao)
            placar_estrategia = [estrategia_padrao]
            placar_estrategia.extend([0,0,0,0,0,0,0,0,0,0,0,0])
            placar_estrategias.append(placar_estrategia)


        message_aposta = bot.reply_to(message_tipo_estrategia, "🤖 Estratégias Cadastradas ✅", reply_markup=markup)

        
    else:
        
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
         
        markup = markup.add('◀ Voltar')

        message_estrategia = bot.reply_to(message_tipo_estrategia, "🤖 Ok! Informe a sequencia de LETRAS (B,P,E) que o bot terá que identificar. *** Após inserir alternadoB ou alternadoP ***  \n\n Ex: B,P,P,alterandoB  / P,P,P,B,alternadoP", reply_markup=markup)
        bot.register_next_step_handler(message_estrategia, registrarEstrategia)
    


@bot.message_handler()
def registrarEstrategia(message_estrategia):
    global estrategia
    global estrategias
    global placar_estrategia
    global placar_estrategias
    global placar_estrategias_diaria
    global estrategias_diaria

    if message_estrategia.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_estrategia, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        return

    
    estrategia = message_estrategia.text
    placar_estrategia = message_estrategia.text
    
    estrategia = estrategia.split(',')
    placar_estrategia = placar_estrategia.split(',')

    placar_estrategia.extend([0,0,0,0,0,0,0,0,0,0,0,0])

    # Adicionando estratégia atual
    estrategias.append(estrategia)
    placar_estrategias.append(placar_estrategia)

    # Acumulando estratégia do dia
    estrategias_diaria.append(estrategia)
    placar_estrategias_diaria.append(placar_estrategia)


    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    bot.reply_to(message_estrategia, "🤖 Estratégia cadastrada com sucesso! ✅", reply_markup=markup)





def registrarEstrategiaExcluida(message_excluir_estrategia):
    global estrategia
    global estrategias

    if message_excluir_estrategia.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_excluir_estrategia, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        return
    
    estrategia_excluir = list(message_excluir_estrategia.text)
    
    for estrategia in estrategias:
        if estrategia_excluir == estrategia:
            estrategias.remove(estrategia)

    
    for pe in placar_estrategias:
        if estrategia_excluir == pe[:-5]:
            placar_estrategias.remove(pe)


    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    bot.reply_to(message_excluir_estrategia, "🤖 Estratégia excluída com sucesso! ✅", reply_markup=markup)





while True:
    try:
        bot.infinity_polling(timeout=600, long_polling_timeout=600)
        bot.infinity_polling(True)
    except Exception as e:
        print(e)
        bot.infinity_polling(timeout=600, long_polling_timeout=600)


