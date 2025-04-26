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

    sg.theme('Dark')   
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

    return sg.Window('BOT ROLETAS AUTOMÁTICO', layout=layout, finalize=True)


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


    def resgatar_historico(self, nome_roleta):
        global historico_roleta
        global resultado

        while True:
            try:
                ''' Elemento das roletas e historico de resultados '''
                roletas = browser.find_elements_by_xpath('//*[@class="lobby-table "]')

                if roletas == []:
                    self.logarSite()
                    continue

                else:
                    pass

                ''' Percorrendo as roletas com historico'''
                for roulette in roletas:
                    if roulette.text.split('\n')[-2] == nome_roleta:
                        #COLETANDO INFORMAÇÕES
                        #Historico de resultados da Roleta
                        historico_roleta = self.formatar_resultados(roulette) # Formata o historico em lista

                        return historico_roleta, roulette

            
            except:
                pass


    def apostas(self, ):
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


    def apostasExternas(self, estrategia_usuario, dic_estrategia_usuario):
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
                    break
                    #print(dic_estrategia_usuario)
            
            return dic_estrategia_usuario
        
        except:
            pass
                

    def formatar_resultados(self, roleta):  

        lista_resultados = []

        try:

            resultados = roleta.text.split('\n')[:-3]
            for numero in resultados:
                if 'x' not in numero:
                    lista_resultados.append(numero)
                
            
            return lista_resultados
        
        except:
            pass

    
    def formatar_resultados_mesa(self, roleta):  

        lista_resultados = []

        try:

            resultados = roleta.text.split('\n')
            for numero in resultados:
                if 'x' not in numero:
                    lista_resultados.append(numero)
                
            
            return lista_resultados
        
        except:
            pass


    def nomeDosCassinos(self, nome_cassino):
        global cassinos
        global nome_dos_cassinos

        nome_dos_cassinos = [
            
            ('Türkçe Lightning Rulet'),
            ('XXXtreme Lightning Roulette'),
            ('Lightning Roulette'),
            ('Ruletka Live'),
            ('Instant Roulette'),
            ('VIP Roulette'),
            ('Immersive Roulette'),
            ('Roulette'),
            ('American Roulette'),
            ('Auto-Roulette VIP'),
            ('Auto-Roulette'),
            ('Speed Auto Roulette'),
            ('Auto-Roulette La Partage'),
            ('French Roulette Gold'),
            ('Türkçe Rulet'),
            ('Football Studio Roulette'),
            ('Ruleta en Vivo'),
            ('Speed Roulette'),
            ('Deutsches Roulette'),
            ('Grand Casino Roulette'),
            ('Hippodrome Grand Casino'),
            ('Dragonara Roulette'),
            ('Arabic Roulette'),
            ('Lightning Roulette Italia'),
            ('Roleta Relâmpago')

            ]

        cassinos = [

            ('Türkçe Lightning Rulet',''),
            ('XXXtreme Lightning Roulette',''),
            ('Lightning Roulette',''),
            ('Ruletka Live',''),
            ('Instant Roulette',''),
            ('VIP Roulette',''),
            ('Immersive Roulette',''),
            ('Roulette',''),
            ('American Roulette',''),
            ('Auto-Roulette VIP',''),
            ('Auto-Roulette',''),
            ('Speed Auto Roulette',''),
            ('Auto-Roulette La Partage',''),
            ('French Roulette Gold',''),
            ('Türkçe Rulet',''),
            ('Football Studio Roulette',''),
            ('Ruleta en Vivo',''),
            ('Speed Roulette',''),
            ('Deutsches Roulette',''),
            ('Grand Casino Roulette',''),
            ('Hippodrome Grand Casino',''),
            ('Dragonara Roulette',''),
            ('Arabic Roulette',''),
            ('Lightning Roulette Italia',''),
            ('Roleta Relâmpago','')

        ]

        #try:
        #    for c in cassinos:
        #        if c[0] == nome_roleta:
        #            url_cassino = c[1]
        #            break
            
        #    return url_cassino
        #except:
        #    pass


    def link_cassino(self, nome_cassino):

        roletas_e_links = [

            #('Türkçe Lightning Rulet','https://betfast.io/br/casino/gamepage?gameid='),
            ('XXXtreme Lightning Roulette','https://betfast.io/br/casino/gamepage?gameid=19816'),
            #('Lightning Roulette','https://betfast.io/br/casino/gamepage?gameid='),
            ('Ruletka Live','https://betfast.io/br/casino/gamepage?gameid=5763'),
            ('Instant Roulette','https://betfast.io/br/casino/gamepage?gameid=13145'),
            ('VIP Roulette','https://betfast.io/br/casino/gamepage?gameid=5772'),
            ('Immersive Roulette','https://betfast.io/br/casino/gamepage?gameid=5751'),
            ('Roulette','https://betfast.io/br/casino/gamepage?gameid=10071'),
            ('American Roulette','https://betfast.io/br/casino/gamepage?gameid=5673'),
            ('Auto-Roulette VIP','https://betfast.io/br/casino/gamepage?gameid=5677'),
            ('Auto-Roulette','https://betfast.io/br/casino/gamepage?gameid=5675'),
            ('Speed Auto Roulette','https://betfast.io/br/casino/gamepage?gameid=7766'),
            ('Auto-Roulette La Partage','https://betfast.io/br/casino/gamepage?gameid=5676'),
            ('French Roulette Gold','https://betfast.io/br/casino/gamepage?gameid=5747'),
            ('Türkçe Rulet','https://betfast.io/br/casino/gamepage?gameid=5768'),
            #('Grand Casino Roulette','https://betfast.io/br/casino/gamepage?gameid='),
            #('Football Studio Roulette','https://betfast.io/br/casino/gamepage?gameid='),
            #('Ruleta en Vivo','https://betfast.io/br/casino/gamepage?gameid='),
            ('Speed Roulette','https://betfast.io/br/casino/gamepage?gameid=5766'),
            ('Deutsches Roulette','https://betfast.io/br/casino/gamepage?gameid=5730'),
            ('Hippodrome Grand Casino','https://betfast.io/br/casino/gamepage?gameid=10632'),
            ('Dragonara Roulette','https://betfast.io/br/casino/gamepage?gameid=10630'),
            ('Arabic Roulette','https://betfast.io/br/casino/gamepage?gameid=5674'),
            ('Lightning Roulette Italia','https://betfast.io/br/casino/gamepage?gameid=20732'),
            ('Roleta Relâmpago','https://betfast.io/br/casino/gamepage?gameid=20745')

        ]

        for roleta in roletas_e_links:
            if roleta[0] == nome_cassino:
                return roleta[1]


    def inicio(self):
        global browser
        global lobby_cassinos
        global logger
        global horario_inicio
        global lista_anterior
        

        lista_anterior = []
        horario_inicio = datetime.now()
        logger = logging.getLogger()

        # Definindo opções para o browser
        warnings.filterwarnings("ignore", category=DeprecationWarning) 
        chrome_options = webdriver.ChromeOptions() 
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)


    def logarSite(self):

        browser.get('https://betfast.io/br/casino/gamepage?gameid=20732')
        try:
            browser.maximize_window()
        except:
            pass
        
        time.sleep(10)
        ''' Inserindo login e senha '''
        ''' Lendo o arquivo txt config-mensagens '''
        txt = open('canais.txt', "r", encoding="utf-8")
        mensagem_login = txt.readlines()
        usuario = mensagem_login[2].replace('\n','').split('= ')[1] 
        senha = mensagem_login[3].replace('\n','').split('= ')[1]


            
        while True:
            try:
                
                #browser.find_element_by_xpath('//*[@class="btn login"]').click()
                #time.sleep(2)
                browser.find_element_by_xpath('//*[@name="userName"]').send_keys(usuario) 
                #Inserindo senha
                browser.find_element_by_xpath('//*[@name="password"]').send_keys(senha) 
                #Clicando no btn login
                browser.find_element_by_xpath('//*[@type="submit"]').click()            
                time.sleep(10)
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


        #ACESSANDO TELA EVOLUTION 
        try:

            browser.get('https://live.wirebankers.com/frontend/evo/r2/#category=roulette&game=roulette')  
            time.sleep(10)

        except:
            pass

        #ACESSANDO IFRAME DO GAME
        c=0
        while c <= 10:
            try:
            
                iframe = browser.find_element_by_xpath('/html/body/div[6]/div[2]/iframe')
                browser.switch_to_frame(iframe)
                break
            
            except:
                time.sleep(3)
                c+=1


    def acessar_iframe(self, elemento_1, elemento_2):
        a=0
        try:
            while a < 10:
                try:

                    ###IFRAME1
                    iframe = browser.find_element_by_name(elemento_1)
                    browser.switch_to_frame(iframe)
                    break

                except:
                    a+=1
                    time.sleep(2)
                
            while a < 10:
                try:
                    
                    ###IFRAME2
                    iframe = browser.find_element_by_xpath(elemento_2)
                    browser.switch_to_frame(iframe)
                    break

                except:
                    a+=1
                    continue

        except:
            pass


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


    def coletarResultados(self):
        global url_cassino
        global dicionario_roletas
        global contador_passagem
        global horario_atual
        global nome_cassino, link_roleta, saldo_inicial

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
        
        self.log('INICIANDO ANALISE DAS ESTRATÉGIAS')
        
        #Pegando Saldo inicial
        try:
            saldo_inicial = browser.find_elements_by_xpath('//*[@class="Typography--46b8a Typography_xs_subtitle1--c55ab Typography_md_h6--ebc04 Typography_xl_h5--c919c bold--9a1d2 colorAccent--e5a5e"]')[0].text
        except:pass

        self.log(f'SALDO INICIAL {saldo_inicial}')


        while True:

            # Validando se foi solicitado o stop do BOT
            if parar != 0:
                break
            else:
                pass
            
            # VALIDAR SE FOI DESCONECTADO
            if browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[6]/div/div[2]/div[2]/button') or browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[5]/div/div[2]/div/div[3]/button'):
                browser.refresh()
                self.logarSite()
                continue

            try:
                ''' Elemento das roletas e historico de resultados '''
                roletas = browser.find_elements_by_xpath('//*[@class="GridListItem--b95c7"]')

                if roletas == []:
                    self.logarSite()

                else:
                    pass

                ''' Percorrendo as roletas com historico'''
                for roleta in roletas:
                    
                    #COLETANDO INFORMAÇÕES
                    #Historico de resultados da Roleta
                    historico_roleta = self.formatar_resultados(roleta) # Formata o historico em lista
                    

                    if historico_roleta == None or historico_roleta == [] or historico_roleta == '':
                        continue
                    else:
                        pass

                    #Nome do Cassino
                    try:

                        nome_cassino = roleta.text.split('\n')[-3]
                        link_roleta = self.link_cassino(nome_cassino)

                    except:
                        pass


                    if link_roleta == '' or link_roleta == None:
                        continue
                    else:
                        pass
                    
                    #Nome e Link da Roleta
                    #nome_cassino = roleta[1].text
                    self.nomeDosCassinos(nome_cassino)

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
                        self.logarSite()
                    else:
                        pass

                    #print(horario_atual)

                    ''' Chama a função que valida a estratégia para enviar o sinal Telegram'''
                    self.validarEstrategia(dicionario_roletas, nome_cassino, roleta)
                    print('=' * 150)
                    
                
            except:
                self.logarSite()
                ''' Pegando a relação de roletas '''
                roletas = browser.find_elements_by_css_selector('.lobby .lobby-table-name')

                ''' removendo roletas sem historico '''
                roletas_com_historico = [] 
                for roleta in enumerate(roletas):

                    self.nomeDosCassinos(roleta[1].text)

                    if roleta[1].text in nome_dos_cassinos:
                        roletas_com_historico.append(roleta[1])
                        pass
                    else:
                        continue
                
                    continue 
        
 
    def validarEstrategia(self, dicionario_roletas, nome_cassino, roleta):
        global estrategia
        global contador_passagem
        global lista_resultados_sinal

        try:

            for estrategia in estrategias:
                
                # Validando se foi solicitado o stop do BOT
                if parar != 0:
                    break
                else:
                    pass

                
                # VALIDAR SE FOI DESCONECTADO
                if browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[6]/div/div[2]/div[2]/button') or browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[5]/div/div[2]/div/div[3]/button'):
                    browser.refresh()
                    self.logarSite()
                    continue


                ''' Pegando o tipo de aposta (AUSENCIA OU REPETIÇÃO '''
                tipo_aposta = estrategia[0]

                ''' Pegando os números da aposta externa da estratégia'''
                aposta_externa = self.apostasExternas(estrategia[1], dic_estrategia_usuario)

                ''' Pegando a sequencia minima da estratégia cadastrada pelo usuário '''
                sequencia_minima = estrategia[2]
                
                ''' ANTES DE PASSAR NO VALIDADOR, VERIFICAR SE EXISTE O RESULTADO 0 POIS O 0 QUEBRA A SEQUENCIA'''
                if '0' in dicionario_roletas[nome_cassino][:int(sequencia_minima)] or '00' in dicionario_roletas[nome_cassino][:int(sequencia_minima)]:
                    print('Sequencia com resultado 0...Analisando outra estratégia!')
                    print('=' * 150)
                    continue
                
                else:
                    pass

                ''' Verifica se os números da seq minima do historico da roleta está dentro da estratégia '''
                validador = self.validarEstrategiaAlerta(dicionario_roletas, nome_cassino, aposta_externa, sequencia_minima, estrategia)
                
                ''' Validando se bateu alguma condição'''
                if validador.count('true') == int(sequencia_minima)-1:
                    print('IDENTIFICADO PRÉ PADRÃO NA ROLETA ', nome_cassino, ' COM A ESTRATÉGIA ', estrategia)
                    
                    ## ENTRANDO NA ROLETA DO ALERTA
                    browser.get(link_roleta)
                    self.enviar_alerta()#dicionario_roletas, nome_cassino, sequencia_minima, estrategia
                    time.sleep(10)

                    ''' Verifica se a ultima condição bate com a estratégia para enviar sinal Telegram '''

                    ###ACESSANDO IFRAME DA ROLETA
                    self.acessar_iframe('game_iframe','/html/body/div[6]/div[2]/iframe')
                            
                    while True:
                        try:
                            
                            ###PEGANDO NOVOS RESULTADOS
                            historico_roleta_alerta = browser.find_elements_by_xpath('//*[@class="numbers--2435c recent-number--c0a86 desktop--bef02"]')
                            
                            ### FORMATANDO OS RESULTADOS
                            lista_proximo_resultados = self.formatar_resultados_mesa(historico_roleta_alerta[0]) # Formata o historico em lista
                            
                            ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
                            if dicionario_roletas[nome_cassino][:3] != lista_proximo_resultados[:3]:

                                print('Historico_Roleta --> ', nome_cassino, lista_proximo_resultados[:int(sequencia_minima)])

                                ### ALIMENTANDO BANCO DE DADOS ###
                                #nome_cassino,lista_proximo_resultados, dicionario_roletas, 'NULL','NULL')

                                if estrategia[0] == 'repetição' and bot_ativado == True:

                                    ''' Verificando se o ultimo resultado da roleta está dentro da estratégia'''
                                    if lista_proximo_resultados[0] in aposta_externa[estrategia[1]]:
                                        dicionario_roletas[nome_cassino] = lista_proximo_resultados

                                        ######### ELEMENTOS #########
                                        if '/' in estrategia[3]:
                                            aposta_um, aposta_um_clicado, aposta_dois, aposta_dois_clicado = self.elemento_apostas(estrategia)
                                            aposta_protecao = '//*[@class="table-cell--Wz6uJ table-cell_color-green--seXf0"]'
                                            aposta_protecao_clicado = '//*[@class="table-cell--Wz6uJ table-cell_color-green--seXf0 table-cell_hover-highlight--fYheT"]'
                                            ######## INSERINDO APOSTAS #######
                                            time.sleep(5)
                                            self.apostar_duas_casas(valor_entrada, aposta_um, aposta_um_clicado, aposta_dois, aposta_dois_clicado, aposta_protecao, aposta_protecao_clicado)
                                            

                                        else:
                                            aposta_um, aposta_um_clicado = self.elemento_apostas(estrategia)
                                            aposta_protecao = '//*[@class="table-cell--Wz6uJ table-cell_color-green--seXf0"]'
                                            aposta_protecao_clicado = '//*[@class="table-cell--Wz6uJ table-cell_color-green--seXf0 table-cell_hover-highlight--fYheT"]'
                                            ######## INSERINDO APOSTAS #######
                                            time.sleep(5)
                                            self.apostar_uma_casa(valor_entrada, aposta_um, aposta_um_clicado, aposta_protecao, aposta_protecao_clicado)
                                        

                                            if bot_ativado == True:
                                                self.fazer_aposta(valor_entrada)
                                            else:
                                                pass

                                            self.enviar_sinal(lista_proximo_resultados[0])
                                            print('=' * 220)
                                            self.checkSinalEnviado(lista_proximo_resultados, nome_cassino, roleta)
                                            time.sleep(1)
                                            break
                                        

                                    else:
                                        self.apagar_alerta()
                                        print('=' * 220)
                                        dicionario_roletas[nome_cassino] = lista_proximo_resultados
                                        browser.get('https://live.wirebankers.com/frontend/evo/r2/#category=roulette&game=roulette')  
                                        time.sleep(10)
                                        break

                                
                                if estrategia[0] == 'ausência' and bot_ativado == True:
                                    ''' Verificando se o ultimo resultado da roleta não está dentro da estratégia'''
                                    if lista_proximo_resultados[0] not in aposta_externa[estrategia[1]]:
                                        dicionario_roletas[nome_cassino] = lista_proximo_resultados

                                        ######### ELEMENTOS #########
                                        if '/' in estrategia[3]:
                                            aposta_um, aposta_um_clicado, aposta_dois, aposta_dois_clicado = self.elemento_apostas(estrategia)
                                            aposta_protecao = '//*[@class="table-cell--Wz6uJ table-cell_color-green--seXf0"]'
                                            aposta_protecao_clicado = '//*[@class="table-cell--Wz6uJ table-cell_color-green--seXf0 table-cell_hover-highlight--fYheT"]'
                                            time.sleep(5)
                                            self.apostar_duas_casas(valor_entrada, aposta_um, aposta_um_clicado, aposta_dois, aposta_dois_clicado, aposta_protecao, aposta_protecao_clicado)
                                            
                                        else:
                                            aposta_um, aposta_um_clicado = self.elemento_apostas(estrategia)
                                            aposta_protecao = '//*[@class="table-cell--Wz6uJ table-cell_color-green--seXf0"]'
                                            aposta_protecao_clicado = '//*[@class="table-cell--Wz6uJ table-cell_color-green--seXf0 table-cell_hover-highlight--fYheT"]'
                                            ######## INSERINDO APOSTAS #######
                                            time.sleep(5)
                                            self.apostar_uma_casa(valor_entrada, aposta_um, aposta_um_clicado, aposta_protecao, aposta_protecao_clicado)
                                        

                                            self.enviar_sinal(lista_proximo_resultados[0])
                                            print('=' * 220)
                                            self.checkSinalEnviado(lista_proximo_resultados, nome_cassino, roleta)
                                            break
                                    
                                    else:
                                        self.apagar_alerta()
                                        print('=' * 220)
                                        dicionario_roletas[nome_cassino] = lista_proximo_resultados
                                        browser.get('https://live.wirebankers.com/frontend/evo/r2/#category=roulette&game=roulette')  
                                        time.sleep(10)
                                        break
                            
                            else:
                                continue

                        except Exception as b:
                            logger.error('Exception ocorrido no ' + repr(b))
                            self.apagar_alerta()
                            print('=' * 220)
                            dicionario_roletas[nome_cassino] = lista_proximo_resultados
                            browser.get('https://live.wirebankers.com/frontend/evo/r2/#category=roulette&game=roulette')  
                            time.sleep(10)                                    
                            break
                            

                        
        except:
            # VALIDAR SE FOI DESCONECTADO
            if browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[6]/div/div[2]/div[2]/button'):
                browser.refresh()
                self.logarSite()
                pass

            else:
                pass


    def validarEstrategiaAlerta(self, dicionario_roletas, nome_cassino, aposta_externa, sequencia_minima, estrategia):
        validador = []
        for n in range(int(sequencia_minima)-1):

            if estrategia[0] == 'repetição':
                if dicionario_roletas[nome_cassino][n] in aposta_externa[estrategia[1]]:
                    validador.append('true')

            if estrategia[0] == 'ausência':
                if dicionario_roletas[nome_cassino][n] not in aposta_externa[estrategia[1]]:
                    validador.append('true')

        
        return validador


    def checkSinalEnviado(self, lista_proximo_resultados, nome_cassino, roleta):
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
        global win_seguido


        resultados = []
        contador_cash = 0
        while contador_cash <= 2:

            # Validando se foi solicitado o stop do BOT
            if parar != 0:
                break
            else:
                pass

            try:

                # VALIDAR SE FOI DESCONECTADO
                if browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[6]/div/div[2]/div[2]/button') or browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[5]/div/div[2]/div/div[3]/button'):
                    browser.refresh()
                    self.logarSite()
                    continue
                

                ''' Lendo novos resultados para validação da estratégia'''
                lista_resultados_sinal = self.formatar_resultados(roleta) # Formata o historico em lista
                #print(historico_roleta)

                ''' Validando se tem dado Vazio '''
                if '' in lista_resultados_sinal:
                    browser.refresh()
                    self.logarSite()


                ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
                if lista_proximo_resultados[:3] != lista_resultados_sinal[:3]:
                    
                    print(lista_resultados_sinal[0])
                    
                    grupo_apostar = self.apostasExternas(estrategia[3], dic_estrategia_usuario)

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
                            win_seguido+=1

                            with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                                arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}\
                                                \nwin_seguido,{win_seguido}")

                                
                            print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
                            #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)


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
                            win_seguido+=1

                            with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                                arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}\
                                                \nwin_seguido,{win_seguido}")

                            # Preenchendo relatório
                            #placar_win+=1
                            #placar_gale1+=1
                            #resultados_sinais = placar_win + placar_loss
                            print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
                            #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)


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
                            win_seguido+=1

                            with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                                arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}\
                                                \nwin_seguido,{win_seguido}")

                                

                            print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
                            #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)
                          
                                            
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
                        
                        

                        print('==================================================')
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

                        if contador_cash <= 2:

                            time.sleep(5)
                            valor_gale = valor_entrada * fator_gale * contador_cash

                            if '/' in estrategia[3]:
                                self.apostar_duas_casas(valor_gale, aposta_um, aposta_um_clicado, aposta_dois, aposta_dois_clicado, aposta_protecao, aposta_protecao_clicado)
                            else:
                                self.apostar_uma_casa(valor_gale, aposta_um, aposta_um_clicado, aposta_protecao, aposta_protecao_clicado)
                            
                            self.msg_matingale(valor_gale, contador_cash)

                        continue


            except Exception as a:
                logger.error('Exception ocorrido no ' + repr(a))
                #logarSite()
                lista_resultados_sinal, roleta = self.resgatar_historico(nome_cassino)
                continue


        if contador_cash == 3:
            stop_loss.append('loss')

            # Preenchendo arquivo txt
            placar_loss +=1
            placar_geral = placar_win + placar_loss
            win_seguido = 0
            
            with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}\
                                \nwin_seguido,{win_seguido}")

            print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
                
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
            
            ### ALIMENTANDO BANCO DE DADOS ###
            #alimenta_banco_dados(nome_cassino, lista_resultados_sinal, dicionario_roletas, estrategia[1], 'LOSS')
                        
            #print('=' * 100)
            #Enviando Saldo Atualizado
            novo_saldo = self.pegar_saldo()
            self.log(f'SALDO ATUAL {novo_saldo}')
            self.validar_stop_loss()
            print('='*100)
            validador_sinal = 0
            contador_cash = 0
            contador_passagem = 0
            dicionario_roletas[nome_cassino] = lista_resultados_sinal
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


    def apostar_duas_casas(valor_aposta, *args):

        moedas = browser.find_elements_by_xpath('//*[@class="chip-animation-wrapper"]//*[name()="text"]')
        protecao_zero = 2.5 if valor_aposta == 25 else 5


        if valor_aposta == 25:
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


        elif valor_aposta == 75:
            #CLICANDO NAS MOEDAS 50 E 20 E 5
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


        elif valor_aposta == 225:
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


        elif valor_aposta == 50:
            #CLICANDO 1 VEZES NA MOEDA 50
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

            except:pass


        elif valor_aposta == 150:
            #CLICANDO 3 VEZES NA MOEDA 50
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

            except:pass


        elif valor_aposta == 450:
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
        protecao_zero = 2.5 if valor_aposta == 25 else 5


        if valor_aposta == 25:
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


        elif valor_aposta == 75:
            #CLICANDO NAS MOEDAS 20 E 5
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
                #MOEDA 20
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
                        break

                time.sleep(1)
                #CLICANDO NA APOSTA
                try:
                    browser.find_element_by_xpath(aposta_um_clicado).click()
                except:
                    browser.find_element_by_xpath(aposta_um).click()
                

            except:pass


        elif valor_aposta == 225:
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

                time.sleep(1)
                #CLICANDO NA APOSTA
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

                time.sleep(1)
                #CLICANDO NA APOSTA
                try:
                    browser.find_element_by_xpath(aposta_um_clicado).click()
                except:
                    browser.find_element_by_xpath(aposta_um).click()

                time.sleep(0.5)


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


        elif valor_aposta == 50:
            #CLICANDO 1 VEZ
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


        elif valor_aposta == 150:
            #CLICANDO 3 VEZES NA MOEDA 50
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

                time.sleep(0.5)
                try:
                    browser.find_element_by_xpath(aposta_um_clicado).click()
                except:
                    browser.find_element_by_xpath(aposta_um).click()

            except:pass


        elif valor_aposta == 450:
            #CLICANDO 9 VEZES NA MOEDA 50
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

                time.sleep(0.5)
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

        elif protecao_zero == 5:
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
            except:
                pass        

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


    def elemento_apostas(self, estrategia):

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
        

    def msg_matingale(self, valor_gale, contador_cash):

        try:
            self.log(f'EXECUTANDO MATINGALE{contador_cash}')
        except:pass


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
        global estrategias, dic_estrategia_usuario, dicionario_roletas

        dic_estrategia_usuario = {}
        dicionario_roletas = {}

        self.inicio()             # Difinição do webBrowser
        self.logarSite()          # Logando no Site
        placar()                  # Chamando o Placar

        while True:
            if bot_status == 1:
                estrategias = self.cadastrar_estrategias_txt()
                self.coletarResultados()      #Iniciano analises
            























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

    