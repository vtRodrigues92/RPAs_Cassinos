from selenium import webdriver
import time
import warnings
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import telebot
from telegram.ext import *
from telebot import *
import logging
import os, ast
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


print()
print('                                #################################################################')
print('                                ######### BOT ROLETAS PRAGMATIC & EVOLUTION & PLAYTECH ##########')
print('                                #################################################################')
print('                                ##################### SEJA BEM VINDO ############################')
print('                                #################################################################')
print('                                ############# DESENVOLVIDO POR VICTOR RODRIGUES #################')
print('                                #################################################################\n')
print('Versão = 1.0.0')
print('Ambiente: Produção\n\n\n')

parar = 0
lista_roletas = []



def auto_refresh():
    global horario_inicio

    data_atual = datetime.now().date().strftime('%d/%m/%Y')
    horario_atual = datetime.today().strftime('%H:%M')
    tres_hora = timedelta(hours=1)
    horario_mais_tres = horario_inicio + tres_hora
    horario_refresh = horario_mais_tres.strftime('%H:%M')

    if horario_atual >= horario_refresh and data_atual == horario_mais_tres.date().strftime('%d/%m/%Y'):
        print('HORA DE REFRESHAR A PAGINA!!!!')
        logarSite()
        time.sleep(10)
        horario_inicio = datetime.now()


# PLACAR
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
        txt = open("arquivos_txt\\canais.txt", "r", encoding="utf-8")
        arquivo = txt.readlines()
        canais = arquivo[12].split(' ')[1].split('\n')[0].split((','))
        
        ''' Enviando mensagem Telegram '''
        try:
            for canal in canais:
                try:
                    globals()[f'placar_{canal}'] = bot.send_message(canal,\
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

    

    # ZERANDO PLACAR E ATUALIZANDO A LISTA DE ESTRATEGIAS DIARIAS
    # Resetando placar Geral (placar geral) e lista de estratégia diária
    #placar_win = 0
    #placar_semGale= 0
    #placar_gale1= 0
    #placar_gale2= 0
    #placar_gale3= 0
    #placar_loss = 0
    #placar_estrategias_diaria = []
    #roletas_diaria = []
    #placar_roletas_diaria = []

    ''' ESTRATEGIAS'''
    # Resetando placar das estrategias (Gestão)
    #for pe in placar_estrategias:
    #    pe[-5], pe[-4], pe[-3], pe[-2], pe[-1] = 0,0,0,0,0
    #    assertividade = '0%'
    #    placar_estrategias_diaria.append(pe) # Atualizando o placar das estratégias diária


    # Atualizando as estratégias diárias com as estratégias atuais
    #for e in estrategias:
    #    estrategias_diaria.append(e)

    ''' ROLETAS '''


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


def resgatar_historico(nome_roleta):
    global historico_roleta
    global resultado

    while True:
        try:
            ''' Elemento das roletas e historico de resultados '''
            roletas = browser.find_elements_by_xpath('//*[@class="lobby-table "]')

            if roletas == []:
                logarSite()
                continue

            else:
                pass

            ''' Percorrendo as roletas com historico'''
            for roulette in roletas:
                if roulette.text.split('\n')[-2] == nome_roleta:
                    #COLETANDO INFORMAÇÕES
                    #Historico de resultados da Roleta
                    if nome_fornecedor == 'pragmatic':

                        historico_roleta = formatar_resultados_pragmatic(roulette) # Formata o historico em lista

                    else:
                        historico_roleta = formatar_resultados_evolution(roulette) # Formata o historico em lista

                    return historico_roleta, roulette

        
        except:
            pass


def apostas():
    global opcoes_apostas

    opcoes_apostas = {

            '1ª coluna': ['1', '4', '7', '10', '13', '16', '19', '22', '25', '28', '31', '34'],
            '2ª coluna': ['2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32', '35'],
            '3ª coluna': ['3', '6', '9', '12', '15', '18', '21', '24', '27', '30', '33', '36'],

            '1ª duzia': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
            '2ª duzia': ['13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'],
            '3ª duzia': ['25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36'],

            'Cor vermelho': ['1', '3', '5', '7', '9', '12', '14', '16', '18', '19', '21', '23', '25', '27', '30', '32', '34', '36'],
            'Cor preto': ['2', '4', '6', '8', '10', '11', '13', '15', '17', '20', '22', '24', '26', '28', '29', '31', '33', '35'],

            'Números par(es)': ['2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24', '26', '28', '30', '32', '34', '36'],
            'Números impar(es)': ['1', '3', '5', '7', '9', '11', '13', '15', '17', '19', '21', '23', '25', '27', '29', '31', '33', '35'],

            'Números baixos': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18'],
            'Números altos': ['19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36'],
            
            '1ª/2ª coluna': ['1', '4', '7', '10', '13', '16', '19', '22', '25', '28', '31', '34', '2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32', '35'],
            '2ª/3ª coluna': ['2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32', '35', '3', '6', '9', '12', '15', '18', '21', '24', '27', '30', '33', '36'],
            '1ª/3ª coluna': ['1', '4', '7', '10', '13', '16', '19', '22', '25', '28', '31', '34', '3', '6', '9', '12', '15', '18', '21', '24', '27', '30', '33', '36'],

            '1ª/2ª duzia': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'],
            '2ª/3ª duzia': ['13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36'],
            '1ª/3ª duzia': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36']
        
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
                #print(dic_estrategia_usuario)
        
        return dic_estrategia_usuario
    
    except:
        pass


def formatar_resultados_pragmatic(roleta):  

    lista_resultados = []

    try:

        resultados = roleta.text.split('\n')[5:]
        for numero in resultados:
            if 'x' not in numero:
                lista_resultados.append(numero)
            
        
        return lista_resultados
    
    except:
        pass


def formatar_resultados_evolution(roleta):  

    lista_resultados = []

    try:

        resultados = roleta.text.split('\n')[:-3]
        for numero in resultados:
            if 'x' not in numero and 'Hot' not in numero:
                lista_resultados.append(numero)
            
        
        return lista_resultados
    
    except:
        pass


def formatar_resultados_playtech(roleta):
    
    lista_resultados = []

    try:

        resultados = roleta.text.split('\n')[2:-2]

        for numero in resultados:
            if 'x' not in numero and 'Hot' not in numero:
                lista_resultados.append(numero)
            
        
        return lista_resultados
    
    except:
        pass


def lista_de_roletas(nome_cassino):

    global cassinos
    global nome_link_dos_cassinos

    nome_link_dos_cassinos = [
        
        ('playtech', 'Roleta Brasileira',  'https://br.betano.com/casino/live/games/roleta-brasileira/444/tables/103910/'),
        ('playtech', 'Mega Fire Blaze Roulette Live',  'https://br.betano.com/casino/live/games/mega-fire-blaze-roulette-live/3744/tables/104310/'),
        ('playtech', 'Who Wants To Be a Millionaire? Roulette',  'https://br.betano.com/casino/live/games/who-wants-to-be-a-millionaire-roulette/4905/tables/105792/'),
        ('playtech', 'Football Roulette', 'https://br.betano.com/casino/live/games/football-roulette/3191/tables/103496/'),
        ('playtech', 'Quantum Roulette Live',  'https://br.betano.com/casino/live/games/quantum-roulette-live/1389/tables/101946/'),
        ('playtech', 'Age Of The Gods Bonus Roulette',  'https://br.betano.com/casino/live/games/age-of-the-gods-bonus-roulette/2190/tables/103533/'),
        ('playtech', 'x1000 Quantum Roulette',  'https://br.betano.com/casino/live/games/x1000-quantum-roulette/6971/tables/106112/'),
        ('playtech', 'Auto Roulette 2',  'https://br.betano.com/casino/live/games/auto-roulette-2/444/tables/107175/'),
        ('playtech', 'Speed Roulette',  'https://br.betano.com/casino/live/games/speed-roulette/444/tables/8/'),
        ('playtech', 'Bucharest Quantum Roulette',  'https://br.betano.com/casino/live/games/bucharest-quantum-roulette/1389/tables/103087/'),
        ('playtech', 'Bucharest French Roulette',  'https://br.betano.com/casino/live/games/bucharest-french-roulette/443/tables/422/'),
        ('playtech', 'Roulette', 'https://br.betano.com/casino/live/games/roulette/444/tables/1642/'),
        ('playtech', 'Greek Quantum Roulette',  'https://br.betano.com/casino/live/games/greek-quantum-roulette/1389/tables/104450/'),
        ('playtech', 'American Roulette',  'https://br.betano.com/casino/live/games/american-roulette/527/tables/101342/'),
        ('playtech', 'UK Roulette',  'https://br.betano.com/casino/live/games/uk-roulette/444/tables/403/'),
        ('playtech', 'Greek Roulette',  'https://br.betano.com/casino/live/games/greek-roulette/444/tables/103912/'),
        ('playtech', 'Roulette Italiana',  'https://br.betano.com/casino/live/games/roulette-italiana/444/tables/101/'),
        ('playtech', 'Prestige Roulette',  'https://br.betano.com/casino/live/games/prestige-roulette/444/tables/441/'),
        ('playtech', 'Deutsches Roulette',  'https://br.betano.com/casino/live/games/deutsches-roulette/444/tables/221/'),
        ('playtech', 'Bucharest Roulette',  'https://br.betano.com/casino/live/games/bucharest-roulette/444/tables/421/'),
        ('playtech', 'Auto Roulette',  'https://br.betano.com/casino/live/games/auto-roulette/444/tables/106252/'),
        ('playtech', 'Speed Auto Roulette',  'https://br.betano.com/casino/live/games/speed-auto-roulette/444/tables/106253/'),


        ('pragmatic', 'PowerUp Roulette', 'https://br.betano.com/casino/live/games/powerup-roulette/8193/tables/'),
        ('pragmatic', 'Mega Roulette',  'https://br.betano.com/casino/live/games/mega-roulette/3523/tables/'),
        ('pragmatic', 'Roulette 10 - Ruby',  'https://br.betano.com/casino/live/games/roulette-10-ruby/5006/tables/'),
        ('pragmatic', 'ROULETTE 14 - SPANISH',  'https://br.betano.com/casino/live/games/roulette-14-spanish/8192/tables/'),
        ('pragmatic', 'Roulette 1 - Azure',  'https://br.betano.com/casino/live/games/roulette-1-azure/3528/tables/'),
        ('pragmatic', 'Roulette 2',  'https://br.betano.com/casino/live/games/roulette-2/3527/tables/'),
        ('pragmatic', 'Auto-Roulette 1',  'https://br.betano.com/casino/live/games/auto-roulette-1/3502/tables/'),
        ('pragmatic', 'Speed Roulette 1',  'https://br.betano.com/casino/live/games/speed-roulette-1/3539/tables/'),
        ('pragmatic', 'Roulette 3 - Macao',  'https://br.betano.com/casino/live/games/roulette-3-macao/3531/tables/'),
        ('pragmatic', 'Roulette 5 - German',  'https://br.betano.com/casino/live/games/roulette-5-german/3529/tables/'),
        ('pragmatic', 'Roulette 6 - Turkish',  'https://br.betano.com/casino/live/games/roulette-6-turkish/3533/tables/'),
        ('pragmatic', 'SPEED ROULETTE 2',  'https://br.betano.com/casino/live/games/speed-roulette-2/8292/tables/'),
        ('pragmatic', 'Roulette 7 - Italian',  'https://br.betano.com/casino/live/games/roulette-7-italian/3530/tables/'),
        ('pragmatic', 'Roulette 4 - Russian',  'https://br.betano.com/casino/live/games/roulette-4-russian/3532/tables/'),
        ('pragmatic', 'Roulette 8 - Indian',  'https://br.betano.com/casino/live/games/roulette-8-indian/4398/tables/'),


        ('evolution', 'Lightning Roulette',  'https://br.betano.com/casino/live/games/lightning-roulette/1524/tables/'),
        ('evolution', 'Immersive Roulette',  'https://br.betano.com/casino/live/games/immersive-roulette/1527/tables/'),
        ('evolution', 'Roleta ao Vivo',  'https://br.betano.com/casino/live/games/roleta-ao-vivo/7899/tables/'),
        ('evolution', 'Roulette',  'https://br.betano.com/casino/live/games/roulette/1526/tables/'),
        ('evolution', 'Speed Roulette', 'https://br.betano.com/casino/live/games/speed-roulette/1530/tables/'),
        ('evolution', 'Speed Auto Roulette',  'https://br.betano.com/casino/live/games/speed-auto-roulette/1538/tables/'),
        ('evolution', 'Bucharest Roulette',  'https://br.betano.com/casino/live/games/bucharest-roulette/1543tables/'),
        ('evolution', 'American Roulette',  'https://br.betano.com/casino/live/games/american-roulette/1536/tables/'),
        ('evolution', 'Casino Malta Roulette', 'https://br.betano.com/casino/live/games/casino-malta-roulette/1542/tables/'),
        ('evolution', 'Turkce Rulet',  'https://br.betano.com/casino/live/games/turkce-rulet/1699/tables/'),
        ('evolution', 'VIP Roulette',  'https://br.betano.com/casino/live/games/vip-roulette/1532/tables/'),
        ('evolution', 'Deutsches Roulette',  'https://br.betano.com/casino/live/games/deutsches-roulette/1698/tables/'),
        ('evolution', 'Auto-Roulette VIP',  'https://br.betano.com/casino/live/games/auto-roulette-vip/1539/tables/'),
        ('evolution', 'Double Ball Roulette',  'https://br.betano.com/casino/live/games/double-ball-roulette/1537/tables/'),
        ('evolution', 'Auto-Roulette',  'https://br.betano.com/casino/live/games/auto-roulette/1529/tables/'),
        ('evolution', 'French Roulette Gold',  'https://br.betano.com/casino/live/games/french-roulette-gold/1981/tables/'),
        ('evolution', 'Auto-Roulette La Partage',  'https://br.betano.com/casino/live/games/auto-roulette-la-partage/1540/tables/')
    
    
        ]
    
    
    for roletaaa in nome_link_dos_cassinos:
        if roletaaa[1] == nome_cassino:
            return roletaaa[2]


def nomeDosCassinos():
    global cassinos
    global nome_dos_cassinos

    nome_dos_cassinos = [
        
        ('Roleta Brasileira'),
        ('Mega Fire Blaze Roulette Live'),
        ('Who Wants To Be a Millionaire? Roulette'),
        ('Football Roulette'),
        ('Quantum Roulette Live'),
        ('Age Of The Gods Bonus Roulette'),
        ('x1000 Quantum Roulette'),
        ('Auto Roulette 2'),
        ('Speed Roulette'),
        ('Bucharest Quantum Roulette'),
        ('Bucharest French Roulette'),
        ('Roulette'),
        ('Greek Quantum Roulette'),
        ('American Roulette'),
        ('UK Roulette'),
        ('Greek Roulette'),
        ('Roulette Italiana'),
        ('Prestige Roulette'),
        ('Deutsches Roulette'),
        ('Bucharest Roulette'),
        ('Auto Roulette'),
        ('Speed Auto Roulette'),

        ('PowerUp Roulette'),
        ('Mega Roulette'),
        ('Roulette 10 - Ruby'),
        ('ROULETTE 14 - SPANISH'),
        ('Roulette 1 - Azure'),
        ('Roulette 2'),
        ('Auto-Roulette 1'),
        ('Speed Roulette 1'),
        ('Roulette 3 - Macao'),
        ('Roulette 5 - German'),
        ('Roulette 6 - Turkish'),
        ('Speed Roulette 2'),
        ('Roulette 7 - Italian'),
        ('Roulette 4 - Russian'),
        ('Roulette 8 - Indian'),


        ('Lightning Roulette'),
        ('Immersive Roulette'),
        ('Roleta ao Vivo'),
        ('Roulette'),
        ('Speed Roulette'),
        ('Speed Auto Roulette'),
        ('Bucharest Roulette'),
        ('American Roulette'),
        ('Casino Malta Roulette'),
        ('Turkce Rulet'),
        ('VIP Roulette'),
        ('Deutsches Roulette'),
        ('Auto-Roulette VIP'),
        ('Double Ball Roulette'),
        ('Auto-Roulette'),
        ('French Roulette Gold'),
        ('Auto-Roulette La Partage')
    
        ]
    

def inicio():
    global browser
    global lobby_cassinos
    global logger
    global horario_inicio
    global lista_anterioR

    lista_anterior = []
    horario_inicio = datetime.now()
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

    browser = webdriver.Chrome(ChromeDriverManager(version='114.0.5735.90').install(),chrome_options=chrome_options)


def logarSite():

    browser.get('https://www.esportiva.bet/#/game/casinolive')
    try:
        browser.maximize_window()
    except:
        pass
    
    time.sleep(10)
    ''' Inserindo login e senha '''
    ''' Lendo o arquivo txt config-mensagens '''
    txt = open('arquivos_txt\\canais.txt', "r", encoding="utf-8")
    mensagem_login = txt.readlines()
    usuario = mensagem_login[2].replace('\n','').split('= ')[1] 
    senha = mensagem_login[3].replace('\n','').split('= ')[1]


    a=1
    while a < 10:
        try:
            ''' Mapeando elementos para inserir credenciais '''
            browser.find_element_by_link_text('Login').click()                                                                                  #Clicando no botão Entrar
            time.sleep(4)
            browser.find_element_by_xpath('/html/body/modal-dialog[1]/div/div/div/div/div[2]/form[1]/input[1]').send_keys(usuario)              #Inserindo login
            browser.find_element_by_xpath('/html/body/modal-dialog[1]/div/div/div/div/div[2]/form[1]/input[2]').send_keys(senha)                #Inserindo senha
            browser.find_element_by_xpath('/html/body/modal-dialog[1]/div/div/div/div/div[2]/form[1]/div[2]/button').click()                    #Clicando no btn login
            time.sleep(5)
            break

        except:
            a+=1
            time.sleep(3)
            break

    ''' Verificando se o login foi feito com sucesso'''
    t3 = 0
    while t3 < 20:
        if browser.find_elements_by_xpath('//*[@class="ng-tns-c47-1"]') != []:
            break
        else:
            time.sleep(1)
            t3+=1
    

def coletarResultados(lista_roletas):
    global url_cassino
    global dicionario_roletas
    global contador_passagem
    global horario_atual
    global nome_cassino, link_roleta_mobile, link_roleta_desktop, nome_fornecedor, historico_roleta
    
    fornecedor = {'pragmatic':['https://www.esportiva.bet/#/game/casinolive?p=175&t=1&g=32810','//*[@id="ROULETTE"]/*[name()="li"]'], 
                  'evolution':['https://www.esportiva.bet/#/game/casinolive?st=&p=508&t=1&g=10519','//*[@class="GridListItem--b95c7"]'],
                  'playtech':['https://www.esportiva.bet/#/game/casinolive?st=&p=480&t=20&g=playtech:RouletteLobby','//*[@class="lobby-tables__item"]']}

    #fornecedor = {'playtech':['https://www.esportiva.bet/#/game/casinolive?st=&p=480&t=20&g=playtech:RouletteLobby','//*[@class="lobby-tables__item"]']}

    while True:

        for key, value in fornecedor.items():

            # Validando se foi solicitado o stop do BOT
            if parar != 0:
                break
            else:
                pass
            
            # Validando o horario para envio do relatório diário
            validaData()

            # Auto Refresh
            auto_refresh()

            #ENTRANDO NO LOBBY
            browser.get(value[0])
            time.sleep(20)


            #ENTRANDO NO IFRAME 2 PLAYTECH
            if key == 'playtech':
                c=0
                while c < 10:
                    try:
                        iframe3 = browser.find_element_by_xpath('//*[@id="SOSWScriptWdget"]/iframe')
                        browser.switch_to_frame(iframe3)
                        break
                    except:
                        c+=1
                        time.sleep(2)

            if key != 'playtech':
                #ENTRANDO NO IFRAME DO LOBBY
                c=0
                while c < 10:

                    try:
                        iframe = browser.find_element_by_id('iframe')
                        browser.switch_to_frame(iframe)
                        break

                    except:
                        c+=1
                        time.sleep(2)
            
            #ENTRANDO NO IFRAME 2 EVOLUTION
            if key == 'evolution':
                c=0
                while c < 10:
                    try:
                        iframe2 = browser.find_element_by_xpath('/html/body/div[6]/div[2]/iframe')
                        browser.switch_to_frame(iframe2)
                        break

                    except:
                        c+=1
                        time.sleep(2)
            

            try:

                #ROLANDO A RELA PARA BAIXO E PARA CIMA
                try:
                    #ELEMENTO QUALQUER DENTRO DO IFRAME
                    elem = browser.find_element_by_xpath('//*[@id="category-roulette"]/div[1]/div[1]/span')
                    #CLICANDO NO ELEMENTO
                    ActionChains(browser).move_to_element(elem).click().perform()
                    time.sleep(1)

                    #INDO ATÉ O FIM DA TELA
                    ActionChains(browser)\
                    .key_down(Keys.END)\
                    .perform()
                    time.sleep(3)

                    #SUBINDO ATÉ O COMEÇO DA TELA
                    ActionChains(browser)\
                    .key_down(Keys.HOME)\
                    .perform()

                except:
                    pass


                ''' Elemento das roletas e historico de resultados '''
                roletas = browser.find_elements_by_xpath(value[1])

                if roletas == []:
                    continue

                else:
                    pass

                ''' Percorrendo as roletas com historico'''
                for roleta in roletas:
                    
                    #COLETANDO INFORMAÇÕES
                    #Historico de resultados da Roleta
                    if key == 'evolution':
                        historico_roleta = formatar_resultados_evolution(roleta) # Formata o historico em lista
                    elif key == 'pragmatic':
                        historico_roleta = formatar_resultados_pragmatic(roleta) # Formata o historico em lista
                    elif key == 'playtech':
                        historico_roleta = formatar_resultados_playtech(roleta) # Formata o historico em lista

                    #Nome do Cassino
                    try:

                        nome_fornecedor = key
                        nome_cassino = roleta.text.split('\n')[-10] if key == 'pragmatic' else roleta.text.split('\n')[-3] if key == 'evolution' else roleta.text.split('\n')[-2]
                        link_roleta_desktop = lista_de_roletas(nome_cassino)

                    except:
                        pass

                    #nome_cassino = roleta[1].text
                    nomeDosCassinos()

                    # Validando se foi solicitado o stop do BOT
                    if parar != 0:
                        break
                    else:
                        pass

                    ''' Valida se tem algum cassino cadastrado pelo usuário. Se não, analisa todos do grupo '''
                    if lista_roletas == [] and nome_cassino in nome_dos_cassinos:
                        pass
                    
                    elif nome_cassino.upper() in lista_roletas:
                        pass
                    
                    else:
                        continue
                    
                    #try:
                    #    historico_resultados.pop(1)
                    #except:
                    #    pass

                    
                    ''' Verifica se o historico da Roleta já consta no dicionario ** Importante para o botão do Telegran "Ultimos Resultados" '''
                    try:
                        if historico_roleta != dicionario_roletas[nome_cassino] or dicionario_roletas == {}:
                            
                            ### ALIMENTANDO BANCO DE DADOS ###
                            #alimenta_banco_dados(nome_cassino,historico_roleta,dicionario_roletas,'NULL','NULL')
                        
                            dicionario_roletas[nome_cassino] = historico_roleta
                            #print(dicionario_roletas)

                    except:
                        dicionario_roletas[nome_cassino] = historico_roleta
                        
                    
                    
                    print(horario_atual)

                    ''' Chama a função que valida a estratégia para enviar o sinal Telegram'''
                    validarEstrategia(dicionario_roletas, nome_cassino, lista_estrategias, roleta)
                    print('=' * 150)
                    
                
            except:

                logarSite()
                
                continue 
        
        browser.refresh()
        time.sleep(10)


def validarEstrategia(dicionario_roletas, nome_cassino, lista_estrategias, roleta):
    global estrategia
    global contador_passagem
    global lista_resultados_sinal, grupos_estrategia, lista_proximo_resultados, historico_roleta, sequencia_minima

    try:

        for estrategia in lista_estrategias:
            
            # Validando se foi solicitado o stop do BOT
            if parar != 0:
                break
            else:
                pass

            # Validando o horario para envio do relatório diário
            validaData()

            ''' Pegando o tipo de aposta (AUSENCIA OU REPETIÇÃO '''
            tipo_aposta = estrategia[0]

            ''' Pegando os números da aposta externa da estratégia'''
            aposta_externa = apostasExternas(estrategia[1], dic_estrategia_usuario)

            ''' Pegando a sequencia minima da estratégia cadastrada pelo usuário '''
            sequencia_minima = estrategia[2]
            
            print('Analisando a Estrategia --> ', estrategia)
            print('Historico_Roleta --> ', nome_cassino, dicionario_roletas[nome_cassino][:int(sequencia_minima)])

            ''' ANTES DE PASSAR NO VALIDADOR, VERIFICAR SE EXISTE O RESULTADO 0 POIS O 0 QUEBRA A SEQUENCIA'''
            if '0' in dicionario_roletas[nome_cassino][:int(sequencia_minima)] or '00' in dicionario_roletas[nome_cassino][:int(sequencia_minima)]:
                print('Sequencia com resultado 0...Analisando outra estratégia!')
                print('=' * 220)
                continue
            
            else:
                pass

            ''' Verifica se os números da seq minima do historico da roleta está dentro da estratégia '''
            validador = validarEstrategiaAlerta(dicionario_roletas, nome_cassino, aposta_externa, sequencia_minima, estrategia)
            
            ''' Validando se bateu alguma condição'''
            if validador.count('true') == int(sequencia_minima)-1:
                print('IDENTIFICADO PRÉ PADRÃO NA ROLETA ', nome_cassino, ' COM A ESTRATÉGIA ', estrategia)
                print('ENVIAR ALERTA')
                enviarAlertaTelegram(dicionario_roletas, nome_cassino, sequencia_minima, nome_fornecedor)
                time.sleep(1)

                ''' Verifica se a ultima condição bate com a estratégia para enviar sinal Telegram '''
                while True:
                    try:
                        # VALIDAR SE FOI DESCONECTADO
                        if browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[6]/div/div[2]/div[2]/button') or browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[5]/div/div[2]/div/div[3]/button'):
                            browser.refresh()
                            logarSite()
                            continue

                        validaData()
 
                        ''' PEGANDO NOVOS RESULTADOS '''
                        if nome_fornecedor == 'evolution':
                            lista_proximo_resultados = formatar_resultados_evolution(roleta) # Formata o historico em lista
                        elif nome_fornecedor == 'pragmatic':
                            lista_proximo_resultados = formatar_resultados_pragmatic(roleta) # Formata o historico em lista
                        elif nome_fornecedor == 'playtech':
                            lista_proximo_resultados = formatar_resultados_playtech(roleta) # Formata o historico em lista
                            
                        print(lista_proximo_resultados)

                        if lista_proximo_resultados == None or lista_proximo_resultados == [] or lista_proximo_resultados == '':
                            print('APAGA SINAL DE ALERTA')
                            apagaAlertaTelegram()
                            print('=' * 220)
                            dicionario_roletas[nome_cassino] = lista_proximo_resultados
                            break

                        '''Valida novamente se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta '''
                        if historico_roleta[:int(sequencia_minima)] != lista_proximo_resultados[:int(sequencia_minima)]:
                        
                            print('Resultado antes do alerta -->', nome_cassino, historico_roleta[:int(sequencia_minima)])
                            print('Resultado apos o alerta  --> ', nome_cassino, lista_proximo_resultados[:int(sequencia_minima)])

                            if estrategia[0] == 'repetição':
                                ''' Verificando se o ultimo resultado da roleta está dentro da estratégia'''
                                if lista_proximo_resultados[0] in aposta_externa[estrategia[1]]:
                                    dicionario_roletas[nome_cassino] = lista_proximo_resultados
                                    print('ENVIANDO SINAL TELEGRAM')
                                    enviarSinalTelegram(nome_cassino)
                                    print('=' * 220)
                                    checkSinalEnviado(lista_proximo_resultados, nome_cassino, roleta)
                                    time.sleep(1)
                                    break
                                
                                else:
                                    print('APAGA SINAL DE ALERTA')
                                    apagaAlertaTelegram()
                                    print('=' * 220)
                                    dicionario_roletas[nome_cassino] = lista_proximo_resultados
                                    historico_roleta = lista_proximo_resultados
                                    break
                            
                            if estrategia[0] == 'ausência':
                                ''' Verificando se o ultimo resultado da roleta não está dentro da estratégia'''
                                if lista_proximo_resultados[0] not in aposta_externa[estrategia[1]]:
                                    dicionario_roletas[nome_cassino] = lista_proximo_resultados
                                    print('ENVIANDO SINAL TELEGRAM')
                                    enviarSinalTelegram(nome_cassino, sequencia_minima, estrategia, nome_fornecedor)
                                    print('=' * 220)
                                    checkSinalEnviado(lista_proximo_resultados, nome_cassino, roleta)
                                    break
                                
                                else:
                                    print('APAGA SINAL DE ALERTA')
                                    apagaAlertaTelegram()
                                    print('=' * 220)
                                    dicionario_roletas[nome_cassino] = lista_proximo_resultados
                                    historico_roleta = lista_proximo_resultados
                                    break
                    
                    except:
                        print('APAGA SINAL DE ALERTA')
                        apagaAlertaTelegram()
                        print('=' * 220)
                        dicionario_roletas[nome_cassino] = lista_proximo_resultados
                        historico_roleta = lista_proximo_resultados
                        break
        
        else:print('='*100)

                    
    except:
        # VALIDAR SE FOI DESCONECTADO
        if browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[6]/div/div[2]/div[2]/button'):
            browser.refresh()
            logarSite()
            pass

        else:
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


def enviarAlertaTelegram(dicionario_roletas, nome_cassino, sequencia_minima, fornecedor):
    global contador_passagem

    ''' Lendo o arquivo txt canais '''
    txt = open('arquivos_txt\\canais.txt', "r", encoding="utf-8")
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
                
                #Variavel Dinâmica
                globals()[f'alerta_{key}'] = bot.send_message(key, 
                                                                message_alerta.replace('[NOME_FORNECEDOR]', nome_fornecedor.title())
                                                                              .replace('[NOME_CASSINO]',nome_cassino.title())\
                                                                              .replace('[SITE_DESKTOP]', link_roleta_desktop).replace('[SITE_MOBILE]', link_roleta_desktop)
                                                                              .replace('[ESTRATEGIA]', estrategia[0].title()+' de '+estrategia[1].title()), 
                                                                parse_mode='HTML', disable_web_page_preview=True)
            except:
                pass

    except:
        pass

    
def enviarSinalTelegram(nome_cassino):
    global table_sinal

    ''' Lendo o arquivo txt canais '''
    txt = open('arquivos_txt\\canais.txt', "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[12].replace('canais= ','').replace('\n','')
    canais = ast.literal_eval(canais) # Convertendo string em dicionario 

    ''' Enviando mensagem Telegram '''
    try:
        for key,value in canais.items():
            try:
                ''' Lendo o arquivo txt '''
                with open('arquivos_txt\\sinal.txt',"r", encoding="utf-8") as arquivo:
                    message_sinal = arquivo.read()

                bot.delete_message(key, globals()[f'alerta_{key}'].message_id)

                globals()[f'sinal_{key}'] = bot.send_message(key, 
                                                               message_sinal.replace('[NOME_FORNECEDOR]', nome_fornecedor.title())
                                                                          .replace('[ESTRATEGIA]', estrategia[0].title()+' de '+estrategia[1].title())
                                                                          .replace('[APOSTA]', estrategia[-1].title())
                                                                          .replace('[NOME_CASSINO]', f'{nome_fornecedor.title()} - {nome_cassino.title()}')
                                                                          .replace('[SITE_DESKTOP]', link_roleta_desktop).replace('[SITE_MOBILE]', link_roleta_desktop)
                                                                          .replace('[LISTA_RESULTADOS]',  ' | '.join(lista_proximo_resultados[:5]))
                                                                          .replace('[ULTIMO_RESULTADO]', lista_proximo_resultados[0])
                                                                          .replace('[SITE_CADASTRO]', value[0]),
                                                               parse_mode='HTML', disable_web_page_preview=True)
            except:
                pass
    
    except:
        pass


def apagaAlertaTelegram():
    global contador_passagem

    ''' Lendo o arquivo txt canais '''
    txt = open('arquivos_txt\\canais.txt', "r", encoding="utf-8")
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


def checkSinalEnviado(lista_proximo_resultados, nome_cassino, roleta):
    global table
    global message_canal
    global resultados_sinais
    global ultimo_horario_resultado
    global validador_sinal
    global stop_loss
    global estrategia
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


    resultados = []
    contador_cash = 0

    #LENDO ARQUIVO GALE
    with open('arquivos_txt//gale.txt', 'r') as arquivo:
        gale = arquivo.read()
 
    
    while contador_cash <= int(gale):

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass

        # Validando o horario para envio do relatório diário
        validaData()

        try:

            # VALIDAR SE FOI DESCONECTADO
            if browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[6]/div/div[2]/div[2]/button') or browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[5]/div/div[2]/div/div[3]/button'):
                logarSite()
                continue
            
            ''' Lendo novos resultados para validação da estratégia'''
            if nome_fornecedor == 'evolution':
                lista_resultados_sinal = formatar_resultados_evolution(roleta) # Formata o historico em lista
            elif nome_fornecedor == 'pragmatic':
                lista_resultados_sinal = formatar_resultados_pragmatic(roleta) # Formata o historico em lista
            elif nome_fornecedor == 'playtech':
                lista_resultados_sinal = formatar_resultados_playtech(roleta) # Formata o historico em lista
            
            #print(historico_roleta)

            ''' Validando se tem dado Vazio '''
            if '' in lista_resultados_sinal or lista_resultados_sinal == [] or lista_resultados_sinal == None:
                logarSite()


            ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
            if lista_proximo_resultados[:int(sequencia_minima)] != lista_resultados_sinal[:int(sequencia_minima)]:

                print(lista_resultados_sinal[0])
                resultados.append(lista_resultados_sinal[0])
                    
                grupo_apostar = apostasExternas(estrategia[3], dic_estrategia_usuario)

                # VALIDANDO WIN OU LOSS
                if lista_resultados_sinal[0] in grupo_apostar[estrategia[3]] or lista_resultados_sinal[0] == '0' or lista_resultados_sinal[0] == '00':
                
                    # validando o tipo de WIN
                    if contador_cash == 0:
                        print('WIN SEM GALE')
                        stop_loss.append('win')

                        ### ALIMENTANDO BANCO DE DADOS ###
                        #alimenta_banco_dados(nome_cassino, lista_resultados_sinal, dicionario_roletas, estrategia[1], 'SG')
                            

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

                        ### ALIMENTANDO BANCO DE DADOS ###
                        #alimenta_banco_dados(nome_cassino, lista_resultados_sinal, dicionario_roletas, estrategia[1], 'G1')
                        

                        # Atualizando placar e Alimentando o arquivo txt
                        placar_win +=1
                        placar_gale1 +=1
                        placar_geral = placar_win + placar_loss
                        
                        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                            arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}")
                        
                        # Preenchendo relatório
                        #placar_win+=1
                        #placar_gale1+=1
                        #resultados_sinais = placar_win + placar_loss
                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
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
                        
                        ### ALIMENTANDO BANCO DE DADOS ###
                        #alimenta_banco_dados(nome_cassino, lista_resultados_sinal, dicionario_roletas, estrategia[1], 'G2')
                        
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
                                    if pe[:-5] == [estrategia[1].upper()]:
                                        pe[-3] = int(pe[-3])+1
                        except:
                            pass
                        
                        if lista_roletas != []:
                            # Somando Win na roleta atual
                            for pr in placar_roletas:
                                    if pr[:-5] == [nome_cassino.upper()]:
                                        pr[-3] = int(pr[-3])+1


                                        
                    # respondendo a mensagem do sinal e condição para enviar sticker
                    try:
                        ''' Lendo o arquivo txt canais '''
                        txt = open('arquivos_txt\\canais.txt', "r", encoding="utf-8")
                        arquivo = txt.readlines()
                        canais = arquivo[12].replace('canais= ','').replace('\n','')
                        canais = ast.literal_eval(canais) # Convertendo string em dicionario 


                        for key,value in canais.items():
                            try:
                                ''' Lendo o arquivo txt config-mensagens '''
                                with open('arquivos_txt\\green.txt',"r", encoding="utf-8") as arquivo:
                                    message_green = arquivo.read()

                                msg_editada = (f"🔷🔷 Entrada Finalizada 🔷🔷\n\
🎰{nome_cassino}\n\
🕹️{estrategia[0].title()} de {estrategia[1].title()}")

                                bot.edit_message_text(chat_id=globals()[f'sinal_{key}'].chat.id, text=msg_editada, message_id=globals()[f'sinal_{key}'].message_id)
                                bot.reply_to(globals()[f'sinal_{key}'], message_green.replace('[LISTA_RESULTADOS]', ' | '.join(resultados)),
                                                                            parse_mode='HTML')
                            except:
                                pass
                    
                    except:
                        pass

                    
                    

                    print('==================================================')
                    validador_sinal = 0
                    contador_cash = 0
                    contador_passagem = 0
                    dicionario_roletas[nome_cassino] = lista_resultados_sinal
                    with open('arquivos_txt/validador_sinal.txt', 'w') as arquivo:
                        arquivo.write('False')

                    return

            

                else:
                    print('LOSSS')
                    print('==================================================')
                    contador_cash+=1
                    lista_proximo_resultados = lista_resultados_sinal
                    continue


        except Exception as a:
            logger.error('Exception ocorrido no ' + repr(a))
            #logarSite()
            lista_resultados_sinal, roleta = resgatar_historico(nome_cassino)
            continue


    if contador_cash >int(gale):
        
        print('LOSSS GALE2')
        stop_loss.append('loss')

        # Preenchendo arquivo txt
        placar_loss +=1
        placar_geral = placar_win + placar_loss
        
        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                            arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}")
                        
        
        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
            
        # editando mensagem
        try:
            ''' Lendo o arquivo txt canais '''
            txt = open('arquivos_txt\\canais.txt', "r", encoding="utf-8")
            arquivo = txt.readlines()
            canais = arquivo[12].replace('canais= ','').replace('\n','')
            canais = ast.literal_eval(canais) # Convertendo string em dicionario 


            for key,value in canais.items():
                try:
                    
                    ''' Lendo o arquivo txt config-mensagens '''
                    with open('arquivos_txt\\red.txt',"r", encoding="utf-8") as arquivo:
                        message_red = arquivo.read()

                    msg_editada = (f"🔷🔷 Entrada Finalizada 🔷🔷\n\
🎰{nome_cassino}\n\
🕹️{estrategia[0].title()} de {estrategia[1].title()}")

                    bot.edit_message_text(chat_id=globals()[f'sinal_{key}'].chat.id, text=msg_editada, message_id=globals()[f'sinal_{key}'].message_id)
                    bot.reply_to(globals()[f'sinal_{key}'], message_red,
                                        parse_mode = 'HTML')
                    
                except:
                    pass
            
        except:
            pass

        ### ALIMENTANDO BANCO DE DADOS ###
        #alimenta_banco_dados(nome_cassino, lista_resultados_sinal, dicionario_roletas, estrategia[1], 'LOSS')
                        

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
    

        print('='*100)
        validador_sinal = 0
        contador_cash = 0
        contador_passagem = 0
        dicionario_roletas[nome_cassino] = lista_resultados_sinal
        with open('arquivos_txt/validador_sinal.txt', 'w') as arquivo:
            arquivo.write('False')
        
        return




inicio()       # Difinição do webBrowser
logarSite()    # Logando no Site 
placar()       # Chamando o Placar

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


# PLACAR
#placar_win = 0
#placar_semGale= 0
#placar_gale1= 0
#placar_gale2= 0
#placar_gale3= 0
#placar_loss = 0
#resultados_sinais = placar_win + placar_loss
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
txt_estrategias_vazio = ''



# LENDO TXT PARA DEFINIR VARIAVEL DE CANAIS E VALIDAÇÃO DE USUÁRIO
txt = open('arquivos_txt\\canais.txt', "r", encoding="utf-8")
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
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        bot.reply_to(message, "🤖 Ok! Mostrando Ultimos Resultados das Roletas", reply_markup=markup)
        try:
            
            for key, value in dicionario_roletas.items():
                #print(key, value)
                bot.send_message(message.chat.id, f'{key}{value}')

        except:
            pass
    

    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Ative o bot primeiro! ", reply_markup=markup)




@bot.message_handler(commands=['⚙🧠 Cadastrar_Estratégia'])
def cadastrarEstrategia(message):
    global contador_passagem

    if contador_passagem == 0:
        #Init keyboard markup
        markup_tipo = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
        
        markup_tipo = markup_tipo.add('◀ Voltar', 'REPETIÇÃO', 'AUSÊNCIA', 'ESTRATÉGIAS PADRÕES')    

        message_tipo_estrategia = bot.reply_to(message, "🤖 Ok! Escolha o tipo de estratégia 👇", reply_markup=markup_tipo)
        bot.register_next_step_handler(message_tipo_estrategia, registrarTipoEstrategia)
    

    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_estrategia = bot.reply_to(message, "🤖⛔ Estou validando uma estratégia! Tente novamente em alguns instanstes.", reply_markup=markup)




@bot.message_handler(commands=['⚙🎰 Cadastrar_Roletas'])
def cadastrarRoletas(message):
    global contador_passagem

    if contador_passagem == 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        
        nomeDosCassinos()
        markup_apostas = generate_buttons_estrategias([f'{roleta.upper()}' for roleta in nome_dos_cassinos], markup)    
        markup_apostas.add('◀ Voltar')

        message_roleta = bot.reply_to(message, "🤖 Ok! Escolha a Roleta que será incluída nas análises 👇. *Lembrando que se iniciar as análises sem nenhuma roleta cadastrada, TODAS as roletas do grupo Evolution serão analisadas.", reply_markup=markup_apostas)
        bot.register_next_step_handler(message_roleta, registrarRoleta)
    

    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

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
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

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
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_excluir_roleta = bot.reply_to(message, "🤖⛔ Estou validando uma estratégia! Tente novamente em alguns instanstes.", reply_markup=markup)



@bot.message_handler(commands=['🧠📜 Estratégias_Cadastradas'])
def estrategiasCadastradas(message):
    global estrategia
    global estrategias
    global lista_estrategias

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

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
    markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

    if lista_roletas != []:
        bot.reply_to(message, "🤖 Ok! Listando Roletas", reply_markup=markup)

        for roletta in lista_roletas:
            #print(estrategia)
            bot.send_message(message.chat.id, f'{roletta}')
    
    else:
        bot.reply_to(message, "🤖 Nenhuma Roleta cadastrada pelo usuário. Com isso, todas as roletas do grupo Evolution serão analisadas 🚨‼", reply_markup=markup)



@bot.message_handler(commands=['📈 Gestão'])
def gestao(message):

    global resultados_sinais
    global placar_estrategias

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

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

    global resultados_sinais

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

    ''' Enviando mensagem Telegram '''
    try:
        placar()
        
        assertividade = asserividade.replace('\n','').replace(' ','')
        #link_cadastro = open('arquivos_txt/link_cadastro.txt', 'r', encoding='UTF-8').read()

        texto = f"📊 Placar Atual do dia {data_hoje}:\n\
        =====================\n\
        😍 WIN - {str(placar_win)}\n\
        🏆 WIN S/ GALE - {str(placar_semGale)}\n\
        🥇 WIN GALE1 - {str(placar_gale1)}\n\
        🥈 WIN GALE2 - {str(placar_gale2)}\n\
        😭 LOSS - {str(placar_loss)}\n\
        =====================\n\
        🎯 Assertividade {assertividade}"

        resposta = bot.reply_to(message, texto, parse_mode='HTML')
    
    except Exception as a:
        logger.error('Exception ocorrido no ' + repr(a))
        #placar = bot.reply_to(message,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%", reply_markup=markup)
        pass



@bot.message_handler(commands=['🛑 Pausar_bot'])
def pausar(message):
    global botStatus
    global validador_sinal
    global browser
    global parar

    if validador_sinal != 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Estou validando um Sinal. Tente novamente em alguns instanstes.", reply_markup=markup)

    elif botStatus == 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Bot já está pausado ", reply_markup=markup)

    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

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
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message, "🤖 Bot de Roletas Iniciado! ✅ Escolha uma opção 👇",
                                    reply_markup=markup)
        
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(message_opcoes, opcoes)
    
    else:
        message_error = bot.reply_to(message, "🤖 Você não tem permissão para acessar este Bot ❌🚫")




@bot.message_handler()
def opcoes(message_opcoes):

    if message_opcoes.text in ['✅ Ativar Bot']:
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

        print('Ativar Bot')

        if botStatus == 1:

            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖⛔ Bot já está ativado",
                                reply_markup=markup)

        
        elif lista_estrategias == []:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖⛔ Cadastre no mínimo 1 estratégia antes de iniciar",
                                reply_markup=markup)

        
        else:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖 Ok! Bot Ativado com sucesso! ✅ Em breve receberá sinais nos canais informados no arquivo auxiliar! ",
                                    reply_markup=markup)
            
            botStatus = 1
            reladiarioenviado = 0
            parar=0
            contador_passagem = 0
            stop_loss = []

            print('##################################################  INICIANDO AS ANÁLISES  ##################################################')
            print()
            
            ''' Verifica se estálogado, se n tiver, realiza o login '''
            if browser.find_elements_by_xpath('//*[@id="username"]'):
                logarSite()

            nomeDosCassinos()     # Coltando o site dos Cassinos
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




@bot.message_handler()
def registrarTipoEstrategia(message_tipo_estrategia):
    global resposta_usuario

    if message_tipo_estrategia.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_tipo_estrategia, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        return




    if message_tipo_estrategia.text in ['ESTRATÉGIAS PADRÕES']:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')
        
        estrategias_padroes = (['repetição', '1ºcoluna', '3', '2ª/3ªcoluna'], 
                               ['repetição', '2ªcoluna', '3', '1º/3ªcoluna'],
                               ['repetição', '3ªcoluna', '3', '1º/2ªcoluna'], 
                               ['repetição', '1ºduzia', '3', '2ª/3ªduzia'], 
                               ['repetição', '2ªduzia', '3', '1º/3ªduzia'], 
                               ['repetição', '3ªduzia', '3', '1º/2ªduzia'])

        for estrategia_padrao in estrategias_padroes:
            lista_estrategias.append(estrategia_padrao)
            placar_estrategia = [estrategia_padrao[1]]
            placar_estrategia.extend([0,0,0,0,0])
            placar_estrategias.append(placar_estrategia)


        message_aposta = bot.reply_to(message_tipo_estrategia, "🤖 Estratégias Cadastradas ✅", reply_markup=markup)





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
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

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
    markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

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
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

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
    markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

    bot.reply_to(message_excluir_estrategia, "🤖 Estratégia excluída com sucesso! ✅", reply_markup=markup)




def registrarRoleta(message_roleta):
    global lista_roletas
    global placar_roletas_diaria


    if message_roleta.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_roleta, "🤖 Escolha uma opção 👇", reply_markup=markup)
        return


    ''' Validando se já existe a estrategia cadastrada '''
    if message_roleta.text not in lista_roletas:

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')


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
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        bot.reply_to(message_roleta, "🤖 A estratégia "+str(message_roleta.text.upper())+" já foi cadastrada anteriormente ❌", reply_markup=markup)




def registrarRoletaExcluida(message_excluir_roleta):
    global estrategia
    global estrategias

    if message_excluir_roleta.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

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
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        bot.reply_to(message_excluir_roleta, "🤖 Roleta excluída com sucesso! ✅", reply_markup=markup)




bot.infinity_polling()













