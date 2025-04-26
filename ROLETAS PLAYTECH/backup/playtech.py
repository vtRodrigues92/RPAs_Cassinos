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



print()
print('                                #################################################################')
print('                                ##################    BOT ROLETAS PLAYTECH    ###################')
print('                                #################################################################')
print('                                ##################### SEJA BEM VINDO ############################')
print('                                #################################################################')
print('                                ############# DESENVOLVIDO POR VICTOR RODRIGUES #################')
print('                                #################################################################\n')
print('Versão = 1.0.0')
print('Ambiente: Produção\n\n\n')

parar = 0
lista_roletas = []

# RELATÓRIO DIÁRIO
def relaDiario():
    global placar
    global resultados_sinais
    global data_resultado
    global placar_win
    global placar_semGale
    global placar_gale1
    global placar_gale2
    global placar_gale3
    global placar_loss
    global roletas_diaria
    global placar_roletas_diaria
    global lista_roletas
    global estrategias
    global lista_ids
    global placar_estrategias_diaria
    global placar_estrategias
    global placar_roletas



    # PLACAR CONSOLIDADO
    for id in lista_ids:
        try:
            placar_1 = bot.send_message(id,"📊 Resultados do dia "+data_resultado+"\n==============================\n")
            placar_2 = bot.send_message(id,"😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%")
        
        except Exception as a:
            logger.error('Exception ocorrido no ' + repr(a))
            placar_1 = bot.send_message(id,"📊 Resultados do dia "+data_resultado+"\n==============================\n")
            placar_2 = bot.send_message(id,"😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%")


        # PLACAR POR ESTRATEGIA
        for pe in placar_estrategias_diaria:
            total = int(pe[-5]) + int(pe[-4]) + int(pe[-3]) + int(pe[-2]) + int(pe[-1])
            soma_win = int(pe[-5]) + int(pe[-4]) + int(pe[-3]) + int(pe[-2])

            try:
                assertividade = str(round(soma_win / total*100, 1)).replace('.0',"")+"%"
            except:
                assertividade = '0%'

            bot.send_message(id, f'🧠 {pe[:-5]} \n==========================\n 🏆= {pe[-5]}  |  🥇= {pe[-4]}  |  🥈= {pe[-3]}  |  🥉= {pe[-2]} \n\n ✅ - {soma_win} \n ❌ - {pe[-1]} \n==========================\n 🎯 {assertividade}')


        try:
            # PLACAR POR ROLETA
            for pr in placar_roletas_diaria:
                total = int(pr[-5]) + int(pr[-4]) + int(pr[-3]) + int(pr[-2]) + int(pr[-1])
                soma_win = int(pr[-5]) + int(pr[-4]) + int(pr[-3]) + int(pr[-2])

                try:
                    assertividade = str(round(soma_win / total*100, 1)).replace('.0',"")+"%"
                except:
                    assertividade = '0%'

                bot.send_message(id, f'🧠 {pr[:-5]} \n==========================\n 🏆= {pr[-5]}  |  🥇= {pr[-4]}  |  🥈= {pr[-3]}  |  🥉= {pr[-2]} \n\n ✅ - {soma_win} \n ❌ - {pr[-1]} \n==========================\n 🎯 {assertividade}')
        except:
            pass


    # ZERANDO PLACAR E ATUALIZANDO A LISTA DE ESTRATEGIAS DIARIAS
    # Resetando placar Geral (placar geral) e lista de estratégia diária
    placar_win = 0
    placar_semGale= 0
    placar_gale1= 0
    placar_gale2= 0
    placar_gale3= 0
    placar_loss = 0
    placar_estrategias_diaria = []
    roletas_diaria = []
    placar_roletas_diaria = []

    ''' ESTRATEGIAS'''
    # Resetando placar das estrategias (Gestão)
    for pe in placar_estrategias:
        pe[-5], pe[-4], pe[-3], pe[-2], pe[-1] = 0,0,0,0,0
        assertividade = '0%'
        placar_estrategias_diaria.append(pe) # Atualizando o placar das estratégias diária


    # Atualizando as estratégias diárias com as estratégias atuais
    for e in estrategias:
        estrategias_diaria.append(e)

    ''' ROLETAS '''
    try:
        # Resetando placar das roletas (Gestão)
        for pr in placar_roletas:
            pr[-5], pr[-4], pr[-3], pr[-2], pr[-1] = 0,0,0,0,0
            assertividade = '0%'
            placar_roletas_diaria.append(pr) # Atualizando o placar das estratégias diária

        # Atualizando as roletas diárias com as roletas atuais
        for r in lista_roletas:
            roletas_diaria.append(r)
    except:
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

    if horario_atual == '00:00' and reladiarioenviado == 0:
        relaDiario()
        reladiarioenviado +=1

    
    if horario_atual == '00:01' and reladiarioenviado == 1:
        reladiarioenviado = 0




def apostas():
    global opcoes_apostas

    opcoes_apostas = {

            '1ºcoluna': ['1', '4', '7', '10', '13', '16', '19', '22', '25', '28', '31', '34'],
            '2ªcoluna': ['2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32', '35'],
            '3ªcoluna': ['3', '6', '9', '12', '15', '18', '21', '24', '27', '30', '33', '36'],

            '1ºduzia': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
            '2ªduzia': ['13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'],
            '3ªduzia': ['25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36'],

            'Cor vermelho': ['1', '3', '5', '7', '9', '12', '14', '16', '18', '19', '21', '23', '25', '27', '30', '32', '34', '36'],
            'Cor preto': ['2', '4', '6', '8', '10', '11', '13', '15', '17', '20', '22', '24', '26', '28', '29', '31', '33', '35'],

            'Números par(es)': ['2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24', '26', '28', '30', '32', '34', '36'],
            'Números impar(es)': ['1', '5', '7', '9', '11', '13', '15', '17', '19', '21', '23', '25', '27', '29', '31', '33', '35'],

            'Números baixos': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18'],
            'Números altos': ['19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36'],
            
            '1º/2ªcoluna': ['1', '4', '7', '10', '13', '16', '19', '22', '25', '28', '31', '34', '2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32', '35'],
            '2ª/3ªcoluna': ['2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32', '35', '3', '6', '9', '12', '15', '18', '21', '24', '27', '30', '33', '36'],
            '1º/3ªcoluna': ['1', '4', '7', '10', '13', '16', '19', '22', '25', '28', '31', '34', '3', '6', '9', '12', '15', '18', '21', '24', '27', '30', '33', '36'],

            '1º/2ªduzia': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'],
            '2ª/3ªduzia': ['13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36'],
            '1º/3ªduzia': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36']
        
        }




def apostasExternas(estrategia_usuario, dic_estrategia_usuario):
    global opcoes_apostas

    try:
        opcoes_apostas = {

            '1ºcoluna': ['1', '4', '7', '10', '13', '16', '19', '22', '25', '28', '31', '34'],
            '2ªcoluna': ['2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32', '35'],
            '3ªcoluna': ['3', '6', '9', '12', '15', '18', '21', '24', '27', '30', '33', '36'],

            '1ºduzia': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
            '2ªduzia': ['13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'],
            '3ªduzia': ['25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36'],

            'cor vermelho': ['1', '3', '5', '7', '9', '12', '14', '16', '18', '19', '21', '23', '25', '27', '30', '32', '34', '36'],
            'cor preto': ['2', '4', '6', '8', '10', '11', '13', '15', '17', '20', '22', '24', '26', '28', '29', '31', '33', '35'],

            'números par(es)': ['2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24', '26', '28', '30', '32', '34', '36'],
            'números impar(es)': ['1', '5', '7', '9', '11', '13', '15', '17', '19', '21', '23', '25', '27', '29', '31', '33', '35'],

            'números baixos': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18'],
            'números altos': ['19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36'],

            '1º/2ªcoluna': ['1', '4', '7', '10', '13', '16', '19', '22', '25', '28', '31', '34', '2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32', '35'],
            '2ª/3ªcoluna': ['2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32', '35', '3', '6', '9', '12', '15', '18', '21', '24', '27', '30', '33', '36'],
            '1º/3ªcoluna': ['1', '4', '7', '10', '13', '16', '19', '22', '25', '28', '31', '34', '3', '6', '9', '12', '15', '18', '21', '24', '27', '30', '33', '36'],

            '1º/2ªduzia': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'],
            '2ª/3ªduzia': ['13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36'],
            '1º/3ªduzia': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36']

        }

        for opcao_aposta in opcoes_apostas:
            if estrategia_usuario == opcao_aposta:
                dic_estrategia_usuario[opcao_aposta] = opcoes_apostas[opcao_aposta]
                print(dic_estrategia_usuario)
        
        return dic_estrategia_usuario
    
    except:
        pass
            



#def mapear_cassinos_playtech():
 #   global dic_cassinos
#
 #   dic_cassinos = {}
#
 #   ''' Pegando nome das roletas'''
 #   nome_roletas = browser.find_elements_by_css_selector('.lobby-table__name-container')
 #   ''' Pegando o link das roletas'''
 #   site_roletas = browser.find_elements_by_css_selector('.tile>.button')
 #   ''' PEGANDO LISTA DE CASSINOS DA PLAYTECH'''
 #   nomeDosCassinos()
 #   ''' LOOP FOR PARA CRIAR UM DICIONARIO COM O NOME DA ROLETA E SEU RESPECTIVO SITE '''
 #   for nome_roleta in enumerate(nome_roletas):
 #       for site_roleta in enumerate(site_roletas):
 #           while nome_roleta[0] == site_roleta[0]:
 #               if nome_roleta[1].text.replace('\ni','') in cassinos:
 #                   #print(nome_roleta[1].text.replace('\ni',''))
 #                   nome_roleta = nome_roleta[1].text
 #                   site_roleta = site_roleta[1].get_attribute('href')
 #                   dic_cassinos[nome_roleta] = site_roleta
#
 #               else:
 #                   break
    
    

def formatar_resultados(lista_resultados, resultado):
    resultados = resultado[1].text.split('\n')
    for numero in resultados:
        if 'x' not in numero:
            lista_resultados.append(numero)
    
    return lista_resultados




def nomeDosCassinos():
    global cassinos

    cassinos = [

        ('Age Of The Gods Bonus Roulette'),
        ('American Roulette'),
        ('Auto Roulette'),
        ('Bucharest Roulette'),
        ('Deutsches Roulette'),
        ('Football Roulette'),
        ('French Roulette'),
        ('Greek Roulette'),
        ('Hindi Roulette'),
        ('Mega Fire Blaze Roulette Live'),
        ('Prestige Roulette'),
        ('Quantum Roulette Live'),
        ('Roleta Brasileira'),
        ('Roulette'),
        ('Roulette Italiana'),
        ('Speed Auto Roulette'),
        ('Speed Roulette'),
        ('Turkish Roulette'),
        ('Who Wants To Be a Millionaire? Roulette')

        #('Spread Bet Roulette'),
        #('Live Mega Fire Blaze Roulette'),
        #('Roleta Brasileira'),
        #('Live Football Roulette'),
        #('Live Age of the Gods Bonus Roulette'),
        #('Live Quantum Roulette'),
        #('Live American Roulette'),
        #('Live Quantum Auto Roulette'),
        #('Live French Roulette'),
        #('Live Prestige Roulette'),
        #('Live Casino Hold’Em'),
        #('Brazilian Roulette', 'https://play.betfair.com/launch/web?returnURL=https%3A%2F%2Flauncher.betfair.com%2F%3FgameId%3Dbrazilian-roulette-cev%26returnURL%3Dhttps%253A%252F%252Fcasino.betfair.com%252Fpt-br%252Fjogos%252Fbrazilian-roulette-cev%26launchProduct%3Dgaming%26RPBucket%3Dgaming%26mode%3Dreal%26dataChannel%3Decasino&_gl=1*1yzh5nv*_ga*MTM0MjM4MDEzLjE2NjU0NjEwOTg.*_ga_K0W97M6SNZ*MTY2NTQ2MTA5OS4xLjEuMTY2NTQ2MTI3My42MC4wLjA.'),
        #('Roleta Relâmpago', 'https://play.betfair.com/launch/web?returnURL=https%3A%2F%2Flauncher.betfair.com%2F%3FgameId%3Dlive-lr-brazil-cev%26returnURL%3Dhttps%253A%252F%252Fcasino.betfair.com%252Fpt-br%252Fp%252Fcassino-ao-vivo%26launchProduct%3Dgaming%26RPBucket%3Dgaming%26mode%3Dreal%26dataChannel%3Decasino&_gl=1*tdxqfo*_ga*ODMzMDkzOTgyLjE2NjU0NTc0MzA.*_ga_K0W97M6SNZ*MTY2NTQ1NzQzMC4xLjEuMTY2NTQ1ODk4Mi42MC4wLjA.'),
        #('Spin & Win Roulette', 'https://casino-com-flash.bfcdl.com/live_desktop/bundles/22.6.2.18/?launch_alias=sgrol_spinandgorol&language=pt&gameType=lobby&redirect_time=1665459292008&backUrl=https%3A%2F%2Fcasino-com-flash.bfcdl.com%2Flive_desktop%2F%3Flaunch_alias%3Dsgrol_spinandgorol%26language%3Dpt#/'),
        #('Lightning Roulette', 'https://play.betfair.com/launch/web?returnURL=https%3A%2F%2Flauncher.betfair.com%2F%3FgameId%3Dlightening-roulette-cev%26returnURL%3Dhttps%253A%252F%252Fcasino.betfair.com%252Fpt-br%252Fp%252Fcassino-ao-vivo%26launchProduct%3Dgaming%26RPBucket%3Dgaming%26mode%3Dreal%26dataChannel%3Decasino&_gl=1*1dxhk9w*_ga*ODMzMDkzOTgyLjE2NjU0NTc0MzA.*_ga_K0W97M6SNZ*MTY2NTQ1NzQzMC4xLjEuMTY2NTQ1OTM4NS42MC4wLjA.'),
        #('American Roulette', 'https://casino-com-flash.bfcdl.com/live_desktop/bundles/22.6.2.18/?launch_alias=rodzl_doublezero&language=pt&gameType=lobby&redirect_time=1665459429266&backUrl=https%3A%2F%2Fcasino-com-flash.bfcdl.com%2Flive_desktop%2F%3Flaunch_alias%3Drodzl_doublezero%26language%3Dpt#/'),
        #('Roulette Live', 'https://play.betfair.com/launch/web?returnURL=https%3A%2F%2Flauncher.betfair.com%2F%3FgameId%3Droulette-live-cev%26returnURL%3Dhttps%253A%252F%252Fcasino.betfair.com%252Fpt-br%252Fp%252Fcassino-ao-vivo%26launchProduct%3Dgaming%26RPBucket%3Dgaming%26mode%3Dreal%26dataChannel%3Decasino&_gl=1*18m9sct*_ga*ODMzMDkzOTgyLjE2NjU0NTc0MzA.*_ga_K0W97M6SNZ*MTY2NTQ1NzQzMC4xLjEuMTY2NTQ1OTQ2OS42MC4wLjA.'),
        #('Who Wants To Be a Millionaire Roulette', 'https://casino-com-flash.bfcdl.com/live_desktop/bundles/22.6.2.18/?launch_alias=wwtbamrol_millrol&language=pt&gameType=lobby&redirect_time=1665459506687&backUrl=https%3A%2F%2Fcasino-com-flash.bfcdl.com%2Flive_desktop%2F%3Flaunch_alias%3Dwwtbamrol_millrol%26language%3Dpt#/'),
        #('French Roulette', 'https://casino-com-flash.bfcdl.com/live_desktop/bundles/22.6.2.18/?launch_alias=rofl_loungerol&language=pt&gameType=lobby&redirect_time=1665459600384&backUrl=https%3A%2F%2Fcasino-com-flash.bfcdl.com%2Flive_desktop%2F%3Flaunch_alias%3Drofl_loungerol%26language%3Dpt#/'),
        #('XXXtreme Lightning Roulette', 'https://play.betfair.com/launch/web?returnURL=https%3A%2F%2Flauncher.betfair.com%2F%3FgameId%3Dxxxtreme-lr-cev%26returnURL%3Dhttps%253A%252F%252Fcasino.betfair.com%252Fpt-br%252Fp%252Fcassino-ao-vivo%26launchProduct%3Dgaming%26RPBucket%3Dgaming%26mode%3Dreal%26dataChannel%3Decasino&_gl=1*1f3vbrj*_ga*ODMzMDkzOTgyLjE2NjU0NTc0MzA.*_ga_K0W97M6SNZ*MTY2NTQ1NzQzMC4xLjEuMTY2NTQ1OTY5My40LjAuMA..'),
        #('Roulette Live', 'https://casino-com-flash.bfcdl.com/live_desktop/bundles/22.6.2.18/?launch_alias=rol_loungerol&language=pt&gameType=lobby&redirect_time=1665459730080&backUrl=https%3A%2F%2Fcasino-com-flash.bfcdl.com%2Flive_desktop%2F%3Flaunch_alias%3Drol_loungerol%26language%3Dpt#/'),
        #('Football French Roulette', 'https://casino-com-flash.bfcdl.com/live_desktop/bundles/22.6.2.18/?launch_alias=rofl_livefootballroulette&language=pt&gameType=lobby&redirect_time=1665459810704&backUrl=https%3A%2F%2Fcasino-com-flash.bfcdl.com%2Flive_desktop%2F%3Flaunch_alias%3Drofl_livefootballroulette%26language%3Dpt#/'),
        #('Bucharest French Roulette', 'https://casino-com-flash.bfcdl.com/live_desktop/bundles/22.6.2.18/?launch_alias=rofl_triumphrol&language=pt&gameType=lobby&redirect_time=1665459899244&backUrl=https%3A%2F%2Fcasino-com-flash.bfcdl.com%2Flive_desktop%2F%3Flaunch_alias%3Drofl_triumphrol%26language%3Dpt#/'),
        #('Classic Roulette')
        #('Live Soho All Bets Blackjack'),
        #('Live Adventures Beyond Wonderland'),

    ]




def inicio():
    global browser
    global lobby_cassinos

    lobby_cassinos = 'https://launcher.betfair.com/?gameId=live-roulette-cptl&returnURL=https%3A%2F%2Fcasino.betfair.com%2Fpt-br%2Fp%2Fcassino-ao-vivo&launchProduct=gaming&RPBucket=gaming&mode=real&dataChannel=ecasino&switchedToPopup=true'

    # Definindo opções para o browser
    warnings.filterwarnings("ignore", category=DeprecationWarning) 
    chrome_options = webdriver.ChromeOptions() 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Opção para executar o prgrama em primeiro ou segundo plano
    escolha = int(input('Deseja que o programa mostre o navegador? [1]SIM [2]NÃO --> '))
    print()
    time.sleep(1)
    if escolha == 1:
        print('O programa será executado mostrando o navegador.\n')
    else:
        print('O programa será executado com o navegador oculto.\n')
        chrome_options.add_argument("--headless")

    browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)




def logarSite():
    browser.get(lobby_cassinos)
    browser.maximize_window()
    time.sleep(10)
    ''' Inserindo login e senha '''
    ''' Lendo o arquivo txt config-mensagens '''
    txt = open("canais.txt", "r", encoding="utf-8")
    mensagem_login = txt.readlines()
    usuario = mensagem_login[2].replace('\n','').split('= ')[1] 
    senha = mensagem_login[3].replace('\n','').split('= ')[1]
    ''' Mapeando elementos para inserir credenciais '''
    try:
        browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click() #cookies
    except:
        pass
    browser.find_element_by_xpath('//*[@id="username"]').send_keys(usuario) #Inserindo login
    browser.find_element_by_xpath('//*[@id="password"]').send_keys(senha) #Inserindo senha
    browser.find_element_by_xpath('//*[@id="login"]').click() #Clicando no btn login
    time.sleep(10)





def coletarResultados(lista_roletas):
    global site_cassino_desktop
    global site_cassino_mobile
    global dicionario_roletas
    global contador_passagem

    while True:

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass
        
        # Validando o horario para envio do relatório diário
        validaData()

        try:
            ''' Elemento das roletas e historico de resultados '''
            roletas = browser.find_elements_by_css_selector('.lobby-table__name-container')
            historico_resultados = browser.find_elements_by_css_selector('.roulette-history_lobbyDxuTPpg3FmAO6mbqrAe7')
            lista_resultados = []
            
            ''' Percorrendo as roletas'''
            for roleta in enumerate(roletas):
                nome_cassino = roleta[1].text

                # Validando se foi solicitado o stop do BOT
                if parar != 0:
                    break
                else:
                    pass

                ''' Valida se tem algum cassino cadastrado pelo usuário. Se não, analisa todos do grupo '''
                if lista_roletas == [] and nome_cassino in cassinos:
                    pass
                
                elif nome_cassino in lista_roletas:
                    pass
                
                else:
                    continue
                
                ''' Percorrendo o historico das Roletas '''
                for resultado in enumerate(historico_resultados):
                    while roleta[0] == resultado[0]:
                        historico_roleta = formatar_resultados(lista_resultados, resultado) # Formata o historico em lista
                        ''' Verifica se o historico da Roleta já consta no dicionario ** Importante para a função de Ultimos Resultados '''
                        try:
                            if historico_roleta != dicionario_roletas[nome_cassino] or dicionario_roletas == {}:
                                dicionario_roletas[nome_cassino] = historico_roleta
                                print(dicionario_roletas)
                        except:
                            dicionario_roletas[nome_cassino] = historico_roleta

                        ''' Chama a função que valida a estratégia para enviar o sinal Telegram'''
                        validarEstrategia(dicionario_roletas, nome_cassino, lista_resultados, lista_estrategias, roleta)
                        print('=' * 220)
                        lista_resultados = []
                        break
            
        except:
            continue 
    



def validarEstrategia(dicionario_roletas, nome_cassino, lista_resultados, lista_estrategias, roleta):
    global estrategia
    global contador_passagem
    global lista_resultados_sinal

    try:

        for estrategia in lista_estrategias:
            
            # Validando se foi solicitado o stop do BOT
            if parar != 0:
                break
            else:
                pass

            # Validando o horario para envio do relatório diário
            validaData()

            print ('Analisando a Estrategia --> ', estrategia)

            ''' Pegando o tipo de aposta (AUSENCIA OU REPETIÇÃO '''
            tipo_aposta = estrategia[0]

            ''' Pegando os números da aposta externa da estratégia'''
            aposta_externa = apostasExternas(estrategia[1], dic_estrategia_usuario)

            ''' Pegando a sequencia minima da estratégia cadastrada pelo usuário '''
            sequencia_minima = estrategia[2]
            
            print('Historico_Roleta --> ', nome_cassino, dicionario_roletas[nome_cassino][:int(sequencia_minima)])

            ''' ANTES DE PASSAR NO VALIDADOR, VERIFICAR SE EXISTE O RESULTADO 0 POIS O 0 QUEBRA A SEQUENCIA'''
            if '0' in dicionario_roletas[nome_cassino][:int(sequencia_minima)] or '00' in dicionario_roletas[nome_cassino][:int(sequencia_minima)]:
                print('Sequencia com resultado 0...Analisando outra estratégia!')
                continue
            
            else:
                pass

            ''' Verifica se os números da seq minima do historico da roleta está dentro da estratégia '''
            validador = validarEstrategiaAlerta(dicionario_roletas, nome_cassino, aposta_externa, sequencia_minima, estrategia)
            
            ''' Validando se bateu alguma condição'''
            if validador.count('true') == int(sequencia_minima)-1:
                print('IDENTIFICADO PRÉ PADRÃO NA ROLETA ', nome_cassino, ' COM A ESTRATÉGIA ', estrategia)
                print('ENVIAR ALERTA')
                enviarAlertaTelegram(dicionario_roletas, nome_cassino, sequencia_minima, estrategia)
                time.sleep(1)

                ''' Verifica se a ultima condição bate com a estratégia para enviar sinal Telegram '''
                while True:
                    
                    ''' Lendo novos resultados para validação da estratégia'''
                    if browser.find_elements_by_xpath(f'//*[@id="root"]/div/div[3]/div[1]/div/div[2]/div[1]/div/div[1]/div/div/div[{roleta[0]+2}]/div/div/div/div[1]/div[5]/div'):
                        numeros_recentes_validacao = browser.find_elements_by_xpath(f'//*[@id="root"]/div/div[3]/div[1]/div/div[2]/div[1]/div/div[1]/div/div/div[{roleta[0]+2}]/div/div/div/div[1]/div[5]/div')
                        
                    ''' LISTA DO PROXIMO RESULTADO APOS O ALERTA'''
                    lista_proximo_resultados = []
                    try:
                        for numeroRecente in numeros_recentes_validacao:
                            numero_r = numeroRecente.text
                            if 'x' not in numero_r:
                                lista_proximo_resultados.append(numero_r)
                    except:
                        pass

                    ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
                    if lista_resultados[:3] != lista_proximo_resultados[:3]:

                        if estrategia[0] == 'repetição':
                            ''' Verificando se o ultimo resultado da roleta está dentro da estratégia'''
                            if lista_proximo_resultados[0] in aposta_externa[estrategia[1]]:
                                dicionario_roletas[nome_cassino] = lista_proximo_resultados
                                print('ENVIANDO SINAL TELEGRAM')
                                enviarSinalTelegram(nome_cassino, sequencia_minima, estrategia)
                                checkSinalEnviado(lista_proximo_resultados, nome_cassino, roleta)
                                time.sleep(1)
                                break
                            
                            else:
                                print('APAGA SINAL DE ALERTA')
                                apagaAlertaTelegram()
                                dicionario_roletas[nome_cassino] = lista_proximo_resultados
                                break
                        
                        if estrategia[0] == 'ausência':
                            ''' Verificando se o ultimo resultado da roleta não está dentro da estratégia'''
                            if lista_proximo_resultados[0] not in aposta_externa[estrategia[1]]:
                                dicionario_roletas[nome_cassino] = lista_proximo_resultados
                                print('ENVIANDO SINAL TELEGRAM')
                                enviarSinalTelegram(nome_cassino, sequencia_minima, estrategia)
                                checkSinalEnviado(lista_proximo_resultados, nome_cassino, roleta)
                                break
                            
                            else:
                                print('APAGA SINAL DE ALERTA')
                                apagaAlertaTelegram()
                                dicionario_roletas[nome_cassino] = lista_proximo_resultados
                                break


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





def enviarAlertaTelegram(dicionario_roletas, nome_cassino, sequencia_minima, estrategia):
    global alerta_free
    global alerta_vip
    global contador_passagem
    global alerta

    ''' Lendo o arquivo txt canais '''
    txt = open("canais.txt", "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[12].split(' ')[1].split('\n')[0].split((','))

    ''' Lendo o arquivo txt config-mensagens '''
    txt = open("config-mensagens.txt", "r", encoding="utf-8")
    mensagem_alerta = txt.readlines()
    
    #headers_alerta = [mensagem_alerta[0].replace('\n','')]
#
    #data_alerta = [
    #
    #    [mensagem_alerta[1].replace('\n','').replace('[FORNECEDOR]', nome_fornecedor)],
    #    [''],
    #    [mensagem_alerta[3].replace('\n','').replace('[NOME_CASSINO]', nome_cassino.title())],
    #    [mensagem_alerta[4].replace('\n','').replace('[ESTRATEGIA]', estrategia[0].title()+' de '+estrategia[1].title())],
    #    [''],
    #    [mensagem_alerta[6].replace('\n','').replace('[TIPO_ESTRATEGIA]', estrategia[0].title()+' de ').replace('[ESTRATEGIA]', estrategia[1].title())],
    #    [mensagem_alerta[7].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(dicionario_roletas[nome_cassino][:int(sequencia_minima)-1]))],
    #    [''],
    #    [''+ mensagem_alerta[9].replace('\n','').replace('[SITE_CASSINO]', site_cassino_desktop)+'➖'+mensagem_alerta[10].replace('\n','').replace('[SITE_CASSINO]', site_cassino_mobile)]
    #
    #]
#
    #table_alerta = columnar(data_alerta, headers_alerta, no_borders=True)
    
    table_alerta = mensagem_alerta[0].replace('\n','') + '\n' + mensagem_alerta[1].replace('\n','') + '\n\n' + mensagem_alerta[3].replace('\n','').replace('[NOME_CASSINO]', nome_cassino.title())+'\n' + mensagem_alerta[4].replace('\n','').replace('[ESTRATEGIA]', estrategia[0].title()+' de '+estrategia[1].title()) + '\n\n' + mensagem_alerta[6].replace('\n','').replace('[TIPO_ESTRATEGIA]', estrategia[0].title()+' de ').replace('[ESTRATEGIA]', estrategia[1].title()) + '\n' + mensagem_alerta[7].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(dicionario_roletas[nome_cassino][:int(sequencia_minima)-1])) + '\n\n' + mensagem_alerta[9].replace('\n','')
    try:
        for canal in canais:
            globals()[f'alerta_{canal}'] = bot.send_message(canal, table_alerta, parse_mode='HTML', disable_web_page_preview=True)  #Variavel Dinâmica

    except:
        pass
    
    ''' Enviando mensagem Telegram '''
    #try:
#
    #    if canal_free != '':
    #        alerta_free = bot.send_message(canal_free, table_alerta, parse_mode='HTML', disable_web_page_preview=True)
    #        
    #    if canal_vip !='':
    #        alerta_vip = bot.send_message(canal_vip, table_alerta, parse_mode='HTML', disable_web_page_preview=True)
#
    #    contador_passagem += 1
#
    #except:
    #    pass





def enviarSinalTelegram(nome_cassino, sequencia_minima, estrategia):
    global alerta
    global alerta_free
    global alerta_vip
    global table_sinal
    global message_canal
    global message_canal_free
    global message_canal_vip
    global text_mensagem
    global text_mensagem2
    global text_mensagem3
    global text_mensagem4
    global text_mensagem5
    global text_mensagem6
    global text_mensagem7
    global text_mensagem8
    global text_mensagem9
    global text_mensagem10
    global text_mensagem11
    global text_mensagem12


    ''' Lendo o arquivo txt config-mensagens '''
    txt = open("config-mensagens.txt", "r", encoding="utf-8")
    arquivo_mensagem = txt.readlines()
    mensagem_sinal = arquivo_mensagem[1].split(',')

    ''' Estruturando mensagem '''
    txt = open("config-mensagens.txt", "r", encoding="utf-8")
    mensagem_sinal = txt.readlines()

    #headers_sinal = [mensagem_sinal[18].replace('\n','')]
#
    #data_sinal = [
#
    #    [mensagem_sinal[19].replace('\n','').replace('[FORNECEDOR]', nome_fornecedor)],
    #    [''],
    #    [mensagem_sinal[21].replace('\n','').replace('[NOME_CASSINO]', nome_cassino.title())],
    #    [mensagem_sinal[22].replace('\n','').replace('[ESTRATEGIA]', estrategia[0].title()+' de '+estrategia[1].title())],
    #    [mensagem_sinal[23].replace('\n','').replace('[APOSTA]', estrategia[3].upper())],
    #    [mensagem_sinal[24].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(dicionario_roletas[nome_cassino][:int(sequencia_minima)]))],
    #    [''],
    #    [mensagem_sinal[26].replace('\n','')],
    #    [''],
    #    [''+ mensagem_sinal[28].replace('\n','').replace('[SITE_CASSINO]', site_cassino_desktop)+'➖'+mensagem_sinal[29].replace('\n','').replace('[SITE_CASSINO]', site_cassino_mobile)]
#
    #]

    table_sinal = mensagem_sinal[18].replace('\n','') + '\n' + mensagem_sinal[19].replace('\n','') + '\n\n' + mensagem_sinal[21].replace('\n','').replace('[NOME_CASSINO]', nome_cassino.title()) + '\n' + mensagem_sinal[22].replace('\n','').replace('[ESTRATEGIA]', estrategia[0].title()+' de '+estrategia[1].title()) + '\n' + mensagem_sinal[23].replace('\n','').replace('[APOSTA]', estrategia[3].upper()) + '\n' + mensagem_sinal[24].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(dicionario_roletas[nome_cassino][:int(sequencia_minima)])) + '\n\n' + mensagem_sinal[26].replace('\n','') + '\n\n' + mensagem_sinal[28].replace('\n','')+mensagem_sinal[29].replace('\n','')

    try:
        for canal in canais:
            bot.delete_message(canal, globals()[f'alerta_{canal}'].message_id)
            globals()[f'sinal_{canal}'] = bot.send_message(canal, table_sinal, parse_mode='HTML', disable_web_page_preview=True)
    
    except:
        pass


    #try:
    #    # deletando o alerta
    #    # enviando sinal Telegram
    #    if canal_free != '':
    #        bot.delete_message(canal_free, alerta_free.message_id)
    #        message_canal_free = bot.send_message(canal_free, table_sinal, parse_mode='HTML', disable_web_page_preview=True)
#
    #    if canal_vip !='':
    #        bot.delete_message(canal_vip, alerta_vip.message_id)
    #        message_canal_vip = bot.send_message(canal_vip, table_sinal, parse_mode='HTML', disable_web_page_preview=True)
#
    #except:
    #    pass





def apagaAlertaTelegram():
    global contador_passagem

    try:
        for canal in canais:
            bot.delete_message(canal, globals()[f'alerta_{canal}'].message_id)
    except:
        pass

    contador_passagem = 0

    #try:
    #    if canal_free != '':
    #        bot.delete_message(canal_free, alerta_free.message_id)
#
    #    if canal_vip !='':
    #        bot.delete_message(canal_vip, alerta_vip.message_id)
#
    #except:
    #    pass

    


def checkSinalEnviado(lista_proximo_resultados, nome_cassino, roleta):
    global table
    global alerta_free
    global alerta_vip
    global message_canal
    global message_canal_free
    global message_canal_vip
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
            
            ''' Lendo novos resultados para validação da estratégia'''
            if browser.find_elements_by_xpath(f'//*[@id="root"]/div/div[3]/div[1]/div/div[2]/div[1]/div/div[1]/div/div/div[{roleta[0]+2}]/div/div/div/div[1]/div[5]/div'):
                numeros_recentes_validacao = browser.find_elements_by_xpath(f'//*[@id="root"]/div/div[3]/div[1]/div/div[2]/div[1]/div/div[1]/div/div/div[{roleta[0]+2}]/div/div/div/div[1]/div[5]/div')
                        

            lista_resultados_sinal = []
            try:
                for numeroRecente in numeros_recentes_validacao:
                    numero_r = numeroRecente.text
                    if 'x' not in numero_r:
                        lista_resultados_sinal.append(numero_r)
            except:
                pass
            
            ''' Validando se tem dado Vazio '''
            if '' in lista_resultados_sinal:
                continue

            ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
            if lista_proximo_resultados[:3] != lista_resultados_sinal[:3]:
                
                print(lista_resultados_sinal[0])
                resultados.append(lista_resultados_sinal[0])
                
                grupo_apostar = apostasExternas(estrategia[3], dic_estrategia_usuario)

                # VALIDANDO WIN OU LOSS
                if lista_resultados_sinal[0] in grupo_apostar[estrategia[3]] or lista_resultados_sinal[0] == '0' or lista_resultados_sinal[0] == '00':
                
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

                        # Preenchendo relatório
                        placar_win+=1
                        placar_gale1+=1
                        resultados_sinais = placar_win + placar_loss
                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
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
                        
                        # Preenchendo relatório
                        placar_win+=1
                        placar_gale2+=1
                        resultados_sinais = placar_win + placar_loss
                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
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

                
                    if contador_cash == 3:
                        print('WIN gale3')
                        stop_loss.append('win')

                        # Preenchendo relatório
                        placar_win+=1
                        placar_gale3+=1
                        resultados_sinais = placar_win + placar_loss
                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)
                        
                        try:
                            # Somando Win na estratégia da lista atual
                            for pe in placar_estrategias:
                                if pe[:-5] == [estrategia[1].upper()]:
                                    pe[-2] = int(pe[-2])+1
                            
                        except:
                            pass

                        if lista_roletas != []:
                            # Somando Win na roleta atual
                            for pr in placar_roletas:
                                if pr[:-5] == [nome_cassino.upper()]:
                                    pr[-2] = int(pr[-2])+1
        

                    # respondendo a mensagem do sinal
                    try:
                        ''' Lendo o arquivo txt config-mensagens '''
                        txt = open("config-mensagens.txt", "r", encoding="utf-8")
                        mensagem_green = txt.readlines()
                        
                        for canal in canais:
                            bot.reply_to(globals()[f'sinal_{canal}'], mensagem_green[37].replace('\n','').replace('[RESULTADO]', ' | '.join(resultados)), parse_mode='HTML')

                        
                        #if canal_free != '':
                        #    bot.reply_to(message_canal_free, mensagem_green[37].replace('\n','').replace('[RESULTADO]', ' | '.join(resultados)), parse_mode='HTML')
                        #    #bot.edit_message_text(table_sinal+"\n============================== \n"+mensagem_green[37].replace('\n','').replace('[RESULTADO]', str(resultados)), message_canal_free.sender_chat.id, message_canal_free.message_id, parse_mode='HTML', disable_web_page_preview=True)   
                        #    
                        #if canal_vip != '':
                        #    bot.reply_to(message_canal_vip, mensagem_green[37].replace('\n','').replace('[RESULTADO]', ' | '.join(resultados)), parse_mode='HTML')
                        #    #bot.edit_message_text(table_sinal+"\n============================== \n"+mensagem_green[37].replace('\n','').replace('[RESULTADO]', str(resultados)), message_canal_vip.sender_chat.id, message_canal_vip.message_id, parse_mode='HTML', disable_web_page_preview=True)   
                            
                    except:
                        pass
                    

                    print('==================================================')
                    validador_sinal = 0
                    contador_cash = 0
                    contador_passagem = 0
                    dicionario_roletas[nome_cassino] = lista_resultados_sinal
                    return

            

                else:
                    print('LOSSS')
                    print('==================================================')
                    contador_cash+=1
                    lista_proximo_resultados = lista_resultados_sinal
                    continue


        except:
            continue


    if contador_cash == 3:
        print('LOSSS GALE2')
        placar_loss +=1
        stop_loss.append('loss')
        
        # editando mensagem e enviando sticker
        try:
            
            ''' Lendo o arquivo txt config-mensagens '''
            txt = open("config-mensagens.txt", "r", encoding="utf-8")
            mensagem_green = txt.readlines()

            for canal in canais:
                bot.reply_to(globals()[f'sinal_{canal}'], mensagem_green[39].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(resultados)), parse_mode = 'HTML')

            
            #if canal_free !='':
            #    bot.reply_to(message_canal_free, mensagem_green[39].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(resultados)), parse_mode = 'HTML')
            #    #bot.edit_message_text(table_sinal+"\n============================== \n"+mensagem_green[39].replace('\n','').replace('[LISTA_RESULTADOS]', str(resultados)), message_canal_free.sender_chat.id, message_canal_free.message_id, parse_mode='HTML', disable_web_page_preview=True)
            #   
#
            #if canal_vip !='':
            #    bot.reply_to(message_canal_vip, mensagem_green[39].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(resultados)), parse_mode='HTML')
            #    #bot.edit_message_text(table_sinal+"\n============================== \n"+mensagem_green[39].replace('\n','').replace('[LISTA_RESULTADOS]', str(resultados)), message_canal_vip.sender_chat.id, message_canal_vip.message_id, parse_mode='HTML', disable_web_page_preview=True)
               

            # Preenchendo relatório
            resultados_sinais = placar_win + placar_loss
            print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
        
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
        


        #if stop_loss.count('loss') == 2:
        #    try:
        #    
        #        if canal_free !='':
        #            bot.send_message(canal_free, f'⛔🛑 Alunos,\nMercado instável! Aguardem a normalização do mesmo conforme indicamos no curso 📚.\n\nAtt, Diretoria Nivus Tips 🤝 ')
    
        #        if canal_vip !='':
        #            bot.send_message(canal_vip, f'⛔🛑 Alunos,\nMercado instável! Aguardem a normalização do mesmo conforme indicamos no curso 📚.\n\nAtt, Diretoria Nivus Tips 🤝 ')
    
        #        stop_loss = []
        #        print('STOP LOSS - ANÁLISE VOLTARÁ EM 30 MINUTOS \n\n')
        #        time.sleep(1800)
    
        #    except:
        #        pass


        print('==================================================')
        validador_sinal = 0
        contador_cash = 0
        contador_passagem = 0
        dicionario_roletas[nome_cassino] = lista_resultados_sinal
        return




inicio()       # Difinição do webBrowser
logarSite()    # Logando no Site
nomeDosCassinos() # Mapeando nome dos cassinos Playtech

#________________________________________________________________________________________ TELEGRAM__________________________________________________________________________________#



print('############################################################# AGUARDANDO COMANDOS #############################################################')

global canais
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
dicionario_roletas = {}



# LENDO TXT PARA DEFINIR VARIAVEL DE CANAIS E VALIDAÇÃO DE USUÁRIO
txt = open("canais.txt", "r", encoding="utf-8")
arquivo = txt.readlines()
usuario = arquivo[2].split(' ')[1]
senha = arquivo[3].split(' ')[1].split('\n')[0]
CHAVE_API = arquivo[7].split(' ')[1].split('\n')[0]

ids = arquivo[11].split(' ')[1].split('\n')[0]
canais = arquivo[12].split(' ')[1].split('\n')[0].split((','))


#try:
#    free = int(arquivo[12].split(' ')[1].split('\n')[0])
#except:
#    free = ''
#try:
#    vip = int(arquivo[13].split(' ')[1].split('\n')[0])
#except:
#    vip = ''


bot = telebot.TeleBot(CHAVE_API)

global message



''' FUNÇÕES BOT ''' ##



def generate_buttons_estrategias(bts_names, markup):
    for button in bts_names:
        markup.add(types.KeyboardButton(button))
    return markup



def pausarBot():
    global parar
    global browser

    while True:
        try:
            parar = 1
            return 

        except:
            continue


@bot.message_handler(commands=['⏲ Ultimos_Resultados'])
def ultimosResultados(message):
    
    if botStatus != 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        bot.reply_to(message, "🤖 Ok! Mostrando Ultimos Resultados das Roletas", reply_markup=markup)
        try:
            
            for key, value in dicionario_roletas.items():
                #print(key, value)
                bot.send_message(message.chat.id, f'{key}{value}')

        except:
            pass
    

    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Ative o bot primeiro! ", reply_markup=markup)




@bot.message_handler(commands=['⚙🧠 Cadastrar_Estratégia'])
def cadastrarEstrategia(message):
    global contador_passagem

    if contador_passagem == 0:
        #Init keyboard markup
        markup_tipo = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
        
        markup_tipo = markup_tipo.add('◀ Voltar', 'REPETIÇÃO', 'AUSÊNCIA')    

        message_tipo_estrategia = bot.reply_to(message, "🤖 Ok! Escolha o tipo de estratégia 👇", reply_markup=markup_tipo)
        bot.register_next_step_handler(message_tipo_estrategia, registrarTipoEstrategia)
    

    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_estrategia = bot.reply_to(message, "🤖⛔ Estou validando uma estratégia! Tente novamente em alguns instanstes.", reply_markup=markup)




@bot.message_handler(commands=['⚙🎰 Cadastrar_Roletas'])
def cadastrarRoletas(message):

    if contador_passagem == 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        
        nomeDosCassinos()
        markup_apostas = generate_buttons_estrategias([f'{roleta.upper()}' for roleta in cassinos], markup)    
        markup_apostas.add('◀ Voltar')

        message_roleta = bot.reply_to(message, "🤖 Ok! Escolha a Roleta que será incluída nas análises 👇. *Lembrando que se iniciar as análises sem nenhuma roleta cadastrada, TODAS as roletas do grupo Evolution serão analisadas.", reply_markup=markup_apostas)
        bot.register_next_step_handler(message_roleta, registrarRoleta)
    

    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_roleta = bot.reply_to(message, "🤖⛔ Estou validando uma estratégia! Tente novamente em alguns instanstes.", reply_markup=markup)





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
        markup_estrategias = generate_buttons_estrategias([f'{estrategia}' for estrategia in estrategias], markup)    
        markup_estrategias.add('◀ Voltar')

        message_excluir_estrategia = bot.reply_to(message, "🤖 Escolha a estratégia a ser excluída 👇", reply_markup=markup_estrategias)
        bot.register_next_step_handler(message_excluir_estrategia, registrarEstrategiaExcluida)
    
    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_excluir_estrategia = bot.reply_to(message, "🤖⛔ Estou validando uma estratégia! Tente novamente em alguns instanstes.", reply_markup=markup)




@bot.message_handler(commands=['🗑🎰 Apagar_Roleta'])
def apagarRoleta(message):
    global estrategia
    global estrategias
    global contador_passagem

    if contador_passagem == 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        #Add to buttons by list with ours generate_buttons function.
        markup_roletas = generate_buttons_estrategias([f'{roletta}' for roletta in lista_roletas], markup)    
        markup_roletas.add('◀ Voltar')

        message_excluir_roleta = bot.reply_to(message, "🤖 Escolha a roleta a ser excluída das análises 👇", reply_markup=markup_roletas)
        bot.register_next_step_handler(message_excluir_roleta, registrarRoletaExcluida)
    
    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_excluir_roleta = bot.reply_to(message, "🤖⛔ Estou validando uma estratégia! Tente novamente em alguns instanstes.", reply_markup=markup)





@bot.message_handler(commands=['🧠📜 Estratégias_Cadastradas'])
def estrategiasCadastradas(message):
    global estrategia
    global estrategias
    global lista_estrategias

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    if lista_estrategias != []:
        bot.reply_to(message, "🤖 Ok! Listando estratégias", reply_markup=markup)

        for estrategia in lista_estrategias:
            #print(estrategia)
            bot.send_message(message.chat.id, f'{estrategia}')
    
    else:
        bot.reply_to(message, "🤖 Nenhuma estratégia cadastrada ❌", reply_markup=markup)




@bot.message_handler(commands=['🎰📜 Roletas_Cadastradas'])
def roletasCadastradas(message):
    global estrategia
    global estrategias
    global lista_roletas

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    if lista_roletas != []:
        bot.reply_to(message, "🤖 Ok! Listando Roletas", reply_markup=markup)

        for roletta in lista_roletas:
            #print(estrategia)
            bot.send_message(message.chat.id, f'{roletta}')
    
    else:
        bot.reply_to(message, "🤖 Nenhuma Roleta cadastrada pelo usuário. Com isso, todas as roletas do grupo Evolution serão analisadas 🚨‼", reply_markup=markup)





@bot.message_handler(commands=['📈 Gestão'])
def gestao(message):
    global placar
    global resultados_sinais
    global placar_estrategias

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

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
    markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    try:
        placar = bot.reply_to(message,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", reply_markup=markup)
    except Exception as a:
        logger.error('Exception ocorrido no ' + repr(a))
        placar = bot.reply_to(message,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%", reply_markup=markup)




@bot.message_handler(commands=['🛑 Pausar_bot'])
def pausar(message):
    global botStatus
    global validador_sinal
    global browser
    global parar

    if validador_sinal != 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Estou validando um Sinal. Tente novamente em alguns instanstes.", reply_markup=markup)

    elif botStatus == 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Bot já está pausado ", reply_markup=markup)

    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

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
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message, "🤖 Bot de Roletas Playtech Iniciado! ✅ Escolha uma opção 👇",
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
            markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖⛔ Bot já está ativado",
                                reply_markup=markup)

        
        elif estrategias == []:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖⛔ Cadastre no mínimo 1 estratégia antes de iniciar",
                                reply_markup=markup)

        
        else:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖 Ok! Bot Ativado com sucesso! ✅ Em breve receberá sinais nos canais informados no arquivo auxiliar! ",
                                    reply_markup=markup)
            
            botStatus = 1
            reladiarioenviado = 0
            parar=0
            contador_passagem = 0
            stop_loss = []

            print('##################################################  INICIANDO AS ANÁLISES  ##################################################')
            print()

            coletarResultados(lista_roletas) # Analisando os Dados
       

    
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


    if message_opcoes.text in ['⚙🎰 Cadastrar Roletas']:
        print('Cadastrar Roletas')
        cadastrarRoletas(message_opcoes)


    if message_opcoes.text in ['🎰📜 Roletas Cadastradas']:
        print('Roletas Cadastradas')
        roletasCadastradas(message_opcoes)   


    if message_opcoes.text in ['🗑🎰 Apagar Roleta']:
        print('Apagar Roleta')
        apagarRoleta(message_opcoes)





#@bot.message_handler(content_types=['text'])
#def escolher_canal(message_canal):
#    global canal_free
#    global canal_vip
#    global placar
#    global estrategia
#    global stop_loss
#    global botStatus
#    global parar
#    global reladiarioenviado
#    global contador_outra_oportunidade
#    global browser
#    global dicionario_estrategia_usuario
#    global contador_passagem
#
#
#    if message_canal.text in ['◀ Voltar']:
#        #Init keyboard markup
#        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
#        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')
#
#        message_opcoes = bot.reply_to(message_canal, "🤖 Escolha uma opção 👇",
#                                reply_markup=markup)
#        return
#
#
#    if message_canal.text in ['📋 Enviar sinais Canal FREE']:
#
#        #Init keyboard markup
#        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
#        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')
#
#        message_final = bot.reply_to(message_canal, "🤖 Ok! Ligando Bot no Canal "+ str(message_canal.text.split(' ')[4:]), reply_markup = markup)
#        
#        print("Iniciar e enviar sinais no Canal FREE ")
#
#
#        canal_free = free
#        canal_vip = ''
#        stop_loss = []
#        botStatus = 1
#        reladiarioenviado = 0
#        parar=0
#        contador_passagem = 0
#
#
#        #placar = bot.send_message(message_canal.chat.id,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%")
#
#        print('#########################  INICIANDO AS ANÁLISES  #########################')
#        print()
#
#        ''' Verifica se estálogado, se n tiver, realiza o login '''
#        if browser.find_elements_by_xpath('//*[@id="username"]'):
#            logarSite()
#
#        coletarResultados(lista_roletas) # Analisando os Dados
#       
#    
#    if message_canal.text in ['🏆 Enviar sinais Canal VIP']:
#        
#        #Init keyboard markup
#        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
#        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')
#
#        message_final = bot.reply_to(message_canal, "🤖 Ok! Ligando Bot no Canal "+ str(message_canal.text.split(' ')[4:]), reply_markup = markup)
#
#        print("Iniciar e enviar sinais no Canal VIP ")
#
#        canal_free = ''
#        canal_vip = vip
#        stop_loss = []
#        botStatus = 1
#        reladiarioenviado = 0
#        contador_outra_oportunidade = 0
#        parar=0
#        contador_passagem = 0
#
#        #placar = bot.send_message(message_canal.chat.id,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%")
#
#        print('#########################  INICIANDO AS ANÁLISES  #########################')
#        print()
#
#        ''' Verifica se estálogado, se n tiver, realiza o login '''
#        if browser.find_elements_by_xpath('//*[@id="username"]'):
#            logarSite()
#
#        coletarResultados(lista_roletas) # Analisando os Dados
#       
#      
#
#    if message_canal.text in ['📋🏆 Enviar sinais Canal FREE & VIP']:
#        
#        #Init keyboard markup
#        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
#        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')
#
#        message_final = bot.reply_to(message_canal, "🤖 Ok! Ligando Bot no Canal "+ str(message_canal.text.split(' ')[4:]), reply_markup = markup)
#        print("Iniciar e enviar sinais no Canal FREE & VIP ")
#
#        canal_free = free
#        canal_vip = vip
#        stop_loss = []
#        botStatus = 1
#        reladiarioenviado = 0
#        contador_outra_oportunidade = 0
#        parar=0
#        contador_passagem = 0
#
#        #placar = bot.send_message(message_canal.chat.id,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%")
#
#        print('#########################  INICIANDO AS ANÁLISES  #########################')
#        print()
#
#        ''' Verifica se estálogado, se n tiver, realiza o login '''
#        if browser.find_elements_by_xpath('//*[@id="username"]'):
#            logarSite()
#
#        coletarResultados(lista_roletas) # Analisando os Dados
       




@bot.message_handler()
def registrarTipoEstrategia(message_tipo_estrategia):
    global resposta_usuario

    if message_tipo_estrategia.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_tipo_estrategia, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        return

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
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

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
    markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

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
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_excluir_estrategia, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        
        return
    

    estrategia_excluir = message_excluir_estrategia.text
    
    ''' Excluindo a estratégia '''
    for estrategia in estrategias:
        if estrategia_excluir == str(estrategia):
            estrategias.remove(estrategia)

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
    markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    bot.reply_to(message_excluir_estrategia, "🤖 Estratégia excluída com sucesso! ✅", reply_markup=markup)




def registrarRoleta(message_roleta):
    global lista_roletas
    global placar_roletas_diaria


    if message_roleta.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_roleta, "🤖 Escolha uma opção 👇", reply_markup=markup)
        return


    ''' Validando se já existe a estrategia cadastrada '''
    if message_roleta.text not in lista_roletas:

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')


        roleta_escolhida = message_roleta.text.lower()

        ''' Placar da Roleta '''
        placar_roleta = list([message_roleta.text])
        placar_roleta.extend([0,0,0,0,0])
        
        # Adicionando estratégia na lista de estratégias
        lista_roletas.append(message_roleta.text)
        placar_roletas.append(placar_roleta)

        # Acumulando estratégia do dia
        roletas_diaria.append(message_roleta.text)
        placar_roletas_diaria.append(placar_roleta)

        bot.reply_to(message_roleta, "🤖 Roleta Cadastrada ✅", reply_markup=markup)

       

    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        bot.reply_to(message_roleta, "🤖 A estratégia "+str(message_roleta.text.upper())+" já foi cadastrada anteriormente ❌", reply_markup=markup)




def registrarRoletaExcluida(message_excluir_roleta):
    global estrategia
    global estrategias

    if message_excluir_roleta.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_excluir_roleta, "🤖 Escolha uma opção 👇", reply_markup=markup)
        return
        
    
    else:

        escolha_usuario = message_excluir_roleta.text
        
        ''' Excluindo a roleta '''
        for roletta in lista_roletas:
            if escolha_usuario == str(roletta):
                lista_roletas.remove(roletta)

        ''' Excluindo o placar da roleta'''
        for pr in placar_roletas:
            if escolha_usuario == pr[0]:
                placar_roletas.remove(pr)

        

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        bot.reply_to(message_excluir_roleta, "🤖 Roleta excluída com sucesso! ✅", reply_markup=markup)





bot.infinity_polling()













