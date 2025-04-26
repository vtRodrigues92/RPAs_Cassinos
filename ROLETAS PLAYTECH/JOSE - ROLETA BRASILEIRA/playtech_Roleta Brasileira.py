from selenium import webdriver
import time
import warnings
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import telebot
from telegram.ext import *
from telebot import *
import logging
import os


print()
print('                                #################################################################')
print('                                ##################    BOT ROLETAS PLAYTECH    ###################')
print('                                #################################################################')
print('                                ##################### SEJA BEM VINDO ############################')
print('                                #################################################################')
print('                                ############# DESENVOLVIDO POR VICTOR RODRIGUES #################')
print('                                #################################################################\n')
print('Versão = 2.0.0')
print('Ambiente: Produção\n\n\n')

parar = 0
lista_roletas = []




def auto_refresh():
    global horario_inicio

    horario_atual = datetime.today().strftime('%H:%M')
    data_atual = datetime.now().date().strftime('%d/%m/%Y')
    tres_hora = timedelta(minutes=30)
    #um_dia = timedelta(days=1)
    horario_mais_tres = horario_inicio + tres_hora
    #proximo_dia = data_atual + um_dia
    horario_refresh = horario_mais_tres.strftime('%H:%M')
    #str_proximo_dia = proximo_dia.strftime('%d/%m/%Y')


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
        txt = open("canais.txt", "r", encoding="utf-8")
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


def resgatar_historico(nome_cassino):
    global historico_roleta
    global resultado
    global roleta

    try:
        
        ''' Elemento das roletas e historico de resultados '''
        roletas = browser.find_elements_by_xpath('//*[@class="lobby-tables__item"]')
        for roleta in roletas:
            try:
                if roleta.text.split('\n')[-2] == nome_cassino:
                    #Historico de resultados da Roleta
                    historico_roleta = formatar_resultados(roleta) # Formata o historico em lista    
                    
                    return historico_roleta, roleta
            except:
                continue    
    except:
        pass


def depara_numeros(numero_base):
    global depara

    depara = {

        '0':['1º/3ªduzia','2ª/3ªcoluna'],
        '1':['1º/2ªduzia','1º/3ªcoluna'], 
        '2':['1º/3ªduzia','1º/2ªcoluna'],
        '3':['1º/3ªduzia','1º/3ªcoluna'],
        '4':['2ª/3ªduzia','1º/3ªcoluna'],
        '5':['1º/2ªduzia','2ª/3ªcoluna'],
        '6':['1º/3ªduzia','2ª/3ªcoluna'],
        '7':['1º/2ªduzia','1º/3ªcoluna'],
        '8':['1º/3ªduzia','2ª/3ªcoluna'],
        '9':['2ª/3ªduzia','1º/3ªcoluna'],
        '10':['2ª/3ªduzia','1º/3ªcoluna'],
        '11':['2ª/3ªduzia','2ª/3ªcoluna'],
        '12':['1º/2ªduzia','2ª/3ªcoluna'],
        '13':['2ª/3ªduzia','2ª/3ªcoluna'],
        '14':['2ª/3ªduzia','1º/2ªcoluna'],
        '15':['2ª/3ªduzia','1º/3ªcoluna'],
        '16':['1º/2ªduzia','1º/3ªcoluna'],
        '17':['2ª/3ªduzia','1º/3ªcoluna'],
        '18':['2ª/3ªduzia','2ª/3ªcoluna'],
        '19':['2ª/3ªduzia','2ª/3ªcoluna'],
        '20':['2ª/3ªduzia','1º/2ªcoluna'],
        '21':['1º/2ªduzia','1º/3ªcoluna'],
        '22':['1º/2ªduzia','1º/3ªcoluna'],
        '23':['2ª/3ªduzia','1º/2ªcoluna'],
        '24':['2ª/3ªduzia','1º/2ªcoluna'],
        '25':['2ª/3ªduzia','1º/2ªcoluna'],
        '26':['1º/3ªduzia','1º/2ªcoluna'],
        '27':['2ª/3ªduzia','1º/3ªcoluna'],
        '28':['1º/3ªduzia','1º/3ªcoluna'],
        '29':['2ª/3ªduzia','2ª/3ªcoluna'],
        '30':['2ª/3ªduzia','1º/2ªcoluna'],
        '31':['2ª/3ªduzia','1º/2ªcoluna'],
        '32':['2ª/3ªduzia','1º/2ªcoluna'],
        '33':['1º/3ªduzia','1º/3ªcoluna'],
        '34':['1º/3ªduzia','2ª/3ªcoluna'],
        '35':['2ª/3ªduzia','2ª/3ªcoluna'],
        '36':['1º/3ªduzia','2ª/3ªcoluna'],

    }

    for key,value in depara.items():
        if key == numero_base:
            return value[0], value[1]


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
            'Números impar(es)': ['1', '3', '5', '7', '9', '11', '13', '15', '17', '19', '21', '23', '25', '27', '29', '31', '33', '35'],

            'Números baixos': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18'],
            'Números altos': ['19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36'],
            
            '1º/2ªcoluna': ['1', '4', '7', '10', '13', '16', '19', '22', '25', '28', '31', '34', '2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32', '35'],
            '2ª/3ªcoluna': ['2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32', '35', '3', '6', '9', '12', '15', '18', '21', '24', '27', '30', '33', '36'],
            '1º/3ªcoluna': ['1', '4', '7', '10', '13', '16', '19', '22', '25', '28', '31', '34', '3', '6', '9', '12', '15', '18', '21', '24', '27', '30', '33', '36'],

            '1º/2ªduzia': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'],
            '2ª/3ªduzia': ['13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36'],
            '1º/3ªduzia': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36']
        
        }


def apostasExternas(estrategia_usuario):
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
            'números impar(es)': ['1', '3', '5', '7', '9', '11', '13', '15', '17', '19', '21', '23', '25', '27', '29', '31', '33', '35'],

            'números baixos': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18'],
            'números altos': ['19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36'],

            '1º/2ªcoluna': ['1', '4', '7', '10', '13', '16', '19', '22', '25', '28', '31', '34', '2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32', '35'],
            '2ª/3ªcoluna': ['2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32', '35', '3', '6', '9', '12', '15', '18', '21', '24', '27', '30', '33', '36'],
            '1º/3ªcoluna': ['1', '4', '7', '10', '13', '16', '19', '22', '25', '28', '31', '34', '3', '6', '9', '12', '15', '18', '21', '24', '27', '30', '33', '36'],

            '1º/2ªduzia': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'],
            '2ª/3ªduzia': ['13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36'],
            '1º/3ªduzia': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36']

        }

        for key,value in opcoes_apostas.items():
            if estrategia_usuario == key:
                return value
                #print(dic_estrategia_usuario)
        
    
    except:
        pass


def formatar_resultados(roleta):  

    lista_resultados = []

    try:

        resultados = roleta.text.split('\n')[2:-2]
        for numero in resultados:
            if 'x' not in numero:
                try:
                    if int(numero) or numero == '0' or numero == '00':
                        lista_resultados.append(numero)
                except:
                    continue
        
        return lista_resultados
    
    except:
        pass


def nomeDosCassinos(nome_roleta):
    global cassinos
    global nome_dos_cassinos

    nome_dos_cassinos = [
        
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
        
        ]

    cassinos = [

        ('Age Of The Gods Bonus Roulette', 'https://br.betano.com/casino/live/games/age-of-the-gods-bonus-roulette/2190/tables/103533/'),
        ('American Roulette', 'https://br.betano.com/casino/live/games/american-roulette/527/tables/101342/'),
        ('Auto Roulette', 'https://br.betano.com/casino/live/games/auto-roulette/444/tables/106252/'),
        ('Bucharest Roulette', 'https://br.betano.com/casino/live/games/bucharest-roulette/444/tables/421/'),
        ('Deutsches Roulette', 'https://br.betano.com/casino/live/games/deutsches-roulette/444/tables/221/'),
        ('Football Roulette', 'https://br.betano.com/casino/live/games/football-roulette/3191/tables/103496/'),
        ('French Roulette', ''),
        ('Greek Roulette', 'https://br.betano.com/casino/live/games/greek-roulette/444/tables/103912/'),
        ('Hindi Roulette', ''),
        ('Mega Fire Blaze Roulette Live', 'https://br.betano.com/casino/live/games/mega-fire-blaze-roulette-live/3744/tables/104310/'),
        ('Prestige Roulette', 'https://br.betano.com/casino/live/games/prestige-roulette/444/tables/441/'),
        ('Quantum Roulette Live', 'https://br.betano.com/casino/live/games/quantum-roulette-live/1389/tables/101946/'),
        ('Roleta Brasileira', 'https://br.betano.com/casino/live/games/roleta-brasileira/444/tables/103910/'),
        ('Roulette', 'https://br.betano.com/casino/live/games/roulette/444/tables/1642/'),
        ('Roulette Italiana', 'https://br.betano.com/casino/live/games/roulette-italiana/444/tables/101/'),
        ('Speed Auto Roulette', 'https://br.betano.com/casino/live/games/speed-auto-roulette/444/tables/106253/'),
        ('Speed Roulette', 'https://br.betano.com/casino/live/games/speed-roulette/444/tables/8/'),
        ('Turkish Roulette', ''),
        ('Who Wants To Be a Millionaire? Roulette', 'https://br.betano.com/casino/live/games/who-wants-to-be-a-millionaire-roulette/4905/tables/105792/')

    ]

    try:
        for c in cassinos:
            if c[0] == nome_roleta:
                url_cassino = c[1]
                break
        
        return url_cassino
    except:
        pass


def inicio():
    global browser
    global lobby_cassinos
    global logger
    global horario_inicio

    horario_inicio = datetime.now()

    logger = logging.getLogger()

    lobby_cassinos = 'https://launcher.betfair.com/?gameId=live-roulette-cptl&returnURL=https%3A%2F%2Fcasino.betfair.com%2Fpt-br%2Fp%2Fcassino-ao-vivo&launchProduct=gaming&RPBucket=gaming&mode=real&dataChannel=ecasino&switchedToPopup=true'

    # Definindo opções para o browser
    warnings.filterwarnings("ignore", category=DeprecationWarning) 
    chrome_options = webdriver.ChromeOptions() 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)


def logarSite():
    browser.get(lobby_cassinos)
    try:
        browser.maximize_window()
    except:
        pass

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

    try:
        browser.find_element_by_xpath('//*[@id="username"]').send_keys(usuario) #Inserindo login
        browser.find_element_by_xpath('//*[@id="password"]').send_keys(senha) #Inserindo senha
        browser.find_element_by_xpath('//*[@id="login"]').click() #Clicando no btn login
        time.sleep(10)
    except:
        pass


def coletarResultados(lista_roletas):
    global url_cassino
    global dicionario_roletas
    global contador_passagem
    global horario_atual
    global nome_cassino, historico_roleta


    while True:

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass
        
        # Validando o horario para envio do relatório diário
        validaData()

        # Auto Refresh
        auto_refresh()


        # VALIDAR SE FOI DESCONECTADO
        if browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[6]/div/div[2]/div[2]/button') or browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[5]/div/div[2]/div/div[3]/button'):
            browser.refresh()
            logarSite()
            continue


        try:
            roletas = browser.find_elements_by_xpath('//*[@class="lobby-tables__item"]')
            ''' Elemento do historico de resultados '''
            #historico_resultados = browser.find_elements_by_css_selector('.roulette-history_lobby--DxuTP')
            #lista_resultados = []


            if roletas == []:
                logarSite()
            else:
                pass
        

            ''' Percorrendo as roletas'''
            for roleta in roletas:
            
                #COLETANDO INFORMAÇÕES
                #Nome do Cassino
                try:
                    nome_cassino = roleta.text.split('\n')[-2]
                except:
                    pass
                #URL do Cassino (Se Tiver)
                url_cassino = nomeDosCassinos(nome_cassino)

                # PARA ESSE USUARIO SÓ PASSA SE FOR ROLETA BRASILEIRA
                if nome_cassino == 'Roleta Brasileira':
                    pass
                else:
                    continue


                #Historico de resultados da Roleta
                historico_roleta = formatar_resultados(roleta) # Formata o historico em lista
                

                # Validando se foi solicitado o stop do BOT
                if parar != 0:
                    break
                else:
                    pass

                
                try:
                    if historico_roleta != dicionario_roletas[nome_cassino] or dicionario_roletas == {}:
                        dicionario_roletas[nome_cassino] = historico_roleta
                        #print(dicionario_roletas)
                except:
                    dicionario_roletas[nome_cassino] = historico_roleta
                
                ''' VALIDA SE A LISTA ESTÁ VAZIA '''
                if historico_roleta == []:
                    browser.refresh()
                    logarSite()
                else:
                    pass

                
                ''' Chama a função que valida a estratégia para enviar o sinal Telegram'''
                validarEstrategia(dicionario_roletas, nome_cassino, lista_estrategias, roleta)
                
                print('=' * 150)

                continue
    
        except:

            logarSite()
            continue 


def validarEstrategia(dicionario_roletas, nome_cassino, lista_estrategias, roleta):
    global estrategia
    global contador_passagem
    global lista_resultados_sinal, historico_roleta, penultimo_numero, ultimo_numero, lista_proximo_resultados

    try:
        
        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            return
        else:
            pass

        # Validando o horario para envio do relatório diário
        validaData()

        # VALIDAR SE FOI DESCONECTADO
        if browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[6]/div/div[2]/div[2]/button') or browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[5]/div/div[2]/div/div[3]/button'):
            browser.refresh()
            logarSite()
            return


        ##### VALIDAÇÃO DA ESTRATEGIA #####
        grupo1 = []
        grupo2 = []
        numero_base = dicionario_roletas[nome_cassino][0]
        grupo_numero_base1, grupo_numero_base2 = depara_numeros(numero_base)
        sequencia_minima = ''

        while True:

            try:

                # VALIDAR SE FOI DESCONECTADO
                if browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[6]/div/div[2]/div[2]/button') or browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[5]/div/div[2]/div/div[3]/button'):
                    browser.refresh()
                    logarSite()
                    continue

                validaData()
                auto_refresh()

                ''' PEGANDO NOVOS RESULTADOS '''
                lista_proximo_resultados = formatar_resultados(roleta) # Formata o historico em lista
                
                ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
                if historico_roleta[:3] != lista_proximo_resultados[:3]:
                    
                    ## SAINDO ZERO, REINICIA A ANALISE DA ESTRATEGIA
                    if lista_proximo_resultados[0] == '0' or lista_proximo_resultados[0] == '00':
                        break

                    numeros_validacao1 = apostasExternas(grupo_numero_base1)
                    numeros_validacao2 = apostasExternas(grupo_numero_base2)

                    if lista_proximo_resultados[0] not in numeros_validacao1:
                        grupo1.append('true')
                    else:
                        grupo1.append('false')
                    
                    if lista_proximo_resultados[0] not in numeros_validacao2:
                        grupo2.append('true')
                    else:
                        grupo2.append('false')
                    
                    print(horario_atual)
                    print(f'Resultado - {lista_proximo_resultados[0]}\n\
Número Base - {numero_base}\n\
grupo1 ------ {grupo_numero_base1}\n\
grupo2 ------ {grupo_numero_base2}\n\
valida Grupo1 {grupo1}\n\
valida Grupo2 {grupo2}'
    )
                    print('='*100)
                    
                    if 'false' not in grupo1 or 'false' not in grupo2:

                        #### VERIFICANDO SE CHEGOU O MOMENTO DE ENVIAR O ALERTA
                        if grupo1.count('true') == 2 and 'false' not in grupo1:
                            print('ENVIAR ALERTA')
                            enviarAlertaTelegram(dicionario_roletas, nome_cassino, url_cassino, sequencia_minima)
                            time.sleep(1)
                            historico_roleta = lista_proximo_resultados
                            continue

                        elif grupo2.count('true') == 2 and 'false' not in grupo2:
                            print('ENVIAR ALERTA')
                            enviarAlertaTelegram(dicionario_roletas, nome_cassino, url_cassino, sequencia_minima)
                            time.sleep(1)
                            historico_roleta = lista_proximo_resultados
                            continue


                        if grupo1.count('true') == 3 and 'false' not in grupo1:
                            dicionario_roletas[nome_cassino] = lista_proximo_resultados
                            print('ENVIANDO SINAL TELEGRAM')
                            apostar = grupo_numero_base1
                            enviarSinalTelegram(nome_cassino, url_cassino, apostar)
                            print('=' * 150)
                            checkSinalEnviado(lista_proximo_resultados, nome_cassino, roleta, numeros_validacao1)
                            time.sleep(1)
                            break

                        
                        elif grupo2.count('true') == 3 and 'false' not in grupo2:
                            dicionario_roletas[nome_cassino] = lista_proximo_resultados
                            print('ENVIANDO SINAL TELEGRAM')
                            apostar = grupo_numero_base2
                            enviarSinalTelegram(nome_cassino, url_cassino, apostar)
                            print('=' * 150)
                            checkSinalEnviado(lista_proximo_resultados, nome_cassino, roleta, numeros_validacao2)
                            time.sleep(1)
                            break
                            

                        else:
                            historico_roleta = lista_proximo_resultados
                            continue
                    

                    elif 'false' in grupo1 and 'false' in grupo2:
                        apagaAlertaTelegram()
                        time.sleep(1)
                        break


                    else:
                        historico_roleta = lista_proximo_resultados
                        continue
                
                else:
                    continue


            except:
                break 
    
    except:
        pass       
  

def enviarAlertaTelegram(dicionario_roletas, nome_cassino, url_cassino, sequencia_minima):
    global contador_passagem

    ''' Lendo o arquivo txt canais '''
    txt = open("canais.txt", "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[12].split(' ')[1].split('\n')[0].split((','))

    ''' Lendo o arquivo txt config-mensagens '''
    txt = open("config-mensagens.txt", "r", encoding="utf-8")
    mensagem_alerta = txt.readlines()
    
    ''' Mensagem '''
    table_alerta = mensagem_alerta[0].replace('\n','')
    
    
    ''' Enviando mensagem Telegram '''
    try:
        for canal in canais:
            try:
                globals()[f'alerta_{canal}'] = bot.send_message(canal, table_alerta, parse_mode='HTML', disable_web_page_preview=True)  #Variavel Dinâmica
            except:
                pass

    except:
        pass

    contador_passagem = 1
    

def enviarSinalTelegram(nome_cassino, url_cassino, apostar):
    global table_sinal

    ''' Lendo o arquivo txt canais '''
    txt = open("canais.txt", "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[12].split(' ')[1].split('\n')[0].split((','))

    ''' Lendo o arquivo txt config-mensagens '''
    txt = open("config-mensagens.txt", "r", encoding="utf-8")
    arquivo_mensagem = txt.readlines()
    mensagem_sinal = arquivo_mensagem[1].split(',')

    ''' Estruturando mensagem '''
    txt = open("config-mensagens.txt", "r", encoding="utf-8")
    mensagem_sinal = txt.readlines()

    table_sinal = mensagem_sinal[18].replace('\n','') + '\n\n' +\
                  mensagem_sinal[20].replace('\n','').replace('[NOME_CASSINO]', nome_cassino.title()) + '\n' +\
                  mensagem_sinal[21].replace('\n','').replace('[APOSTA]', apostar.upper()) + '\n' +\
                  mensagem_sinal[22].replace('\n','') + '\n' +\
                  mensagem_sinal[23].replace('\n','') + '\n' +\
                  mensagem_sinal[24].replace('\n','') + '\n' +\
                  mensagem_sinal[26].replace('\n','').replace('[LISTA_RESULTADOS]', lista_proximo_resultados[0]) + '\n\n' +\
                  mensagem_sinal[28].replace('\n','')

    ''' Enviando mensagem Telegram '''
    try:
        for canal in canais:
            try:
                bot.delete_message(canal, globals()[f'alerta_{canal}'].message_id)
                globals()[f'sinal_{canal}'] = bot.send_message(canal, table_sinal, parse_mode='HTML', disable_web_page_preview=True)
            except:
                pass
    
    except:
        pass


def apagaAlertaTelegram():
    global contador_passagem

    ''' Lendo o arquivo txt canais '''
    txt = open("canais.txt", "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[12].split(' ')[1].split('\n')[0].split((','))

    try:
        for canal in canais:
            try:
                
                bot.delete_message(canal, globals()[f'alerta_{canal}'].message_id)
                print('APAGA SINAL DE ALERTA')

            except:
                pass
    except:
        pass

    contador_passagem = 0


def checkSinalEnviado(lista_proximo_resultados, nome_cassino, roleta, grupo_numero_base):
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
    global resultado


    resultados = []
    contador_cash = 0
    while contador_cash <= 1:

        ultimo_numero = lista_proximo_resultados[0]
        penultimo_numero = lista_proximo_resultados[1]

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass

        # Validando o horario para envio do relatório diário
        validaData()
        auto_refresh()

        try:

            # VALIDAR SE FOI DESCONECTADO
            if browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[6]/div/div[2]/div[2]/button') or browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[5]/div/div[2]/div/div[3]/button'):
                browser.refresh()
                logarSite()
                continue
            

            ''' Lendo novos resultados para validação da estratégia'''
            lista_resultados_sinal = formatar_resultados(roleta) # Formata o historico em lista
            #print(historico_roleta)

            ''' Validando se tem dado Vazio '''
            if '' in lista_resultados_sinal:
                browser.refresh()
                logarSite()


            ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
            if lista_proximo_resultados[:3] != lista_resultados_sinal[:3]:
                
                print(lista_resultados_sinal[0])
                resultados.append(lista_resultados_sinal[0])

                # VALIDANDO WIN OU LOSS
                if lista_resultados_sinal[0] in grupo_numero_base or lista_resultados_sinal[0] == ultimo_numero or lista_resultados_sinal[0] == penultimo_numero\
                    or lista_resultados_sinal[0] == '0' or lista_resultados_sinal[0] == '00':
                
                    # validando o tipo de WIN
                    if contador_cash == 0:
                        print('WIN SEM GALE')
                        stop_loss.append('win')

                        tipo_resultado = 'SEM GALE'

                        # Atualizando placar e Alimentando o arquivo txt
                        placar_win +=1
                        placar_semGale +=1
                        placar_geral = placar_win + placar_loss

                        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                            arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}")

                            
                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                       
                    if contador_cash == 1:
                        print('WIN GALE1')
                        stop_loss.append('win')

                        tipo_resultado = 'NO GALE'

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
                        

                    # respondendo a mensagem do sinal e condição para enviar sticker
                    try:
                        ''' Lendo o arquivo txt canais '''
                        txt = open("canais.txt", "r", encoding="utf-8")
                        arquivo = txt.readlines()
                        canais = arquivo[12].split(' ')[1].split('\n')[0].split((','))
                        sticker = arquivo[14].split('=')[1].replace('\n','')

                        ''' Lendo o arquivo txt config-mensagens '''
                        txt = open("config-mensagens.txt", "r", encoding="utf-8")
                        mensagem_green = txt.readlines()
                        
                        for canal in canais:
                            try:
                                bot.reply_to(globals()[f'sinal_{canal}'], mensagem_green[38].replace('\n','').replace('[GALE]', tipo_resultado),parse_mode='HTML')
                            except:
                                pass
                            
                            # CONDIÇÃO PARA ENVIAR O STICKER
                            if stop_loss.count('win') == 25:
                                bot.send_sticker(canal, sticker=sticker)

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


        except Exception as a:
            logger.error('Exception ocorrido no ' + repr(a))
            logarSite()
            resultado, roleta = resgatar_historico(nome_cassino)
            continue


    if contador_cash > 1:
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
            txt = open("canais.txt", "r", encoding="utf-8")
            arquivo = txt.readlines()
            canais = arquivo[12].split(' ')[1].split('\n')[0].split((','))

            ''' Lendo o arquivo txt config-mensagens '''
            txt = open("config-mensagens.txt", "r", encoding="utf-8")
            mensagem_green = txt.readlines()

            for canal in canais:
                try:
                    bot.reply_to(globals()[f'sinal_{canal}'], mensagem_green[40], parse_mode = 'HTML')
                except:
                    pass
            

            
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
    

        print('='*100)
        validador_sinal = 0
        contador_cash = 0
        contador_passagem = 0
        dicionario_roletas[nome_cassino] = lista_resultados_sinal
        return




inicio()       # Difinição do webBrowser
logarSite()    # Logando no Site 
placar()       # Chamando o Placar

#________________________________________________________________________________________ TELEGRAM__________________________________________________________________________________#


print()
print()
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
    
    if botStatus == 0 and dicionario_roletas == {}:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','🟢 Ativar Bot','⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Ative o bot primeiro! ", reply_markup=markup)
       
    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','🟢 Ativar Bot','⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        bot.reply_to(message, "🤖 Ok! Mostrando Ultimos Resultados das Roletas", reply_markup=markup)
        try:
            
            for key, value in dicionario_roletas.items():
                #print(key, value)
                bot.send_message(message.chat.id, f'{key}{value}')

        except:
            pass



@bot.message_handler(commands=['📊 Placar Atual'])
def placar_atual(message):
    global placar
    global resultados_sinais

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup = markup.add('/start','🟢 Ativar Bot','⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

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
    global browser
    global parar

    if contador_passagem != 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','🟢 Ativar Bot','⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Estou validando um Sinal. Tente novamente em alguns instanstes.", reply_markup=markup)

    elif botStatus == 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','🟢 Ativar Bot','⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Bot já está pausado ", reply_markup=markup)

    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','🟢 Ativar Bot','⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        botStatus = 0
        parar = 1
        #pausarBot()

        print('\n\n')
        print('Pausar Bot')
        print('Parando o Bot....\n')

        message_final = bot.reply_to(message, "🤖 Ok! Bot pausado 🛑", reply_markup=markup)

        print('\n\n')
        print('############################################ AGUARDANDO COMANDOS ############################################')
        
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
        markup = markup.add('/start','🟢 Ativar Bot','⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message, "🤖 Bot de Roletas Playtech Iniciado! ✅ Escolha uma opção 👇",
                                    reply_markup=markup)
        
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(message_opcoes, opcoes)
    
    else:
        message_error = bot.reply_to(message, "🤖 Você não tem permissão para acessar este Bot ❌🚫")




@bot.message_handler()
def opcoes(message_opcoes):

    if message_opcoes.text in ['🟢 Ativar Bot']:
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
            markup = markup.add('/start','🟢 Ativar Bot','⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖⛔ Bot já está ativado",
                                reply_markup=markup)

        
        else:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            markup = markup.add('/start','🟢 Ativar Bot','⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

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

    
    if message_opcoes.text in ['⏲ Ultimos Resultados']:
        print('Ultimos Resultados')
        ultimosResultados(message_opcoes)



bot.infinity_polling()













