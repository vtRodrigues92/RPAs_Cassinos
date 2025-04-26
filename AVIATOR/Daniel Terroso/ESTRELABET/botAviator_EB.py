from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
import logging
from datetime import datetime, timedelta
import telebot
from telegram.ext import *
from telebot import *
import os
import ast
import warnings
#from webdriver_manager.firefox import GeckoDriverManager
import requests
import threading
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


#_______________________________________________________________________#____________________________________________________________________________________________________

print()
print('                                #################################################################')
print('                                ###################     BOT AVIATOR     #########################')
print('                                #################################################################')
print('                                ##################### SEJA BEM VINDO ############################')
print('                                #################################################################')
print('                                ############# DESENVOLVIDO POR VICTOR RODRIGUES #################')
print('                                #################################################################\n')
print('Versão = 2.0.0')
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
                    'link_refer':[value[1] for key,value in self.canais.items()],
                    'link_game_bet':[value[0] for key,value in self.canais.items()]
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

    if horario_atual >= horario_refresh:
        print('HORA DE REFRESHAR A PAGINA!!!!')
        
        browser.close()

        time.sleep(10)

        inicio()

        logar_site()
        
        #logar_site()
        #time.sleep(10)
        horario_inicio = datetime.now()

        return True
    
    else: return False


def inicio():
    global sticker_alerta
    global sticker_win
    global sticker_win_2x
    global sticker_win_5x
    global sticker_loss
    global logger
    global browser
    global lista_anterior
    global horario_inicio
    global url
    global headers

    url = "https://app.bootbost.com.br/api/v1/call"
    
    headers = {
    'Content-Type': 'application/json'
    }

    horario_inicio = datetime.now()

    lista_anterior = []
    logger = logging.getLogger()

    # Definindo opções para o browser
    warnings.filterwarnings("ignore", category=DeprecationWarning) 
    chrome_options = webdriver.ChromeOptions() 
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument('--disable-application-cache')
    #chrome_options.add_experimental_option('useAutomationExtension', False)
    #chrome_options.add_argument("--incognito") #abrir chrome no modo anônimo
    #chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    #chrome_options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    #chrome_options.add_argument("window-size=1037,547")
    #chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    #chrome_options.add_argument('disable-extensions')
    #chrome_options.add_argument('disable-popup-blocking')
    #chrome_options.add_argument('disable-infobars')
    #chrome_options.add_argument('--disable-dev-shm-usage')
    #chrome_options.add_argument('log-level=3')

    browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)                      # Chrome
    #browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())                                     # FireFox        
    #browser  = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install())                       # Brave
    #browser = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(),chrome_options=chrome_options)                     # Chromium


def logar_site():

    #logger = logging.getLogger()
    browser.get(r"https://estrelabet.com/pb#/overview")
    try:
        browser.maximize_window()
    except:pass
    
    time.sleep(15)

    ''' Mapeando elementos para inserir credenciais '''
    try:
        #browser.find_element_by_xpath('//*[@id="trader-estrelabet"]/div[2]/div/a[1]').click() #Recusando cookies
        #browser.find_element_by_xpath('//*[@id="trader-estrelabet"]/div[1]/div/a[1]').click() #Recusando cookies
        browser.find_element_by_xpath('//*[@class="cookie-layout"]//*[@class="cookie-accept"]//*[@class="site-btn site-btn__primary"]').click()
    
    except:
        try:
            browser.find_element_by_link_text("Got It").click()
        
        except:
            pass

    try:

        ''' Inserindo login e senha '''
        ''' Lendo o arquivo txt config-mensagens '''
        txt = open("canais.txt", "r", encoding="utf-8")
        mensagem_login = txt.readlines()
        usuario = mensagem_login[2].replace('\n','').split('= ')[1] 
        senha = mensagem_login[3].replace('\n','').split('= ')[1]

        while True:
            try:

                ''' Mapeando elementos para inserir credenciais '''
                try:
                    browser.find_element_by_xpath('//*[@class="header-right-menu main-header-wrpr--desktop"]//*[text()="Conecte-se"]').click()
                    time.sleep(2)
                except:pass
                
                browser.find_element_by_xpath('//*[@class="controls"]//*[@type="email"]').send_keys(usuario) #Inserindo login
                browser.find_element_by_xpath('//*[@class="form-group"]//*[@type="password"]').send_keys(senha) #Inserindo senha
                browser.find_element_by_xpath('//*[@class="login_submitBtn"]//*[@type="button"]').click() #Clicando no btn login
                time.sleep(10)
                break

            except:
                break
                #print('ERRO AO INSERIR LOGIN -- CONTATE O DESENVOLVEDOR')

        ''' Verificando se o login foi feito com sucesso'''
        t3 = 0
        while t3 < 20:
            if browser.find_elements_by_xpath('//*[@id="header"]/div[1]/div[1]/div/div[2]/div[2]/ul/li[1]') != []:
                break
            else:
                t3+=1

    except:pass

    ''' Acessando o jogo '''
    browser.get('https://estrelabet.com/pb/gameplay/aviator/real-game')
    time.sleep(20)

    # MODO TELA CHEIA
    #contador = 0
    #while contador<10:
    #    try:

    #        tela_cheia = browser.find_element_by_id('gamePlayIframe').get_attribute('src')
    #        browser.get(tela_cheia)
    #        time.sleep(10)
    #        break

    #    except:
    #        contador+=1
    #        time.sleep(3)
    #        continue

    acessarIframe()

    #CLICANDO EM MINIMIZAR O CHAT
    #c=0
    #while c < 10:
    #    try:
    #        browser.find_element_by_xpath('//*[@class="close"]').click()
    #        break
    #    except:
    #        c+=1
    #        time.sleep(3)
    #        continue
    
    #MINIMIZANDO A TELA
    try:
        browser.minimize_window()
    except:
        pass



def acessarIframe():
    t=0
    while t < 10:
        try:
            iframe = browser.find_element_by_id('gamePlayIframe')
            browser.switch_to.frame(iframe)
            break
        
        except:
            time.sleep(5)
            t+=1


def enviar_alerta(estrategia, vela_atual):
    global contador_passagem

    '''Lendo o arquivo txt canais '''
    txt = open("chats.txt", "r", encoding="utf-8")
    arquivo = txt.read()
    canais = ast.literal_eval(arquivo) # Convertendo string em dicionario 

    ''' Lendo o arquivo txt config-mensagens '''
    txt = open("config-mensagens.txt", "r", encoding="utf-8")
    mensagem_alerta = txt.readlines()
    
    # Enviando POST para a API
    try:

        texto = mensagem_alerta[0].replace('\n','') + '\n\n' + \
                  mensagem_alerta[2].replace('\n','') + '\n\n' + \
                  mensagem_alerta[4].replace('\n','').replace('[VELA_ATUAL]', vela_atual).replace('[OPERADOR]', 'maior' if estrategia[-3][0] == '+' else 'menor').replace('[ULTIMA_CONDICAO]', estrategia[-3][1:])
        
        enviarPostAPI(canais, 'alert', texto).start()

    except Exception as e:
        print(e)
    
    # Enviando Mensagem Telegram
    horario_inicial = datetime.now()
    
    try:
        for key, value in canais.items():
            try:
                # Mensagem
                
                if value[1] != '':

                    table_alerta = mensagem_alerta[0].replace('\n','') + '\n\n' + \
                                mensagem_alerta[2].replace('\n','') + '\n\n' + \
                                mensagem_alerta[4].replace('\n','').replace('[VELA_ATUAL]', vela_atual).replace('[OPERADOR]', 'maior' if estrategia[-3][0] == '+' else 'menor').replace('[ULTIMA_CONDICAO]', estrategia[-3][1:]) + '\n\n' + \
                                mensagem_alerta[6].replace('\n','').replace('[LINK_JOGO]', value[0]) + '\n\n' + \
                                mensagem_alerta[8].replace('\n','').replace('[LINK_CADASTRO]', value[1])

                else:

                    table_alerta = mensagem_alerta[0].replace('\n','') + '\n\n' + \
                                    mensagem_alerta[2].replace('\n','') + '\n\n' + \
                                    mensagem_alerta[4].replace('\n','').replace('[VELA_ATUAL]', vela_atual).replace('[OPERADOR]', 'maior' if estrategia[-3][0] == '+' else 'menor').replace('[ULTIMA_CONDICAO]', estrategia[-3][1:]) + '\n\n' + \
                                    mensagem_alerta[6].replace('\n','').replace('[LINK_JOGO]', value[0])
                
                globals()[f'alerta_{key}'] = enviarAlertaTelegram(key, table_alerta).start()
                
                time.sleep(0.2)

            except:
                print('NÃO CONSEGUI ENVIAR A MENSAGEM PARA O CANAL', key)

    except:
        pass

    print('MENSAGEM ENVIADA PARA TODOS OS CANAIS EM ---> ', datetime.now() - horario_inicial)

    contador_passagem = 1


def enviar_sinal(vela_atual, estrategia):
    global table_sinal

    '''Lendo o arquivo txt canais '''
    txt = open("chats.txt", "r", encoding="utf-8")
    arquivo = txt.read()
    canais = ast.literal_eval(arquivo) # Convertendo string em dicionario 

    ''' Lendo o arquivo txt config-mensagens '''
    txt = open("config-mensagens.txt", "r", encoding="utf-8")
    mensagem_sinal = txt.readlines()

    #ENVIANDO POST PARA A API
    try:
    
        texto = mensagem_sinal[16].replace('\n','') + '\n\n' + \
                mensagem_sinal[18].replace('\n','').replace('[VELA_ATUAL]', vela_atual) + '\n\n' + \
                mensagem_sinal[20].replace('\n','').replace('[CASH_OUT]', estrategia[-2]),
        
        enviarPostAPI(canais, 'confirm', texto).start()
    
    except Exception as e:
        print(e)

    # Enviando Mensagem Telegram
    horario_inicial = datetime.now()
    
    try:
        for key, value in canais.items():
            try:

                # Mensgaem
                if value[1] != '':
                    table_sinal = mensagem_sinal[16].replace('\n','') + '\n\n' + \
                                  mensagem_sinal[18].replace('\n','').replace('[VELA_ATUAL]', vela_atual) + '\n\n' + \
                                  mensagem_sinal[20].replace('\n','').replace('[CASH_OUT]', estrategia[-2]) + '\n\n' + \
                                  mensagem_sinal[22].replace('\n','').replace('[LINK_JOGO]', value[0]) + '\n\n' + \
                                  mensagem_sinal[24].replace('\n','').replace('[LINK_CADASTRO]', value[1]) + '\n\n' + \
                                  mensagem_sinal[26].replace('\n','')
                                
                else:
                    table_sinal = mensagem_sinal[16].replace('\n','') + '\n\n' + \
                                  mensagem_sinal[18].replace('\n','').replace('[VELA_ATUAL]', vela_atual) + '\n\n' + \
                                  mensagem_sinal[20].replace('\n','').replace('[CASH_OUT]', estrategia[-2]) + '\n\n' + \
                                  mensagem_sinal[22].replace('\n','').replace('[LINK_JOGO]', value[0]) + '\n\n' + \
                                  mensagem_sinal[26].replace('\n','')
                              
                globals()[f'sinal_{key}'] = enviarSinalTelegram(key, table_sinal).start()
                
                time.sleep(0.1)

            except:
                print('NÃO CONSEGUI ENVIAR A MENSAGEM PARA O CANAL', key)
                pass
    
    except:
        pass
    
    print('MENSAGEM ENVIADA PARA TODOS OS CANAIS EM ---> ', datetime.now() - horario_inicial)


def apagar_alerta():
    global contador_passagem

    '''Lendo o arquivo txt canais '''
    txt = open("chats.txt", "r", encoding="utf-8")
    arquivo = txt.read()
    canais = ast.literal_eval(arquivo) # Convertendo string em dicionario 

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


def validador_estrategia(estrategia, lista_resultados, sequencia_minima):
    # Validando se o resultado se encaixa na estratégia ( TRUE ou FALSE )
    validador = []
    try:
        for e in enumerate(estrategia[:-2]): 
            for v in enumerate(lista_resultados[int(-sequencia_minima):]):

                while v[0] == e[0]:
                    if '+' in e[1]:
                        if float(v[1]) > float(e[1][1:]):
                            validador.append(True)
                            break
                        else:
                            validador.append(False)
                            break

                        
                    if '-' in e[1]:
                        if float(v[1]) < float(e[1][1:]):
                            validador.append(True)
                            break
                        else:
                            validador.append(False)
                            break


                    else:
                        print('ERRO NA ESTRATÉGIA ', estrategia,'...VERIFIQUE O CADASTRO DA MESMA.')
                        time.sleep(3)
                        break


        print(f'Validador  --> {validador}')
        return validador
    except:
        pass


def coletar_dados():
    global estrategia

    while True:

        # Validando data para envio do relatório diário
        refreshar_pagina = auto_refresh()

        if refreshar_pagina == True:
            print('HORA DE REFRESHAR A PAGINA!!!!')
            logar_site()
            time.sleep(10)
        
        else:pass

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass
        
    
        while True:
            try:
                # Auto Refresh
                refreshar_pagina = auto_refresh()

                if refreshar_pagina == True:
                    print('HORA DE REFRESHAR A PAGINA!!!!')
                    logar_site()
                    time.sleep(10)
                
                else:pass

                # Validando data para envio do relatório diário
                validaData()
                
                # Validando se foi solicitado o stop do BOT
                if parar != 0:
                    break
                else:
                    pass

                #ROLANDO A RELA PARA BAIXO E PARA CIMA
                try:
                    #ELEMENTO QUALQUER DENTRO DO IFRAME
                    elem = browser.find_element_by_xpath('//*[@class="dom-container"]')
                    #CLICANDO NO ELEMENTO
                    ActionChains(browser).move_to_element(elem).click().perform()
                    time.sleep(1)

                    #INDO ATÉ O FIM DA TELA
                    ActionChains(browser)\
                    .key_down(Keys.END)\
                    .perform()
                    time.sleep(1)

                    #SUBINDO ATÉ O COMEÇO DA TELA
                    ActionChains(browser)\
                    .key_down(Keys.HOME)\
                    .perform()

                except:
                    pass


                
                lista_resultados = []
                # Pegando o histórico de resultados
                historico_velas = browser.find_elements_by_xpath('//*[@class="payout ng-star-inserted"]')
                
                ''' Inserindo velas na lista'''
                try:
                    for vela in reversed(historico_velas[:10]):
                        numero = vela.text.replace('x','')
                        lista_resultados.append(numero)
                except:
                    print('Erro ao inserir resultados na Lista... Refreshando...')
                    logar_site()
                    continue
                

                ''' VALIDANDO SE TEM DADO VAZIO NA LISTA'''
                if '' in lista_resultados:
                    continue

                ''' VALIDANDO SE A LISTA ESTA VAZIA'''
                if lista_resultados == []:
                    logar_site()
                    continue

                
                # Validando se foi solicitado o stop do BOT
                if parar != 0:
                    break
                else:
                    pass
                

                print(datetime.now().strftime('%H:%M'))
                ''' Chama a função que valida a estratégia para enviar o sinal Telegram '''
                validar_estrategia(lista_resultados, estrategias)   #Lista de estrategia

                print('=' * 100)
                lista_resultados = []
                break

                ''' Exceção se o jogo não estiver disponível '''
            except:
                print('Algo deu errado na funcao Coletar Dados..Refreshando...')
                logar_site()


def validar_estrategia(lista_resultados, estrategias):
    global gale
    global vela_atual

    try:
        for estrategia in estrategias:

            # Validando se foi solicitado o stop do BOT
            if parar != 0:
                break
            else:
                pass


            print ('Analisando a Estrategia --> ', estrategia)

            sequencia_minima_alerta = len(estrategia[:-3])
            sequencia_minima_sinal = len(estrategia[:-2])


            print('Historico_Velas --> ', lista_resultados)

            ''' VALIDADOR DE ESTRATEGIA '''
            validador = validador_estrategia(estrategia, lista_resultados, sequencia_minima_alerta)

            ''' Validando se bateu alguma condição'''
            if validador.count(True) == int(sequencia_minima_alerta):
                print('ENVIANDO ALERTA')

                vela_atual = lista_resultados[-1]

                enviar_alerta(estrategia, vela_atual)
                print('=' * 100)
                time.sleep(1)
                
                ''' Verifica se a ultima condição bate com a estratégia para enviar sinal Telegram '''
                while True:
                    
                    # Relatório de Placar
                    validaData()

                    # Validando se foi solicitado o stop do BOT
                    if parar != 0:
                        break
                    else:
                        pass
                    
                    ''' Lendo novos resultados para validação da estratégia'''
                    numeros_recentes_validacao = browser.find_elements_by_xpath('//*[@class="payout ng-star-inserted"]')
                        
                    ''' LISTA DO PROXIMO RESULTADO APOS O ALERTA'''
                    lista_proximo_resultados = []
                    try:
                        for numeroRecente in reversed(numeros_recentes_validacao[:10]):
                            numero_r = numeroRecente.text.replace('x','')
                            lista_proximo_resultados.append(numero_r)
                    except:
                        continue
                    
                    print(lista_proximo_resultados)

                    if '' in lista_proximo_resultados:
                        continue
                    

                    ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
                    if lista_resultados != lista_proximo_resultados:
                        validador = validador_estrategia(estrategia, lista_proximo_resultados, sequencia_minima_sinal)

                        ''' ALIMENTANDO O BANCO '''
                        #alimenta_banco_painel(lista_proximo_resultados)

                        ''' VALIDA SE ENVIA SINAL OU APAGA O ALERTA '''
                        if validador.count(True) == int(sequencia_minima_sinal):
                            print(lista_proximo_resultados[-1])
                            print('ENVIA SINAL TELEGRAM')
                            vela_atual = lista_proximo_resultados[-1]
                            enviar_sinal(vela_atual, estrategia)
                            print('=' * 100)
                            checar_sinal_enviado(lista_proximo_resultados, estrategia)
                            time.sleep(2)
                            break


                        else:
                            print('APAGA SINAL DE ALERTA')
                            apagar_alerta()
                            print('=' * 100)
                            lista_resultados = lista_proximo_resultados
                            time.sleep(2)
                            break
            
            else:
                print('=' * 100)


    except:
        pass


def checar_sinal_enviado(lista_proximo_resultados, estrategia):
    global table
    global message_canal
    global resultados_sinais
    global ultimo_horario_resultado
    global validador_sinal
    global stop_loss
    global contador_passagem
    global lista_resultados_sinal
    global placar_win
    global placar_semGale
    global placar_gale1
    global placar_gale2
    global placar_loss
    global placar_geral
    global asserividade
    global data_hoje
    global lista_resultados


    resultados = []
    contador_cash = 0

    while contador_cash <= int(estrategia[-1]):

        # Validando data para envio do relatório diário
        validaData()

        # Validando data para envio do relatório diário
        refreshar_pagina = auto_refresh()

        if refreshar_pagina == True:
            print('HORA DE REFRESHAR A PAGINA!!!!')
            logar_site()
            time.sleep(10)
        
        else:pass

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass


        try:
            ''' Lendo novos resultados para validação da estratégia'''
            numeros_recentes_validacao = browser.find_elements_by_xpath('//*[@class="payout ng-star-inserted"]')

            lista_resultados_sinal = []
            try:
                for numeroRecente in reversed(numeros_recentes_validacao[:10]):
                    numero_r = numeroRecente.text.replace('x','')
                    lista_resultados_sinal.append(numero_r)
            except:
                continue


            if '' in lista_resultados_sinal:
                continue
            

            ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
            if lista_proximo_resultados != lista_resultados_sinal:

                resultados.append(lista_resultados_sinal[-1])
                
                print(lista_resultados_sinal[-1])
                #alimenta_banco_painel(lista_resultados_sinal)
            
                # VALIDANDO WIN OU LOSS
                if float(lista_resultados_sinal[-1]) >= float(estrategia[-2].strip('xX')):
                    
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

                        # Somando Win na estratégia da lista atual
                        for pe in placar_estrategias:
                            if pe[:-5] == estrategia:
                                pe[-5] = int(pe[-5])+1

                        

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

                        # Somando Win na estratégia da lista atual
                        for pe in placar_estrategias:
                            if pe[:-5] == estrategia:
                                pe[-4] = int(pe[-4])+1



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
                        
                        # Somando Win na estratégia da lista atual
                        for pe in placar_estrategias:
                            if pe[:-5] == estrategia:
                                pe[-3] = int(pe[-3])+1


                    # respondendo a mensagem do sinal e condição para enviar sticker
                    try:
                        '''Lendo o arquivo txt canais '''
                        txt = open("chats.txt", "r", encoding="utf-8")
                        arquivo = txt.read()
                        canais = ast.literal_eval(arquivo) # Convertendo string em dicionario 

                        ''' Lendo o arquivo txt config-mensagens '''
                        txt = open("config-mensagens.txt", "r", encoding="utf-8")
                        mensagem_green = txt.readlines()
                        
                        #ENVIANDO POST PARA A API
                        try:
                        
                            texto = mensagem_green[32].replace('\n','').replace('[RESULTADO]', ' | '.join(resultados))

                            enviarPostAPI(canais, 'success', texto).start()
                        
                        except Exception as e:
                            print(e)
                        
                        # Enviando Mensagem Telegram
                        horario_inicial = datetime.now()

                        for key, value in canais.items():
                            try:
                            
                                responderMensagemTelegram(key, mensagem_green[32].replace('[RESULTADO]', ' | '.join(resultados))).start()
                                time.sleep(0.1)

                            except:
                                pass
                        
                        print('MENSAGEM ENVIADA PARA TODOS OS CANAIS EM ---> ', datetime.now() - horario_inicial)

                    except:
                        pass
                    
                    print('=' * 100)
                    validador_sinal = 0
                    contador_cash = 0
                    contador_passagem = 0
                    lista_resultados = lista_resultados_sinal
                    return
        
                else:
                    print('LOSSS')
                    print('=' * 100)
                    contador_cash+=1
                    lista_proximo_resultados = lista_resultados_sinal
                    continue
        
        except:
            continue


    if contador_cash > int(estrategia[-1]):
        print('LOSSS GALE ',estrategia[-1])

        # Preenchendo arquivo txt
        placar_loss +=1
        placar_geral = placar_win + placar_loss
        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
            arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}")
            
        
        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
            
        # editando mensagem
        try:
            '''Lendo o arquivo txt canais '''
            txt = open("chats.txt", "r", encoding="utf-8")
            arquivo = txt.read()
            canais = ast.literal_eval(arquivo) # Convertendo string em dicionario 

            ''' Lendo o arquivo txt config-mensagens '''
            txt = open("config-mensagens.txt", "r", encoding="utf-8")
            mensagem_red = txt.readlines()

            #ENVIANDO POST PARA A API
            try:
            
                texto = mensagem_red[34].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(resultados))

                enviarPostAPI(canais, 'failure', texto).start()
            
            except Exception as e:
                print(e)
            
            # Enviando Mensagem Telegram
            horario_inicial = datetime.now()

            for key, value in canais.items():
                try:
                
                    responderMensagemTelegram(key, mensagem_red[34].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(resultados))).start()
                    time.sleep(0.1)

                except:
                    pass
            
            print('MENSAGEM ENVIADA PARA TODOS OS CANAIS EM ---> ', datetime.now() - horario_inicial)

            
        except:
            pass


        # Atualizando placar da estratégia
        for pe in placar_estrategias:
            if pe[:-5] == estrategia:
                pe[-1] = int(pe[-1])+1

        
        
        print('=' * 100)
        validador_sinal = 0
        contador_cash = 0
        contador_passagem = 0
        lista_resultados = lista_resultados_sinal
        return






inicio()            # Difinição do webBrowser
logar_site()         # Logando no Site
placar()             # Chamando o Placar


#________________________________________________________________________________________ TELEGRAM__________________________________________________________________________________#


print('\n\n')
print('############################################ AGUARDANDO COMANDOS ############################################')



# PLACAR
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
botStatus = 0
contador_passagem = 0
lista_estrategias = []



# LENDO TXT PARA DEFINIR VARIAVEL DE CANAIS E VALIDAÇÃO DE USUÁRIO
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
     while True:
        try:
            global parar
            global browser
            parar = 1
            time.sleep(1)
            break

        except:
            continue




@bot.message_handler(commands=['🤑 Cadastrar Canal'])
def cadastra_canal(message):
    try:
        #Init keyboard markup
        markup_canal = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
        markup_canal = markup_canal.add('◀ Voltar')    

        mensagem_cadastro = bot.reply_to(message, "🤖 Ok! Insira as Informações do Canal no Padrão a Seguir: -12345678,www.link_game.com,www.link_afiliado.com 👇", reply_markup=markup_canal)
        bot.register_next_step_handler(mensagem_cadastro, registra_canal_cadastrado)

    except Exception as e:
        print(e)



@bot.message_handler(commands=['💬 Listar_Canais'])
def listar_canais(message):
    try:
        with open('chats.txt', 'r', encoding='UTF-8') as file:
            lista_canais = file.read()
            lista_canais = ast.literal_eval(lista_canais)

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','🟢 Ativar Bot', '🤑 Cadastrar Canal', '💬 Listar Canais', '🚮 Excluir Canal', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        bot.reply_to(message, "🤖 Ok! Listando Canais Cadastrados....", reply_markup=markup)

        for key, value in lista_canais.items():

            bot.send_message(message.chat.id, 
f'Canal: {key}\n\
Link Game: {value[0]}\n\
Link Afiliado: {value[1]}\n\
===========================')
            
    except Exception as e:
        print(e)



@bot.message_handler(commands=['🚮 Excluir_Canal'])
def excluir_canal(message):
    global lista_canais

    try:
        with open('chats.txt', 'r', encoding='UTF-8') as file:
            lista_canais = file.read()
            lista_canais = ast.literal_eval(lista_canais)

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        #Add to buttons by list with ours generate_buttons function.
        markup_canais = generate_buttons_estrategias([key for key, value in lista_canais.items()], markup)    
        markup_canais.add('◀ Voltar')

        message_excluir_canal = bot.reply_to(message, "🤖 Escolha o Canal a ser excluído ou Insira uma lista de Canais separado por vírgula 👇", reply_markup=markup_canais)
        bot.register_next_step_handler(message_excluir_canal, registrar_canal_excluido)
    
    except Exception as e:
        print(e)



@bot.message_handler(commands=['⚙ Cadastrar_Estratégia'])
def cadastrarEstrategia(message):

    global contador_passagem

    if contador_passagem == 0:
        #Init keyboard markup
        markup_tipo = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
        
        markup_tipo = markup_tipo.add('◀ Voltar', 'ESTRATÉGIAS PADRÕES', 'NOVA ESTRATÉGIA')    

        message_tipo_estrategia = bot.reply_to(message, "🤖 Ok! Escolha cadastrar uma nova estratégia ou cadastrar estratégias padrões 👇", reply_markup=markup_tipo)
        bot.register_next_step_handler(message_tipo_estrategia, registrarTipoEstrategia)
    
    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','🟢 Ativar Bot', '🤑 Cadastrar Canal', '💬 Listar Canais', '🚮 Excluir Canal', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

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
        markup = markup.add('/start','🟢 Ativar Bot', '🤑 Cadastrar Canal', '💬 Listar Canais', '🚮 Excluir Canal', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_excluir_estrategia = bot.reply_to(message, "🤖⛔ Estou validando uma estratégia! Tente novamente em alguns instanstes.", reply_markup=markup)



@bot.message_handler(commands=['📜 Estrategias_Cadastradas'])
def estrategiasCadastradas(message):
    global estrategia
    global estrategias

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup = markup.add('/start','🟢 Ativar Bot', '🤑 Cadastrar Canal', '💬 Listar Canais', '🚮 Excluir Canal', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    bot.reply_to(message, "🤖 Ok! Listando estratégias", reply_markup=markup)

    for estrategia in estrategias:
        #print(estrategia)
        bot.send_message(message.chat.id, f'{estrategia}')



@bot.message_handler(commands=['📊 Placar Atual'])
def placar_atual(message):
    global placar
    global resultados_sinais

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=3)
    markup = markup.add('/start','🟢 Ativar Bot', '🤑 Cadastrar Canal', '💬 Listar Canais', '🚮 Excluir Canal', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

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
    markup = markup.add('/start','🟢 Ativar Bot', '🤑 Cadastrar Canal', '💬 Listar Canais', '🚮 Excluir Canal', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

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
    markup = markup.add('/start','🟢 Ativar Bot', '🤑 Cadastrar Canal', '💬 Listar Canais', '🚮 Excluir Canal', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    
    for pe in placar_estrategias:
        total = int(pe[-5]) + int(pe[-4]) + int(pe[-3]) + int(pe[-2]) + int(pe[-1])
        soma_win = int(pe[-5]) + int(pe[-4]) + int(pe[-3]) + int(pe[-2])

        try:
            assertividade = str(round(soma_win / total*100, 1)).replace('.0',"")+"%"
        except:
            assertividade = '0%'

        bot.send_message(message.chat.id, f'🧠 {pe[:-5]} \n==========================\n 🏆= {pe[-5]}  |  🥇= {pe[-4]}  |  🥈= {pe[-3]}  |  🥉= {pe[-2]} \n\n ✅ - {soma_win} \n ❌ - {pe[-1]} \n==========================\n 🎯 {assertividade}  ', reply_markup=markup)
        


    

@bot.message_handler(commands=['🛑 Pausar_bot'])
def pausar(message):
    global botStatus
    global contador_passagem

    

    if botStatus == 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','🟢 Ativar Bot', '🤑 Cadastrar Canal', '💬 Listar Canais', '🚮 Excluir Canal', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Bot já está pausado ", reply_markup=markup)

    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','🟢 Ativar Bot', '🤑 Cadastrar Canal', '💬 Listar Canais', '🚮 Excluir Canal', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        print('\n\n')
        print('Pausar Bot')
        print('Parando o Bot....\n')
        botStatus = 0
        pausarBot()

        message_final = bot.reply_to(message, "🤖 Ok! Bot pausado 🛑", reply_markup=markup)
        
        print('###################### AGUARDANDO COMANDOS ######################')




        
@bot.message_handler(commands=['start'])
def start(message):

    if str(message.chat.id) in ids:

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','🟢 Ativar Bot', '🤑 Cadastrar Canal', '💬 Listar Canais', '🚮 Excluir Canal', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message, "🤖 Bot Aviator Iniciado! ✅ Escolha uma opção 👇",
                                reply_markup=markup)
        
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(message_opcoes, opcoes)
    
    else:
        message_error = bot.reply_to(message, "🤖 Você não tem permissão para acessar este Bot ❌🚫")





@bot.message_handler()
def opcoes(message_opcoes):
    global message_canal
    global estrategia
    global stop_loss
    global botStatus
    global parar
    global reladiarioenviado
    global contador_outra_oportunidade
    global browser
    global dicionario_estrategia_usuario
    global contador_passagem


    
    if message_opcoes.text in ['🤑 Cadastrar Canal']:
        print('CADASTRAR CANAL')

        cadastra_canal(message_opcoes)


    if message_opcoes.text in ['💬 Listar Canais']:
        print('LISTAR CANAIS')

        listar_canais(message_opcoes)


    if message_opcoes.text in ['🚮 Excluir Canal']:
        print('Excluir Canal')

        excluir_canal(message_opcoes)
    

    if message_opcoes.text in ['⚙ Cadastrar Estratégia']:
        print('Cadastrar Estrategia')

        cadastrarEstrategia(message_opcoes)


    if message_opcoes.text in['📜 Estratégias Cadastradas']:
        print('Estrategias Cadastradas')
        estrategiasCadastradas(message_opcoes)


    if message_opcoes.text in ['🗑 Apagar Estratégia']:
        print('Apagar estrategia')
        apagarEstrategia(message_opcoes)



    if message_opcoes.text in ['🟢 Ativar Bot']:
        global botStatus
        global message_canal
        global parar

        print('Ativar Bot')

        if botStatus == 1:

            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','🟢 Ativar Bot', '🤑 Cadastrar Canal', '💬 Listar Canais', '🚮 Excluir Canal', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖⛔ Bot já está ativado",
                                reply_markup=markup)

        elif estrategias == []:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','🟢 Ativar Bot', '🤑 Cadastrar Canal', '💬 Listar Canais', '🚮 Excluir Canal', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖⛔ Cadastre no mínimo 1 estratégia antes de iniciar",
                                reply_markup=markup)
        
        else:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=3)
            markup = markup.add('/start','🟢 Ativar Bot', '🤑 Cadastrar Canal', '💬 Listar Canais', '🚮 Excluir Canal', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖 Ok! Bot Ativado com sucesso! ✅ Em breve receberá sinais nos canais informados no arquivo auxiliar! ",
                                    reply_markup=markup)
            
            botStatus = 1
            reladiarioenviado = 0
            parar=0
            contador_passagem = 0
            stop_loss = []

            print('##################################################  INICIANDO AS ANÁLISES  ##################################################')
            print()
            coletar_dados()

    
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
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=3)
        markup = markup.add('/start','🟢 Ativar Bot', '🤑 Cadastrar Canal', '💬 Listar Canais', '🚮 Excluir Canal', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_tipo_estrategia, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        return


    if message_tipo_estrategia.text in ['ESTRATÉGIAS PADRÕES']:
        #Init keyboard markup
        markup_tipo = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)

        markup_tipo = markup_tipo.add('◀ Voltar', 'CASH OUT 1.5X', 'CASH OUT 2X')

        message_tipo_cash_out = bot.reply_to(message_tipo_estrategia, "🤖 Escolha o grupo de estratégias com o CASH OUT abaixo 👇", reply_markup=markup_tipo)
        bot.register_next_step_handler(message_tipo_cash_out, registrar_cash_out)
        

    else:

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

        resposta_usuario = message_tipo_estrategia.text.lower()
        print(resposta_usuario)
         
        markup_nova_estrategia = markup.add('◀ Voltar')

        message_nova_estrategia = bot.reply_to(message_tipo_estrategia, "🤖 Ok! Escolha um padrão acima ou abaixo de velas, a vela que deverá fazer CASH OUT e uma opção de GALE \n\n Ex: +2,-2,-10.35,1.5X,2", reply_markup=markup_nova_estrategia)
        bot.register_next_step_handler(message_nova_estrategia, registrarEstrategia)




        
@bot.message_handler()
def registrar_cash_out(message_tipo_cash_out):

    if message_tipo_cash_out.text in ['◀ Voltar']:
        #Init keyboard markup
        markup_tipo = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
        
        markup_tipo = markup_tipo.add('◀ Voltar', 'ESTRATÉGIAS PADRÕES', 'NOVA ESTRATÉGIA')    

        message_tipo_estrategia = bot.reply_to(message_tipo_cash_out, "🤖 Ok! Escolha cadastrar uma nova estratégia ou cadastrar estratégias padrões 👇", reply_markup=markup_tipo)
        bot.register_next_step_handler(message_tipo_estrategia, registrarTipoEstrategia)
    

    if message_tipo_cash_out.text in ['CASH OUT 1.5X']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=3)
        markup = markup.add('/start','🟢 Ativar Bot', '🤑 Cadastrar Canal', '💬 Listar Canais', '🚮 Excluir Canal', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        estrategias_padroes = (['-1.8','-1.8','-1.8','-1.8','-1.8','+1.5','1.5x','2'],
                                ['-1.5','-1.5','-1.5','+1.5','1.5x','2'], 
                                ['+1.5','+2','-5','+1.5','1.5x','2'], 
                                ['-2','-2','+1.5','1.5x','2'])
        
        for estrategia_padrao in estrategias_padroes:
            estrategias.append(estrategia_padrao)
            placar_estrategia = [estrategia_padrao[1]]
            placar_estrategia.extend([0,0,0,0,0])
            placar_estrategias.append(placar_estrategia)


        message_aposta = bot.reply_to(message_tipo_cash_out, "🤖 Estratégias Cadastradas ✅", reply_markup=markup)

        
    if message_tipo_cash_out.text in ['CASH OUT 2X']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=3)
        markup = markup.add('/start','🟢 Ativar Bot', '🤑 Cadastrar Canal', '💬 Listar Canais', '🚮 Excluir Canal', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        estrategias_padroes = (
                                ['-1.5','-1.5','-1.5','+1.5','2x','2'],
                                ['+1.5','+2','-5','+1.5','2x','2'],
                                ['-2','-2','+1.5','2x','2'],
                                ['-1.8','-1.8','-1.8','-1.8','-1.8','+1.5','2x','2'],
                                ['-2','-2','-2','-2','-2','-2','+2','2x','2'], 
                                ['-1.9','-1.8','+2','-2','+2','+2','2x','2'], 
                                ['+5','+3','+3','-1.5','-1,5','+2','2x','2']
                              )

        for estrategia_padrao in estrategias_padroes:
            estrategias.append(estrategia_padrao)
            placar_estrategia = [estrategia_padrao[1]]
            placar_estrategia.extend([0,0,0,0,0])
            placar_estrategias.append(placar_estrategia)


        message_sucesso = bot.reply_to(message_tipo_cash_out, "🤖 Estratégias Cadastradas ✅", reply_markup=markup)


        


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
        markup = markup.add('/start','🟢 Ativar Bot', '🤑 Cadastrar Canal', '💬 Listar Canais', '🚮 Excluir Canal', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

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
    markup = markup.add('/start','🟢 Ativar Bot', '🤑 Cadastrar Canal', '💬 Listar Canais', '🚮 Excluir Canal', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    bot.reply_to(message_estrategia, "🤖 Estratégia cadastrada com sucesso! ✅", reply_markup=markup)




    

def registrarEstrategiaExcluida(message_excluir_estrategia):
    global estrategia
    global estrategias

    if message_excluir_estrategia.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','🟢 Ativar Bot', '🤑 Cadastrar Canal', '💬 Listar Canais', '🚮 Excluir Canal', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')
        
        message_opcoes = bot.reply_to(message_excluir_estrategia, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        
        return
    

    estrategia_excluir = message_excluir_estrategia.text
    
    for estrategia in estrategias:
        if estrategia_excluir == str(estrategia):
            estrategias.remove(estrategia)

    
    for pe in placar_estrategias:
        if estrategia_excluir == str(pe[:-5]):
            placar_estrategias.remove(pe)


    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup = markup.add('/start','🟢 Ativar Bot', '🤑 Cadastrar Canal', '💬 Listar Canais', '🚮 Excluir Canal', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    bot.reply_to(message_excluir_estrategia, "🤖 Estratégia excluída com sucesso! ✅", reply_markup=markup)


def registrar_canal_excluido(message_excluir_canal):

    try:

        if message_excluir_canal.text in ['◀ Voltar']:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','🟢 Ativar Bot', '🤑 Cadastrar Canal', '💬 Listar Canais', '🚮 Excluir Canal', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')
            
            message_opcoes = bot.reply_to(message_excluir_canal, "🤖 Escolha uma opção 👇",
                                    reply_markup=markup)
            
            return


        else:
            resposta_usuario = message_excluir_canal.text

            if ',' in resposta_usuario:
                lista_resposta_usuario = message_excluir_canal.text.split(',')
                for chat in lista_resposta_usuario:
                    lista_canais.pop(int(chat))

            else:
                lista_canais.pop(int(resposta_usuario))


            ###ATUALIZANDO TXT CANAIS
            with open('chats.txt', 'w', encoding='UTF-8') as file:
                file.write(str(lista_canais))
                file.close()


            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','🟢 Ativar Bot', '🤑 Cadastrar Canal', '💬 Listar Canais', '🚮 Excluir Canal', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

            bot.reply_to(message_excluir_canal, "🤖 Canal(is) excluído com sucesso! ✅", reply_markup=markup)

    except:
        #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','🟢 Ativar Bot', '🤑 Cadastrar Canal', '💬 Listar Canais', '🚮 Excluir Canal', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

            bot.reply_to(message_excluir_canal, "🤖🔴 Algo Inesperado Aconteceu. Tente Novamente.", reply_markup=markup)


def registra_canal_cadastrado(mensagem_cadastro):
    try:

        if mensagem_cadastro.text in ['◀ Voltar']:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','🟢 Ativar Bot', '🤑 Cadastrar Canal', '💬 Listar Canais', '🚮 Excluir Canal', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')
            
            message_opcoes = bot.reply_to(mensagem_cadastro, "🤖 Escolha uma opção 👇",
                                    reply_markup=markup)
            
            return

        else:
            novo_dado = {}
            resposta_do_usuario = mensagem_cadastro.text.split(',')

            ###LENDO ARQUIVO CANAIS
            with open('chats.txt', 'r', encoding='UTF-8') as file:
                lista_canais = file.read()
                lista_canais = ast.literal_eval(lista_canais)

            novo_dado[int(resposta_do_usuario[0])] = [resposta_do_usuario[1],resposta_do_usuario[2]]
            lista_canais.update(novo_dado) 

            ###ATUALIZANDO ARQUIVO CANAIS
            with open('chats.txt', 'w', encoding='UTF-8') as file:
                file.write(str(lista_canais))
                file.close()

            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','🟢 Ativar Bot', '🤑 Cadastrar Canal', '💬 Listar Canais', '🚮 Excluir Canal', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

            bot.reply_to(mensagem_cadastro, "🤖 Canal Cadastrado com Sucesso! ✅", reply_markup=markup)


    except Exception as e:
        print(e)





    

bot.infinity_polling()






