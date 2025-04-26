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
import requests
import json



print()
print('                                #################################################################')
print('                                ###################   BOT ROLETAS EVOLUTION   ###################')
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
                #print(dic_estrategia_usuario)
        
        return dic_estrategia_usuario
    
    except:
        pass


def siteCassino():
    global cassinos

    cassinos = [
        #######  EVOLUTION
        ('EVOLUTION', 'Auto-Roulette VIP', 'https://estrelabet.com/ptb/games/livecasino/detail/normal/18451/evol_01rb77cq1gtenhmo_BRL', 'https://m.estrelabet.com/ptb/games/livecasino/detail/18451/evol_01rb77cq1gtenhmo_BRL'),
        ('EVOLUTION', 'Roulette', 'https://estrelabet.com/ptb/games/livecasino/detail/normal/18111/evol_vctlz20yfnmp1ylr_BRL', 'https://m.estrelabet.com/ptb/games/livecasino/detail/18111/evol_vctlz20yfnmp1ylr_BRL'),
        ('EVOLUTION', 'Brazilian Roulette', 'https://estrelabet.com/ptb/games/livecasino/detail/normal/20799/evol_o44hwr2lc3a7spdh_BRL', 'https://m.estrelabet.com/ptb/games/livecasino/detail/20799/evol_o44hwr2lc3a7spdh_BRL'),
        ('EVOLUTION', 'VIP Roulette', 'https://estrelabet.com/ptb/games/livecasino/detail/normal/18410/evol_wzg6kdkad1oe7m5k_BRL', 'https://m.estrelabet.com/ptb/games/livecasino/detail/18410/evol_wzg6kdkad1oe7m5k_BRL'),
        ('EVOLUTION', 'Speed Auto Roulette', 'https://estrelabet.com/ptb/games/livecasino/detail/normal/18294/evol_SpeedAutoRo00001_BRL', 'https://m.estrelabet.com/ptb/games/livecasino/detail/18294/evol_SpeedAutoRo00001_BRL'),
        ('EVOLUTION', 'Lightning Roulette', 'https://estrelabet.com/ptb/games/livecasino/detail/normal/18091/evol_LightningTable01_BRL', 'https://m.estrelabet.com/ptb/games/livecasino/detail/18091/evol_LightningTable01_BRL'),
        ('EVOLUTION', 'Speed Roulette', 'https://estrelabet.com/ptb/games/livecasino/detail/normal/18372/evol_lkcbrbdckjxajdol_BRL', 'https://m.estrelabet.com/ptb/games/livecasino/detail/18372/evol_lkcbrbdckjxajdol_BRL'),
        ('EVOLUTION', 'American Roulette', 'https://estrelabet.com/ptb/games/livecasino/detail/normal/18493/evol_AmericanTable001_BRL', 'https://m.estrelabet.com/ptb/games/livecasino/detail/18493/evol_AmericanTable001_BRL'),
        ('EVOLUTION', 'Immersive Roulette', 'https://estrelabet.com/ptb/games/livecasino/detail/normal/18503/evol_7x0b1tgh7agmf6hv_BRL', 'https://m.estrelabet.com/ptb/games/livecasino/detail/18503/evol_7x0b1tgh7agmf6hv_BRL'),
        ('EVOLUTION', 'Auto-Roulette', 'https://estrelabet.com/ptb/games/livecasino/detail/normal/18225/evol_48z5pjps3ntvqc1b_BRL', 'https://m.estrelabet.com/ptb/games/livecasino/detail/18225/evol_48z5pjps3ntvqc1b_BRL')
    
    ]
    
        #######  PRAGMATIC
        #('PRAGMATIC', 'Autoroleta1','https://estrelabet.com/ptb/games/livecasino/detail/normal/11375/225-BRL', 'https://m.estrelabet.com/ptb/games/livecasino/detail/11375/225-BRL'),
        #('PRAGMATIC', 'Roleta 1 Azure', 'https://estrelabet.com/ptb/games/livecasino/detail/normal/11376/227-BRL', 'https://m.estrelabet.com/ptb/games/livecasino/detail/11376/227-BRL'),
        #('PRAGMATIC', 'Roleta 10-Ruby', 'https://estrelabet.com/ptb/games/livecasino/detail/normal/19626/230-BRL', 'https://m.estrelabet.com/ptb/games/livecasino/detail/19626/230-BRL'),
        #('PRAGMATIC', 'Roleta 3-Macau', 'https://estrelabet.com/ptb/games/livecasino/detail/normal/9391/206-BRL', 'https://m.estrelabet.com/ptb/games/livecasino/detail/9391/206-BRL'),
        #('PRAGMATIC', 'Roleta Rápida1', 'https://estrelabet.com/ptb/games/livecasino/detail/normal/9357/203-BRL', 'https://m.estrelabet.com/ptb/games/livecasino/detail/9357/203-BRL')


        #('Roleta 8-Indiana', 'https://estrelabet.com/ptb/games/livecasino/detail/normal/19625/229-BRL', 'https://m.estrelabet.com/ptb/games/livecasino/detail/19625/229-BRL'),
        #('Roleta 2', 'https://estrelabet.com/ptb/games/livecasino/detail/normal/9356/201-BRL', 'https://m.estrelabet.com/ptb/games/livecasino/detail/9356/201-BRL'),
        #('Mega Roulete', 'https://estrelabet.com/ptb/games/livecasino/detail/normal/13518/204-BRL', 'https://m.estrelabet.com/ptb/games/livecasino/detail/13518/204-BRL'),
        #('Auto-Roulette La Partage', 'https://estrelabet.com/ptb/games/livecasino/detail/normal/18207/evol_f1f4rm9xgh4j3u2z_BRL')
        #('XXXtreme Lightning Roulette', 'https://estrelabet.com/ptb/games/livecasino/detail/normal/19884/evol_XxxtremeLigh0001_BRL'),
        #('Brazilian Lightning Roulette', 'https://estrelabet.com/ptb/games/livecasino/detail/normal/20801/evol_PorROULigh000001_BRL'),
        #('Instant Roulette', 'https://estrelabet.com/ptb/games/livecasino/detail/normal/18526/evol_InstantRo0000001_BRL'), /// NÃO MOSTRA OS ULTIMOS RESULTADOS
        #('Double Ball Roulette', 'https://estrelabet.com/ptb/games/livecasino/detail/normal/18437/evol_DoubleBallRou001_BRL'),
        #('Salon Privé Roulette', 'https://estrelabet.com/ptb/games/livecasino/detail/normal/18251/evol_mdkqijp3dctrhnuv_BRL'), /// SÓ PODE ENTRAR NO CASSINO COM 50K DE BANCA
        #('Gold Bar Roulette', 'https://estrelabet.com/ptb/games/livecasino/detail/normal/20161/evol_GoldbarRo0000001_BRL'),

    
def inicio():
    global browser
    global url
    global headers

    url = "https://app.bootbost.com.br/api/v1/call"
    headers = {
    'Content-Type': 'application/json'
    }

    # Definindo opções para o browser
    warnings.filterwarnings("ignore", category=DeprecationWarning) 
    chrome_options = webdriver.ChromeOptions() 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Opção para executar o prgrama em primeiro ou segundo plano
    #escolha = int(input('Deseja que o programa mostre o navegador? [1]SIM [2]NÃO --> '))
    #print()
    #time.sleep(1)
    #if escolha == 1:
    #    print('O programa será executado mostrando o navegador.\n')
    #else:
    #    print('O programa será executado com o navegador oculto.\n')
    #    chrome_options.add_argument("--headless")

    browser = webdriver.Chrome(ChromeDriverManager(version='114.0.5735.90').install(),chrome_options=chrome_options)


def logarSite():
    browser.get(r"https://estrelabet.com/ptb/games/livecasino/category/2")
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
        browser.find_element_by_xpath('//*[@id="trader-estrelabet"]/div[2]/div/a[1]').click() #Recusando cookies
        browser.find_element_by_xpath('//*[@id="trader-estrelabet"]/div[1]/div/a[1]').click() #Recusando cookies
    except:
        pass
    
    try:
        browser.find_element_by_xpath('//*[@id="username"]').send_keys(usuario) #Inserindo login
        browser.find_element_by_xpath('//*[@id="password-login"]').send_keys(senha) #Inserindo senha
        browser.find_element_by_xpath('//*[@id="header"]/div/div[1]/div/div[2]/app-login/form/div/div/div[2]').click() #Clicando no btn login
        time.sleep(5)
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


def coletarResultados(lista_roletas):
    global site_cassino_desktop
    global site_cassino_mobile
    global dicionario_roletas
    global contador_passagem
    global horario_atual
    global nome_fornecedor

    while True:

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass
        
        # Validando o horario para envio do relatório diário
        validaData()

        try:
            dicionario_roletas = {}
            lista_resultados = []

            for cassino in cassinos:

                # Validando se foi solicitado o stop do BOT
                if parar != 0:
                    break
                else:
                    pass

                ''' Valida se tem algum cassino cadastrado pelo usuário. Se não, analisa todos do grupo '''
                if lista_roletas == []:
                    pass
                
                elif cassino[1].upper() in lista_roletas:
                    pass
                
                else:
                    continue


                ''' Começa a analise do Cassino '''
                try:
                    nome_fornecedor = cassino[0]
                    nome_cassino = cassino[1]
                    site_cassino_desktop = cassino[2]
                    site_cassino_mobile = cassino[3]

                    ''' Entrando no cassino '''
                    browser.get(cassino[2])


                except:
                    pass

                while True:
                    try:

                        ''' Aguardando o elemento do historico aparecer'''
                        c=0
                        while c <= 10:

                            # Validando se foi solicitado o stop do BOT
                            if parar != 0:
                                break
                            else:
                                pass

                            ''' Acessando o Iframe do jogo '''
                            try:
                                iframe = browser.find_element_by_id('gm-frm')
                                browser.switch_to_frame(iframe)
                            except:
                                pass

                            # Acesso ao Segundo Iframe do Jogo
                            try:
                                iframe2 = browser.find_element_by_xpath('/html/body/div[6]/div[2]/iframe')
                                browser.switch_to_frame(iframe2)
                            except:
                                pass
                            
                            try:
                                ''' PEGANDO RESULTADOS DA EVOLUTION '''
                                if browser.find_elements_by_css_selector('.single-number--43778 .value--877c6'):
                                    numeros_recentes = browser.find_elements_by_css_selector('.single-number--43778 .value--877c6')
                                    break
                                
                                ''' PEGANDO RESULTADOS DA PRAGMATIC '''
                                if browser.find_elements_by_xpath('//*[@id="ministats-container"]/div/app-single-row-stats/div/table/tbody/tr/td'):
                                    numeros_recentes = browser.find_elements_by_xpath('//*[@id="ministats-container"]/div/app-single-row-stats/div/table/tbody/tr/td') 
                                    break  

                                else:
                                    time.sleep(3)
                                    c+=1
                                    continue
                            except:
                                time.sleep(5)
                                c+=1
                                continue
                        

                        # Validando se foi solicitado o stop do BOT
                        if parar != 0:
                            break
                        else:
                            pass

                        try:
                            for numeroRecente in numeros_recentes:
                                numero = numeroRecente.text
                                if 'x' not in numero:
                                    lista_resultados.append(numero)
                                else:
                                    lista_resultados.append(numero[:2])

                        except:
                            ''' CASO NÃO MAPEIE O RESULTADO, VERIFICAR SE ESTÁ LOGADO, SE TIVER, CONSULTAR RESULTADOS NOVAMENTE ''' 
                            if browser.find_elements_by_xpath('//*[@id="username"]'):
                                logarSite()
                            else:
                                break
                                
                
                        dicionario_roletas[nome_cassino] = lista_resultados
                        #print(dicionario_roletas)
                        print(horario_atual)
                        ''' Chama a função que valida a estratégia para enviar o sinal Telegram'''
                        validarEstrategia(dicionario_roletas, nome_cassino, lista_resultados, nome_fornecedor, lista_estrategias)
                        print('=' * 220)
                        lista_resultados = []
                        break

                        ''' Exceção se o cassino não estiver disponível'''
                    except:
                        if browser.find_elements_by_xpath('//*[@id="sticky-container"]/main/app-games/app-live-casino-detail/div[2]/div/div/message-box/div/div'):
                            if browser.find_element_by_xpath('//*[@id="sticky-container"]/main/app-games/app-live-casino-detail/div[2]/div/div/message-box/div/div').text == 'Algo deu errado. Contate o atendimento.':
                                break
                        break
        
        except:
            continue
                

def validarEstrategia(dicionario_roletas, nome_cassino, lista_resultados, nome_fornecedor, lista_estrategias):
    global estrategia
    global contador_passagem
    global lista_resultados_sinal
    global sequencia_minima

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
                enviarAlertaTelegram(dicionario_roletas, nome_cassino, sequencia_minima, estrategia, nome_fornecedor)
                time.sleep(1)

                ''' Verifica se a ultima condição bate com a estratégia para enviar sinal Telegram '''
                while True:
                    try:
                    
                        ''' Lendo novos resultados para validação da estratégia'''
                        ''' PEGANDO RESULTADOS DA EVOLUTION '''
                        if browser.find_elements_by_css_selector('.single-number--43778 .value--877c6'):
                            numeros_recentes_validacao = browser.find_elements_by_css_selector('.single-number--43778 .value--877c6')
                            
                        
                        ''' PEGANDO RESULTADOS DA PRAGMATIC '''
                        if browser.find_elements_by_xpath('//*[@id="ministats-container"]/div/app-single-row-stats/div/table/tbody/tr/td'):
                            numeros_recentes_validacao = browser.find_elements_by_xpath('//*[@id="ministats-container"]/div/app-single-row-stats/div/table/tbody/tr/td') 
                            

                        ''' LISTA DO PROXIMO RESULTADO APOS O ALERTA'''
                        lista_proximo_resultados = []
                        try:
                            for numeroRecente in numeros_recentes_validacao:
                                numero_r = numeroRecente.text
                                if 'x' not in numero_r:
                                    lista_proximo_resultados.append(numero_r)
                                
                                else:
                                    lista_proximo_resultados.append(numero_r[:2])

                        except:
                            pass
                        
                        ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
                        if lista_resultados[:int(sequencia_minima)] != lista_proximo_resultados[:int(sequencia_minima)]:
                            
                            ''' Lendo novos resultados para validação da estratégia'''
                            ''' PEGANDO RESULTADOS DA EVOLUTION '''
                            if browser.find_elements_by_css_selector('.single-number--43778 .value--877c6'):
                                numeros_recentes_validacao = browser.find_elements_by_css_selector('.single-number--43778 .value--877c6')
                                
                            
                            ''' PEGANDO RESULTADOS DA PRAGMATIC '''
                            if browser.find_elements_by_xpath('//*[@id="ministats-container"]/div/app-single-row-stats/div/table/tbody/tr/td'):
                                numeros_recentes_validacao = browser.find_elements_by_xpath('//*[@id="ministats-container"]/div/app-single-row-stats/div/table/tbody/tr/td') 

                            ''' PEGANDO A LISTA E VALIDANDO NOVAMENTE '''
                            lista_proximo_resultados = []
                            try:
                                for numeroRecente in numeros_recentes_validacao:
                                    numero_r = numeroRecente.text
                                    if 'x' not in numero_r:
                                        lista_proximo_resultados.append(numero_r)
                                    
                                    else:
                                        lista_proximo_resultados.append(numero_r[:2])

                            except:
                                pass

                            
                            '''Valida novamente se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta '''
                            if lista_resultados[:int(sequencia_minima)] != lista_proximo_resultados[:int(sequencia_minima)]:
                            
                                print('Resultado antes do alerta -->', nome_cassino, lista_resultados[:int(sequencia_minima)])
                                print('Resultado apos o alerta  --> ', nome_cassino, lista_proximo_resultados[:int(sequencia_minima)])

                                if estrategia[0] == 'repetição':
                                    ''' Verificando se o ultimo resultado da roleta está dentro da estratégia'''
                                    if lista_proximo_resultados[0] in aposta_externa[estrategia[1]]:
                                        dicionario_roletas[nome_cassino] = lista_proximo_resultados
                                        print('ENVIANDO SINAL TELEGRAM')
                                        enviarSinalTelegram(nome_cassino, sequencia_minima, estrategia, nome_fornecedor)
                                        print('=' * 220)
                                        checkSinalEnviado(lista_proximo_resultados, nome_cassino)
                                        time.sleep(1)
                                        break
                                    
                                    else:
                                        print('APAGA SINAL DE ALERTA')
                                        apagaAlertaTelegram()
                                        print('=' * 220)
                                        dicionario_roletas[nome_cassino] = lista_proximo_resultados
                                        lista_resultados = lista_proximo_resultados
                                        break
                                
                                if estrategia[0] == 'ausência':
                                    ''' Verificando se o ultimo resultado da roleta não está dentro da estratégia'''
                                    if lista_proximo_resultados[0] not in aposta_externa[estrategia[1]]:
                                        dicionario_roletas[nome_cassino] = lista_proximo_resultados
                                        print('ENVIANDO SINAL TELEGRAM')
                                        enviarSinalTelegram(nome_cassino, sequencia_minima, estrategia, nome_fornecedor)
                                        print('=' * 220)
                                        checkSinalEnviado(lista_proximo_resultados, nome_cassino)
                                        break
                                    
                                    else:
                                        print('APAGA SINAL DE ALERTA')
                                        apagaAlertaTelegram()
                                        print('=' * 220)
                                        dicionario_roletas[nome_cassino] = lista_proximo_resultados
                                        lista_resultados = lista_proximo_resultados
                                        break
                    
                    except:
                        print('APAGA SINAL DE ALERTA')
                        apagaAlertaTelegram()
                        print('=' * 220)
                        dicionario_roletas[nome_cassino] = lista_proximo_resultados
                        lista_resultados = lista_proximo_resultados
                        break
                    
            else:
                print('=' * 220)


    except:
        pass

                
def enviarAlertaTelegram(dicionario_roletas, nome_cassino, sequencia_minima, estrategia, nome_fornecedor):
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
            'content':  mensagem_alerta[0].replace('\n','') + '\n' +\
                            mensagem_alerta[1].replace('\n','').replace('[FORNECEDOR]', nome_fornecedor) + '\n\n' +\
                            mensagem_alerta[3].replace('\n','').replace('[NOME_CASSINO]', nome_cassino.title())+'\n' +\
                            mensagem_alerta[4].replace('\n','').replace('[ESTRATEGIA]', estrategia[0].title()+' de '+estrategia[1].title()) + '\n\n' +\
                            mensagem_alerta[6].replace('\n','').replace('[TIPO_ESTRATEGIA]', estrategia[0].title()+' de ').replace('[ESTRATEGIA]', estrategia[1].title()) + '\n' +\
                            mensagem_alerta[7].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(dicionario_roletas[nome_cassino][:int(sequencia_minima)-1])),
            
            'link_refer':[value[1] for key,value in canais.items()],
            'link_game_bet':['https://mesk.bet/casino/?cat=live&gameid=7312']
    }

    requests.post(url, headers=headers, json=payload)    

    ''' Enviando mensagem Telegram '''
    try:
        for key, value in canais.items():
            try:

                if value[0] == 'estrelabet':

                    ''' Mensagem '''
                    table_alerta = mensagem_alerta[0].replace('\n','') + '\n' +\
                                mensagem_alerta[1].replace('\n','').replace('[FORNECEDOR]', nome_fornecedor) + '\n\n' +\
                                mensagem_alerta[3].replace('\n','').replace('[NOME_CASSINO]', nome_cassino.title())+'\n' +\
                                mensagem_alerta[4].replace('\n','').replace('[ESTRATEGIA]', estrategia[0].title()+' de '+estrategia[1].title()) + '\n\n' +\
                                mensagem_alerta[6].replace('\n','').replace('[TIPO_ESTRATEGIA]', estrategia[0].title()+' de ').replace('[ESTRATEGIA]', estrategia[1].title()) + '\n' +\
                                mensagem_alerta[7].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(dicionario_roletas[nome_cassino][:int(sequencia_minima)-1])) + '\n\n' +\
                                mensagem_alerta[9].replace('\n','').replace('[SITE_CASSINO]', site_cassino_desktop)+\
                                mensagem_alerta[10].replace('\n','').replace('[SITE_CASSINO]', site_cassino_mobile)+'\n\n'+\
                                mensagem_alerta[12].replace('\n','').replace('[SITE_CADASTRO]', value[1]) if value[1] != '' else\
                                \
                                mensagem_alerta[0].replace('\n','') + '\n' +\
                                mensagem_alerta[1].replace('\n','').replace('[FORNECEDOR]', nome_fornecedor) + '\n\n' +\
                                mensagem_alerta[3].replace('\n','').replace('[NOME_CASSINO]', nome_cassino.title())+'\n' +\
                                mensagem_alerta[4].replace('\n','').replace('[ESTRATEGIA]', estrategia[0].title()+' de '+estrategia[1].title()) + '\n\n' +\
                                mensagem_alerta[6].replace('\n','').replace('[TIPO_ESTRATEGIA]', estrategia[0].title()+' de ').replace('[ESTRATEGIA]', estrategia[1].title()) + '\n' +\
                                mensagem_alerta[7].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(dicionario_roletas[nome_cassino][:int(sequencia_minima)-1])) + '\n\n' +\
                                mensagem_alerta[9].replace('\n','').replace('[SITE_CASSINO]', site_cassino_desktop)+\
                                mensagem_alerta[10].replace('\n','').replace('[SITE_CASSINO]', site_cassino_mobile)
                                


                    globals()[f'alerta_{key}'] = bot.send_message(key, table_alerta, parse_mode='HTML', disable_web_page_preview=True)  #Variavel Dinâmica


                else:
                    table_alerta = mensagem_alerta[0].replace('\n','') + '\n' +\
                    mensagem_alerta[1].replace('\n','').replace('[FORNECEDOR]', nome_fornecedor) + '\n\n' +\
                    mensagem_alerta[3].replace('\n','').replace('[NOME_CASSINO]', nome_cassino.title())+'\n' +\
                    mensagem_alerta[4].replace('\n','').replace('[ESTRATEGIA]', estrategia[0].title()+' de '+estrategia[1].title()) + '\n\n' +\
                    mensagem_alerta[6].replace('\n','').replace('[TIPO_ESTRATEGIA]', estrategia[0].title()+' de ').replace('[ESTRATEGIA]', estrategia[1].title()) + '\n' +\
                    mensagem_alerta[7].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(dicionario_roletas[nome_cassino][:int(sequencia_minima)-1])) + '\n\n' +\
                    mensagem_alerta[9].replace('\n','').replace('[SITE_CASSINO]', value[0])+\
                    mensagem_alerta[10].replace('\n','').replace('[SITE_CASSINO]', value[0])+'\n\n'+\
                    mensagem_alerta[12].replace('\n','').replace('[SITE_CADASTRO]', value[1]) if value[1] != '' else\
                    \
                    mensagem_alerta[0].replace('\n','') + '\n' +\
                    mensagem_alerta[1].replace('\n','').replace('[FORNECEDOR]', nome_fornecedor) + '\n\n' +\
                    mensagem_alerta[3].replace('\n','').replace('[NOME_CASSINO]', nome_cassino.title())+'\n' +\
                    mensagem_alerta[4].replace('\n','').replace('[ESTRATEGIA]', estrategia[0].title()+' de '+estrategia[1].title()) + '\n\n' +\
                    mensagem_alerta[6].replace('\n','').replace('[TIPO_ESTRATEGIA]', estrategia[0].title()+' de ').replace('[ESTRATEGIA]', estrategia[1].title()) + '\n' +\
                    mensagem_alerta[7].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(dicionario_roletas[nome_cassino][:int(sequencia_minima)-1])) + '\n\n' +\
                    mensagem_alerta[9].replace('\n','').replace('[SITE_CASSINO]', value[0])+\
                    mensagem_alerta[10].replace('\n','').replace('[SITE_CASSINO]', value[0])
                    

                    globals()[f'alerta_{key}'] = bot.send_message(key, table_alerta, parse_mode='HTML', disable_web_page_preview=True)  #Variavel Dinâmica

                
            except:
                pass

    except:
        pass

    contador_passagem = 1


def enviarSinalTelegram(nome_cassino, sequencia_minima, estrategia, nome_fornecedor):
    global table_sinal
    
    ''' Lendo o arquivo txt canais '''
    txt = open("canais.txt", "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[12].replace('canais= ','').replace('\n','')
    canais = ast.literal_eval(canais) # Convertendo string em dicionario 

    ''' Lendo o arquivo txt config-mensagens '''
    txt = open("config-mensagens.txt", "r", encoding="utf-8")
    arquivo_mensagem = txt.readlines()
    mensagem_sinal = arquivo_mensagem[1].split(',')

    ''' Estruturando mensagem '''
    txt = open("config-mensagens.txt", "r", encoding="utf-8")
    mensagem_sinal = txt.readlines()


    #ENVIANDO POST PARA A API
    payload = {
            'status': 'confirm', #alert | confirm | success | failure | denied
            'chat_id': [key for key,value in canais.items()],
            'content': mensagem_sinal[18].replace('\n','') + '\n' +\
                        mensagem_sinal[19].replace('\n','').replace('[FORNECEDOR]', nome_fornecedor) + '\n\n' +\
                        mensagem_sinal[21].replace('\n','').replace('[NOME_CASSINO]', nome_cassino.title()) + '\n' +\
                        mensagem_sinal[22].replace('\n','').replace('[ESTRATEGIA]', estrategia[0].title()+' de '+estrategia[1].title()) + '\n' +\
                        mensagem_sinal[23].replace('\n','').replace('[APOSTA]', estrategia[3].upper()) + '\n' +\
                        mensagem_sinal[24].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(dicionario_roletas[nome_cassino][:int(sequencia_minima)])) + '\n\n' +\
                        mensagem_sinal[26].replace('\n',''),

            'link_refer':[value[1] for key,value in canais.items()],
            'link_game_bet':['https://mesk.bet/casino/?cat=live&gameid=7312']
    }

    requests.post(url, headers=headers, json=payload)


    ''' Enviando mensagem Telegram '''
    try:
        for key,value in canais.items():
            try:

                if value[0] == 'estrelabet':

                    ''' Mensagem '''
                    table_sinal = mensagem_sinal[18].replace('\n','') + '\n' +\
                                mensagem_sinal[19].replace('\n','').replace('[FORNECEDOR]', nome_fornecedor) + '\n\n' +\
                                mensagem_sinal[21].replace('\n','').replace('[NOME_CASSINO]', nome_cassino.title()) + '\n' +\
                                mensagem_sinal[22].replace('\n','').replace('[ESTRATEGIA]', estrategia[0].title()+' de '+estrategia[1].title()) + '\n' +\
                                mensagem_sinal[23].replace('\n','').replace('[APOSTA]', estrategia[3].upper()) + '\n' +\
                                mensagem_sinal[24].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(dicionario_roletas[nome_cassino][:int(sequencia_minima)])) + '\n\n' +\
                                mensagem_sinal[26].replace('\n','') + '\n\n' +\
                                mensagem_sinal[28].replace('\n','').replace('[SITE_CASSINO]', site_cassino_desktop)+\
                                mensagem_sinal[29].replace('\n','').replace('[SITE_CASSINO]', site_cassino_mobile)+'\n\n'+\
                                mensagem_sinal[31].replace('\n','').replace('[SITE_CADASTRO]', value[1]) if value[1] != '' else\
                                \
                                mensagem_sinal[18].replace('\n','') + '\n' +\
                                mensagem_sinal[19].replace('\n','').replace('[FORNECEDOR]', nome_fornecedor) + '\n\n' +\
                                mensagem_sinal[21].replace('\n','').replace('[NOME_CASSINO]', nome_cassino.title()) + '\n' +\
                                mensagem_sinal[22].replace('\n','').replace('[ESTRATEGIA]', estrategia[0].title()+' de '+estrategia[1].title()) + '\n' +\
                                mensagem_sinal[23].replace('\n','').replace('[APOSTA]', estrategia[3].upper()) + '\n' +\
                                mensagem_sinal[24].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(dicionario_roletas[nome_cassino][:int(sequencia_minima)])) + '\n\n' +\
                                mensagem_sinal[26].replace('\n','') + '\n\n' +\
                                mensagem_sinal[28].replace('\n','').replace('[SITE_CASSINO]', value[0])+\
                                mensagem_sinal[29].replace('\n','').replace('[SITE_CASSINO]', value[0])


                    bot.delete_message(key, globals()[f'alerta_{key}'].message_id)
                    globals()[f'sinal_{key}'] = bot.send_message(key, table_sinal, parse_mode='HTML', disable_web_page_preview=True)
                
                
                else:
                    table_sinal = mensagem_sinal[18].replace('\n','') + '\n' +\
                                mensagem_sinal[19].replace('\n','').replace('[FORNECEDOR]', nome_fornecedor) + '\n\n' +\
                                mensagem_sinal[21].replace('\n','').replace('[NOME_CASSINO]', nome_cassino.title()) + '\n' +\
                                mensagem_sinal[22].replace('\n','').replace('[ESTRATEGIA]', estrategia[0].title()+' de '+estrategia[1].title()) + '\n' +\
                                mensagem_sinal[23].replace('\n','').replace('[APOSTA]', estrategia[3].upper()) + '\n' +\
                                mensagem_sinal[24].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(dicionario_roletas[nome_cassino][:int(sequencia_minima)])) + '\n\n' +\
                                mensagem_sinal[26].replace('\n','') + '\n\n' +\
                                mensagem_sinal[28].replace('\n','').replace('[SITE_CASSINO]', value[0])+\
                                mensagem_sinal[29].replace('\n','').replace('[SITE_CASSINO]', value[0])+'\n\n'+\
                                mensagem_sinal[31].replace('\n','').replace('[SITE_CADASTRO]', value[1]) if value[1] != '' else\
                                \
                                mensagem_sinal[18].replace('\n','') + '\n' +\
                                mensagem_sinal[19].replace('\n','').replace('[FORNECEDOR]', nome_fornecedor) + '\n\n' +\
                                mensagem_sinal[21].replace('\n','').replace('[NOME_CASSINO]', nome_cassino.title()) + '\n' +\
                                mensagem_sinal[22].replace('\n','').replace('[ESTRATEGIA]', estrategia[0].title()+' de '+estrategia[1].title()) + '\n' +\
                                mensagem_sinal[23].replace('\n','').replace('[APOSTA]', estrategia[3].upper()) + '\n' +\
                                mensagem_sinal[24].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(dicionario_roletas[nome_cassino][:int(sequencia_minima)])) + '\n\n' +\
                                mensagem_sinal[26].replace('\n','') + '\n\n' +\
                                mensagem_sinal[28].replace('\n','').replace('[SITE_CASSINO]', value[0])+\
                                mensagem_sinal[29].replace('\n','').replace('[SITE_CASSINO]', value[0])
                                

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


def checkSinalEnviado(lista_proximo_resultados, nome_cassino):
    global table_sinal
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
    global sequencia_minima
    global lista_resultados

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
            ''' PEGANDO RESULTADOS DA EVOLUTION '''
            if browser.find_elements_by_css_selector('.single-number--43778 .value--877c6'):
                numeros_recentes_validacao = browser.find_elements_by_css_selector('.single-number--43778 .value--877c6')
                
            ''' PEGANDO RESULTADOS DA PRAGMATIC '''
            if browser.find_elements_by_xpath('//*[@id="ministats-container"]/div/app-single-row-stats/div/table/tbody/tr/td'):
                numeros_recentes_validacao = browser.find_elements_by_xpath('//*[@id="ministats-container"]/div/app-single-row-stats/div/table/tbody/tr/td') 


            lista_resultados_sinal = []
            try:
                for numeroRecente in numeros_recentes_validacao:
                    numero_r = numeroRecente.text
                    if 'x' not in numero_r:
                        lista_resultados_sinal.append(numero_r)
                    else:
                        lista_resultados_sinal.append(numero_r[:2])
            except:
                pass

            ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
            if lista_proximo_resultados[:int(sequencia_minima)] != lista_resultados_sinal[:int(sequencia_minima)]:
                
                ''' Lendo novos resultados para validação da estratégia'''
                ''' PEGANDO RESULTADOS DA EVOLUTION '''
                if browser.find_elements_by_css_selector('.single-number--43778 .value--877c6'):
                    numeros_recentes_validacao = browser.find_elements_by_css_selector('.single-number--43778 .value--877c6')
                    
                ''' PEGANDO RESULTADOS DA PRAGMATIC '''
                if browser.find_elements_by_xpath('//*[@id="ministats-container"]/div/app-single-row-stats/div/table/tbody/tr/td'):
                    numeros_recentes_validacao = browser.find_elements_by_xpath('//*[@id="ministats-container"]/div/app-single-row-stats/div/table/tbody/tr/td') 


                lista_resultados_sinal = []
                try:
                    for numeroRecente in numeros_recentes_validacao:
                        numero_r = numeroRecente.text
                        if 'x' not in numero_r:
                            lista_resultados_sinal.append(numero_r)
                        else:
                            lista_resultados_sinal.append(numero_r[:2])
                except:
                    pass

                
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

                            # Atualizando placar e Alimentando o arquivo txt
                            placar_win +=1
                            placar_gale1 +=1
                            placar_geral = placar_win + placar_loss
                            with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                                arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}")
                            
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

                                

                        # editando mensagem enviada
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
                                    'content': mensagem_green[37].replace('\n','').replace('[RESULTADO]', ' | '.join(resultados)),
                                    'link_refer':[value[1] for key,value in canais.items()],
                                    'link_game_bet':['https://mesk.bet/casino/?cat=live&gameid=7312']
                            }

                            requests.post(url, headers=headers, json=payload)
                            
                            for key,value in canais.items():
                                try:
                                    bot.reply_to(globals()[f'sinal_{key}'], mensagem_green[37].replace('\n','').replace('[RESULTADO]', ' | '.join(resultados)), parse_mode='HTML')
                                except:
                                    pass
                    
                        except:
                            pass
                        

                        print('==================================================')
                        validador_sinal = 0
                        contador_cash = 0
                        contador_passagem = 0
                        dicionario_roletas[nome_cassino] = lista_resultados_sinal
                        lista_resultados = lista_resultados_sinal
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
        stop_loss.append('loss')

        # Preenchendo arquivo txt
        placar_loss +=1
        placar_geral = placar_win + placar_loss
        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
            arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}")


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
                    'content':  mensagem_green[39].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(resultados)),
                    'link_refer':[value[1] for key,value in canais.items()],
                    'link_game_bet':['https://mesk.bet/casino/?cat=live&gameid=7312']
            }

            requests.post(url, headers=headers, json=payload)


            for key,value in canais.items():
                try:
                    bot.reply_to(globals()[f'sinal_{key}'], mensagem_green[39].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(resultados)), parse_mode = 'HTML')
                except:
                    pass


            print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
        
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
        lista_resultados = lista_resultados_sinal
        return



inicio()            # Difinição do webBrowser
logarSite()         # Logando no Site
placar()            # Gerando o Placar

#________________________________________________________________________________________ TELEGRAM__________________________________________________________________________________#



print('############################################################# AGUARDANDO COMANDOS #############################################################')

global canal
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



# LENDO TXT PARA DEFINIR VARIAVEL FREE E VIP E VALIDAÇÃO DE USUÁRIO
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
        
        markup_tipo = markup_tipo.add('◀ Voltar', 'REPETIÇÃO', 'AUSÊNCIA', 'ESTRATÉGIAS PADRÕES')    

        message_tipo_estrategia = bot.reply_to(message, "🤖 Ok! Escolha o tipo de estratégia 👇", reply_markup=markup_tipo)
        bot.register_next_step_handler(message_tipo_estrategia, registrarTipoEstrategia)
    

    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_estrategia = bot.reply_to(message, "🤖⛔ Estou validando uma estratégia! Tente novamente em alguns instanstes.", reply_markup=markup)




@bot.message_handler(commands=['⚙🎰 Cadastrar_Roletas'])
def cadastrarRoletas(message):
    global contador_passagem

    if contador_passagem == 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        
        siteCassino()
        markup_apostas = generate_buttons_estrategias([f'{roleta[1].upper()}' for roleta in cassinos], markup)    
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

    ''' Enviando mensagem Telegram '''
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
        🎯 Assertividade "+ asserividade, reply_markup=markup)
    
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

        message_opcoes = bot.reply_to(message, "🤖 Bot de Roletas Evolution Iniciado! ✅ Escolha uma opção 👇",
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

        
        elif lista_estrategias == []:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖⛔ Cadastre no mínimo 1 estratégia antes de iniciar",
                                reply_markup=markup)

        
        else:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
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
            ''' Verifica se estálogado, se n tiver, realiza o login '''
            if browser.find_elements_by_xpath('//*[@id="username"]'):
                logarSite()

            siteCassino()       # Coltando o site dos Cassinos
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
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_tipo_estrategia, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        return




    if message_tipo_estrategia.text in ['ESTRATÉGIAS PADRÕES']:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')
        
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







