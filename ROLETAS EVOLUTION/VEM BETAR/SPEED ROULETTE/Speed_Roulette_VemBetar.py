import time
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import telebot
from telegram.ext import *
from telebot import *
import ast
import os
import requests
import json
import time
from websocket import create_connection



print()
print('                                #################################################################')
print('                                ############    BOT SPEED ROULETTE VEMBETAR     #################')
print('                                #################################################################')
print('                                ##################### SEJA BEM VINDO ############################')
print('                                #################################################################')
print('                                ############# DESENVOLVIDO POR VICTOR RODRIGUES #################')
print('                                #################################################################\n')
print('Versão = 1.0.0')
print('Ambiente: Produção\n\n\n')


def inicio():

    global url
    global headers
    global lista_resultados

    url = "https://app.bootbost.com.br/api/v1/call"
    headers = {
    'Content-Type': 'application/json'
    }

    horario_inicio = datetime.now()
    lista_resultados = []


def pegar_evosessionid():

    ''' Inserindo login e senha '''
    ''' Lendo o arquivo txt config-mensagens '''
    txt = open("canais.txt", "r", encoding="utf-8")
    mensagem_login = txt.readlines()
    usuario = mensagem_login[2].replace('\n','').split('= ')[1] 
    senha = mensagem_login[3].replace('\n','').split('= ')[1]

    urlLogin = "https://odin.sportingtech.com/api/user/login"
    
    payloadLogin = '{"requestBody":{"username":"'+usuario+'","email":null,"phone":null,"keepLoggedIn":null,"password":"'+senha+'","loginType":1,"fingerPrint":"946fb7e168879bc7e8f28c581f272b46"},"languageId":23,"device":"d"}'
    
    headersLogin = {"Accept":"application/json, text/plain, */*",
                    "Content-Type": "application/json",
                    "Finger_print": "946fb7e168879bc7e8f28c581f272b46",
                    "Origin":"https://vembetar.com",
                    "Referer":"https://vembetar.com/",
                    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
                    }

    dadosLogin = requests.post(urlLogin, data=payloadLogin, headers=headersLogin)

    print(dadosLogin.text,'\n\n')

    s7oryo9stv = dadosLogin.headers['s7oryO9STV']
    traderId = json.loads(dadosLogin.text)['data']['traderId']
    code = json.loads(dadosLogin.text)['data']['code']
    balance = json.loads(dadosLogin.text)['data']['balance']

    print('traderId:',traderId,' | code:',code,' | s7oryo9stv:',s7oryo9stv,' | balance: R$',balance,'\n\n')

    while True:
        urlEvo = "https://odin.sportingtech.com/api/user/casinoapi/openGame"
        
        payloadEvo = '{"requestBody":{"gameId":"18372","channel":"web","vendorLimitId":"evol_lkcbrbdckjxajdol_BRL","vendorId":130,"redirectUrl":"https://vembetar.com/ptb/games/livecasino/detail/normal/18372/evol_lkcbrbdckjxajdol_BRL"},"identity":null,"device":"d","languageId":23}'

        headersEvo = {"Content-Type": "application/json",
                    "Origin":"https://vembetar.com",
                    "Referer":"https://vembetar.com/",
                    "s7oryO9STV":s7oryo9stv,
                    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                    "X-PGDevice":"d",
                    "X-Pgusername":"2023028999844"}

        dadosEvo = requests.post(urlEvo, data=payloadEvo, headers=headersEvo)

        if dadosEvo.status_code == 200:
            gameUrl = json.loads(dadosEvo.text)['data']['gameUrl']
            break
        else:
            time.sleep(5)
            continue

    print('gameUrl: ',gameUrl,'\n\n')

    noiframeUrl = requests.get(gameUrl,allow_redirects=False).headers.get('Location')

    print('Location:',noiframeUrl,'\n\n')

    firstnesUrl = requests.get(noiframeUrl,cookies={"EVOSESSIONID": ""},allow_redirects=False)

    evosessionid = firstnesUrl.cookies.get('EVOSESSIONID')

    return evosessionid


def conectar_websocket(evosessionid):
    global URL
    global ws
    global cont
    global ultimo_result
    global ultimo_valor_armazenado


    header = {
      
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "no-cache",
    "Connection": "Upgrade",
    "Host": "nesvembataross.evo-games.com",
    "Origin": "https://nesvembataross.evo-games.com",
    "Pragma": "no-cache",
    "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
    "Sec-WebSocket-Key": "39/oEKqvnzcGcUomXoRa+Q==",
    "Sec-WebSocket-Version": "13",
    "Upgrade": "websocket",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"

    }

   
    URL = f'wss://nesvembataross.evo-games.com/public/roulette/player/game/lkcbrbdckjxajdol/socket?messageFormat=json&instance=hy7lom-qzilw7f3a63qzjda-lkcbrbdckjxajdol&tableConfig=&EVOSESSIONID={evosessionid}&client_version=6.20230801.71909.28703-8f46577e22'
    
    ws = create_connection(URL, verify=False)

    ws.send(json.dumps([json.dumps(header)]))

    cont = 0
    ultimo_result = ''
    ultimo_valor_armazenado = ''


# GERA TXT DO PLACAR
def placar():
    global placar_win
    global placar_semGale
    global placar_gale1
    global placar_gale2
    global placar_loss
    global placar_geral
    global asserividade
    global data_hoje

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
            
            except:
                pass

            
    else:
        # Criar um arquivo com a data atual
        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
            arquivo.write("win,0\nsg,0\ng1,0\ng2,0\nloss,0\nass,0")

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
            
            except:
                pass


# ENVIA PLACAR CANAIS TELEGRAM
def envia_placar():

    try:
        placar()

        ''' Lendo o arquivo txt canais '''
        txt = open("canais.txt", "r", encoding="utf-8")
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
        😍 WIN - "+str(placar_win)+"\n\
        🏆 WIN S/ GALE - "+str(placar_semGale)+"\n\
        🥇 WIN GALE1 - "+str(placar_gale1)+"\n\
        🥈 WIN GALE2 - "+str(placar_gale2)+"\n\
        😭 LOSS - "+str(placar_loss)+"\n\
        =====================\n\
        🎯 Assertividade "+ asserividade)
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

    if horario_atual == '11:00' and reladiarioenviado == 0 or horario_atual == '17:00' and reladiarioenviado == 0:
        envia_placar()
        reladiarioenviado +=1

    
    if horario_atual == '11:01' and reladiarioenviado == 1 or horario_atual == '17:01' and reladiarioenviado == 1:
        reladiarioenviado = 0


    # Condição que zera o placar quando o dia muda
    if horario_atual == '00:00' and reladiarioenviado == 0:
        placar()
        reladiarioenviado +=1

    # Condição que zera o placar quando o dia muda
    if horario_atual == '00:01' and reladiarioenviado == 1:
        reladiarioenviado = 0

    
def apostas():
    global opcoes_apostas

    opcoes_apostas = {

            '1ª coluna': ['1', '4', '7', '10', '13', '16', '19', '22', '25', '28', '31', '34'],
            '2ª coluna': ['2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32', '35'],
            '3ª coluna': ['3', '6', '9', '12', '15', '18', '21', '24', '27', '30', '33', '36'],

            '1ª duzia': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
            '2ª duzia': ['13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'],
            '3ª duzia': ['25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36'],

            'Cor vermelho': ['1', '3', '5', '7', '9', '12', '14', '16', '18', '19', '21', '23', '25', '27', '30', '32', '34', '36'],
            'Cor preto': ['2', '4', '6', '8', '10', '11', '13', '15', '17', '20', '22', '24', '26', '28', '29', '31', '33', '35'],

            'Números par(es)': ['2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24', '26', '28', '30', '32', '34', '36'],
            'Números impar(es)': ['1', '5', '7', '9', '11', '13', '15', '17', '19', '21', '23', '25', '27', '29', '31', '33', '35'],

            'Números baixos': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18'],
            'Números altos': ['19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36'],
            
            '1ª/2ª coluna': ['1', '4', '7', '10', '13', '16', '19', '22', '25', '28', '31', '34', '2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32', '35'],
            '2ª/3ª coluna': ['2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32', '35', '3', '6', '9', '12', '15', '18', '21', '24', '27', '30', '33', '36'],
            '1ª/3ª coluna': ['1', '4', '7', '10', '13', '16', '19', '22', '25', '28', '31', '34', '3', '6', '9', '12', '15', '18', '21', '24', '27', '30', '33', '36'],

            '1ª/2ª duzia': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'],
            '2ª/3ª duzia': ['13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36'],
            '1ª/3ª duzia': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36']
        
        }


def apostasExternas(estrategia_usuario, dic_estrategia_usuario):
    global opcoes_apostas

    try:
        opcoes_apostas = {

            '1ºcoluna': ['1', '4', '7', '10', '13', '16', '19', '22', '25', '28', '31', '34'],
            '2ªcoluna': ['2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32', '35'],
            '3ªcoluna': ['3', '6', '9', '12', '15', '18', '21', '24', '27', '30', '33', '36'],

            '1ºduzia': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
            '2ªduzia': ['13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'],
            '3ªduzia': ['25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36'],

            'cor vermelho': ['1', '3', '5', '7', '9', '12', '14', '16', '18', '19', '21', '23', '25', '27', '30', '32', '34', '36'],
            'cor preto': ['2', '4', '6', '8', '10', '11', '13', '15', '17', '20', '22', '24', '26', '28', '29', '31', '33', '35'],

            'números par(es)': ['2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24', '26', '28', '30', '32', '34', '36'],
            'números impar(es)': ['1', '5', '7', '9', '11', '13', '15', '17', '19', '21', '23', '25', '27', '29', '31', '33', '35'],

            'números baixos': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18'],
            'números altos': ['19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36'],

            '1º/2ªcoluna': ['1', '4', '7', '10', '13', '16', '19', '22', '25', '28', '31', '34', '2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32', '35'],
            '2ª/3ªcoluna': ['2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32', '35', '3', '6', '9', '12', '15', '18', '21', '24', '27', '30', '33', '36'],
            '1º/3ªcoluna': ['1', '4', '7', '10', '13', '16', '19', '22', '25', '28', '31', '34', '3', '6', '9', '12', '15', '18', '21', '24', '27', '30', '33', '36'],

            '1º/2ªduzia': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'],
            '2ª/3ªduzia': ['13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36'],
            '1º/3ªduzia': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36']

        }

        for opcao_aposta in opcoes_apostas:
            if estrategia_usuario == opcao_aposta:
                dic_estrategia_usuario[opcao_aposta] = opcoes_apostas[opcao_aposta]
                #print(dic_estrategia_usuario)
        
        return dic_estrategia_usuario
    
    except:
        pass
            

def validarEstrategiaAlerta(dicionario_roletas, nome_cassino, sequencia_minima, estrategia):
    global aposta_externa

    validador = []
    for n in range(int(sequencia_minima)-1):
        
        ''' Pegando os números da aposta externa da estratégia'''
        aposta_externa = apostasExternas(estrategia[n], dic_estrategia_usuario)

        if dicionario_roletas[nome_cassino][n] in aposta_externa[estrategia[n]]:
            validador.append('true')

       
    return validador


def coletarResultados():
    global dicionario_roletas
    global contador_passagem
    global horario_atual
    global nome_fornecedor
    global lista_resultados, nome_cassino

    nome_cassino = 'Speed Roulette'
    nome_fornecedor = 'Evolution'
    site_cassino_desktop = 'https://vembetar.com/ptb/games/livecasino/detail/normal/18372/evol_lkcbrbdckjxajdol_BRL'
    site_cassino_mobile = 'https://m.vembetar.com/ptb/games/livecasino/detail/18372/evol_lkcbrbdckjxajdol_BRL'
    #EVOSESSIONID = processo_pegar_jsessionid()
    #conectar_websocket(EVOSESSIONID)

    evosessionid = pegar_evosessionid()
    conectar_websocket(evosessionid)

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
                
            if 'roulette.winSpots' in ultimo_result:
                try:

                    ultimo_resultado = json.loads(ultimo_result)['args']['code']
                    lista_resultados.insert(0, ultimo_resultado)
                    #print(lista_resultados)
                    
                except:
                    ultimo_valor_armazenado = ultimo_result
                    continue
            else:
                ultimo_valor_armazenado = ultimo_result
                continue

    
            dicionario_roletas[nome_cassino] = lista_resultados
            #print(dicionario_roletas)
            print(horario_atual)

            ''' Chama a função que valida a estratégia para enviar o sinal Telegram'''
            validarEstrategia(dicionario_roletas, lista_estrategias)

            print('=' * 150)
            continue

        
        except Exception as e:
            print(e)
            evosessionid = pegar_evosessionid()
            conectar_websocket(evosessionid)
            continue

            
def validarEstrategia(dicionario_roletas, lista_estrategias):
    global estrategia
    global contador_passagem
    global sequencia_minima
    global lista_resultados

    try:

        for estrategia in lista_estrategias:
            
            # Validando se foi solicitado o stop do BOT
            if parar != 0:
                break
            else:
                pass

            # Validando o horario para envio do relatório diário
            validaData()

            
            ''' Pegando a sequencia minima da estratégia cadastrada pelo usuário '''
            sequencia_minima = estrategia[3]
            
            print('Analisando a Estrategia --> ', estrategia)
            print('Historico_Roleta --> ', nome_cassino, dicionario_roletas[nome_cassino][:int(sequencia_minima)])

            
            ''' Verifica se os números da seq minima do historico da roleta está dentro da estratégia '''
            validador = validarEstrategiaAlerta(dicionario_roletas, nome_cassino, sequencia_minima, estrategia)
            
            ''' Validando se bateu alguma condição'''
            if validador.count('true') == int(sequencia_minima)-1:
                print('IDENTIFICADO PRÉ PADRÃO NA ROLETA ', nome_cassino, ' COM A ESTRATÉGIA ', estrategia)
                print('ENVIAR ALERTA')
                enviarAlertaTelegram(dicionario_roletas, nome_cassino, sequencia_minima, estrategia, nome_fornecedor)
                time.sleep(1)

                ''' Verifica se a ultima condição bate com a estratégia para enviar sinal Telegram '''
                while True:

                    
                    validaData()

                    try:
                        
                        ultimo_result = ws.recv()
                
                        if 'roulette.winSpots' in ultimo_result:
                            try:

                                ultimo_resultado = json.loads(ultimo_result)['args']['code']
                                lista_resultados.insert(0, ultimo_resultado)
                                #print(lista_proximo_resultados)
                                
                            except:
                                ultimo_valor_armazenado = ultimo_result
                                continue
                        else:
                            ultimo_valor_armazenado = ultimo_result
                            continue
                        
                        dicionario_roletas[nome_cassino] = lista_resultados

                        print('Resultado apos o alerta  --> ', nome_cassino, lista_resultados[:int(sequencia_minima)])

                        
                        ''' Verificando se o ultimo resultado da roleta está dentro da estratégia'''
                        if lista_resultados[0] in aposta_externa[estrategia[2]] or estrategia[2] == '0':
                            
                            print('ENVIANDO SINAL TELEGRAM')
                            
                            ultimos_resultados = ' | '.join(dicionario_roletas[nome_cassino][:int(sequencia_minima)]) 
                            ultimo_resultado = lista_resultados[0]
                            enviarSinalTelegram(nome_cassino, sequencia_minima, estrategia, nome_fornecedor, ultimo_resultado)
                            print('=' * 150)
                            checar_sinal_enviado(lista_resultados, nome_cassino, ultimos_resultados)
                            time.sleep(1)
                            break
                        
                        else:
                            print('APAGA SINAL DE ALERTA')
                            apagaAlertaTelegram()
                            print('=' * 150)
                            break
                        
                    

                    except Exception as e:
                        
                        if e.args[0] == 'socket is already closed.':
                            conectar_websocket(evosessionid)
                        
                        else:
                            print(e)
                            evosessionid = pegar_evosessionid()
                            conectar_websocket(evosessionid)
                            continue
                        

            else:
                print('=' * 150)


    except Exception as e:
        print(e)
        pass

                  
def enviarAlertaTelegram(dicionario_roletas, nome_cassino, sequencia_minima, estrategia, nome_fornecedor):
    global contador_passagem

    ''' Lendo o arquivo txt canais '''
    txt = open("canais.txt", "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[12].replace('canais= ','').replace('\n','')
    canais = ast.literal_eval(canais) # Convertendo string em dicionario 

    ''' Lendo o arquivo txt config-mensagens '''
    txt = open("mensagens_txt\\alerta.txt", "r", encoding="utf-8")
    mensagem_api = txt.readlines()

    #ENVIANDO POST PARA A API
    payload = {
            'status': 'alert', #alert | confirm | success | failure | denied
            'chat_id': [key for key,value in canais.items()],
            'content':  mensagem_api[0].replace('\n','') + '\n' +\
                        mensagem_api[2].replace('\n','') + '\n\n' +\
                        mensagem_api[8].replace('\n','').replace('[ESTRATEGIA]', estrategia[0]+'|'+estrategia[1]+'|'+estrategia[2]+' - '+estrategia[4]),

            'link_refer':[value[0] for key,value in canais.items()],
            'link_game_bet':['https://m.vembetar.com/ptb/games/livecasino/detail/18372/evol_lkcbrbdckjxajdol_BRL']
    }

    requests.post(url, headers=headers, json=payload)


    ''' Enviando mensagem Telegram '''
    try:
        for key, value in canais.items():
            try:

                with open('mensagens_txt\\alerta.txt',"r", encoding="utf-8") as arquivo:
                    message_alerta = arquivo.read()

                globals()[f'alerta_{key}'] = bot.send_message(key, message_alerta\
                                                              .replace('[LINK_CADASTRO]', value[0])\
                                                              .replace('[ESTRATEGIA]', estrategia[0]+'|'+estrategia[1]+'|'+estrategia[2]+' - '+estrategia[4]), 
                                                              parse_mode='HTML', disable_web_page_preview=True)  #Variavel Dinâmica


            except:
                pass

    except:
        pass

    contador_passagem = 1


def enviarSinalTelegram(nome_cassino, sequencia_minima, estrategia, nome_fornecedor, ultimo_resultado):
    global table_sinal
    
    ''' Lendo o arquivo txt canais '''
    txt = open("canais.txt", "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[12].replace('canais= ','').replace('\n','')
    canais = ast.literal_eval(canais) # Convertendo string em dicionario 
    
    ''' Lendo o arquivo txt config-mensage/ns '''
    txt = open("mensagens_txt\\sinal.txt", "r", encoding="utf-8")
    mensagem_api = txt.readlines()

    #ENVIANDO POST PARA A API
    payload = {
            'status': 'confirm', #alert | confirm | success | failure | denied
            'chat_id': [key for key,value in canais.items()],
            'content':  mensagem_api[0].replace('\n','') + '\n' +\
                        mensagem_api[2].replace('\n','') + '\n\n' +\
                        mensagem_api[6].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(dicionario_roletas[nome_cassino][:int(sequencia_minima)])) + '\n' +\
                        mensagem_api[8].replace('\n','').replace('[ULTIMO_RESULTADO]', ultimo_resultado) + '\n' +\
                        mensagem_api[9].replace('\n','').replace('[APOSTA]', estrategia[4].upper()) + '\n' +\
                        mensagem_api[10].replace('\n','') + '\n' +\
                        mensagem_api[16].replace('\n','').replace('[ESTRATEGIA]', estrategia[0]+'|'+estrategia[1]+'|'+estrategia[2]+' - '+estrategia[4]),

            'link_refer':[value[0] for key,value in canais.items()],
            'link_game_bet':['https://m.vembetar.com/ptb/games/livecasino/detail/18372/evol_lkcbrbdckjxajdol_BRL']
    }

    requests.post(url, headers=headers, json=payload)


    ''' Enviando mensagem Telegram '''
    try:
        for key,value in canais.items():
            try:
                ''' Lendo o arquivo txt config-mensagens '''
                with open('mensagens_txt\\sinal.txt',"r", encoding="utf-8") as arquivo:
                    message_sinal = arquivo.read()


                bot.delete_message(key, globals()[f'alerta_{key}'].message_id)
                globals()[f'sinal_{key}'] = bot.send_message(key, message_sinal\
                                                             .replace('[LISTA_RESULTADOS]', ' | '.join(dicionario_roletas[nome_cassino][:int(sequencia_minima)]))
                                                             .replace('[ULTIMO_RESULTADO]', ultimo_resultado)
                                                             .replace('[APOSTA]', estrategia[4].upper())
                                                             .replace('[LINK_CADASTRO]', value[0])
                                                             .replace('[ESTRATEGIA]', estrategia[0]+'|'+estrategia[1]+'|'+estrategia[2]+' - '+estrategia[4])
                                                             , parse_mode='HTML', disable_web_page_preview=True)

            except:
                pass

    except:
        pass


def apagaAlertaTelegram():
    global contador_passagem

    ''' Lendo o arquivo txt canais '''
    txt = open("canais.txt", "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[12].replace('canais= ','').replace('\n','')
    canais = ast.literal_eval(canais) # Convertendo string em dicionario 

    #ENVIANDO POST PARA A API
    payload = {
            'status': 'denied', #alert | confirm | success | failure | denied
            'chat_id': [key for key,value in canais.items()],
            'content': ['Entrada Não Confirmada'],
            'link_refer':['Entrada Não Confirmada'],
            'link_game_bet':['Entrada Não Confirmada']
    }

    requests.post(url, headers=headers, json=payload)

    try:
        for key, value in canais.items():
            try:
                bot.delete_message(key, globals()[f'alerta_{key}'].message_id)
            except:
                pass
    except:
        pass

    contador_passagem = 0


def checar_sinal_enviado(lista_resultados, nome_cassino, ultimos_resultados):
    global table_sinal
    global placar_win
    global placar_semGale
    global placar_gale1
    global placar_gale2
    global placar_gale3
    global placar_loss
    global resultados_sinais
    global ultimo_horario_resultado
    global validador_sinal
    global stop_loss
    global estrategia
    global contador_passagem
    global sequencia_minima

    resultados = []
    contador_cash = 0

    while contador_cash <= 2:

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass

        # Validando o horario para envio do relatório diário
        validaData()


        try:
            
            ultimo_result = ws.recv()
                
            if 'roulette.winSpots' in ultimo_result:
                try:

                    ultimo_resultado = json.loads(ultimo_result)['args']['code']
                    lista_resultados.insert(0, ultimo_resultado)
                    #print(lista_resultados_sinal)
                    
                except:
                    ultimo_valor_armazenado = ultimo_result
                    continue
            else:
                ultimo_valor_armazenado = ultimo_result
                continue
            
            dicionario_roletas[nome_cassino] = lista_resultados

            resultados.append(lista_resultados[0])
            
            grupo_apostar = apostasExternas(estrategia[4], dic_estrategia_usuario)
           
            print(ultimo_resultado)
           
           # VALIDANDO WIN OU LOSS
            if lista_resultados[0] in grupo_apostar[estrategia[4]] or lista_resultados[0] == '0' or lista_resultados[0] == '00':
                
                # validando o tipo de WIN
                if contador_cash == 0:
                    print('WIN SEM GALE')
                    stop_loss.append('win')

                    # Atualizando placar e Alimentando o arquivo txt
                    placar_win +=1
                    placar_semGale +=1
                    placar_geral = placar_win + placar_loss

                    with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                        arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}")

                    print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
                    #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                    try:
                        # Somando Win na estratégia da lista atual
                        for pe in placar_estrategias:
                            if pe[:-5] == [estrategia[1].upper()]:
                                pe[-5] = int(pe[-5])+1
                    except:
                        pass
                    
                    
                    if lista_roletas != []:
                        # Somando Win na roleta atual
                        for pr in placar_roletas:
                            if pr[:-5] == [nome_cassino.upper()]:
                                pr[-5] = int(pr[-5])+1

                    

                if contador_cash == 1:
                    print('WIN GALE1')
                    stop_loss.append('win')

                    # Atualizando placar e Alimentando o arquivo txt
                    placar_win +=1
                    placar_gale1 +=1
                    placar_geral = placar_win + placar_loss
                    with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                        arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}")
                        
                    print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
                    #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                    try:
                        # Somando Win na estratégia da lista atual
                        for pe in placar_estrategias:
                            if pe[:-5] == [estrategia[1].upper()]:
                                pe[-4] = int(pe[-4])+1

                        if lista_roletas != []:
                            # Somando Win na roleta atual
                            for pr in placar_roletas:
                                if pr[:-5] == [nome_cassino.upper()]:
                                    pr[-4] = int(pr[-4])+1
                    except:
                        pass


                if contador_cash == 2:
                    print('WIN GALE2')
                    stop_loss.append('win')
                    
                    # Atualizando placar e Alimentando o arquivo txt
                    placar_win +=1
                    placar_gale2 +=1
                    placar_geral = placar_win + placar_loss
                    with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                        arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}")
            
                    print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
                    #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)
                    
                    try:
                        # Somando Win na estratégia da lista atual
                        for pe in placar_estrategias:
                                if pe[:-5] == [estrategia[1].upper()]:
                                    pe[-3] = int(pe[-3])+1
                    except:
                        pass
                    
                    if lista_roletas != []:
                        # Somando Win na roleta atual
                        for pr in placar_roletas:
                                if pr[:-5] == [nome_cassino.upper()]:
                                    pr[-3] = int(pr[-3])+1

            
                # editando mensagem enviada
                try:
                    ''' Lendo o arquivo txt canais '''
                    txt = open("canais.txt", "r", encoding="utf-8")
                    arquivo = txt.readlines()
                    canais = arquivo[12].replace('canais= ','').replace('\n','')
                    canais = ast.literal_eval(canais) # Convertendo string em dicionario 

                    ''' Lendo o arquivo txt config-mensage/ns '''
                    txt = open("mensagens_txt\\green.txt", "r", encoding="utf-8")
                    mensagem_api = txt.readlines()

                    #ENVIANDO POST PARA A API
                    payload = {
                            'status': 'success', #alert | confirm | success | failure | denied
                            'chat_id': [key for key,value in canais.items()],
                            'content':  mensagem_api[0].replace('\n','') + '\n' +\
                                        mensagem_api[2].replace('\n','').replace('[LISTA_RESULTADOS]', ultimos_resultados) + '\n\n' +\
                                        mensagem_api[4].replace('\n','').replace('[APOSTA]', estrategia[4].upper()) + '\n' +\
                                        mensagem_api[5].replace('\n','').replace('[RESULTADO]', ' | '.join(resultados)) + '\n' +\
                                        mensagem_api[7].replace('\n','') + '\n' +\
                                        mensagem_api[8].replace('\n','') + '\n' +\
                                        mensagem_api[12].replace('\n','').replace('[ESTRATEGIA]', estrategia[0]+'|'+estrategia[1]+'|'+estrategia[2]+' - '+estrategia[4]),

                            'link_refer':[value[0] for key,value in canais.items()],
                            'link_game_bet':['https://m.vembetar.com/ptb/games/livecasino/detail/18372/evol_lkcbrbdckjxajdol_BRL']
                    }

                    requests.post(url, headers=headers, json=payload)

                    for key,value in canais.items():
                        try:
                            ''' Lendo o arquivo txt config-mensagens '''
                            with open('mensagens_txt\\green.txt',"r", encoding="utf-8") as arquivo:
                                message_green = arquivo.read()

                            bot.delete_message(key, globals()[f'sinal_{key}'].message_id)
                            bot.send_message(key, message_green\
                                                    .replace('[LISTA_RESULTADOS]', ultimos_resultados)
                                                    .replace('[APOSTA]', estrategia[4].upper())
                                                    .replace('[RESULTADO]', ' | '.join(resultados))
                                                    .replace('[LINK_CADASTRO]', value[0])
                                                    .replace('[ESTRATEGIA]', estrategia[0]+'|'+estrategia[1]+'|'+estrategia[2]+' - '+estrategia[4])
                                                    , parse_mode='HTML')
                                                                                            
                        except:
                            pass

                except:
                    pass
                

                print('==================================================')
                validador_sinal = 0
                contador_cash = 0
                contador_passagem = 0
                return

        

            else:
                print('LOSSS')
                print('==================================================')
                contador_cash+=1
                continue


        except Exception as e:

            if e.args[0] == 'socket is already closed.':
                conectar_websocket(evosessionid)

            else:
                print(e)
                evosessionid = pegar_evosessionid()
                conectar_websocket(evosessionid)
                continue
            


    if contador_cash == 3:
        print('LOSSS GALE2')
        stop_loss.append('loss')

        # Preenchendo arquivo txt
        placar_loss +=1
        placar_geral = placar_win + placar_loss
        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
            arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}")
        
        ''' Lendo o arquivo txt config-mensage/ns '''
        txt = open("mensagens_txt\\red.txt", "r", encoding="utf-8")
        mensagem_api = txt.readlines()

        #ENVIANDO POST PARA A API
        payload = {
                'status': 'failure', #alert | confirm | success | failure | denied
                'chat_id': [key for key,value in canais.items()],
                'content':  mensagem_api[0].replace('\n','') + '\n' +\
                            mensagem_api[2].replace('\n','').replace('[LISTA_RESULTADOS]', ultimos_resultados) + '\n\n' +\
                            mensagem_api[4].replace('\n','').replace('[APOSTA]', estrategia[4].upper()) + '\n' +\
                            mensagem_api[5].replace('\n','').replace('[RESULTADO]', ' | '.join(resultados)) + '\n' +\
                            mensagem_api[7].replace('\n','') + '\n' +\
                            mensagem_api[8].replace('\n','') + '\n' +\
                            mensagem_api[12].replace('\n','').replace('[ESTRATEGIA]', estrategia[0]+'|'+estrategia[1]+'|'+estrategia[2]+' - '+estrategia[4]),

                'link_refer':[value[0] for key,value in canais.items()],
                'link_game_bet':['https://m.vembetar.com/ptb/games/livecasino/detail/18372/evol_lkcbrbdckjxajdol_BRL']
        }

        requests.post(url, headers=headers, json=payload)
        
        # editando mensagem
        try:
            ''' Lendo o arquivo txt canais '''
            txt = open("canais.txt", "r", encoding="utf-8")
            arquivo = txt.readlines()
            canais = arquivo[12].replace('canais= ','').replace('\n','')
            canais = ast.literal_eval(canais) # Convertendo string em dicionario 

            for key,value in canais.items():
                try:
                    ''' Lendo o arquivo txt config-mensagens '''
                    with open('mensagens_txt\\red.txt',"r", encoding="utf-8") as arquivo:
                        message_red = arquivo.read()

                    bot.delete_message(key, globals()[f'sinal_{key}'].message_id)
                    bot.send_message(key, message_red\
                                            .replace('[LISTA_RESULTADOS]', ultimos_resultados)
                                            .replace('[APOSTA]', estrategia[4].upper())
                                            .replace('[RESULTADO]', ' | '.join(resultados))
                                            .replace('[LINK_CADASTRO]', value[0])
                                            .replace('[ESTRATEGIA]', estrategia[0]+'|'+estrategia[1]+'|'+estrategia[2]+' - '+estrategia[4])
                                            , parse_mode='HTML')
                except:
                    pass


            print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
        
        except:
            pass


        ''' Alimentando "Gestão" estratégia e roleta '''
        try:
            # Somando Win na estratégia da lista atual
            for pe in placar_estrategias:
                if pe[:-5] == [estrategia[1].upper()]:
                    pe[-1] = int(pe[-1])+1
            

            # Somando Win na roleta atual
            for pr in placar_roletas:
                if pr[:-5] == [nome_cassino.upper()]:
                    pr[-1] = int(pr[-1])+1
        except:
            pass

        
        
        # Validando o stop_loss
        if 'win' in stop_loss:
            stop_loss = []
            stop_loss.append('loss')
        

        print('==================================================')
        validador_sinal = 0
        contador_cash = 0
        contador_passagem = 0
        return


inicio()
placar()            # Gerando o Placar

#________________________________________________________________________________________ TELEGRAM__________________________________________________________________________________#



print('############################################################# AGUARDANDO COMANDOS #############################################################')

global canal
global bot
global placar_win
global placar_semGale
global placar_gale1
global placar_gale2
global placar_gale3
global placar_loss
global resultados_sinais

#CHAVE_API = '5651549126:AAFaVyaQkxTTVPq9WxpIBejBMR_oUPdt_5o' # DEV
#CHAVE_API = '5798408552:AAF-HyDxLlj_07r-O6JgtKT5HZetxtAeKJ4' # PRODUÇÃO



# PLACAR
placar_win = 0
placar_semGale= 0
placar_gale1= 0
placar_gale2= 0
placar_gale3= 0
placar_loss = 0
resultados_sinais = placar_win + placar_loss
estrategias = []
placar_estrategia = []
placar_estrategias = []
estrategias_diaria = []
placar_estrategias_diaria = []
contador = 0
botStatus = 0
validador_sinal = 0
parar = 0
dic_estrategia_usuario = {}
lista_seq_minima = []
lista_onde_apostar = []
lista_roletas = []
placar_roletas = []
roletas_diaria = []
placar_roletas_diaria = []
contador_passagem = 0
lista_ids = []
lista_estrategias = []
dicionario_roletas = {}



# LENDO TXT PARA DEFINIR VARIAVEL FREE E VIP E VALIDAÇÃO DE USUÁRIO
txt = open("canais.txt", "r", encoding="utf-8")
arquivo = txt.readlines()
usuario = arquivo[2].split(' ')[1]
senha = arquivo[3].split(' ')[1].split('\n')[0]
CHAVE_API = arquivo[7].split(' ')[1].split('\n')[0]

ids = arquivo[11].split(' ')[1].split('\n')[0]
canais = arquivo[12].split(' ')[1].split('\n')[0].split((','))
bot = telebot.TeleBot(CHAVE_API)

global message



''' FUNÇÕES BOT ''' ##



def generate_buttons_estrategias(bts_names, markup):
    for button in bts_names:
        markup.add(types.KeyboardButton(button))
    return markup



def pausarBot():
    global parar
    global browser

    while True:
        try:
            parar = 1
            return 

        except:
            continue


@bot.message_handler(commands=['⏲ Ultimos_Resultados'])
def ultimosResultados(message):
    
    if botStatus != 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        bot.reply_to(message, "🤖 Ok! Mostrando Ultimos Resultados das Roletas", reply_markup=markup)
        try:
            
            for key, value in dicionario_roletas.items():
                #print(key, value)
                bot.send_message(message.chat.id, f'{key}{value}')

        except:
            pass
    

    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Ative o bot primeiro! ", reply_markup=markup)


@bot.message_handler(commands=['⚙🧠 Cadastrar_Estratégia'])
def cadastrarEstrategia(message):
    global contador_passagem

    if contador_passagem == 0:
        #Init keyboard markup
        markup_tipo = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
        
        markup_tipo = markup_tipo.add('◀ Voltar', 'REPETIÇÃO', 'AUSÊNCIA', 'ESTRATÉGIAS PADRÕES')    

        message_tipo_estrategia = bot.reply_to(message, "🤖 Ok! Escolha o tipo de estratégia 👇", reply_markup=markup_tipo)
        bot.register_next_step_handler(message_tipo_estrategia, registrarTipoEstrategia)
    

    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_estrategia = bot.reply_to(message, "🤖⛔ Estou validando uma estratégia! Tente novamente em alguns instanstes.", reply_markup=markup)



@bot.message_handler(commands=['🗑🧠 Apagar_Estratégia'])
def apagarEstrategia(message):
    global estrategia
    global estrategias
    global contador_passagem

    print('Excluir estrategia')

    if contador_passagem == 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        #Add to buttons by list with ours generate_buttons function.
        markup_estrategias = generate_buttons_estrategias([f'{estrategia}' for estrategia in estrategias], markup)    
        markup_estrategias.add('◀ Voltar')

        message_excluir_estrategia = bot.reply_to(message, "🤖 Escolha a estratégia a ser excluída 👇", reply_markup=markup_estrategias)
        bot.register_next_step_handler(message_excluir_estrategia, registrarEstrategiaExcluida)
    
    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_excluir_estrategia = bot.reply_to(message, "🤖⛔ Estou validando uma estratégia! Tente novamente em alguns instanstes.", reply_markup=markup)



@bot.message_handler(commands=['🧠📜 Estratégias_Cadastradas'])
def estrategiasCadastradas(message):
    global estrategia
    global estrategias
    global lista_estrategias

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    if lista_estrategias != []:
        bot.reply_to(message, "🤖 Ok! Listando estratégias", reply_markup=markup)

        for estrategia in lista_estrategias:
            #print(estrategia)
            bot.send_message(message.chat.id, f'{estrategia}')
    
    else:
        bot.reply_to(message, "🤖 Nenhuma estratégia cadastrada ❌", reply_markup=markup)



@bot.message_handler(commands=['🎰📜 Roletas_Cadastradas'])
def roletasCadastradas(message):
    global estrategia
    global estrategias
    global lista_roletas

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    if lista_roletas != []:
        bot.reply_to(message, "🤖 Ok! Listando Roletas", reply_markup=markup)

        for roletta in lista_roletas:
            #print(estrategia)
            bot.send_message(message.chat.id, f'{roletta}')
    
    else:
        bot.reply_to(message, "🤖 Nenhuma Roleta cadastrada pelo usuário. Com isso, todas as roletas do grupo Evolution serão analisadas 🚨‼", reply_markup=markup)





@bot.message_handler(commands=['📈 Gestão'])
def gestao(message):
    global placar
    global resultados_sinais
    global placar_estrategias

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    if placar_estrategias != []:
        ''' Enviando Relatório das estratégias'''
        for pe in placar_estrategias:
            total = int(pe[-5]) + int(pe[-4]) + int(pe[-3]) + int(pe[-2]) + int(pe[-1])
            soma_win = int(pe[-5]) + int(pe[-4]) + int(pe[-3]) + int(pe[-2])

            try:
                assertividade = str(round(soma_win / total*100, 1)).replace('.0',"")+"%"
            except:
                assertividade = '0%'

            bot.send_message(message.chat.id, f'🧠 {pe[:-5]} \n==========================\n 🏆= {pe[-5]}  |  🥇= {pe[-4]}  |  🥈= {pe[-3]}  |  🥉= {pe[-2]} \n\n ✅ - {soma_win} \n ❌ - {pe[-1]} \n==========================\n 🎯 {assertividade}  ', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, '🤖 Nenhuma estratégia cadastrada ⛔')


    if lista_roletas != []:
        ''' Enviando Relatório das Roletas'''
        for pr in placar_roletas:
            total = int(pr[-5]) + int(pr[-4]) + int(pr[-3]) + int(pr[-2]) + int(pr[-1])
            soma_win = int(pr[-5]) + int(pr[-4]) + int(pr[-3]) + int(pr[-2])

            try:
                assertividade = str(round(soma_win / total*100, 1)).replace('.0',"")+"%"
            except:
                assertividade = '0%'

            bot.send_message(message.chat.id, f'🎰 {pr[:-5]} \n==========================\n 🏆= {pr[-5]}  |  🥇= {pr[-4]}  |  🥈= {pr[-3]}  |  🥉= {pr[-2]} \n\n ✅ - {soma_win} \n ❌ - {pr[-1]} \n==========================\n 🎯 {assertividade}  ', reply_markup=markup)
    
    else:
        bot.send_message(message.chat.id, '🤖 Só consigo gerar a gestão das roletas quando a mesma é cadastrada na opção *Cadastrar Roleta*')

    


@bot.message_handler(commands=['📊 Placar Atual'])
def placar_atual(message):
    global placar
    global resultados_sinais

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    ''' Enviando mensagem Telegram '''
    try:
        placar()

        resposta = bot.reply_to(message,\
        "📊 Placar Atual do dia "+data_hoje+":\n\
        =====================\n\
        😍 WIN - "+str(placar_win)+"\n\
        🏆 WIN S/ GALE - "+str(placar_semGale)+"\n\
        🥇 WIN GALE1 - "+str(placar_gale1)+"\n\
        🥈 WIN GALE2 - "+str(placar_gale2)+"\n\
        😭 LOSS - "+str(placar_loss)+"\n\
        =====================\n\
        🎯 Assertividade "+ asserividade, reply_markup=markup)
    
    except Exception as a:
        logger.error('Exception ocorrido no ' + repr(a))
        #placar = bot.reply_to(message,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%", reply_markup=markup)
        pass



@bot.message_handler(commands=['🛑 Pausar_bot'])
def pausar(message):
    global botStatus
    global validador_sinal
    global browser
    global parar

    if validador_sinal != 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Estou validando um Sinal. Tente novamente em alguns instanstes.", reply_markup=markup)

    elif botStatus == 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Bot já está pausado ", reply_markup=markup)

    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        print('\n\n')
        print('Pausar Bot')
        print('Parando o Bot....\n')
        botStatus = 0
        parar = 1
        #pausarBot()

        message_final = bot.reply_to(message, "🤖 Ok! Bot pausado 🛑", reply_markup=markup)
        
        print('###################### AGUARDANDO COMANDOS ######################')
        
        return




@bot.message_handler(commands=['start'])
def start(message):

    if str(message.chat.id) in ids:

        ''' Add id na lista de ids'''
        if str(message.chat.id) not in lista_ids:
            lista_ids.append(message.chat.id)
        else:
            pass
       
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message, "🤖 Bot Speed Roulette Vem Betar Iniciado! ✅ Escolha uma opção 👇",
                                    reply_markup=markup)
        
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(message_opcoes, opcoes)
    
    else:
        message_error = bot.reply_to(message, "🤖 Você não tem permissão para acessar este Bot ❌🚫")




@bot.message_handler()
def opcoes(message_opcoes):

    if message_opcoes.text in ['✅ Ativar Bot']:
        global message_canal
        global placar
        global estrategia
        global stop_loss
        global botStatus
        global parar
        global reladiarioenviado
        global contador_outra_oportunidade
        global browser
        global dicionario_estrategia_usuario
        global contador_passagem

        print('Ativar Bot')

        if botStatus == 1:

            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖⛔ Bot já está ativado",
                                reply_markup=markup)

        
        elif lista_estrategias == []:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖⛔ Cadastre no mínimo 1 estratégia antes de iniciar",
                                reply_markup=markup)

        
        else:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖 Ok! Bot Ativado com sucesso! ✅ Em breve receberá sinais nos canais informados no arquivo auxiliar! ",
                                    reply_markup=markup)
            
            botStatus = 1
            reladiarioenviado = 0
            parar=0
            contador_passagem = 0
            stop_loss = []

            print('##################################################  INICIANDO AS ANÁLISES  ##################################################')
            print()
            
            coletarResultados() # Analisando os Dados



    
    if message_opcoes.text in['📊 Placar Atual']:
        print('Placar Atual')
        placar_atual(message_opcoes)


    if message_opcoes.text in ['🛑 Pausar Bot']:
        print('Pausar Bot')
        pausar(message_opcoes)

    
    if message_opcoes.text in ['⚙🧠 Cadastrar Estratégia']:
        print('Cadastrar Estratégia')
        cadastrarEstrategia(message_opcoes)


    if message_opcoes.text in ['🧠📜 Estratégias Cadastradas']:
        print('Estratégias Cadastradas')
        estrategiasCadastradas(message_opcoes)


    if message_opcoes.text in ['🗑🧠 Apagar Estratégia']:
        print('Excluir Estratégia')
        apagarEstrategia(message_opcoes)
    

    if message_opcoes.text in['📈 Gestão']:
            print('Gestão')
            gestao(message_opcoes)


    if message_opcoes.text in ['⏲ Ultimos Resultados']:
        print('Ultimos Resultados')
        ultimosResultados(message_opcoes)


    if message_opcoes.text in ['🎰📜 Roletas Cadastradas']:
        print('Roletas Cadastradas')
        roletasCadastradas(message_opcoes)   



@bot.message_handler()
def registrarTipoEstrategia(message_tipo_estrategia):
    global resposta_usuario

    if message_tipo_estrategia.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_tipo_estrategia, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        return




    if message_tipo_estrategia.text in ['ESTRATÉGIAS PADRÕES']:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')
        
        estrategias_padroes = (
                                
                               ['1ºcoluna', '1ºcoluna', '1ºcoluna', '3', '2ª/3ªcoluna'], 
                               ['1ºcoluna', '1ºcoluna', '2ªcoluna', '3', '1º/3ªcoluna'], 
                               ['1ºcoluna', '1ºcoluna', '3ªcoluna', '3', '1º/2ªcoluna'],

                               ['2ªcoluna', '2ªcoluna', '2ªcoluna', '3', '1º/3ªcoluna'], 
                               ['2ªcoluna', '2ªcoluna', '1ºcoluna', '3', '2ª/3ªcoluna'], 
                               ['2ªcoluna', '2ªcoluna', '3ªcoluna', '3', '1º/2ªcoluna'],

                               ['3ªcoluna', '3ªcoluna', '3ªcoluna', '3', '1º/2ªcoluna'], 
                               ['3ªcoluna', '3ªcoluna', '1ºcoluna', '3', '2ª/3ªcoluna'], 
                               ['3ªcoluna', '3ªcoluna', '2ªcoluna', '3', '1º/3ªcoluna'],

                               ['1ºcoluna', '1ºcoluna', '0', '3', '2ª/3ªcoluna'], 
                               ['2ªcoluna', '2ªcoluna', '0', '3', '1º/3ªcoluna'], 
                               ['3ªcoluna', '3ªcoluna', '0', '3', '1º/2ªcoluna'],    
                       
                               
                               )

        for estrategia_padrao in estrategias_padroes:
            lista_estrategias.append(estrategia_padrao)
            placar_estrategia = [estrategia_padrao[1]]
            placar_estrategia.extend([0,0,0,0,0])
            placar_estrategias.append(placar_estrategia)


        message_aposta = bot.reply_to(message_tipo_estrategia, "🤖 Estratégias Cadastradas ✅", reply_markup=markup)





    else:

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

        resposta_usuario = message_tipo_estrategia.text.lower()
        print(resposta_usuario)
        
        apostas()
        markup_apostas = generate_buttons_estrategias([f'{aposta.upper()}' for aposta in opcoes_apostas], markup)    
        markup_apostas.add('◀ Voltar')

        message_aposta = bot.reply_to(message_tipo_estrategia, "🤖 Ok! Agora escolha o tipo de aposta externa 👇", reply_markup=markup_apostas)
        bot.register_next_step_handler(message_aposta, registrarApostaExterna)




def registrarApostaExterna(message_aposta):
    global estrategia
    global estrategias
    global placar_estrategia
    global placar_estrategias
    global placar_estrategias_diaria
    global estrategias_diaria
    global resposta_usuario
    global resposta_usuario2
    global resposta_usuario3
    global resposta_usuario4
    global dicionario_estrategia_usuario

    if message_aposta.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_aposta, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        return


    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

        ''' Buscando o dicionario da aposta definida pelo usuario '''
        resposta_usuario2 = message_aposta.text.lower()
        #dicionario_estrategia_usuario = apostasExternas(resposta_usuario2, dic_estrategia_usuario)

        ''' Placar da estratégia '''
        placar_estrategia = list([message_aposta.text])
        placar_estrategia.extend([0,0,0,0,0])

        # Adicionando estratégia na lista de estratégias
        estrategias.append(message_aposta.text)
        placar_estrategias.append(placar_estrategia)

        # Acumulando estratégia do dia
        estrategias_diaria.append(message_aposta.text)
        placar_estrategias_diaria.append(placar_estrategia)

        markup_voltar = markup.add('◀ Voltar')
        seq_minima = bot.reply_to(message_aposta, "🤖 Agora escolha um número que será a sequencia MÍNIMA necessária para que eu possa enviar o sinal ", reply_markup=markup_voltar)
        bot.register_next_step_handler(seq_minima, registraSequenciaMinima)




def registraSequenciaMinima(seq_minima):
    global sequencia_minima
    global resposta_usuario
    global resposta_usuario2
    global resposta_usuario3
    global resposta_usuario4

    if seq_minima.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup_apostas = generate_buttons_estrategias([f'{aposta.upper()}' for aposta in opcoes_apostas], markup)    
        markup_apostas.add('◀ Voltar')

        ''' Excluindo a estratégia '''
        estrategias.remove(resposta_usuario2.upper())

        message_estrategia = bot.reply_to(seq_minima, "🤖 Ok! Escolha o tipo de aposta externa 👇", reply_markup=markup_apostas)
        bot.register_next_step_handler(message_estrategia, registrarApostaExterna)
        


    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        
        resposta_usuario3 = seq_minima.text
        sequencia_minima = ([resposta_usuario, resposta_usuario2, int(resposta_usuario3)])
        lista_seq_minima.append(sequencia_minima)
        print(sequencia_minima)

        markup_apostas = generate_buttons_estrategias([f'{aposta.upper()}' for aposta in opcoes_apostas], markup)    
        markup_apostas.add('◀ Voltar')

        ond_apostar = bot.reply_to(seq_minima, "🤖 Perfeito! Agora, quando o sinal for enviado para o Canal, onde os jogadores irão apostar?", reply_markup=markup_apostas)
        bot.register_next_step_handler(ond_apostar, registraOndeApostar)




def registraOndeApostar(ond_apostar):
    global onde_apostar
    global resposta_usuario
    global resposta_usuario2
    global resposta_usuario3
    global resposta_usuario4
    global lista_estrategias

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    resposta_usuario4 = ond_apostar.text.lower()
    onde_apostar = ([resposta_usuario, resposta_usuario2, resposta_usuario3, resposta_usuario4])
    lista_estrategias.append(onde_apostar)
    print(onde_apostar)
    bot.reply_to(ond_apostar, "🤖 Estratégia Cadastrada ✅", reply_markup=markup)




def registrarEstrategiaExcluida(message_excluir_estrategia):
    global estrategia
    global estrategias

    if message_excluir_estrategia.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_excluir_estrategia, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        
        return
    

    estrategia_excluir = message_excluir_estrategia.text
    
    ''' Excluindo a estratégia '''
    for estrategia in estrategias:
        if estrategia_excluir == str(estrategia):
            estrategias.remove(estrategia)

    ''' Excluindo o placar da estratégia'''
    for pe in placar_estrategias:
        if estrategia_excluir == pe[0]:
            placar_estrategias.remove(pe)

    ''' Excluindo da lista consolidada '''
    for estrate in lista_estrategias:
        if estrate[1] == estrategia_excluir.lower():
            lista_estrategias.remove(estrate)



    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    bot.reply_to(message_excluir_estrategia, "🤖 Estratégia excluída com sucesso! ✅", reply_markup=markup)




def registrarRoleta(message_roleta):
    global lista_roletas
    global placar_roletas_diaria


    if message_roleta.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_roleta, "🤖 Escolha uma opção 👇", reply_markup=markup)
        return


    ''' Validando se já existe a estrategia cadastrada '''
    if message_roleta.text not in lista_roletas:

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')


        roleta_escolhida = message_roleta.text.lower()

        ''' Placar da Roleta '''
        placar_roleta = list([message_roleta.text])
        placar_roleta.extend([0,0,0,0,0])
        
        # Adicionando estratégia na lista de estratégias
        lista_roletas.append(message_roleta.text)
        placar_roletas.append(placar_roleta)

        # Acumulando estratégia do dia
        roletas_diaria.append(message_roleta.text)
        placar_roletas_diaria.append(placar_roleta)

        bot.reply_to(message_roleta, "🤖 Roleta Cadastrada ✅", reply_markup=markup)

       

    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        bot.reply_to(message_roleta, "🤖 A estratégia "+str(message_roleta.text.upper())+" já foi cadastrada anteriormente ❌", reply_markup=markup)




def registrarRoletaExcluida(message_excluir_roleta):
    global estrategia
    global estrategias

    if message_excluir_roleta.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_excluir_roleta, "🤖 Escolha uma opção 👇", reply_markup=markup)
        return
        
    
    else:

        escolha_usuario = message_excluir_roleta.text
        
        ''' Excluindo a roleta '''
        for roletta in lista_roletas:
            if escolha_usuario == str(roletta):
                lista_roletas.remove(roletta)

        ''' Excluindo o placar da roleta'''
        for pr in placar_roletas:
            if escolha_usuario == pr[0]:
                placar_roletas.remove(pr)

        

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        bot.reply_to(message_excluir_roleta, "🤖 Roleta excluída com sucesso! ✅", reply_markup=markup)




while True:
    try:
        bot.infinity_polling(timeout=600, long_polling_timeout=600)
        bot.infinity_polling(True)
    except:
        pass






