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
from selenium.webdriver.common.action_chains import ActionChains


print()
print('                                #################################################################')
print('                                ################  BOT ROLETA XXXTREME AUTO.   ###################')
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

    lobby_cassinos = 'https://launcher.betfair.com/?gameId=xxxtreme-lr-cev&returnURL=https%3A%2F%2Fcasino.betfair.com%2Fpt-br%2Fp%2Fcassino-ao-vivo&launchProduct=gaming&RPBucket=gaming&mode=real&dataChannel=ecasino'
    
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

    c=0
    while 0 < 10:
        try:
            iframe = browser.find_element_by_id('game-client-iframe-id')
            browser.switch_to_frame(iframe)

            iframe2 = browser.find_element_by_xpath('/html/body/div[6]/div[2]/iframe')
            browser.switch_to_frame(iframe2)

            break
        except:
            c+=1
            time.sleep(3)


def coletarResultados():
    global url_cassino
    global contador_passagem
    global horario_atual
    global aposta, numero_multiplicador

    url_cassino = ''
    lista_registrar_resultado = []
    numero_multiplicador = 0

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

            historico_resultados = browser.find_elements_by_xpath('//*[@class="recentNumbers--9cf87 immersive2--49761"]')
            
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
            
            #VALIDANDO SE O RESULTADO VEIO MULTIPLICADOR ACIMA DE 50X
            if 'x' in lista_resultados[0] or 'X' in lista_resultados[0]:
                numero_multiplicador = lista_resultados[0].split('x')[0]
            
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

            ''' Chama a função que valida a estratégia para enviar o sinal Telegram'''
            validarEstrategia(historico_resultados, lista_resultados)
            print('=' * 150)

            continue
    
        except:

            logarSite()
            continue 


def validarEstrategia(historico_resultados, lista_resultados):
    global estrategia
    global contador_passagem
    global aposta_protecao, aposta_protecao_clicado, sinal_repeticao_numeros, saldo_antes_aposta

    try:
        sinal = False
        saldo_antes_aposta = browser.find_element_by_xpath('//*[@class="amount--bb99f"]').text.split('R$ ')[1]
            
        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            return
        else:
            pass


        ultimo_numero = lista_resultados[0]
        sinal_repeticao_numeros = 0

        # Validando o horario para envio do relatório diário
        validaData()

        # VALIDAR SE FOI DESCONECTADO
        if browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[6]/div/div[2]/div[2]/button') or browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[5]/div/div[2]/div/div[3]/button'):
            browser.refresh()
            logarSite()
            return
        
        print('Historico_Roleta --> ', 'Roleta XXXTREME', lista_resultados)

        #VALIDANDO ESTRATEGIA DE REPETIÇÃO DE NÚMERO
        for i in lista_resultados[:8]:
            if lista_resultados[:repeticao_numeros].count(i) > 1:
                sinal = True
                break

        if sinal == True:
            
            sinal_repeticao_numeros = 1

            print('PADRÃO DE REPETIÇÃO DE NÚMEROS CONFIRMADO! TENTATIVA DE APOSTA!!!!')
        
            time.sleep(8)
            conseguiu_apostar = apostar(valor_entrada)

            if conseguiu_apostar == True:
                #### ENVIANDO SINAL PRO TELEGREM #####
                enviarSinalTelegram(valor_entrada)
                print('=' * 150)

                #### CHECANDO SINAL ENVIADO ####
                checkSinalEnviado(lista_resultados, historico_resultados)
                time.sleep(1)
                return
            else:
                print('TEMPO PARA APOSTAS ESGOTADO')
        

        #VALIDANDO ESTRATEGIA DE NÚMERO 0
        if ultimo_numero == '0' or ultimo_numero == '00':

            print('PADRÃO DO ZERO CONFIRMADO! TENTATIVA DE APOSTA!!!!')
        
            time.sleep(8)
            conseguiu_apostar = apostar(valor_entrada)

            if conseguiu_apostar == True:
                #### ENVIANDO SINAL PRO TELEGREM #####
                enviarSinalTelegram(valor_entrada)
                print('=' * 150)

                #### CHECANDO SINAL ENVIADO ####
                checkSinalEnviado(lista_resultados, historico_resultados)
                time.sleep(1)
                return
            else:
                print('TEMPO PARA APOSTAS ESGOTADO')


        #VALIDANDO ESTRATEGIA DE MULTIPLICADOR ACIMA DE 50X
        if int(numero_multiplicador) > 50:

            print('PADRÃO DO NÚMERO MULTIPLICADOR CONFIRMADO! TENTATIVA DE APOSTA!!')
        
            time.sleep(8)
            conseguiu_apostar = apostar(valor_entrada)

            if conseguiu_apostar == True:

                #### ENVIANDO SINAL PRO TELEGREM #####
                enviarSinalTelegram(valor_entrada)
                print('=' * 150)

                #### CHECANDO SINAL ENVIADO ####
                checkSinalEnviado(lista_resultados, historico_resultados)
                time.sleep(1)
                return
            
            else:
                print('TEMPO PARA APOSTAS ESGOTADO')

                


    except:
        # VALIDAR SE FOI DESCONECTADO
        if browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[6]/div/div[2]/div[2]/button'):
            browser.refresh()
            logarSite()
            pass

        else:
            pass


def enviarSinalTelegram(valor_entrada):
    global table_sinal

    ''' Lendo o arquivo txt config-mensagens '''
    txt = open("config-mensagens.txt", "r", encoding="utf-8")
    arquivo_mensagem = txt.readlines()
    mensagem_sinal = arquivo_mensagem[1].split(',')

    ''' Estruturando mensagem '''
    txt = open("config-mensagens.txt", "r", encoding="utf-8")
    mensagem_sinal = txt.readlines()

    table_sinal = mensagem_sinal[11].replace('\n','') + '\n' +\
                  mensagem_sinal[13].replace('\n','').replace('[VALOR_APOSTA]', str(valor_entrada))
    
    ''' Enviando mensagem Telegram '''
    try:

        bot.send_message(id_usuario, table_sinal, parse_mode='HTML')
    
    except:
        pass


def checkSinalEnviado(lista_resultados, historico_resultados):
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
    global data_hoje, numero_multiplicador
    
    contador_entradas = 0
    cond_repeticao_entrada = repeticao_entrada if sinal_repeticao_numeros == 0 else sinal_repeticao_numeros

    # Validando se foi solicitado o stop do BOT
    if parar != 0:
        return
    else:
        pass

    # Validando o horario para envio do relatório diário
    validaData()
    #auto_refresh()

    while contador_entradas <= cond_repeticao_entrada:
        try:

            # VALIDAR SE FOI DESCONECTADO
            if browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[6]/div/div[2]/div[2]/button') or browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[5]/div/div[2]/div/div[3]/button'):
                browser.refresh()
                logarSite()
                return
            

            ''' Lendo novos resultados para validação da estratégia'''
            # Formata o historico em lista
            lista_resultados_sinal = historico_resultados[0].text.split('\n') 
            #print(historico_roleta)

            ''' Validando se tem dado Vazio '''
            if '' in lista_resultados_sinal:
                browser.refresh()
                logarSite()

            #VALIDANDO SE O RESULTADO VEIO MULTIPLICADOR ACIMA DE 50X
            if 'x' in lista_resultados_sinal[0] or 'X' in lista_resultados_sinal[0]:
                numero_multiplicador = lista_resultados_sinal[0].split('x')[0]
            else:
                numero_multiplicador = None

            #REMOVENDO X DOS RESULTADOS:
            for r in lista_resultados_sinal:
                if 'x' in r:
                    lista_resultados_sinal.remove(r)
                    

            ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
            if lista_resultados[:3] != lista_resultados_sinal[:3]:
                
                # VALIDANDO WIN OU LOSS
                if numero_multiplicador != None:
                
                    print('WIN')
                    contador_entradas=0

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
                            bot.send_message(id_usuario, mensagem_green[23].replace('\n',''), parse_mode='HTML')
                            time.sleep(1)
                            
                        except:
                            pass

                    except:
                        pass

                
                    print('==================================================')
                    
                    lista_resultados = lista_resultados_sinal
                    
                    apostar(valor_entrada)

            
                else:
                    print('LOSSS')
                    print('==================================================')
                    
                    contador_entradas+=1

                    # editando mensagem
                    try:
                        
                        ''' Lendo o arquivo txt config-mensagens '''
                        txt = open("config-mensagens.txt", "r", encoding="utf-8")
                        mensagem_red = txt.readlines()

                        try:
                            
                            bot.send_message(id_usuario, mensagem_red[25].replace('\n',''), parse_mode='HTML')
                        
                        except:
                            pass

                        
                    except:
                        pass

                    # Preenchendo arquivo txt
                    placar_loss +=1
                    placar_geral = placar_win + placar_loss
                    with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                        arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}")
                        
                    # Preenchendo dados do LOSS
                    with open("historico_loss.txt", "a") as arquivo: 
                        arquivo.write('\n'+datetime.now().strftime('%d-%m-%Y %H:%M:%S')+' - '+ str(estrategia))

                    lista_resultados = lista_resultados_sinal

                    apostar(valor_entrada)
                    

        except Exception as a:
            logger.error('Exception ocorrido no ' + repr(a))
            logarSite()
            historico_resultados = resgatar_historico()
            continue
    

    try:
                            
        bot.send_message(id_usuario, " ⚠️ SEQUENCIA DE ENTRADAS FINALIZADA! VOLTANDO A ANALISAR OS PADRÕES.", parse_mode='HTML')
    
    except:
        pass


def apostar(valor_aposta):

    moedas = browser.find_elements_by_xpath('//*[@class="expandedChipStack--0a379"]//*[name()="text"]')

    if browser.find_elements_by_xpath('//*[@class="dddRacetrack-wrapper"]/*[@data-bet-spot-id="17"]') != []:
        numero17 = '//*[@class="dddRacetrack-wrapper"]/*[@data-bet-spot-id="17"]'
        numero9 = '//*[@class="dddRacetrack-wrapper"]/*[@data-bet-spot-id="9"]'
    
    else:
        numero17 = '//*[@class="classicRacetrack-wrapper"]/*[@data-bet-spot-id="17"]'
        numero9 = '//*[@class="classicRacetrack-wrapper"]/*[@data-bet-spot-id="17"]'

    botao_mais = '//*[@class="plus--4a8fc"]'

    #AUMENTANDO O NÚMERO DE VIZINHOS
    while True:
        if browser.find_elements_by_xpath('//*[@class="plus--4a8fc"]') != []:
            ActionChains(browser).move_to_element(browser.find_element_by_xpath(botao_mais)).click().perform()

        break


    if valor_aposta == 1:
        #CLICANDO NA MOEDA 5
        try:

            for moeda in moedas:
                if moeda.text == '1':
                    ActionChains(browser).move_to_element(moeda).click().perform()
                    break               

            #DAR 1 CLICK
            ActionChains(browser).move_to_element(browser.find_element_by_xpath(numero17)).click().perform()
            time.sleep(1)
            ActionChains(browser).move_to_element(browser.find_element_by_xpath(numero9)).click().perform()
            time.sleep(1)

            saldo_apos_aposta = browser.find_element_by_xpath('//*[@class="amount--bb99f"]').text.split('R$ ')[1]
            if saldo_antes_aposta != saldo_apos_aposta:
                return True

            else:
                return False
            
        except:
            pass



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
valor_entrada = 0
repeticao_entrada = 0
repeticao_numeros = 0


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


# CARREGAR OPÇÕES DE ENTRADA
with open ('entradas.txt', 'r', encoding='UTF-8') as arquivo:
    opcoes_entradas = arquivo.readlines()

    if opcoes_entradas != [] :
        valor_entrada = float(opcoes_entradas[0].split(',')[1])
        repeticao_entrada = int(opcoes_entradas[1].split(',')[1])
        repeticao_numeros = int(opcoes_entradas[2].split(',')[1])
        
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
    markup = markup.add('/start','🟢 Ativar Bot', '💰 Valor Aposta', '💵 Saldo Atual', '🔂 Repetição Entrada', '🔂 Repetição Numeros', '⏲ Ultimos Resultados', '📊 Placar Atual', '🛑 Pausar Bot')

    while True:
        try:

            saldo_atual = browser.find_element_by_xpath('//*[@class="amount--bb99f"]').text
            message_final = bot.reply_to(message, f"💰 SALDO ATUAL: {saldo_atual}", reply_markup=markup)
            break
            
        except:
            message_final = bot.reply_to(message, "Ocorreu um Erro ao Pegar o Saldo. Fazendo uma Nova Tentativa....", reply_markup=markup )
            logarSite()



@bot.message_handler(commands=['⏲ Ultimos_Resultados'])
def ultimosResultados(message):
    
    if botStatus == 0 and dicionario_roletas == {}:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','🟢 Ativar Bot', '💰 Valor Aposta', '💵 Saldo Atual', '🔂 Repetição Entrada', '🔂 Repetição Numeros', '⏲ Ultimos Resultados', '📊 Placar Atual', '🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Ative o bot primeiro! ", reply_markup=markup)
       
    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','🟢 Ativar Bot', '💰 Valor Aposta', '💵 Saldo Atual', '🔂 Repetição Entrada', '🔂 Repetição Numeros', '⏲ Ultimos Resultados', '📊 Placar Atual', '🛑 Pausar Bot')

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
    markup = markup.add('/start','🟢 Ativar Bot', '💰 Valor Aposta', '💵 Saldo Atual', '🔂 Repetição Entrada', '🔂 Repetição Numeros', '⏲ Ultimos Resultados', '📊 Placar Atual', '🛑 Pausar Bot')

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
        markup = markup.add('/start','🟢 Ativar Bot', '💰 Valor Aposta', '💵 Saldo Atual', '🔂 Repetição Entrada', '🔂 Repetição Numeros', '⏲ Ultimos Resultados', '📊 Placar Atual', '🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Bot já está pausado ", reply_markup=markup)

    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','🟢 Ativar Bot', '💰 Valor Aposta', '💵 Saldo Atual', '🔂 Repetição Entrada', '🔂 Repetição Numeros', '⏲ Ultimos Resultados', '📊 Placar Atual', '🛑 Pausar Bot')

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
        markup = markup.add('/start','🟢 Ativar Bot', '💰 Valor Aposta', '💵 Saldo Atual', '🔂 Repetição Entrada', '🔂 Repetição Numeros', '⏲ Ultimos Resultados', '📊 Placar Atual', '🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message, "🤖 Bot Automático para Roletas Iniciado! ✅ Escolha uma opção 👇",
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
            markup = markup.add('/start','🟢 Ativar Bot', '💰 Valor Aposta', '💵 Saldo Atual', '🔂 Repetição Entrada', '🔂 Repetição Numeros', '⏲ Ultimos Resultados', '📊 Placar Atual', '🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖⛔ Bot já está ativado",
                                reply_markup=markup)

        
        else:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            markup = markup.add('/start','🟢 Ativar Bot', '💰 Valor Aposta', '💵 Saldo Atual', '🔂 Repetição Entrada', '🔂 Repetição Numeros', '⏲ Ultimos Resultados', '📊 Placar Atual', '🛑 Pausar Bot')

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
       

    if message_opcoes.text in ['💰 Valor Aposta']:
        print('Apostas')

        if str(message_opcoes.chat.id) in ids:

            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            markup = markup.add('◀ Voltar')

            escolha_config_entrada = bot.reply_to(message_opcoes, "🤖 Perfeito! Escolha o valor da entrada 👇",
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

    
    if message_opcoes.text in ['⏲ Ultimos Resultados']:
        print('Ultimos Resultados')
        ultimosResultados(message_opcoes)


    if message_opcoes.text in ['🔂 Repetição Entrada']:
        print('Repetição Entrada')

        if str(message_opcoes.chat.id) in ids:

            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            markup = markup.add('◀ Voltar')

            escolha_repeticao_entrada = bot.reply_to(message_opcoes, "🤖 Perfeito! Escolha a Repetição de Entrada 👇",
                                    reply_markup=markup)
            
            #Here we assign the next handler function and pass in our response from the user. 
            bot.register_next_step_handler(escolha_repeticao_entrada, registra_repeticao_entrada)
        
        else:
            message_error = bot.reply_to(message_opcoes, "🤖 Você não tem permissão para acessar este Bot ❌🚫")


    if message_opcoes.text in ['🔂 Repetição Numeros']:
        print('Repetição Entrada')

        if str(message_opcoes.chat.id) in ids:

            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            markup = markup.add('◀ Voltar')

            escolha_repeticao_numeros = bot.reply_to(message_opcoes, "🤖 Perfeito! Escolha a Quantidade de Repetição de Números 👇",
                                    reply_markup=markup)
            
            #Here we assign the next handler function and pass in our response from the user. 
            bot.register_next_step_handler(escolha_repeticao_numeros, registra_repeticao_numeros)
        
        else:
            message_error = bot.reply_to(message_opcoes, "🤖 Você não tem permissão para acessar este Bot ❌🚫")



def opcoes_config_entrada(escolha_config_entrada):
    global resposta_usuario, valor_entrada

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup = markup.add('/start','🟢 Ativar Bot', '💰 Valor Aposta', '💵 Saldo Atual', '🔂 Repetição Entrada', '🔂 Repetição Numeros', '⏲ Ultimos Resultados', '📊 Placar Atual', '🛑 Pausar Bot')

    if escolha_config_entrada.text in ['◀ Voltar']:

        escolha_inicial = bot.reply_to(escolha_config_entrada, "🤖 Certo! Escolha uma opção 👇",
                                reply_markup=markup)
        
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(escolha_inicial, opcoes)

    
    valor_entrada = float(escolha_config_entrada.text)

    # ATUALIZANDO ARQUIVO TXT
    with open('entradas.txt', 'w', encoding='UTF-8') as file:
        file.write(
f"Entrada,{valor_entrada}\n\
repeticao_entrada,{repeticao_entrada}\n\
repeticao_numeros,{repeticao_numeros}")

    mensagem_final = bot.reply_to(escolha_config_entrada, f"🤖 Valor Cadastrado com Sucesso!✅",
                                    reply_markup=markup)


def registra_repeticao_entrada(escolha_repeticao_entrada):
    global repeticao_entrada

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup = markup.add('/start','🟢 Ativar Bot', '💰 Valor Aposta', '💵 Saldo Atual', '🔂 Repetição Entrada', '🔂 Repetição Numeros', '⏲ Ultimos Resultados', '📊 Placar Atual', '🛑 Pausar Bot')

    if escolha_repeticao_entrada.text in ['◀ Voltar']:

        escolha_inicial = bot.reply_to(escolha_repeticao_entrada, "🤖 Certo! Escolha uma opção 👇",
                                reply_markup=markup)
        
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(escolha_inicial, opcoes)

    
    repeticao_entrada = int(escolha_repeticao_entrada.text)

    # ATUALIZANDO ARQUIVO TXT
    with open('entradas.txt', 'w', encoding='UTF-8') as file:
        file.write(
f"Entrada,{valor_entrada}\n\
repeticao_entrada,{repeticao_entrada}\n\
repeticao_numeros,{repeticao_numeros}")

    mensagem_final = bot.reply_to(escolha_repeticao_entrada, f"🤖 Valor Cadastrado com Sucesso!✅",
                                    reply_markup=markup)


def registra_repeticao_numeros(escolha_repeticao_numeros):
    global repeticao_numeros

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup = markup.add('/start','🟢 Ativar Bot', '💰 Valor Aposta', '💵 Saldo Atual', '🔂 Repetição Entrada', '🔂 Repetição Numeros', '⏲ Ultimos Resultados', '📊 Placar Atual', '🛑 Pausar Bot')

    if escolha_repeticao_numeros.text in ['◀ Voltar']:

        escolha_inicial = bot.reply_to(escolha_repeticao_numeros, "🤖 Certo! Escolha uma opção 👇",
                                reply_markup=markup)
        
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(escolha_inicial, opcoes)

    
    repeticao_numeros = int(escolha_repeticao_numeros.text)

    # ATUALIZANDO ARQUIVO TXT
    with open('entradas.txt', 'w', encoding='UTF-8') as file:
        file.write(
f"Entrada,{valor_entrada}\n\
repeticao_entrada,{repeticao_entrada}\n\
repeticao_numeros,{repeticao_numeros}")

    mensagem_final = bot.reply_to(escolha_repeticao_numeros, f"🤖 Valor Cadastrado com Sucesso!✅",
                                    reply_markup=markup)


def enviar_saldo():
    global id_usuario, saldo_atual

    while True:
        try:

            saldo_atual = browser.find_element_by_xpath('//*[@class="amount--bb99f"]').text
            enviar_saldo = bot.send_message(id_usuario, f"💰 SALDO ATUAL: {saldo_atual}")
            
            return saldo_atual
        
        except:

            enviar_saldo = bot.send_message(id_usuario, "⚠️ Ocorreu um Erro ao Pegar Saldo. Fazendo uma Nova Tentativa...")
            logarSite()
            continue
    






bot.infinity_polling()













