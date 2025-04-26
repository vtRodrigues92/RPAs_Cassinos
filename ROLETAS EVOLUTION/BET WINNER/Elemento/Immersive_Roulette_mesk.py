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
print('                                ################   BOT IMMERSIVE ROULETTE  ######################')
print('                                #################################################################')
print('                                ##################### SEJA BEM VINDO ############################')
print('                                #################################################################')
print('                                ############# DESENVOLVIDO POR VICTOR RODRIGUES #################')
print('                                #################################################################\n')
print('Versão = 1.0.0')
print('Ambiente: Produção\n\n\n')



# THREAD PARA ENVIAR ALERTA TELEGRAM
class enviarAlertaTelegram(threading.Thread):
    def __init__(self, canal, mensagem):
        self.canal = canal
        self.mensagem = mensagem
        threading.Thread.__init__(self)
    
    def run(self):
        
        try:
            globals()[f'alerta_{self.canal}'] = bot.send_message(self.canal, self.mensagem, parse_mode='HTML', disable_web_page_preview=True)  #Variavel Dinâmica

            return globals()[f'alerta_{self.canal}']
        
        except:

            print('NÃO CONSEGUI ENVIAR A MENSAGEM PARA O CANAL', self.canal)

                
# THREAD PARA ENVIAR SINAL TELEGRAM
class enviarSinalTelegram(threading.Thread):
    def __init__(self, canal, mensagem):
        self.canal = canal
        self.mensagem = mensagem
        threading.Thread.__init__(self)
    
    def run(self):
        
        try:

            bot.delete_message(self.canal, globals()[f'alerta_{self.canal}'].message_id)
            
            globals()[f'sinal_{self.canal}'] = bot.send_message(self.canal, self.mensagem, parse_mode='HTML', disable_web_page_preview=True)  #Variavel Dinâmica

            return globals()[f'sinal_{self.canal}']

        except:

            print('NÃO CONSEGUI ENVIAR A MENSAGEM PARA O CANAL', self.canal)


# THREAD PARA APAGAR MENSAGEM TELEGRAM
class apagarMensagemTelegram(threading.Thread):
    def __init__(self, canal):
        self.canal = canal
        threading.Thread.__init__(self)
    
    def run(self):
        
        try:

            bot.delete_message(self.canal, globals()[f'alerta_{self.canal}'].message_id)
        
        except:
            print('NÃO CONSEGUI APAGAR A MENSAGEM DO CANAL', self.canal)


# THREAD PARA ENVIAR SINAL TELEGRAM
class responderMensagemTelegram(threading.Thread):
    def __init__(self, canal, mensagem):
        self.canal = canal
        self.mensagem = mensagem
        threading.Thread.__init__(self)
    
    def run(self):

        try:

            bot.reply_to(globals()[f'sinal_{self.canal}'], self.mensagem, parse_mode='HTML')
        
        except:
            
            print('NÃO CONSEGUI RESPONDER A MENSAGEM DO CANAL', self.canal)

#Fordbracom2022
#Gabriel@2023

#leonardotheo23  
#Fordbracom2023

def pegar_evosessionid():

    while True:
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
        
        response = requests.post(URL, headers=header, json=payload)
        token = response.json()['token']

        ### DADOS ACESSO
        header = {
                    'Content-Type': 'application/json',
                    "authorization": f"bearer {token}"
                    }
        

        payload = {"email":usuario,
                "password":senha}
        

        URL = 'https://backoffice.mesk.bet/api/auth/me'

        response = requests.post(URL, headers=header, json=payload)
        uuid_usuario = response.json()['player']['uuid']

        print(f'uuid_usuario - {uuid_usuario}')
        
        ### ACESSAR GAME
        #Usando o UUID do usuário Logado para Acessar a SMARTSOFT e Pegar o Token
        URL_FORNECEDOR = f'https://pi.njoybingo.com/game.do?token={uuid_usuario}&pn=meskbet&lang=pt&game=EVOLUTION-roulette-7x0b1tgh7agmf6hv&type=CHARGED'
        
        header = {
            "Cookie":"__cf_bm=3Jh53qm2Nk0jMLhr4o6qFi6xPsLgY1TyYvXNopS914Q-1692632575-0-AZS/L9TYPRE8QCCV9Gn7oqJ639E2aK1otHxWemUJXVU9eGTphEY/kDpHFl9jY3lrRhnh98Rh4PKf1sgULGXuoug="
        }

        response = requests.get(URL_FORNECEDOR, allow_redirects=False)

        if response.status_code == 302:
            LOCATION = response.headers.get('location')
            EVOSESSIONID = response.headers.get('location').split('JSESSIONID=')[1]
            print(f'LOCATION - {LOCATION} | EVOSESSIONID - {EVOSESSIONID}')
            break

        else:
            time.sleep(5)
            continue

    ### PEGANDO JSESSIONID
    header = {
                "Accept":'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                "Accept-Encoding":'gzip, deflate, br',
                "Accept-Language":"pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                "Connection":"keep-alive",
                "Cookie":"cdn=https://static.egcdn.com; lang=bp; locale=pt-BR; EVOSESSIONID=q46vrmxdeigoqacorh3qqhv4kxw5tqmdf839e03b37e3ec16d3379d3bd1c645dac3c7e350af184d3b",
                "Host":"wac.evo-games.com",
                "Referer":"https://mesk.bet/",
                "Sec-Ch-Ua":'"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
                "Sec-Ch-Ua-Mobile":"?0",
                "Sec-Ch-Ua-Platform":"Windows",
                "Sec-Fetch-Dest":"iframe",
                "Sec-Fetch-Mode":"navigate",
                "Sec-Fetch-Site":"cross-site",
                "Sec-Fetch-User":"?1",
                "Upgrade-Insecure-Requests":"1",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
                }
    
    evosessionid = requests.get(LOCATION, headers=header, allow_redirects=False).headers.get('Set-Cookie').split('EVOSESSIONID=')[1].split('; Path')[0]




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
    "Cookie":f"EVOSESSIONID={evosessionid}; cdn=https://static.egcdn.com; lang=bp; locale=pt-BR",
    "Host": "wac.evo-games.com",
    "Origin": "https://wac.evo-games.com",
    "Pragma": "no-cache",
    "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
    "Sec-WebSocket-Key": "zLcUYCrCuWycniSU5ynLiA==",
    "Sec-WebSocket-Version": "13",
    "Upgrade": "websocket",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"

    }

   
    URL = f'wss://wac.evo-games.com/public/roulette/player/game/7x0b1tgh7agmf6hv/socket?messageFormat=json&instance=l474op-rh3izqmfkxw5dt5p-7x0b1tgh7agmf6hv&tableConfig=&EVOSESSIONID={evosessionid}&client_version=6.20230811.72855.29328-3b257f829b'
    
    ws = create_connection(URL)

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

            '1ª coluna': ['1', '4', '7', '10', '13', '16', '19', '22', '25', '28', '31', '34'],
            '2ª coluna': ['2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32', '35'],
            '3ª coluna': ['3', '6', '9', '12', '15', '18', '21', '24', '27', '30', '33', '36'],

            '1ª duzia': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
            '2ª duzia': ['13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'],
            '3ª duzia': ['25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36'],

            'cor vermelho': ['1', '3', '5', '7', '9', '12', '14', '16', '18', '19', '21', '23', '25', '27', '30', '32', '34', '36'],
            'cor preto': ['2', '4', '6', '8', '10', '11', '13', '15', '17', '20', '22', '24', '26', '28', '29', '31', '33', '35'],

            'números par(es)': ['2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24', '26', '28', '30', '32', '34', '36'],
            'números impar(es)': ['1', '5', '7', '9', '11', '13', '15', '17', '19', '21', '23', '25', '27', '29', '31', '33', '35'],

            'números baixos': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18'],
            'números altos': ['19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36'],

            '1ª/2ª coluna': ['1', '4', '7', '10', '13', '16', '19', '22', '25', '28', '31', '34', '2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32', '35'],
            '2ª/3ª coluna': ['2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32', '35', '3', '6', '9', '12', '15', '18', '21', '24', '27', '30', '33', '36'],
            '1ª/3ª coluna': ['1', '4', '7', '10', '13', '16', '19', '22', '25', '28', '31', '34', '3', '6', '9', '12', '15', '18', '21', '24', '27', '30', '33', '36'],

            '1ª/2ª duzia': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'],
            '2ª/3ª duzia': ['13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36'],
            '1ª/3ª duzia': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36']

        }

        for opcao_aposta in opcoes_apostas:
            if estrategia_usuario == opcao_aposta:
                dic_estrategia_usuario[opcao_aposta] = opcoes_apostas[opcao_aposta]
                break
                #print(dic_estrategia_usuario)
        
        return dic_estrategia_usuario
    
    except:
        pass
     

def validarEstrategiaAlerta(dicionario_roletas, nome_cassino, aposta_externa, sequencia_minima, estrategia):

    validador = []
    for n in range(int(sequencia_minima)-1):

        if estrategia[0] == 'repetição':
            if dicionario_roletas[nome_cassino][n] in aposta_externa[estrategia[1]]:
                validador.append('true')

        if estrategia[0] == 'ausência':
            if dicionario_roletas[nome_cassino][n] not in aposta_externa[estrategia[1]]:
                validador.append('true')

    
    return validador


def coletarResultados():
    global dicionario_roletas
    global contador_passagem
    global horario_atual
    global nome_fornecedor
    global lista_resultados, nome_cassino

    nome_cassino = 'Immersive Roulette'
    nome_fornecedor = 'Evolution'
    lista_resultados = []
    dicionario_roletas = {}
    #site_cassino_desktop = 'https://vembetar.com/ptb/games/livecasino/detail/normal/18372/evol_lkcbrbdckjxajdol_BRL'
    #site_cassino_mobile = 'https://m.vembetar.com/ptb/games/livecasino/detail/18372/evol_lkcbrbdckjxajdol_BRL'

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
            #leonardotheo23
            #Fordbracom2023
            #taniaevelyn23
            #Fordbracom2023
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

            ''' Pegando o tipo de aposta (AUSENCIA OU REPETIÇÃO '''
            tipo_aposta = estrategia[0]

            ''' Pegando os números da aposta externa da estratégia'''
            aposta_externa = apostasExternas(estrategia[1], dic_estrategia_usuario)

            ''' Pegando a sequencia minima da estratégia cadastrada pelo usuário '''
            sequencia_minima = estrategia[2]
            
            print('Analisando a Estrategia --> ', estrategia)
            print('Historico_Roleta --> ', nome_cassino, dicionario_roletas[nome_cassino][:int(sequencia_minima)])

            
            ''' Verifica se os números da seq minima do historico da roleta está dentro da estratégia '''
            validador = validarEstrategiaAlerta(dicionario_roletas, nome_cassino, aposta_externa, sequencia_minima, estrategia)
            
            ''' Validando se bateu alguma condição'''
            if validador.count('true') == int(sequencia_minima)-1:
                print('IDENTIFICADO PRÉ PADRÃO NA ROLETA ', nome_cassino, ' COM A ESTRATÉGIA ', estrategia)
                print('ENVIAR ALERTA')
                enviar_alerta_telegram(dicionario_roletas, nome_cassino, sequencia_minima, estrategia, nome_fornecedor)
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

                        if estrategia[0] == 'repetição':
                            ''' Verificando se o ultimo resultado da roleta está dentro da estratégia'''
                            if lista_resultados[0] in aposta_externa[estrategia[1]]:
                                #dicionario_roletas[nome_cassino] = lista_resultados
                                print('ENVIANDO SINAL TELEGRAM')
                                enviar_sinal_telegram(nome_cassino, sequencia_minima, estrategia, ultimo_resultado)
                                print('=' * 220)
                                checar_sinal_enviado(lista_resultados)
                                time.sleep(1)
                                break
                            
                            else:
                                print('APAGA SINAL DE ALERTA')
                                apagar_alerta_telegram()
                                print('=' * 220)
                                break

                            
                        if estrategia[0] == 'ausência':
                            ''' Verificando se o ultimo resultado da roleta não está dentro da estratégia'''
                            if lista_resultados[0] not in aposta_externa[estrategia[1]]:
                                #dicionario_roletas[nome_cassino] = lista_resultados
                                print('ENVIANDO SINAL TELEGRAM')
                                enviar_sinal_telegram(nome_cassino, sequencia_minima, estrategia, ultimo_resultado)
                                print('=' * 150)
                                checar_sinal_enviado(lista_resultados)
                                break
                            
                            else:
                                print('APAGA SINAL DE ALERTA')
                                apagar_alerta_telegram()
                                print('=' * 220)
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

                
def enviar_alerta_telegram(dicionario_roletas, nome_cassino, sequencia_minima, estrategia, nome_fornecedor):
    global contador_passagem

    ''' Lendo o arquivo txt canais '''
    txt = open("canais.txt", "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[12].replace('canais= ','').replace('\n','')
    canais = ast.literal_eval(canais) # Convertendo string em dicionario 

    # Enviando Mensagem Telegram
    horario_inicial = datetime.now()

    ''' Enviando mensagem Telegram '''
    try:
        for key, value in canais.items():

            try:

                with open('mensagens_txt\\alerta.txt',"r", encoding="utf-8") as arquivo:
                    message_alerta = arquivo.read()

                table_alerta =  message_alerta\
                                .replace('[LINK_CADASTRO]', value[0])\

                globals()[f'alerta_{key}'] = enviarAlertaTelegram(key, table_alerta).start()

                time.sleep(0.2)

            except:
                print('NÃO CONSEGUI ENVIAR A MENSAGEM PARA O CANAL', key)

    except:
        pass


    print('MENSAGEM ENVIADA PARA TODOS OS CANAIS EM ---> ', datetime.now() - horario_inicial)

    contador_passagem = 1


def enviar_sinal_telegram(nome_cassino, sequencia_minima, estrategia, ultimo_resultado):
    global table_sinal
    
    ''' Lendo o arquivo txt canais '''
    txt = open("canais.txt", "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[12].replace('canais= ','').replace('\n','')
    canais = ast.literal_eval(canais) # Convertendo string em dicionario 

    # Enviando Mensagem Telegram
    horario_inicial = datetime.now()

    ''' Enviando mensagem Telegram '''
    try:
        for key,value in canais.items():
            try:
                ''' Lendo o arquivo txt config-mensagens '''
                with open('mensagens_txt\\sinal.txt',"r", encoding="utf-8") as arquivo:
                    message_sinal = arquivo.read()

                table_sinal= message_sinal\
                            .replace('[LISTA_RESULTADOS]', ' | '.join(dicionario_roletas[nome_cassino][:int(sequencia_minima)]))\
                            .replace('[ULTIMO_RESULTADO]', ultimo_resultado)\
                            .replace('[APOSTA]', estrategia[3].upper())\
                            .replace('[LINK_CADASTRO]', value[0])

                globals()[f'sinal_{key}'] = enviarSinalTelegram(key, table_sinal).start()
                
                time.sleep(0.1)

            except:
                print('NÃO CONSEGUI ENVIAR A MENSAGEM PARA O CANAL', key)
                pass
    
    except:
        pass
    
    print('MENSAGEM ENVIADA PARA TODOS OS CANAIS EM ---> ', datetime.now() - horario_inicial)


def apagar_alerta_telegram():
    global contador_passagem

    ''' Lendo o arquivo txt canais '''
    txt = open("canais.txt", "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[12].replace('canais= ','').replace('\n','')
    canais = ast.literal_eval(canais) # Convertendo string em dicionario 

    # Apagando Mensagem Telegram
    horario_inicial = datetime.now()

    try:
        for key, value in canais.items():
            try:
            
                apagarMensagemTelegram(key).start()
            
            except:
                print('NÃO CONSEGUI APAGAR A MENSAGEM DO CANAL', key)
                pass
    except:
        pass
    
    print('MENSAGEM APAGADA EM TODOS OS CANAIS EM ---> ', datetime.now() - horario_inicial)
    contador_passagem = 0


def checar_sinal_enviado(ultimos_resultados):
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
    global lista_resultados

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
            
            grupo_apostar = apostasExternas(estrategia[3], dic_estrategia_usuario)

            # VALIDANDO WIN OU LOSS
            if lista_resultados[0] in grupo_apostar[estrategia[3]] or lista_resultados[0] == '0' or lista_resultados[0] == '00':
            
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

                    # Enviando Mensagem Telegram
                    horario_inicial = datetime.now()

                    for key,value in canais.items():
                        try:
                            ''' Lendo o arquivo txt config-mensagens '''
                            with open('mensagens_txt\\green.txt',"r", encoding="utf-8") as arquivo:
                                message_green = arquivo.read()

                            msg_green = message_green\
                                        .replace('[LISTA_RESULTADOS]', ' | '.join(resultados))
                            
                            responderMensagemTelegram(key, msg_green).start()

                            time.sleep(0.1)
                                                                                                
                        except:
                            pass
                            
                    print('MENSAGEM ENVIADA PARA TODOS OS CANAIS EM ---> ', datetime.now() - horario_inicial)

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

      # editando mensagem
        try:
            ''' Lendo o arquivo txt canais '''
            txt = open("canais.txt", "r", encoding="utf-8")
            arquivo = txt.readlines()
            canais = arquivo[12].replace('canais= ','').replace('\n','')
            canais = ast.literal_eval(canais) # Convertendo string em dicionario 
            
            # Enviando Mensagem Telegram
            horario_inicial = datetime.now()

            for key,value in canais.items():
                try:
                    ''' Lendo o arquivo txt config-mensagens '''
                    with open('mensagens_txt\\red.txt',"r", encoding="utf-8") as arquivo:
                        message_red = arquivo.read()

                    msg_red = message_red\
                                .replace('[LISTA_RESULTADO]', ' | '.join(resultados))
                    
                    responderMensagemTelegram(key, msg_red).start()

                    time.sleep(0.1)

                except:
                    pass
            
            print('MENSAGEM ENVIADA PARA TODOS OS CANAIS EM ---> ', datetime.now() - horario_inicial)
            

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



placar()            # Gerando o Placar
#pegar_evosessionid()

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
    global parar, contador_passagem
    global browser

    while True:
        try:
            parar = 1
            contador_passagem = 0
            return 

        except:
            continue


@bot.message_handler(commands=['⏲ Ultimos_Resultados'])
def ultimosResultados(message):
    
    if botStatus != 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        bot.reply_to(message, "🤖 Ok! Mostrando Ultimos Resultados das Roletas", reply_markup=markup)
        try:
            
            for key, value in dicionario_roletas.items():
                #print(key, value)
                bot.send_message(message.chat.id, f'{key}{value}')

        except:
            pass
    

    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

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
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

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
        markup_estrategias = generate_buttons_estrategias([f'{estrategia}' for estrategia in lista_estrategias], markup)    
        markup_estrategias.add('◀ Voltar')

        message_excluir_estrategia = bot.reply_to(message, "🤖 Escolha a estratégia a ser excluída 👇", reply_markup=markup_estrategias)
        bot.register_next_step_handler(message_excluir_estrategia, registrarEstrategiaExcluida)
    
    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_excluir_estrategia = bot.reply_to(message, "🤖⛔ Estou validando uma estratégia! Tente novamente em alguns instanstes.", reply_markup=markup)


@bot.message_handler(commands=['🧠📜 Estratégias_Cadastradas'])
def estrategiasCadastradas(message):
    global estrategia
    global estrategias
    global lista_estrategias

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    if lista_estrategias != []:
        bot.reply_to(message, "🤖 Ok! Listando estratégias", reply_markup=markup)

        for estrategia in lista_estrategias:
            #print(estrategia)
            bot.send_message(message.chat.id, f'{estrategia}')
    
    else:
        bot.reply_to(message, "🤖 Nenhuma estratégia cadastrada ❌", reply_markup=markup)


@bot.message_handler(commands=['📈 Gestão'])
def gestao(message):
    global placar
    global resultados_sinais
    global placar_estrategias

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

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
    markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

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
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Estou validando um Sinal. Tente novamente em alguns instanstes.", reply_markup=markup)

    elif botStatus == 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Bot já está pausado ", reply_markup=markup)

    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

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
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message, "🤖 Bot Immersive Roulette! ✅ Escolha uma opção 👇",
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
            markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖⛔ Bot já está ativado",
                                reply_markup=markup)

        
        elif lista_estrategias == []:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖⛔ Cadastre no mínimo 1 estratégia antes de iniciar",
                                reply_markup=markup)

        
        else:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖 Ok! Bot Ativado com sucesso! ✅ Em breve receberá sinais nos canais informados no arquivo auxiliar! ",
                                    reply_markup=markup)
            
            botStatus = 1
            reladiarioenviado = 0
            parar=0
            contador_passagem = 0
            stop_loss = []

            print('##################################################  INICIANDO AS ANÁLISES  ##################################################')
            print()
            print()
              
            coletarResultados()



    
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


@bot.message_handler()
def registrarTipoEstrategia(message_tipo_estrategia):
    global resposta_usuario

    if message_tipo_estrategia.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_tipo_estrategia, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        return




    if message_tipo_estrategia.text in ['ESTRATÉGIAS PADRÕES']:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        estrategias_padroes = (['repetição', '1ª coluna', '3', '2ª/3ª coluna'],
                               ['repetição', '2ª coluna', '3', '1ª/3ª coluna'], 
                               ['repetição', '3ª coluna', '3', '1ª/2ª coluna'], 
                               ['repetição', '1ª duzia', '3', '2ª/3ª duzia'], 
                               ['repetição', '2ª duzia', '3', '1ª/3ª duzia'], 
                               ['repetição', '3ª duzia', '3', '1ª/2ª duzia'],
                               ['repetição', 'números par(es)', '3', 'números impar(es)'],
                               ['repetição', 'números impar(es)', '3', 'números par(es)'],
                               ['repetição', 'números baixos', '3', 'números altos'],
                               ['repetição', 'números altos', '3', 'números baixos'])
        

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
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

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
    markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

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
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_excluir_estrategia, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        
        return
    

    estrategia_excluir = message_excluir_estrategia.text
    
    ''' Excluindo a estratégia '''
    for estrategia in lista_estrategias:
        if estrategia_excluir == str(estrategia):
            lista_estrategias.remove(estrategia)

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
    markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    bot.reply_to(message_excluir_estrategia, "🤖 Estratégia excluída com sucesso! ✅", reply_markup=markup)




while True:
    try:
        bot.infinity_polling(timeout=1, long_polling_timeout=1)
        bot.infinity_polling(True)
    except:
        pass






