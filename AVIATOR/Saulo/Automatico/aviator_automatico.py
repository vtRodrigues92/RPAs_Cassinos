import PySimpleGUI as sg
import json
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
import logging
from datetime import datetime, timedelta
from telegram.ext import *
from telebot import *
import os
import ast
import warnings
from threading import Thread
from selenium.webdriver.common.action_chains import ActionChains
from tkinter import messagebox
#from webdriver_manager.firefox import GeckoDriverManager


def main():
    global parar, simulador_parar, estrategias
    global simulador_banca_inicial, simulador_stop_win, simulador_stop_loss, simulador_gale, simulador_fator_gale, simulador_valor_aposta

    parar = None
    simulador_parar = None

    simulador_banca_inicial = ''
    simulador_stop_win = ''
    simulador_stop_loss = ''
    simulador_gale = ''
    simulador_fator_gale = ''
    simulador_valor_aposta = ''

    try:
        estrategias = cadastrar_estrategias_txt()

        with open("credenciais.txt", "r", encoding='utf-8-sig') as f:
            t = f.read().replace("'", '"')
            texto = json.loads(t)
            tela = pegar_dados_salvos(texto)
            f.close()
    except:
        # criar a janela
        estrategias = ''
        tela = janela_principal()
    
    pegando_eventos(tela)


def cadastrar_estrategias_txt():
    global placar_estrategias

    with open('estrategias.txt', 'r', encoding='UTF-8') as arquivo:

        estrategias_txt = arquivo.read()
        estrategias_txt = ast.literal_eval(estrategias_txt)

        estrategias = []

        for estrategia_txt in estrategias_txt:
                
            estrategias.append(estrategia_txt)
            

        return estrategias


# GERA TXT DO PLACAR
def placar(simulador):
    global placar_win
    global placar_semGale
    global placar_gale1
    global placar_gale2
    global placar_loss
    global placar_geral
    global asserividade, placar_2x
    global data_hoje
    global placar_win_simulador
    global placar_semGale_simulador
    global placar_gale1_simulador
    global placar_gale2_simulador
    global placar_loss_simulador
    global placar_geral_simulador
    global asserividade_simulador, placar_2x_simulador
    global data_hoje_simulador, data_hoje_simulador_placar

    if simulador == False:

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
                    asserividade = arq_placar[5].split(',')[1].replace('\n','')+'%'
                    placar_2x = int(arq_placar[6].split(',')[1])
                

                except:
                    pass

                
        else:
            # Criar um arquivo com a data atual
            with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                arquivo.write("win,0\nsg,0\ng1,0\ng2,0\nloss,0\nass,0\npl2x,0")

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
                    asserividade = arq_placar[5].split(',')[1].replace('\n','')+'%'
                    placar_2x = int(arq_placar[6].split(',')[1])
                
                except:
                    pass

    else:
        
        data_hoje_simulador_placar = datetime.today().strftime('%d-%m-%Y')
        data_hoje_simulador = datetime.today().strftime('%d-%m-%Y-%H-%M-%S')
        arquivos_placares = os.listdir(r"placar/")

        if f'{data_hoje_simulador}.txt' in arquivos_placares:
            # Carregar arquivo de placar
            with open(f"placar/{data_hoje_simulador}.txt", 'r') as arquivo:
                try:

                    arq_placar = arquivo.readlines()
                    placar_win_simulador = int(arq_placar[0].split(',')[1])
                    placar_semGale_simulador = int(arq_placar[1].split(',')[1])
                    placar_gale1_simulador = int(arq_placar[2].split(',')[1])
                    placar_gale2_simulador = int(arq_placar[3].split(',')[1])
                    placar_loss_simulador = int(arq_placar[4].split(',')[1])
                    placar_geral_simulador = int(placar_win_simulador) + int(placar_loss_simulador)
                    asserividade_simulador = arq_placar[5].split(',')[1].replace('\n','')+'%'
                    

                except:
                    pass

                
        else:
            # Criar um arquivo com a data atual
            with open(f"placar/{data_hoje_simulador}.txt", 'w') as arquivo:
                arquivo.write("win,0\nsg,0\ng1,0\ng2,0\nloss,0\nass,0")

            # Ler o arquivo de placar criado
            with open(f"placar/{data_hoje_simulador}.txt", 'r') as arquivo:
                try:

                    arq_placar = arquivo.readlines()
                    placar_win_simulador = int(arq_placar[0].split(',')[1])
                    placar_semGale_simulador = int(arq_placar[1].split(',')[1])
                    placar_gale1_simulador = int(arq_placar[2].split(',')[1])
                    placar_gale2_simulador = int(arq_placar[3].split(',')[1])
                    placar_loss_simulador = int(arq_placar[4].split(',')[1])
                    placar_geral_simulador = int(placar_win_simulador) + int(placar_loss_simulador)
                    asserividade_simulador = arq_placar[5].split(',')[1].replace('\n','')+'%'
                    
                except:
                    pass


# ENVIA PLACAR CANAIS TELEGRAM
def envia_placar(simulador):

    try:
        if simulador == False:
            placar(False)

            ''' Enviando mensagem Telegram '''
            try:
                msg_placar = \
                \
                "Placar Atual do dia "+data_hoje+":\n\
    =====================\n\
    WIN - "+str(placar_win)+"\n\
    WIN S/ GALE - "+str(placar_semGale)+"\n\
    WIN GALE1 - "+str(placar_gale1)+"\n\
    WIN GALE2 - "+str(placar_gale2)+"\n\
    LOSS - "+str(placar_loss)+"\n\
    =====================\n\
    Assertividade - "+ asserividade
            

                return msg_placar   

            except:
                pass

        else:
            #placar(True)

            ''' Enviando mensagem Telegram '''
            try:
                msg_placar = \
                \
                "Placar Atual do dia "+data_hoje_simulador_placar+":\n\
    =====================\n\
    WIN - "+str(placar_win_simulador)+"\n\
    WIN S/ GALE - "+str(placar_semGale_simulador)+"\n\
    WIN GALE1 - "+str(placar_gale1_simulador)+"\n\
    WIN GALE2 - "+str(placar_gale2_simulador)+"\n\
    LOSS - "+str(placar_loss_simulador)+"\n\
    =====================\n\
    Assertividade - "+ asserividade_simulador
            

                return msg_placar   

            except:
                
                return "Inicie o simulador para ter acesso ao placar"


    except Exception as a:
        logger.error('Exception ocorrido no ' + repr(a))
        #placar = bot.reply_to(message,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%", reply_markup=markup)
        pass


def pegar_dados_salvos(json):
    
    dados = json

    valor_entrada_bet1 = dados[0].get("valor_entrada_bet1", "")
    valor_entrada_bet2 = dados[0].get("valor_entrada_bet2", "")
    fator_gale = dados[0].get("fatorgale", "")
    stop_win = dados[0].get("stopwin", "")
    stop_loss = dados[0].get("stoploss", "")
    sequencia_green = dados[0].get("seqgreen","")

    return janela_principal(valor_entrada_bet1, valor_entrada_bet2, fator_gale, stop_win, stop_loss, sequencia_green)
    

def janela_principal(valor_entrada_bet1="", valor_entrada_bet2="", fator_gale="", stop_win="", stop_loss="", sequencia_green=""):

    sg.theme('DarkBlue2')   
    # All the stuff inside your window.
    linhas = [      
                    
            [sg.Text('Valor Entrada Bet1', size=(14, 1)), sg.Input(valor_entrada_bet1, key='valor_entrada_bet1', size=(60, 5))],
            [sg.Text('Valor Entrada Bet2', size=(14, 1)), sg.Input(valor_entrada_bet2, key='valor_entrada_bet2', size=(60, 5))],
            [sg.Text('Fator Gale', size=(14, 1)), sg.Input(fator_gale, key='fator_gale', size=(60, 5))],
            [sg.Text('Stop Win', size=(14, 1)), sg.Input(stop_win, key='stop_win', size=(60, 5))],
            [sg.Text('Stop Loss', size=(14, 1)), sg.Input(stop_loss, key='stop_loss', size=(60, 5))],
            [sg.Text('Seq Green', size=(14, 1)), sg.Input(sequencia_green, key='sequencia_green', size=(60, 5))],
            [sg.Output(size=(76,20))],
            [sg.Button("Placar Atual", size=68)], [sg.Button("Estratégias", size=68)],
            [sg.Button("Validador de Estratégias", size=68)],
            [sg.Button("Ligar Bot", size=33), sg.Button("Pausar Bot", size=33)]
            

            ]

    layout = [
                [sg.Frame('CONFIGURAÇÕES', layout=linhas)],
                
            ]

    return sg.Window('BOT AVIATOR AUTOMÁTICO', layout=layout, finalize=True)


def atualizar_dodos_configuracoes():

    objetos = []
    valor_entrada_bet1_lista = []
    valor_entrada_bet2_lista = []
    fator_gale_lista = []
    stop_win_lista = []
    stop_loss_lista = []
    sequencia_green_lista = []
    
    #print(valores.items())

    for key, value in valores.items():
        
        if "valor_entrada_bet1" in key:
            valor_entrada_bet1_lista.append(value)
        elif "valor_entrada_bet2" in key:
            valor_entrada_bet2_lista.append(value)
        elif "fator_gale" in key:
            fator_gale_lista.append(value)
        elif "stop_win" in key:
            stop_win_lista.append(value)
        elif "stop_loss" in key:
            stop_loss_lista.append(value)
        elif "sequencia_green" in key:
            sequencia_green_lista.append(value)
        

    for valor_entrada_bet1, valor_entrada_bet2, fator_gale, stop_win, stop_loss, sequencia_green in zip(valor_entrada_bet1_lista, valor_entrada_bet2_lista, fator_gale_lista, stop_win_lista, stop_loss_lista, sequencia_green_lista):
        obj = {}
        obj["valor_entrada_bet1"] = valor_entrada_bet1
        obj["valor_entrada_bet2"] = valor_entrada_bet2
        obj["fatorgale"] = fator_gale
        obj["stopwin"] = stop_win
        obj["stoploss"] = stop_loss
        obj["seqgreen"] = sequencia_green
        objetos.append(obj)

    #print(objetos)
    if objetos:
        with open("credenciais.txt", "w", encoding='utf-8-sig') as f:
            f.write(str(objetos))

    return valor_entrada_bet1, valor_entrada_bet2, fator_gale, stop_win, stop_loss, sequencia_green, True


def pegando_eventos(janela):
    global valores, estrategias, valor_entrada_bet1, valor_entrada_bet2, fator_gale, stop_win, stop_loss, sequencia_green, placar_estrategias, parar, bot_status, valor_entrada_bet1_inicial, valor_entrada_bet2_inicial
    global simulador_banca_inicial, simulador_stop_win, simulador_stop_loss, simulador_fator_gale, simulador_valor_aposta, simulador_banca_atual, simulador_valor_aposta_inicial, browser, simulador_bot_ativado, simulador_parar, simulador_bot_status


    # Event Loop to process "events" and get the "values" of the inputs
    while True:

        evento, valores = janela.read()
        if evento == sg.WIN_CLOSED or evento == 'Cancel': # if user closes window or clicks cancel
            break
        
        if evento == "Ligar Bot":

            valor_entrada_bet1, valor_entrada_bet2, fator_gale, stop_win, stop_loss, sequencia_green, atualizar_dados = atualizar_dodos_configuracoes()

            if atualizar_dados == True:

                if parar == None:
                    valor_entrada_bet1_inicial = valor_entrada_bet1
                    valor_entrada_bet2_inicial = valor_entrada_bet2
                    thread_bot = Thread(target=Bot)
                    thread_bot.start()

                else:
                    parar = 0
                    bot_status = 1
                    bot_ativado = True


        if evento == "Pausar Bot":
            print(datetime.now().strftime('%d-%m-%Y - %H:%M:%S'), 'PAUSANDO BOT...')
            parar = 1
            bot_status = 0
            print(datetime.now().strftime('%d-%m-%Y - %H:%M:%S'), 'BOT PAUSADO')
            

        if evento == "Placar Atual":
            msg_placar = envia_placar(False)
            sg.popup_auto_close(msg_placar, title='PLACAR', auto_close_duration=5)

        
        if evento == "Estratégias":

            sg.theme('DarkBlue2')   
            # All the stuff inside your window.
            linhas = [      
                            
                    [sg.Multiline(estrategias, size=(100, 20))]
                    
                    ]

            layout = [
                        [sg.Frame('ESTRATEGIAS', layout=linhas)],
                        [sg.Button("Gravar Alterações", size=44), sg.Button("Cancelar", size=44)]
                        
                    ]

            janela_estrategias = sg.Window('BOT AVIATOR AUTOMÁTICO', layout=layout, finalize=True)

            while True:
                evento, valores = janela_estrategias.read()

                if evento == sg.WIN_CLOSED or evento == 'Cancelar': # if user closes window or clicks cancel
                    break
                
                if evento == "Gravar Alterações":

                    with open('estrategias.txt', 'w', encoding='UTF-8') as arquivo:

                        print(datetime.now().strftime('%d-%m-%Y - %H:%M:%S'), "ALTERAÇÃO DE ESTRATEGIA")

                        try:
                            arquivo.write(valores[0])
                            sg.popup_auto_close("Gravado com Sucesso!", auto_close_duration=4)
                        except:
                            sg.popup_auto_close("Erro na Gravação!", auto_close_duration=4)

                        
                        janela_estrategias.close()

                    estrategias = cadastrar_estrategias_txt()

            janela_estrategias.close()


        if evento == "Validador de Estratégias":

            sg.theme('DarkBlue2')   
            # All the stuff inside your window.
            linhas = [      
                            
                    [sg.Text('Banca Inicial', size=(14, 1)), sg.Input(simulador_banca_inicial, key='simulador_banca_inicial', size=(60, 5))],
                    [sg.Text('Valor Aposta', size=(14, 1)), sg.Input(simulador_valor_aposta, key='simulador_valor_aposta', size=(60, 5))],
                    [sg.Text('Stop Win', size=(14, 1)), sg.Input(simulador_stop_win, key='simulador_stop_win', size=(60, 5))],
                    [sg.Text('Stop Loss', size=(14, 1)), sg.Input(simulador_stop_loss, key='simulador_stop_loss', size=(60, 5))],
                    [sg.Text('Fator Gale', size=(14, 1)), sg.Input(simulador_fator_gale, key='simulador_fator_gale', size=(60, 5))],
                    [sg.Output(size=(100,20))],

                    ]

            layout = [
                        [sg.Frame('VALIDADOR DE ESTRATEGIAS', layout=linhas)],
                        [sg.Button("Iniciar Simulador", size=44), sg.Button("Pausar Simulador", size=44)],
                        [sg.Button("Placar Atual", size=44), sg.Button("Banca Atual", size=44)],
                        [sg.Button("Cancelar", size=90)]
                        
                    ]

            janela_simulador = sg.Window('BOT AVIATOR AUTOMÁTICO', layout=layout, finalize=True)

            while True:

                evento, valores = janela_simulador.read()

                if evento == sg.WIN_CLOSED or evento == 'Cancelar': # if user closes window or clicks cancel
                    simulador_parar = 1
                    simulador_bot_status = 0

                    janela_simulador.close()

                    janela.close()

                    main()
                    
                    break


                if evento == 'Iniciar Simulador':
                    
                    #Mapeando valores
                    for key, value in valores.items():
        
                        if "simulador_banca_inicial" in key:
                            simulador_banca_inicial = value
                        elif "simulador_stop_win" in key:
                            simulador_stop_win = value
                        elif "simulador_stop_loss" in key:
                            simulador_stop_loss = value
                        elif "simulador_fator_gale" in key:
                            simulador_fator_gale = value
                        elif "simulador_valor_aposta" in key:
                            simulador_valor_aposta = value
                            simulador_valor_aposta_inicial = value
                    
                    if simulador_parar == None:
                        simulador_banca_atual = simulador_banca_inicial
                        thread_bot = Thread(target=Simulador)
                        thread_bot.start()

                    else:
                        simulador_parar = 0
                        simulador_bot_status = 1
                        simulador_banca_atual = simulador_banca_inicial
                        thread_bot = Thread(target=Simulador)
                        thread_bot.start()


                if evento == "Placar Atual":
                    msg_placar = envia_placar(True)
                    sg.popup_auto_close(msg_placar, title='PLACAR', auto_close_duration=5)


                if evento == 'Banca Atual':
                    try:
                        sg.popup_auto_close(f'Você está com R$ {simulador_banca_atual} de banca', title='Banca Atual', auto_close_duration=5)
                    except:
                        sg.popup_auto_close("Inicie o simulador para usar essa função.", title='Banca Atual', auto_close_duration=5)
                

                if evento == "Pausar Simulador":
                    print(datetime.now().strftime('%d-%m-%Y - %H:%M:%S'), 'PAUSANDO BOT...')
                    simulador_parar = 1
                    simulador_bot_status = 0
                    print(datetime.now().strftime('%d-%m-%Y - %H:%M:%S'), 'BOT PAUSADO')

            janela_simulador.close()


    janela.close()




#######################################################################################################################################


class Bot():

    def __init__(self):
        global parar, bot_status, reladiarioenviado, contador_passagem, validador_sequencia_green, bot_ativado
        
        bot_status = 1
        reladiarioenviado = 0
        parar=0
        contador_passagem = 0
        validador_sequencia_green = 0
        bot_ativado = True

        self.run()


    # VALIDADOR DE DATA
    def validaData(self):
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
            self.placar()
            reladiarioenviado +=1

        # Condição que zera o placar quando o dia muda
        if horario_atual == '00:01' and reladiarioenviado == 1:
            reladiarioenviado = 0

        
    def auto_refresh(self):
        global horario_inicio

        horario_atual = datetime.today().strftime('%H:%M')
        tres_hora = timedelta(hours=1)
        horario_mais_tres = horario_inicio + tres_hora
        horario_refresh = horario_mais_tres.strftime('%H:%M')

        if horario_atual >= horario_refresh:
            print('HORA DE REFRESHAR A PAGINA!!!!')
            self.logar_site()
            time.sleep(10)
            horario_inicio = datetime.now()


    def inicio(self):
        global sticker_alerta
        global sticker_win
        global sticker_win_2x
        global sticker_win_5x
        global sticker_loss
        global logger
        global browser
        global lista_anterior
        global horario_inicio
        
        self.log('INICIANDO BOT')
        horario_inicio = datetime.now()

        lista_anterior = []
        logger = logging.getLogger()

        # Definindo opções para o browser
        warnings.filterwarnings("ignore", category=DeprecationWarning) 
        chrome_options = webdriver.ChromeOptions() 
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        #chrome_options.add_argument("--disable-gpu")        

        browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)                      # Chrome
        #browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())


    def logar_site(self):
        global cash_out_1_ativado, cash_out_2_ativado

        #logger = logging.getLogger()
        browser.get(r"https://blaze.com/")
        time.sleep(10)

        try:
            browser.maximize_window()
        except:
            pass

        try:

            ''' Inserindo login e senha '''
            ''' Lendo o arquivo txt config-mensagens '''
            txt = open("canais.txt", "r", encoding="utf-8")
            mensagem_login = txt.readlines()
            usuario = mensagem_login[2].replace('\n','').split('= ')[1] 
            senha = mensagem_login[3].replace('\n','').split('= ')[1]

            while True:
                try:

                    ''' Mapeando elementos para inserir credenciais '''
                    browser.find_element_by_xpath('//*[@class="link"]').click()                                           #Clicando no botão Entrar
                    time.sleep(5)                                           
                    browser.find_element_by_xpath('//*[@class="input-wrapper"]//*[@name="username"]').send_keys(usuario)  #Inserindo login
                    browser.find_element_by_xpath('//*[@class="input-wrapper"]//*[@name="password"]').send_keys(senha)    #Inserindo senha
                    browser.find_element_by_xpath('//*[@class="input-footer"]//*[@type="button"]').click()                #Clicando no btn login
                    time.sleep(10)
                    break

                except:
                    break
                    #print('ERRO AO INSERIR LOGIN -- CONTATE O DESENVOLVEDOR')

            ''' Verificando se o login foi feito com sucesso'''
            t3 = 0
            while t3 < 20:
                if browser.find_elements_by_xpath('//*[@class="amount"]'):
                    break
                else:
                    t3+=1
        
        except:
            pass

        try:
        
            ''' Entrando no game '''
            browser.get(r"https://blaze.com/pt/games/aviator")
            time.sleep(15)

            tela_cheia = browser.find_element_by_xpath('//*[@id="game_wrapper"]/iframe').get_attribute('src')
                                                    
            browser.get(tela_cheia)
            time.sleep(15)

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
            
            
        except:
            pass       
        
        #time.sleep(10)

        #Ativando Botão Auto
        try:
            if float(valor_entrada_bet1) > 0:
                browser.find_elements_by_xpath('//*[@class="navigation-switcher"]')[1].click()
            
            time.sleep(2)
            
            if float(valor_entrada_bet2) > 0:
                browser.find_elements_by_xpath('//*[@class="navigation-switcher"]')[2].click()

            time.sleep(2)

        except:pass

        time.sleep(3)
        cash_out_1_ativado = 0
        cash_out_2_ativado = 0

        while cash_out_1_ativado == 0 and cash_out_2_ativado == 0:

            #Ativar Auto cashOut
            try:

                if float(valor_entrada_bet1) > 0:
                    browser.find_elements_by_xpath('//*[@class="input-switch off"]')[3].click()
                    cash_out_1_ativado+=1

                time.sleep(2)
                
                if float(valor_entrada_bet2) > 0:
                    browser.find_elements_by_xpath('//*[@class="input-switch off"]')[3].click()
                    cash_out_2_ativado+=1

                break
            
            except:
                try:

                    time.sleep(3)

                    if float(valor_entrada_bet1) > 0:
                        browser.find_elements_by_xpath('//*[@class="input-switch off"]')[0].click()
                        cash_out_1_ativado+=1

                    time.sleep(2)

                    if float(valor_entrada_bet2) > 0:
                        browser.find_elements_by_xpath('//*[@class="input-switch off"]')[0].click()
                        cash_out_2_ativado+=1

                    break

                except:
                    self.logar_site()
                    continue        

        
        self.log('INICIADO COM SUCESSO')

                    
    def enviar_alerta(self):
        global contador_passagem

        ''' Lendo o arquivo txt canais '''
        txt = open("canais.txt", "r", encoding="utf-8")
        arquivo = txt.readlines()
        canais = arquivo[12].replace('canais= ','').replace('\n','')
        canais = ast.literal_eval(canais) # Convertendo string em dicionario 

        ''' Lendo o arquivo txt config-mensagens '''
        txt = open("config-mensagens.txt", "r", encoding="utf-8")
        mensagem_alerta = txt.readlines()

        try:
        
            self.log(mensagem_alerta[0].replace('\n',''))
            self.log(mensagem_alerta[2].replace('\n',''))
                        

        except:
            pass

        contador_passagem = 1


    def enviar_sinal(self, vela_atual, estrategia):
        global table_sinal

        ''' Lendo o arquivo txt canais '''
        txt = open("canais.txt", "r", encoding="utf-8")
        arquivo = txt.readlines()
        canais = arquivo[12].replace('canais= ','').replace('\n','')
        canais = ast.literal_eval(canais) # Convertendo string em dicionario 

        ''' Lendo o arquivo txt config-mensagens '''
        txt = open("config-mensagens.txt", "r", encoding="utf-8")
        mensagem_sinal = txt.readlines()

        ''' Enviando mensagem Telegram '''
        try:
            
            # Estruturando mensgaem
            self.log(mensagem_sinal[17].replace('\n',''))
            self.log(mensagem_sinal[19].replace('\n','').replace('[VELA_ATUAL]', vela_atual))
            self.log(mensagem_sinal[21].replace('\n','').replace('[VALOR_ENTRADA_BET1]', valor_entrada_bet1).replace('[VALOR_ENTRADA_BET2]', valor_entrada_bet2))
            self.log(mensagem_sinal[22].replace('\n','').replace('[CASH_OUT_BET1]', estrategia[-2]))
            
         
        except:
            pass
        

    def apagar_alerta(self):
        global contador_passagem

        try:
            self.log('ENTRADA NÃO CONFIRMADA')
        except:pass
        
        contador_passagem = 0


    def validador_estrategia(self, estrategia, lista_resultados, sequencia_minima):
        # Validando se o resultado se encaixa na estratégia ( TRUE ou FALSE )
        validador = []
        try:
            for e in enumerate(estrategia[:-2]): 
                for v in enumerate(lista_resultados[int(-sequencia_minima):]):

                    while v[0] == e[0]:
                        if '+' in e[1]:
                            if float(v[1]) > float(e[1][1:]):
                                validador.append(True)
                                break
                            else:
                                validador.append(False)
                                break

                            
                        if '-' in e[1]:
                            if float(v[1]) < float(e[1][1:]):
                                validador.append(True)
                                break
                            else:
                                validador.append(False)
                                break


                        else:
                            print('ERRO NA ESTRATÉGIA ', estrategia,'...VERIFIQUE O CADASTRO DA MESMA.')
                            time.sleep(3)
                            break


            #print(f'Validador  --> {validador}')
            return validador
        except:
            pass


    def coletar_dados(self):
        global estrategia
        global lista_resultados, bot_status, saldo_inicial

        self.log('INICIANDO ANALISE DAS ESTRATÉGIAS')
        
        #Pegando Saldo inicial
        try:
            saldo_inicial = browser.find_elements_by_xpath('//*[@class="balance px-2 d-flex justify-content-end align-items-center"]')[0].text
        except:pass

        self.log(f'SALDO INICIAL {saldo_inicial}')

        while True:

            # Validando data para envio do relatório diário
            #validaData()

            # Validando se foi solicitado o stop do BOT
            if parar != 0:
                bot_status = 0

                break
            else:
                pass
            
        
            while True:
                try:
                    # Auto Refresh
                    #auto_refresh()

                    # Validando data para envio do relatório diário
                    #validaData()
                    
                    # Validando se foi solicitado o stop do BOT
                    if parar != 0:
                        bot_status = 0
                        break
                    else:
                        pass

                    
                    lista_resultados = []
                    # Pegando o histórico de resultados
                    historico_velas = browser.find_elements_by_xpath('//*[@class="payout ng-star-inserted"]')
                    
                    ''' Inserindo velas na lista'''
                    try:
                        for vela in reversed(historico_velas[:10]):
                            numero = vela.text.replace('x','')
                            lista_resultados.append(numero)
                    except:
                        print('Erro ao inserir resultados na Lista... Refreshando...')
                        self.logar_site()
                        continue
                    

                    ''' VALIDANDO SE TEM DADO VAZIO NA LISTA'''
                    if '' in lista_resultados:
                        continue

                    ''' VALIDANDO SE A LISTA ESTA VAZIA'''
                    if lista_resultados == []:
                        self.logar_site()
                        continue

                    
                    # Validando se foi solicitado o stop do BOT
                    if parar != 0:
                        bot_status = 0
                        break
                    else:
                        pass
                    

                    #print(datetime.now().strftime('%H:%M'))
                    ''' Chama a função que valida a estratégia para enviar o sinal Telegram '''
                    self.validar_estrategia(estrategias)   #Lista de estrategia

                    #print('=' * 100)
                    lista_resultados = []
                    break

                    ''' Exceção se o jogo não estiver disponível '''
                except Exception as e:
                    print(e)
                    self.logar_site()


    def validar_estrategia(self, estrategias):
        global gale
        global vela_atual
        global lista_resultados, bot_status, cashOut

        try:
            for estrategia in estrategias:

                # Validando se foi solicitado o stop do BOT
                if parar != 0:
                    bot_status = 0
                    break
                else:
                    pass


                #print ('Analisando a Estrategia --> ', estrategia)

                sequencia_minima_alerta = len(estrategia[:-3])
                sequencia_minima_sinal = len(estrategia[:-2])
                cashOut = float(estrategia[-2].strip('xX'))

                #print('Historico_Velas --> ', lista_resultados)

                ''' VALIDADOR DE ESTRATEGIA '''
                validador = self.validador_estrategia(estrategia, lista_resultados, sequencia_minima_alerta)

                ''' Validando se bateu alguma condição'''
                if validador.count(True) == int(sequencia_minima_alerta):
                    #ENVIANDO ALERTA
                    self.enviar_alerta()
                    #print('=' * 50)


                    ''' Verifica se a ultima condição bate com a estratégia para enviar sinal Telegram '''
                    while True:
                        
                        # Relatório de Placar
                        #validaData()

                        # Validando se foi solicitado o stop do BOT
                        if parar != 0:
                            bot_status = 0
                            break
                        else:
                            pass
                        
                        ''' Lendo novos resultados para validação da estratégia'''
                        numeros_recentes_validacao = browser.find_elements_by_xpath('//*[@class="payout ng-star-inserted"]')
                            
                        ''' LISTA DO PROXIMO RESULTADO APOS O ALERTA'''
                        lista_proximo_resultados = []
                        try:
                            for numeroRecente in reversed(numeros_recentes_validacao[:10]):
                                numero_r = numeroRecente.text.replace('x','')
                                lista_proximo_resultados.append(numero_r)
                        except:
                            continue
                        
                        #print(lista_proximo_resultados)

                        if '' in lista_proximo_resultados:
                            continue
                        

                        ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
                        if lista_resultados != lista_proximo_resultados:
                            validador = self.validador_estrategia(estrategia, lista_proximo_resultados, sequencia_minima_sinal)


                            ''' VALIDA SE ENVIA SINAL OU APAGA O ALERTA '''
                            if validador.count(True) == int(sequencia_minima_sinal):
                                #print(lista_proximo_resultados[-1])

                                if bot_ativado == True:
                                    self.fazer_aposta(valor_entrada_bet1, valor_entrada_bet2, estrategia[-2])
                                else:
                                    pass
                                
                                #print('=' * 50)
                                vela_atual = lista_proximo_resultados[-1]
                                self.enviar_sinal(vela_atual, estrategia)
                                self.checar_sinal_enviado(lista_proximo_resultados, estrategia)
                                time.sleep(1)
                                break


                            else:
                                #print('APAGA SINAL DE ALERTA')
                                #print('=' * 100)
                                self.apagar_alerta()
                                lista_resultados = lista_proximo_resultados
                                break
                
                else:
                    pass
                    #print('=' * 100)


        except:
            pass


    def checar_sinal_enviado(self, lista_proximo_resultados, estrategia):
        global table
        global message_canal
        global resultados_sinais
        global ultimo_horario_resultado
        global validador_sinal
        global stop_loss
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
        global placar_2x
        global lista_resultados, bot_status, valor_gale, bot_ativado, validador_sequencia_green, valor_entrada_bet1_inicial, valor_entrada_bet2_inicial, valor_entrada_bet1, valor_entrada_bet2


        resultados = []
        contador_cash = 0
        gale = estrategia[-1]
        

        while contador_cash <= int(gale):

            # Validando data para envio do relatório diário
            #validaData()

            # Validando se foi solicitado o stop do BOT
            if parar != 0:
                bot_status = 0
                break
            else:
                pass


            try:
                ''' Lendo novos resultados para validação da estratégia'''
                numeros_recentes_validacao = browser.find_elements_by_xpath('//*[@class="payout ng-star-inserted"]')

                lista_resultados_sinal = []
                try:
                    for numeroRecente in reversed(numeros_recentes_validacao[:10]):
                        numero_r = numeroRecente.text.replace('x','')
                        lista_resultados_sinal.append(numero_r)
                except:
                    continue


                if '' in lista_resultados_sinal:
                    continue
                

                ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
                if lista_proximo_resultados != lista_resultados_sinal:

                    resultados.append(lista_resultados_sinal[-1])
                    
                    #print(lista_resultados_sinal[-1])
                    #alimenta_banco_painel(lista_resultados_sinal)
                
                    # VALIDANDO WIN OU LOSS
                    if float(lista_resultados_sinal[-1]) >= float(estrategia[-2].strip('xX')):
                        
                        #Verificando se a vela é maior que 2x
                        if float(lista_resultados_sinal[-1]) >= 2: 
                            placar_2x +=1


                        if contador_cash == 0:
                            #self.log('WIN SEM GALE')
                            #stop_loss.append('win')

                            if bot_ativado == True:

                                # Atualizando placar e Alimentando o arquivo txt
                                placar_win +=1
                                placar_semGale +=1
                                placar_geral = placar_win + placar_loss

                                try:
                                    with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                                        arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}\npl2x,{placar_2x}")
                                except:
                                    pass
                                    
                                #print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")

                            else:
                                pass

                            
                        if contador_cash == 1:
                            #self.log('WIN GALE1')
                            #stop_loss.append('win')
                            
                            if bot_ativado == True:
                                # Atualizando placar e Alimentando o arquivo txt
                                placar_win +=1
                                placar_gale1 +=1
                                placar_geral = placar_win + placar_loss

                                try:
                                    with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                                        arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}\npl2x,{placar_2x}")
                                except:
                                    pass

                                #print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
                                #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)
                            else:
                                pass


                        if contador_cash == 2:
                            #self.log('WIN GALE2')

                            if bot_ativado == True:
                                # Atualizando placar e Alimentando o arquivo txt
                                placar_win +=1
                                placar_gale2 +=1
                                placar_geral = placar_win + placar_loss

                                try:
                                    with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                                        arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}\npl2x,{placar_2x}")
                                except:
                                    pass
                                    
                                #print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
                                #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)
                            else:
                                pass


                        if int(gale) > 2 and bot_ativado == True:
                            # Somando WIN no Placar Geral
                            placar_win +=1


                        # respondendo a mensagem do sinal e condição para enviar sticker
                        try:
                            ''' Lendo o arquivo txt canais '''
                            txt = open("canais.txt", "r", encoding="utf-8")
                            arquivo = txt.readlines()
                            canais = arquivo[12].replace('canais= ','').replace('\n','')
                            canais = ast.literal_eval(canais) # Convertendo string em dicionario 
                        
                            ''' Lendo o arquivo txt config-mensagens '''
                            txt = open("config-mensagens.txt", "r", encoding="utf-8")
                            mensagem_green = txt.readlines()
                        
                            try:
                                
                                self.log(mensagem_green[31].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(resultados)))
                                self.log(mensagem_green[32].replace('\n','').replace('[GREEN]',str(placar_win)).replace('[LOSS]', str(placar_loss)))
                                self.log(mensagem_green[33].replace('\n','').replace('[ASSERTIVIDADE]', str(round(placar_win / (placar_geral)*100, 0))))

                                #Enviando Saldo Atualizado
                                novo_saldo = self.pegar_saldo()
                                self.log(f'SALDO ATUAL {novo_saldo}')
                                #Validando StopWin
                                self.validar_stop_win()

                            except:
                                pass
                                
                        except:
                            pass
                        
                        #print('=' * 100)
                        validador_sinal = 0
                        contador_cash = 0
                        contador_passagem = 0
                        lista_resultados = lista_resultados_sinal
                        valor_entrada_bet1 = valor_entrada_bet1_inicial
                        valor_entrada_bet2 = valor_entrada_bet2_inicial

                        if bot_ativado == True:
                            validador_sequencia_green+=1

                        if str(validador_sequencia_green) == sequencia_green:
                            self.log("SEQUENCIA DE GREEN ATINGIDA. PAUSANDO AS APOSTAS")
                            bot_ativado = False
                            validador_sequencia_green = 0


                        return
            
                    else:
                        self.log('LOSSS')
                        #print('=' * 100)
                        contador_cash+=1
                        lista_proximo_resultados = lista_resultados_sinal
                        self.validar_stop_loss()
                            
                        if contador_cash <= int(gale) and bot_ativado == True:

                            valor_gale_bet1 = round(float(valor_entrada_bet1),2) * float(fator_gale)
                            valor_gale_bet2 = round(float(valor_entrada_bet2),2) * float(fator_gale)
                            self.fazer_aposta(valor_gale_bet1, valor_gale_bet2, estrategia[-2])
                            self.log(f'EXECUTANDO MATINGALE{contador_cash}')

                            valor_entrada_bet1 = round(float(valor_entrada_bet1),2) * float(fator_gale)
                            valor_entrada_bet2 = round(float(valor_entrada_bet2),2) * float(fator_gale)

                        continue
            
            except:
                continue


        if contador_cash > int(gale):
            self.log('LOSSS GALE '+ estrategia[-1])

            if bot_ativado == True:
                # Preenchendo arquivo txt
                placar_loss +=1
                placar_geral = placar_win + placar_loss

                try:
                    with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                        arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}\npl2x,{placar_2x}")
                except:
                    pass    
                
                #print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
                    
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

                
                try:

                    self.log(mensagem_green[37].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(resultados)))
                    self.log(mensagem_green[38].replace('\n','').replace('[GREEN]',str(placar_win)).replace('[LOSS]', str(placar_loss)))
                    self.log(mensagem_green[39].replace('\n','').replace('[ASSERTIVIDADE]', str(round(placar_win / (placar_geral)*100, 0))))

                except:
                    pass
                
            except:
                pass


            #print('=' * 100)
            #Enviando Saldo Atualizado
            novo_saldo = self.pegar_saldo()
            self.log(f'SALDO ATUAL {novo_saldo}')
            self.validar_stop_loss()
            validador_sinal = 0
            contador_cash = 0
            contador_passagem = 0
            lista_resultados = lista_resultados_sinal
            valor_entrada_bet1 = valor_entrada_bet1_inicial
            valor_entrada_bet2 = valor_entrada_bet2_inicial

            # ATIVANDO BOT APOS LOSS
            if bot_ativado == False:
                self.log("ATIVANDO AS APOSTAS")
                bot_ativado = True

            if bot_ativado == True:
                self.log("REINICIANDO CONTAGEM DE GREENS SEGUIDOS")
                validador_sequencia_green = 0
                


            return


    def cadastrar_estrategias_txt(self):
        global placar_estrategias

        with open('estrategias.txt', 'r', encoding='UTF-8') as arquivo:

            estrategias_txt = arquivo.read()
            estrategias_txt = ast.literal_eval(estrategias_txt)

            estrategias = []

            for estrategia_txt in estrategias_txt:
                    
                estrategias.append(estrategia_txt)
                

            return estrategias


    def fazer_aposta(self, valor_bet1, valor_bet2, cash_out):
    
        while True:
            try:

                action = ActionChains(browser)
                
                if float(valor_bet1) > 0:
                    #Dois Cliques no Campo valor da bet 1 com Action Chains
                    elemento_campo_valor =  browser.find_elements_by_xpath('//*[@class="font-weight-bold"]')[0]
                    action.double_click(on_element = elemento_campo_valor)
                    action.send_keys(str(valor_bet1))

                    #Dois Cliques no Campo CashOut da bet 1 com Action Chains
                    elemento_campo_cashout = browser.find_elements_by_xpath('//*[@class="font-weight-bold"]')[1]
                    action.double_click(on_element = elemento_campo_cashout)
                    action.send_keys(str(cash_out))

                #if float(valor_bet2) > 0:
                    #Dois Cliques no Campo valor da bet 2 com Action Chains
                #    elemento_campo_valor =  browser.find_elements_by_xpath('//*[@class="font-weight-bold"]')[2]
                #    action.double_click(on_element = elemento_campo_valor)
                #    action.send_keys(str(valor_bet2))

                    #Dois Cliques no Campo CashOut da bet 1 com Action Chains
                #    elemento_campo_cashout = browser.find_elements_by_xpath('//*[@class="font-weight-bold"]')[3]
                #    action.double_click(on_element = elemento_campo_cashout)
                #    action.send_keys(str(cash_out_bet2))

                #Efetivando as ações
                action.perform()
                
                if float(valor_bet1) > 0:
                    #Clicando no botão Apostar bet 1
                    browser.find_elements_by_xpath('//*[@class="btn btn-success bet ng-star-inserted"]')[0].click()
                
                #if float(valor_bet2) > 0:
                    #Clicando no botão Apostar bet 2
                #    browser.find_elements_by_xpath('//*[@class="btn btn-success bet ng-star-inserted"]')[0].click()
                    
                break

            except:continue

    
    def pegar_saldo(self):

        try:
            
            saldo = browser.find_elements_by_xpath('//*[@class="balance px-2 d-flex justify-content-end align-items-center"]')[0].text
            return saldo
        
        except:pass


    def log(self, mensagem):
        print(datetime.now().strftime('%d-%m-%Y - %H:%M:%S'), mensagem)


    def validar_stop_win(self):
        global parar, bot_status, bot_ativado

        time.sleep(3)

        saldo_atualizado = browser.find_elements_by_xpath('//*[@class="balance px-2 d-flex justify-content-end align-items-center"]')[0].text.strip(' BRLUSD')

        if (float(saldo_atualizado) - float(saldo_inicial.strip(' BRLUSD'))) >= int(stop_win):

            print(datetime.now().strftime('%d-%m-%Y - %H:%M:%S'),"STOP WIN ATINGIDO!!! PAUSANDO AS OPERAÇÕES")
            parar = 1
            bot_status = 0
            bot_ativado = False
            
            messagebox.showinfo("STOP WIN", "PARABÉNS! STOP WIN ATINGIDO!")
            #sg.popup_auto_close('PARABÉNS! STOP WIN ATINGIDO!', title='STOP WIN', auto_close_duration=5)
            

    def validar_stop_loss(self):
        global parar, bot_status, bot_ativado

        time.sleep(3)

        saldo_atualizado = browser.find_elements_by_xpath('//*[@class="balance px-2 d-flex justify-content-end align-items-center"]')[0].text.strip(' BRLUSD')

        if  (float(saldo_inicial.strip(' BRLUSD')) - float(saldo_atualizado)) >= int(stop_loss):

            print(datetime.now().strftime('%d-%m-%Y - %H:%M:%S'),"STOP LOSS ATINGIDO. PAUSANDO AS OPERAÇÕES")

            parar = 1
            bot_status = 0
            bot_ativado = False
            
            messagebox.showerror("STOP LOSS", "EITA! STOP LOSS ATINGIDO! MANTENHA O GERENCIAMENTO!")
            #sg.popup_auto_close('EITA! STOP LOSS ATINGIDO! MANTENHA O GERENCIAMENTO!', title='STOP LOSS', auto_close_duration=5)



    def run(self):
        global estrategias

        self.inicio()             # Difinição do webBrowser
        self.logar_site()         # Logando no Site
        placar(False)             # Chamando o Placar

        while True:
            if bot_status == 1:
                estrategias = self.cadastrar_estrategias_txt()
                self.coletar_dados()      #Iniciano analises
            


class Simulador():


    def __init__(self):
        global simulador_parar, simulador_bot_status, contador_passagem, simulador_bot_ativado
        
        simulador_bot_status = 1
        simulador_parar = 0
        contador_passagem = 0
        simulador_bot_ativado = True

        self.run()

    
    def iniciar_browser(self):
        global simulador_browser

        try:
            # Definindo opções para o browser
            warnings.filterwarnings("ignore", category=DeprecationWarning) 
            chrome_options = webdriver.ChromeOptions() 
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            #chrome_options.add_argument("--disable-gpu")        

            simulador_browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)                      # Chrome
            #browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())

            simulador_browser.get(r"http://186.195.175.50:8888/aviator") #Produção
            #browser.get('http://127.0.0.1:3000/index.html') #Homologação
            time.sleep(10)

            try:
                simulador_browser.maximize_window()
            except:
                pass


        except:pass


    def enviar_alerta(self):
        global simulador_contador_passagem

        ''' Lendo o arquivo txt canais '''
        txt = open("canais.txt", "r", encoding="utf-8")
        arquivo = txt.readlines()
        canais = arquivo[12].replace('canais= ','').replace('\n','')
        canais = ast.literal_eval(canais) # Convertendo string em dicionario 

        ''' Lendo o arquivo txt config-mensagens '''
        txt = open("config-mensagens.txt", "r", encoding="utf-8")
        mensagem_alerta = txt.readlines()

        try:
        
            self.log(mensagem_alerta[0].replace('\n',''))
            self.log(mensagem_alerta[2].replace('\n',''))
                        

        except:
            pass

        simulador_contador_passagem = 1


    def enviar_sinal(self, vela_atual, estrategia):
        global table_sinal

        ''' Lendo o arquivo txt canais '''
        txt = open("canais.txt", "r", encoding="utf-8")
        arquivo = txt.readlines()
        canais = arquivo[12].replace('canais= ','').replace('\n','')
        canais = ast.literal_eval(canais) # Convertendo string em dicionario 

        ''' Lendo o arquivo txt config-mensagens '''
        txt = open("config-mensagens.txt", "r", encoding="utf-8")
        mensagem_sinal = txt.readlines()

        ''' Enviando mensagem Telegram '''
        try:
            
            # Estruturando mensgaem
            self.log(mensagem_sinal[17].replace('\n',''))
            self.log(mensagem_sinal[19].replace('\n','').replace('[VELA_ATUAL]', vela_atual))
            self.log(mensagem_sinal[21].replace('\n','').replace('[VALOR_ENTRADA_BET1]', valor_entrada_bet1).replace('[VALOR_ENTRADA_BET2]', valor_entrada_bet2))
            self.log(mensagem_sinal[22].replace('\n','').replace('[CASH_OUT_BET1]', estrategia[-2]))
            
         
        except:
            pass
        

    def apagar_alerta(self):
        global simulador_contador_passagem

        try:
            self.log('ENTRADA NÃO CONFIRMADA')
        except:pass
        
        simulador_contador_passagem = 0


    def validador_estrategia(self, estrategia, lista_resultados, sequencia_minima):
        # Validando se o resultado se encaixa na estratégia ( TRUE ou FALSE )
        validador = []
        try:
            for e in enumerate(estrategia[:-2]): 
                for v in enumerate(lista_resultados[int(-sequencia_minima):]):

                    while v[0] == e[0]:
                        if '+' in e[1]:
                            if float(v[1]) > float(e[1][1:]):
                                validador.append(True)
                                break
                            else:
                                validador.append(False)
                                break

                            
                        if '-' in e[1]:
                            if float(v[1]) < float(e[1][1:]):
                                validador.append(True)
                                break
                            else:
                                validador.append(False)
                                break


                        else:
                            print('ERRO NA ESTRATÉGIA ', estrategia,'...VERIFIQUE O CADASTRO DA MESMA.')
                            time.sleep(3)
                            break


            #print(f'Validador  --> {validador}')
            return validador
        except:
            pass


    def coletar_dados(self):
        global estrategia
        global lista_resultados, simulador_bot_status, simulador_saldo_inicial

        self.log('INICIANDO ANALISE DAS ESTRATÉGIAS')
        
        #Pegando Saldo inicial
        try:
            saldo_inicial_simulador = simulador_banca_inicial
        except:pass

        self.log(f'SALDO INICIAL {simulador_banca_inicial}')

        while True:

            # Validando data para envio do relatório diário
            #validaData()

            # Validando se foi solicitado o stop do BOT
            if simulador_parar != 0:
                simulador_bot_status = 0

                break
            else:
                pass
            
        
            while True:
                try:

                    # Validando se foi solicitado o stop do BOT
                    if simulador_parar != 0:
                        simulador_bot_status = 0
                        break
                    else:
                        pass

                    lista_resultados = []
                    # Pegando o histórico de resultados
                    historico_velas = simulador_browser.find_element_by_id('results').text.split('\n')
                    
                    ''' Inserindo velas na lista'''
                    try:

                        for vela in reversed(historico_velas[:40]):
                            if ':' in vela:
                                continue
                            else:
                                lista_resultados.append(vela)

                    except Exception as e:
                        self.log(f'Erro ao inserir resultados na Lista - {e}')
                        continue
                    

                    ''' VALIDANDO SE TEM DADO VAZIO NA LISTA'''
                    if '' in lista_resultados:
                        continue

                    ''' VALIDANDO SE A LISTA ESTA VAZIA'''
                    if lista_resultados == []:
                        self.log('Lista de resultados está vazia.')
                        continue

                    
                    # Validando se foi solicitado o stop do BOT
                    if simulador_parar != 0:
                        simulador_bot_status = 0
                        break
                    else:
                        pass
                    

                    ''' Chama a função que valida a estratégia para enviar o sinal Telegram '''
                    self.validar_estrategia(estrategias)   #Lista de estrategia

                    lista_resultados = []
                    break

                    ''' Exceção se o jogo não estiver disponível '''
                except Exception as e:
                    simulador_browser.refresh()
                    #self.log(f'Algo inesperado aconteceu -- {e}')


    def validar_estrategia(self, estrategias):
        global gale
        global vela_atual
        global lista_resultados, simulador_bot_status, simulador_cashOut, simulador_valor_aposta_inicial, simulador_saldo_antes_aposta

        try:
            for estrategia in estrategias:

                # Validando se foi solicitado o stop do BOT
                if simulador_parar != 0:
                    simulador_bot_status = 0
                    break
                else:
                    pass


                #print ('Analisando a Estrategia --> ', estrategia)

                sequencia_minima_alerta = len(estrategia[:-3])
                sequencia_minima_sinal = len(estrategia[:-2])
                simulador_cashOut = float(estrategia[-2].strip('xX'))
                
                #print('Historico_Velas --> ', lista_resultados)

                ''' VALIDADOR DE ESTRATEGIA '''
                validador = self.validador_estrategia(estrategia, lista_resultados, sequencia_minima_alerta)

                ''' Validando se bateu alguma condição'''
                if validador.count(True) == int(sequencia_minima_alerta):
                    #ENVIANDO ALERTA
                    self.enviar_alerta()
                    #print('=' * 50)

                    ''' Verifica se a ultima condição bate com a estratégia para enviar sinal Telegram '''
                    while True:
                        
                        # Relatório de Placar
                        #validaData()

                        # Validando se foi solicitado o stop do BOT
                        if simulador_parar != 0:
                            simulador_bot_status = 0
                            break
                        else:
                            pass
                        
                        ''' Lendo novos resultados para validação da estratégia'''
                        numeros_recentes_validacao = simulador_browser.find_element_by_id('results').text.split('\n')
                            
                        ''' LISTA DO PROXIMO RESULTADO APOS O ALERTA'''
                        lista_proximo_resultados = []
                        try:
                            for vela in reversed(numeros_recentes_validacao[:40]):
                                if ':' in vela:
                                    continue
                                else:
                                    lista_proximo_resultados.append(vela)
                        except:
                            continue
                        
                        #print(lista_proximo_resultados)

                        if '' in lista_proximo_resultados:
                            continue
                        
                        if lista_proximo_resultados == []:
                            continue

                        ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
                        if lista_resultados != lista_proximo_resultados:
                            validador = self.validador_estrategia(estrategia, lista_proximo_resultados, sequencia_minima_sinal)


                            ''' VALIDA SE ENVIA SINAL OU APAGA O ALERTA '''
                            if validador.count(True) == int(sequencia_minima_sinal):

                                #print('=' * 50)
                                vela_atual = lista_proximo_resultados[-1]
                                
                                if simulador_bot_ativado == True:
                                    
                                    #SALVANDO SALDO ANTES DE APOSTAR
                                    simulador_saldo_antes_aposta = simulador_banca_atual
                                    #TIRANDO VALOR DA APOSTA NO SALDO
                                    self.tirar_valor_saldo(round(float(simulador_valor_aposta),2))

                                    #MENSAGEM
                                    self.log(f'SINAL CONFIRMADO! APOSTANDO {simulador_valor_aposta} NO CASHOUT {estrategia[-2]}')
                                    self.checar_sinal_enviado(lista_proximo_resultados, estrategia)
                                    time.sleep(1)
                                    break
                                
                                else:
                                    pass

                            else:
                                #print('APAGA SINAL DE ALERTA')
                                #print('=' * 100)
                                self.apagar_alerta()
                                lista_resultados = lista_proximo_resultados
                                break
                
                else:
                    pass
                    #print('=' * 100)


        except:
            pass


    def checar_sinal_enviado(self, lista_proximo_resultados, estrategia):
        global table
        global message_canal
        global resultados_sinais
        global ultimo_horario_resultado
        global validador_sinal
        global stop_loss
        global simulador_contador_passagem
        global lista_resultados_sinal
        global placar_win_simulador
        global placar_semGale_simulador
        global placar_gale1_simulador
        global placar_gale2_simulador
        global placar_loss_simulador
        global placar_geral_simulador
        global asserividade_simulador
        global data_hoje_simulador
        global placar_2x_simulador, simulador_saldo_antes_aposta
        global lista_resultados, simulador_bot_status, simulador_bot_ativado, validador_sequencia_green, simulador_banca_inicial, simulador_banca_final, asserividade_simulador, simulador_valor_aposta, simulador_valor_aposta_inicial


        resultados = []
        contador_cash = 0
        gale = estrategia[-1]
        cashOut = float(estrategia[-2].strip('xX'))
        

        while contador_cash <= int(gale):

            # Validando data para envio do relatório diário
            #validaData()

            # Validando se foi solicitado o stop do BOT
            if simulador_parar != 0:
                simulador_bot_status = 0
                break
            else:
                pass


            try:
                ''' Lendo novos resultados para validação da estratégia'''
                numeros_recentes_validacao = simulador_browser.find_element_by_id('results').text.split('\n')

                lista_resultados_sinal = []
                try:
                    for vela in reversed(numeros_recentes_validacao[:40]):
                        if ':' in vela:
                            continue
                        else:
                            lista_resultados_sinal.append(vela)
                except:
                    continue


                if '' in lista_resultados_sinal:
                    continue
                

                ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
                if lista_proximo_resultados != lista_resultados_sinal:

                    resultados.append(lista_resultados_sinal[-1])
                    
                    #print(lista_resultados_sinal[-1])
                    #alimenta_banco_painel(lista_resultados_sinal)
                
                    # VALIDANDO WIN OU LOSS
                    if float(lista_resultados_sinal[-1]) >= float(estrategia[-2].strip('xX')):


                        if contador_cash == 0:
                            #self.log('WIN SEM GALE')
                            #stop_loss.append('win')

                            if simulador_bot_ativado == True:

                                # Atualizando placar e Alimentando o arquivo txt
                                placar_win_simulador +=1
                                placar_semGale_simulador +=1
                                placar_geral_simulador = placar_win_simulador + placar_loss_simulador
                                asserividade_simulador = str(round(placar_win_simulador / (placar_geral_simulador)*100, 0))

                                try:
                                    with open(f"placar/{data_hoje_simulador}.txt", 'w') as arquivo:
                                        arquivo.write(f"win,{placar_win_simulador}\nsg,{placar_semGale_simulador}\ng1,{placar_gale1_simulador}\ng2,{placar_gale2_simulador}\nloss,{placar_loss_simulador}\nass,{str(round(placar_win_simulador / (placar_geral_simulador)*100, 0)).replace('.0','')}")
                                except:
                                    pass
                                    
                                #print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")

                            else:
                                pass

                            
                        if contador_cash == 1:
                            #self.log('WIN GALE1')
                            #stop_loss.append('win')
                            
                            if simulador_bot_ativado == True:
                                # Atualizando placar e Alimentando o arquivo txt
                                placar_win_simulador +=1
                                placar_gale1_simulador +=1
                                placar_geral_simulador = placar_win_simulador + placar_loss_simulador
                                asserividade_simulador = str(round(placar_win_simulador / (placar_geral_simulador)*100, 0))

                                try:
                                    with open(f"placar/{data_hoje_simulador}.txt", 'w') as arquivo:
                                        arquivo.write(f"win,{placar_win_simulador}\nsg,{placar_semGale_simulador}\ng1,{placar_gale1_simulador}\ng2,{placar_gale2_simulador}\nloss,{placar_loss_simulador}\nass,{str(round(placar_win_simulador / (placar_geral_simulador)*100, 0)).replace('.0','')}")
                                except:
                                    pass

                                #print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
                                #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)
                            else:
                                pass


                        if contador_cash == 2:
                            #self.log('WIN GALE2')

                            if simulador_bot_ativado == True:
                                # Atualizando placar e Alimentando o arquivo txt
                                placar_win_simulador +=1
                                placar_gale2_simulador +=1
                                placar_geral_simulador = placar_win_simulador + placar_loss_simulador
                                asserividade_simulador = str(round(placar_win_simulador / (placar_geral_simulador)*100, 0))

                                try:
                                    with open(f"placar/{data_hoje_simulador}.txt", 'w') as arquivo:
                                        arquivo.write(f"win,{placar_win_simulador}\nsg,{placar_semGale_simulador}\ng1,{placar_gale1_simulador}\ng2,{placar_gale2_simulador}\nloss,{placar_loss_simulador}\nass,{str(round(placar_win_simulador / (placar_geral_simulador)*100, 0)).replace('.0','')}")
                                except:
                                    pass
                                    
                                #print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
                                #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)
                            else:
                                pass


                        if int(gale) > 2 and simulador_bot_ativado == True:
                            # Somando WIN no Placar Geral
                            placar_win_simulador +=1

                        #SOMANDO GANHO NO SALDO
                        self.somar_valor_saldo(float(simulador_valor_aposta) * cashOut)

                        # respondendo a mensagem do sinal e condição para enviar sticker
                        try:
                
                            ''' Lendo o arquivo txt config-mensagens '''
                            txt = open("config-mensagens.txt", "r", encoding="utf-8")
                            mensagem_green = txt.readlines()
                        
                            try:
                                
                                self.log(mensagem_green[31].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(resultados)))
                                self.log(mensagem_green[32].replace('\n','').replace('[GREEN]',str(placar_win_simulador)).replace('[LOSS]', str(placar_loss_simulador)))
                                self.log(mensagem_green[33].replace('\n','').replace('[ASSERTIVIDADE]', str(round(placar_win_simulador / (placar_geral_simulador)*100, 0))))

                                #Enviando Saldo Atualizado
                                #novo_saldo = int(simulador_banca_inicial)
                                self.log(f'SALDO ATUAL {str(simulador_banca_atual)}')
                                self.log(f'LUCRO REAL DA SESSÃO - {round(simulador_banca_atual - float(simulador_saldo_antes_aposta),2)}')
                                #Validando StopWin
                                self.validar_stop_win()
                                self.validar_stop_loss()

                            except:
                                pass
                                
                        except:
                            pass
                        
                        #print('=' * 100)
                        validador_sinal = 0
                        contador_cash = 0
                        simulador_contador_passagem = 0
                        lista_resultados = lista_resultados_sinal
                        simulador_valor_aposta = simulador_valor_aposta_inicial

                        return
            
                    else:
                        self.log('LOSSS')
                        #print('=' * 100)
                        contador_cash+=1
                        lista_proximo_resultados = lista_resultados_sinal

                        self.validar_stop_loss()
                        
                        if contador_cash <= int(gale) and simulador_bot_ativado == True:
                            
                            self.log(f'SALDO ATUAL {round(simulador_banca_atual,2)}')
                            self.tirar_valor_saldo(round(float(simulador_valor_aposta)*float(simulador_fator_gale),2))
                            self.log(f'EXECUTANDO MATINGALE{contador_cash} APOSTANDO {round(float(simulador_valor_aposta)*float(simulador_fator_gale),2)} NO CASHOUT {estrategia[-2]}')
                            self.log(f'SALDO ATUAL {round(simulador_banca_atual,2)}')
                            simulador_valor_aposta = round(float(simulador_valor_aposta)*float(simulador_fator_gale),2)

                        continue
            
            except Exception as e:
                simulador_browser.refresh()
                continue


        if contador_cash > int(gale):
            self.log('LOSSS GALE '+ estrategia[-1])

            if simulador_bot_ativado == True:
                # Preenchendo arquivo txt
                placar_loss_simulador +=1
                placar_geral_simulador = placar_win_simulador + placar_loss_simulador
                asserividade_simulador = str(round(placar_win_simulador / (placar_geral_simulador)*100, 0))

                try:
                    with open(f"placar/{data_hoje_simulador}.txt", 'w') as arquivo:
                        arquivo.write(f"win,{placar_win_simulador}\nsg,{placar_semGale_simulador}\ng1,{placar_gale1_simulador}\ng2,{placar_gale2_simulador}\nloss,{placar_loss_simulador}\nass,{str(round(placar_win_simulador / (placar_geral_simulador)*100, 0)).replace('.0','')}\npl2x,{placar_2x}")
                except:
                    pass    
                
                #print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
                    
            # editando mensagem
            try:
                
                ''' Lendo o arquivo txt config-mensagens '''
                txt = open("config-mensagens.txt", "r", encoding="utf-8")
                mensagem_green = txt.readlines()

                
                try:

                    self.log(mensagem_green[37].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(resultados)))
                    self.log(mensagem_green[38].replace('\n','').replace('[GREEN]',str(placar_win_simulador)).replace('[LOSS]', str(placar_loss_simulador)))
                    self.log(mensagem_green[39].replace('\n','').replace('[ASSERTIVIDADE]', str(round(placar_win_simulador / (placar_geral_simulador)*100, 0))))

                except:
                    pass
                
            except:
                pass


            #print('=' * 100)
            #Enviando Saldo Atualizado
            #novo_saldo = simulador_banca_inicial
            self.log(f'SALDO ATUAL {simulador_banca_atual}')
            self.validar_stop_loss()
            validador_sinal = 0
            contador_cash = 0
            simulador_contador_passagem = 0
            lista_resultados = lista_resultados_sinal
            simulador_valor_aposta = simulador_valor_aposta_inicial

            # ATIVANDO BOT APOS LOSS
            if simulador_bot_ativado == False:
                self.log("ATIVANDO AS APOSTAS")
                simulador_bot_ativado = True

            
            return


    def tirar_valor_saldo(self, valor):
        global simulador_banca_inicial, simulador_banca_atual

        try:
        
            simulador_banca_atual = round((float(simulador_banca_atual) - valor),2)

        except:pass


    def somar_valor_saldo(self, valor):
        global simulador_banca_inicial, simulador_banca_atual

        try:

            simulador_banca_atual = round((float(simulador_banca_atual) + valor),2)

        except:
            pass


    def log(self, mensagem):
        print(datetime.now().strftime('%d-%m-%Y - %H:%M:%S'), mensagem)


    def validar_stop_win(self):
        global simulador_parar, simulador_bot_status, simulador_banca_atual, simulador_bot_ativado

        time.sleep(3)

        saldo_atualizado = simulador_banca_atual

        if (float(saldo_atualizado) - float(simulador_banca_inicial)) >= int(simulador_stop_win):

            print(datetime.now().strftime('%d-%m-%Y - %H:%M:%S'),"STOP WIN ATINGIDO!!! PAUSANDO AS OPERAÇÕES")
            simulador_parar = 1
            simulador_bot_status = 0
            simulador_bot_ativado = False
            
            messagebox.showinfo("STOP WIN", f"PARABÉNS! STOP WIN ATINGIDO! SALDO ATUAL R${simulador_banca_atual}")
            #sg.popup_auto_close('PARABÉNS! STOP WIN ATINGIDO!', title='STOP WIN', auto_close_duration=5)
            

    def validar_stop_loss(self):
        global simulador_parar, simulador_bot_status, placar_loss_simulador, placar_geral_simulador, asserividade_simulador, simulador_bot_ativado

        time.sleep(3)

        saldo_atualizado = simulador_banca_atual

        if  (float(simulador_banca_inicial)) - float(saldo_atualizado) >= float(simulador_stop_loss):

            print(datetime.now().strftime('%d-%m-%Y - %H:%M:%S'),"STOP LOSS ATINGIDO. PAUSANDO AS OPERAÇÕES")

            simulador_parar = 1
            simulador_bot_status = 0
            simulador_bot_ativado = False
            
            messagebox.showerror("STOP LOSS", f"EITA! STOP LOSS ATINGIDO! MANTENHA O GERENCIAMENTO! \n BANCA ATUAL R${simulador_banca_atual}")
            #sg.popup_auto_close('EITA! STOP LOSS ATINGIDO! MANTENHA O GERENCIAMENTO!', title='STOP LOSS', auto_close_duration=5)

            # Preenchendo arquivo txt
            placar_loss_simulador +=1
            placar_geral_simulador = placar_win_simulador + placar_loss_simulador
            asserividade_simulador = str(round(placar_win_simulador / (placar_geral_simulador)*100, 0))

            try:
                with open(f"placar/{data_hoje_simulador}.txt", 'w') as arquivo:
                    arquivo.write(f"win,{placar_win_simulador}\nsg,{placar_semGale_simulador}\ng1,{placar_gale1_simulador}\ng2,{placar_gale2_simulador}\nloss,{placar_loss_simulador}\nass,{str(round(placar_win_simulador / (placar_geral_simulador)*100, 0)).replace('.0','')}\npl2x,{placar_2x}")
            except:
                pass    








    def run(self):
        #Chamar Placar
        placar(True)

        #Iniciar Browser
        self.iniciar_browser()

        #Fazer Simulação
        self.coletar_dados()










if __name__=="__main__":
    main()

    