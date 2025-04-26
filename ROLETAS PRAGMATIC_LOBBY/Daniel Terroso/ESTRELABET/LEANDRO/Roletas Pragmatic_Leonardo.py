from selenium import webdriver
import time
import warnings
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import telebot
from telegram.ext import *
from telebot import *
import logging
import os, ast, requests, json


print()
print('                                #################################################################')
print('                                ################## BOT ROLETAS PRAGMATIC PLAY ###################')
print('                                #################################################################')
print('                                ##################### SEJA BEM VINDO ############################')
print('                                #################################################################')
print('                                ############# DESENVOLVIDO POR VICTOR RODRIGUES #################')
print('                                #################################################################\n')
print('Versão = 1.0.0')
print('Ambiente: Produção\n\n\n')

parar = 0
lista_roletas = []


# THREAD PARA ENVIAR POST PARA API
class enviarPostAPI(threading.Thread):
    def __init__(self, canais, status, texto, link_roleta):
        self.canais = canais
        self.status = status
        self.texto = texto
        self.link = link_roleta
        threading.Thread.__init__(self)
    
    def run(self):
        try:
        
            payload = {
                    'status': self.status, #alert | confirm | success | failure | denied
                    'chat_id': [key for key,value in self.canais.items()],
                    'content': self.texto,
                    'link_refer':[value[0] for key,value in self.canais.items()],
                    'link_game_bet': self.link
            }

            requests.post(url, headers=headers, json=payload)
        
        except Exception as e:
            print(e)



def mensagem_previa(horario):
    global msg_previa_enviada

    try:
        validaData()
       
        with open ('arquivos_txt/tempo_msg_previa.txt', encoding='UTF-8') as arquivo: 
            tempo_previo = arquivo.read()

        horario_atual = datetime.today().strftime('%H:%M') 
        horario_sessao = datetime.strptime(horario,'%H:%M')
        minuto_previo = timedelta(minutes=int(tempo_previo))
        horario_menos_minuto_previo = horario_sessao - minuto_previo
        horario_msg_previa = horario_menos_minuto_previo.strftime('%H:%M')

        if horario_atual == horario_msg_previa and msg_previa_enviada == False:
            
            minutos = open('arquivos_txt/tempo_msg_previa.txt', 'r', encoding='UTF-8').read()
            ''' Lendo o arquivo txt canais '''
            txt = open('arquivos_txt\\canais.txt', "r", encoding="utf-8")
            arquivo = txt.readlines()
            canais = arquivo[12].replace('canais= ','').replace('\n','')
            canais = ast.literal_eval(canais) # Convertendo string em dicionario 

            #envia msg previa
            try:
                for key,value in canais.items():
                    try:
                        ''' Lendo o arquivo txt '''
                        with open('arquivos_txt\\msg_previa.txt',"r", encoding="utf-8") as arquivo:
                            message_previa = arquivo.read()
                        
                        #Variavel Dinâmica
                        bot.send_message(key, 
                                            message_previa.replace('[HORARIO]', minutos), 
                                            parse_mode='HTML', disable_web_page_preview=True)
                    except:
                        pass

                msg_previa_enviada = True

            except:
                pass

    except:pass


# ENVIA PLACAR CANAIS TELEGRAM
def envia_placar_pos_sessao(placar_win_sessao, placar_loss_sessao):

    try:
        #placar()

        ''' Lendo o arquivo txt canais '''
        msg_sessao_finalizada = open('arquivos_txt\\msg_fim_sessao.txt', "r", encoding="utf-8").read()
        txt = open('arquivos_txt\\canais.txt', "r", encoding="utf-8")
        arquivo = txt.readlines()
        canais = arquivo[12].replace('canais= ','').replace('\n','')
        canais = ast.literal_eval(canais) # Convertendo string em dicionario 

        for key, value in canais.items():
            try:
                bot.send_message(key, msg_sessao_finalizada
                                        .replace('[DATA_HOJE]', data_hoje)
                                        .replace('[PLACAR_WIN_SESSAO]', str(placar_win_sessao))
                                        .replace('[PLACAR_LOSS_SESSAO]', str(placar_loss_sessao))
                                        , parse_mode='HTML', disable_web_page_preview=True)
        
            except:
                pass


    except Exception as a:
        logger.error('Exception ocorrido no ' + repr(a))
        #placar = bot.reply_to(message,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%", reply_markup=markup)
        pass


def valida_horario_sessao():

    global sessao_ativa, contagem_sinais, placar_win_sessao, placar_loss_sessao, msg_previa_enviada

    validaData()

    # Auto Refresh
    #refreshar_pagina = auto_refresh()

    #if refreshar_pagina == True:
        
    #    print('HORA DE REFRESHAR A PAGINA!!!!')
    #    logarSite()
    #    time.sleep(10)
    
    #else:pass
    
    horario_atual = datetime.today().strftime('%H:%M')


    with open ('arquivos_txt/horario_sessoes.txt', encoding='UTF-8') as arquivo: 
        horarios = arquivo.read().split(',')

    with open ('arquivos_txt/qnt_sinais_sessao.txt', encoding='UTF-8') as arquivo: 
        qntd_sinais_sessao = arquivo.read()        

    
    for horario in horarios:

        mensagem_previa(horario)

        if horario_atual == horario and sessao_ativa == False:

            contagem_sinais = 0
            sessao_ativa = True

            print(f'Sessão das {horario} Ativada!!')

            placar_win_sessao = 0
            placar_loss_sessao = 0

            break
        
        else:
            continue


    #Validação pra Finalizar Sessão
    if contagem_sinais >= int(qntd_sinais_sessao) and sessao_ativa == True:

        print(f'Sessão das Desativada!!')

        envia_placar_pos_sessao(placar_win_sessao, placar_loss_sessao)

        placar_win_sessao = 0
        placar_loss_sessao = 0
        sessao_ativa = False
        msg_previa_enviada = False
        contagem_sinais = 0

    
    #time.sleep(5)


def auto_refresh():
    global horario_inicio

    data_atual = datetime.now().date().strftime('%d/%m/%Y')
    horario_atual = datetime.today().strftime('%H:%M')
    tres_hora = timedelta(hours=1)
    horario_mais_tres = horario_inicio + tres_hora
    horario_refresh = horario_mais_tres.strftime('%H:%M')

    if horario_atual >= horario_refresh and data_atual == horario_mais_tres.date().strftime('%d/%m/%Y'):
        
        horario_inicio = datetime.now()

        return True
    
    else: return False


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
                    historico_roleta = formatar_resultados(roulette) # Formata o historico em lista

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

            '1ª coluna': ['1', '4', '7', '10', '13', '16', '19', '22', '25', '28', '31', '34'],
            '2ª coluna': ['2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32', '35'],
            '3ª coluna': ['3', '6', '9', '12', '15', '18', '21', '24', '27', '30', '33', '36'],

            '1ª duzia': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
            '2ª duzia': ['13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'],
            '3ª duzia': ['25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36'],

            'cor vermelho': ['1', '3', '5', '7', '9', '12', '14', '16', '18', '19', '21', '23', '25', '27', '30', '32', '34', '36'],
            'cor preto': ['2', '4', '6', '8', '10', '11', '13', '15', '17', '20', '22', '24', '26', '28', '29', '31', '33', '35'],

            'números par(es)': ['2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24', '26', '28', '30', '32', '34', '36'],
            'números impar(es)': ['1', '3', '5', '7', '9', '11', '13', '15', '17', '19', '21', '23', '25', '27', '29', '31', '33', '35'],

            'números baixos': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18'],
            'números altos': ['19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36'],

            '1ª/2ª coluna': ['1', '4', '7', '10', '13', '16', '19', '22', '25', '28', '31', '34', '2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32', '35'],
            '2ª/3ª coluna': ['2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32', '35', '3', '6', '9', '12', '15', '18', '21', '24', '27', '30', '33', '36'],
            '1ª/3ª coluna': ['1', '4', '7', '10', '13', '16', '19', '22', '25', '28', '31', '34', '3', '6', '9', '12', '15', '18', '21', '24', '27', '30', '33', '36'],

            '1ª/2ª duzia': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'],
            '2ª/3ª duzia': ['13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36'],
            '1ª/3ª duzia': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36']

        }

        for opcao_aposta in opcoes_apostas:
            if estrategia_usuario == opcao_aposta:
                dic_estrategia_usuario[opcao_aposta] = opcoes_apostas[opcao_aposta]
                #print(dic_estrategia_usuario)
        
        return dic_estrategia_usuario
    
    except:
        pass
            

def formatar_resultados(roleta):  

    lista_resultados = []

    try:

        resultados = roleta.text.split('\n')[3:]
        for numero in resultados:
            if 'x' not in numero:
                lista_resultados.append(numero)
            
        
        return lista_resultados
    
    except:
        pass


def nomeDosCassinos(nome_cassino):
    global cassinos
    global nome_dos_cassinos

    nome_dos_cassinos = [
        
        ('Mega Roleta'),
        ('Roleta Azure'),
        ('PowerUP Roleta'),
        ('Roleta Ruby'),
        ('Autorroleta'),
        ('Roleta Verde'),
        ('Autorroleta Rápida'),
        ('Roleta Macau'),
        ('Roleta Russa'),
        ('Roleta Rápida 2')

        ]

    cassinos = [

        ('Mega Roleta',''),
        ('Roleta Azure',''),
        ('PowerUP Roleta',''),
        ('Roleta Ruby',''),
        ('Autorroleta',''),
        ('Roleta Verde',''),
        ('Autorroleta Rápida',''),
        ('Roleta Macau',''),
        ('Roleta Russa',''),
        ('Roleta Rápida 2','')


    ]


def link_roletas(nome_roleta):


    roletas_e_links = [

        ('Mega Roleta','https://estrelabet.com/pb/gameplay/pp204/1/pragmaticplay/real-game'),
        ('Roleta Azure','https://estrelabet.com/pb/gameplay/roulette-azure/real-game'),
        ('PowerUP Roleta','https://estrelabet.com/pb/gameplay/pp240/1/pragmaticplay/real-game'),
        ('Roleta Ruby','https://estrelabet.com/pb/gameplay/pp230a24/1/pragmaticplay/real-game'),
        ('Autorroleta','https://estrelabet.com/pb/gameplay/pp225/1/pragmaticplay/real-game'),
        ('Roleta Verde','https://estrelabet.com/pb/gameplay/pp201/1/pragmaticplay/real-game'),
        ('Autorroleta Rápida','https://estrelabet.com/pb/gameplay/pp226/1/pragmaticplay/real-game'),
        ('Roleta Macau','https://estrelabet.com/pb/gameplay/pp206/1/pragmaticplay/real-game'),
        ('Roleta Russa','https://estrelabet.com/pb/gameplay/pp221/1/pragmaticplay/real-game'),
        ('Roleta Rápida 2','https://estrelabet.com/pb/gameplay/pp205/1/pragmaticplay/real-game')

    ]

    for roleta in roletas_e_links:
        if roleta[0] == nome_roleta:
            return roleta[1]


def inicio():
    global browser
    global lobby_cassinos
    global logger
    global horario_inicio
    global lista_anterior
    global url
    global headers, sessao_ativa, contagem_sinais, msg_previa_enviada, placar_win_sessao, placar_loss_sessao

    url = "https://app.bootbost.com.br/api/v1/call"
    headers = {
    'Content-Type': 'application/json'
    }

    placar_win_sessao = 0
    placar_loss_sessao = 0
    msg_previa_enviada = False
    sessao_ativa = False
    contagem_sinais = 0
    lista_anterior = []
    horario_inicio = datetime.now()
    logger = logging.getLogger()

    # Definindo opções para o browser
    warnings.filterwarnings("ignore", category=DeprecationWarning) 
    chrome_options = webdriver.ChromeOptions() 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)


def logarSite():

    try:
        browser.maximize_window()
    except:pass

    #logger = logging.getLogger()
    while True:
        try:
            time.sleep(3)
            browser.set_page_load_timeout(30)
            browser.get(r"https://estrelabet.com/pb#/overview")
            browser.maximize_window()
            time.sleep(15)
            break
        except:continue

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
                browser.find_element_by_xpath('//*[@class="header-right-menu main-header-wrpr--desktop"]//*[text()="Conecte-se"]').click()
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


    #ACESSANDO JOGO PRAGMATIC 
    try:

        time.sleep(1)
        browser.get('https://estrelabet.com/pb/gameplay/roleta-brasileira/real-game')
        time.sleep(10)
    except:
        pass

    #IFRAME
    a=1
    while a < 10:
        try:
            iframe_game = browser.find_element_by_id('gamePlayIframe').get_attribute('src')
            browser.get(iframe_game)
            time.sleep(10)
            a+=1
            break
        except:
            time.sleep(1)
            continue


    #ACESSANDO LOBBY PRAGMATIC
    try:

        browser.get('https://client.pragmaticplaylive.net/desktop/lobby/')
        time.sleep(20)
    
    except:pass


def coletarResultados(lista_roletas):
    global url_cassino
    global dicionario_roletas
    global contador_passagem
    global horario_atual
    global nome_cassino, link_roleta, sessao_ativa

    ''' Pegando a relação de roletas '''
    #roletas = browser.find_elements_by_css_selector('.lobby .lobby-table-name')

    ''' removendo roletas sem historico '''
    #roletas_com_historico = [] 
    #for roleta in enumerate(roletas):

    #    nomeDosCassinos(roleta[1].text)

    #    if roleta[1].text in nome_dos_cassinos:
    #        roletas_com_historico.append(roleta[1])
    #        pass
    #    else:
    #        continue
    

    while True:

        valida_horario_sessao()

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass
        
        # Validando o horario para envio do relatório diário
        validaData()

        # Auto Refresh
        refreshar_pagina = auto_refresh()

        if refreshar_pagina == True:
            
            print('HORA DE REFRESHAR A PAGINA!!!!')
            logarSite()
            time.sleep(10)
        
        else:pass
    

        # VALIDAR SE FOI DESCONECTADO
        if browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[6]/div/div[2]/div[2]/button') or browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[5]/div/div[2]/div/div[3]/button'):
            browser.refresh()
            logarSite()
            continue

        try:
            ''' Elemento das roletas e historico de resultados '''
            roletas = browser.find_elements_by_xpath('//*[@id="ROULETTE"]/*[name()="li"]')

            if roletas == []:
                logarSite()

            else:
                pass

            ''' Percorrendo as roletas com historico'''
            for roleta in roletas:
                
                #COLETANDO INFORMAÇÕES
                #Historico de resultados da Roleta
                historico_roleta = formatar_resultados(roleta) # Formata o historico em lista
                
                #Nome do Cassino
                try:
                    nome_cassino = roleta.text.split('\n')[2]
                    link_roleta = link_roletas(nome_cassino)

                except:
                    pass


                #Validando se é Roleta Azure
                if nome_cassino == 'Roleta Azure':
                    pass
                else:
                    continue


                #nome_cassino = roleta[1].text
                nomeDosCassinos(nome_cassino)

                # Validando se foi solicitado o stop do BOT
                if parar != 0:
                    break
                else:
                    pass


                ''' Valida se tem algum cassino cadastrado pelo usuário. Se não, analisa todos do grupo '''
                #if lista_roletas == [] and nome_cassino in nome_dos_cassinos:
                #    pass
                
                #elif nome_cassino.upper() in lista_roletas:
                #    pass
                
                #else:
                #    continue
                
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
                    
                
                ''' VALIDA SE A LISTA ESTÁ VAZIA '''
                if historico_roleta == []:
                    browser.refresh()
                    logarSite()
                else:
                    pass

                print(horario_atual)

                ''' Chama a função que valida a estratégia para enviar o sinal Telegram'''
                validarEstrategia(dicionario_roletas, nome_cassino, lista_estrategias, roleta)
                print('=' * 150)
                
            
        except:
            logarSite()
            ''' Pegando a relação de roletas '''
            roletas = browser.find_elements_by_css_selector('.lobby .lobby-table-name')

            ''' removendo roletas sem historico '''
            roletas_com_historico = [] 
            for roleta in enumerate(roletas):

                nomeDosCassinos(roleta[1].text)

                if roleta[1].text in nome_dos_cassinos:
                    roletas_com_historico.append(roleta[1])
                    pass
                else:
                    continue
            
                continue 

            
def validarEstrategia(dicionario_roletas, nome_cassino, lista_estrategias, roleta):
    global estrategia
    global contador_passagem
    global lista_resultados_sinal, sessao_ativa

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


            ''' Pegando o tipo de aposta (AUSENCIA OU REPETIÇÃO '''
            tipo_aposta = estrategia[0]

            ''' Pegando os números da aposta externa da estratégia'''
            aposta_externa = apostasExternas(estrategia[1], dic_estrategia_usuario)

            ''' Pegando a sequencia minima da estratégia cadastrada pelo usuário '''
            sequencia_minima = estrategia[2]
            
            print ('Analisando a Estrategia --> ', estrategia)
            print('Historico_Roleta --> ', nome_cassino, dicionario_roletas[nome_cassino][:int(sequencia_minima)])

            ''' ANTES DE PASSAR NO VALIDADOR, VERIFICAR SE EXISTE O RESULTADO 0 POIS O 0 QUEBRA A SEQUENCIA'''
            if '0' in dicionario_roletas[nome_cassino][:int(sequencia_minima)] or '00' in dicionario_roletas[nome_cassino][:int(sequencia_minima)]:
                print('Sequencia com resultado 0...Analisando outra estratégia!')
                print('=' * 150)
                continue
            
            else:
                pass

            ''' Verifica se os números da seq minima do historico da roleta está dentro da estratégia '''
            validador = validarEstrategiaAlerta(dicionario_roletas, nome_cassino, aposta_externa, sequencia_minima, estrategia)
            
            ''' Validando se bateu alguma condição'''
            if validador.count('true') == int(sequencia_minima)-1:
                print('IDENTIFICADO PRÉ PADRÃO NA ROLETA ', nome_cassino, ' COM A ESTRATÉGIA ', estrategia)
                print('ENVIAR ALERTA')
                enviarAlertaTelegram(dicionario_roletas, nome_cassino, sequencia_minima, estrategia, link_roleta)
                time.sleep(1)

                ''' Verifica se a ultima condição bate com a estratégia para enviar sinal Telegram '''
                while True:
                    
                    valida_horario_sessao()

                    try:
                        # VALIDAR SE FOI DESCONECTADO
                        if browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[6]/div/div[2]/div[2]/button') or browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[5]/div/div[2]/div/div[3]/button'):
                            browser.refresh()
                            logarSite()
                            continue

                        validaData()
 
                        ''' PEGANDO NOVOS RESULTADOS '''
                        lista_proximo_resultados = formatar_resultados(roleta) # Formata o historico em lista
                        print(lista_proximo_resultados)

                        if lista_proximo_resultados == None or lista_proximo_resultados == [] or lista_proximo_resultados == '':
                            print('APAGA SINAL DE ALERTA')
                            apagaAlertaTelegram()
                            print('=' * 220)
                            dicionario_roletas[nome_cassino] = lista_proximo_resultados
                            break

                        ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
                        if dicionario_roletas[nome_cassino][:3] != lista_proximo_resultados[:3]:

                            print('Historico_Roleta --> ', nome_cassino, lista_proximo_resultados[:int(sequencia_minima)])

                            ### ALIMENTANDO BANCO DE DADOS ###
                            #nome_cassino,lista_proximo_resultados, dicionario_roletas, 'NULL','NULL')

                            if estrategia[0] == 'repetição':
                                ''' Verificando se o ultimo resultado da roleta está dentro da estratégia'''
                                if lista_proximo_resultados[0] in aposta_externa[estrategia[1]]:
                                    dicionario_roletas[nome_cassino] = lista_proximo_resultados
                                    print('ENVIANDO SINAL TELEGRAM')
                                    enviarSinalTelegram(nome_cassino, sequencia_minima, estrategia,link_roleta)
                                    print('=' * 220)
                                    checkSinalEnviado(lista_proximo_resultados, nome_cassino, roleta)
                                    time.sleep(1)
                                    break
                                
                                else:
                                    print('APAGA SINAL DE ALERTA')
                                    apagaAlertaTelegram()
                                    print('=' * 220)
                                    dicionario_roletas[nome_cassino] = lista_proximo_resultados
                                    break

                            
                            if estrategia[0] == 'ausência':
                                ''' Verificando se o ultimo resultado da roleta não está dentro da estratégia'''
                                if lista_proximo_resultados[0] not in aposta_externa[estrategia[1]]:
                                    dicionario_roletas[nome_cassino] = lista_proximo_resultados
                                    print('ENVIANDO SINAL TELEGRAM')
                                    enviarSinalTelegram(nome_cassino, sequencia_minima, estrategia, link_roleta)
                                    print('=' * 220)
                                    checkSinalEnviado(lista_proximo_resultados, nome_cassino, roleta)
                                    break
                                
                                else:
                                    print('APAGA SINAL DE ALERTA')
                                    apagaAlertaTelegram()
                                    print('=' * 220)
                                    dicionario_roletas[nome_cassino] = lista_proximo_resultados
                                    break
                        
                        else:
                            continue

                    except Exception as b:
                        logger.error('Exception ocorrido no ' + repr(b))
                        print('APAGA SINAL DE ALERTA')
                        apagaAlertaTelegram()
                        print('=' * 220)
                        dicionario_roletas[nome_cassino] = lista_proximo_resultados
                        break
                        

                    
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


def enviarAlertaTelegram(dicionario_roletas, nome_cassino, sequencia_minima, estrategia, link_roleta):
    global contador_passagem

    ''' Lendo o arquivo txt canais '''
    txt = open('arquivos_txt\\canais.txt', "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[12].replace('canais= ','').replace('\n','')
    canais = ast.literal_eval(canais) # Convertendo string em dicionario 


    # Enviando POST para a API
    try:
        ''' Lendo o arquivo txt '''
        with open('arquivos_txt\\alerta.txt',"r", encoding="utf-8") as arquivo:
            message_alerta = arquivo.readlines()

        texto = message_alerta[0].replace('\n','')+'\n'+\
                message_alerta[1].replace('\n','')+'\n\n'+\
                message_alerta[3].replace('\n','').replace('[NOME_CASSINO]',nome_cassino.title())+'\n'+\
                message_alerta[4].replace('\n','').replace('[ESTRATEGIA]',estrategia[0].title()+' de '+estrategia[1].title())+'\n\n'+\
                message_alerta[6].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(dicionario_roletas[nome_cassino][:int(sequencia_minima)-1]))
        
        enviarPostAPI(canais, 'alert', texto, link_roleta).start()

    except Exception as e:
        print(e)



    ''' Enviando mensagem Telegram '''
    try:
        for key,value in canais.items():

            if value[0] == 'sessao' and sessao_ativa == True:

                try:
                    ''' Lendo o arquivo txt '''
                    with open('arquivos_txt\\alerta.txt',"r", encoding="utf-8") as arquivo:
                        message_alerta = arquivo.read()
                    
                    #Variavel Dinâmica
                    globals()[f'alerta_{key}'] = bot.send_message(key, 
                                                                    message_alerta.replace('[NOME_CASSINO]',nome_cassino.title())\
                                                                                .replace('[ESTRATEGIA]',estrategia[0].title()+' de '+estrategia[1].title())\
                                                                                .replace('[LISTA_RESULTADOS]', ' | '.join(dicionario_roletas[nome_cassino][:int(sequencia_minima)-1]))\
                                                                                .replace('[SITE_DESKTOP]', link_roleta).replace('[SITE_MOBILE]', link_roleta)
                                                                                .replace('[SITE_CADASTRO]', value[1]) if value[1] != '' else\
                                                                                    
                                                                    message_alerta.replace('[NOME_CASSINO]',nome_cassino.title())\
                                                                                .replace('[ESTRATEGIA]',estrategia[0].title()+' de '+estrategia[1].title())\
                                                                                .replace('[LISTA_RESULTADOS]', ' | '.join(dicionario_roletas[nome_cassino][:int(sequencia_minima)-1]))\
                                                                                .replace('[SITE_DESKTOP]', link_roleta).replace('[SITE_MOBILE]', link_roleta)
                                                                                .replace("\n\n<b><a href='[SITE_CADASTRO]'>CADASTRE-SE AQUI</a></b>\n", '')
                                                                                , 
                                                                    parse_mode='HTML', disable_web_page_preview=True)
                except:
                    pass
            
            elif value[0] != 'sessao':
                
                try:
                    ''' Lendo o arquivo txt '''
                    with open('arquivos_txt\\alerta.txt',"r", encoding="utf-8") as arquivo:
                        message_alerta = arquivo.read()
                    
                    #Variavel Dinâmica
                    globals()[f'alerta_{key}'] = bot.send_message(key, 
                                                                    message_alerta.replace('[NOME_CASSINO]',nome_cassino.title())\
                                                                                .replace('[ESTRATEGIA]',estrategia[0].title()+' de '+estrategia[1].title())\
                                                                                .replace('[LISTA_RESULTADOS]', ' | '.join(dicionario_roletas[nome_cassino][:int(sequencia_minima)-1]))\
                                                                                .replace('[SITE_DESKTOP]', link_roleta).replace('[SITE_MOBILE]', link_roleta)
                                                                                .replace('[SITE_CADASTRO]', value[0]) if value[0] != '' else\
                                                                                    
                                                                    message_alerta.replace('[NOME_CASSINO]',nome_cassino.title())\
                                                                                .replace('[ESTRATEGIA]',estrategia[0].title()+' de '+estrategia[1].title())\
                                                                                .replace('[LISTA_RESULTADOS]', ' | '.join(dicionario_roletas[nome_cassino][:int(sequencia_minima)-1]))\
                                                                                .replace('[SITE_DESKTOP]', link_roleta).replace('[SITE_MOBILE]', link_roleta)
                                                                                .replace("\n\n<b><a href='[SITE_CADASTRO]'>CADASTRE-SE AQUI</a></b>\n", '')
                                                                                , 
                                                                    parse_mode='HTML', disable_web_page_preview=True)
                except:pass


    except:
        pass

    contador_passagem = 1
    

def enviarSinalTelegram(nome_cassino, sequencia_minima, estrategia, link_roleta):
    global table_sinal

    ''' Lendo o arquivo txt canais '''
    txt = open('arquivos_txt\\canais.txt', "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[12].replace('canais= ','').replace('\n','')
    canais = ast.literal_eval(canais) # Convertendo string em dicionario 



    #ENVIANDO POST PARA A API
    try:

        ''' Lendo o arquivo txt '''
        with open('arquivos_txt\\sinal.txt',"r", encoding="utf-8") as arquivo:
            message_sinal = arquivo.readlines()

        texto = message_sinal[0].replace('\n','')+'\n'+\
                message_sinal[1].replace('\n','')+'\n\n'+\
                message_sinal[3].replace('\n','').replace('[NOME_CASSINO]', nome_cassino.title())+'\n'+\
                message_sinal[4].replace('\n','').replace('[ESTRATEGIA]', estrategia[0].title()+' de '+estrategia[1].title())+'\n'+\
                message_sinal[5].replace('\n','').replace('[APOSTA]', estrategia[3].upper())+'\n'+\
                message_sinal[6].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(dicionario_roletas[nome_cassino][:1]))+'\n\n'+\
                message_sinal[8].replace('\n','')
        
        enviarPostAPI(canais, 'confirm', texto, link_roleta).start()
    
    except Exception as e:
        print(e)


    ''' Enviando mensagem Telegram '''
    try:
        for key,value in canais.items():

            if value[0] == 'sessao' and sessao_ativa == True:

                try:
                    ''' Lendo o arquivo txt '''
                    with open('arquivos_txt\\sinal.txt',"r", encoding="utf-8") as arquivo:
                        message_sinal = arquivo.read()

                    bot.delete_message(key, globals()[f'alerta_{key}'].message_id)

                    globals()[f'sinal_{key}'] = bot.send_message(key, 
                                                                message_sinal.replace('[APOSTA]', estrategia[3].upper())
                                                                            .replace('[NOME_CASSINO]', nome_cassino.title())
                                                                            .replace('[ESTRATEGIA]', estrategia[0].title()+' de '+estrategia[1].title())
                                                                            .replace('[LISTA_RESULTADOS]', ' | '.join(dicionario_roletas[nome_cassino][:1]))
                                                                            .replace('[SITE_DESKTOP]', link_roleta).replace('[SITE_MOBILE]', link_roleta)
                                                                            .replace('[SITE_CADASTRO]', value[1]) if value [1] != '' else\
                                                                                
                                                                    message_sinal.replace('[APOSTA]', estrategia[3].upper())
                                                                            .replace('[NOME_CASSINO]', nome_cassino.title())
                                                                            .replace('[ESTRATEGIA]', estrategia[0].title()+' de '+estrategia[1].title())
                                                                            .replace('[LISTA_RESULTADOS]', ' | '.join(dicionario_roletas[nome_cassino][:1]))
                                                                            .replace('[SITE_DESKTOP]', link_roleta).replace('[SITE_MOBILE]', link_roleta)
                                                                            .replace("\n\n<b><a href='[SITE_CADASTRO]'>CADASTRE-SE AQUI</a></b>\n\n", ''),
                                                                parse_mode='HTML', disable_web_page_preview=True)
                except:
                    pass
            
            elif value[0] != 'sessao':

                try:
                    ''' Lendo o arquivo txt '''
                    with open('arquivos_txt\\sinal.txt',"r", encoding="utf-8") as arquivo:
                        message_sinal = arquivo.read()

                    bot.delete_message(key, globals()[f'alerta_{key}'].message_id)

                    globals()[f'sinal_{key}'] = bot.send_message(key, 
                                                                message_sinal.replace('[APOSTA]', estrategia[3].upper())
                                                                            .replace('[NOME_CASSINO]', nome_cassino.title())
                                                                            .replace('[ESTRATEGIA]', estrategia[0].title()+' de '+estrategia[1].title())
                                                                            .replace('[LISTA_RESULTADOS]', ' | '.join(dicionario_roletas[nome_cassino][:1]))
                                                                            .replace('[SITE_DESKTOP]', link_roleta).replace('[SITE_MOBILE]', link_roleta)
                                                                            .replace('[SITE_CADASTRO]', value[0]) if value [0] != '' else\
                                                                                
                                                                    message_sinal.replace('[APOSTA]', estrategia[3].upper())
                                                                            .replace('[NOME_CASSINO]', nome_cassino.title())
                                                                            .replace('[ESTRATEGIA]', estrategia[0].title()+' de '+estrategia[1].title())
                                                                            .replace('[LISTA_RESULTADOS]', ' | '.join(dicionario_roletas[nome_cassino][:1]))
                                                                            .replace('[SITE_DESKTOP]', link_roleta).replace('[SITE_MOBILE]', link_roleta)
                                                                            .replace("\n\n<b><a href='[SITE_CADASTRO]'>CADASTRE-SE AQUI</a></b>\n\n", ''),
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
    
    #ENVIANDO POST PARA A API
    try:
    
        texto = ['Entrada Não Confirmada']

        enviarPostAPI(canais, 'denied', texto, link_roleta).start()
    
    except Exception as e:
        print(e)


    try:
        for key,value in canais.items():

            if value[0] == 'sessao' and sessao_ativa == True:

                try:
                    bot.delete_message(key, globals()[f'alerta_{key}'].message_id)
                except:
                    pass
            
            elif value[0] != 'sessao':

                try:
                    bot.delete_message(key, globals()[f'alerta_{key}'].message_id)
                except:
                    pass
            
    except:
        pass

    contador_passagem = 0


def checkSinalEnviado(lista_proximo_resultados, nome_cassino, roleta):
    global table, contagem_sinais
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
    global data_hoje, placar_win_sessao, placar_loss_sessao,sessao_ativa


    resultados = []
    contador_cash = 0
    while contador_cash <= 2:

        valida_horario_sessao()

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
            lista_resultados_sinal = formatar_resultados(roleta) # Formata o historico em lista
            #print(historico_roleta)

            ''' Validando se tem dado Vazio '''
            if '' in lista_resultados_sinal or lista_resultados_sinal == [] or lista_resultados_sinal == None:
                logarSite()


            ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
            if lista_proximo_resultados[:3] != lista_resultados_sinal[:3]:
                
                print(lista_resultados_sinal[0])
                
                grupo_apostar = apostasExternas(estrategia[3], dic_estrategia_usuario)

                # VALIDANDO WIN OU LOSS
                if lista_resultados_sinal[0] in grupo_apostar[estrategia[3]] or lista_resultados_sinal[0] == '0' or lista_resultados_sinal[0] == '00':
                
                    # validando o tipo de WIN
                    if contador_cash == 0:
                        print('WIN SEM GALE')
                        stop_loss.append('win')

                        ''' ADD RESULTADO NA LISTA DE RESULTADOS DO SINAL '''
                        resultados.append(f'<b>{lista_resultados_sinal[0]}</b>')

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

                        ''' ADD RESULTADO NA LISTA DE RESULTADOS DO SINAL '''
                        resultados.append(f'<b>{lista_resultados_sinal[0]}</b>')

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
                        
                        ''' ADD RESULTADO NA LISTA DE RESULTADOS DO SINAL '''
                        resultados.append(f'<b>{lista_resultados_sinal[0]}</b>')

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


                        #ENVIANDO POST PARA A API
                        try:

                            ''' Lendo o arquivo txt config-mensagens '''
                            with open('arquivos_txt\\green.txt',"r", encoding="utf-8") as arquivo:
                                message_green = arquivo.read()
                        
                            texto =  message_green.replace('[LISTA_RESULTADOS]', ' | '.join(resultados))

                            enviarPostAPI(canais, 'success', texto, link_roleta).start()
                        
                        except Exception as e:
                            print(e)


                        for key,value in canais.items():

                            if value[0] == 'sessao' and sessao_ativa == True:

                                try:
                                    ''' Lendo o arquivo txt config-mensagens '''
                                    with open('arquivos_txt\\green.txt',"r", encoding="utf-8") as arquivo:
                                        message_green = arquivo.read()

                                    bot.reply_to(globals()[f'sinal_{key}'], message_green.replace('[LISTA_RESULTADOS]', ' | '.join(resultados)),
                                                                                parse_mode='HTML')
                                except:
                                    pass
                            
                            elif value[0] != 'sessao':

                                try:
                                    ''' Lendo o arquivo txt config-mensagens '''
                                    with open('arquivos_txt\\green.txt',"r", encoding="utf-8") as arquivo:
                                        message_green = arquivo.read()

                                    bot.reply_to(globals()[f'sinal_{key}'], message_green.replace('[LISTA_RESULTADOS]', ' | '.join(resultados)),
                                                                                parse_mode='HTML')
                                except:
                                    pass

                    except:
                        pass

                    
                    

                    print('==================================================')
                    #Contagem Sinais por Sessão
                    if sessao_ativa == True:
                        contagem_sinais+=1
                        placar_win_sessao+=1

                    validador_sinal = 0
                    contador_cash = 0
                    contador_passagem = 0
                    dicionario_roletas[nome_cassino] = lista_resultados_sinal
                    return

            

                else:
                    print('LOSSS')
                    ''' ADD RESULTADO NA LISTA DE RESULTADOS DO SINAL '''
                    resultados.append(lista_resultados_sinal[0])

                    ### ALIMENTANDO BANCO DE DADOS ###
                    #alimenta_banco_dados(nome_cassino, lista_resultados_sinal, dicionario_roletas, 'NULL', 'NULL')
         
                    print('==================================================')
                    contador_cash+=1
                    lista_proximo_resultados = lista_resultados_sinal
                    continue


        except Exception as a:
            logger.error('Exception ocorrido no ' + repr(a))
            #logarSite()
            lista_resultados_sinal, roleta = resgatar_historico(nome_cassino)
            continue


    if contador_cash == 3:
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


            #ENVIANDO POST PARA A API
            try:

                ''' Lendo o arquivo txt config-mensagens '''
                with open('arquivos_txt\\red.txt',"r", encoding="utf-8") as arquivo:
                    message_red = arquivo.read()
            
                texto = message_red.replace('[LISTA_RESULTADOS]', ' | '.join(resultados))

                enviarPostAPI(canais, 'failure', texto, link_roleta).start()
            
            except Exception as e:
                print(e)


            for key,value in canais.items():

                if value[0] == 'sessao' and sessao_ativa == True:

                    try:
                        ''' Lendo o arquivo txt config-mensagens '''
                        with open('arquivos_txt\\red.txt',"r", encoding="utf-8") as arquivo:
                            message_red = arquivo.read()

                        bot.reply_to(globals()[f'sinal_{key}'], message_red.replace('[LISTA_RESULTADOS]', ' | '.join(resultados)),
                                            parse_mode = 'HTML')
                    except:
                        pass
                
                elif value[0] != 'sessao':

                    ''' Lendo o arquivo txt config-mensagens '''
                    with open('arquivos_txt\\red.txt',"r", encoding="utf-8") as arquivo:
                        message_red = arquivo.read()

                    bot.reply_to(globals()[f'sinal_{key}'], message_red.replace('[LISTA_RESULTADOS]', ' | '.join(resultados)),
                                        parse_mode = 'HTML')

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
        #Contagem Sinais por Sessão
        if sessao_ativa == True:
            contagem_sinais+=1
            placar_loss_sessao+=1

        validador_sinal = 0
        contador_cash = 0
        contador_passagem = 0
        dicionario_roletas[nome_cassino] = lista_resultados_sinal
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



# VERIFICANDO SE TEM ALGUMA ESTRATEGIA NO TXT E CARREGAR
#with open ('arquivos_txt\\estrategias.txt', 'r', encoding='UTF-8') as arquivo:
#    estrategias_salvas = arquivo.readlines()
#
#    if estrategias_salvas != [] :
#        txt_estrategias_vazio = False
#        for e in estrategias_salvas:
#            e = e.replace('\n','')
#            lista_estrategias.append(e)

#    else:
#        txt_estrategias_vazio = True
#        pass




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
        markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Ative o bot primeiro! ", reply_markup=markup)
       
    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

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
        markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_estrategia = bot.reply_to(message, "🤖⛔ Estou validando uma estratégia! Tente novamente em alguns instanstes.", reply_markup=markup)




@bot.message_handler(commands=['⚙🎰 Cadastrar_Roletas'])
def cadastrarRoletas(message):

    if contador_passagem == 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        
        nomeDosCassinos(parar)  # Mapeando nome dos cassinos
        markup_apostas = generate_buttons_estrategias([f'{roleta[0].upper()}' for roleta in cassinos], markup)    
        markup_apostas.add('◀ Voltar')

        message_roleta = bot.reply_to(message, "🤖 Ok! Escolha a Roleta que será incluída nas análises 👇. *Lembrando que se iniciar as análises sem nenhuma roleta cadastrada, TODAS as roletas do grupo Evolution serão analisadas.", reply_markup=markup_apostas)
        bot.register_next_step_handler(message_roleta, registrarRoleta)
    

    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_roleta = bot.reply_to(message, "🤖⛔ Estou validando uma estratégia! Tente novamente em alguns instanstes.", reply_markup=markup)





@bot.message_handler(commands=['🗑🧠 Apagar_Estratégia'])
def apagarEstrategia(message):
    global estrategia
    global estrategias
    global contador_passagem, lista_estrategias

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
        markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

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
        markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_excluir_roleta = bot.reply_to(message, "🤖⛔ Estou validando uma estratégia! Tente novamente em alguns instanstes.", reply_markup=markup)





@bot.message_handler(commands=['🧠📜 Estratégias_Cadastradas'])
def estrategiasCadastradas(message):
    global estrategia
    global estrategias
    global lista_estrategias

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

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
    markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

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
    markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

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
    markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

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
        🎯 Assertividade "+ asserividade,
        parse_mode='HTML', reply_markup=markup)
        
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
        markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Bot já está pausado ", reply_markup=markup)

    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

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
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=3)
        markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message, "🤖 Bot de Roletas Pragmatic Play Iniciado! ✅ Escolha uma opção 👇",
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
            markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖⛔ Bot já está ativado",
                                reply_markup=markup)

        
        elif lista_estrategias == []:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖⛔ Cadastre no mínimo 1 estratégia antes de iniciar",
                                reply_markup=markup)

        
        else:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

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


    if message_opcoes.text in ['⏰ Horário Sessões']:
        
        try:

            with open ('arquivos_txt/horario_sessoes.txt', encoding='UTF-8') as arquivo: 
                horario_sessoes = arquivo.read()

        except:pass

        try:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
            markup = markup.add(
                                horario_sessoes,
                                '◀ Voltar'
                                )

            message_editar_valor = bot.reply_to(message_opcoes, "🤖 Perfeito! Segue Horário das Sessões. Para Editar, Insira a Nova Lista de Horários Separado por vírgula (,) 👇",
                                    reply_markup=markup)
        
            #Here we assign the next handler function and pass in our response from the user. 
            bot.register_next_step_handler(message_editar_valor, registrar_horario_sessoes)
        
        except:
            message_error = bot.reply_to(message_opcoes, "🤖❌ Algo deu Errado. Tente Novamente.")

    
    if message_opcoes.text in ['🚦 Sinais por Sessão']:
        try:

            with open ('arquivos_txt/qnt_sinais_sessao.txt', encoding='UTF-8') as arquivo: 
                qntd_sinais_sessao = arquivo.read()

        except:pass

        try:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
            markup = markup.add(
                                qntd_sinais_sessao,
                                '◀ Voltar'
                                )

            message_editar_valor = bot.reply_to(message_opcoes, "🤖 Perfeito! Segue Quantidade de Sinais Por Sessão. Para Editar, Insira o Novo Valor 👇",
                                    reply_markup=markup)
        
            #Here we assign the next handler function and pass in our response from the user. 
            bot.register_next_step_handler(message_editar_valor, registrar_qntd_sinais)
        
        except:
            message_error = bot.reply_to(message_opcoes, "🤖❌ Algo deu Errado. Tente Novamente.")

    


@bot.message_handler()
def registrarTipoEstrategia(message_tipo_estrategia):
    global resposta_usuario, lista_estrategias

    if message_tipo_estrategia.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_tipo_estrategia, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        return


    if message_tipo_estrategia.text in ['ESTRATÉGIAS PADRÕES']:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')
        
        estrategias_padroes = (['repetição', '1ª coluna', '2', '2ª/3ª coluna'],
                               ['ausência', '1ª coluna', '2', '1ª/2ª coluna']
                               )
        

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
        markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

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
    markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

    resposta_usuario4 = ond_apostar.text.lower()
    onde_apostar = ([resposta_usuario, resposta_usuario2, resposta_usuario3, resposta_usuario4])
    lista_estrategias.append(onde_apostar)
    print(onde_apostar)


    #Registrando Estrategia no TXT

    if txt_estrategias_vazio == False:
        with open('arquivos_txt\\estrategias.txt', 'a', encoding='UTF-8') as arq:
            arq.write('\n'+str(onde_apostar))
    
    else:
        with open('arquivos_txt\\estrategias.txt', 'w', encoding='UTF-8') as arq:
            arq.write(str(onde_apostar))
            txt_estrategias_vazio = False


    bot.reply_to(ond_apostar, "🤖 Estratégia Cadastrada ✅", reply_markup=markup)


def registrarEstrategiaExcluida(message_excluir_estrategia):
    global estrategia
    global estrategias

    if message_excluir_estrategia.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_excluir_estrategia, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        
        return
    

    estrategia_excluir = message_excluir_estrategia.text
    
    ''' Excluindo a estratégia '''
    for estrategia in lista_estrategias:
        if estrategia_excluir == str(estrategia):
            lista_estrategias.remove(estrategia)


    ''' SUBSTITUINDO estrategia do TXT '''
    c=0
    arquivo = open('arquivos_txt\\estrategias.txt', 'w', encoding='UTF-8')
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

    ''' Excluindo da lista consolidada '''
    for estrate in lista_estrategias:
        if estrate[1] == estrategia_excluir.lower():
            lista_estrategias.remove(estrate)



    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

    bot.reply_to(message_excluir_estrategia, "🤖 Estratégia excluída com sucesso! ✅", reply_markup=markup)


def registrarRoleta(message_roleta):
    global lista_roletas
    global placar_roletas_diaria


    if message_roleta.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_roleta, "🤖 Escolha uma opção 👇", reply_markup=markup)
        return


    ''' Validando se já existe a estrategia cadastrada '''
    if message_roleta.text not in lista_roletas:

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')


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
        markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        bot.reply_to(message_roleta, "🤖 A estratégia "+str(message_roleta.text.upper())+" já foi cadastrada anteriormente ❌", reply_markup=markup)


def registrarRoletaExcluida(message_excluir_roleta):
    global estrategia
    global estrategias

    if message_excluir_roleta.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

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
        markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        bot.reply_to(message_excluir_roleta, "🤖 Roleta excluída com sucesso! ✅", reply_markup=markup)


def registrar_horario_sessoes(message_editar_valor):
    
    if message_editar_valor.text == '◀ Voltar':
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_editar_valor, "🤖 Escolha uma opção 👇",
                                    reply_markup=markup)
            
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(message_opcoes, opcoes)
    
    else:
        try:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

            with open ('arquivos_txt/horario_sessoes.txt', 'w', encoding='UTF-8') as arquivo: 
                        arquivo.write(message_editar_valor.text)

            message_sucess = bot.reply_to(message_editar_valor, "🤖 Horarios Editados com Sucesso! ✅", reply_markup=markup)
            
        except:
            pass


def registrar_qntd_sinais(message_editar_valor):

    if message_editar_valor.text == '◀ Voltar':
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_editar_valor, "🤖 Escolha uma opção 👇",
                                    reply_markup=markup)
            
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(message_opcoes, opcoes)
    
    else:
        try:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start', '⏰ Horário Sessões', '🚦 Sinais por Sessão', '✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','🛑 Pausar Bot')

            with open ('arquivos_txt/qnt_sinais_sessao.txt', 'w', encoding='UTF-8') as arquivo: 
                        arquivo.write(message_editar_valor.text)

            message_sucess = bot.reply_to(message_editar_valor, "🤖 Quantidade de Sinais Editado com Sucesso! ✅", reply_markup=markup)
            
        except:
            pass





while True:
    try:
        bot.infinity_polling(timeout=600)
    except:
        bot.infinity_polling(timeout=600)













