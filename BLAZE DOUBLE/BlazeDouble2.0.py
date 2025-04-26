from webbrowser import BaseBrowser
from selenium import webdriver
import time
import warnings
from webdriver_manager.chrome import ChromeDriverManager
import logging
from datetime import datetime, timedelta
from selenium.webdriver.support.color import Color
import pandas as pd
from columnar import columnar
import telebot
from telegram.ext import *
from telebot import *
import operator


#_______________________________________________________________________#____________________________________________________________________________________________________

print()
print('                                #################################################################')
print('                                ###################   BOT AVIATOR NIVUS   #########################')
print('                                #################################################################')
print('                                ##################### SEJA BEM VINDO ############################')
print('                                #################################################################')
print('                                ############# DESENVOLVIDO POR VICTOR RODRIGUES #################')
print('                                #################################################################\n')
print('Versão = 1.0.0')
print('Ambiente: Produção\n\n\n')



# ESSA VERSÃO, DEVIDO A ATUALIZAÇÃO DO SITE, NÃO ESTÁ MAIS CONTANDO A VELA MAIOR QUE EM TEMPO REAL
# FUNCIONALIDADE DE RELATORIO DIÁRIO DE TODAS AS ESTRATEGIAS CADASTRADAS
# AUMENTO DO NUMERO DE WIN PARA ENVIAR O GIF DO PATO PARA 20
# NÃO DEIXAR PARAR O BOT QUANDO ESTIVER VALIDANDO ESTRATÉGIA



# Definindo opções para o browser
warnings.filterwarnings("ignore", category=DeprecationWarning) 
chrome_options = webdriver.ChromeOptions() 
chrome_options.add_argument("--disable-gpu")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])


# Opção para executar o prgrama em primeiro ou segundo plano
escolha = int(input('Deseja que o programa seja executado em primeiro[1] ou segundo[2] plano? --> '))
print()
time.sleep(1)

if escolha == 1:
    print('O programa será executado em primeiro plano.\n')
else:
    print('O programa será executado em segundo plano.\n')
    chrome_options.add_argument("--headless")


# CORES
roxo = '#6b07d2'
azul = '#005d91'
rosa =  '#900087'


# DATA FRAME
df = pd.DataFrame(columns = ['data','horario','hora','minuto','vela','cor','capturado' ])


# CAPTURANDO CAMPOS
def campos():
    global data_atual
    global horario_atual
    global hora
    global minuto
    global capturado

    data_atual = datetime.today().strftime('%Y-%m-%d')
    horario_atual = datetime.today().strftime('%H:%M')
    hora = horario_atual[0:2]
    minuto = horario_atual[3:]
    capturado = 1
    return data_atual, horario_atual, hora, minuto, capturado


#usuario: Fordbracom22
#senha : Fordbracom2022

time.sleep(1)
print()
print('O Programa está sendo iniciado......')

browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)   
print('\n\n')

logger = logging.getLogger()

#browser.get(r"https://pi.njoybingo.com/game.do?token=18298495-0dce-4997-944e-f52c78717619&pn=meskbet&lang=pt&game=SPRIBE-aviator&type=CHARGED") # DEV
browser.get(r"https://br.betano.com/casino/games/aviator/3337/") # PRODUÇÃO
browser.maximize_window()


time.sleep(10)
# acessando o iframe do login
while True:
    try:
        iframe = browser.find_element_by_xpath('//*[@id="my-account-modal"]/div/iframe')
        browser.switch_to.frame(iframe)
        browser.find_element_by_xpath('//*[@id="username"]').send_keys('aviator.22')
        browser.find_element_by_xpath('//*[@id="password"]').send_keys('vb920115')
        browser.find_element_by_xpath('//*[@id="app"]/div/main/div/div/form/button').click()
        break

    except:
        #browser.get(r"https://eu-server.ssgportal.com/GameLauncher/Loader.aspx?GameCategory=JetX&GameName=JetX&ReturnUrl&Token=d54959d6-e20f-4c78-8ff1-bf8ab79c267d&PortalName=meskbet")  # DEV
        browser.get(r"https://br.betano.com/casino/games/aviator/3337/") # PRODUÇÃO
        time.sleep(10)


time.sleep(10)
# Acessando o iframe do Jogo
while True:
    try:
        iframe = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/main/div[1]/div/div[1]/div/div[1]/div/iframe')
        browser.switch_to.frame(iframe)
        break

    except:
        #browser.get(r"https://eu-server.ssgportal.com/GameLauncher/Loader.aspx?GameCategory=JetX&GameName=JetX&ReturnUrl&Token=d54959d6-e20f-4c78-8ff1-bf8ab79c267d&PortalName=meskbet")  # DEV
        browser.get(r"https://br.betano.com/casino/games/aviator/3337/") # PRODUÇÃO
        time.sleep(20)



'aviator.22'
'vb920115'



# RELATÓRIO DIÁRIO
def relaDiario():
    global placar
    global resultados_sinais
    global placar_estrategias_diaria
    global data_resultado
    global placar_win
    global placar_semGale
    global placar_gale1
    global placar_gale2
    global placar_gale3
    global placar_loss


    # PLACAR CONSOLIDADO
    try:
        placar_1 = bot.send_message(1476864287,"📊 Resultados do dia "+data_resultado+"\n==============================\n")
        placar_2 = bot.send_message(1476864287,"😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%")
    
    except Exception as a:
        logger.error('Exception ocorrido no ' + repr(a))
        placar_1 = bot.send_message(1476864287,"📊 Resultados do dia "+data_resultado+"\n==============================\n")
        placar_2 = bot.send_message(1476864287,"😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%")


    # PLACAR POR ESTRATEGIA
    for pe in placar_estrategias_diaria:
        total = int(pe[-5]) + int(pe[-4]) + int(pe[-3]) + int(pe[-2]) + int(pe[-1])
        soma_win = int(pe[-5]) + int(pe[-4]) + int(pe[-3]) + int(pe[-2])

        try:
            assertividade = str(round(soma_win / total*100, 1)).replace('.0',"")+"%"
        except:
            assertividade = '0%'

        bot.send_message(1476864287, f'🧠 {pe[:-5]} \n==========================\n 🏆= {pe[-5]}  |  🥇= {pe[-4]}  |  🥈= {pe[-3]}  |  🥉= {pe[-2]} \n\n ✅ - {soma_win} \n ❌ - {pe[-1]} \n==========================\n 🎯 {assertividade}')
        

    # ZERANDO PLACAR E ATUALIZANDO A LISTA DE ESTRATEGIAS DIARIAS
    # Resetando placar Geral (placar geral) e lista de estratégia diária
    placar_win = 0
    placar_semGale= 0
    placar_gale1= 0
    placar_gale2= 0
    placar_gale3= 0
    placar_loss = 0
    placar_estrategias_diaria = []
    estrategias_diaria = []


    # Resetando placar das estrategias (Gestão)
    for pe in placar_estrategias:
        pe[-5], pe[-4], pe[-3], pe[-2], pe[-1] = 0,0,0,0,0
        assertividade = '0%'
        placar_estrategias_diaria.append(pe) # Atualizando o placar das estratégias diária
    

    # Atualizando as estratégias diárias com as estratégias atuais
    for e in estrategias:
        estrategias_diaria.append(e)




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

    if horario_atual == '00:00' and reladiarioenviado == 0:
        relaDiario()
        reladiarioenviado +=1

    
    if horario_atual == '00:01' and reladiarioenviado == 1:
        reladiarioenviado = 0



# VALIDADOR DE ESTRATEGIAS
def funcValidador():

    global sticker_alerta
    global contador
    global cPrint
    global cValidador
    global cVela
    global reset_contagemVela
    global estrategia
    global estrategias
    global resetar_resultados
    global contagem_vela
    global validacao
    global contador_passagem
    global alerta
    global horario_atual
    global vela_atual


    if contador == 0:
        
        print(horario_atual)
        contagem_vela.append(vela_atual)
        print(f'Resultados --> {contagem_vela}')

        for estrategia in estrategias:
            for e in enumerate(estrategia[:-2]):

                if cPrint == 0:
                    print(f'Estratégia --> {estrategia}')
                    cPrint+=1


                for v in enumerate(contagem_vela):

                    while v[0] == e[0]:
                        if '+' in e[1]:
                            resultado = operator.gt(float(v[1][:-1]), float(e[1][1:]))
                            validacao.append(resultado)
                            cValidador+=1
                            cVela+=1
                            break
                            
                        if '-' in e[1]:
                            resultado = operator.lt(float(v[1][:-1]), float(e[1][1:]))
                            validacao.append(resultado)
                            cValidador+=1
                            cVela+=1
                            break
            
            if False in validacao:
                resetar_resultados+=1
            
            if resetar_resultados == len(estrategias):
                    contagem_vela = []
                    reset_contagemVela = 0
                    resetar_resultados = 0

            print(f'Validador  --> {validacao}')
            

            if validacao.count(True) == len(estrategia[:-3]):
                if False not in validacao:
                        contador+=1
                        contador_passagem +=1
                        resetar_resultados = 0
                        cPrint = 0
                        print('====================================================================')
                        return

            else:
                print('====================================================================')
                cPrint = 0
                validacao = []
    
        
                


# RASPAGEM DOS DADOS
def raspagem():

    global parar
    global browser
    global message
    global placar_win
    global placar_loss
    global cor
    global df
    global placar_win
    global placar_loss
    global placar
    global placar_semGale
    global placar_gale1
    global placar_gale2
    global placar_gale3
    global estrategias
    global estrategia
    global resultados_sinais
    global placar_estrategias
    global placar_estrategia
    global stop_loss
    global contador
    global sticker_alerta
    global cPrint
    global cValidador
    global cVela
    global reset_contagemVela
    global resetar_resultados
    global contagem_vela
    global validacao
    global contador_passagem
    global alerta
    global vela_maluca
    global table
    global message_canal_free
    global message_canal_vip
    global seq_vela_maluca
    global canal_free
    global canal_vip
    global alerta_free
    global alerta_vip
    global horario_atual
    global vela_atual
    global vela_anterior



    parar=0
    contador = 0
    contador_passagem = 0
    resetar_resultados = 0
    cValidador = 0
    cVela = 0
    cPrint = 0
    reset_contagemVela = 0
    vela_maluca = 0
    vela_repetida = 0
    validador = 0
    
    sticker_alerta = 'CAACAgEAAxkBAAEYLJFjJkhT10YXaG74v6jCEl_2RkU7tgACQQMAAnlMMUWR_eeU_LF4YCkE'
    sticker_win_2x = 'CAACAgEAAxkBAAEYLJVjJki4SBRzxvn6_GQem_rvNn6Y8wACmAIAAg-yMUU1ST1X9wZMjCkE'
    sticker_win_5x = 'CAACAgEAAxkBAAEYLJdjJkjRzpheeZlHjtPCqMZyEGfn6AAC3QIAAuMpMEW0rdfUdv7p3SkE'
    sticker_loss = 'CAACAgEAAxkBAAEYLJNjJkicux8r219JTaSpftzka4jllQACIwMAAmALOEVwyY0DApu-bikE'

    contagem_cor = []
    contagem_vela = []
    validacao = []
    

    while True:

        # Validando data para envio do relatório diário
        validaData()


        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass


        try:

            # Tentar pegar o xpath da vela. Se não conseguir, entrar na pagina novamente e tentar pegar p xpath da vela
            while True:
                try:
                    vela_atual = browser.find_element_by_xpath('/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]/div/app-payout-item[1]/div').text
                    str_cor =  Color.from_string(browser.find_element_by_xpath('/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]/div/app-payout-item[1]/div').value_of_css_property('background-color')).hex
                    break

                except:
                    #browser.get(r"https://pi.njoybingo.com/game.do?token=18298495-0dce-4997-944e-f52c78717619&pn=meskbet&lang=pt&game=SPRIBE-aviator&type=CHARGED") # DEV
                    browser.get(r"https://pi.njoybingo.com/game.do?token=e748e77d-a0da-4d44-84f9-54acdf45910f&pn=meskbet&lang=en&game=SPRIBE-aviator&type=CHARGED") # PRODUÇÃO
                    time.sleep(10)
                    

            # Funcionalidade que valida se está capturando a mesma vela.
            if vela_anterior != vela_atual or vela_anterior == 0:
                vela_repetida = 0
                pass

            elif browser.find_element_by_xpath('/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]/div/app-payout-item[1]/div').text == browser.find_element_by_xpath('/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]/div/app-payout-item[2]/div').text and vela_repetida == 0:
                if validador < 3:
                    time.sleep(1)
                    print('entrei aqui pq acho que o valor é repetido.. Validando: ', validador)
                    validador += 1
                    continue
                else:
                    print('MESMO RESULTADO DUAS VEZES NESSE MOMENTO')
                    vela_repetida +=1
                    validador = 0
                    pass
            
            else:
                continue
            
            
            contagem_vela.append(vela_atual)
            print(f'Resultados --> {contagem_vela}')

            # VALIDADOR DE_BUG
            if len(contagem_vela) <= 10:
                pass
            else:
                print('====================================================================')
                print('BUG IDENTIFICADO..REINICIANDO ANÁLISES')
                print('====================================================================')
                raspagem()


            # Validando se o resultado se encaixa na estratégia ( TRUE ou FALSE )
            if contador == 0:
                for estrategia in estrategias:
                    for e in enumerate(estrategia[:-2]):

                        if cPrint == 0:
                            print(f'Estratégia --> {estrategia}')
                            cPrint+=1

                        for v in enumerate(contagem_vela):

                            while v[0] == e[0]:
                                if '+' in e[1]:
                                    resultado = operator.gt(float(v[1][:-1]), float(e[1][1:]))
                                    validacao.append(resultado)
                                    cValidador+=1
                                    cVela+=1
                                    break
                                    
                                if '-' in e[1]:
                                    resultado = operator.lt(float(v[1][:-1]), float(e[1][1:]))
                                    validacao.append(resultado)
                                    cValidador+=1
                                    cVela+=1
                                    break
                                
                                else:
                                    print('ERRO NA ESTRATÉGIA ', estrategia,'...VERIFIQUE O CADASTRO DA MESMA.')
                                    time.sleep(5)
                                    break

                    print(f'Validador  --> {validacao}')

                    if False in validacao:
                        resetar_resultados+=1
                    

                    if resetar_resultados == len(estrategias):    # Resetando contagem de vela
                            
                        reset_contagemVela = 0
                        cPrint = 0
                        resetar_resultados = 0
                        validacao = []
                        contador = 0
                        contagem_vela = [] ####
                        print('====================================================================')
                        print('TODAS AS ESTRATEGIAS COM CONDIÇÕES FALSAS! RESETANDO ANALISE! -- Resetou na primeira função \n\n ')
                        funcValidador()
                        if contador == 0:
                            validacao = []
                            cPrint = 0
                            validador = 0
                            vela_anterior = vela_atual ##########################
                            break
                        else:
                            pass
                    

                    # SE FALTAR UMA CONDIÇÃO A SER VERDADEIRA, MANDAR ALERTA
                    if validacao.count(True) == len(estrategia[:-3]):
                            if False not in validacao:
                                print('ENVIANDO ALERTA TELEGRAM')
                                print('====================================================================')
                                try:
                                    if canal_free != '':
                                        alerta_free = bot.send_sticker(canal_free, sticker=sticker_alerta)
                                    
                                    if canal_vip !='':
                                        alerta_vip = bot.send_sticker(canal_vip, sticker=sticker_alerta)
                                    
                                    
                                    if contador == 0:
                                        contador+=1
                                        contador_passagem +=1
                                    else:
                                        pass
                                    
                                    validacao = []
                                    resetar_resultados = 0
                                    cPrint = 0
                                    validador = 0
                                    vela_anterior = vela_atual
                                    time.sleep(5)
                                    break

                                except:
                                    pass
                            
                            else:
                                print('====================================================================')
                                validacao = []
                                cPrint = 0
                        
                    else:
                        print('====================================================================')
                        validacao = []
                        cPrint = 0
                        continue


            # PASSAGEM
            if len(contagem_vela) <= 10:
                pass

            else:
                print('====================================================================')
                print('BUG IDENTIFICADO..REINICIANDO ANÁLISES')
                print('====================================================================')
                raspagem()
                    


            if contador_passagem == 2:
                pass


            elif contador_passagem == 1:
                contador_passagem+=1
                continue

            else:
                resetar_resultados = 0
                cValidador = 0
                cPrint = 0
                validacao = []
                validador = 0
                vela_anterior = vela_atual
                time.sleep(5)
                continue



            # APÓS ENVIAR ALERTA, VALIDAR SE ENVIA SINAL TELEGRAM
            if contador == 1:
                resetar_resultados=0 

                for estrategia in estrategias:
                    for e in enumerate(estrategia[:-2]):

                        if cPrint == 0:
                            print(f'Estratégia --> {estrategia}')
                            cPrint+=1

                        for v in enumerate(contagem_vela):

                            while v[0] == e[0]:
                                if '+' in e[1]:
                                    resultado = operator.gt(float(v[1][:-1]), float(e[1][1:]))
                                    validacao.append(resultado)
                                    cValidador+=1
                                    cVela+=1
                                    break
                                    
                                if '-' in e[1]:
                                    resultado = operator.lt(float(v[1][:-1]), float(e[1][1:]))
                                    validacao.append(resultado)
                                    cValidador+=1
                                    cVela+=1
                                    break
                                
                                else:
                                    print('ERRO NA ESTRATÉGIA ', estrategia,'...VERIFIQUE O CADASTRO DA MESMA.')
                                    time.sleep(5)
                                    break


                        if False in validacao:
                            resetar_resultados+=1
                        
                        if resetar_resultados == len(estrategias):
                                resetar_resultados=0
                        
                        else:
                            continue

                    print(f'Validador  --> {validacao}')


                    if False in validacao:
                        reset_contagemVela +=1
        

                    if validacao.count(True) == len(estrategia[:-2]):
                        if False not in validacao:
                    
                            # SE O CONTADOR FOR IGUAL A 2 E TODAS AS CONDIÇÕES TRUE, ENVIAR SINAL TELEGRAM
                            if validacao.count(True) == len(estrategia[:-2]) and contador == 2 or validacao.count(True) == len(estrategia[:-2]) and contador == 1:

                                print('ENVIANDO SINAL TELEGRAM')

                                headers = [' ✅ ENCERRAR EM ' + estrategia[-2] + '                                                   ']

                                data = [
                                    ['⏰ ENTRAR APÓS '+ vela_atual                    ],
                                    ['🔰 ATÉ ' + estrategia[-1] + ' GALES' if int(estrategia[-1]) > 0 else '🔰 SEM GALE'],
                                    ["🌐 <a href='https://br.betano.com/casino/games/aviator/3337/'>Site do Aviator</a>     "]
                                ]
                                
                                table = columnar(data, headers, no_borders=True)

                                try:
                                    # deletando o alerta
                                    # enviando sinal Telegram
                                    if canal_free != '':
                                        bot.delete_message(canal_free, alerta_free.message_id)
                                        message_canal_free = bot.send_message(canal_free,table, parse_mode='HTML', disable_web_page_preview=True)

                                    if canal_vip !='':
                                        bot.delete_message(canal_vip, alerta_vip.message_id)
                                        message_canal_vip = bot.send_message(canal_vip,table, parse_mode='HTML', disable_web_page_preview=True)

                                except:
                                    pass

                                print('====================================================================')
                                vela_anterior = vela_atual
                                validador = 0
                                break
                    
                    else:
                        print('====================================================================')
                        cPrint = 0
                        validacao = []
                
            # SE MANDAR O ALERTA MAS A ULTIMA CONDIÇÃO NÃO BATER, APAGAR O ALERTA E REINICIAR ANALISE
            if contador == 1 and validacao == [] or validacao == []:
                try:

                    if canal_free !='':
                        bot.delete_message(canal_free, alerta_free.message_id)
                        
                    if canal_vip !='':
                        bot.delete_message(canal_vip, alerta_vip.message_id)

                    contador = 0
                    contador_passagem = 0
                    resetar_resultados = 0
                    cPrint = 0
                    validacao = []

                    if reset_contagemVela == len(estrategias):
                        cPrint = 0
                        validacao = []
                        reset_contagemVela = 0
                        resetar_resultados = 0
                        contagem_vela = [] ####
                        print('TODAS AS ESTRATEGIAS COM CONDIÇÕES FALSAS! RESETANDO ANALISE! -- Resetou na segunda função \n\n ')
                        continue
                    
                    vela_anterior = vela_atual
                    validador = 0
                    time.sleep(5)
                    continue
                
                except:
                    pass
            
            else:
                break
            
        
        except:
            continue
               
                                            


    # Rodada após o envio do sinal Telegram
    validacao = []
    contador_cash = 0
    time.sleep(5)

    # Validando se foi solicitado o stop do BOT
    while contador_cash <= int(estrategia[-1]):

        # Validando data para envio do relatório diário
        validaData()

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass


        try:

            # Tentar pegar o xpath da vela. Se não conseguir, entrar na pagina novamente e tentar pegar p xpath da vela
            while True:
                try:
                    vela_atual = browser.find_element_by_xpath('/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]/div/app-payout-item[1]/div').text
                    str_cor =  Color.from_string(browser.find_element_by_xpath('/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]/div/app-payout-item[1]/div').value_of_css_property('background-color')).hex
                    break

                except:
                    #browser.get(r"https://pi.njoybingo.com/game.do?token=18298495-0dce-4997-944e-f52c78717619&pn=meskbet&lang=pt&game=SPRIBE-aviator&type=CHARGED") # DEV
                    browser.get(r"https://pi.njoybingo.com/game.do?token=e748e77d-a0da-4d44-84f9-54acdf45910f&pn=meskbet&lang=en&game=SPRIBE-aviator&type=CHARGED") # PRODUÇÃO
                    time.sleep(10)


            # Funcionalidade que valida se está capturando a mesma vela.
            if vela_anterior != vela_atual or vela_anterior == 0:
                vela_repetida = 0
                pass

            elif browser.find_element_by_xpath('/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]/div/app-payout-item[1]/div').text == browser.find_element_by_xpath('/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]/div/app-payout-item[2]/div').text and vela_repetida == 0:
                if validador < 3:
                    time.sleep(1)
                    print('entrei aqui pq acho que o valor é repetido.. Validando: ', validador)
                    validador += 1
                    continue
                else:
                    print('MESMO RESULTADO DUAS VEZES NESSE MOMENTO')
                    vela_repetida +=1
                    validador = 0
                    pass
            
            else:
                continue



            # VALIDANDO WIN OU LOSS
            print(vela_atual)
            vela_atual = vela_atual.strip('x')                                      

            
            if float(vela_atual) > float(estrategia[-2].strip('Xx')):
                
                # validando o tipo de WIN
                if contador_cash == 0:
                    print('WIN SEM GALE')
                    stop_loss.append('win')

                    # Preenchendo relatório
                    placar_win+=1
                    placar_semGale+=1
                    resultados_sinais = placar_win + placar_loss
                    print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
                    #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                    for pe in placar_estrategias:
                        if pe[:-5] == estrategia:
                            pe[-5] = int(pe[-5])+1 


                if contador_cash == 1:
                    print('WIN GALE1')
                    stop_loss.append('win')

                    # Preenchendo relatório
                    placar_win+=1
                    placar_gale1+=1
                    resultados_sinais = placar_win + placar_loss
                    print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
                    #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                    for pe in placar_estrategias:
                        if pe[:-5] == estrategia:
                            pe[-4] = int(pe[-4])+1


                if contador_cash == 2:
                    print('WIN GALE2')
                    stop_loss.append('win')
                    
                    # Preenchendo relatório
                    placar_win+=1
                    placar_gale2+=1
                    resultados_sinais = placar_win + placar_loss
                    print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
                    #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)
                    
                    
                    for pe in placar_estrategias:
                        if pe[:-5] == estrategia:
                            pe[-3] = int(pe[-3])+1


                if contador_cash == 3:
                    print('WIN gale3')
                    stop_loss.append('win')

                    # Preenchendo relatório
                    placar_win+=1
                    placar_gale3+=1
                    resultados_sinais = placar_win + placar_loss
                    print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
                    #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                    
                    for pe in placar_estrategias:
                        if pe[:-5] == estrategia:
                            pe[-2] = int(pe[-2])+1



                # editando mensagem enviada e enviando sticker
                try:
                    if canal_free != '':
                        bot.edit_message_text(table +"  \n============================== \n              WINNNN ✅ --- 🎯 "+ vela_atual+"x", message_canal_free.sender_chat.id, message_canal_free.message_id, parse_mode='HTML', disable_web_page_preview=True)   
                        
                        if float(vela_atual) < 5.0:
                                bot.send_sticker(canal_free, sticker=sticker_win_2x)
                        elif float(vela_atual) > 5.0:
                            bot.send_sticker(canal_free, sticker=sticker_win_5x)
                        else:
                            #bot.send_sticker(canal_free, sticker=sticker_win)
                            print('SEM FIGURINHA PARA O CHECK OUT CADASTRADO')


                    if canal_vip != '':
                        bot.edit_message_text(table +"  \n============================== \n              WINNNN ✅ --- 🎯 "+ vela_atual+"x", message_canal_vip.sender_chat.id, message_canal_vip.message_id, parse_mode='HTML', disable_web_page_preview=True)   

                        if float(vela_atual) < 5.0:
                                bot.send_sticker(canal_free, sticker=sticker_win_2x)
                        elif float(vela_atual) > 5.0:
                            bot.send_sticker(canal_free, sticker=sticker_win_5x)
                        else:
                            #bot.send_sticker(canal_free, sticker=sticker_win)
                            print('SEM FIGURINHA PARA O CHECK OUT CADASTRADO')


                    # CONDIÇÃO PARA ENVIAR O GIF DO PATO
                    if stop_loss.count('win') == 20:
                        try:
        
                            if canal_free !='':
                                bot.send_video(canal_free, video=open('money-donald-duck.mp4', 'rb'), supports_streaming=True)

                            if canal_vip !='':
                                bot.send_video(canal_vip, video=open('money-donald-duck.mp4', 'rb'), supports_streaming=True)

                        except:
                            pass


                except:
                    pass
                
                seq_vela_maluca = 0
                print('==================================================')
                time.sleep(5)
                vela_anterior = vela_atual+'x' ##########################
                raspagem()
            
            else:
                print('LOSSS')
                print('==================================================')
                contador_cash+=1
                if contador_cash <= int(estrategia[-1]):
                    vela_anterior = vela_atual+'x' ####################
                    validador = 0
                    time.sleep(5)
                else:
                    pass

                continue


        
        except:
            continue
    

    if parar != 0:
        return
    else:
        pass


    print('LOSSS GALE ',estrategia[-1])
    placar_loss +=1
    stop_loss.append('loss')
    
    
    # editando mensagem e enviando sticker
    try:
        
        if canal_free !='':
            bot.edit_message_text(table +"\n============================== \n              LOSS ✖", message_canal_free.sender_chat.id, message_canal_free.message_id, parse_mode='HTML', disable_web_page_preview=True)
            bot.send_sticker(canal_free, sticker=sticker_loss)


        if canal_vip !='':
            bot.edit_message_text(table +"\n============================== \n              LOSS ✖", message_canal_vip.sender_chat.id, message_canal_vip.message_id, parse_mode='HTML', disable_web_page_preview=True)
            bot.send_sticker(canal_vip, sticker=sticker_loss)
        

        # Preenchendo relatório
        resultados_sinais = placar_win + placar_loss
        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
    
        # Atualizando placar da estratégia
        for pe in placar_estrategias:
            if pe[:-5] == estrategia:
                pe[-1] = int(pe[-1])+1

    except:
        pass

    
        

    # Validando o stop_loss
    if 'win' in stop_loss:
        stop_loss = []
        stop_loss.append('loss')
    
    if stop_loss.count('loss') == 2:
        try:
        
            if canal_free !='':
                bot.send_message(canal_free, f'⛔🛑 Alunos,\nMercado instável! Aguardem a normalização do mesmo conforme indicamos no curso 📚.\n\nAtt, Diretoria Nivus Tips 🤝 ')

            if canal_vip !='':
                bot.send_message(canal_vip, f'⛔🛑 Alunos,\nMercado instável! Aguardem a normalização do mesmo conforme indicamos no curso 📚.\n\nAtt, Diretoria Nivus Tips 🤝 ')

            stop_loss = []
            print('STOP LOSS - ANÁLISE VOLTARÁ EM 30 MINUTOS \n\n')
            time.sleep(1800)

        except:
            pass



    print('==================================================')
    time.sleep(5)
    vela_anterior = vela_atual+'x' ##########################
    raspagem()




#________________________________________________________________________________________ TELEGRAM__________________________________________________________________________________#


print('###################### AGUARDANDO COMANDOS ######################')

global canal
global bot

#CHAVE_API = '5651549126:AAFaVyaQkxTTVPq9WxpIBejBMR_oUPdt_5o' # DEV
CHAVE_API = '5414434134:AAGwdWsXSmsflY3BbD5R-FU-dA7EXVRW3ZE' # PRODUÇÃO

bot = telebot.TeleBot(CHAVE_API)

# PLACAR
placar_win = 0
placar_semGale= 0
placar_gale1= 0
placar_gale2= 0
placar_gale3= 0
placar_loss = 0
resultados_sinais = placar_win + placar_loss
estrategias = []
placar_estrategias = []
estrategias_diaria = []
placar_estrategias_diaria = []
contador = 0
botStatus = 0
contador_passagem = 0



# LENDO TXT PARA DEFINIR VARIAVEL FREE E VIP E VALIDAÇÃO DE USUÁRIO
txt = open("canais.txt", "r")
free = txt.readlines(1)
vip = txt.readlines(2)
ids = txt.readlines(3)

for canal in free:
    free = canal.split(' ')
    free = int(free[1])
    

for canal in vip:
    vip=canal.split(' ')
    vip = int(vip[1])


for id in ids:
    id_usuario = id.split(' ')
    id_usuario = id_usuario[1]


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
        placar = bot.reply_to(message,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", reply_markup=markup)
    except Exception as a:
        logger.error('Exception ocorrido no ' + repr(a))
        placar = bot.reply_to(message,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%", reply_markup=markup)




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

    if contador_passagem != 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_excluir_estrategia = bot.reply_to(message, "🤖⛔ Estou validando uma estratégia. Deseja realmente pausar o Bot? Tente novamente em alguns instanstes.", reply_markup=markup)

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
        print('Pausar Bot')
        print('Parando o Bot....\n')
        botStatus = 0
        pausarBot()

        message_final = bot.reply_to(message, "🤖 Ok! Bot pausado 🛑", reply_markup=markup)
        
        print('###################### AGUARDANDO COMANDOS ######################')




@bot.message_handler(commands=['start'])
def start(message):

    if str(message.chat.id) in id_usuario:
       

        #Add to buttons by list with ours generate_buttons function.
        #markup = generate_buttons(['/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','📊 Placar Atual','❌ Pausar Bot'], markup)
        
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message, "🤖 Bot Aviator NIVUS Iniciado! ✅ Escolha uma opção 👇",
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
        global message_canal

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
            markup = markup.add('◀ Voltar', '📋 Enviar sinais Canal FREE', '🏆 Enviar sinais Canal VIP', '📋🏆 Enviar sinais Canal FREE & VIP')

            message_canal = bot.reply_to(message_opcoes, "🤖 Escolha para onde enviar os sinais 👇",
                                    reply_markup=markup)
            
            bot.register_next_step_handler(message_canal, escolher_canal)

    
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
    



@bot.message_handler(content_types=['text'])
def escolher_canal(message_canal):
    global canal_free
    global canal_vip
    global placar
    global estrategia
    global stop_loss
    global botStatus
    global seq_vela_maluca
    global vela_anterior
    global reladiarioenviado


    if message_canal.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_canal, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)

    if message_canal.text in ['📋 Enviar sinais Canal FREE']:

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_final = bot.reply_to(message_canal, "🤖 Ok! Ligando Bot nas configurações:\n===============================\n" + "Canal: "+ str(message_canal.text.split(' ')[4:]) + '\n Estratégia(s): \n' + str([f'{estrategia}' for estrategia in estrategias]), reply_markup = markup)
        
        print("Iniciar e enviar sinais no Canal FREE ")


        canal_free = free
        canal_vip = ''
        stop_loss = []
        botStatus = 1
        seq_vela_maluca = 0
        vela_anterior = 0
        reladiarioenviado = 0

        placar = bot.send_message(message_canal.chat.id,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%")

        print('######################### ANALISANDO AS ESTRATÉGIAS CADASTRADAS  #########################')
        print()

        raspagem()
    

    if message_canal.text in ['🏆 Enviar sinais Canal VIP']:
        
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_final = bot.reply_to(message_canal, "🤖 Ok! Ligando Bot nas configurações:\n===============================\n" + "Canal: "+ str(message_canal.text.split(' ')[4:]) + '\n Estratégia(s): \n' + str([f'{estrategia}' for estrategia in estrategias]), reply_markup = markup)
        
        print("Iniciar e enviar sinais no Canal VIP ")

        canal_free = ''
        canal_vip = vip
        stop_loss = []
        botStatus = 1
        seq_vela_maluca = 0
        vela_anterior = 0
        reladiarioenviado = 0

        placar = bot.send_message(message_canal.chat.id,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%")

        print('######################### ANALISANDO AS ESTRATÉGIAS CADASTRADAS  #########################')
        print()

        raspagem()


    if message_canal.text in ['📋🏆 Enviar sinais Canal FREE & VIP']:
        
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_final = bot.reply_to(message_canal, "🤖 Ok! Ligando Bot nas configurações:\n===============================\n" + "Canal: "+ str(message_canal.text.split(' ')[4:]) + '\n Estratégia(s): \n' + str([f'{estrategia}' for estrategia in estrategias]), reply_markup = markup)
        
        print("Iniciar e enviar sinais no Canal FREE & VIP ")

        canal_free = free
        canal_vip = vip
        stop_loss = []
        botStatus = 1
        seq_vela_maluca = 0
        vela_anterior = 0
        reladiarioenviado = 0

        placar = bot.send_message(message_canal.chat.id,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%")

        print('######################### ANALISANDO AS ESTRATÉGIAS CADASTRADAS  #########################')
        print()

        raspagem()




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






