from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
import logging
from datetime import datetime, timedelta
import warnings
import mysql.connector
from mysql.connector import Error
#from webdriver_manager.firefox import GeckoDriverManager



#_______________________________________________________________________#____________________________________________________________________________________________________

print()
print('                                #################################################################')
print('                                ###########   BOT DADOS FUTEBOL VIRTUAL PLAYPIX   ###############')
print('                                #################################################################')
print('                                ##################### SEJA BEM VINDO ############################')
print('                                #################################################################')
print('                                ############# DESENVOLVIDO POR VICTOR RODRIGUES #################')
print('                                #################################################################\n')
print('Versão = 1.0.0')
print('Ambiente: Produção\n\n\n')

ultimo_resultado = []

    
def auto_refresh():
    global horario_inicio

    horario_atual = datetime.today().strftime('%H:%M')
    tres_hora = timedelta(minutes=30)
    horario_mais_tres = horario_inicio + tres_hora
    horario_refresh = horario_mais_tres.strftime('%H:%M')

    if horario_atual >= horario_refresh:
        print('HORA DE REFRESHAR A PAGINA!!!!')

        logar_site()

        time.sleep(10)
        horario_inicio = datetime.now()


def inicio():
    global logger
    global browser
    global horario_inicio

    horario_inicio = datetime.now()
    logger = logging.getLogger()

    # Definindo opções para o browser
    warnings.filterwarnings("ignore", category=DeprecationWarning) 
    chrome_options = webdriver.ChromeOptions() 
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option('useAutomationExtension', False)
    #chrome_options.add_argument("--incognito") #abrir chrome no modo anônimo
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    #chrome_options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    #chrome_options.add_argument("window-size=1037,547")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_argument('disable-extensions')
    chrome_options.add_argument('disable-popup-blocking')
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('log-level=3')

    
    browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)  # Chrome
    #browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())                                     # FireFox        
    #browser  = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install())                       # Brave
    #browser = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(),chrome_options=chrome_options)                     # Chromium


def logar_site():

    #logger = logging.getLogger()
    browser.get(r"https://www.playpix.com/pt/virtual-sports/betconstruct?game=1")
    try:
        browser.maximize_window()
    except:pass
    
    time.sleep(10)
    
    try:
        browser.find_element_by_xpath('//*[@class="btn a-color s-small cookie-message-button "]').click()
    except:
        pass

    time.sleep(2)

    try:
        
        #acessando IFRAME
        acessarIframe()

        #Clicando nos Ultimos Resultados
        browser.find_element_by_xpath('//*[@class="results-button"]').click()
    
    except:pass
    time.sleep(10)


def acessarIframe():
    t=0
    while t < 10:
        try:
            iframe = iframe = browser.find_element_by_xpath('//*[@class="iframe-full-page virtual-sports"]')
            browser.switch_to.frame(iframe)
            break
        
        except:
            time.sleep(5)
            t+=1


def coletar_dados():
    global ultimo_resultado

    while True:

        while True:
            try:
                # Auto Refresh
                auto_refresh()

                # Pegando o histórico de resultados
                lista_jogos = browser.find_elements_by_xpath('//*[@class="game-result-items"]')

                #VALIDANDO SE A LISTA ESTA VAZIA
                if lista_jogos == []:
                    print('Lista de Jogos Vazia. Reiniciando....')
                    logar_site()
                    continue

                #Correção de Bug
                if '49:46' in lista_jogos[0].text: 
                    
                    #Fechando Janela
                    browser.find_element_by_xpath('//*[@class="pop-up-close"]').click()
                    #clicando no botão resultados
                    browser.find_element_by_xpath('//*[@class="results-button"]').click()

                    time.sleep(5)

                    continue

                novo_resultado = lista_jogos[0].text

                if ultimo_resultado != novo_resultado:
                    #Formatando dados do ultimo jogo
                    try:

                        data_game = lista_jogos[0].text.split(',')[0]
                        hora_game = lista_jogos[0].text.split(',')[1].split('\n')[0].replace(' ','')
                        time_1 = lista_jogos[0].text.split(',')[1].split('\n')[1].split(' - ')[0]
                        time_2 = lista_jogos[0].text.split(',')[1].split('\n')[1].split(' - ')[1]
                        placar = lista_jogos[0].text.split('\n')[-1]

                    except:
                        print('Erro ao inserir resultados na Lista... Refreshando...')
                        logar_site()
                        continue
                
                    
                    print(datetime.now().strftime('%H:%M'))
                    print(f'{data_game} | {hora_game} | {time_1} | {time_2} | {placar}')
                    #Chama função para enviar dados para o banco
                    enviar_dados_banco(data_game, hora_game, time_1, time_2, placar)

                    print('=' * 100)

                    ultimo_resultado = novo_resultado


                #Fechando Janela
                browser.find_element_by_xpath('//*[@class="pop-up-close"]').click()
                #clicando no botão resultados
                browser.find_element_by_xpath('//*[@class="results-button"]').click()

                time.sleep(5)

                break

                ''' Exceção se o jogo não estiver disponível '''
            except Exception as e:
                print(f'Algo deu errado -- {e}.. Reiniciando...')
                logar_site()


def enviar_dados_banco(data_game, hora_game, time_1, time_2, placar):
    #banco de dados
    HOST = '162.240.147.7'
    USER = 'easycoanalytics_storage'
    PASS = ',jr2BCU}E7n]7VB?HR'
    DB =  'easycoanalytics_storage'
    TABELA = 'results_virtual_futebol'

    try:
        #CONECTANDO COM O BANCO '''
        db_conexao = mysql.connector.connect(host=HOST, database=DB, user=USER, password=PASS)

        #Variavel que executa as querys
        cursor = db_conexao.cursor()

        ''' QUERY '''
        query_inserir_dados = (f"""INSERT INTO {TABELA} 
                                VALUES(NULL, '{data_game}', '{hora_game}', '{time_1}', '{time_2}', '{placar}')""")

        cursor.execute(query_inserir_dados)
        db_conexao.commit()

    except Exception as g:
        logger.error('Exception ocorrido na conexão com o banco MYSQL: ' + repr(g))
        pass



if __name__ == '__main__':

    while True:
        try:

            print('\n\nPREPARANDO O AMBIENTE....')

            inicio()
            logar_site()

            print('\n\nINICIANDO COLETA DOS DADOS......')

            coletar_dados()

        except Exception as e:
            print(f'Erro inesperado -- {e} -- Reiniciando em 30 segundos.....')
            time.sleep(30)