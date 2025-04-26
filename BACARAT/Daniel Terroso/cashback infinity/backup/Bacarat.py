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

    if horario_atual == '11:55' and reladiarioenviado == 0 or horario_atual == '23:55' and reladiarioenviado == 0:
        envia_placar()
        reladiarioenviado +=1

    
    if horario_atual == '11:56' and reladiarioenviado == 1 or horario_atual == '23:56' and reladiarioenviado == 1:
        reladiarioenviado = 0

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
        logar_site()
        time.sleep(10)
        horario_inicio = datetime.now()



def inicio():
    global browser
    global horario_inicio

    horario_inicio = datetime.now()
    
    # Definindo opções para o browser
    warnings.filterwarnings("ignore", category=DeprecationWarning) 
    chrome_options = webdriver.ChromeOptions() 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)



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
        txt = open("arquivos_txt/canais.txt", "r", encoding="utf-8")
        mensagem_login = txt.readlines()
        usuario = mensagem_login[2].replace('\n','').split('= ')[1] 
        senha = mensagem_login[3].replace('\n','').split('= ')[1]

        while True:
            try:

                ''' Mapeando elementos para inserir credenciais '''
                try:
                    browser.find_element_by_xpath('//*[@class="header-right-menu main-header-wrpr--desktop"]//*[text()="Conecte-se"]').click()
                except:pass
                
                time.sleep(2)
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
            if browser.find_elements_by_xpath('//*[@id="header"]/div[1]/div[1]/div/div[2]/div[2]/ul/li[1]'):
                break
            else:
                t3+=1

    except:pass

    ''' Acessando o jogo '''
    
    browser.get('https://estrelabet.com/pb/gameplay/baccarat/real-game')
    
    time.sleep(20)

    browser.get('https://aleaplay.evo-games.com/frontend/evo/r2/#category=baccarat_sicbo&game=baccarat&table_id=oytmvb9m1zysmc44&vt_id=rkg3352umanu65ye&lobby_launch_id=88e103b29fc449448e39ec9b66e6612a')
    
    time.sleep(20)

    # MODO TELA CHEIA
    contador = 0
    while contador<10:
        try:

            tela_cheia = browser.find_element_by_id('gamePlayIframe').get_attribute('src')
            browser.get(tela_cheia)
            time.sleep(10)
            break

        except:
            contador+=1
            time.sleep(3)
            continue

    #acessarIframe()

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



def gerarListaResultados(resultados):
    ''' Convertendo a letra em cor '''
    while True:
        try:
            lista = []
            for resultado in reversed(resultados[:10]):
                lista.append(resultado.text)
                #if resultado.text == 'C':
                #    resultado = '\U0001F534'
                #    lista.append(resultado)
                #    continue
#
                #if resultado.text == 'V':
                #    resultado = '\U0001F535'
                #    lista.append(resultado)
                #    continue
#
                #if resultado.text == 'E':
                #    resultado = '\U0001F7E1'
                #    lista.append(resultado)
                #    continue
          
            return lista
            
        except:
            validarJogoPausado()
            resultados = browser.find_elements_by_css_selector('.historyItem--a1907')
            continue



def validarJogoPausado():
    try:

        terminou_sessao = browser.find_elements_by_xpath('//*[@class="fontRegular css-11g6187 e1qs5c4n16"]')
        for sessao in terminou_sessao:
            if 'Não foi possível conectar ao servidor. Certifique-se de estar conectado à internet e reinicie o jogo'\
            in sessao.text:
                logar_site()


        #sessao_expirada = browser.find_elements_by_css_selector('.titleContainer--fe91d')
        #for sessao in sessao_expirada:
        #    if sessao.text == 'SESSION EXPIRED':
        #        logar_site()


        att_pagina = browser.find_elements_by_xpath('//*[@class="fontRegular css-1dn11ym e9tpw8f2"]')
        for pagina in att_pagina:
            if 'Oops! Something happened. Please close the game and start it again from the lobby'\
                in pagina.text:
                logar_site()

        jogo_pausado = browser.find_elements_by_xpath('//*[@class="css-f3g03p e1qs5c4n20"]')
        for jogo in jogo_pausado:
            if 'Jogo pausado devido à inatividade. Pressione OK para continuar.' in jogo.text:
                browser.find_element_by_xpath('//*[@id="scalable"]/div[10]/div/div[3]/button').click()

        fundos_insu = browser.find_elements_by_xpath('//*[@class="fontRegular css-11g6187 e1qs5c4n16"]')
        for texto in fundos_insu:
            if 'FUNDOS INSUFICIENTES' in texto.text:
                browser.find_element_by_xpath('//*[@id="scalable"]/div[6]/div/div[3]/button[1]').click()


        


    except:
        pass

    try:
        if browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div[6]/div[1]/span').text == 'GAME PAUSED DUE TO INACTIVITY':
            browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div').click()
    
    except:
        try:
            if browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div[10]/div[1]/span').text == 'GAME PAUSED DUE TO INACTIVITY':
                browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div').click()

        except:
            try:
                if browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div[10]/div[1]/span').text == 'GAME PAUSED DUE TO INACTIVITY':
                    browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div').click()
            except:
                try:
                    if browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div[5]/div/div/div/div[1]/div[2]').text == 'Your balance is too low to join this table.':
                        logar_site()
                except:
                    pass        



def coletarDados():

    while True:

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass
        
        # Validando o horario para envio do relatório diário
        validaData()


        # Jogo Pausado
        validarJogoPausado()


        #Auto Refresh
        auto_refresh()


        try:
            ''' Pegando Resultados do Jogo '''
            lista_resultados = browser.find_elements_by_css_selector('.beadroad-container')[0].text.split('\n')
            ''' Lista de resultados Convertidas em cores '''
            #lista_resultados = gerarListaResultados(resultados)
            print(datetime.now())
            print(lista_resultados)

            if lista_resultados == []:
                logar_site()
                continue
            else:
                pass

            validaEstrategias(lista_resultados)

            print('='*100)

        except:
            logar_site()
            continue
            


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

        #print ('Analisando a Estratégia --> ', estrategia)
        #print('Historico da Mesa --> ', lista_resultados[:sequencia_minima_alerta])

        ''' Verifica se os resultados da mesa batem com a estrategia para enviar o alerta '''
        if estrategia[:sequencia_minima_alerta] == lista_resultados[-sequencia_minima_alerta:]:
            print('IDENTIFICADO O PADRÃO DA ESTRATÉGIA --> ', estrategia)
            print('ENVIAR ALERTA')
            enviarAlertaTelegram()
            time.sleep(1)

            ''' Verifica se a ultima condição bate com a estratégia para enviar sinal Telegram '''
            while True:
                # Jogo Pausado
                validarJogoPausado()
                
                try:
                    ''' Lendo novos resultados para validação da estratégia'''
                    if browser.find_elements_by_css_selector('.beadroad-container'):
                        lista_resultados_validacao = browser.find_elements_by_css_selector('.beadroad-container')[0].text.split('\n')
                    
                    ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
                    if lista_resultados != lista_resultados_validacao:
                        ''' Verificando se o ultimo resultado da mesa está dentro da estratégia'''
                        if estrategia[:sequencia_minima_sinal] == lista_resultados_validacao[-sequencia_minima_sinal:]:
                            print('PADRÃO DA ESTRATÉGIA ', estrategia, ' CONFIRMADO!')
                            print('ENVIANDO SINAL TELEGRAM')
                            enviarSinalTelegram()
                            time.sleep(1)
                            checkSinalEnviado(lista_resultados_validacao)
                            break
                            
                        else:
                            print('APAGA SINAL DE ALERTA')
                            apagaAlertaTelegram()
                            break
                        
                except:
                    logar_site()



def enviarAlertaTelegram():
    global contador_passagem

    ''' Lendo o arquivo txt canais '''
    txt = open(r"arquivos_txt\canais.txt", "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[12].replace('canais= ','').replace('\n','')
    canais = ast.literal_eval(canais) # Convertendo string em dicionario 

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
                                                                    .replace('[COR]', '🟥' if estrategia[-1] == 'B' else '🟦' if estrategia[-1] == 'J' else '🟩' )
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
    global lista_resultados_sinal
    global table
    global contador_cash
    global placar_maior
    global inicio_alternado

    resultado_valida_sinal = []
    contador_cash = 0
    resultado_estrategia = estrategia[-1]

    if resultado_estrategia == 'alternadoB':
        inicio_alternado = 'B'
    elif resultado_estrategia == 'alternadoP':
        inicio_alternado = 'P'


    while True:

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass

        # Validando o horario para envio do relatório diário
        validaData()

        # Jogo Pausado
        validarJogoPausado()

        try:
           
            if browser.find_elements_by_css_selector('.beadroad-container'):
                lista_resultados_sinal = browser.find_elements_by_css_selector('.beadroad-container')[0].text.split('\n')
                    
            ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
            if lista_resultados_validacao != lista_resultados_sinal:
    
                print(lista_resultados_sinal[-1])

                if lista_resultados_sinal[-1] == 'J':
                    resultado_valida_sinal.append('🟦')

                if lista_resultados_sinal[-1] == 'B':
                    resultado_valida_sinal.append('🟥')
                
                if lista_resultados_sinal[-1] == 'E':
                    resultado_valida_sinal.append('🟩')

                #resultado_valida_sinal.append(lista_resultados_sinal[-1])
                    
                
                # VALIDANDO WIN OU LOSS
                if lista_resultados_sinal[-1] == resultado_estrategia or lista_resultados_sinal[-1] == 'E':
                    
                    print('GREEN')
                    print('==================================================')
                    contador_cash+=1
                    lista_resultados_validacao = lista_resultados_sinal

                    ### FUNÇÃO PARA ESTRATEGIA ALTERNADA
    
                    inicio_alternado = estrategia_alterada(inicio_alternado)

                    continue

            
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
                                if pe[:-5] == estrategia:
                                    pe[-5] = int(pe[-5])+1
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
                                if pe[:-5] == estrategia:
                                    pe[-4] = int(pe[-4])+1

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
                                    if pe[:-5] == estrategia:
                                        pe[-3] = int(pe[-3])+1
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
                                if pe[:-5] == estrategia:
                                    pe[-4] = int(pe[-4])+1

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
                                if pe[:-5] == estrategia:
                                    pe[-4] = int(pe[-4])+1

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
                                if pe[:-5] == estrategia:
                                    pe[-4] = int(pe[-4])+1

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
                                if pe[:-5] == estrategia:
                                    pe[-4] = int(pe[-4])+1

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
                                if pe[:-5] == estrategia:
                                    pe[-4] = int(pe[-4])+1

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
                                if pe[:-5] == estrategia:
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
                                if pe[:-5] == estrategia:
                                    pe[-4] = int(pe[-4])+1

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
                                if pe[:-5] == estrategia:
                                    pe[-4] = int(pe[-4])+1

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
                                if pe[:-5] == estrategia:
                                    pe[-5] = int(pe[-5])+1
                        except:
                            pass
                        

                    # editando mensagem enviada
                    try:
                        ''' Lendo o arquivo txt canais '''
                        txt = open(r"arquivos_txt\canais.txt", "r", encoding="utf-8")
                        arquivo = txt.readlines()
                        canais = arquivo[12].replace('canais= ','').replace('\n','')
                        canais = ast.literal_eval(canais) # Convertendo string em dicionario 
                       
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
                    lista_resultados = lista_resultados_sinal


                    return
                

        except:
            continue




def estrategia_alterada(inicio_alternado):

    try:

        if inicio_alternado == 'B':
            inicio_alternado = 'P'
        
        elif inicio_alternado == 'P':
            inicio_alternado = 'B'


        return inicio_alternado
        
    
    except Exception as e:
        print(e)




inicio()
logar_site()
placar()




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

    if contador_passagem != 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_excluir_estrategia = bot.reply_to(message, "🤖⛔ Estou validando uma estratégia! Tente novamente em alguns instanstes.", reply_markup=markup)

    elif botStatus == 0:
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


        estrategias_padroes = ( ['B','B','B','B','B'],
                                ['J','J','J','J','J'],
                                ['B','B','J','J','B','B'], 
                                ['J','J','B','B','J','J'],
                                ['J','J','J','alternadoB'],
                                ['B','B','B','alternadoP'],
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

        message_estrategia = bot.reply_to(message_tipo_estrategia, "🤖 Ok! Informe a sequencia de LETRAS (B,J,E) que o bot terá que identificar. *** A última LETRA será a da aposta ***  \n\n Ex: VVVVVVC  / CCCCCV", reply_markup=markup)
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





bot.infinity_polling()



