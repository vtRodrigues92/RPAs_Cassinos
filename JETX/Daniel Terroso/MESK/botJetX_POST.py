#from webbrowser import BaseBrowser
#from xml.dom.minidom import Document
#from selenium import webdriver
import time
import warnings
#from webdriver_manager.chrome import ChromeDriverManager
import logging
from datetime import datetime, timedelta
import telebot
from telegram.ext import *
from telebot import *
#import operator
import os
import ast
#from webdriver_manager.firefox import GeckoDriverManager
import requests
import json



#_______________________________________________________________________#____________________________________________________________________________________________________

print()
print('                                #################################################################')
print('                                ######################   BOT JETX   #############################')
print('                                #################################################################')
print('                                ##################### SEJA BEM VINDO ############################')
print('                                #################################################################')
print('                                ############# DESENVOLVIDO POR VICTOR RODRIGUES #################')
print('                                #################################################################\n')
print('Versão = 1.0.0')
print('Ambiente: Produção\n\n\n')




def requisicao(token_game):
    #with open("api.txt","r") as arquivo:

    while True:
        header = {
        'Content-Type': 'application/json'
        }

        url_jetx =  f'https://eu-server-w2.ssgportal.com/JetXNode41//api/JetXapi/Board/{token_game}' #arquivo.readlines()

        session = requests.Session()
        response = session.get(url_jetx, headers=header)

        #Validando se o Status é diferente de 200
        if response.status_code != 200:

            print('LINK DA API ESTÁ INVÁLIDO! INSIRA UM NOVO LINK.')
            processo_pegar_tokenapi()

        return response


def processo_pegar_tokenapi():
    global token_game
    global uuid_usuario
    global token_game
    global username

    token_autorizacao = logar()
    uuid_usuario = puxar_dados_acesso(token_autorizacao)
    token_game = acessar_game(uuid_usuario)


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
    
    response = requests.post(URL, headers=header, json=payload)
    token = response.json()['token']

    return token


def puxar_dados_acesso(token_autorizacao):
    global username
    global uuid_usuario

    header = {
                'Content-Type': 'application/json',
                "authorization": f"bearer {token_autorizacao}"
                }
    

    payload = {"email":usuario,
               "password":senha}
    

    URL = 'https://backoffice.mesk.bet/api/auth/me'

    response = requests.post(URL, headers=header, json=payload)
    uuid_usuario = response.json()['player']['uuid']

    print(f'uuid_usuario - {uuid_usuario}')

    return uuid_usuario


def acessar_game(uuid_usuario):

    while True:
        #Usando o UUID do usuário Logado para Acessar a SMARTSOFT e Pegar o Token
        URL_FORNECEDOR = f'https://pi.njoybingo.com/game.do?token={uuid_usuario}&pn=meskbet&lang=pt&game=SMARTSOFT-JetX_JetX&type=CHARGED'
        response = requests.get(URL_FORNECEDOR, allow_redirects=False)

        if response.status_code == 302:

            token_location = response.headers.get('location').split('Token=')[1].split('&Portal')[0]

            header = {
            'Content-Type': 'application/json',
            "referer": f"https://eu-server.ssgportal.com/GameLauncher/Loader.aspx?GameCategory=JetX&GameName=JetX&ReturnUrl&Token={token_location}&PortalName=meskbet&skin=meskjet"
            }

            #Usando o Token gerado pelo FORNECEDOR para Acessar o GAME e pegar o TOKEN para ter acesso aos dados do GAME
            URL_GAME = f'https://eu-server.ssgportal.com/GameLauncher/Loader.aspx?GameCategory=JetX&GameName=JetX&ReturnUrl&Token={token_location}&PortalName=meskbet&skin=meskjet'
            response = requests.get(URL_GAME, allow_redirects=False)
            #token_game = response.text.split('RedirectUrl')[2].split('Token=')[1].split('&Lang')[0]
            token_game = response.text.split('HiddenTokenKey')[1].split('value="')[1].split('" id="')[0]

            URL_ACESSO_LOADER = f'https://eu-server-w2.ssgportal.com/JetXNode41/JetXLight/Loader.aspx?Gametype=&GameName=JetXLight&StartPage=Board&Token={token_game}&Lang=en&ReturnURL=&Skin=meskjet'
            response_1 = requests.get(URL_ACESSO_LOADER)

            URL_ACESSO_BOARD = f'https://eu-server-w2.ssgportal.com/JetXNode41/JetXLight/Board.aspx?Token={token_game}&ReturnUrl=&StopUrl=&Skin=meskjet&chat='
            response_2 = requests.get(URL_ACESSO_BOARD)

            return token_game
        
        else:
            time.sleep(5)
            continue


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
        logarSite()
        time.sleep(10)
        horario_inicio = datetime.now()


def inicio():

    global logger
    global url
    global headers
    global lista_resultados

    url = "https://app.bootbost.com.br/api/v1/call"
    headers = {
    'Content-Type': 'application/json'
    }

    logger = logging.getLogger() #Log de erro

    lista_resultados = []

    # Definindo opções para o browser
    warnings.filterwarnings("ignore", category=DeprecationWarning) 
    #chrome_options = webdriver.ChromeOptions() 
    #chrome_options.add_argument("--disable-gpu")
    #chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Opção para executar o prgrama em primeiro ou segundo plano
    #escolha = int(input('Deseja que o programa mostre o navegador? [1]SIM [2]NÃO --> '))
    #print()
    #time.sleep(1)
    #if escolha == 1:
    #    print('O programa será executado mostrando o navegador.\n')
    #else:
    #    print('O programa será executado com o navegador oculto.\n')
    #    chrome_options.add_argument("--headless")

    #browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
    #browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())


def logarSite():
    browser.get(r"https://mesk.bet/")
    browser.maximize_window()
    time.sleep(5)
    try:
        # cookies
        browser.find_element_by_xpath('//*[@id="__layout"]/main/div[4]/div/div/div[2]/button[2]').click()
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
                browser.find_element_by_css_selector('.button-login[data-v-4fd60510]').click()         #Clicando no botão Entrar
                browser.find_element_by_xpath('//*[@id="page-top"]/div[2]/div/div[2]/form/input').send_keys(usuario) #Inserindo login
                browser.find_element_by_xpath('//*[@id="page-top"]/div[2]/div/div[2]/form/div[1]/input').send_keys(senha) #Inserindo senha
                browser.find_element_by_xpath('/html/body/div[1]/div/main/nav/div[2]/div/div[2]/form/div[2]/button').click() #Clicando no btn login
                time.sleep(3)
                break

            except:
                break
                

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
        browser.find_element_by_link_text('Jet X').click()
        time.sleep(10)
        iframe = browser.find_element_by_xpath('/html/body/div[1]/div/main/div[3]/div/div/div/div/div/div[3]/div/iframe')
        link_tela_cheia = iframe.get_attribute('src')
        browser.get(link_tela_cheia)
        time.sleep(10)

        ''' Acessando iframe do jogo'''
        acessarIframe()

    except:
        pass


def acessarIframe():
    t=0
    while t < 10:
        try:
            iframe = browser.find_element_by_id('game-frame')
            browser.switch_to.frame(iframe)
            break
        
        except:
            time.sleep(5)
            t+=1


def enviarAlertaTelegram():
    global contador_passagem

    ''' Lendo o arquivo txt canais '''
    txt = open("canais.txt", "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[12].replace('canais= ','').replace('\n','')
    canais = ast.literal_eval(canais) # Convertendo string em dicionario 
    
    ''' Lendo o arquivo txt config-mensagens '''
    txt = open("config-mensagens.txt", "r", encoding="utf-8")
    mensagem_alerta = txt.readlines()

    #ENVIANDO POST PARA A API
    payload = {
            'status': 'alert', #alert | confirm | success | failure | denied
            'chat_id': [key for key,value in canais.items()],
            'content': mensagem_alerta[0].replace('\n','') + '\n\n' + \
                       mensagem_alerta[2].replace('\n',''),
            'link_refer':[value[1] for key,value in canais.items()],
            'link_game_bet':[value[0] for key,value in canais.items()]
    }

    requests.post(url, headers=headers, json=payload)

    ''' Enviando mensagem Telegram '''    
    try:
        for key, value in canais.items():
            try:
                table_alerta = mensagem_alerta[0].replace('\n','') + '\n\n' + \
                               mensagem_alerta[2].replace('\n','') + '\n\n' + \
                               mensagem_alerta[4].replace('\n','').replace('[LINK_JOGO]', value[0])
            
                globals()[f'alerta_{key}'] = bot.send_message(key, table_alerta, parse_mode='HTML', disable_web_page_preview=True)  #Variavel Dinâmica
            
            except:
                pass
    except:
        pass

    contador_passagem = 1


def enviarSinalTelegram(vela_atual):
    global table_sinal

    ''' Lendo o arquivo txt canais '''
    txt = open("canais.txt", "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[12].replace('canais= ','').replace('\n','')
    canais = ast.literal_eval(canais) # Convertendo string em dicionario 

    ''' Lendo o arquivo txt config-mensagens '''
    txt = open("config-mensagens.txt", "r", encoding="utf-8")
    mensagem_sinal = txt.readlines()

    #ENVIANDO POST PARA A API
    payload = {
            'status': 'confirm', #alert | confirm | success | failure | denied
            'chat_id': [key for key,value in canais.items()],
            'content': mensagem_sinal[13].replace('\n','') + '\n\n' +\
                        mensagem_sinal[15].replace('\n','').replace('[VELA_ATUAL]', vela_atual) + '\n\n' +\
                        mensagem_sinal[17].replace('\n','').replace('\n',''),

            'link_refer':[value[1] for key,value in canais.items()],
            'link_game_bet':[value[0] for key,value in canais.items()]
    }

    requests.post(url, headers=headers, json=payload)

    try:
        for key, value in canais.items():
            try:
                # Estruturando mensgaem
                table_sinal = mensagem_sinal[13].replace('\n','') + '\n\n' +\
                              mensagem_sinal[15].replace('\n','').replace('[VELA_ATUAL]', vela_atual) + '\n\n' +\
                              mensagem_sinal[17].replace('\n','').replace('\n','') + '\n\n' +\
                              mensagem_sinal[19].replace('\n','').replace('[LINK_JOGO]', value[0]) + '\n' +\
                              mensagem_sinal[20].replace('\n','') + '\n' +\
                              mensagem_sinal[21].replace('\n','').replace('[LINK_CADASTRO]', value[1])
            
                bot.delete_message(key, globals()[f'alerta_{key}'].message_id)
                globals()[f'sinal_{key}'] = bot.send_message(key, table_sinal, parse_mode='HTML', disable_web_page_preview=True)
            
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


def coletarDados():
    global gale
    global cash_out
    global estrategia
    global url_jetx
    global response
    global lista_resultados


    while True:

        # Validando data para envio do relatório diário
        validaData()

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass
        
        while True:

            try:
                
                # Pegando o histórico de resultados
                response = requisicao(token_game)

                if '"IsFinnished":true' in response.text:

                    vela_atual = json.loads(response.content)['SocketInfo']['Value']
                    lista_resultados.append(str(vela_atual))
                    
                else:
                    continue

                # Validando se foi solicitado o stop do BOT
                if parar != 0:
                    break
                else:
                    pass
                
                
                ''' VALIDANDO SE TEM DADO VAZIO NA LISTA'''
                if '' in lista_resultados:
                    continue

                
                print(datetime.now().strftime('%H:%M'))
                ''' Chama a função que valida a estratégia para enviar o sinal Telegram '''
                validarEstrategia(lista_resultados, estrategias)   #Lista de estrategia

                print('=' * 150)

                time.sleep(5)

                break

            except:
                continue


def validarEstrategia(lista_resultados, estrategias):
    
    global cash_out
    global gale
    global vela_atual
    global response

    try:
        for estrategia in estrategias:

            # Validando se foi solicitado o stop do BOT
            if parar != 0:
                break
            else:
                pass


            # Validando o horario para envio do relatório diário
            validaData()

            print ('Analisando a Estrategia --> ', estrategia)
            sequencia_minima_alerta = len(estrategia[:-3])
            sequencia_minima_sinal = len(estrategia[:-2])
            cash_out = estrategia[-2]
            gale = estrategia[-1]
            print('Historico_Velas --> ', lista_resultados)

            ''' VALIDADOR DE ESTRATEGIA '''
            validador = validador_estrategia(estrategia, lista_resultados, sequencia_minima_alerta)

            ''' Validando se bateu alguma condição'''
            if validador.count(True) == int(sequencia_minima_alerta):
                print('ENVIANDO ALERTA')
                enviarAlertaTelegram()
                time.sleep(5)


                ''' Verifica se a ultima condição bate com a estratégia para enviar sinal Telegram '''
                while True:
                    
                    try:

                        # Pegando o histórico de resultados
                        response = requisicao(token_game)

                        if '"IsFinnished":true' in response.text:

                            vela_atual = json.loads(response.content)['SocketInfo']['Value']
                            lista_resultados.append(str(vela_atual))
                            
                        else:
                            continue
                    
                        ''' VALIDANDO SE TEM DADO VAZIO NA LISTA'''
                        if '' in lista_resultados:
                            continue

                
                        validador = validador_estrategia(estrategia, lista_resultados, sequencia_minima_sinal)

                        if validador.count(True) == int(sequencia_minima_sinal):
                            print(lista_resultados[-1])
                            print('ENVIA SINAL TELEGRAM')
                            vela_atual = lista_resultados[-1]
                            enviarSinalTelegram(vela_atual)
                            time.sleep(5)
                            checkSinalEnviado(lista_resultados, estrategia)
                            time.sleep(1)
                            break


                        else:
                            print('APAGA SINAL DE ALERTA')
                            apagaAlertaTelegram()
                            break

                    except:
                       continue
            
            else:
                print('=' * 150)


    except:
        pass


def checkSinalEnviado(lista_resultados, estrategia):
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


    contador_cash = 0
    resultados = []
    
    while contador_cash <= int(estrategia[-1]):

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass

        # Validando o horario para envio do relatório diário
        validaData()

        try:

            # Pegando o histórico de resultados
            response = requisicao(token_game)

            if '"IsFinnished":true' in response.text:

                vela_atual = json.loads(response.content)['SocketInfo']['Value']
                lista_resultados.append(str(vela_atual))
                
            else:
                continue
            
        
            print(lista_resultados[-1])
            resultados.append(lista_resultados[-1]+'x')

            if float(lista_resultados[-1]) >= float(estrategia[-2].strip('Xx')):
                
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
                    


                # editando mensagem enviada e enviando sticker
                try:
                    ''' Lendo o arquivo txt canais '''
                    txt = open("canais.txt", "r", encoding="utf-8")
                    arquivo = txt.readlines()
                    canais = arquivo[12].replace('canais= ','').replace('\n','')
                    canais = ast.literal_eval(canais) # Convertendo string em dicionario 
                    
                    ''' Lendo o arquivo txt config-mensagens '''
                    txt = open("config-mensagens.txt", "r", encoding="utf-8")
                    mensagem_green = txt.readlines()

                    #ENVIANDO POST PARA A API
                    payload = {
                            'status': 'success', #alert | confirm | success | failure | denied
                            'chat_id': [key for key,value in canais.items()],
                            'content': mensagem_green[29].replace('\n','').replace('[RESULTADO]', ' | '.join(resultados)),
                            'link_refer':[value[1] for key,value in canais.items()],
                            'link_game_bet':[value[0] for key,value in canais.items()]
                    }

                    requests.post(url, headers=headers, json=payload)

                    for key, value in canais.items():
                        try:
                            bot.reply_to(globals()[f'sinal_{key}'], mensagem_green[29].replace('\n','').replace('[RESULTADO]', ' | '.join(resultados)), parse_mode='HTML')
                        except:
                            pass

                except:
                    pass

                
                print('=' * 100)
                validador_sinal = 0
                contador_cash = 0
                contador_passagem = 0
                return
            
            else:
                print('LOSSS')
                print('=' * 100)
                contador_cash+=1
                time.sleep(5)
                continue
                

        except Exception as a:
            logger.error('Exception ocorrido no ' + repr(a))
            logarSite()
    

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
            ''' Lendo o arquivo txt canais '''
            txt = open("canais.txt", "r", encoding="utf-8")
            arquivo = txt.readlines()
            canais = arquivo[12].replace('canais= ','').replace('\n','')
            canais = ast.literal_eval(canais) # Convertendo string em dicionario 
            
            ''' Lendo o arquivo txt config-mensagens '''
            txt = open("config-mensagens.txt", "r", encoding="utf-8")
            mensagem_green = txt.readlines()

            #ENVIANDO POST PARA A API
            payload = {
                    'status': 'failure', #alert | confirm | success | failure | denied
                    'chat_id': [key for key,value in canais.items()],
                    'content': mensagem_green[31].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(resultados)),
                    'link_refer':[value[1] for key,value in canais.items()],
                    'link_game_bet':[value[0] for key,value in canais.items()]
            }

            requests.post(url, headers=headers, json=payload)

            for key, value in canais.items():
                try:
                    bot.reply_to(globals()[f'sinal_{key}'], mensagem_green[31].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(resultados)), parse_mode = 'HTML')
                except:
                    pass
            
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
    return







inicio()            # Difinição do webBrowser
#logarSite()         # Logando no Site
placar ()           # Chamando o Placar
#processo_pegar_tokenapi()
#coletarDados()


#________________________________________________________________________________________ TELEGRAM__________________________________________________________________________________#

print('\n\n')
print('###################### AGUARDANDO COMANDOS ######################')



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
contador_passagem = 0
botStatus = 0
lista_ids = []


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
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('◀ Voltar')

        message_estrategia = bot.reply_to(message, "🤖 Ok! Escolha um padrão acima ou abaixo de velas, a vela que deverá fazer CASH OUT e uma opção de GALE \n\n Ex: +1,-2,-10.35,1.5X,1", reply_markup=markup)
        bot.register_next_step_handler(message_estrategia, registrarEstrategia)
    
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
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
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

        bot.send_message(message.chat.id, f'🧠 {pe[:-5]} \n==========================\n 🏆= {pe[-5]}  |  🥇= {pe[-4]}  |  🥈= {pe[-3]}  |  🥉= {pe[-2]} \n\n ✅ - {soma_win} \n ❌ - {pe[-1]} \n==========================\n 🎯 {assertividade}  ', reply_markup=markup)
        
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

        #Add to buttons by list with ours generate_buttons function.
        #markup = generate_buttons(['/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','📊 Placar Atual','❌ Pausar Bot'], markup)
        
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message, "🤖 Bot JetX Iniciado! ✅ Escolha uma opção 👇",
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
        global message_canal
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
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖 Ok! Bot Ativado com sucesso! ✅ Em breve receberá sinais nos canais informados no arquivo auxiliar! ",
                                    reply_markup=markup)
            
            botStatus = 1
            reladiarioenviado = 0
            parar=0
            contador_passagem = 0
            stop_loss = []

            print('####################### INICIANDO AS ANÁLISES  #######################')
            print()
            processo_pegar_tokenapi()
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
        if estrategia_excluir == str(pe[:-5]):
            placar_estrategias.remove(pe)


    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    bot.reply_to(message_excluir_estrategia, "🤖 Estratégia excluída com sucesso! ✅", reply_markup=markup)





bot.infinity_polling()






