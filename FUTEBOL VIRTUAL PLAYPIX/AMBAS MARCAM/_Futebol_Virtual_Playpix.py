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



#_______________________________________________________________________#____________________________________________________________________________________________________

print()
print('                                #################################################################')
print('                                ################     BOT FUTEBOL VIRTUAL    #####################')
print('                                #################################################################')
print('                                ##################### SEJA BEM VINDO ############################')
print('                                #################################################################')
print('                                ############# DESENVOLVIDO POR VICTOR RODRIGUES #################')
print('                                #################################################################\n')
print('Versão = 2.0.0')
print('Ambiente: Produção\n\n\n')


        
        

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
        logar_site()
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
        logar_site()
        time.sleep(10)
        horario_inicio = datetime.now()


def inicio():
    global logger
    global browser
    global lista_anterior
    global horario_inicio

    horario_inicio = datetime.now()

    lista_anterior = []
    logger = logging.getLogger()

    # Definindo opções para o browser
    warnings.filterwarnings("ignore", category=DeprecationWarning) 
    chrome_options = webdriver.ChromeOptions() 
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option('useAutomationExtension', False)
    #chrome_options.add_argument("--incognito") #abrir chrome no modo anônimo
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    #chrome_options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    #chrome_options.add_argument("window-size=1037,547")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_argument('disable-extensions')
    chrome_options.add_argument('disable-popup-blocking')
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('log-level=3')

    
    browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)  # Chrome
    #browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())                                     # FireFox        
    #browser  = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install())                       # Brave
    #browser = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(),chrome_options=chrome_options)                     # Chromium


def logar_site():

    #logger = logging.getLogger()
    browser.get(r"https://www.playpix.com/pt/virtual-sports/betconstruct?game=1")
    browser.maximize_window()

    time.sleep(10)
    
    try:
        browser.find_element_by_xpath('//*[@class="btn a-color s-small cookie-message-button "]').click()
    except:
        pass

    time.sleep(2)

    try:
        
        #acessando IFRAME
        acessarIframe()

        #Clicando nos Ultimos Resultados
        browser.find_element_by_xpath('//*[@class="results-button"]').click()
    
    except:pass
    time.sleep(10)


def acessarIframe():
    t=0
    while t < 10:
        try:
            iframe = iframe = browser.find_element_by_xpath('//*[@class="iframe-full-page virtual-sports"]')
            browser.switch_to.frame(iframe)
            break
        
        except:
            time.sleep(5)
            t+=1


def enviar_alerta():
    global contador_passagem

    ''' Lendo o arquivo txt canais '''
    txt = open("canais.txt", "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[12].replace('canais= ','').replace('\n','')
    canais = ast.literal_eval(canais) # Convertendo string em dicionario 

    ''' Lendo o arquivo txt config-mensagens '''
    txt = open("config-mensagens.txt", "r", encoding="utf-8")
    mensagem_alerta = txt.readlines()
    
    # Enviando Mensagem Telegram
    horario_inicial = datetime.now()
    
    try:
        for key, value in canais.items():
            try:
                # Mensagem
                table_alerta = mensagem_alerta[0].replace('\n','') + '\n\n' + \
                                mensagem_alerta[2].replace('\n','') + '\n\n' + \
                                mensagem_alerta[4].replace('\n','') + '\n\n' + \
                                mensagem_alerta[6].replace('\n','') + '\n\n' + \
                                mensagem_alerta[8].replace('\n','').replace('[LINK_CADASTRO]', value[1])
            
                globals()[f'alerta_{key}'] = bot.send_message(key, table_alerta, parse_mode='HTML', disable_web_page_preview=True)

            except:
                print('NÃO CONSEGUI ENVIAR A MENSAGEM PARA O CANAL', key)

    except:
        pass

    print('MENSAGEM ENVIADA PARA TODOS OS CANAIS EM ---> ', datetime.now() - horario_inicial)

    contador_passagem = 1


def enviar_sinal(sinal, gale1, gale2):
    global table_sinal

    ''' Lendo o arquivo txt canais '''
    txt = open("canais.txt", "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[12].replace('canais= ','').replace('\n','')
    canais = ast.literal_eval(canais) # Convertendo string em dicionario 

    ''' Lendo o arquivo txt config-mensagens '''
    txt = open("config-mensagens.txt", "r", encoding="utf-8")
    mensagem_sinal = txt.readlines()

    # Enviando Mensagem Telegram
    horario_inicial = datetime.now()
    
    try:
        for key, value in canais.items():
            try:

                # Mensgaem
                table_sinal = mensagem_sinal[14].replace('\n','') + '\n\n' + \
                            mensagem_sinal[16].replace('\n','').replace('[HORA1]', sinal).replace('[HORA2]', gale1).replace('[HORA3]', gale2) + '\n\n' + \
                            mensagem_sinal[18].replace('\n','') + '\n' + \
                            mensagem_sinal[19].replace('\n','') + '\n' + \
                            mensagem_sinal[20].replace('\n','') + '\n\n' + \
                            mensagem_sinal[22].replace('\n','') + '\n' + \
                            mensagem_sinal[23].replace('\n','') + '\n\n' + \
                            mensagem_sinal[25].replace('\n','') + '\n\n' + \
                            mensagem_sinal[27].replace('\n','').replace('[LINK_JOGO]', value[0])


                bot.delete_message(key, globals()[f'alerta_{key}'].message_id)
            
                globals()[f'sinal_{key}'] = bot.send_message(key, table_sinal, parse_mode='HTML', disable_web_page_preview=True)  #Variavel Dinâmica

                
            except:
                print('NÃO CONSEGUI ENVIAR A MENSAGEM PARA O CANAL', key)
                pass
    
    except:
        pass
    
    print('MENSAGEM ENVIADA PARA TODOS OS CANAIS EM ---> ', datetime.now() - horario_inicial)


def apagar_alerta():
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

                bot.delete_message(key, globals()[f'alerta_{key}'].message_id)
            
            except:
                print('NÃO CONSEGUI APAGAR A MENSAGEM DO CANAL', key)
                pass
    except:
        pass
    
    print('MENSAGEM APAGADA EM TODOS OS CANAIS EM ---> ', datetime.now() - horario_inicial)
    contador_passagem = 0


def validador_estrategia(lista_placares, sequencia_minima):

    # Validando se o resultado se encaixa na estratégia ( TRUE ou FALSE )
    validador = []

    try:

        for placar in lista_placares[:sequencia_minima]:

            if '0' in placar:
                validador.append(True)

            else:
                validador.append(False)

        print(f'Validador  --> {validador}')
        return validador
        
    except:
        pass


def coletar_dados():
    global estrategia

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
                # Auto Refresh
                #auto_refresh()

                # Validando data para envio do relatório diário
                validaData()
                
                # Validando se foi solicitado o stop do BOT
                if parar != 0:
                    break
                else:
                    pass

                
                lista_placares = []
                # Pegando o histórico de resultados
                lista_jogos = browser.find_elements_by_xpath('//*[@class="game-result-items"]')

                ''' Inserindo velas na lista'''
                try:

                    for jogo in lista_jogos[:10]:
                        
                        placar = jogo.text.split('\n')[-1].split('(')[0]

                        lista_placares.append(placar)
                        
                except:
                    print('Erro ao inserir resultados na Lista... Refreshando...')
                    logar_site()
                    continue
                

                ''' VALIDANDO SE A LISTA ESTA VAZIA'''
                if lista_placares == []:
                    logar_site()
                    continue

                
                # Validando se foi solicitado o stop do BOT
                if parar != 0:
                    break
                else:
                    pass
                

                print(datetime.now().strftime('%H:%M'))
                ''' Chama a função que valida a estratégia para enviar o sinal Telegram '''
                validar_estrategia(lista_placares)   #Lista de estrategia

                print('=' * 100)
                lista_placares = []

                #Fechando Janela
                browser.find_element_by_xpath('//*[@class="pop-up-close"]').click()
                #clicando no botão resultados
                browser.find_element_by_xpath('//*[@class="results-button"]').click()

                time.sleep(5)

                break

                ''' Exceção se o jogo não estiver disponível '''
            except:
                print('Algo deu errado na funcao Coletar Dados..Refreshando...')
                logar_site()


def validar_estrategia(lista_placares):
    global estrategia_repeticao

    try:

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            return
        else:
            pass


        #print ('Analisando a Estrategia --> ', estrategia)

        sequencia_minima_alerta = estrategia_repeticao-1
        sequencia_minima_sinal = estrategia_repeticao

        print('Historico de Placares --> ', lista_placares)

        ''' VALIDADOR DE ESTRATEGIA '''
        validador = validador_estrategia(lista_placares, sequencia_minima_alerta)

        ''' Validando se bateu alguma condição'''
        if validador.count(True) == int(sequencia_minima_alerta):
            print('ENVIANDO ALERTA')

            enviar_alerta()
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
                
                lista_placares_validacao = []
                
                try:
                    # Pegando o histórico de resultados
                    lista_jogos = browser.find_elements_by_xpath('//*[@class="game-result-items"]')
                except:
                    logar_site()
                    continue
                
                ''' Inserindo velas na lista'''
                try:

                    for jogo in lista_jogos[:10]:
                        
                        placar = jogo.text.split('\n')[-1].split('(')[0]

                        lista_placares_validacao.append(placar)
                        
                except:
                    print('Erro ao inserir resultados na Lista... Refreshando...')
                    logar_site()
                    continue
                
                print(lista_placares_validacao)

                ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
                if lista_placares != lista_placares_validacao:
                    
                    validador = validador_estrategia(lista_placares_validacao, sequencia_minima_sinal)

                    ''' VALIDA SE ENVIA SINAL OU APAGA O ALERTA '''
                    if validador.count(True) == int(sequencia_minima_sinal):
                        
                        print(lista_placares_validacao[0])
                        
                        print('ENVIA SINAL TELEGRAM')

                        #Formatando Horario
                        text_horario_base = lista_jogos[0].text.split('\n')[0].split(', ')[1]
                        horario_base = datetime.strptime(text_horario_base,'%H:%M')
                        dois_minutos = timedelta(minutes=2)
                        cinco_minutos = timedelta(minutes=5)
                        oito_minutos = timedelta(minutes=8)
                        ###########################################################
                        sinal = (horario_base+dois_minutos).strftime('%H:%M')
                        gale1 = (horario_base+cinco_minutos).strftime('%H:%M')
                        gale2 = (horario_base+oito_minutos).strftime('%H:%M')

                        enviar_sinal(sinal, gale1, gale2)
                        
                        print('=' * 100)
                        
                        checar_sinal_enviado(lista_placares_validacao, sinal, gale1, gale2)
                        
                        time.sleep(2)

                        break


                    else:
                        print('APAGA SINAL DE ALERTA')
                        apagar_alerta()
                        print('=' * 100)
                        time.sleep(2)
                        break
                
                else:
                    #Fechando Janela
                    browser.find_element_by_xpath('//*[@class="pop-up-close"]').click()
                    #clicando no botão resultados
                    browser.find_element_by_xpath('//*[@class="results-button"]').click()

                    time.sleep(5)
                    

        else:
            print('=' * 100)


    except:
        pass


def checar_sinal_enviado(lista_placares_validacao, sinal, gale1, gale2):
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

    while contador_cash <= 2:

        # Validando data para envio do relatório diário
        validaData()

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass


        try:
            lista_placares_sinal = []
                
            # Pegando o histórico de resultados
            lista_jogos = browser.find_elements_by_xpath('//*[@class="game-result-items"]')

            ''' Inserindo velas na lista'''
            try:

                for jogo in lista_jogos[:10]:
                    
                    placar = jogo.text.split('\n')[-1].split('(')[0]

                    lista_placares_sinal.append(placar)
                    
            except:
                print('Erro ao inserir resultados na Lista... Refreshando...')
                logar_site()
                continue
            
            #Correção de Bug
            if lista_placares_sinal[0] == '49:46': 
                
                #Fechando Janela
                browser.find_element_by_xpath('//*[@class="pop-up-close"]').click()
                #clicando no botão resultados
                browser.find_element_by_xpath('//*[@class="results-button"]').click()

                time.sleep(5)

                continue

            ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
            if lista_placares_validacao != lista_placares_sinal:

                print(lista_placares_sinal[0])
                #alimenta_banco_painel(lista_resultados_sinal)

                # VALIDANDO WIN OU LOSS
                if '0' not in lista_placares_sinal[0]:
                    
                    #placar_green = lista_jogos[0].text.split('\n')[2]

                    if contador_cash == 0:
                        
                        resultados.append(sinal)
                        
                        try:
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
                        except:
                            pass

                        

                    if contador_cash == 1:
                        
                        resultados.append(gale1)
                        

                        try:

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
                        
                        except:pass



                    if contador_cash == 2:
                        
                        resultados.append(gale2)
                        
                        try:

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
                        
                        except:pass


                    # respondendo a mensagem do sinal e condição para enviar sticker
                    try:
                        ''' Lendo o arquivo txt canais '''
                        txt = open("canais.txt", "r", encoding="utf-8")
                        arquivo = txt.readlines()
                        canais = arquivo[12].replace('canais= ','').replace('\n','')
                        canais = ast.literal_eval(canais) # Convertendo string em dicionario 
                        
                        
                        ''' Lendo o arquivo txt config-mensagens '''
                        txt = open("config-mensagens.txt", "r", encoding="utf-8")
                        mensagem_green = txt.readlines()
                        
                        # Enviando Mensagem Telegram
                        horario_inicial = datetime.now()

                        for key, value in canais.items():
                            try:
                                
                                bot.reply_to(globals()[f'sinal_{key}'], mensagem_green[32].replace('\n','')+'\n'+\
                                                                        mensagem_green[33].replace('\n','')+'\n'+\
                                                                        mensagem_green[34].replace('[RESULTADO]', ' - '.join(resultados)), parse_mode='HTML')
                                
                            except:
                                pass
                        
                        print('MENSAGEM ENVIADA PARA TODOS OS CANAIS EM ---> ', datetime.now() - horario_inicial)

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
                    lista_placares_validacao = lista_placares_sinal
                    time.sleep(2)
                    continue
            
            else:
                #Fechando Janela
                browser.find_element_by_xpath('//*[@class="pop-up-close"]').click()
                #clicando no botão resultados
                browser.find_element_by_xpath('//*[@class="results-button"]').click()

                time.sleep(5)

        except:
            logar_site()
            continue

    if contador_cash > 2:

        try:
        
            print('LOSSS GALE 2')

            # Preenchendo arquivo txt
            placar_loss +=1
            placar_geral = placar_win + placar_loss
            with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}")
                
            
            print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
        
        except:pass

        # editando mensagem
        try:
            ''' Lendo o arquivo txt canais '''
            txt = open("canais.txt", "r", encoding="utf-8")
            arquivo = txt.readlines()
            canais = arquivo[12].replace('canais= ','').replace('\n','')
            canais = ast.literal_eval(canais) # Convertendo string em dicionario 
            
            ''' Lendo o arquivo txt config-mensagens '''
            txt = open("config-mensagens.txt", "r", encoding="utf-8")
            mensagem_red = txt.readlines()
            
            # Enviando Mensagem Telegram
            horario_inicial = datetime.now()

            for key, value in canais.items():
                try:
                    
                    bot.reply_to(globals()[f'sinal_{key}'], mensagem_red[39], parse_mode='HTML')
                  
                except:
                    pass
            
            print('MENSAGEM ENVIADA PARA TODOS OS CANAIS EM ---> ', datetime.now() - horario_inicial)

            
        except:
            pass

        try:

        # Atualizando placar da estratégia
            for pe in placar_estrategias:
                if pe[:-5] == estrategia:
                    pe[-1] = int(pe[-1])+1

        except:pass
        
        print('=' * 100)
        validador_sinal = 0
        contador_cash = 0
        contador_passagem = 0
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
estrategia_repeticao = None
placar_estrategias = []
contador = 0
botStatus = 0
contador_passagem = 0




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




@bot.message_handler(commands=['⚙ Cadastrar_Repetição'])
def cadastrarEstrategia(message):

    global contador_passagem

    if contador_passagem == 0:
        #Init keyboard markup
        markup_tipo = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
        
        markup_tipo = markup_tipo.add('◀ Voltar')    

        message_repeticao = bot.reply_to(message, "🤖 Ok! Inseria a Quantidade de Repetições que o Bot irá Analisar para Enviar os Sinais 👇", reply_markup=markup_tipo)
        bot.register_next_step_handler(message_repeticao, registrar_repeticao)
    
    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot', '⚙ Cadastrar Repetição', '📝🧠 Editar Repetição', '📊 Placar Atual', '🛑 Pausar Bot')

        bot.reply_to(message, "🤖⛔ Estou validando uma estratégia! Tente novamente em alguns instanstes.", reply_markup=markup)



@bot.message_handler(commands=['📝🧠 Editar_Repetição'])
def editar_estrategia(message):

    global contador_passagem

    try:
    
        message_editar_repeticao = bot.reply_to(message, "🤖 Insira o novo número de Repetições 👇")
        
        bot.register_next_step_handler(message_editar_repeticao, editar_campo_escolhido)
    
    except:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot', '⚙ Cadastrar Repetição', '📝🧠 Editar Repetição', '📊 Placar Atual', '🛑 Pausar Bot')

        message_editar_estrategia = bot.reply_to(message, "🤖 Algo deu Errado. Tente Novamente 🙁.", reply_markup=markup)



@bot.message_handler(commands=['📊 Placar Atual'])
def placar_atual(message):
    global placar
    global resultados_sinais

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup = markup.add('/start','✅ Ativar Bot', '⚙ Cadastrar Repetição', '📝🧠 Editar Repetição', '📊 Placar Atual', '🛑 Pausar Bot')

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



@bot.message_handler(commands=['🛑 Pausar_bot'])
def pausar(message):
    global botStatus
    global contador_passagem

    

    if botStatus == 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot', '⚙ Cadastrar Repetição', '📝🧠 Editar Repetição', '📊 Placar Atual', '🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Bot já está pausado ", reply_markup=markup)

    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot', '⚙ Cadastrar Repetição', '📝🧠 Editar Repetição', '📊 Placar Atual', '🛑 Pausar Bot')

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
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot', '⚙ Cadastrar Repetição', '📝🧠 Editar Repetição', '📊 Placar Atual', '🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message, "🤖 Bot Futebol Virtual Iniciado! ✅ Escolha uma opção 👇",
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


    if message_opcoes.text in ['⚙ Cadastrar Repetição']:
        print('Cadastrar Repetição')

        cadastrarEstrategia(message_opcoes)


    if message_opcoes.text in ['📝🧠 Editar Repetição']:
        print('Editar Repetição')
        editar_estrategia(message_opcoes)


    if message_opcoes.text in ['✅ Ativar Bot']:
        global botStatus
        global message_canal
        global parar

        print('Ativar Bot')

        if botStatus == 1:

            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            markup = markup.add('/start','✅ Ativar Bot', '⚙ Cadastrar Repetição', '📝🧠 Editar Repetição', '📊 Placar Atual', '🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖⛔ Bot já está ativado",
                                reply_markup=markup)

        elif estrategia_repeticao == None:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            markup = markup.add('/start','✅ Ativar Bot', '⚙ Cadastrar Repetição', '📝🧠 Editar Repetição', '📊 Placar Atual', '🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖⛔ Cadastre no mínimo 1 estratégia antes de iniciar",
                                reply_markup=markup)
        
        else:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            markup = markup.add('/start','✅ Ativar Bot', '⚙ Cadastrar Repetição', '📝🧠 Editar Repetição', '📊 Placar Atual', '🛑 Pausar Bot')

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



    if message_opcoes.text in ['🛑 Pausar Bot']:
        print('Pausar Bot')
        pausar(message_opcoes)
    


@bot.message_handler()
def registrar_repeticao(message_repeticao):
    global estrategia_repeticao

    if message_repeticao.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot', '⚙ Cadastrar Repetição', '📝🧠 Editar Repetição', '📊 Placar Atual', '🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_repeticao, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        return


    else: 
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot', '⚙ Cadastrar Repetição', '📝🧠 Editar Repetição', '📊 Placar Atual', '🛑 Pausar Bot')

        estrategia_repeticao = int(message_repeticao.text)

        bot.reply_to(message_repeticao, "🤖 Condição Cadastrada com Sucesso! ✅", reply_markup=markup)



def editar_campo_escolhido(message_editar_estrategia):
    global estrategia_repeticao

    if message_editar_estrategia.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot', '⚙ Cadastrar Repetição', '📝🧠 Editar Repetição', '📊 Placar Atual', '🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_editar_estrategia, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        
        return
    

    else:

        estrategia_repeticao = int(message_editar_estrategia.text)

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot', '⚙ Cadastrar Repetição', '📝🧠 Editar Repetição', '📊 Placar Atual', '🛑 Pausar Bot')

        bot.reply_to(message_editar_estrategia, "🤖 Valor Editado com Sucesso ✅", reply_markup=markup)

        


    

bot.infinity_polling()






