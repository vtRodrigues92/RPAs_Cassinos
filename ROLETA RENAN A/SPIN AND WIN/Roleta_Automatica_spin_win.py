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
import ast


print()
print('                                #################################################################')
print('                                ################  BOT ROLETA BRASILEIRA AUTO. ###################')
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
    tres_hora = timedelta(hours=1)
    horario_mais_tres = horario_inicio + tres_hora
    horario_refresh = horario_mais_tres.strftime('%H:%M')

    if horario_atual == horario_refresh:
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


def resgatar_historico(): 
    global roleta

    try:
        # Formata o historico em lista
        historico_roleta = browser.find_elements_by_xpath('//*[@class="roulette-game-area__history-line"]')       
        return historico_roleta
    
    except:pass


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

        for opcao_aposta in opcoes_apostas:
            if estrategia_usuario == opcao_aposta:
                dic_estrategia_usuario[opcao_aposta] = opcoes_apostas[opcao_aposta]
                #print(dic_estrategia_usuario)
        
        return dic_estrategia_usuario
    
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

    lobby_cassinos = 'https://launcher.betfair.com/?gameId=live-spin-and-win-roulette-cptl&returnURL=https%3A%2F%2Fcasino.betfair.com%2Fpt-br%2F&launchProduct=gaming&RPBucket=gaming&mode=real&dataChannel=ecasino&switchedToPopup=true'
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


def coletarResultados():
    global url_cassino
    global contador_passagem
    global horario_atual
    global aposta, apostando_zero

    url_cassino = ''
    apostando_zero = False
    lista_registrar_resultado = []

    while True:

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass
        
        # Validando o horario para envio do relatório diário
        validaData()

        # Auto Refresh
        #auto_refresh()


        # VALIDAR SE FOI DESCONECTADO
        if browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[6]/div/div[2]/div[2]/button') or browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[5]/div/div[2]/div/div[3]/button'):
            browser.refresh()
            logarSite()
            continue


        try:

            historico_resultados = browser.find_elements_by_xpath('//*[@class="roulette-game-area__history-line"]')
            
            # Validando se foi solicitado o stop do BOT
            if parar != 0:
                break
            else:
                pass

            
            ''' VALIDA SE A LISTA ESTÁ VAZIA '''
            if historico_resultados == []:
                browser.refresh()
                logarSite()
            else:
                pass


            # Formatando o Historico de Resultados.
            lista_resultados = historico_resultados[0].text.split('\n')
            
            #VALIDANDO SE O HISTORICO_ROLETA É UM HISTORICO VÁLIDO
            if len(lista_resultados) > 7:
                pass
            else:
                continue
            
            #REMOVENDO X DOS RESULTADOS:
            for r in lista_resultados:
                if 'x' in r:
                    lista_resultados.remove(r)
                
            # REGISTRANDO RESULTADO NO TXT
            if lista_registrar_resultado == [] or lista_registrar_resultado != lista_resultados:

                data_hoje = datetime.today().strftime('%d-%m-%Y')
                arquivo_resultados = os.listdir(r"resultados/")
                if f'{data_hoje}.txt' in arquivo_resultados:
                    with open(f"resultados/{data_hoje}.txt", 'a') as resultados:
                        resultados.write('\n'+ datetime.now().strftime('%d-%m-%Y') + '|'+ str(lista_resultados[0]))
                    
                    lista_registrar_resultado = lista_resultados
                    
                else:
                    with open(f"resultados/{data_hoje}.txt", 'w') as resultados:
                        resultados.write(datetime.now().strftime('%d-%m-%Y') + '|'+ str(lista_resultados[0]))
                    
                    lista_registrar_resultado = lista_resultados
                    

            print(horario_atual)

            # VALIDANDO FUNÇÃO DE APOSTAR NO ZERO
            if fezinha == 'SIM' and lista_resultados[0] == '0' or fezinha == 'SIM' and lista_resultados[0] == '00':
                apostando_zero = True
                print('APOSTANDO NO ZERO')
                time.sleep(3)
                apostar_zero()
                time.sleep(2)

                bot.send_message(id_usuario, '🙌 FAZENDO UMA FÉZINHA DE R$ 10 NO 0')

                check_sinal_zero(lista_resultados, historico_resultados)

                continue


            ''' Chama a função que valida a estratégia para enviar o sinal Telegram'''
            validarEstrategia(historico_resultados, lista_resultados, lista_estrategias)
            print('=' * 150)

            continue
    
        except:

            logarSite()
            continue 


def validarEstrategia(historico_resultados, lista_resultados, lista_estrategias):
    global estrategia
    global contador_passagem
    global aposta_protecao, aposta_protecao_clicado

    try:

        for estrategia in lista_estrategias:
            
            # Validando se foi solicitado o stop do BOT
            if parar != 0:
                break
            else:
                pass

            # Validando o horario para envio do relatório diário
            validaData()

            # VALIDAR SE FOI DESCONECTADO
            if browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[6]/div/div[2]/div[2]/button') or browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[5]/div/div[2]/div/div[3]/button'):
                browser.refresh()
                logarSite()
                continue
            

            ''' Convertendo a string em formato lista'''
            try:
                estrategia = ast.literal_eval(estrategia)
            except:pass
            ''' Pegando o tipo de aposta (AUSENCIA OU REPETIÇÃO '''
            tipo_aposta = estrategia[0]

            ''' Pegando os números da aposta externa da estratégia'''
            aposta_externa = apostasExternas(estrategia[1], dic_estrategia_usuario)

            ''' Pegando a sequencia minima da estratégia cadastrada pelo usuário '''
            sequencia_minima = estrategia[2]
            
            print ('Analisando a Estrategia --> ', estrategia)
            print('Historico_Roleta --> ', 'Roleta Brasileira', lista_resultados)

            ''' ANTES DE PASSAR NO VALIDADOR, VERIFICAR SE EXISTE O RESULTADO 0 POIS O 0 QUEBRA A SEQUENCIA'''
            if '0' in lista_resultados[:int(sequencia_minima)] or '00' in lista_resultados[:int(sequencia_minima)]:
                print('Sequencia com resultado 0...Analisando outra estratégia!')
                print('=' * 150)
                continue
            
            else:
                pass

            ''' Verifica se os números da seq minima do historico da roleta está dentro da estratégia '''
            validador = validarEstrategiaAlerta(lista_resultados, aposta_externa, sequencia_minima, estrategia)
            
            ''' Validando se bateu alguma condição'''
            if validador.count('true') == int(sequencia_minima)-1:
                print('IDENTIFICADO PRÉ PADRÃO NA ROLETA ', 'Roleta Brasileira', ' COM A ESTRATÉGIA ', estrategia)
                print('ENVIAR ALERTA')
                enviarAlertaTelegram(lista_resultados, sequencia_minima, estrategia)
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
                        #auto_refresh()
 
                        ''' PEGANDO NOVOS RESULTADOS '''
                        # Formata o historico em lista
                        lista_proximo_resultados = historico_resultados[0].text.split('\n') 
                        #print(lista_proximo_resultados)

                        #REMOVENDO X DOS RESULTADOS:
                        for r in lista_proximo_resultados:
                            if 'x' in r:
                                lista_proximo_resultados.remove(r)

                        ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
                        if lista_resultados[:3] != lista_proximo_resultados[:3]:

                            print('Historico_Roleta --> ', 'Roleta Brasileira', lista_proximo_resultados[:int(sequencia_minima)])

                            if estrategia[0] == 'repetição':
                                ''' Verificando se o ultimo resultado da roleta está dentro da estratégia'''
                                if lista_proximo_resultados[0] in aposta_externa[estrategia[1]]:
                                    #dicionario_roletas[nome_cassino] = lista_proximo_resultados
                                    print('SINAL CONFIRMADO! APOSTANDO!!')
                                    
                                    ######### ELEMENTOS #########
                                    if '/' in estrategia[3]:
                                        aposta_um, aposta_um_clicado, aposta_dois, aposta_dois_clicado = elemento_apostas(estrategia)
                                        aposta_protecao = '//*[@class="table-cell--Wz6uJ table-cell_color-green--seXf0"]'
                                        aposta_protecao_clicado = '//*[@class="table-cell--Wz6uJ table-cell_color-green--seXf0 table-cell_hover-highlight--fYheT"]'
                                        ######## INSERINDO APOSTAS #######
                                        time.sleep(5)
                                        apostar_duas_casas(valor_entrada, aposta_um, aposta_um_clicado, aposta_dois, aposta_dois_clicado, aposta_protecao, aposta_protecao_clicado)
                                        

                                    else:
                                        aposta_um, aposta_um_clicado = elemento_apostas(estrategia)
                                        aposta_protecao = '//*[@class="table-cell--Wz6uJ table-cell_color-green--seXf0"]'
                                        aposta_protecao_clicado = '//*[@class="table-cell--Wz6uJ table-cell_color-green--seXf0 table-cell_hover-highlight--fYheT"]'
                                        ######## INSERINDO APOSTAS #######
                                        time.sleep(5)
                                        apostar_uma_casa(valor_entrada, aposta_um, aposta_um_clicado, aposta_protecao, aposta_protecao_clicado)
                                    

                                    #### ENVIANDO SINAL PRO TELEGREM #####
                                    enviarSinalTelegram(lista_proximo_resultados, valor_entrada, sequencia_minima, estrategia)
                                    print('=' * 150)

                                    #### CHECANDO SINAL ENVIADO ####
                                    checkSinalEnviado(lista_proximo_resultados, historico_resultados)
                                    time.sleep(1)
                                    return
                                
                                else:
                                    print('APAGA SINAL DE ALERTA')
                                    apagaAlertaTelegram()
                                    print('=' * 150)
                                    lista_resultados = lista_proximo_resultados
                                    break

                            
                            if estrategia[0] == 'ausência':
                                ''' Verificando se o ultimo resultado da roleta não está dentro da estratégia'''
                                if lista_proximo_resultados[0] not in aposta_externa[estrategia[1]]:
                                    #dicionario_roletas[nome_cassino] = lista_proximo_resultados
                                    print('SINAL CONFIRMADO! APOSTANDO!!')
                                    
                                    ######### ELEMENTOS #########
                                    if '/' in estrategia[3]:
                                        aposta_um, aposta_um_clicado, aposta_dois, aposta_dois_clicado = elemento_apostas(estrategia)
                                        aposta_protecao = '//*[@class="table-cell--Wz6uJ table-cell_color-green--seXf0"]'
                                        aposta_protecao_clicado = '//*[@class="table-cell--Wz6uJ table-cell_color-green--seXf0 table-cell_hover-highlight--fYheT"]'
                                        time.sleep(5)
                                        apostar_duas_casas(valor_entrada, aposta_um, aposta_um_clicado, aposta_dois, aposta_dois_clicado, aposta_protecao, aposta_protecao_clicado)
                                        
                                    else:
                                        aposta_um, aposta_um_clicado = elemento_apostas(estrategia)
                                        aposta_protecao = '//*[@class="table-cell--Wz6uJ table-cell_color-green--seXf0"]'
                                        aposta_protecao_clicado = '//*[@class="table-cell--Wz6uJ table-cell_color-green--seXf0 table-cell_hover-highlight--fYheT"]'
                                        ######## INSERINDO APOSTAS #######
                                        time.sleep(5)
                                        apostar_uma_casa(valor_entrada, aposta_um, aposta_um_clicado, aposta_protecao, aposta_protecao_clicado)
                                    
                                    
                                    #### ENVIANDO SINAL PRO TELEGREM #####
                                    enviarSinalTelegram(lista_proximo_resultados, valor_entrada, sequencia_minima, estrategia)
                                    print('=' * 150)

                                    #### CHECANDO SINAL ENVIADO ####
                                    checkSinalEnviado(lista_proximo_resultados, historico_resultados)
                                    return
                                
                                else:
                                    print('APAGA SINAL DE ALERTA')
                                    apagaAlertaTelegram()
                                    print('=' * 150)
                                    lista_resultados = lista_proximo_resultados
                                    break
                        
                        else:
                            continue

                    except Exception as b:
                        logger.error('Exception ocorrido no ' + repr(b))
                        print('APAGA SINAL DE ALERTA')
                        apagaAlertaTelegram()
                        print('=' * 150)
                        lista_resultados = lista_proximo_resultados
                        break
            

            else:
                print('=' * 150)

                    
    except:
        # VALIDAR SE FOI DESCONECTADO
        if browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[6]/div/div[2]/div[2]/button'):
            browser.refresh()
            logarSite()
            pass

        else:
            pass


def validarEstrategiaAlerta(lista_resultados, aposta_externa, sequencia_minima, estrategia):
    validador = []
    for n in range(int(sequencia_minima)-1):

        if estrategia[0] == 'repetição':
            if lista_resultados[n] in aposta_externa[estrategia[1]]:
                validador.append('true')

        if estrategia[0] == 'ausência':
            if lista_resultados[n] not in aposta_externa[estrategia[1]]:
                validador.append('true')

    
    return validador


def enviarAlertaTelegram(lista_resultados, sequencia_minima, estrategia):
    global contador_passagem
    global mensagem_telegram_alerta

    ''' Lendo o arquivo txt config-mensagens '''
    txt = open("config-mensagens.txt", "r", encoding="utf-8")
    mensagem_alerta = txt.readlines()
    
    ''' Mensagem '''
    table_alerta = mensagem_alerta[0].replace('\n','') + '\n' + \
                   mensagem_alerta[1].replace('\n','').replace('[ESTRATEGIA]', estrategia[0].title()+' de '+estrategia[1].title()) + '\n' + \
                   mensagem_alerta[2].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(lista_resultados[:int(sequencia_minima)-1]))
                   
    ''' Enviando mensagem Telegram '''
    try:
    
        mensagem_telegram_alerta = bot.send_message(id_usuario, table_alerta, parse_mode='HTML')

    except:
        pass

    contador_passagem = 1
    

def enviarSinalTelegram(lista_resultados, valor_entrada, sequencia_minima, estrategia):
    global table_sinal

    ''' Lendo o arquivo txt config-mensagens '''
    txt = open("config-mensagens.txt", "r", encoding="utf-8")
    arquivo_mensagem = txt.readlines()
    mensagem_sinal = arquivo_mensagem[1].split(',')

    ''' Estruturando mensagem '''
    txt = open("config-mensagens.txt", "r", encoding="utf-8")
    mensagem_sinal = txt.readlines()

    table_sinal = mensagem_sinal[11].replace('\n','') + '\n' +\
                  mensagem_sinal[12].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(lista_resultados[:int(sequencia_minima)])) + '\n' +\
                  mensagem_sinal[13].replace('\n','').replace('[VALOR_APOSTA]', str(valor_entrada)).replace('[APOSTA]', estrategia[3].upper()) + '\n' +\
                  mensagem_sinal[14].replace('\n','')

    ''' Enviando mensagem Telegram '''
    try:

        bot.delete_message(id_usuario, mensagem_telegram_alerta.message_id)
        bot.send_message(id_usuario, table_sinal, parse_mode='HTML')
    
    except:
        pass


def apagaAlertaTelegram():
    global contador_passagem

    try:    
        
        bot.delete_message(id_usuario, mensagem_telegram_alerta.message_id)
        
    except:
        pass

    contador_passagem = 0


def checkSinalEnviado(lista_proximo_resultados, historico_resultados):
    global table
    global message_canal
    global resultados_sinais
    global ultimo_horario_resultado
    global validador_sinal
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
    global lista_resultados, apostando_zero

    resultados = []
    contador_cash = 0

    while contador_cash <= int(martingale):

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass

        # Validando o horario para envio do relatório diário
        validaData()
        #auto_refresh()

        try:

            # VALIDAR SE FOI DESCONECTADO
            if browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[6]/div/div[2]/div[2]/button') or browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[5]/div/div[2]/div/div[3]/button'):
                browser.refresh()
                logarSite()
                continue
            

            ''' Lendo novos resultados para validação da estratégia'''
            # Formata o historico em lista
            lista_resultados_sinal = historico_resultados[0].text.split('\n') 
            #print(historico_roleta)

            ''' Validando se tem dado Vazio '''
            if '' in lista_resultados_sinal:
                browser.refresh()
                logarSite()


            #REMOVENDO X DOS RESULTADOS:
            for r in lista_resultados_sinal:
                if 'x' in r:
                    lista_resultados_sinal.remove(r)

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
                        

                    if contador_cash == 1:
                        print('WIN GALE1')

                        # Atualizando placar e Alimentando o arquivo txt
                        placar_win +=1
                        placar_gale1 +=1
                        placar_geral = placar_win + placar_loss
                        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                            arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}")
                         
                        stop_loss
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

                        except:
                            pass


                    if contador_cash == 2:
                        print('WIN GALE2')
                        
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
                        

                                        
                    # respondendo a mensagem do sinal e condição para enviar sticker
                    try:
                        
                        ''' Lendo o arquivo txt config-mensagens '''
                        txt = open("config-mensagens.txt", "r", encoding="utf-8")
                        mensagem_green = txt.readlines()
                        
                        try:
                            #Envia Green Telegram
                            bot.send_message(id_usuario, mensagem_green[25].replace('\n','').replace('[RESULTADO]', ' | '.join(resultados)), parse_mode='HTML')
                            time.sleep(1)
                            # Validando o STOP WIN
                            validar_stop_win()


                        except:
                            pass

                    except:
                        pass

                    
                    

                    print('==================================================')
                    validador_sinal = 0
                    contador_cash = 0
                    contador_passagem = 0
                    lista_resultados = lista_resultados_sinal
                    return

            
                else:
                    print('LOSSS')
                    print('==================================================')

                    # VALIDANDO SE A APOSTA É NO ZERO ESTÁ ATIVA
                    if apostando_zero == True:
                        apostando_zero = False
                        return


                    contador_cash+=1
                    lista_proximo_resultados = lista_resultados_sinal
                    

                    if contador_cash <= martingale:

                        time.sleep(5)
                        valor_gale = valor_entrada * fator_gale * contador_cash
                        if '/' in estrategia[3]:
                            apostar_duas_casas(valor_gale, aposta_um, aposta_um_clicado, aposta_dois, aposta_dois_clicado, aposta_protecao, aposta_protecao_clicado)
                        else:
                            apostar_uma_casa(valor_gale, aposta_um, aposta_um_clicado, aposta_protecao, aposta_protecao_clicado)
                        
                        msg_matingale(valor_gale, contador_cash)
                    
                    
                    continue


        except Exception as a:
            logger.error('Exception ocorrido no ' + repr(a))
            logarSite()
            historico_resultados = resgatar_historico()
            continue


    if contador_cash > int(martingale):
        
        print('LOSSS GALE', int(martingale))

        # Preenchendo arquivo txt
        placar_loss +=1
        placar_geral = placar_win + placar_loss
        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
            arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}")
            

        # Preenchendo dados do LOSS
        with open("historico_loss.txt", "a") as arquivo: 
            arquivo.write('\n'+datetime.now().strftime('%d-%m-%Y %H:%M:%S')+' - '+ str(estrategia))


        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
            
        # editando mensagem
        try:
            
            ''' Lendo o arquivo txt config-mensagens '''
            txt = open("config-mensagens.txt", "r", encoding="utf-8")
            mensagem_red = txt.readlines()

            try:
                
                bot.send_message(id_usuario, mensagem_red[27].replace('\n','').replace('[RESULTADO]', ' | '.join(resultados)), parse_mode='HTML')
            
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
            
        except:
            pass

        

        validar_stop_loss()

        print('='*100)
        validador_sinal = 0
        contador_cash = 0
        contador_passagem = 0
        lista_resultados = lista_resultados_sinal
        return


def apostar_duas_casas(valor_aposta, *args):

    moedas = browser.find_elements_by_xpath('//*[@class="chip-animation-wrapper"]//*[name()="text"]')
    protecao_zero = valor_aposta/10


    if valor_aposta == 1:
        #CLICANDO NA MOEDA 5
        try:

            for moeda in moedas:
                if moeda.text == '1':
                    moeda.click()
                    break               

            #DAR 1 CLICK
            browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)
            browser.find_element_by_xpath(aposta_dois).click()

        except:
            pass



    elif valor_aposta == 2 or valor_aposta == 4:
        #CLICANDO NA MOEDA 5
        try:

            for moeda in moedas:
                if moeda.text == '2':
                    moeda.click()
                    break  

            if valor_aposta == 2:
                #DAR 1 CLICK
                browser.find_element_by_xpath(aposta_um).click()
                time.sleep(0.5)
                browser.find_element_by_xpath(aposta_dois).click()
            if valor_aposta == 4:
                #DAR 1 CLICK
                browser.find_element_by_xpath(aposta_um).click()
                time.sleep(0.5)
                browser.find_element_by_xpath(aposta_dois).click()
                time.sleep(0.5)
                #DAR 1 CLICK
                browser.find_element_by_xpath(aposta_um).click()
                time.sleep(0.5)
                browser.find_element_by_xpath(aposta_dois).click()


        except:
            pass


    elif valor_aposta == 5 or valor_aposta == 15:
        #CLICANDO NA MOEDA 5
        try:
            for moeda in moedas:
                if moeda.text == '5':
                    moeda.click()
                    break               
        except:
            pass
        
        if valor_aposta == 5:
            #DAR 1 CLICK
            browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)
            browser.find_element_by_xpath(aposta_dois).click()
        
        elif valor_aposta == 15:
            a = 1
            b = 0
            while a <=3:
                try:
                    if b == 0:
                        browser.find_element_by_xpath(aposta_um).click()
                        time.sleep(0.5)
                        browser.find_element_by_xpath(aposta_dois).click()
                        a+=1
                        b+=1
                        time.sleep(0.5)
                        continue
                    else:
                        browser.find_element_by_xpath(aposta_um).click()
                        time.sleep(0.5)
                        browser.find_element_by_xpath(aposta_dois).click()
                        a+=1
                        time.sleep(0.5)
                        continue
                
                except:
                    a+=1
                    time.sleep(0.5)
                    continue
            
            b = 0


    elif valor_aposta == 25:
        #CLICANDO NAS MOEDAS 20 E 5
        try:

            # MOEDA 20
            for moeda in moedas:
                if moeda.text == '20':
                    moeda.click()
                    break

            time.sleep(1)
            #CLICANDO NA APOSTA
            browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)
            browser.find_element_by_xpath(aposta_dois).click()

            #MOEDA 5
            for moeda in moedas:
                if moeda.text == '5':
                    moeda.click()  

            time.sleep(1)
            #CLICANDO NA APOSTA
            browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)
            browser.find_element_by_xpath(aposta_dois).click()


        except:
            pass


    elif valor_aposta == 45:
        #CLICANDO NAS MOEDAS 20 E 5
        try:
            #MOEDA 20
            for moeda in moedas:
                if moeda.text == '20':
                    moeda.click()
                    break    


            time.sleep(1)
            #CLICANDO NA APOSTA
            browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)
            browser.find_element_by_xpath(aposta_dois).click()

            time.sleep(1)
            #CLICANDO NA APOSTA
            browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)
            browser.find_element_by_xpath(aposta_dois).click()


            #MOEDA 5
            for moeda in moedas:
                if moeda.text == '5':
                    moeda.click()
                    break

            time.sleep(1)
            #CLICANDO NA APOSTA
            browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)
            browser.find_element_by_xpath(aposta_dois).click()

        except:pass


    elif valor_aposta == 125:
        #CLICANDO 2 VEZES NA MOEDA 50 E UMA VEZ NA MOEDA 25
        try:
            #MOEDA 50
            for moeda in moedas:
                if moeda.text == '50':
                    moeda.click()
                    break   

            time.sleep(1)
            #CLICANDO NA APOSTA
            browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)
            browser.find_element_by_xpath(aposta_dois).click()

            time.sleep(1)
            #CLICANDO NA APOSTA
            browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)
            browser.find_element_by_xpath(aposta_dois).click()

            # MOEDA 20
            for moeda in moedas:
                if moeda.text == '20':
                    moeda.click()
                    break

            time.sleep(1)
            #CLICANDO NA APOSTA
            browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)
            browser.find_element_by_xpath(aposta_dois).click()

            #MOEDA 5
            for moeda in moedas:
                if moeda.text == '5':
                    moeda.click()  

            time.sleep(1)
            #CLICANDO NA APOSTA
            browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)
            browser.find_element_by_xpath(aposta_dois).click()

        except:pass


    elif valor_aposta == 135:
        #CLICANDO 2 VEZES NA MOEDA 50 E UMA VEZ NA MOEDA 25
        try:
            #MOEDA 50
            for moeda in moedas:
                if moeda.text == '50':
                    moeda.click()
                    break   

            time.sleep(1)
            #CLICANDO NA APOSTA
            browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)
            browser.find_element_by_xpath(aposta_dois).click()

            time.sleep(1)
            #CLICANDO NA APOSTA
            browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)
            browser.find_element_by_xpath(aposta_dois).click()

            # MOEDA 20
            for moeda in moedas:
                if moeda.text == '20':
                    moeda.click()
                    break

            time.sleep(1)
            #CLICANDO NA APOSTA
            browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)
            browser.find_element_by_xpath(aposta_dois).click()

            #MOEDA 5
            for moeda in moedas:
                if moeda.text == '5':
                    moeda.click()  

            time.sleep(1)
            #CLICANDO NA APOSTA
            browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)
            browser.find_element_by_xpath(aposta_dois).click()


            #MOEDA 5
            for moeda in moedas:
                if moeda.text == '5':
                    moeda.click()
                    break

            time.sleep(1)
            #CLICANDO NA APOSTA
            browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)
            browser.find_element_by_xpath(aposta_dois).click()

            time.sleep(1)
            #CLICANDO NA APOSTA
            browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)
            browser.find_element_by_xpath(aposta_dois).click()

        except:pass


    elif valor_aposta == 100:
        #CLICANDO 2 VEZES NA MOEDA 50 E UMA VEZ NA MOEDA 25
        try:
            #MOEDA 50
            for moeda in moedas:
                if moeda.text == '50':
                    moeda.click()
                    break  

            time.sleep(1)
            #CLICANDO NA APOSTA
            browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)
            browser.find_element_by_xpath(aposta_dois).click()

            time.sleep(1)
            #CLICANDO NA APOSTA
            browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)
            browser.find_element_by_xpath(aposta_dois).click()
        
        except:pass


    elif valor_aposta == 300:
        #CLICANDO 2 VEZES NA MOEDA 50 E UMA VEZ NA MOEDA 25
        try:
            #MOEDA 50
            for moeda in moedas:
                if moeda.text == '50':
                    moeda.click()
                    break

            time.sleep(0.5)
            #CLICANDO NA APOSTA
            browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)
            browser.find_element_by_xpath(aposta_dois).click()

            time.sleep(0.5)
            #CLICANDO NA APOSTA
            browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)
            browser.find_element_by_xpath(aposta_dois).click()

            time.sleep(0.5)
            #CLICANDO NA APOSTA
            browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)
            browser.find_element_by_xpath(aposta_dois).click()

            time.sleep(0.5)
            #CLICANDO NA APOSTA
            browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)
            browser.find_element_by_xpath(aposta_dois).click()

            time.sleep(0.5)
            #CLICANDO NA APOSTA
            browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)
            browser.find_element_by_xpath(aposta_dois).click()

            time.sleep(0.5)
            #CLICANDO NA APOSTA
            browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)
            browser.find_element_by_xpath(aposta_dois).click()
        
        except:pass




    ############# PROTEÇÃO


    if protecao_zero == 0.5:

        try:

            #CLICANDO NA MOEDA 0.5
            for moeda in moedas:
                if moeda.text == '0.5':
                    moeda.click()   

            time.sleep(1)
            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()
            time.sleep(0.5)


        except:
            pass

    elif protecao_zero == 1.5:
        
        try:
            #CLICANDO NA MOEDA 1
            for moeda in moedas:
                if moeda.text == '1':
                    moeda.click()       
            
            time.sleep(1)
            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()
            time.sleep(0.5)

        except:
            pass

        try:
            #CLICANDO NA MOEDA 0.5
            for moeda in moedas:
                if moeda.text == '0.5':
                    moeda.click()   

            time.sleep(1)
            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()
            time.sleep(0.5)

        except:
            pass

    elif protecao_zero == 2.5:
        try:
            #CLICANDO NA MOEDA 2
            for moeda in moedas:
                if moeda.text == '2':
                    moeda.click()       
            
            time.sleep(1)
            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()
            time.sleep(0.5)

        except:
            pass

        try:
            #CLICANDO NA MOEDA 0.5
            for moeda in moedas:
                if moeda.text == '0.5':
                    moeda.click()   

            time.sleep(1)
            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()
            time.sleep(0.5)

        except:
            pass

    elif protecao_zero == 3.0:
        try:
            #CLICANDO NA MOEDA 1
            for moeda in moedas:
                if moeda.text == '1':
                    moeda.click()

            time.sleep(1)
            #CLICANDO NA APOSTA
            a = 1
            b = 0
            while a <= 3:
                try:
                    if b == 0:
                        try:
                            browser.find_element_by_xpath(aposta_protecao).click()
                        except:
                            browser.find_element_by_xpath(aposta_protecao_clicado).click()
                        time.sleep(0.5)
                        a+=1
                        b+=1
                        continue
                    else:
                        try:
                            browser.find_element_by_xpath(aposta_protecao).click()
                        except:
                            browser.find_element_by_xpath(aposta_protecao_clicado).click()
                        time.sleep(0.5)
                        a+=1
                        continue


                except:

                    time.sleep(0.5)
                    a+=1
                    continue
            
            b=0

        except:
            pass

    elif protecao_zero == 4.5:
        try:
            #CLICK NA MOEDA 2
            for moeda in moedas:
                if moeda.text == '2':
                    moeda.click()       
            time.sleep(1)

            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()
            time.sleep(0.5)

            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()
            time.sleep(0.5)


            #CLICK NA MOEDA 0.5
            for moeda in moedas:
                if moeda.text == '0.5':
                    moeda.click()

            time.sleep(1)
            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()

            time.sleep(0.5)

        except:pass

    elif protecao_zero == 12.5:
        try:
            #CLICK NA MOEDA 5
            for moeda in moedas:
                if moeda.text == '5':
                    moeda.click()       
            time.sleep(1)

            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()

            time.sleep(0.5)

            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()
            time.sleep(0.5)

            #CLICK NA MOEDA 2
            for moeda in moedas:
                if moeda.text == '2':
                    moeda.click()       
            time.sleep(1)

            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()
            time.sleep(0.5)
        
            #CLICK NA MOEDA 0.5
            for moeda in moedas:
                if moeda.text == '0.5':
                    moeda.click()

            time.sleep(1)
            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()
            time.sleep(0.5)

        except:pass

    elif protecao_zero == 13.5:
        try:
            #CLICK NA MOEDA 5
            for moeda in moedas:
                if moeda.text == '5':
                    moeda.click()       
            time.sleep(1)

            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()
            time.sleep(0.5)

            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()
            time.sleep(0.5)

            #CLICK NA MOEDA 1
            for moeda in moedas:
                if moeda.text == '1':
                    moeda.click()       
            time.sleep(1)

            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()
            time.sleep(0.5)

            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()
            time.sleep(0.5)

            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()
            time.sleep(0.5)


            #CLICK NA MOEDA 0.5
            for moeda in moedas:
                if moeda.text == '0.5':
                    moeda.click()

            time.sleep(1)
            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()
            time.sleep(0.5)

        except:pass


def apostar_uma_casa(valor_aposta, *args):

    moedas = browser.find_elements_by_xpath('//*[@class="chip-animation-wrapper"]//*[name()="text"]')
    protecao_zero = valor_aposta/10


    if valor_aposta == 1:
        #CLICANDO NA MOEDA 5
        try:

            for moeda in moedas:
                if moeda.text == '1':
                    moeda.click()
                    break               

            #DAR 1 CLICK
            time.sleep(0.5)
            browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)

        except:
            pass



    elif valor_aposta == 2 or valor_aposta == 4:
        #CLICANDO NA MOEDA 5
        try:

            for moeda in moedas:
                if moeda.text == '2':
                    moeda.click()
                    break  

            if valor_aposta == 2:
                #DAR 1 CLICK
                browser.find_element_by_xpath(aposta_um).click()

            if valor_aposta == 4:
                #DAR 1 CLICK
                browser.find_element_by_xpath(aposta_um).click()
                time.sleep(0.5)
                try:
                    browser.find_element_by_xpath(aposta_um_clicado).click()
                except:
                    browser.find_element_by_xpath(aposta_um).click()
                time.sleep(0.5)
                

        except:
            pass


    elif valor_aposta == 5 or valor_aposta == 15:
        #CLICANDO NA MOEDA 5
        try:
            for moeda in moedas:
                if moeda.text == '5':
                    moeda.click()
                    break               
        except:
            pass
        
        if valor_aposta == 5:
            #DAR 1 CLICK
            time.sleep(0.5)
            browser.find_element_by_xpath(aposta_um).click()
            
        
        elif valor_aposta == 15:
            a = 1
            b = 0
            while a <=3:
                try:
                    if b == 0:
                        time.sleep(0.5)
                        browser.find_element_by_xpath(aposta_um).click()
                        a+=1
                        b+=1
                        time.sleep(0.5)
                        continue

                    else:

                        try:
                            browser.find_element_by_xpath(aposta_um_clicado).click()
                        except:
                            browser.find_element_by_xpath(aposta_um).click()
                        a+=1
                        time.sleep(0.5)
                        continue
                
                except:
                    a+=1
                    time.sleep(0.5)
                    continue
            
            b = 0


    elif valor_aposta == 25:
        #CLICANDO NAS MOEDAS 20 E 5
        try:

            # MOEDA 20
            for moeda in moedas:
                if moeda.text == '20':
                    moeda.click()
                    break

            time.sleep(1)
            #CLICANDO NA APOSTA
            browser.find_element_by_xpath(aposta_um).click()

            #MOEDA 5
            for moeda in moedas:
                if moeda.text == '5':
                    moeda.click()  

            time.sleep(1)
            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_um_clicado).click()
            except:
                browser.find_element_by_xpath(aposta_um).click()
            

        except:
            pass


    elif valor_aposta == 45:
        #CLICANDO NAS MOEDAS 20 E 5
        try:
            #MOEDA 20
            for moeda in moedas:
                if moeda.text == '20':
                    moeda.click()
                    break    


            time.sleep(1)
            #CLICANDO NA APOSTA
            browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)
            try:
                browser.find_element_by_xpath(aposta_um_clicado).click()
            except:
                browser.find_element_by_xpath(aposta_um).click()


            #MOEDA 5
            for moeda in moedas:
                if moeda.text == '5':
                    moeda.click()
                    break

            time.sleep(1)
            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_um_clicado).click()
            except:
                browser.find_element_by_xpath(aposta_um).click()
            

        except:pass


    elif valor_aposta == 125:
        #CLICANDO 2 VEZES NA MOEDA 50 E UMA VEZ NA MOEDA 25
        try:
            #MOEDA 50
            for moeda in moedas:
                if moeda.text == '50':
                    moeda.click()
                    break   

            time.sleep(1)
            #CLICANDO NA APOSTA
            browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)
            try:
                browser.find_element_by_xpath(aposta_um_clicado).click()
            except:
                browser.find_element_by_xpath(aposta_um).click()

           
            # MOEDA 20
            for moeda in moedas:
                if moeda.text == '20':
                    moeda.click()
                    break

            time.sleep(1)
            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_um_clicado).click()
            except:
                browser.find_element_by_xpath(aposta_um).click()

            #MOEDA 5
            for moeda in moedas:
                if moeda.text == '5':
                    moeda.click()  

            time.sleep(1)
            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_um_clicado).click()
            except:
                browser.find_element_by_xpath(aposta_um).click()
           

        except:pass


    elif valor_aposta == 135:
        #CLICANDO 2 VEZES NA MOEDA 50 E UMA VEZ NA MOEDA 25
        try:
            #MOEDA 50
            for moeda in moedas:
                if moeda.text == '50':
                    moeda.click()
                    break   

            time.sleep(1)
            #CLICANDO NA APOSTA
            browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)
            try:
                browser.find_element_by_xpath(aposta_um_clicado).click()
            except:
                browser.find_element_by_xpath(aposta_um).click()


            # MOEDA 20
            for moeda in moedas:
                if moeda.text == '20':
                    moeda.click()
                    break

            time.sleep(1)
            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_um_clicado).click()
            except:
                browser.find_element_by_xpath(aposta_um).click()

            #MOEDA 5
            for moeda in moedas:
                if moeda.text == '5':
                    moeda.click()  

            time.sleep(1)
            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_um_clicado).click()
            except:
                browser.find_element_by_xpath(aposta_um).click()
           

            #MOEDA 5
            for moeda in moedas:
                if moeda.text == '5':
                    moeda.click()
                    break

            time.sleep(1)
            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_um_clicado).click()
            except:
                browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)
            try:
                browser.find_element_by_xpath(aposta_um_clicado).click()
            except:
                browser.find_element_by_xpath(aposta_um).click()

        except:pass


    elif valor_aposta == 100:
        #CLICANDO 2 VEZES NA MOEDA 50 E UMA VEZ NA MOEDA 25
        try:
            #MOEDA 50
            for moeda in moedas:
                if moeda.text == '50':
                    moeda.click()
                    break  

            time.sleep(1)
            #CLICANDO NA APOSTA
            browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)
            try:
                browser.find_element_by_xpath(aposta_um_clicado).click()
            except:
                browser.find_element_by_xpath(aposta_um).click()
        except:pass


    elif valor_aposta == 300:
        #CLICANDO 2 VEZES NA MOEDA 50 E UMA VEZ NA MOEDA 25
        try:
            #MOEDA 50
            for moeda in moedas:
                if moeda.text == '50':
                    moeda.click()
                    break

            time.sleep(0.5)
            #CLICANDO NA APOSTA
            browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)
            try:
                browser.find_element_by_xpath(aposta_um_clicado).click()
            except:
                browser.find_element_by_xpath(aposta_um).click()

            time.sleep(0.5)
            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_um_clicado).click()
            except:
                browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)
            try:
                browser.find_element_by_xpath(aposta_um_clicado).click()
            except:
                browser.find_element_by_xpath(aposta_um).click()

            time.sleep(0.5)
            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_um_clicado).click()
            except:
                browser.find_element_by_xpath(aposta_um).click()
            time.sleep(0.5)
            try:
                browser.find_element_by_xpath(aposta_um_clicado).click()
            except:
                browser.find_element_by_xpath(aposta_um).click()

        
        except:pass




    ############# PROTEÇÃO


    if protecao_zero == 0.5:

        try:

            #CLICANDO NA MOEDA 0.5
            for moeda in moedas:
                if moeda.text == '0.5':
                    moeda.click()   

            time.sleep(1)
            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()
            time.sleep(0.5)


        except:
            pass

    elif protecao_zero == 1.5:
        
        try:
            #CLICANDO NA MOEDA 1
            for moeda in moedas:
                if moeda.text == '1':
                    moeda.click()       
            
            time.sleep(1)
            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()
            time.sleep(0.5)

        except:
            pass

        try:
            #CLICANDO NA MOEDA 0.5
            for moeda in moedas:
                if moeda.text == '0.5':
                    moeda.click()   

            time.sleep(1)
            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()
            time.sleep(0.5)

        except:
            pass

    elif protecao_zero == 2.5:
        try:
            #CLICANDO NA MOEDA 2
            for moeda in moedas:
                if moeda.text == '2':
                    moeda.click()       
            
            time.sleep(1)
            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()
            time.sleep(0.5)

        except:
            pass

        try:
            #CLICANDO NA MOEDA 0.5
            for moeda in moedas:
                if moeda.text == '0.5':
                    moeda.click()   

            time.sleep(1)
            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()
            time.sleep(0.5)

        except:
            pass

    elif protecao_zero == 3.0:
        try:
            #CLICANDO NA MOEDA 1
            for moeda in moedas:
                if moeda.text == '1':
                    moeda.click()

            time.sleep(1)
            #CLICANDO NA APOSTA
            a = 1
            b = 0
            while a <= 3:
                try:
                    if b == 0:
                        try:
                            browser.find_element_by_xpath(aposta_protecao).click()
                        except:
                            browser.find_element_by_xpath(aposta_protecao_clicado).click()
                        time.sleep(0.5)
                        a+=1
                        b+=1
                        continue
                    else:
                        try:
                            browser.find_element_by_xpath(aposta_protecao).click()
                        except:
                            browser.find_element_by_xpath(aposta_protecao_clicado).click()
                        time.sleep(0.5)
                        a+=1
                        continue


                except:

                    time.sleep(0.5)
                    a+=1
                    continue
            
            b=0

        except:
            pass

    elif protecao_zero == 4.5:
        try:
            #CLICK NA MOEDA 2
            for moeda in moedas:
                if moeda.text == '2':
                    moeda.click()       
            time.sleep(1)

            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()
            time.sleep(0.5)

            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()
            time.sleep(0.5)


            #CLICK NA MOEDA 0.5
            for moeda in moedas:
                if moeda.text == '0.5':
                    moeda.click()

            time.sleep(1)
            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()

            time.sleep(0.5)

        except:pass

    elif protecao_zero == 12.5:
        try:
            #CLICK NA MOEDA 5
            for moeda in moedas:
                if moeda.text == '5':
                    moeda.click()       
            time.sleep(1)

            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()

            time.sleep(0.5)

            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()
            time.sleep(0.5)

            #CLICK NA MOEDA 2
            for moeda in moedas:
                if moeda.text == '2':
                    moeda.click()       
            time.sleep(1)

            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()
            time.sleep(0.5)
        
            #CLICK NA MOEDA 0.5
            for moeda in moedas:
                if moeda.text == '0.5':
                    moeda.click()

            time.sleep(1)
            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()
            time.sleep(0.5)

        except:pass

    elif protecao_zero == 13.5:
        try:
            #CLICK NA MOEDA 5
            for moeda in moedas:
                if moeda.text == '5':
                    moeda.click()       
            time.sleep(1)

            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()
            time.sleep(0.5)

            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()
            time.sleep(0.5)

            #CLICK NA MOEDA 1
            for moeda in moedas:
                if moeda.text == '1':
                    moeda.click()       
            time.sleep(1)

            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()
            time.sleep(0.5)

            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()
            time.sleep(0.5)

            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()
            time.sleep(0.5)


            #CLICK NA MOEDA 0.5
            for moeda in moedas:
                if moeda.text == '0.5':
                    moeda.click()

            time.sleep(1)
            #CLICANDO NA APOSTA
            try:
                browser.find_element_by_xpath(aposta_protecao).click()
            except:
                browser.find_element_by_xpath(aposta_protecao_clicado).click()
            time.sleep(0.5)

        except:pass




def apostar_zero():

    aposta_zero = '//*[@class="table-cell--Wz6uJ table-cell_color-green--seXf0"]'
    aposta_zero_clicado = '//*[@class="table-cell--Wz6uJ table-cell_color-green--seXf0 table-cell_hover-highlight--fYheT"]'
    
    moedas = browser.find_elements_by_xpath('//*[@class="chip-animation-wrapper"]//*[name()="text"]')

    #CLICK NA MOEDA 5
    for moeda in moedas:
        if moeda.text == '5':
            moeda.click() 
            break      
    
    time.sleep(1)

    #CLICANDO NA APOSTA
    browser.find_element_by_xpath(aposta_zero).click()
    time.sleep(2)
    try:
        browser.find_element_by_xpath(aposta_zero_clicado).click()
    except:
        browser.find_element_by_xpath(aposta_zero).click()
    time.sleep(1)


def check_sinal_zero(lista_proximo_resultados, historico_resultados):
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
    global lista_resultados, apostando_zero


    resultados = []
    contador_cash = 0

    while contador_cash <= 0:

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass

        # Validando o horario para envio do relatório diário
        validaData()
        #auto_refresh()

        try:

            # VALIDAR SE FOI DESCONECTADO
            if browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[6]/div/div[2]/div[2]/button') or browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[5]/div/div[2]/div/div[3]/button'):
                browser.refresh()
                logarSite()
                continue
            

            ''' Lendo novos resultados para validação da estratégia'''
            # Formata o historico em lista
            lista_resultados_sinal = historico_resultados[0].text.split('\n') 
            #print(historico_roleta)

            ''' Validando se tem dado Vazio '''
            if '' in lista_resultados_sinal:
                browser.refresh()
                logarSite()


            #REMOVENDO X DOS RESULTADOS:
            for r in lista_resultados_sinal:
                if 'x' in r:
                    lista_resultados_sinal.remove(r)

            ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
            if lista_proximo_resultados[:3] != lista_resultados_sinal[:3]:
                
                print(lista_resultados_sinal[0])
                resultados.append(lista_resultados_sinal[0])
                

                # VALIDANDO WIN OU LOSS
                if lista_resultados_sinal[0] == '0' or lista_resultados_sinal[0] == '00':
                
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
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)


                    # respondendo a mensagem do sinal e condição para enviar sticker
                    try:
                        
                        ''' Lendo o arquivo txt config-mensagens '''
                        txt = open("config-mensagens.txt", "r", encoding="utf-8")
                        mensagem_green = txt.readlines()
                        
                        try:
                            #Envia Green Telegram
                            bot.send_message(id_usuario, mensagem_green[25].replace('\n','').replace('[RESULTADO]', ' | '.join(resultados)), parse_mode='HTML')
                            time.sleep(1)
                            # Validando o STOP WIN
                            validar_stop_win()


                        except:
                            pass

                    except:
                        pass

                    

                    print('==================================================')
                    validador_sinal = 0
                    contador_cash = 0
                    contador_passagem = 0
                    lista_resultados = lista_resultados_sinal
                    return

            
                else:
                    print('LOSSS')
                    print('==================================================')

                    bot.send_message(id_usuario, '😥 NÃO FOI DESSA VEZ')

                    # VALIDANDO SE A APOSTA É NO ZERO ESTÁ ATIVA
                    if apostando_zero == True:
                        apostando_zero = False
                        return


        except Exception as a:
            logger.error('Exception ocorrido no ' + repr(a))
            logarSite()
            historico_resultados = resgatar_historico()
            continue
            

def elemento_apostas(estrategia):

    global aposta_um, aposta_um_clicado, aposta_dois, aposta_dois_clicado, aposta_protecao, aposta_protecao_clicado

    elementos = {

            '1º/2ªcoluna': ['//*[@class="table-cell--Wz6uJ table-cell_side-bottom-column--OqCSy"]', 
                            '//*[@class="table-cell--Wz6uJ table-cell_side-bottom-column--OqCSy table-cell_hover-highlight--fYheT"]',
                            '//*[@class="table-cell--Wz6uJ table-cell_side-middle-column--T3Lzx"]',
                            '//*[@class="table-cell--Wz6uJ table-cell_side-middle-column--T3Lzx table-cell_hover-highlight--fYheT"]'
                            ],

            '2ª/3ªcoluna': ['//*[@class="table-cell--Wz6uJ table-cell_side-middle-column--T3Lzx"]',
                            '//*[@class="table-cell--Wz6uJ table-cell_side-middle-column--T3Lzx table-cell_hover-highlight--fYheT"]',
                            '//*[@class="table-cell--Wz6uJ table-cell_side-top-column--WUiBj"]',
                            '//*[@class="table-cell--Wz6uJ table-cell_side-top-column--WUiBj table-cell_hover-highlight--fYheT"]'
                            ],

            '1º/3ªcoluna': ['//*[@class="table-cell--Wz6uJ table-cell_side-bottom-column--OqCSy"]', 
                            '//*[@class="table-cell--Wz6uJ table-cell_side-bottom-column--OqCSy table-cell_hover-highlight--fYheT"]',
                            '//*[@class="table-cell--Wz6uJ table-cell_side-top-column--WUiBj"]',
                            '//*[@class="table-cell--Wz6uJ table-cell_side-top-column--WUiBj table-cell_hover-highlight--fYheT"]'
                            ],

            '1º/2ªduzia': ['//*[@class="table-cell--Wz6uJ table-cell_side-first-dozen--lHojX"]',
                           '//*[@class="table-cell--Wz6uJ table-cell_side-first-dozen--lHojX"]',
                           '//*[@class="table-cell--Wz6uJ table-cell_side-second-dozen--bjWFT"]',
                           '//*[@class="table-cell--Wz6uJ table-cell_side-second-dozen--bjWFT"]'
                           ],

            '2ª/3ªduzia': ['//*[@class="table-cell--Wz6uJ table-cell_side-second-dozen--bjWFT"]',
                           '//*[@class="table-cell--Wz6uJ table-cell_side-second-dozen--bjWFT"]',
                           '//*[@class="table-cell--Wz6uJ table-cell_side-third-dozen--XTlgH"]',
                           '//*[@class="table-cell--Wz6uJ table-cell_side-third-dozen--XTlgH"]'
                           ],

            '1º/3ªduzia': ['//*[@class="table-cell--Wz6uJ table-cell_side-first-dozen--lHojX"]',
                           '//*[@class="table-cell--Wz6uJ table-cell_side-first-dozen--lHojX"]',
                           '//*[@class="table-cell--Wz6uJ table-cell_side-third-dozen--XTlgH"]',
                           '//*[@class="table-cell--Wz6uJ table-cell_side-third-dozen--XTlgH"]'
                           ],


            'cor vermelho': ['//*[@class="table-cell--Wz6uJ table-cell_side-red--ot8JV"]',
                             '//*[@class="table-cell--Wz6uJ table-cell_side-red--ot8JV table-cell_hover-highlight--fYheT"]'
                             ],

            'cor preto': ['//*[@class="table-cell--Wz6uJ table-cell_side-black--Tj9Du"]',
                          '//*[@class="table-cell--Wz6uJ table-cell_side-black--Tj9Du table-cell_hover-highlight--fYheT"]'
                          ],
        
            'números baixos': ['//*[@class="table-cell--Wz6uJ table-cell_side-low--YDiON"]',
                               '//*[@class="table-cell--Wz6uJ table-cell_side-low--YDiON table-cell_hover-highlight--fYheT"]'
                               ],

            'números altos': ['//*[@class="table-cell--Wz6uJ table-cell_side-high--ZPKxS"]',
                              '//*[@class="table-cell--Wz6uJ table-cell_side-high--ZPKxS table-cell_hover-highlight--fYheT"]'
                              ]
        
        
        
        
        }
    

    for elemento in elementos:
        if estrategia[3] == elemento:
            if '/' in elemento:
                aposta_um = elementos[elemento][0]
                aposta_um_clicado = elementos[elemento][1]
                aposta_dois = elementos[elemento][2]
                aposta_dois_clicado = elementos[elemento][3]

                return aposta_um, aposta_um_clicado, aposta_dois, aposta_dois_clicado
            
            else:
                aposta_um = elementos[elemento][0]
                aposta_um_clicado = elementos[elemento][1]

                return aposta_um, aposta_um_clicado


            #print(dic_estrategia_usuario)
    

def msg_matingale(valor_gale, contador_cash):

    try:
        bot.send_message(id_usuario, f"🤞 TENTANDO RECUPERAÇÃO DE R${valor_gale} NO GALE "+str(contador_cash) + '\n' + \
                                     f'🟢 COBRINDO O ZERO COM 10% DO VALOR DO GALE.'
                                     )
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


valor_entrada = ''
stop_gain = ''
stop_loss = ''
martingale = ''
fator_gale = ''
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
did_onde_apostar = {}
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
fezinha = ''


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


# VERIFICANDO SE TEM ALGUMA ESTRATEGIA NO TXT E CARREGAR
with open ('estrategias.txt', 'r', encoding='UTF-8') as arquivo:
    estrategias_salvas = arquivo.readlines()

    if estrategias_salvas != [] :
        txt_estrategias_vazio = False
        for e in estrategias_salvas:
            e = e.replace('\n','')
            lista_estrategias.append(e)

    else:
        txt_estrategias_vazio = True
        pass


# CARREGAR OPÇÕES DE ENTRADA
with open ('entradas.txt', 'r', encoding='UTF-8') as arquivo:
    opcoes_entradas = arquivo.readlines()

    if opcoes_entradas != [] :
        valor_entrada = float(opcoes_entradas[0].split(',')[1])
        stop_gain = float(opcoes_entradas[1].split(',')[1])
        stop_loss = float(opcoes_entradas[2].split(',')[1])
        martingale = float(opcoes_entradas[3].split(',')[1])
        fator_gale = float(opcoes_entradas[4].split(',')[1])
        fezinha = opcoes_entradas[5].split(',')[1]
        
    else:
        txt_entradas_vazio = True
        pass
        
        
        




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




@bot.message_handler(commands=['💵 Saldo Atual'])
def enviar_saldo_atual(message):
    
    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=3)
    markup = markup.add('/start','✅ Ativar Bot', '💰 Opções Apostas', '💵 Saldo Atual', '⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual', '🛑 Pausar Bot')

    while True:
        try:

            saldo_atual = browser.find_element_by_xpath('//*[@class="fit-container--zbc9x"]').text
            message_final = bot.reply_to(message, f"💰 SALDO ATUAL: {saldo_atual}", reply_markup=markup)
            break
            
        except:
            message_final = bot.reply_to(message, "Ocorreu um Erro ao Pegar o Saldo. Fazendo uma Nova Tentativa....", reply_markup=markup )
            logarSite()



@bot.message_handler(commands=['⏲ Ultimos_Resultados'])
def ultimosResultados(message):
    
    if botStatus == 0 and dicionario_roletas == {}:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot', '💰 Opções Apostas', '💵 Saldo Atual', '⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual', '🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Ative o bot primeiro! ", reply_markup=markup)
       
    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot', '💰 Opções Apostas', '💵 Saldo Atual', '⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual', '🛑 Pausar Bot')

        bot.reply_to(message, "🤖 Ok! Mostrando Ultimos Resultados das Roletas", reply_markup=markup)
        try:
            
            for key, value in dicionario_roletas.items():
                #print(key, value)
                bot.send_message(message.chat.id, f'{key}{value}')

        except:
            pass



@bot.message_handler(commands=['⚙🧠 Cadastrar_Estratégia'])
def cadastrarEstrategia(message):
    global contador_passagem

    if contador_passagem == 0:
        #Init keyboard markup
        markup_tipo = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
        
        markup_tipo = markup_tipo.add('◀ Voltar', 'REPETIÇÃO', 'AUSÊNCIA', 'ESTRATÉGIAS PADRÕES')    

        message_tipo_estrategia = bot.reply_to(message, "🤖 Ok! Escolha o tipo de estratégia ou cadastrar estratégias padrões 👇", reply_markup=markup_tipo)
        bot.register_next_step_handler(message_tipo_estrategia, registrarTipoEstrategia)
    

    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot', '💰 Opções Apostas', '💵 Saldo Atual', '⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual', '🛑 Pausar Bot')

        message_estrategia = bot.reply_to(message, "🤖⛔ Estou validando uma estratégia! Tente novamente em alguns instanstes.", reply_markup=markup)



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
        markup_estrategias = generate_buttons_estrategias([f'{estrategia}' for estrategia in lista_estrategias], markup)    
        markup_estrategias.add('◀ Voltar')

        message_excluir_estrategia = bot.reply_to(message, "🤖 Escolha a estratégia a ser excluída 👇", reply_markup=markup_estrategias)
        bot.register_next_step_handler(message_excluir_estrategia, registrarEstrategiaExcluida)
    
    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot', '💰 Opções Apostas', '💵 Saldo Atual', '⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual', '🛑 Pausar Bot')

        message_excluir_estrategia = bot.reply_to(message, "🤖⛔ Estou validando uma estratégia! Tente novamente em alguns instanstes.", reply_markup=markup)



@bot.message_handler(commands=['🧠📜 Estratégias_Cadastradas'])
def estrategiasCadastradas(message):
    global estrategia
    global estrategias
    global lista_estrategias

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup = markup.add('/start','✅ Ativar Bot', '💰 Opções Apostas', '💵 Saldo Atual', '⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual', '🛑 Pausar Bot')

    if lista_estrategias != []:
        bot.reply_to(message, "🤖 Ok! Listando estratégias", reply_markup=markup)

        for estrategia in lista_estrategias:
            #print(estrategia)
            bot.send_message(message.chat.id, f'{estrategia}')
    
    else:
        bot.reply_to(message, "🤖 Nenhuma estratégia cadastrada ❌", reply_markup=markup)



@bot.message_handler(commands=['📈 Gestão'])
def gestao(message):
    global placar
    global resultados_sinais
    global placar_estrategias

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup = markup.add('/start','✅ Ativar Bot', '💰 Opções Apostas', '💵 Saldo Atual', '⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual', '🛑 Pausar Bot')

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



@bot.message_handler(commands=['📊 Placar Atual'])
def placar_atual(message):
    global placar
    global resultados_sinais

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup = markup.add('/start','✅ Ativar Bot', '💰 Opções Apostas', '💵 Saldo Atual', '⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual', '🛑 Pausar Bot')

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

    
    if botStatus == 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot', '💰 Opções Apostas', '💵 Saldo Atual', '⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual', '🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Bot já está pausado ", reply_markup=markup)

    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot', '💰 Opções Apostas', '💵 Saldo Atual', '⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual', '🛑 Pausar Bot')

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

    global id_usuario

    if str(message.chat.id) in ids:

        id_usuario = message.chat.id


        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot', '💰 Opções Apostas', '💵 Saldo Atual', '⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual', '🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message, "🤖 Bot Automático para Roletas Iniciado! ✅ Escolha uma opção 👇",
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
        global botStatus
        global parar
        global reladiarioenviado
        global contador_outra_oportunidade
        global browser
        global dicionario_estrategia_usuario
        global contador_passagem, saldo_inicial

        print('Ativar Bot')

        if botStatus == 1:

            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            markup = markup.add('/start','✅ Ativar Bot', '💰 Opções Apostas', '💵 Saldo Atual', '⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual', '📈 Gestão', '🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖⛔ Bot já está ativado",
                                reply_markup=markup)

        
        elif lista_estrategias == []:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            markup = markup.add('/start','✅ Ativar Bot', '💰 Opções Apostas', '💵 Saldo Atual', '⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual', '🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖⛔ Cadastre no mínimo 1 estratégia antes de iniciar",
                                reply_markup=markup)

        
        else:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            markup = markup.add('/start','✅ Ativar Bot', '💰 Opções Apostas', '💵 Saldo Atual', '⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual', '🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖 Ok! Bot Ativado com sucesso! ✅",
                                    reply_markup=markup)
            
            botStatus = 1
            reladiarioenviado = 0
            parar=0
            contador_passagem = 0

            print('##################################################  INICIANDO AS ANÁLISES  ##################################################')
            print()
            saldo_inicial = enviar_saldo()
            coletarResultados() # Analisando os Dados
       

    if message_opcoes.text in ['💰 Opções Apostas']:
        print('Apostas')

        if str(message_opcoes.chat.id) in ids:

            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            markup = markup.add(
                                f'Valor Entrada = {valor_entrada}',
                                f'Stop Gain = {stop_gain}',
                                f'Stop Loss = {stop_loss}',
                                f'Martingale = {martingale}',
                                f'Fator Gale = {fator_gale}',
                                f'FÉZINHA NO 0 = {fezinha}',
                                '◀ Voltar')

            escolha_config_entrada = bot.reply_to(message_opcoes, "🤖 Perfeito! Escolha uma opção 👇",
                                    reply_markup=markup)
            
            #Here we assign the next handler function and pass in our response from the user. 
            bot.register_next_step_handler(escolha_config_entrada, opcoes_config_entrada)
        
        else:
            message_error = bot.reply_to(message_opcoes, "🤖 Você não tem permissão para acessar este Bot ❌🚫")


    if message_opcoes.text in ['💵 Saldo Atual']:
        print('Enviar Saldo')
        enviar_saldo_atual(message_opcoes)

        
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



@bot.message_handler()
def registrarTipoEstrategia(message_tipo_estrategia):
    global resposta_usuario
    global lista_estrategias

    if message_tipo_estrategia.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot', '💰 Opções Apostas', '💵 Saldo Atual', '⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual', '🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_tipo_estrategia, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        return


    if message_tipo_estrategia.text in ['ESTRATÉGIAS PADRÕES']:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot', '💰 Opções Apostas', '💵 Saldo Atual', '⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual', '📈 Gestão', '🛑 Pausar Bot')

        estrategias_padroes = ( ['repetição', '1ºcoluna', '3', '2ª/3ªcoluna'],
                                ['repetição', '2ªcoluna', '3', '1º/3ªcoluna'],
                                ['repetição', '3ªcoluna', '3', '1º/2ªcoluna'],
                                ['repetição', '1ºduzia', '3', '2ª/3ªduzia'],
                                ['repetição', '2ªduzia', '3', '1º/3ªduzia'],
                                ['repetição', '3ªduzia', '3', '1º/2ªduzia'],
                                ['repetição', 'cor vermelho', '4', '1º/3ªcoluna'],
                                ['repetição', 'cor preto', '4', '1º/2ªcoluna'],
                                ['repetição', 'números par(es)', '3', '2ª/3ªduzia'],
                                ['repetição', 'números impar(es)', '4', '1º/3ªduzia'])

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









def opcoes_config_entrada(escolha_config_entrada):
    global resposta_usuario


    if escolha_config_entrada.text in ['◀ Voltar']:

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot', '💰 Opções Apostas', '💵 Saldo Atual', '⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual', '🛑 Pausar Bot')

        #arkup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        escolha_inicial = bot.reply_to(escolha_config_entrada, "🤖 Certo! Escolha uma opção 👇",
                                reply_markup=markup)
        
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(escolha_inicial, opcoes)


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
    

    if escolha_config_entrada.text.split(' =')[0] in ['FÉZINHA NO 0']:
        
        resposta_usuario = escolha_config_entrada.text.split(' =')[0]

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('SIM', 'NAO', '◀ Voltar')

        escolha_fezinha = bot.reply_to(escolha_config_entrada, "🤖 Perfeito! Escolha uma opção 👇",
                                reply_markup=markup)
        

        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(escolha_fezinha, registra_dados_usuario)

            




def registra_dados_usuario(dado_usuario):
    global valor_entrada, stop_gain, stop_loss, protecao, martingale, fator_gale, martingale_empate, fator_gale_empate, fezinha

    try:

        if dado_usuario.text in ['◀ Voltar']:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            markup = markup.add(
                                f'Valor Entrada = {valor_entrada}',
                                f'Stop Gain = {stop_gain}',
                                f'Stop Loss = {stop_loss}',
                                f'Martingale = {martingale}',
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
        
        if resposta_usuario == 'Martingale':
            martingale = int(dado_usuario.text)

        if resposta_usuario == 'Fator Gale':
            fator_gale = float(dado_usuario.text)

        if resposta_usuario == 'FÉZINHA NO 0':
            fezinha = dado_usuario.text


        # ATUALIZANDO ARQUIVO TXT
        with open('entradas.txt', 'w', encoding='UTF-8') as file:
            file.write(
f"Entrada,{valor_entrada}\n\
Stop Win,{stop_gain}\n\
Stop Loss,{stop_loss}\n\
Martingale,{martingale}\n\
Fator Gale,{fator_gale}\n\
Fezinha no 0,{fezinha}"
        )


        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add(
                            f'Valor Entrada = {valor_entrada}',
                            f'Stop Gain = {stop_gain}',
                            f'Stop Loss = {stop_loss}',
                            f'Martingale = {martingale}',
                            f'Fator Gale = {fator_gale}',
                            f'FÉZINHA NO 0 = {fezinha}',
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

            saldo_atual = browser.find_element_by_xpath('//*[@class="fit-container--zbc9x"]').text
            enviar_saldo = bot.send_message(id_usuario, f"💰 SALDO ATUAL: {saldo_atual}")
            
            return saldo_atual
        
        except:

            enviar_saldo = bot.send_message(id_usuario, "⚠️ Ocorreu um Erro ao Pegar Saldo. Fazendo uma Nova Tentativa...")
            logarSite()
            continue
    

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
        markup = markup.add('/start','✅ Ativar Bot', '💰 Opções Apostas', '💵 Saldo Atual', '⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual', '🛑 Pausar Bot')

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
    global lista_estrategias, txt_estrategias_vazio

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup = markup.add('/start','✅ Ativar Bot', '💰 Opções Apostas', '💵 Saldo Atual', '⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual', '🛑 Pausar Bot')

    resposta_usuario4 = ond_apostar.text.lower()
    onde_apostar = ([resposta_usuario, resposta_usuario2, resposta_usuario3, resposta_usuario4])
    lista_estrategias.append(onde_apostar)
    print(onde_apostar)

    #Registrando Estrategia no TXT

    if txt_estrategias_vazio == False:
        with open('estrategias.txt', 'a', encoding='UTF-8') as arq:
            arq.write('\n'+str(onde_apostar))
    
    else:
        with open('estrategias.txt', 'w', encoding='UTF-8') as arq:
            arq.write(str(onde_apostar))
            txt_estrategias_vazio = False


    bot.reply_to(ond_apostar, "🤖 Estratégia Cadastrada ✅", reply_markup=markup)


def registrarEstrategiaExcluida(message_excluir_estrategia):
    global estrategia
    global estrategias

    if message_excluir_estrategia.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot', '💰 Opções Apostas', '💵 Saldo Atual', '⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual', '🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_excluir_estrategia, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        
        return
    

    estrategia_excluir = message_excluir_estrategia.text
    
    ''' Excluindo a estratégia '''
    for estrategia in lista_estrategias:
        if estrategia_excluir == str(estrategia):
            lista_estrategias.remove(estrategia)
            break

    
    ''' SUBSTITUINDO estrategia do TXT '''
    c=0
    arquivo = open('estrategias.txt', 'w', encoding='UTF-8')
    for for_estrategia in lista_estrategias:
        if c == 0:
            arquivo.write(str(for_estrategia))
            c+=1

        else:
            arquivo.write('\n'+str(for_estrategia))
            
    arquivo.close()

    ''' Excluindo o placar da estratégia'''
    for pe in placar_estrategias:
        if estrategia_excluir == pe[0]:
            placar_estrategias.remove(pe)





    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup = markup.add('/start','✅ Ativar Bot', '💰 Opções Apostas', '💵 Saldo Atual', '⚙🧠 Cadastrar Estratégia', '🧠📜 Estratégias Cadastradas', '🗑🧠 Apagar Estratégia', '⏲ Ultimos Resultados', '📊 Placar Atual', '📈 Gestão', '🛑 Pausar Bot')

    bot.reply_to(message_excluir_estrategia, "🤖 Estratégia excluída com sucesso! ✅", reply_markup=markup)








bot.infinity_polling()













