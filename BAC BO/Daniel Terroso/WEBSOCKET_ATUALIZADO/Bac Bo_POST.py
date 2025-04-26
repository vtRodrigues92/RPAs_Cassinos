import time
from datetime import datetime, timedelta
#from columnar import columnar
import telebot
from telegram.ext import *
from telebot import *
import ast
#from selenium.webdriver.support.color import Color
import os
from websocket import create_connection
import json
import requests
#from fake_useragent import UserAgent


print()
print('                                #################################################################')
print('                                #####################   BOT BAC BO   ############################')
print('                                #################################################################')
print('                                ##################### SEJA BEM VINDO ############################')
print('                                #################################################################')
print('                                ############# DESENVOLVIDO POR VICTOR RODRIGUES #################')
print('                                #################################################################\n')
print('Versão = 1.0.0')
print('Ambiente: Produção\n\n\n')





# THREAD PARA ENVIAR POST PARA API
class enviarPostAPI(threading.Thread):
    def __init__(self, canais, status, texto):
        self.canais = canais
        self.status = status
        self.texto = texto
        threading.Thread.__init__(self)
    
    def run(self):
        try:
        
            payload = {
                    'status': self.status, #alert | confirm | success | failure | denied
                    'chat_id': [key for key,value in self.canais.items()],
                    'content': self.texto,
                    'link_refer':[value[0] for key,value in self.canais.items()],
                    'link_game_bet':[value[2] for key,value in self.canais.items()]
            }

            requests.post(url, headers=headers, json=payload)
        
        except Exception as e:
            print(e)


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
    usuario = 'lucasjulio23'
    senha = 'Fordbracom2023'

    #lucasjulio23
    #Fordbracom2023

    #ua = UserAgent()
    #user_agent = ua.random

    urlLogin = "https://odin.sportingtech.com/api/user/login"
    
    payloadLogin = '{"requestBody":{"username":"' + usuario + '","email":null,"phone":null,"keepLoggedIn":null,"password":"' + senha + '","loginType":1},"languageId":23,"device":"d"}'
    
    headersLogin = {"Accept":"application/json, text/plain, */*",
                    "Content-Type": "application/json",
                    "Finger_print": "946fb7e168879bc7e8f28c581f272b46",
                    "Origin":"https://vembetar.com",
                    "Referer":"https://vembetar.com/",
                    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                    "X-PGDevice":"d",
                    }

    dadosLogin = requests.post(urlLogin, data=payloadLogin, headers=headersLogin)

    print(dadosLogin.text,'\n\n')

    s7oryo9stv = dadosLogin.headers['s7oryO9STV']
    traderId = json.loads(dadosLogin.text)['data']['traderId']
    code = json.loads(dadosLogin.text)['data']['code']
    balance = json.loads(dadosLogin.text)['data']['balance']

    print('traderId:',traderId,' | code:',code,' | s7oryo9stv:',s7oryo9stv,' | balance: R$',balance,'\n\n')

    urlEvo = "https://odin.sportingtech.com/api/user/casinoapi/openGame"

    payloadEvo = '{"requestBody":{"gameId":"18280","channel":"web","vendorLimitId":"evol_BacBo00000000001_BRL","vendorId":130,"redirectUrl":"https://vembetar.com/ptb/games/livecasino/detail/normal/18280/evol_BacBo00000000001_BRL"},"identity":null,"device":"d","languageId":23}'
    
    headersEvo = {"Content-Type": "application/json",
                  "Origin":"https://vembetar.com",
                  "Referer":"https://vembetar.com/",
                  "s7oryO9STV":s7oryo9stv,
                  "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                  "X-PGDevice":"d"
                  }

    dadosEvo = requests.post(urlEvo, data=payloadEvo, headers=headersEvo)

    gameUrl = json.loads(dadosEvo.text)['data']['gameUrl']

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
    "Host": "belloatech.evo-games.com",
    "Origin": "https://belloatech.evo-games.com",
    "Pragma": "no-cache",
    "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
    "Sec-WebSocket-Key": "CZgku/PZXaA6wWHHbuYC7w==",
    "Sec-WebSocket-Version": "13",
    "Upgrade": "websocket",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"

    }

   
    #f'wss://wac.evo-games.com/public/bacbo/player/game/BacBo00000000001/socket?messageFormat=json&instance=632u9-qo2wix3z5rclnkzu-BacBo00000000001&tableConfig=&EVOSESSIONID={evosessionid}&client_version=6.20230309.65135.22518-6c9b2e0e13'
    #URL = f'wss://belloatech.evo-games.com/public/bacbo/player/game/BacBo00000000001/socket?messageFormat=json&instance=fjf32l-rhjuf7mokioplhho-BacBo00000000001&tableConfig=&EVOSESSIONID={evosessionid}&client_version=6.20230823.71249.29885-78ea79aff8'
    URL = f'wss://belloatech.evo-games.com/public/bacbo/player/game/BacBo00000000001/socket?messageFormat=json&instance=8i5uph-rhjuf7mokioplhho-BacBo00000000001&tableConfig=&EVOSESSIONID={evosessionid}&client_version=6.20231217.210359.36178-ee689a66ae'
    
    ws = create_connection(URL)

    ws.send(json.dumps([json.dumps(header)]))

    cont = 0
    ultimo_result = ''
    ultimo_valor_armazenado = ''


def formata_dados(ultimo_result):
    ''' Convertendo a letra em cor '''
    # Pegando Resultado da rodada no arquivo JSON
    resultado = json.loads(ultimo_result)['args']['history'][-1]['winner']
            
    if resultado == 'Player':
        resultado = 'P'
        
    if resultado == 'Banker':
        resultado = 'B'
        
    if resultado == 'Tie':
        resultado = 'T'
        
    return resultado


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


def inicio():
    global horario_inicio
    global url
    global headers
    global lista_resultados

    url = "https://app.bootbost.com.br/api/v1/call"
    headers = {
    'Content-Type': 'application/json'
    }

    horario_inicio = datetime.now()
    lista_resultados = []

    

def logarSite():

    browser.get(r"https://mesk.bet/")
    browser.maximize_window()
    time.sleep(5)
    ''' Inserindo login e senha '''
    ''' Lendo o arquivo txt config-mensagens '''
    txt = open("canais.txt", "r", encoding="utf-8")
    mensagem_login = txt.readlines()
    usuario = mensagem_login[12].replace('\n','').split(' ')[1]
    senha = mensagem_login[13].replace('\n','').split(' ')[1]

    ''' Mapeando elementos para inserir credenciais '''
    try:
        browser.find_element_by_css_selector('.button-login[data-v-742e4e55]').click() #Clicando no botão Entrar
        browser.find_element_by_xpath('//*[@id="page-top"]/div[2]/div/div[2]/form/input').send_keys(usuario) #Inserindo login
        browser.find_element_by_xpath('//*[@id="page-top"]/div[2]/div/div[2]/form/div[1]/input').send_keys(senha) #Inserindo senha
        browser.find_element_by_css_selector('.button-login-modal[data-v-742e4e55]').click() #Clicando no btn login
        
        ''' Verificando se o login foi feito com sucesso'''
        t3 = 0
        while t3 < 20:
            if browser.find_elements_by_xpath('//*[@id="page-top"]/div[1]/div[2]/div[1]/span[1]'):
                break
            else:
                t3+=1
    except:
        pass
    
    try:
        
        ''' Entrando no ambiente '''
        browser.get(r"https://mesk.bet/casino/?cat=mocked-most&gameid=7341")
        time.sleep(10)

        # TELA CHEIA
        tela_cheia = browser.find_element_by_xpath('//*[@id="__layout"]/main/div[3]/div/div/div/div/div/div[3]/div/iframe').get_attribute('src')
        browser.get(tela_cheia)
        time.sleep(10)


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


        browser.minimize_window()

    except:
        pass


def gerarListaResultados(resultados):
    ''' Convertendo a letra em cor '''
    while True:
        try:
            lista = []
            for resultado in resultados[-11:]:
                if resultado == 'P':
                    resultado = 'Player'
                    lista.append(resultado)
                    continue
#
                if resultado == 'B':
                    resultado = 'Banker'
                    lista.append(resultado)
                    continue
#
                if resultado == 'T':
                    resultado = 'Tie'
                    lista.append(resultado)
                    continue
          
            return lista
            
        except:
            #validarJogoPausado()
            ''' Pegando Resultados do Jogo '''
            resultados = browser.find_elements_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div[6]/div/div[2]/div/div/div[2]//*[name()="svg"][@name]')

            '''Verificando se o painel mudou de lado ''' 
            if resultados == []:
                resultados = browser.find_elements_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div[2]/div/div[6]/div[2]/div/div/div/div[2]/div/div//*[name()="svg"][@name]')
                
            continue


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

                    if 'bacbo.road' in ultimo_result:

                        resultado_atual = json.loads(ultimo_result)['args']['history'][-1]['winner']
                        lista_resultados.append(resultado_atual)
                                        

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
    global ultimo_valor_armazenado
    global ws
    
    for estrategia in estrategias:
        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass
        # Validando o horario para envio do relatório diário
        validaData()

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
            time.sleep(10)

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

                    if 'bacbo.road' in ultimo_result:
                        resultado_atual = json.loads(ultimo_result)['args']['history'][-1]['winner']
                        lista_resultados.append(resultado_atual)
                        
                    
                        if estrategia[:sequencia_minima_sinal] == lista_resultados[-sequencia_minima_sinal:]:
                            print('PADRÃO DA ESTRATÉGIA ', estrategia, ' CONFIRMADO!')
                            print('ENVIANDO SINAL TELEGRAM')
                            enviar_sinal_telegram()
                            time.sleep(10)
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
                    
                

        else:
             print('=' * 100)

    if contador_passagem == 1:
            print('ERRO NA REQUISIÇÃO APÓS ENVIAR ALERTA. APAGANDO ALERTA')
            print('=' * 100)
            apaga_alerta_telegram()


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

    #ENVIANDO POST PARA A API
    try:

        texto = mensagem_alerta[0].replace('\n','') + '\n\n' + \
                mensagem_alerta[1].replace('\n','')
        
        enviarPostAPI(canais, 'alert', texto).start()

    except Exception as e:
        print(e)
            
    
    # Enviando Mensagem Telegram
    horario_inicial = datetime.now()

    try:
        for key,value in canais.items():
            try:
                ''' Mensagem '''
                table_alerta = mensagem_alerta[0].replace('\n','') + '\n' +\
                               mensagem_alerta[1].replace('\n','') + '\n' +\
                               mensagem_alerta[2].replace('\n','').replace('[SITE_PC]', value[1]) +\
                               mensagem_alerta[3].replace('\n','').replace('[SITE_MB]', value[2])
                
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

    #ENVIANDO POST PARA A API
    try:

        texto =  mensagem_sinal[9].replace('\n','') + '\n' +\
                mensagem_sinal[11].replace('\n','').replace('[COR]','🟦PLAYER' if estrategia[-1] == 'Player' else '🟥BANKER' if estrategia[-1] == 'Banker' else '🟨TIE') + '\n' +\
                mensagem_sinal[12].replace('\n',''),

        enviarPostAPI(canais, 'confirm', texto).start()
    
    except Exception as e:
        print(e)
        

    # Enviando Mensagem Telegram
    horario_inicial = datetime.now()

    try:
        for key, value in canais.items():
            try:
                ''' Mensagem '''
                table_sinal = mensagem_sinal[9].replace('\n','') + '\n' +\
                              mensagem_sinal[10].replace('\n','').replace('[LINK_CANAL]',value[0]) + '\n' +\
                              mensagem_sinal[11].replace('\n','').replace('[COR]','🟦PLAYER' if estrategia[-1] == 'Player' else '🟥BANKER' if estrategia[-1] == 'Banker' else '🟨TIE') + '\n' +\
                              mensagem_sinal[12].replace('\n','') + '\n\n' +\
                              mensagem_sinal[15].replace('\n','').replace('[SITE_PC]',value[1]) +\
                              mensagem_sinal[16].replace('\n','').replace('[SITE_MB]',value[2]) if value[0] != ''\
                              \
                              else\
                              mensagem_sinal[9].replace('\n','') + '\n' +\
                              mensagem_sinal[11].replace('\n','').replace('[COR]','🟦PLAYER' if estrategia[-1] == 'Player' else '🟥BANKER' if estrategia[-1] == 'Banker' else '🟨TIE') + '\n' +\
                              mensagem_sinal[12].replace('\n','') + '\n\n' +\
                              mensagem_sinal[15].replace('\n','').replace('[SITE_PC]',value[1]) +\
                              mensagem_sinal[16].replace('\n','').replace('[SITE_MB]',value[2])
                
                
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

    #ENVIANDO POST PARA A API
    try:
    
        texto = ['Entrada Não Confirmada']

        enviarPostAPI(canais, 'denied', texto).start()
    
    except Exception as e:
        print(e)
    
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
    global ultimo_valor_armazenado
    global ws

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

            if 'bacbo.road' in ultimo_result:
                resultado_atual = json.loads(ultimo_result)['args']['history'][-1]['winner']
                lista_resultados.append(resultado_atual)

                print(lista_resultados[-1])

                if lista_resultados[-1] == 'Tie':
                    resultado_valida_sinal.append('🟨')

                if lista_resultados[-1] == 'Banker':
                    resultado_valida_sinal.append('🟥')
                
                if lista_resultados[-1] == 'Player':
                    resultado_valida_sinal.append('🟦')

                
                # VALIDANDO WIN OU LOSS
                if lista_resultados[-1] == estrategia[-1] or lista_resultados[-1] == 'Tie':
                
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
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

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
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)
                        
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

                        #ENVIANDO POST PARA A API
                        try:

                            texto = mensagem_green[22].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(resultado_valida_sinal)),
                        
                            enviarPostAPI(canais, 'success', texto).start()
                        
                        except Exception as e:
                            print(e)
                        
                        # Enviando Mensagem Telegram
                        horario_inicial = datetime.now()

                        for key, value in canais.items():
                            try:
                            
                                responderMensagemTelegram(key, mensagem_green[22].replace('[LISTA_RESULTADOS]', ' | '.join(resultado_valida_sinal))).start()
                                time.sleep(0.1)

                            except:
                                pass
                        
                        print('MENSAGEM ENVIADA PARA TODOS OS CANAIS EM ---> ', datetime.now() - horario_inicial)
            
                    except:
                        pass
                    

                    print('='*100)
                    validador_sinal = 0
                    contador_cash = 0
                    contador_passagem = 0
                    return

            
                else:
                    print('LOSSS')
                    print('==================================================')
                    contador_cash+=1
                    continue
            
            else:
                continue
                #validarJogoPausado()
                

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

        # Preenchendo arquivo txt
        placar_loss +=1
        placar_geral = placar_win + placar_loss
        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
            arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}")
        

        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")

        stop_loss.append('loss')
        
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

            #ENVIANDO POST PARA A API
            try:

                texto = mensagem_red[24].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(resultado_valida_sinal)),
            
                enviarPostAPI(canais, 'failure', texto).start()
            
            except Exception as e:
                print(e)


            # Enviando Mensagem Telegram
            horario_inicial = datetime.now()

            for key,value in canais.items():

                try:
                     
                    responderMensagemTelegram(key, mensagem_red[24].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(resultado_valida_sinal))).start()
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
        

        print('==================================================')
        validador_sinal = 0
        contador_cash = 0
        contador_passagem = 0
        return




inicio()
placar()



#________________________________________________________________________________________ TELEGRAM__________________________________________________________________________________#

print('\n\n')
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
lista_ids = []



# LENDO TXT PARA DEFINIR VARIAVEL DE CANAIS E VALIDAÇÃO DE USUÁRIO
txt = open("canais.txt", "r", encoding="utf-8")
arquivo = txt.readlines()

CHAVE_API = arquivo[2].split(' ')[1].split('\n')[0]

ids = arquivo[6].split(' ')[1].split('\n')[0]
canais = arquivo[7].split(' ')[1].split('\n')[0].split((','))


bot = telebot.TeleBot(CHAVE_API)

global message

######################################################




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
        markup_estrategias = generate_buttons_estrategias([f'{estrategia}' for estrategia in estrategias], markup)
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
        bot.send_message(message.chat.id, f'{estrategia}')




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

        ''' Add id na lista de ids'''
        if str(message.chat.id) not in lista_ids:
            lista_ids.append(message.chat.id)
        else:
            pass
       
        #Add to buttons by list with ours generate_buttons function.
        #markup = generate_buttons(['/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','📊 Placar Atual','❌ Pausar Bot'], markup)
        
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message, "🤖 Bot Bac Bo Iniciado! ✅ Escolha uma opção 👇",
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


        estrategias_padroes = ( ['Banker','Banker','Banker','Player'],
                                ['Banker','Player','Banker','Player','Player'], 
                                ['Player','Player','Player','Banker'], 
                                ['Player','Banker','Player','Banker','Banker'] 
                               )
        

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

        message_estrategia = bot.reply_to(message_tipo_estrategia, "🤖 Ok! Informe a Sequencia de Resultados que o Bot Terá que Identificar. *** O último Resultado será a da APOSTA *** Ex: Player,Player,Player,Banker / Banker,Banker,Banker,Player", reply_markup=markup)
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
    
    estrategia_excluir = message_excluir_estrategia.text
    
    for estrategia in estrategias:
        if estrategia_excluir == str(estrategia):
            estrategias.remove(estrategia)

    
    for pe in placar_estrategias:
        if estrategia_excluir == str(pe[:-5][0]):
            placar_estrategias.remove(pe)


    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    bot.reply_to(message_excluir_estrategia, "🤖 Estratégia excluída com sucesso! ✅", reply_markup=markup)





bot.infinity_polling()



