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
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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




def mensagem_previa(horario):
    global msg_previa_enviada

    try:
        validaData()
       
        with open ('arquivos_txt/tempo_msg_previa.txt', encoding='UTF-8') as arquivo: 
            tempo_previo = arquivo.read()

        horario_atual = datetime.today().strftime('%H:%M') 
        horario_sessao = datetime.strptime(horario,'%H:%M')
        minuto_previo = timedelta(minutes=int(tempo_previo))
        horario_menos_minuto_previo = horario_sessao - minuto_previo
        horario_msg_previa = horario_menos_minuto_previo.strftime('%H:%M')

        if horario_atual == horario_msg_previa and msg_previa_enviada == False:
            
            minutos = open('arquivos_txt/tempo_msg_previa.txt', 'r', encoding='UTF-8').read()
            ''' Lendo o arquivo txt canais '''
            txt = open('arquivos_txt\\canais.txt', "r", encoding="utf-8")
            arquivo = txt.readlines()
            canais = arquivo[12].replace('canais= ','').replace('\n','')
            canais = ast.literal_eval(canais) # Convertendo string em dicionario 

            #envia msg previa
            try:
                for key,value in canais.items():
                    try:
                        ''' Lendo o arquivo txt '''
                        with open('arquivos_txt\\msg_previa.txt',"r", encoding="utf-8") as arquivo:
                            message_previa = arquivo.read()
                        
                        #Variavel Dinâmica
                        bot.send_message(key, 
                                            message_previa.replace('[HORARIO]', minutos), 
                                            parse_mode='HTML', disable_web_page_preview=True)
                    except:
                        pass

                msg_previa_enviada = True

            except:
                pass

    except:pass


# ENVIA PLACAR CANAIS TELEGRAM
def envia_placar_pos_sessao(placar_win_sessao, placar_loss_sessao):

    try:
        #placar()

        ''' Lendo o arquivo txt canais '''
        msg_sessao_finalizada = open('arquivos_txt\\msg_fim_sessao.txt', "r", encoding="utf-8").read()
        txt = open('arquivos_txt\\canais.txt', "r", encoding="utf-8")
        arquivo = txt.readlines()
        canais = arquivo[7].replace('canais= ','').replace('\n','')
        canais = ast.literal_eval(canais) # Convertendo string em dicionario 

        for key, value in canais.items():
            try:
                bot.send_message(key, msg_sessao_finalizada
                                        .replace('[DATA_HOJE]', data_hoje)
                                        .replace('[PLACAR_WIN_SESSAO]', str(placar_win_sessao))
                                        .replace('[PLACAR_LOSS_SESSAO]', str(placar_loss_sessao))
                                        , parse_mode='HTML', disable_web_page_preview=True)
        
            except:
                pass


    except Exception as a:
        logger.error('Exception ocorrido no ' + repr(a))
        #placar = bot.reply_to(message,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%", reply_markup=markup)
        pass


def mensagem_previa(horario):
    global msg_previa_enviada

    try:
        validaData()
       
        with open ('arquivos_txt/tempo_msg_previa.txt', encoding='UTF-8') as arquivo: 
            tempo_previo = arquivo.read()

        horario_atual = datetime.today().strftime('%H:%M') 
        horario_sessao = datetime.strptime(horario,'%H:%M')
        minuto_previo = timedelta(minutes=int(tempo_previo))
        horario_menos_minuto_previo = horario_sessao - minuto_previo
        horario_msg_previa = horario_menos_minuto_previo.strftime('%H:%M')

        if horario_atual == horario_msg_previa and msg_previa_enviada == False:
            
            minutos = open('arquivos_txt/tempo_msg_previa.txt', 'r', encoding='UTF-8').read()
            ''' Lendo o arquivo txt canais '''
            txt = open("arquivos_txt/canais.txt", "r", encoding="utf-8")
            arquivo = txt.readlines()
            canais = arquivo[7].replace('canais= ','').replace('\n','')
            canais = ast.literal_eval(canais) # Convertendo string em dicionario 

            #envia msg previa
            try:
                for key,value in canais.items():
                    try:
                        ''' Lendo o arquivo txt '''
                        with open('arquivos_txt\\msg_previa.txt',"r", encoding="utf-8") as arquivo:
                            message_previa = arquivo.read()
                        
                        #Variavel Dinâmica
                        bot.send_message(key, 
                                            message_previa.replace('[HORARIO]', minutos), 
                                            parse_mode='HTML', disable_web_page_preview=True)
                    except:
                        pass

                msg_previa_enviada = True

            except:
                pass

    except:pass


def valida_horario_sessao():

    global sessao_ativa, contagem_sinais, placar_win_sessao, placar_loss_sessao, msg_previa_enviada

    validaData()
    
    horario_atual = datetime.today().strftime('%H:%M')


    with open ('arquivos_txt/horario_sessoes.txt', encoding='UTF-8') as arquivo: 
        horarios = arquivo.read().split(',')

    with open ('arquivos_txt/qnt_sinais_sessao.txt', encoding='UTF-8') as arquivo: 
        qntd_sinais_sessao = arquivo.read()        

    
    for horario in horarios:

        mensagem_previa(horario)

        if horario_atual == horario and sessao_ativa == False:

            contagem_sinais = 0
            sessao_ativa = True

            print(f'Sessão das {horario} Ativada!!')

            placar_win_sessao = 0
            placar_loss_sessao = 0

            break
        
        else:
            continue


    #Validação pra Finalizar Sessão
    if contagem_sinais >= int(qntd_sinais_sessao) and sessao_ativa == True:

        print(f'Sessão das Desativada!!')

        envia_placar_pos_sessao(placar_win_sessao, placar_loss_sessao)

        placar_win_sessao = 0
        placar_loss_sessao = 0
        sessao_ativa = False
        msg_previa_enviada = False
        contagem_sinais = 0

    
    #time.sleep(5)


def pegar_evosessionid():

    while True:

        try:

            #LOGIN
            URL = 'https://arbety.eway.dev:3013/api/auth/signin'

            header = {
            'Content-Type': 'application/json'
            }

            payload = {"email":"gabriellaranjeira1610@gmail.com",
                    "password":"Samuray1@!@!"}
            
            response = requests.post(URL, headers=header, json=payload, verify=False)
            
            token_autorizacao = response.json()['access_token']

            
            #### ENTRANDO NO GAME
            #REQUISIÇÃO1
            URL = 'https://arbety.eway.dev:3000/api/sports/login'

            payload = {"game_id": "31848e6ae9134b07b5333ff6e13f776a"}

            header = {
                "Accept":"application/json, text/plain, */*",
                "Authorization":token_autorizacao,
                "Host":"arbety.eway.dev:3000",
                "Origin":"https://www.arbety.com",
                "Referer":"https://www.arbety.com/",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
                "X-Access-Token":token_autorizacao
                }
            
            response = requests.post(URL, json=payload, headers=header, verify=False)

            url_entry_params = json.loads(response.content)['game_url'].split('":"')[1].split('"}')[0]

            #REQUISIÇÃO2
            URL = url_entry_params

            response = requests.get(URL, allow_redirects=False)

            location = 'https://tmkybox.evo-games.com'+response.headers.get('Location')

            #REQUISIÇÃO3
            headers = {
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Cookie":"cdn=https://static.egcdn.com; lang=bp; locale=pt-BR; EVOSESSIONID=rleug2e4au4av7zrrm5kswlek36m5yde6f244ded283c9592b0eaeceba743f902835f77076681aca9",
                "Host":"tmkybox.evo-games.com",
                "Referer":"https://www.arbety.com/",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
            }
            response = requests.get(location, headers=headers, allow_redirects=False, verify=False)

            evosessionid = response.headers.get('Set-Cookie').split('; Path')[0]

            return evosessionid
        
        except:
            time.sleep(10)
            continue


def conectar_websocket(evosessionid):
    global URL
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
        'Cookie':f'cdn=https://static.egcdn.com; lang=bp; locale=pt-BR; {evosessionid}',
        "Host": "tmkybox.evo-games.com",
        "Origin": "https://tmkybox.evo-games.com",
        "Pragma": "no-cache",
        "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
        "Sec-WebSocket-Key": "OB2AkmyQZUp2UQFxnyaUnw==",
        "Sec-WebSocket-Version": "13",
        "Upgrade": "websocket",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

        }

        URL = f'wss://tmkybox.evo-games.com/public/topcard/player/game/TopCard000000001/socket?messageFormat=json&instance=87zegm-rq6dkxywmpfqben5-TopCard000000001&tableConfig=&{evosessionid}&client_version=6.20231201.222826.35479-28ac39f090'
        #URL = f'wss://belloatech.evo-games.com/public/bacbo/player/game/BacBo00000000001/socket?messageFormat=json&instance=pe7y9k-rhjuf7mokioplhho-BacBo00000000001&tableConfig=&EVOSESSIONID={evosessionid}&client_version=6.20230823.71249.29885-78ea79aff8'
        
        ws = create_connection(URL, verify=False)

        ws.send(json.dumps([json.dumps(header)]))

        cont = 0
        ultimo_result = ''
        ultimo_valor_armazenado = ''

    except Exception as e:
        print('ERRO NA FUNÇÃO CONECTAR WEBSOCKET----', e)


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
    global horario_inicio
    global lista_resultados
    global sessao_ativa, contagem_sinais, msg_previa_enviada, placar_win_sessao, placar_loss_sessao

    placar_win_sessao = 0
    placar_loss_sessao = 0
    msg_previa_enviada = False
    sessao_ativa = False
    contagem_sinais = 0

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
                    
                    valida_horario_sessao()

                    if sessao_ativa == True:

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
    txt = open("arquivos_txt/canais.txt", "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[7].replace('canais= ','').replace('\n','')
    canais = ast.literal_eval(canais) # Convertendo string em dicionario 

    ''' Lendo o arquivo txt config-mensagens '''
    txt = open("arquivos_txt/alerta.txt", "r", encoding="utf-8")
    mensagem_alerta = txt.read()

    
    # Enviando Mensagem Telegram
    horario_inicial = datetime.now()

    ''' Enviando mensagem Telegram '''
    try:
        for key,value in canais.items():
            try:

                if value[0] != '' and value[1] != '':
                    ''' Mensagem '''
                    table_alerta = mensagem_alerta\
                                    .replace('[SITE_PC]', value[1])\
                                    .replace('[SITE_MB]', value[1])\
                                    .replace('[SITE_CADASTRO]', value[0])\

                else:
                    table_alerta = mensagem_alerta\
                                    .replace('[SITE_CADASTRO]', value[0])\

                
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
    txt = open("arquivos_txt/canais.txt", "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[7].replace('canais= ','').replace('\n','')
    canais = ast.literal_eval(canais) # Convertendo string em dicionario 

    ''' Lendo o arquivo txt config-mensagens '''
    txt = open("arquivos_txt/sinal.txt", "r", encoding="utf-8")
    mensagem_sinal = txt.read()
    

    # Enviando Mensagem Telegram
    horario_inicial = datetime.now()
    
    try:
        for key, value in canais.items():
            try:
                ''' Mensagem '''
                if value[0] != '' and value[1] != '':
                    table_sinal = mensagem_sinal\
                                    .replace('[COR]','VERMELHO' if estrategia[-1] == 'C' else 'AZUL' if estrategia[-1] == 'V' else 'EMPATE')\
                                    .replace('[SITE_PC]', value[1])\
                                    .replace('[SITE_MB]', value[1])\
                                    .replace('[SITE_CADASTRO]', value[0])\
                    
                else:
                    table_sinal = mensagem_sinal\
                                    .replace('[COR]','VERMELHO' if estrategia[-1] == 'C' else 'AZUL' if estrategia[-1] == 'V' else 'EMPATE')\
                                    .replace('[SITE_CADASTRO]', value[0])\
                                    
                
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
    txt = open("arquivos_txt/canais.txt", "r", encoding="utf-8")
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
    global lista_resultados_sinal, placar_win_sessao, placar_loss_sessao, sessao_ativa, contagem_sinais

    resultado_valida_sinal = []
    contador_cash = 0

    gale = open('arquivos_txt/gale.txt', 'r', encoding='UTF-8').read()

    while contador_cash <= int(gale):

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
                        txt = open("arquivos_txt/canais.txt", "r", encoding="utf-8")
                        arquivo = txt.readlines()
                        canais = arquivo[7].replace('canais= ','').replace('\n','')
                        canais = ast.literal_eval(canais) # Convertendo string em dicionario 

                        ''' Lendo o arquivo txt config-mensagens '''
                        txt = open("arquivos_txt/green.txt", "r", encoding="utf-8")
                        mensagem_green = txt.read()
                        
                        # Enviando Mensagem Telegram
                        horario_inicial = datetime.now()

                        for key, value in canais.items():
                            try:

                                responderMensagemTelegram(key, mensagem_green.replace('[RESULTADO]', ' | '.join(resultado_valida_sinal))).start()
                                time.sleep(0.1)

                            except:
                                pass
                        
                        print('MENSAGEM ENVIADA PARA TODOS OS CANAIS EM ---> ', datetime.now() - horario_inicial)


                    except:
                        pass
                    

                    print('='*150)
                    
                    #Contagem Sinais por Sessão
                    if sessao_ativa == True:
                        contagem_sinais+=1
                        placar_win_sessao+=1

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


    if contador_cash > int(gale):
        print('LOSSS FINAL')
        
        # Preenchendo arquivo txt
        placar_loss +=1
        placar_geral = placar_win + placar_loss
        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
            arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}")
            
        
        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
        

        # editando mensagem
        try:
            ''' Lendo o arquivo txt canais '''
            txt = open("arquivos_txt/canais.txt", "r", encoding="utf-8")
            arquivo = txt.readlines()
            canais = arquivo[7].replace('canais= ','').replace('\n','')
            canais = ast.literal_eval(canais) # Convertendo string em dicionario 

            ''' Lendo o arquivo txt config-mensagens '''
            txt = open("arquivos_txt/red.txt", "r", encoding="utf-8")
            mensagem_red = txt.read()

            # Enviando Mensagem Telegram
            horario_inicial = datetime.now()

            for key,value in canais.items():
                try:

                    responderMensagemTelegram(key, mensagem_red).start()
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
        #Contagem Sinais por Sessão
        if sessao_ativa == True:
            contagem_sinais+=1
            placar_loss_sessao+=1

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
txt = open("arquivos_txt/canais.txt", "r", encoding="utf-8")
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
        markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

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
        markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_excluir_estrategia = bot.reply_to(message, "🤖⛔ Estou validando uma estratégia! Tente novamente em alguns instanstes.", reply_markup=markup)



@bot.message_handler(commands=['📜 Estrategias_Cadastradas'])
def estrategiasCadastradas(message):
    global estrategia
    global estrategias

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

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
    markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

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
    markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

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
    markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    
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
        markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Bot já está pausado ", reply_markup=markup)

    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

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
        
        markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')
        
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
            markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖⛔ Bot já está ativado",
                                reply_markup=markup)

        elif estrategias == []:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖⛔ Cadastre no mínimo 1 estratégia antes de iniciar",
                                reply_markup=markup)
        
        else:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

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
    

    if message_opcoes.text in ['⏰ Horário Sessões']:
        
        try:

            with open ('arquivos_txt/horario_sessoes.txt', encoding='UTF-8') as arquivo: 
                horario_sessoes = arquivo.read()

        except:pass

        try:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
            markup = markup.add(
                                horario_sessoes,
                                '◀ Voltar'
                                )

            message_editar_valor = bot.reply_to(message_opcoes, "🤖 Perfeito! Segue Horário das Sessões. Para Editar, Insira a Nova Lista de Horários Separado por vírgula (,) 👇",
                                    reply_markup=markup)
        
            #Here we assign the next handler function and pass in our response from the user. 
            bot.register_next_step_handler(message_editar_valor, registrar_horario_sessoes)
        
        except:
            message_error = bot.reply_to(message_opcoes, "🤖❌ Algo deu Errado. Tente Novamente.")

    
    if message_opcoes.text in ['🚦 Sinais por Sessão']:
        try:

            with open ('arquivos_txt/qnt_sinais_sessao.txt', encoding='UTF-8') as arquivo: 
                qntd_sinais_sessao = arquivo.read()

        except:pass

        try:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
            markup = markup.add(
                                qntd_sinais_sessao,
                                '◀ Voltar'
                                )

            message_editar_valor = bot.reply_to(message_opcoes, "🤖 Perfeito! Segue Quantidade de Sinais Por Sessão. Para Editar, Insira o Novo Valor 👇",
                                    reply_markup=markup)
        
            #Here we assign the next handler function and pass in our response from the user. 
            bot.register_next_step_handler(message_editar_valor, registrar_qntd_sinais)
        
        except:
            message_error = bot.reply_to(message_opcoes, "🤖❌ Algo deu Errado. Tente Novamente.")

    



@bot.message_handler()
def registrarTipoEstrategia(message_tipo_estrategia):
    global resposta_usuario

    if message_tipo_estrategia.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_tipo_estrategia, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        return


    if message_tipo_estrategia.text in ['ESTRATÉGIAS PADRÕES']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')


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
        markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

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
    markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    bot.reply_to(message_estrategia, "🤖 Estratégia cadastrada com sucesso! ✅", reply_markup=markup)



def registrarEstrategiaExcluida(message_excluir_estrategia):
    global estrategia
    global estrategias

    if message_excluir_estrategia.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

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
    markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    bot.reply_to(message_excluir_estrategia, "🤖 Estratégia excluída com sucesso! ✅", reply_markup=markup)


def registrar_horario_sessoes(message_editar_valor):
    
    if message_editar_valor.text == '◀ Voltar':
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')
        
        message_opcoes = bot.reply_to(message_editar_valor, "🤖 Escolha uma opção 👇",
                                    reply_markup=markup)
            
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(message_opcoes, opcoes)
    
    else:
        try:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')
        
            with open ('arquivos_txt/horario_sessoes.txt', 'w', encoding='UTF-8') as arquivo: 
                        arquivo.write(message_editar_valor.text)

            message_sucess = bot.reply_to(message_editar_valor, "🤖 Horarios Editados com Sucesso! ✅", reply_markup=markup)
            
        except:
            pass


def registrar_qntd_sinais(message_editar_valor):

    if message_editar_valor.text == '◀ Voltar':
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')
        
        message_opcoes = bot.reply_to(message_editar_valor, "🤖 Escolha uma opção 👇",
                                    reply_markup=markup)
            
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(message_opcoes, opcoes)
    
    else:
        try:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')
        
            with open ('arquivos_txt/qnt_sinais_sessao.txt', 'w', encoding='UTF-8') as arquivo: 
                        arquivo.write(message_editar_valor.text)

            message_sucess = bot.reply_to(message_editar_valor, "🤖 Quantidade de Sinais Editado com Sucesso! ✅", reply_markup=markup)
            
        except:
            pass






while True:
    try:
        bot.infinity_polling(timeout=600)
    except:
        bot.infinity_polling(timeout=600)


