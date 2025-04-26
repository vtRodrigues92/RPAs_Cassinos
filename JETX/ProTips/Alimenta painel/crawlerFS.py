# -*- coding: utf-8 -*-
from selenium import webdriver
import time
import warnings
from webdriver_manager.chrome import ChromeDriverManager
import logging
from datetime import datetime, timedelta
from selenium.webdriver.support.color import Color
import pandas as pd
from telegram.ext import * 
import mysql.connector
from mysql.connector import Error


print()
print('                                #################################################################')
print('                                ############   BOT ALIMENTA SQL FOOTBALSTUDIO   #################')
print('                                #################################################################')
print('                                ##################### SEJA BEM VINDO ############################')
print('                                #################################################################')
print('                                ############# DESENVOLVIDO POR VICTOR RODRIGUES #################')
print('                                #################################################################\n')
print('Versão = 1.0.0')
print('Ambiente: Produção\n\n\n')

#protips33
#Vb920115@




def auto_refresh():
    global horario_inicio

    horario_atual = datetime.today().strftime('%H:%M')
    dez_minutos = timedelta(minutes=10)
    horario_mais_dez = horario_inicio + dez_minutos
    horario_refresh = horario_mais_dez.strftime('%H:%M')

    if horario_atual >= horario_refresh:
        logarSite()
        horario_inicio = datetime.now()






def inicio():
    global browser
    global logger
    global horario_inicio

    horario_inicio = datetime.now()

    logger = logging.getLogger()

    # Definindo opções para o browser
    warnings.filterwarnings("ignore", category=DeprecationWarning) 
    chrome_options = webdriver.ChromeOptions() 
    #chrome_options.add_argument("--disable-gpu")
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
    browser.get(r"https://pi.njoybingo.com/game.do?token=3fc5c8c1-d620-4ac5-ad61-6a5285b78e93&pn=meskbet&lang=pt&game=EVOLUTION-topcard-nvrpqglt6teqkvaf&type=CHARGED")
    browser.maximize_window()
    time.sleep(10)





def validarJogoPausado():
    try:
        if browser.find_elements_by_xpath('//*[@id="root"]/div/div[2]/div/div/div[10]/div[1]'):
            browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div').click()
    
    except:
        pass





# CAMPOS DE DATA
def campos():
    global data_atual
    global horario_atual
    global hora
    global minuto
    global capturado

    data_atual = datetime.today().strftime('%Y-%m-%d')
    horario_atual = datetime.today().strftime('%H:%M:%S')
    hora = horario_atual[0:2]
    minuto = horario_atual[3:5]
    capturado = 1
    return data_atual, horario_atual, hora, minuto, capturado






def criar_lista(resultados):
    while True:
        try:
            lista = []
            for resultado in resultados:    
                lista.append(resultado.text)

            return lista
            
        except:
            resultados = browser.find_elements_by_css_selector('.historyItem--a1907')
            continue





def coletarDados():
    global resultado
    global cor
    global df
    global browser
    global lista_resultados_anterior
    global lista_resultados_atual

    lista_resultados_anterior = 0

    while True:
        try:
            # Jogo Pausado
            validarJogoPausado()
            # auto refresh
            auto_refresh()


            # Tentar pegar a tabela de resultados, acionar a função que converte a tabela em lista
            if browser.find_elements_by_css_selector('.historyItem--a1907'):
                resultados = browser.find_elements_by_css_selector('.historyItem--a1907')
                ''' Função que converte as letras em cores '''
                lista_resultados_atual = criar_lista(resultados)

            # Funcionalidade que valida se está capturando o mesmo resultado
            if lista_resultados_atual != lista_resultados_anterior or lista_resultados_anterior == 0:
                
                resultado = lista_resultados_atual[0]
                campo = campos()
                alimentaBanco()

                print(campo[0], campo[1], lista_resultados_atual[0], "azul" if resultado == "V" else "vermelho" if resultado == "C" else "amarelo")
                #df.to_excel('aviator_banco_dados.xlsx', index=None)

                lista_resultados_anterior = lista_resultados_atual
                time.sleep(3)

        except:
            continue






# ALIMENTANDO O BANCO
def alimentaBanco():
    global resultado_atual


    try:
        
        db_conexao = mysql.connector.connect(host='sql728.main-hosting.eu', database='u253295982_dbaviator', user='u253295982_aviator', password='Aviator22')

    except Exception as g:

        logger.error('Exception ocorrido na conexão com o banco MYSQL: ' + repr(g))


    #Variavel que executa as querys
    cursor = db_conexao.cursor()


    query_inserir_dados = (f"""INSERT INTO u253295982_dbaviator.footballStudio_mosaico 
                                                                VALUES(NULL, '{data_atual}', '{horario_atual}','{hora}', '{minuto}','{resultado}', '1', '{"azul" if resultado == "V" else "vermelho" if resultado == "C" else "amarelo"}')""")

    cursor.execute(query_inserir_dados)
    db_conexao.commit()




inicio()
logarSite()
print('\n\n')
print('######################################## INICIANDO O REGISTRO DOS DADOS ########################################')
coletarDados()