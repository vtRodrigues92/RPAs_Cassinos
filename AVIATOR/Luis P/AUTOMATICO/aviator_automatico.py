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
def placar():
    global placar_win
    global placar_semGale
    global placar_gale1
    global placar_gale2
    global placar_loss
    global placar_geral
    global asserividade, placar_2x
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

    except Exception as a:
        logger.error('Exception ocorrido no ' + repr(a))
        #placar = bot.reply_to(message,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%", reply_markup=markup)
        pass


def pegar_dados_salvos(json):
    
    dados = json

    valor_entrada = dados[0].get("valor_entrada", "")
    fator_gale = dados[0].get("fatorgale", "")
    stop_win = dados[0].get("stopwin", "")
    stop_loss = dados[0].get("stoploss", "")
    sequencia_green = dados[0].get("seqgreen","")

    return janela_principal(valor_entrada, fator_gale, stop_win, stop_loss, sequencia_green)
    

def janela_principal(valor_entrada="", fator_gale="", stop_win="", stop_loss="", sequencia_green=""):

    sg.theme('DarkBlue2')   
    # All the stuff inside your window.
    linhas = [      
                    
            [sg.Text('Valor Entrada', size=(10, 1)), sg.Input(valor_entrada, key='valor_entrada', size=(60, 5))],
            [sg.Text('Fator Gale', size=(10, 1)), sg.Input(fator_gale, key='fator_gale', size=(60, 5))],
            [sg.Text('Stop Win', size=(10, 1)), sg.Input(stop_win, key='stop_win', size=(60, 5))],
            [sg.Text('Stop Loss', size=(10, 1)), sg.Input(stop_loss, key='stop_loss', size=(60, 5))],
            [sg.Text('Seq Green', size=(10, 1)), sg.Input(sequencia_green, key='sequencia_green', size=(60, 5))],
            [sg.Output(size=(72,20))],
            [sg.Button("Placar Atual", size=64)], [sg.Button("Estratégias", size=64)],
            [sg.Button("Ligar Bot", size=31), sg.Button("Pausar Bot", size=31)]
            

            ]

    layout = [
                [sg.Frame('CONFIGURAÇÕES', layout=linhas)],
                
            ]

    return sg.Window('BOT AVIATOR AUTOMÁTICO', layout=layout, finalize=True)


def atualizar_dodos_configuracoes():

    objetos = []
    valor_entrada_lista = []
    fator_gale_lista = []
    stop_win_lista = []
    stop_loss_lista = []
    sequencia_green_lista = []
    
    #print(valores.items())

    for key, value in valores.items():
        
        if "valor_entrada" in key:
            valor_entrada_lista.append(value)
        elif "fator_gale" in key:
            fator_gale_lista.append(value)
        elif "stop_win" in key:
            stop_win_lista.append(value)
        elif "stop_loss" in key:
            stop_loss_lista.append(value)
        elif "sequencia_green" in key:
            sequencia_green_lista.append(value)
        

    for valor_entrada, fator_gale, stop_win, stop_loss, sequencia_green in zip(valor_entrada_lista, fator_gale_lista, stop_win_lista, stop_loss_lista, sequencia_green_lista):
        obj = {}
        obj["valor_entrada"] = valor_entrada
        obj["fatorgale"] = fator_gale
        obj["stopwin"] = stop_win
        obj["stoploss"] = stop_loss
        obj["seqgreen"] = sequencia_green
        objetos.append(obj)

    #print(objetos)
    if objetos:
        with open("credenciais.txt", "w", encoding='utf-8-sig') as f:
            f.write(str(objetos))

    return valor_entrada, fator_gale, stop_win, stop_loss, sequencia_green, True


def pegando_eventos(janela):
    global valores, estrategias, valor_entrada, fator_gale, stop_win, stop_loss, sequencia_green, placar_estrategias, parar, bot_status

    # Event Loop to process "events" and get the "values" of the inputs
    while True:

        evento, valores = janela.read()
        if evento == sg.WIN_CLOSED or evento == 'Cancel': # if user closes window or clicks cancel
            break
        
        if evento == "Ligar Bot":

            valor_entrada, fator_gale, stop_win, stop_loss, sequencia_green, atualizar_dados = atualizar_dodos_configuracoes()

            if atualizar_dados == True:

                if parar == None:
                    thread_bot = Thread(target=Bot)
                    thread_bot.start()

                else:
                    parar = 0
                    bot_status = 1


        if evento == "Pausar Bot":
            print(datetime.now().strftime('%d-%m-%Y - %H:%M:%S'), 'PAUSANDO BOT...')
            parar = 1
            bot_status = 0
            print(datetime.now().strftime('%d-%m-%Y - %H:%M:%S'), 'BOT PAUSADO')
            

        if evento == "Placar Atual":
            msg_placar = envia_placar()
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

        if horario_atual == '11:55' and reladiarioenviado == 0 or horario_atual == '23:55' and reladiarioenviado == 0:
            self.envia_placar()
            reladiarioenviado +=1

        
        if horario_atual == '11:56' and reladiarioenviado == 1 or horario_atual == '23:56' and reladiarioenviado == 1:
            reladiarioenviado = 0

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
        global cash_outativado

        #logger = logging.getLogger()
        browser.get(r"https://betfast.io/br/casino/gamepage?gameid=20870")
        try:
            browser.maximize_window()
        except:
            pass

        time.sleep(5)

        try:
            browser.refresh()
            time.sleep(5)
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

                    browser.find_element_by_xpath('//*[@name="userName"]').send_keys(usuario) 
                    #Inserindo senha
                    browser.find_element_by_xpath('//*[@name="password"]').send_keys(senha) 
                    #Clicando no btn login
                    browser.find_element_by_xpath('//*[@type="submit"]').click()            
                    time.sleep(5)
                    break

                except:
                    break
                    #print('ERRO AO INSERIR LOGIN -- CONTATE O DESENVOLVEDOR')

            ''' Verificando se o login foi feito com sucesso'''
            t3 = 0
            while t3 < 20:
                if browser.find_elements_by_xpath('//*[@class="username"]'):
                    break
                else:
                    t3+=1
        
        except:
            pass

        #ACESSANDO O IFRAME
        try:
            c=0
            while c < 10:
                try:
                    iframe = browser.find_element_by_name('game_iframe')
                    browser.switch_to_frame(iframe)
                    break
                except:
                    c+=1
                    time.sleep(3)
        except:
            pass
        
        time.sleep(10)
        #Ativando Botão Auto
        try:
            browser.find_elements_by_xpath('//*[@class="navigation-switcher"]')[1].click()
        except:pass

        time.sleep(3)
        cash_outativado = 0

        while cash_outativado == 0:

            #Ativar Auto cashOut
            try:
                browser.find_elements_by_xpath('//*[@class="input-switch off"]')[1].click()
                cash_outativado+=1
                break
            
            except:
                try:
                    browser.find_elements_by_xpath('//*[@class="input-switch off"]')[3].click()
                    cash_outativado+=1
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
            self.log(mensagem_sinal[21].replace('\n','').replace('[VALOR_ENTRADA]', valor_entrada))
            self.log(mensagem_sinal[22].replace('\n','').replace('[CASH_OUT]', estrategia[-2]))
            
         
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
                                    self.fazer_aposta(valor_entrada)
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
        global lista_resultados, bot_status, valor_gale, bot_ativado, validador_sequencia_green


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
                                self.log(mensagem_green[33].replace('\n','').replace('[MAIOR_2X]', str(placar_2x)))
                                self.log(mensagem_green[34].replace('\n','').replace('[ASSERTIVIDADE]', str(round(placar_win / (placar_geral)*100, 0))))

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

                        if contador_cash <= int(gale) and bot_ativado == True:

                            valor_gale = int(valor_entrada) * int(fator_gale) * contador_cash
                            self.fazer_aposta(valor_gale)
                            self.log(f'EXECUTANDO MATINGALE{contador_cash}')

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

                    self.log(mensagem_green[38].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(resultados)))
                    self.log(mensagem_green[39].replace('\n','').replace('[GREEN]',str(placar_win)).replace('[LOSS]', str(placar_loss)))
                    self.log(mensagem_green[40].replace('\n','').replace('[MAIOR_2X]', str(placar_2x)))
                    self.log(mensagem_green[41].replace('\n','').replace('[ASSERTIVIDADE]', str(round(placar_win / (placar_geral)*100, 0))))

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


    def fazer_aposta(self, valor):
    
        while True:
            try:
                action = ActionChains(browser)
                
                #Dois Cliques no Campo valor com Action Chains
                elemento_campo_valor =  browser.find_elements_by_xpath('//*[@class="font-weight-bold"]')[0]
                action.double_click(on_element = elemento_campo_valor)
                action.send_keys(valor)
                #Dois Cliques no Campo CashOut com Action Chains
                elemento_campo_cashout = browser.find_elements_by_xpath('//*[@class="font-weight-bold"]')[1]
                action.double_click(on_element = elemento_campo_cashout)
                action.send_keys(str(cashOut))
                action.perform()
                
                #Clicando no botão Apostar
                browser.find_elements_by_xpath('//*[@class="btn btn-success bet ng-star-inserted"]')[0].click()
                
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
        global parar, bot_status

        time.sleep(3)

        saldo_atualizado = browser.find_elements_by_xpath('//*[@class="balance px-2 d-flex justify-content-end align-items-center"]')[0].text

        if (float(saldo_atualizado.split(' BRL')[0]) - float(saldo_inicial.split(' BRL')[0])) >= int(stop_win):

            print(datetime.now().strftime('%d-%m-%Y - %H:%M:%S'),"STOP WIN ATINGIDO!!! PAUSANDO AS OPERAÇÕES")
            parar = 1
            bot_status = 0
            
            messagebox.showinfo("STOP WIN", "PARABÉNS! STOP WIN ATINGIDO!")
            #sg.popup_auto_close('PARABÉNS! STOP WIN ATINGIDO!', title='STOP WIN', auto_close_duration=5)
            

    def validar_stop_loss(self):
        global parar, bot_status

        time.sleep(3)

        saldo_atualizado = browser.find_elements_by_xpath('//*[@class="balance px-2 d-flex justify-content-end align-items-center"]')[0].text

        if  (float(saldo_inicial.split(' BRL')[0]) - float(saldo_atualizado.split(' BRL')[0])) >= int(stop_loss):

            print(datetime.now().strftime('%d-%m-%Y - %H:%M:%S'),"STOP LOSS ATINGIDO. PAUSANDO AS OPERAÇÕES")

            parar = 1
            bot_status = 0
            
            messagebox.showerror("STOP LOSS", "EITA! STOP LOSS ATINGIDO! MANTENHA O GERENCIAMENTO!")
            #sg.popup_auto_close('EITA! STOP LOSS ATINGIDO! MANTENHA O GERENCIAMENTO!', title='STOP LOSS', auto_close_duration=5)



    def run(self):
        global estrategias

        self.inicio()             # Difinição do webBrowser
        self.logar_site()         # Logando no Site
        placar()                  # Chamando o Placar

        while True:
            if bot_status == 1:
                estrategias = self.cadastrar_estrategias_txt()
                self.coletar_dados()      #Iniciano analises
            























if __name__=="__main__":
    global parar, estrategias

    parar = None

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

    