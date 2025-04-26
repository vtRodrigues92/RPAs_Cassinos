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



def validarJogoPausado():
    try:

        terminou_sessao = browser.find_elements_by_css_selector('.contentElement--e8ecb')
        for sessao in terminou_sessao:
            if sessao.text == 'Terminou a sessão. Feche esta janela e inicie sessão novamente para jogar.' \
            or sessao.text == 'Você foi desconectado. Feche esta janela e conecte novamente para jogar.' \
            or sessao.text == 'Esta tabela está temporariamente inativa. Volte mais tarde ou selecione uma tabela diferente.':
                logarSite()


        sessao_expirada = browser.find_elements_by_css_selector('.titleContainer--fe91d')
        for sessao in sessao_expirada:
            if sessao.text == 'SESSÃO EXPIRADA' or sessao.text == 'Ocorreu um problema. Tente novamente mais tarde ou escolha uma mesa diferente.':
                logarSite()


        att_pagina = browser.find_elements_by_css_selector('.content--c7c5e')
        for pagina in att_pagina:
            if pagina.text == 'Recarregue a página para voltar ao jogo neste dispositivo' \
            or sessao.text == 'Você foi desconectado. Feche esta janela e conecte novamente para jogar.' \
            or sessao.text == 'Esta tabela está temporariamente inativa. Volte mais tarde ou selecione uma tabela diferente.':
                logarSite()

        jogo_pausado = browser.find_elements_by_xpath('//*[@class="label--75060"]')
        for jogo in jogo_pausado:
            if jogo.text == 'JOGO PAUSADO POR INATIVIDADE':
                browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div').click()


    except:
        pass

    try:
        if browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div[6]/div[1]/span').text == 'JOGO PAUSADO POR INATIVIDADE':
            browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div').click()
    
    except:
        try:
            if browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div[10]/div[1]/span').text == 'JOGO PAUSADO POR INATIVIDADE':
                browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div').click()

        except:
            try:
                if browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div[10]/div[1]/span').text == 'JOGO PAUSADO POR INATIVIDADE':
                    browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div').click()
            except:
                try:
                    if browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div[5]/div/div/div/div[1]/div[2]').text == 'Your balance is too low to join this table.':
                        logarSite()
                except:
                    pass        


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
    global placar_empate

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
                placar_empate = int(arq_placar[4].split(',')[1])
                placar_loss = int(arq_placar[5].split(',')[1])
                placar_geral = int(placar_win) + int(placar_loss)
                asserividade = arq_placar[6].split(',')[1]+"%"
            
            except:
                pass

            
    else:
        # Criar um arquivo com a data atual
        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
            arquivo.write("win,0\nsg,0\ng1,0\ng2,0\nemp,0\nloss,0\nass,0")

        # Ler o arquivo de placar criado
        with open(f"placar/{data_hoje}.txt", 'r') as arquivo:
            try:

                arq_placar = arquivo.readlines()
                placar_win = int(arq_placar[0].split(',')[1])
                placar_semGale = int(arq_placar[1].split(',')[1])
                placar_gale1 = int(arq_placar[2].split(',')[1])
                placar_gale2 = int(arq_placar[3].split(',')[1])
                placar_empate = int(arq_placar[4].split(',')[1])
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
        😥 WIN EMPATE - "+str(placar_empate)+"\n\
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
    global url
    global headers

    url = "https://app.bootbost.com.br/api/v1/call"
    headers = {
    'Content-Type': 'application/json'
    }

    horario_inicio = datetime.now()
    lista_resultados = []

    horario_inicio = datetime.now()
    
    # Definindo opções para o browser
    warnings.filterwarnings("ignore", category=DeprecationWarning) 
    chrome_options = webdriver.ChromeOptions() 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)


def logarSite():
    #browser.get(r"https://pi.njoybingo.com/game.do?token=7d10f64b-e3db-4fb8-a8f7-330ff4d0d407&pn=meskbet&lang=pt&game=EVOLUTION-topcard-nvrpqglt6teqkvaf&type=CHARGED")  #PRODUÇÃO
    #browser.get(r"https://pi.njoybingo.com/game.do?token=18298495-0dce-4997-944e-f52c78717619&pn=meskbet&lang=pt&game=EVOLUTION-topcard-nvrpqglt6teqkvaf&type=CHARGED")  #DEV
    #browser.maximize_window()
    #time.sleep(10)

    while True:

        try:
            browser.get(r"https://b2xbet.com/MultiGame/191098/LIVE_CASINO/false/56/null")
            
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
                browser.find_element_by_xpath('//*[@class="login-input ng-untouched ng-pristine ng-invalid"]').send_keys(usuario) #Inserindo login
                browser.find_element_by_xpath('//*[@class="login-input ng-untouched ng-pristine ng-invalid"]').send_keys(senha) #Inserindo senha
                browser.find_element_by_xpath('//*[@class="login-input-submit"]').click() #Clicando no btn login
                
                time.sleep(3)

                browser.refresh()

                time.sleep(10)
                ''' Verificando se o login foi feito com sucesso'''
                t3 = 0
                while t3 < 20:
                    if browser.find_elements_by_xpath('//*[@class="btn btn-sm btn-deposit-header ng-star-inserted"]'):
                        break
                    else:
                        t3+=1
            except:
                pass
            
            ''' Entrando no ambiente '''
            browser.get(browser.find_element_by_xpath('//*[@class="resp-iframe resp-iframe0 casino ng-star-inserted"]').get_attribute('src'))
                                
            time.sleep(15)
                    
            break
        
        except:
            continue
        

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
            resultados = browser.find_elements_by_css_selector('.historyItem--a1907')
            ''' Lista de resultados Convertidas em cores '''
            lista_resultados = gerarListaResultados(resultados)
            print(lista_resultados)

            if lista_resultados == []:
                logarSite()
                continue
            else:
                pass

            validaEstrategias(lista_resultados)

        except:
            logarSite()
            continue


def validaEstrategias(lista_resultados):
    global estrategias
    global estrategia
    global aposta
    
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
            enviar_alerta_telegram()
            time.sleep(1)

            ''' Verifica se a ultima condição bate com a estratégia para enviar sinal Telegram '''
            while True:

                # Jogo Pausado
                validarJogoPausado()
                
                try:
                    ''' Lendo novos resultados para validação da estratégia'''
                    if browser.find_elements_by_css_selector('.historyItem--a1907'):
                        resultados = browser.find_elements_by_css_selector('.historyItem--a1907')

                    ''' Função que converte as letras em cores '''
                    lista_resultados_validacao = gerarListaResultados(resultados)

                    ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
                    if lista_resultados != lista_resultados_validacao:
                        ''' Verificando se o ultimo resultado da mesa está dentro da estratégia'''
                        if estrategia[:sequencia_minima_sinal] == lista_resultados_validacao[-sequencia_minima_sinal:]:
                            print('PADRÃO DA ESTRATÉGIA ', estrategia, ' CONFIRMADO!')
                            
                            #DEFININDO QUAL COR ENTRAR
                            if estrategia[-1] == 'V':
                                aposta = browser.find_element_by_xpath('//*[@class="mainBet--3538e tiger--77988 isTabletDesktop--b0f82 isTopCard--b9357 isDesktop--b14c3 isSolidTieMode--09bc6 withStats--f8164"]')
                                
                            if estrategia[-1] == 'C':
                                aposta = browser.find_element_by_xpath('//*[@class="mainBet--3538e dragon--6af9d isTabletDesktop--b0f82 isTopCard--b9357 isDesktop--b14c3 isSolidTieMode--09bc6 withStats--f8164"]')
                            

                            print('INSERINDO APOSTA')
                            time.sleep(5)
                            apostar(valor_entrada, protecao, aposta)
                            enviar_sinal_telegram()
                            time.sleep(1)
                            checkSinalEnviado(lista_resultados_validacao)
                            break
                            
                        else:
                            print('APAGA SINAL DE ALERTA')
                            apaga_alerta_telegram()
                            break
                        
                except:
                    print('APAGA SINAL DE ALERTA')
                    apaga_alerta_telegram()
                    break
                        

def enviar_alerta_telegram():
    global contador_passagem
    global mensagem_telegram_alerta

    ''' Lendo o arquivo txt config-mensagens '''
    txt = open("config-mensagens.txt", "r", encoding="utf-8")
    mensagem_alerta = txt.readlines()

    ''' Enviando mensagem Telegram '''
    try:
        
        table_alerta = mensagem_alerta[0].replace('\n','')
        
        mensagem_telegram_alerta = bot.send_message(id_usuario, table_alerta)

    except:
        pass
    
    contador_passagem = 1


def enviar_sinal_telegram():
    global table_sinal
    
    ''' Lendo o arquivo txt config-mensagens '''
    txt = open("config-mensagens.txt", "r", encoding="utf-8")
    arquivo_mensagem = txt.readlines()
    mensagem_sinal = arquivo_mensagem[1].split(',')

    ''' Estruturando mensagem '''
    txt = open("config-mensagens.txt", "r", encoding="utf-8")
    mensagem_sinal = txt.readlines()

    try:
        if int(protecao) != 0:
            ''' Mensagem '''
            table_sinal = mensagem_sinal[9].replace('\n','') + '\n' +\
                          mensagem_sinal[10].replace('\n','').replace('[VALOR_APOSTA]', 'R$'+str(valor_entrada)).replace('[COR]','🟥' if estrategia[-1] == 'C' else '🟦' if estrategia[-1] == 'V' else '🟨') + '\n' +\
                          mensagem_sinal[11].replace('\n','').replace('[VALOR_PROTEÇÃO]','R$'+str(protecao))
        
        else:
            table_sinal = mensagem_sinal[9].replace('\n','') + '\n' +\
                          mensagem_sinal[10].replace('\n','').replace('[VALOR_APOSTA]', 'R$'+str(valor_entrada)).replace('[COR]','VERMELHO' if estrategia[-1] == 'C' else 'AZUL' if estrategia[-1] == 'V' else 'AMARELO')


        bot.delete_message(id_usuario, mensagem_telegram_alerta.message_id)
        bot.send_message(id_usuario, table_sinal)
    
    except:
        pass
    

def apaga_alerta_telegram():
    global contador_passagem

    try:    
        
        bot.delete_message(id_usuario, mensagem_telegram_alerta.message_id)
        
    except:
        pass
    
    contador_passagem = 0


def checkSinalEnviado(lista_resultados_validacao):
    global placar_win
    global placar_semGale
    global placar_gale1
    global placar_gale2
    global placar_gale3
    global placar_loss
    global placar_empate
    global resultados_sinais
    global ultimo_horario_resultado
    global validador_sinal
    global estrategia
    global contador_passagem
    global lista_resultados_sinal

    resultado_valida_sinal = []
    contador_cash = 0


    while contador_cash <= martingale:

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
           
            if browser.find_elements_by_css_selector('.historyItem--a1907'):
                resultados = browser.find_elements_by_css_selector('.historyItem--a1907')
                ''' Função que converte as letras em cores '''
                lista_resultados_sinal = gerarListaResultados(resultados)

            ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
            if lista_resultados_validacao != lista_resultados_sinal:
    
                print(lista_resultados_sinal[-1])

                if lista_resultados_sinal[-1] == 'V':
                    resultado_valida_sinal.append('🟦')

                if lista_resultados_sinal[-1] == 'C':
                    resultado_valida_sinal.append('🟥')
                
                if lista_resultados_sinal[-1] == 'E':
                    resultado_valida_sinal.append('🟨')

                #resultado_valida_sinal.append(lista_resultados_sinal[-1])

                # VALIDANDO WIN OU LOSS
                if lista_resultados_sinal[-1] == estrategia[-1] or lista_resultados_sinal[-1] == 'E' and protecao != 0:
                
                    # validando o tipo de WIN
                    if contador_cash == 0:
                        print('WIN SEM GALE')
                        

                        # Atualizando placar e Alimentando o arquivo txt
                        placar_win +=1
                        placar_semGale +=1
                        placar_geral = placar_win + placar_loss

                        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                            arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nemp,{placar_empate}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}")

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

                        # Atualizando placar e Alimentando o arquivo txt
                        placar_win +=1
                        placar_gale1 +=1
                        placar_geral = placar_win + placar_loss
                        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                            arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nemp,{placar_empate}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}")
 
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
                        
                        # Atualizando placar e Alimentando o arquivo txt
                        placar_win +=1
                        placar_gale2 +=1
                        placar_geral = placar_win + placar_loss
                        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                            arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nemp,{placar_empate}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}")

                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
                        
                        try:
                            # Somando Win na estratégia da lista atual
                            for pe in placar_estrategias:
                                    if pe[:-5] == estrategia:
                                        pe[-3] = int(pe[-3])+1
                        except:
                            pass
                        
                    #REGISTRANDO EMPATE
                    if lista_resultados_sinal[-1] == 'E':
                        
                        # Atualizando placar e Alimentando o arquivo txt
                        placar_empate +=1

                        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                            arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nemp,{placar_empate}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}")



                    # editando mensagem enviada
                    try:
                        ''' Lendo o arquivo txt config-mensagens '''
                        txt = open("config-mensagens.txt", "r", encoding="utf-8")
                        mensagem_green = txt.readlines()
                        
                        try:
                            #Envia Green Telegram
                            bot.send_message(id_usuario, mensagem_green[22].replace('\n','').replace('[RESULTADO]', ' | '.join(resultado_valida_sinal)), parse_mode='HTML')
                            time.sleep(1)
                            # Validando o STOP WIN
                            validar_stop_win()


                        except:
                            pass
                        

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
                    lista_resultados_validacao = lista_resultados_sinal
                    contador_cash+=1

                    if contador_cash <= martingale:

                        time.sleep(5)
                        valor_gale = valor_entrada * fator_gale * contador_cash
                        executar_martingale(valor_gale, aposta, contador_cash)

                        

                    continue
            
            else:
                continue

        except Exception as e:
            print(e)
            continue


    if contador_cash > martingale :
        print('LOSSS GALE2')
        
        # Preenchendo arquivo txt
        placar_loss +=1
        placar_geral = placar_win + placar_loss
        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
            arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}")
            
        
        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
        

        # editando mensagem
        try:

            ''' Lendo o arquivo txt config-mensagens '''
            txt = open("config-mensagens.txt", "r", encoding="utf-8")
            mensagem_red = txt.readlines()
           
            try:
                
                bot.send_message(id_usuario, mensagem_red[24].replace('\n','').replace('[RESULTADO]', ' | '.join(resultado_valida_sinal)), parse_mode='HTML')
            
            except:
                pass
            

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

        validar_stop_loss()
        print("="*100)
        validador_sinal = 0
        contador_cash = 0
        contador_passagem = 0
        return


def apostar(valor_aposta, protecao, aposta):

    if valor_entrada >= 10:
        #CLICANDO NA MOEDA 10
        try:
            browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div[6]/div/div[5]/div/div[2]/div/div[3]/div[2]').click()                    
        except:
            pass

        moeda = 10

    else:
        #CLICANDO NA MOEDA 2.5
        try:
            browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div[6]/div/div[5]/div/div[2]/div/div[1]/div[2]').click()
        except:
            pass

        moeda = 2.50

    #FAZENDO APOSTA
    click = 1
    qnt_clicks = int((valor_aposta//moeda))


    try:

        while click <= qnt_clicks:

            #Clicando Onde Apostar
            aposta.click()
            time.sleep(0.5)

            click+=1


        if int(protecao) != 0:
            #FAZENDO PROTEÇÃO
            click_protecao = 1
            qntd_clicks_protecao = int((protecao//2.50))
            #CLICANDO NA MOEDA 2.5
            try:
                browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div[6]/div/div[5]/div/div[2]/div/div[1]/div[2]').click()
            except:
                pass

            while click_protecao <= qntd_clicks_protecao:

                # Clicando na Proteção
                browser.find_element_by_xpath('//*[@class="svg--55b97 betspot--6c7ce"]').click()

                click_protecao+=1


    except:pass
           

def executar_martingale(valor_gale, aposta, contador_cash):

    if valor_entrada >= 10:
        #CLICANDO NA MOEDA 10
        try:
            browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div[6]/div/div[5]/div/div[2]/div/div[3]/div[2]').click()                    
        except:
            pass
       
        moeda = 10

    else:
        #CLICANDO NA MOEDA 2.5
        try:
            browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div[6]/div/div[5]/div/div[2]/div/div[1]/div[2]').click()
        except:
            pass

        moeda = 2.50
        
    #FAZENDO APOSTA
    click_gale = 1
    qnt_clicks_gale = int((valor_gale//moeda))


    while True:

        try:

            while click_gale <= qnt_clicks_gale:

                #Clicando Onde Apostar
                aposta.click()
                time.sleep(0.5)

                click_gale+=1


            if martingale_empate == 'SIM':

                #FAZENDO PROTEÇÃO
                click_protecao_gale = 1
                valor_gale_empate = protecao * fator_gale_empate
                qntd_clicks_protecao = int((valor_gale_empate//2.50))
                #CLICANDO NA MOEDA 2.5
                try:
                    browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div[6]/div/div[5]/div/div[2]/div/div[1]/div[2]').click()
                except:
                    pass

                while click_protecao_gale <= qntd_clicks_protecao:

                    # Clicando na Proteção
                    browser.find_element_by_xpath('//*[@class="svg--55b97 betspot--6c7ce"]').click()

                    click_protecao_gale+=1

            
            bot.send_message(id_usuario, f"🤞 Tentando a Recuperação de R${valor_gale} NO GALE "+str(contador_cash) + '\n' + \
                                         f' E Cobrindo com R${valor_gale_empate} no 🟨' if martingale_empate == 'SIM'\
                                         else\
                                         f"🤞 Tentando a Recuperação de {valor_gale} NO GALE "+str(contador_cash)
                                         )

        except:
            continue
            
        break


def validar_stop_win():

    time.sleep(3)

    saldo_atualizado = enviar_saldo() 

    if (float(saldo_atualizado.split(' ')[1].replace(',','.')) - float(saldo_inicial.split(' ')[1].replace(',','.'))) >= stop_gain:

        bot.send_message(id_usuario, "✅💰💵 MARAVILHA! STOP WIN ATINGIDO!!! PAUSANDO AS OPERAÇÕES....")

        pausarBot()


def validar_stop_loss():

    time.sleep(3)

    saldo_atualizado = enviar_saldo() 

    if (float(saldo_inicial.split(' ')[1].replace(',','.')) - float(saldo_atualizado.split(' ')[1].replace(',','.'))) >= stop_loss:

        bot.send_message(id_usuario, "❌ EITA!! STOP LOSS ATINGIDO!! PAUSANDO AS OPERAÇÕES....")

        pausarBot()


inicio()
logarSite()
placar()



#________________________________________________________________________________________ TELEGRAM__________________________________________________________________________________#


print('############################################ AGUARDANDO COMANDOS ############################################')

global canal


valor_entrada = ''
stop_gain = ''
stop_loss = ''
protecao = ''
martingale = ''
fator_gale = ''
martingale_empate = ''
fator_gale_empate = ''
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
bot = telebot.TeleBot(CHAVE_API)



########################################################################################


global message


def generate_buttons_estrategias(bts_names, markup):
    for button in bts_names:
        markup.add(types.KeyboardButton(button))
    return markup



@bot.message_handler(commands=['💵 Saldo Atual'])
def enviar_saldo_atual(message):
    
    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=3)
    markup = markup.add('/start','✅ Ativar Bot','⚙💰 Configurações de Entrada', '💵 Saldo Atual', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot','◀ Voltar')

    while True:
        try:

            saldo_atual = browser.find_element_by_xpath('//*[@class="amount--bb99f"]').text
            message_final = bot.reply_to(message, f"💰 SALDO ATUAL :{saldo_atual}", reply_markup=markup)
            break
            
        except:
            message_final = bot.reply_to(message, "Ocorreu um Erro ao Pegar o Saldo. Fazendo uma Nova Tentativa....", reply_markup=markup )
            logarSite()

        

@bot.message_handler(commands=['⚙ Cadastrar_Estratégia'])
def cadastrarEstrategia(message):

    global contador_passagem

    if contador_passagem == 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
         
        markup = markup.add('◀ Voltar')

        message_estrategia = bot.reply_to(message, "🤖 Ok! Informe a sequencia de LETRAS (V,C,E) que o bot terá que identificar. *** A última LETRA será a da aposta ***  \n\n Ex: VVVVVVC  / CCCCCV", reply_markup=markup)
        bot.register_next_step_handler(message_estrategia, registrarEstrategia)
    

    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=3)
        markup = markup.add('/start','✅ Ativar Bot','⚙💰 Configurações de Entrada', '💵 Saldo Atual', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot','◀ Voltar')

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
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=3)
        markup = markup.add('/start','✅ Ativar Bot','⚙💰 Configurações de Entrada', '💵 Saldo Atual', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot','◀ Voltar')

        message_excluir_estrategia = bot.reply_to(message, "🤖⛔ Estou validando uma estratégia! Tente novamente em alguns instanstes.", reply_markup=markup)


@bot.message_handler(commands=['📜 Estrategias_Cadastradas'])
def estrategiasCadastradas(message):
    global estrategia
    global estrategias

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=3)
    markup = markup.add('/start','✅ Ativar Bot','⚙💰 Configurações de Entrada', '💵 Saldo Atual', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot','◀ Voltar')

    mensagem = bot.reply_to(message, "🤖 Ok! Listando estratégias", reply_markup=markup)


    for estrategia in estrategias:
        #print(estrategia)
        bot.send_message(message.chat.id, ''.join(estrategia))


@bot.message_handler(commands=['📊 Placar Atual'])
def placar_atual(message):
    global resultados_sinais

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=3)
    markup = markup.add('/start','✅ Ativar Bot','⚙💰 Configurações de Entrada', '💵 Saldo Atual', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot','◀ Voltar')

    try:
        placar()

        resposta = bot.reply_to(message,\
        "📊 Placar Atual do dia "+data_hoje+":\n\
        =====================\n\
        😍 WIN - "+str(placar_win)+"\n\
        🏆 WIN S/ GALE - "+str(placar_semGale)+"\n\
        🥇 WIN GALE1 - "+str(placar_gale1)+"\n\
        🥈 WIN GALE2 - "+str(placar_gale2)+"\n\
        😥 WIN EMPATE - "+str(placar_empate)+"\n\
        😭 LOSS - "+str(placar_loss)+"\n\
        =====================\n\
        🎯 Assertividade "+ asserividade,\
         reply_markup=markup)
        
        
    except Exception as a:
        logger.error('Exception ocorrido no ' + repr(a))
        #placar = bot.reply_to(message,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%", reply_markup=markup)
        pass


@bot.message_handler(commands=['📈 Gestão'])
def gestao(message):
    global placar
    global resultados_sinais
    global placar_estrategias

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=3)
    markup = markup.add('/start','✅ Ativar Bot','⚙💰 Configurações de Entrada', '💵 Saldo Atual', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot','◀ Voltar')

    mensagem = bot.reply_to(message, "🤖 Ok! Listando Mostrando o Placar por Estratégia", reply_markup=markup)
    
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
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=3)
        markup = markup.add('/start','✅ Ativar Bot','⚙💰 Configurações de Entrada', '💵 Saldo Atual', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot','◀ Voltar')

        message_excluir_estrategia = bot.reply_to(message, "🤖⛔ Estou validando uma estratégia! Tente novamente em alguns instanstes.", reply_markup=markup)

        bot.register_next_step_handler(message_excluir_estrategia, opcoes_painel_princial)


    elif botStatus == 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=3)
        markup = markup.add('/start','✅ Ativar Bot','⚙💰 Configurações de Entrada', '💵 Saldo Atual', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot','◀ Voltar')

        message_final = bot.reply_to(message, "🤖⛔ Bot já está pausado ", reply_markup=markup)

        bot.register_next_step_handler(message_final, opcoes_painel_princial)

    else:   
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙💰 Configurações de Entrada', '💵 Saldo Atual', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot','◀ Voltar')

        print('\n\n')
        print('Comando: Parar BOT')
        print('Parando o BOT....\n')
        botStatus = 0
        parar += 1
        #pausarBot()

        print('###################### AGUARDANDO COMANDOS ######################')

        message_final = bot.reply_to(message, "🤖 Ok! Bot pausado 🛑", reply_markup=markup)

        #bot.register_next_step_handler(message_final, opcoes_painel_princial)


@bot.message_handler(commands=['start'])
def start(message):

    global id_usuario

    if str(message.chat.id) in ids:

        id_usuario = message.chat.id

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=3)
        markup = markup.add('/start','✅ Ativar Bot','⚙💰 Configurações de Entrada', '💵 Saldo Atual', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot','◀ Voltar')

        #arkup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        escolha_inicial = bot.reply_to(message, "🤖 Bot Football Studio Iniciado! ✅ Escolha uma opção 👇",
                                reply_markup=markup)
        
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(escolha_inicial, opcoes_painel_princial)
    
    else:
        message_error = bot.reply_to(message, "🤖 Você não tem permissão para acessar este Bot ❌🚫")


@bot.message_handler()
def opcoes_painel_princial(escolha_painel_princial):


    
    if escolha_painel_princial.text in ['⚙💰 Configurações de Entrada']:

        if str(escolha_painel_princial.chat.id) in ids:

            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            markup = markup.add(
                                f'Valor Entrada = {valor_entrada}',
                                f'Stop Gain = {stop_gain}',
                                f'Stop Loss = {stop_loss}',
                                f'Proteção = {protecao}',
                                f'Martingale = {martingale}',
                                f'Fator Gale = {fator_gale}',
                                f'Martingale Empate = {martingale_empate}',
                                f'Fator Gale Empate = {fator_gale_empate}',
                                '◀ Voltar')

            escolha_config_entrada = bot.reply_to(escolha_painel_princial, "🤖 Perfeito! Escolha uma opção 👇",
                                    reply_markup=markup)
            
            #Here we assign the next handler function and pass in our response from the user. 
            bot.register_next_step_handler(escolha_config_entrada, opcoes_config_entrada)
        
        else:
            message_error = bot.reply_to(escolha_painel_princial, "🤖 Você não tem permissão para acessar este Bot ❌🚫")


    if escolha_painel_princial.text in ['💵 Saldo Atual']:
        print('Enviar Saldo')
        enviar_saldo_atual(escolha_painel_princial)


    if escolha_painel_princial.text in ['⚙ Cadastrar Estratégia']:
        print('Cadastrar Estrategia')

        cadastrarEstrategia(escolha_painel_princial)


    if escolha_painel_princial.text in['📜 Estratégias Cadastradas']:
        print('Estrategias Cadastradas')
        estrategiasCadastradas(escolha_painel_princial)


    if escolha_painel_princial.text in ['🗑 Apagar Estratégia']:
        print('Apagar estrategia')
        apagarEstrategia(escolha_painel_princial)


    if escolha_painel_princial.text in ['✅ Ativar Bot']:
        global botStatus
        global estrategia
        global botStatus
        global reladiarioenviado
        global parar, saldo_inicial

        print('Ativar Bot')

        if botStatus == 1:

            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','✅ Ativar Bot','💵 Saldo Atual', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot','◀ Voltar')

            message_canal = bot.reply_to(escolha_painel_princial, "🤖⛔ Bot já está ativado",
                                reply_markup=markup)

            #bot.register_next_step_handler(message_canal, opcoes_painel_princial)

        elif estrategias == []:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','✅ Ativar Bot','💵 Saldo Atual', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot','◀ Voltar')

            message_canal = bot.reply_to(escolha_painel_princial, "🤖⛔ Cadastre no mínimo 1 estratégia antes de iniciar",
                                reply_markup=markup)
            
            #bot.register_next_step_handler(message_canal, opcoes_painel_princial)
        
        else:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','✅ Ativar Bot','💵 Saldo Atual', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot','◀ Voltar')

            message_final = bot.reply_to(escolha_painel_princial, "🤖 Ok! Bot Ativado com sucesso! ✅", reply_markup = markup)
            
            #bot.register_next_step_handler(message_final, opcoes_painel_princial)

            botStatus = 1
            vela_anterior = 0
            reladiarioenviado = 0
            parar = 0
    
            print('######################### ANALISANDO AS ESTRATÉGIAS CADASTRADAS  #########################')
            
            print()
            saldo_inicial = enviar_saldo()
            coletarDados()
            
    
    if escolha_painel_princial.text in ['📊 Placar Atual']:
        print('Placar Atual')
        placar_atual(escolha_painel_princial)

        
    if escolha_painel_princial.text in ['📈 Gestão']:
        print('Gestão')
        gestao(escolha_painel_princial)


    if escolha_painel_princial.text in ['🛑 Pausar Bot']:
        print('Pausar Bot')
        pausar(escolha_painel_princial)
    

    
    return


def opcoes_config_entrada(escolha_config_entrada):
    global resposta_usuario


    if escolha_config_entrada.text in ['◀ Voltar']:

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
        markup = markup.add('/start','✅ Ativar Bot','⚙💰 Configurações de Entrada', '💵 Saldo Atual', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot','◀ Voltar')

        #arkup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        escolha_inicial = bot.reply_to(escolha_config_entrada, "🤖 Certo! Escolha uma opção 👇",
                                reply_markup=markup)
        
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(escolha_inicial, opcoes_painel_princial)


    if escolha_config_entrada.text.split(' =')[0] in ['Valor Entrada']:

        resposta_usuario = escolha_config_entrada.text.split(' =')[0]
        
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
        markup = markup.add('◀ Voltar')

        escolha_valor_entrada = bot.reply_to(escolha_config_entrada, "🤖 Massa! Agora escolha o valor da Entrada, Lembrando que o valor mínimo aceito é o mesmo da casa de apostas 👇",
                                reply_markup=markup)
        
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(escolha_valor_entrada, registra_dados_usuario)
    
    
    if escolha_config_entrada.text.split(' =')[0] in ['Stop Gain']:
        
        resposta_usuario = escolha_config_entrada.text.split(' =')[0]
        
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
        markup = markup.add('◀ Voltar')

        escolha_valor_stop_gain = bot.reply_to(escolha_config_entrada, "🤖 Massa! Agora escolha o valor do STOP GAIN 👇",
                                reply_markup=markup)
        
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(escolha_valor_stop_gain, registra_dados_usuario)
    

    if escolha_config_entrada.text.split(' =')[0] in ['Stop Loss']:
        
        resposta_usuario = escolha_config_entrada.text.split(' =')[0]
        
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
        markup = markup.add('◀ Voltar')

        escolha_valor_stop_loss = bot.reply_to(escolha_config_entrada, "🤖 Massa! Agora escolha o valor do STOP LOSS 👇",
                                reply_markup=markup)
        
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(escolha_valor_stop_loss, registra_dados_usuario)
    

    if escolha_config_entrada.text.split(' =')[0] in ['Proteção']:
        
        resposta_usuario = escolha_config_entrada.text.split(' =')[0]
        
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
        markup = markup.add('◀ Voltar')

        escolha_protecao = bot.reply_to(escolha_config_entrada, "🤖 Massa! Agora insira o valor da proteção. Se não Desejar Proteção é só colocar 0 👇",
                                reply_markup=markup)
        
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(escolha_protecao, registra_dados_usuario)
    

    if escolha_config_entrada.text.split(' =')[0] in ['Martingale']:
        
        resposta_usuario = escolha_config_entrada.text.split(' =')[0]
        
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
        markup = markup.add('◀ Voltar')

        escolha_qnt_gale = bot.reply_to(escolha_config_entrada, "🤖 Massa! Agora escolha a Quantidade de Martingale 👇",
                                reply_markup=markup)
        
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(escolha_qnt_gale, registra_dados_usuario)
    

    if escolha_config_entrada.text.split(' =')[0] in ['Fator Gale']:
        
        resposta_usuario = escolha_config_entrada.text.split(' =')[0]
        
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
        markup = markup.add('◀ Voltar')

        escolha_tipo_gale = bot.reply_to(escolha_config_entrada, "🤖 Massa! Agora escolha o Fator Multiplicador do Gale 👇",
                                reply_markup=markup)
        
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(escolha_tipo_gale, registra_dados_usuario)
    

    if escolha_config_entrada.text.split(' =')[0] in ['Martingale Empate']:

        resposta_usuario = escolha_config_entrada.text.split(' =')[0]
        
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
        markup = markup.add('SIM', 'NÃO', '◀ Voltar')

        escolha_gale_empate = bot.reply_to(escolha_config_entrada, "🤖 Massa! Agora escolha se Deseja Gale no EMPATE 👇",
                                reply_markup=markup)
        
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(escolha_gale_empate, registra_dados_usuario)


    if escolha_config_entrada.text.split(' =')[0] in ['Fator Gale Empate']:
        
        resposta_usuario = escolha_config_entrada.text.split(' =')[0]
        
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
        markup = markup.add('◀ Voltar')

        escolha_gale_empate = bot.reply_to(escolha_config_entrada, "🤖 Massa! Agora escolha o Fator Multiplicador do Gale no Empate. 👇",
                                reply_markup=markup)
        
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(escolha_gale_empate, registra_dados_usuario)


def registrarEstrategiaExcluida(message_excluir_estrategia):
    global estrategia
    global estrategias

    if message_excluir_estrategia.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙💰 Configurações de Entrada', '💵 Saldo Atual', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot','◀ Voltar')

        message_opcoes = bot.reply_to(message_excluir_estrategia, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        
        bot.register_next_step_handler(message_opcoes, opcoes_painel_princial)
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
    markup = markup.add('/start','✅ Ativar Bot','💵 Saldo Atual', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot','◀ Voltar')

    sucesso = bot.reply_to(message_excluir_estrategia, "🤖 Estratégia excluída com sucesso! ✅", reply_markup=markup)



def pausarBot():
     while True:
        try:
            global parar
            global browser
            parar = 1
            botStatus = 0
            time.sleep(1)
            break

        except:
            continue


def registra_dados_usuario(dado_usuario):
    global valor_entrada, stop_gain, stop_loss, protecao, martingale, fator_gale, martingale_empate, fator_gale_empate

    try:

        if dado_usuario.text in ['◀ Voltar']:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            markup = markup.add(
                                f'Valor Entrada = {valor_entrada}',
                                f'Stop Gain = {stop_gain}',
                                f'Stop Loss = {stop_loss}',
                                f'Proteção = {protecao}',
                                f'Martingale = {martingale}',
                                f'Fator Gale = {fator_gale}',
                                f'Martingale Empate = {martingale_empate}',
                                f'Fator Gale = {fator_gale}',
                                '◀ Voltar')

            escolha_config_entrada = bot.reply_to(dado_usuario, "🤖 Perfeito! Escolha uma opção 👇",
                                    reply_markup=markup)
            
            #Here we assign the next handler function and pass in our response from the user. 
            bot.register_next_step_handler(escolha_config_entrada, opcoes_config_entrada)


        if resposta_usuario == 'Valor Entrada':
            valor_entrada = float(dado_usuario.text)
    
        if resposta_usuario == 'Stop Loss':
            stop_loss = float(dado_usuario.text)

        if resposta_usuario == 'Stop Gain':
            stop_gain = float(dado_usuario.text)
        
        if resposta_usuario == 'Proteção':
            protecao = float(dado_usuario.text)
        
        if resposta_usuario == 'Martingale':
            martingale = int(dado_usuario.text)

        if resposta_usuario == 'Fator Gale':
            fator_gale = float(dado_usuario.text)

        if resposta_usuario == 'Martingale Empate':
            martingale_empate = dado_usuario.text
        
        if resposta_usuario == 'Fator Gale Empate':
            fator_gale_empate = float(dado_usuario.text)




        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add(
                            f'Valor Entrada = {valor_entrada}',
                            f'Stop Gain = {stop_gain}',
                            f'Stop Loss = {stop_loss}',
                            f'Proteção = {protecao}',
                            f'Martingale = {martingale}',
                            f'Fator Gale = {fator_gale}',
                            f'Martingale Empate = {martingale_empate}',
                            f'Fator Gale Empate = {fator_gale_empate}',
                            '◀ Voltar')
        
        entrada_cadastrada = bot.reply_to(dado_usuario, f"🤖 {resposta_usuario[0]} Cadastrado com Sucesso!✅",
                                    reply_markup=markup)


        bot.register_next_step_handler(entrada_cadastrada, opcoes_config_entrada)
        

    except Exception as e:
        print(e)
        pass


def enviar_saldo():
    global id_usuario, saldo_atual

    while True:
        try:

            saldo_atual = browser.find_element_by_xpath('//*[@class="amount--bb99f"]').text
            enviar_saldo = bot.send_message(id_usuario, f"💰 SALDO ATUAL: {saldo_atual}")
            bot.register_next_step_handler(enviar_saldo, opcoes_painel_princial)
        
            return saldo_atual
        
        except:
            enviar_saldo = bot.send_message(id_usuario, "⚠️ Ocorreu um Erro ao Pegar Saldo. Fazendo uma Nova Tentativa...")
            logarSite()
            continue
    

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
        markup = markup.add('/start','✅ Ativar Bot','⚙💰 Configurações de Entrada', '💵 Saldo Atual', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot','◀ Voltar')

        message_opcoes = bot.reply_to(message_estrategia, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        
        bot.register_next_step_handler(message_opcoes, opcoes_painel_princial)

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
    markup = markup.add('/start','✅ Ativar Bot','⚙💰 Configurações de Entrada', '💵 Saldo Atual', '⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot','◀ Voltar')

    sucesso = bot.reply_to(message_estrategia, "🤖 Estratégia cadastrada com sucesso! ✅", reply_markup=markup)










########################################################################################




try:
    bot.infinity_polling(timeout=1, long_polling_timeout=1)
    bot.infinity_polling(True)
except:
    pass
    

