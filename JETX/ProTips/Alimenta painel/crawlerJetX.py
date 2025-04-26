from selenium import webdriver
import time
import warnings
from webdriver_manager.chrome import ChromeDriverManager
import logging
from datetime import datetime
from selenium.webdriver.support.color import Color
import pandas as pd
from telegram.ext import * 
import mysql.connector
from mysql.connector import Error
from selenium.webdriver.firefox.options import *



#Definindo opções para o browser
warnings.filterwarnings("ignore", category=DeprecationWarning) 
chrome_options = webdriver.ChromeOptions() 
chrome_options.add_argument("--disable-gpu")
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_experimental_option('useAutomationExtension', False)
#chrome_options.add_argument("--incognito") #abrir chrome no modo anônimo
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
#chrome_options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

# Opção para executar o prgrama em primeiro ou segundo plano
escolha = int(input('Deseja que o programa seja executado em primeiro[1] ou segundo[2] plano? --> '))
print()
time.sleep(1)

if escolha == 1:
    print('O programa será executado em primeiro plano.\n')
else:
    print('O programa será executado em segundo plano.\n')
    chrome_options.add_argument("--headless")



time.sleep(1)
print()
print('O Programa está sendo iniciado......')

browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
print('\n\n')

#logger = logging.getLogger()
browser.get(r"https://eu-server.ssgportal.com/GameLauncher/Loader.aspx?GameCategory=JetX&GameName=JetX&ReturnUrl&Token=2355b71c-eecb-4063-96ed-35ea73a63c0e&PortalName=meskbet")
browser.maximize_window()
time.sleep(10)


print('######################### INICIANDO COLETA DOS DADOS #########################')
print()

logger = logging.getLogger()


# CORES
cinza = '#ff2f2f'
verde = '#4ec520'

# DATA FRAME
df = pd.DataFrame(columns = ['data','horario','hora','minuto','vela','cor','capturado' ])


# CAMPOS DE DATA
def campos():
    global data_atual
    global horario_atual
    global hora
    global minuto
    global capturado

    data_atual = datetime.today().strftime('%Y-%m-%d')
    horario_atual = datetime.today().strftime('%H:%M')
    hora = horario_atual[0:2]
    minuto = horario_atual[3:]
    capturado = 1
    return data_atual, horario_atual, hora, minuto, capturado


# RASPAGEM DOS DADOS
def raspagem():
    global vela
    global cor
    global df
    global browser
    global vela_anterior
    global vela_atual

    vela_anterior = 0
    
    # acessando o iframe do jogo
    iframe = browser.find_element_by_id('game-frame')
    browser.switch_to.frame(iframe)

    while True:
        try:

            if browser.find_elements_by_class_name('game-started') == []:
                time.sleep(1)
                
                # Tentar pegaro xpath da vela. Se não conseguir, entrar na pagina novamente e tentar pegar p xpath da vela
                while True:
                    try:
                        vela_atual = browser.find_element_by_xpath('//*[@id="last100Spins"]/div[1]').text
                        str_cor = Color.from_string(browser.find_element_by_xpath('//*[@id="last100Spins"]/div[1]').value_of_css_property('color')).hex
                        break
                    except:
                        if browser.current_url == 'https://eu-server.ssgportal.com/GameLauncher/Loader.aspx?GameCategory=JetX&GameName=JetX&ReturnUrl&Token=2355b71c-eecb-4063-96ed-35ea73a63c0e&PortalName=meskbet':
                            pass
                        else:
                            browser.get(r"https://eu-server.ssgportal.com/GameLauncher/Loader.aspx?GameCategory=JetX&GameName=JetX&ReturnUrl&Token=2355b71c-eecb-4063-96ed-35ea73a63c0e&PortalName=meskbet")
                            time.sleep(15)
                            # acessando o iframe do jogo
                            iframe = browser.find_element_by_id('game-frame')
                            browser.switch_to.frame(iframe)


                # Funcionalidade que valida se está capturando a mesma vela.
                if vela_anterior != vela_atual or vela_anterior == 0:
                    pass

                elif browser.find_element_by_xpath(f'//*[@id="last100Spins"]/div[1]').text == browser.find_element_by_xpath(f'//*[@id="last100Spins"]/div[2]').text:
                    time.sleep(6)
                    pass
                
                else:
                    continue

                # Definindo cor de acordo com a vela
                if float(vela_atual) < 2:
                    cor = 'cinza'
                    campo = campos()
                    df=df.append({'data':campo[0],
                               'horario':campo[1],
                               'hora':campo[2],
                               'minuto':campo[3],
                               'vela':vela_atual,
                               'cor':cor,
                               'capturado':campo[4]},
                                ignore_index=True)

                    alimentaBanco()
                    
                    

                if float(vela_atual) >=2:
                    cor = 'verde'
                    campo = campos()
                    df=df.append({'data':campo[0],
                               'horario':campo[1],
                               'hora':campo[2],
                               'minuto':campo[3],
                               'vela':vela_atual,
                               'cor':cor,
                               'capturado':campo[4]},
                                ignore_index=True)

                    alimentaBanco()


                print(campo[0], campo[1], vela_atual, cor)
                #df.to_excel('aviator_banco_dados.xlsx', index=None)

                
                    
                vela_anterior = vela_atual
                time.sleep(5)
        except:
            continue



# ALIMENTANDO O BANCO
def alimentaBanco():

    global vela_atual


    try:
        
        db_conexao = mysql.connector.connect(host='sql728.main-hosting.eu', database='u253295982_dbaviator', user='u253295982_aviator', password='Aviator22')

    except Exception as g:

        logger.error('Exception ocorrido na conexão com o banco MYSQL: ' + repr(g))


    #Variavel que executa as querys
    cursor = db_conexao.cursor()


    query_inserir_dados = (f"""INSERT INTO u253295982_dbaviator.jetx_mosaico 
                                                                VALUES(NULL, '{data_atual}', '{horario_atual}','{hora}', '{minuto}','{vela_atual}', '{cor}', '1')""")

    cursor.execute(query_inserir_dados)
    db_conexao.commit()


raspagem()












