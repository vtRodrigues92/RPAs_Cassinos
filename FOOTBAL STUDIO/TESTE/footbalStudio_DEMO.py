from selenium import webdriver
import time
import warnings
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import telebot
from telegram.ext import *
from telebot import *
import ast
import os
#from webdriver_manager.firefox import GeckoDriverManager
#from websocket import create_connection
import json
import requests
from websocket import create_connection
from fake_useragent import UserAgent


print()
print('                                #################################################################')
print('                                ##################   BOT FOOTBALSTUDIO   ########################')
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


 

def pegar_evosessionid():
    #LOGIN
    URL = 'https://backoffice.mesk.bet/api/auth/login'

    header = {
    'Content-Type': 'application/json'
    }

    payload = {"email":'DanielaAline22',
            "password":'Fordbracom22'}
    
    response = requests.post(URL, headers=header, json=payload)
    
    token_autorizacao = response.json()['token']

    
    #### ENTRANDO NO GAME
    #REQUISIÇÃO1
    URL = 'https://backoffice.mesk.bet/api/casino/softgaming/auth'

    payload = {"game_id": "14615"}

    header = {
        "Accept":"application/json, text/plain, */*",
        "Authorization":f"bearer {token_autorizacao}",
        "Origin":"https://mesk.bet",
        "Referer":"https://mesk.bet/",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
            }
    
    response = requests.post(URL, json=payload, headers=header)

    url_1 = json.loads(response.content)['url']

    #REQUISIÇÃO2
    URL = f'{url_1}&ref=https://mesk.bet'

    response = requests.get(URL)

    url_2 = json.loads(response.content)['data']

    #REQUISIÇÃO3
    URL = url_2

    headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Cookie":"cdn=https://static.egcdn.com; lang=en; locale=en-GB; EVOSESSIONID=rkimpvrwoyoblpe3rkimqshnmany7wcf4588b17809d39462ac1b30cfa2d31d5476bcf0169e16227c",
        "Host":"live.wirebankers.com",
        "Referer":"https://mesk.bet/",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }
    response = requests.get(URL, headers=headers, allow_redirects=False)

    evosessionid = response.headers.get('Set-Cookie').split('; Path')[0]

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
    "Host": "live.wirebankers.com",
    "Origin": "https://live.wirebankers.com",
    "Pragma": "no-cache",
    "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
    "Sec-WebSocket-Key": "dBtJzWbn5Y/9jndYxdsmXg==",
    "Sec-WebSocket-Version": "13",
    "Upgrade": "websocket",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"

    }

   
    #f'wss://wac.evo-games.com/public/topcard/player/game/TopCard000000001/socket?messageFormat=json&instance=409uj-qo2wix3z5rclnkzu-nvrpqglt6teqkvaf&tableConfig=nvrpqglt6teqkvaf&EVOSESSIONID={evosessionid}&client_version=6.20230323.70223.23049-6a8fb42f8b'
    #URL=f'wss://belloatech.evo-games.com/public/topcard/player/game/TopCard000000001/socket?messageFormat=json&instance=o6q2h6-rhjuf7mokioplhho-TopCard000000001&tableConfig=&EVOSESSIONID={evosessionid}&client_version=6.20230823.71249.29885-78ea79aff8'
    URL=f'wss://live.wirebankers.com/public/topcard/player/game/TopCard000000001/socket?messageFormat=json&instance=dwnh20-rkjz6lh3uz6rjl2l-TopCard000000001&tableConfig=&{evosessionid}'
    
    ws = create_connection(URL, verify = False)

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

    # Condição que zera o placar quando o dia muda
    if horario_atual == '00:00' and reladiarioenviado == 0:
        placar()
        reladiarioenviado +=1

    # Condição que zera o placar quando o dia muda
    if horario_atual == '00:01' and reladiarioenviado == 1:
        reladiarioenviado = 0


def auto_refresh():
    global horario_inicio

    horario_atual = datetime.today().strftime('%H:%M')
    tres_hora = timedelta(hours=1)
    horario_mais_tres = horario_inicio + tres_hora
    horario_refresh = horario_mais_tres.strftime('%H:%M')

    if horario_atual == horario_refresh:
        print('HORA DE REFRESHAR A PAGINA!!!!')
        logarSite()
        time.sleep(10)
        horario_inicio = datetime.now()


def inicio():
    global browser
    global horario_inicio
    global lista_resultados

    horario_inicio = datetime.now()
    lista_resultados = []

    horario_inicio = datetime.now()
    

def logarSite():
    #browser.get(r"https://pi.njoybingo.com/game.do?token=7d10f64b-e3db-4fb8-a8f7-330ff4d0d407&pn=meskbet&lang=pt&game=EVOLUTION-topcard-nvrpqglt6teqkvaf&type=CHARGED")  #PRODUÇÃO
    #browser.get(r"https://pi.njoybingo.com/game.do?token=18298495-0dce-4997-944e-f52c78717619&pn=meskbet&lang=pt&game=EVOLUTION-topcard-nvrpqglt6teqkvaf&type=CHARGED")  #DEV
    #browser.maximize_window()
    #time.sleep(10)

    browser.get(r"https://mesk.bet/")
    
    try:
        browser.maximize_window()
    except:
        pass
    
    time.sleep(5)
    ''' Inserindo login e senha '''
    ''' Lendo o arquivo txt config-mensagens '''
    txt = open("canais.txt", "r", encoding="utf-8")
    mensagem_login = txt.readlines()
    usuario = mensagem_login[12].replace('\n','').split(' ')[1]
    senha = mensagem_login[13].replace('\n','').split(' ')[1]

    ''' Mapeando elementos para inserir credenciais '''
    try:
        browser.find_element_by_css_selector('.button-login[data-v-3a47816a]').click() #Clicando no botão Entrar
        browser.find_element_by_xpath('//*[@id="page-top"]/div[2]/div/div[2]/form/input').send_keys(usuario) #Inserindo login
        browser.find_element_by_xpath('//*[@id="page-top"]/div[2]/div/div[2]/form/div[1]/input').send_keys(senha) #Inserindo senha
        browser.find_element_by_css_selector('.button-login-modal[data-v-3a47816a]').click() #Clicando no btn login
        
        ''' Verificando se o login foi feito com sucesso'''
        t3 = 0
        while t3 < 20:
            if browser.find_elements_by_xpath('//*[@id="page-top"]/div[1]/div[2]/div[1]/span[1]'):
                break
            else:
                t3+=1
    except:
        pass

    ''' Entrando no ambiente '''
    browser.get(r'https://pi.njoybingo.com/game.do?token=dcf77b1e-8f99-4e30-b088-501d195cc4e7&pn=meskbet&lang=pt&game=EVOLUTION-topcard-nvrpqglt6teqkvaf&type=CHARGED')
    
    #browser.get(r"https://pi.njoybingo.com/game.do?token=18298495-0dce-4997-944e-f52c78717619&pn=meskbet&lang=pt&game=EVOLUTION-topcard-nvrpqglt6teqkvaf&type=CHARGED")
    time.sleep(10)
    #'https://pi.njoybingo.com/game.do?token=18298495-0dce-4997-944e-f52c78717619&pn=meskbet&lang=pt&game=EVOLUTION-topcard-nvrpqglt6teqkvaf&type=CHARGED'


    #ENTRANDO NO IFRAME
    a=1
    while a<10:
        try:
            
            iframe = browser.find_element_by_xpath('/html/body/div[6]/div[2]/iframe')
            browser.switch_to_frame(iframe)
            break

        except:
            a+=1
            time.sleep(3)


    try:
        browser.minimize_window()
    except:
        pass


def formata_dados(ultimo_result):
    ''' Convertendo a letra em cor '''
    # Pegando Resultado da rodada no arquivo JSON
    resultado = json.loads(ultimo_result)['args']['result']['winner']    

    if resultado == 'Dragon':
        resultado = 'C'
        
    if resultado == 'Tiger':
        resultado = 'V'
        
    if resultado == 'Tie':
        resultado = 'E'
        
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

                    if 'resolved' in ultimo_result:
                        resultado_atual = formata_dados(ultimo_result)
                        lista_resultados.append(resultado_atual)
                        
                        print(datetime.now().strftime('%H:%M'))

                        ''' Chama a função que valida a estratégia para enviar o sinal Telegram '''
                        validaEstrategias(lista_resultados)

                        #Separador
                        print('=' * 100)
                        ultimo_valor_armazenado = ultimo_result
                        time.sleep(7)
                    
                    ultimo_valor_armazenado = ultimo_result  

                                        
                
            except Exception as e:
                print(e)
                evosessionid = pegar_evosessionid()
                continue
                
    
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

        if len(lista_resultados) > 10:
            print('Historico da Mesa --> ', lista_resultados[-10:])
        else:
            print('Historico da Mesa --> ', lista_resultados)
            

        ''' Verifica se os resultados da mesa batem com a estrategia para enviar o alerta '''
        if estrategia[:sequencia_minima_alerta] == lista_resultados[-sequencia_minima_alerta:]:
            print('IDENTIFICADO O PADRÃO DA ESTRATÉGIA --> ', estrategia)
            print('ENVIAR ALERTA')
            enviar_alerta_telegram()
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

                    if 'resolved' in ultimo_result:
                        resultado_atual = formata_dados(ultimo_result)
                        lista_resultados.append(resultado_atual)
                    
                        if estrategia[:sequencia_minima_sinal] == lista_resultados[-sequencia_minima_sinal:]:
                            print('PADRÃO DA ESTRATÉGIA ', estrategia, ' CONFIRMADO!')
                            print('ENVIANDO SINAL TELEGRAM')
                            enviar_sinal_telegram()
                            time.sleep(7)
                            checkSinalEnviado(lista_resultados)
                            break
                            
                        else:
                            print('APAGA SINAL DE ALERTA')
                            apaga_alerta_telegram()
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
                        

def enviar_alerta_telegram():
    global contador_passagem

    ''' Lendo o arquivo txt canais '''
    txt = open("canais.txt", "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[7].replace('canais= ','').replace('\n','')
    canais = ast.literal_eval(canais) # Convertendo string em dicionario 

    ''' Lendo o arquivo txt config-mensagens '''
    txt = open("config-mensagens.txt", "r", encoding="utf-8")
    mensagem_alerta = txt.readlines()

    
    # Enviando Mensagem Telegram
    horario_inicial = datetime.now()

    ''' Enviando mensagem Telegram '''
    try:
        for key,value in canais.items():
            try:

                if value[1] != '' and value[2] != '':
                    ''' Mensagem '''
                    table_alerta = mensagem_alerta[0].replace('\n','') + '\n' +\
                                mensagem_alerta[1].replace('\n','') + '\n' +\
                                mensagem_alerta[2].replace('\n','').replace('[SITE_PC]', value[1]) +\
                                mensagem_alerta[3].replace('\n','').replace('[SITE_MB]', value[2])
                    

                else:
                    table_alerta = mensagem_alerta[0].replace('\n','') + '\n' +\
                                    mensagem_alerta[1].replace('\n','') + '\n' +\
                                    mensagem_alerta[4].replace('\n','').replace('[LINK_CADASTRO]', value[0])

                
                globals()[f'alerta_{key}'] = enviarAlertaTelegram(key, table_alerta).start()
                time.sleep(0.2)

            except:
                print('NÃO CONSEGUI ENVIAR A MENSAGEM PARA O CANAL', key)

    except:
        pass
    
    print('MENSAGEM ENVIADA PARA TODOS OS CANAIS EM ---> ', datetime.now() - horario_inicial)

    contador_passagem = 1


def enviar_sinal_telegram():
    global table_sinal
    
    ''' Lendo o arquivo txt canais '''
    txt = open("canais.txt", "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[7].replace('canais= ','').replace('\n','')
    canais = ast.literal_eval(canais) # Convertendo string em dicionario 

    ''' Lendo o arquivo txt config-mensagens '''
    txt = open("config-mensagens.txt", "r", encoding="utf-8")
    arquivo_mensagem = txt.readlines()
    mensagem_sinal = arquivo_mensagem[1].split(',')

    ''' Estruturando mensagem '''
    txt = open("config-mensagens.txt", "r", encoding="utf-8")
    mensagem_sinal = txt.readlines()

    
    # Enviando Mensagem Telegram
    horario_inicial = datetime.now()
    
    try:
        for key, value in canais.items():
            try:
                ''' Mensagem '''
                if value[1] != '' and value[2] != '':
                    table_sinal = mensagem_sinal[9].replace('\n','') + '\n' +\
                                mensagem_sinal[10].replace('\n','').replace('[LINK_CANAL]',value[0]) + '\n' +\
                                mensagem_sinal[11].replace('\n','').replace('[COR]','VERMELHO' if estrategia[-1] == 'C' else 'AZUL' if estrategia[-1] == 'V' else 'AMARELO') + '\n' +\
                                mensagem_sinal[12].replace('\n','') + '\n\n' +\
                                mensagem_sinal[15].replace('\n','').replace('[SITE_PC]',value[1]) +\
                                mensagem_sinal[16].replace('\n','').replace('[SITE_MB]',value[2]) if value[0] != ''\
                                \
                                else\
                                mensagem_sinal[9].replace('\n','') + '\n' +\
                                mensagem_sinal[11].replace('\n','').replace('[COR]','VERMELHO' if estrategia[-1] == 'C' else 'AZUL' if estrategia[-1] == 'V' else 'AMARELO') + '\n' +\
                                mensagem_sinal[12].replace('\n','') + '\n\n' +\
                                mensagem_sinal[15].replace('\n','').replace('[SITE_PC]',value[1]) +\
                                mensagem_sinal[16].replace('\n','').replace('[SITE_MB]',value[2])
                    
                else:
                    table_sinal = mensagem_sinal[9].replace('\n','') + '\n' +\
                                mensagem_sinal[11].replace('\n','').replace('[COR]','VERMELHO' if estrategia[-1] == 'C' else 'AZUL' if estrategia[-1] == 'V' else 'AMARELO') + '\n' +\
                                mensagem_sinal[12].replace('\n','') + '\n' +\
                                mensagem_sinal[10].replace('\n','').replace('[LINK_CANAL]',value[0]) 
                              
                
                globals()[f'sinal_{key}'] = enviarSinalTelegram(key, table_sinal).start()
                
                time.sleep(0.1)

            except:
                print('NÃO CONSEGUI ENVIAR A MENSAGEM PARA O CANAL', key)
                pass
    
    
    except:
        pass
    
    print('MENSAGEM ENVIADA PARA TODOS OS CANAIS EM ---> ', datetime.now() - horario_inicial)


def apaga_alerta_telegram():
    global contador_passagem

    ''' Lendo o arquivo txt canais '''
    txt = open("canais.txt", "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[7].replace('canais= ','').replace('\n','')
    canais = ast.literal_eval(canais) # Convertendo string em dicionario 

    # Apagando Mensagem Telegram
    horario_inicial = datetime.now()

    try:
        for key,value in canais.items():
            try:
                apagarMensagemTelegram(key).start()
            
            except:
                print('NÃO CONSEGUI APAGAR A MENSAGEM DO CANAL', key)
                pass
    except:
        pass
    
    print('MENSAGEM APAGADA EM TODOS OS CANAIS EM ---> ', datetime.now() - horario_inicial)
    contador_passagem = 0


def checkSinalEnviado(lista_resultados):
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
    global lista_resultados_sinal

    resultado_valida_sinal = []
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

            if 'resolved' in ultimo_result:
                resultado_atual = formata_dados(ultimo_result)
                lista_resultados.append(resultado_atual)

                print(lista_resultados[-1])

                if lista_resultados[-1] == 'V':
                    resultado_valida_sinal.append('🟦')

                if lista_resultados[-1] == 'C':
                    resultado_valida_sinal.append('🟥')
                
                if lista_resultados[-1] == 'E':
                    resultado_valida_sinal.append('🟨')


                # VALIDANDO WIN OU LOSS
                if lista_resultados[-1] == estrategia[-1] or lista_resultados[-1] == 'E':
                
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

                        try:
                            # Somando Win na estratégia da lista atual
                            for pe in placar_estrategias:
                                if pe[:-5] == estrategia:
                                    pe[-5] = int(pe[-5])+1
                        except:
                            pass
                        
                        
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
                        
                        try:
                            # Somando Win na estratégia da lista atual
                            for pe in placar_estrategias:
                                if pe[:-5] == estrategia:
                                    pe[-4] = int(pe[-4])+1

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
                        
                        try:
                            # Somando Win na estratégia da lista atual
                            for pe in placar_estrategias:
                                    if pe[:-5] == estrategia:
                                        pe[-3] = int(pe[-3])+1
                        except:
                            pass
                        
        
                    # editando mensagem enviada
                    try:
                        ''' Lendo o arquivo txt canais '''
                        txt = open("canais.txt", "r", encoding="utf-8")
                        arquivo = txt.readlines()
                        canais = arquivo[7].replace('canais= ','').replace('\n','')
                        canais = ast.literal_eval(canais) # Convertendo string em dicionario 

                        ''' Lendo o arquivo txt config-mensagens '''
                        txt = open("config-mensagens.txt", "r", encoding="utf-8")
                        mensagem_green = txt.readlines()
                        
                        # Enviando Mensagem Telegram
                        horario_inicial = datetime.now()

                        for key, value in canais.items():
                            try:

                                responderMensagemTelegram(key, mensagem_green[22].replace('\n','').replace('[RESULTADO]', ' | '.join(resultado_valida_sinal))).start()
                                time.sleep(0.1)

                            except:
                                pass
                        
                        print('MENSAGEM ENVIADA PARA TODOS OS CANAIS EM ---> ', datetime.now() - horario_inicial)


                    except:
                        pass
                    

                    print('='*150)
                    validador_sinal = 0
                    contador_cash = 0
                    contador_passagem = 0
                    return

            
                else:
                    print('LOSSS')
                    print('='*100)
                    contador_cash+=1
                    continue
            
            else:
                continue

        except Exception as e:
            print(e)
            evosessionid = pegar_evosessionid()
            conectar_websocket(evosessionid)
            continue


    if contador_cash == 3:
        print('LOSSS GALE2')
        
        # Preenchendo arquivo txt
        placar_loss +=1
        placar_geral = placar_win + placar_loss
        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
            arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}")
            
        
        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
        

        # editando mensagem
        try:
            ''' Lendo o arquivo txt canais '''
            txt = open("canais.txt", "r", encoding="utf-8")
            arquivo = txt.readlines()
            canais = arquivo[7].replace('canais= ','').replace('\n','')
            canais = ast.literal_eval(canais) # Convertendo string em dicionario 

            ''' Lendo o arquivo txt config-mensagens '''
            txt = open("config-mensagens.txt", "r", encoding="utf-8")
            mensagem_red = txt.readlines()

            # Enviando Mensagem Telegram
            horario_inicial = datetime.now()

            for key,value in canais.items():
                try:

                    texto = mensagem_red[24].replace('\n','')+'\n'+\
                            mensagem_red[25].replace('\n','')+'\n'+\
                            mensagem_red[26].replace('\n','')

                    responderMensagemTelegram(key, texto).start()
                    time.sleep(0.1)
                
                except:
                    pass
            
            print('MENSAGEM ENVIADA PARA TODOS OS CANAIS EM ---> ', datetime.now() - horario_inicial)


        except:
            pass


        ''' Alimentando "Gestão" estratégia '''
        try:
            # Somando Win na estratégia da lista atual
            for pe in placar_estrategias:
                if pe[:-5] == estrategia:
                    pe[-1] = int(pe[-1])+1
            
        except:
            pass

        

        # Validando o stop_loss
        if 'win' in stop_loss:
            stop_loss = []
            stop_loss.append('loss')
        

        print("="*100)
        validador_sinal = 0
        contador_cash = 0
        contador_passagem = 0
        return



inicio()
placar()



#________________________________________________________________________________________ TELEGRAM__________________________________________________________________________________#


print('############################################ AGUARDANDO COMANDOS ############################################')

global canal


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



# LENDO TXT PARA DEFINIR VARIAVEL FREE E VIP E VALIDAÇÃO DE USUÁRIO
txt = open("canais.txt", "r", encoding="utf-8")
arquivo = txt.readlines()
CHAVE_API = arquivo[2].split(' ')[1].split('\n')[0]

ids = arquivo[6].split(' ')[1].split('\n')[0]
canais = arquivo[7].split(' ')[1].split('\n')[0].split((','))
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
        markup = markup.add('◀ Voltar', 'ESTRATÉGIAS PADRÕES', 'NOVA ESTRATÉGIA')

        
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
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

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
        🎯 Assertividade "+ asserividade,\
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
        total = int(pe[-5]) + int(pe[-4]) + int(pe[-3]) + int(pe[-2]) + int(pe[-1])
        soma_win = int(pe[-5]) + int(pe[-4]) + int(pe[-3]) + int(pe[-2])

        try:
            assertividade = str(round(soma_win / total*100, 1)).replace('.0',"")+"%"
        except:
            assertividade = '0%'

        bot.send_message(message.chat.id, '🧠 '+''.join(pe[:-5]) + f'\n==========================\n 🏆= {pe[-5]}  |  🥇= {pe[-4]}  |  🥈= {pe[-3]}  |  🥉= {pe[-2]} \n\n ✅ - {soma_win} \n ❌ - {pe[-1]} \n==========================\n 🎯 {assertividade}  ', reply_markup=markup)
        
        #print(f'🧠 {pe[:-5]} \n==========================\n 🏆= {pe[-5]}  |  🥇= {pe[-4]}  |  🥈= {pe[-3]}  |  🥉= {pe[-2]} \n\n ✅ - {soma_win} \n ❌ - {pe[-1]} \n==========================\n 🎯 {assertividade}'
        #)

    


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

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message, "🤖 Bot Football Studio Iniciado! ✅ Escolha uma opção 👇",
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


        estrategias_padroes = ( ['V','V','V','V','C'],
                                ['C','C','C','C','V'], 
                                ['V','C','V','C','V','C','C'], 
                                ['C','V','C','V','C','V','V'] )
        

        for estrategia_padrao in estrategias_padroes:
            estrategias.append(estrategia_padrao)
            placar_estrategia = [estrategia_padrao]
            placar_estrategia.extend([0,0,0,0,0])
            placar_estrategias.append(placar_estrategia)


        message_aposta = bot.reply_to(message_tipo_estrategia, "🤖 Estratégias Cadastradas ✅", reply_markup=markup)

    
    else:
        
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
         
        markup = markup.add('◀ Voltar')

        message_estrategia = bot.reply_to(message_tipo_estrategia, "🤖 Ok! Informe a sequencia de LETRAS (V,C,E) que o bot terá que identificar. *** A última LETRA será a da aposta ***  \n\n Ex: VVVVVVC  / CCCCCV", reply_markup=markup)
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
    
    estrategia = list(estrategia)
    placar_estrategia = list(placar_estrategia)

    placar_estrategia.extend([0,0,0,0,0])

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


