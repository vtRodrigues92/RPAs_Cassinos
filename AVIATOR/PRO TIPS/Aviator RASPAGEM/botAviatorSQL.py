from selenium import webdriver
import time
import warnings
from webdriver_manager.chrome import ChromeDriverManager
import logging
from datetime import datetime,timedelta
from selenium.webdriver.support.color import Color
import pandas as pd
from telegram.ext import * 
import mysql.connector
from mysql.connector import Error



def auto_refresh():
    global horario_inicio

    horario_atual = datetime.today().strftime('%H:%M')
    tres_hora = timedelta(hours=1)
    horario_mais_tres = horario_inicio + tres_hora
    horario_refresh = horario_mais_tres.strftime('%H:%M')

    if horario_atual >= horario_refresh:
        login()
        horario_inicio = datetime.now()





def inicio():
    global browser
    global df
    global logger
    global roxo
    global azul
    global rosa
    global horario_inicio

    horario_inicio = datetime.now()

    logger = logging.getLogger()

    # CORES
    roxo = '#6b07d2'
    azul = '#005d91'
    rosa =  '#900087'

    # DATA FRAME
    df = pd.DataFrame(columns = ['data','horario','hora','minuto','vela','cor','capturado' ])


    # Definindo opções para o browser
    warnings.filterwarnings("ignore", category=DeprecationWarning) 
    chrome_options = webdriver.ChromeOptions() 
    #chrome_options.add_argument("--disable-gpu")
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


    browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)   
    print('\n\n')





def login():

    #Dubai3
    #Vb920115

    #logger = logging.getLogger()
    browser.get(r"https://m.esportesdasorte.com/ptb/games/casino/detail/normal/7787")
    time.sleep(10)
    try:
        ''' CLICANDO NO RATIO BUTTON EMAIL '''
        #browser.find_element_by_xpath('//*[@id="allCnt"]/main/app-authentication/app-signin/div/form/div[2]/div[2]/div[2]/label').click() 
        time.sleep(1)
        ''' INSERINDO LOGIN E SENHA'''
        browser.find_element_by_id('username').send_keys('Dubai3')
        browser.find_element_by_id('password').send_keys('Vb920115')
        ''' CLICANDO EM ENTRAR '''
        browser.find_element_by_xpath('//*[@id="allCnt"]/main/app-authentication/app-signin/div/form/button').click()
        time.sleep(10)
    
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
    vela_repetida = 0
    validador = 0
    

    while True:
        try:

            # Tentar pegaro xpath da vela. Se não conseguir, entrar na pagina novamente e tentar pegar p xpath da vela
            while True:
                try:
                    vela_atual = browser.find_element_by_xpath('/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]/div/app-payout-item[1]/div').text
                    str_cor =  Color.from_string(browser.find_element_by_xpath('/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]/div/app-payout-item[1]/div').value_of_css_property('background-color')).hex
                    break

                except:
                    login()
                    

            # Funcionalidade que valida se está capturando a mesma vela.
            if vela_anterior != vela_atual or vela_anterior == 0:
                vela_repetida = 0
                pass

            elif browser.find_element_by_xpath('/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]/div/app-payout-item[1]/div').text == browser.find_element_by_xpath('/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]/div/app-payout-item[2]/div').text and vela_repetida == 0:
                if validador < 3:
                    time.sleep(1)
                    print('entrei aqui pq acho que o valor é repetido.. Validando: ', validador)
                    validador += 1
                    continue
                else:
                    print('MESMO RESULTADO DUAS VEZES NESSE MOMENTO')
                    vela_repetida +=1
                    validador = 0
                    pass
            
            else:
                continue


            # Pegando campos para registrar no banco de dados
            if str_cor == roxo:
                cor = 'roxo'
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
                

            if str_cor == azul:
                cor = 'azul'
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
                
                

            if str_cor == rosa:
                cor = 'rosa'
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
            validador = 0
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


    query_inserir_dados = (f"""INSERT INTO u253295982_dbaviator.aviator_mosaico 
                                                                VALUES( null, '{data_atual}', '{horario_atual}','{hora}', '{minuto}','{vela_atual}', '{cor}', '1')""")

    cursor.execute(query_inserir_dados)
    db_conexao.commit()



inicio()
login()
print('############################################# INICIANDO COLETA DOS DADOS #############################################')
print()
raspagem()












