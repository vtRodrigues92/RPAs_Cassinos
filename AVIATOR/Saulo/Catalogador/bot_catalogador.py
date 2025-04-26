from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
import logging
from datetime import datetime, timedelta
#from telegram.ext import *
from telebot import *
import warnings, pytz, json
from lxml import etree
#import undetected_chromedriver as uc


#_______________________________________________________________________#____________________________________________________________________________________________________


#----------------------------------------------------------------------------------#
################################## CONFIGURE AQUI ##################################

#html_dir = "C:\Apache\Apache24\htdocs\aviator" #caminho padrão vps Windows
html_dir = "index.html" #caminho local
base = 10000 #quantidade de velas armazenar

####################################################################################
#----------------------------------------------------------------------------------#


def get_time():
    fuso_horario = pytz.timezone('America/Sao_Paulo')
    data_hora_atual = datetime.now(fuso_horario)
    hora = data_hora_atual.strftime('%H')
    minuto = data_hora_atual.strftime('%M')
    return f"{hora}:{minuto}"


def get_data():
    fuso_horario = pytz.timezone('America/Sao_Paulo')
    data_hora_atual = datetime.now(fuso_horario)
    dia = data_hora_atual.strftime('%d')
    mes = data_hora_atual.strftime('%m')
    hora = data_hora_atual.strftime('%H')
    minuto = data_hora_atual.strftime('%M')
    return f"{dia}/{mes} - {hora}:{minuto}"


def clear():
    global html
    while True:
        try:
            with open("results.json", "w") as file_results:
                json.dump([], file_results, indent=4)

            with open(html_dir, 'r') as file:
                html = file.read()
            root = etree.HTML(html)
            results_div = root.find('.//div[@id="results"]')
            num_filhos = len(results_div)
            if num_filhos > 0:            
                for div in results_div:
                    results_div.remove(div)
                now_date = get_data()
                filhos_div = root.find('.//div[@id="contador"]')
                filhos_div.text = f'0 velas capturadas de {start_date} a {now_date}'
                filhos_div = root.find('.//div[@id="ctgUP0"]')
                filhos_div.text = f'0'
                filhos_div = root.find('.//div[@id="ctgUP1-5"]')
                filhos_div.text = f'0'
                filhos_div = root.find('.//div[@id="ctgUP2"]')
                filhos_div.text = f'0'
                filhos_div = root.find('.//div[@id="ctgUP5"]')
                filhos_div.text = f'0'
                filhos_div = root.find('.//div[@id="ctgUP10"]')
                filhos_div.text = f'0'
                filhos_div = root.find('.//div[@id="ctgUP20"]')
                filhos_div.text = f'0'
                filhos_div = root.find('.//div[@id="maxUP0"]')
                filhos_div.text = f'0'
                filhos_div = root.find('.//div[@id="maxUP1-5"]')
                filhos_div.text = f'0'
                filhos_div = root.find('.//div[@id="maxUP2"]')
                filhos_div.text = f'0'
                filhos_div = root.find('.//div[@id="maxUP5"]')
                filhos_div.text = f'0'
                filhos_div = root.find('.//div[@id="maxUP10"]')
                filhos_div.text = f'0'
                filhos_div = root.find('.//div[@id="maxUP20"]')
                filhos_div.text = f'0'
                filhos_div = root.find('.//div[@id="maxUP50"]')
                filhos_div.text = f'0'
                filhos_div = root.find('.//div[@id="maxUP100"]')
                filhos_div.text = f'0'

                intervalo_div = root.find('.//div[@id="sub-containerUP0"]')
                intervalo_div.text = f'-'
                intervalo_div = root.find('.//div[@id="sub-containerUP1-5"]')
                intervalo_div.text = f'-'
                intervalo_div = root.find('.//div[@id="sub-containerUP2"]')
                intervalo_div.text = f'-'
                intervalo_div = root.find('.//div[@id="sub-containerUP5"]')
                intervalo_div.text = f'-'
                intervalo_div = root.find('.//div[@id="sub-containerUP10"]')
                intervalo_div.text = f'-'
                intervalo_div = root.find('.//div[@id="sub-containerUP20"]')
                intervalo_div.text = f'-'
                intervalo_div = root.find('.//div[@id="sub-containerUP50"]')
                intervalo_div.text = f'-'
                intervalo_div = root.find('.//div[@id="sub-containerUP100"]')
                intervalo_div.text = f'-'

                html_atualizado = etree.tostring(root, pretty_print=True, encoding='unicode')
                with open(html_dir, 'w') as file:
                    file.write(html_atualizado)
                return
            else:
                return
        except Exception as e:
            print(f"Erro: {e}")
            pass


def calc_intervalo_maximo(sequencia):
    intervalos_maximos = {}
    last_occurrence = {}
    for idx, classe in enumerate(sequencia):
        if classe in last_occurrence:
            interval = idx - last_occurrence[classe]
            if classe not in intervalos_maximos or interval > intervalos_maximos[classe]:
                intervalos_maximos[classe] = interval       
        last_occurrence[classe] = idx
    return intervalos_maximos


def update(num, hora):
    global html, start_date, ctgUP0, ctgUP1_5, ctgUP2, ctgUP5, ctgUP10, ctgUP20, ctgUP50, ctgUP100, maxUP0, maxUP1_5, maxUP2, maxUP5, maxUP10, maxUP20, maxUP50, maxUP100, ant, seq, base, seq_cor
    while True:
        try:
            with open(html_dir, 'r') as file:
                html = file.read()
            root = etree.HTML(html)
            results_div = root.find('.//div[@id="results"]')
            num_filhos = len(results_div)
            if num_filhos >= base:
                ultimo_filho = results_div[-1]
                results_div.remove(ultimo_filho)
            if num >= 100:
                classe = "sub-containerUP100"
                ctgUP100 += 1
                if classe == ant:
                    seq += 1
                    if seq > maxUP100:
                        maxUP100 = seq
                else:
                    ant = classe
                    seq = 1
            elif 50 <= num < 100:
                classe = "sub-containerUP50"
                ctgUP50 += 1
                if classe == ant:
                    seq += 1
                    if seq > maxUP50:
                        maxUP50 = seq
                else:
                    ant = classe
                    seq = 1
            elif 20 <= num < 50:
                classe = "sub-containerUP20"
                ctgUP20 += 1
                if classe == ant:
                    seq += 1
                    if seq > maxUP20:
                        maxUP20 = seq
                else:
                    ant = classe
                    seq = 1
            elif 10 <= num < 20:
                classe = "sub-containerUP10"
                ctgUP10 += 1
                if classe == ant:
                    seq += 1
                    if seq > maxUP10:
                        maxUP10 = seq
                else:
                    ant = classe
                    seq = 1
            elif 5 <= num < 10:
                classe = "sub-containerUP5"
                ctgUP5 += 1
                if classe == ant:
                    seq += 1
                    if seq > maxUP5:
                        maxUP5 = seq
                else:
                    ant = classe
                    seq = 1
            elif 2 <= num < 5:
                classe = "sub-containerUP2"
                ctgUP2 += 1
                if classe == ant:
                    seq += 1
                    if seq > maxUP2:
                        maxUP2 = seq
                else:
                    ant = classe
                    seq = 1
            elif 1.5 <= num < 2:
                classe = "sub-containerUP1-5"
                ctgUP1_5 += 1
                if classe == ant:
                    seq += 1
                    if seq > maxUP1_5:
                        maxUP1_5 = seq
                else:
                    ant = classe
                    seq = 1
            elif num < 1.5:
                classe = "sub-containerUP0"
                ctgUP0 += 1
                if classe == ant:
                    seq += 1
                    if seq > maxUP0:
                        maxUP0 = seq
                else:
                    ant = classe
                    seq = 1

            seq_cor.append(classe)
            resultados = calc_intervalo_maximo(seq_cor)
            for cla, intervalo_maximo in resultados.items():
                print(f"Classe {cla}: Intervalo máximo = {intervalo_maximo}")
                filhos_div = root.find(f'.//div[@id="{cla}"]')
                filhos_div.text = f'{intervalo_maximo}'
                    
            new_div = etree.Element('div', attrib={'class': classe})
            new_div_num = etree.Element('div', attrib={'class': 'vela'})
            new_div_num.text = f'{num}'
            new_div_hora = etree.Element('div', attrib={'class': 'hora'})
            new_div_hora.text = f'{hora}'
            new_div.append(new_div_num)
            new_div.append(new_div_hora)
            results_div.insert(0, new_div)
            num_filhos = len(results_div)
            print(f"\nVELAS CAPTURADAS: {num_filhos}")
            now_date = get_data()
            filhos_div = root.find('.//div[@id="contador"]')
            filhos_div.text = f'{num_filhos} velas capturadas de {start_date} a {now_date}'
            filhos_div = root.find('.//div[@id="ctgUP0"]')
            filhos_div.text = f'{ctgUP0}'
            filhos_div = root.find('.//div[@id="ctgUP1-5"]')
            filhos_div.text = f'{ctgUP1_5}'
            filhos_div = root.find('.//div[@id="ctgUP2"]')
            filhos_div.text = f'{ctgUP2}'
            filhos_div = root.find('.//div[@id="ctgUP5"]')
            filhos_div.text = f'{ctgUP5}'
            filhos_div = root.find('.//div[@id="ctgUP10"]')
            filhos_div.text = f'{ctgUP10}'
            filhos_div = root.find('.//div[@id="ctgUP20"]')
            filhos_div.text = f'{ctgUP20}'
            filhos_div = root.find('.//div[@id="ctgUP50"]')
            filhos_div.text = f'{ctgUP50}'
            filhos_div = root.find('.//div[@id="ctgUP100"]')
            filhos_div.text = f'{ctgUP100}'
            filhos_div = root.find('.//div[@id="maxUP0"]')
            filhos_div.text = f'{maxUP0}'
            filhos_div = root.find('.//div[@id="maxUP1-5"]')
            filhos_div.text = f'{maxUP1_5}'
            filhos_div = root.find('.//div[@id="maxUP2"]')
            filhos_div.text = f'{maxUP2}'
            filhos_div = root.find('.//div[@id="maxUP5"]')
            filhos_div.text = f'{maxUP5}'
            filhos_div = root.find('.//div[@id="maxUP10"]')
            filhos_div.text = f'{maxUP10}'
            filhos_div = root.find('.//div[@id="maxUP20"]')
            filhos_div.text = f'{maxUP20}'
            filhos_div = root.find('.//div[@id="maxUP50"]')
            filhos_div.text = f'{maxUP50}'
            filhos_div = root.find('.//div[@id="maxUP100"]')
            filhos_div.text = f'{maxUP100}'
            html_atualizado = etree.tostring(root, pretty_print=True, encoding='unicode')
            with open(html_dir, 'w') as file:
                file.write(html_atualizado)
            return
        except Exception as e:
            print(f"Erro: {e}")
            pass


def auto_refresh():
    global horario_inicio

    horario_atual = datetime.today().strftime('%H:%M')
    tres_hora = timedelta(hours=1)
    horario_mais_tres = horario_inicio + tres_hora
    horario_refresh = horario_mais_tres.strftime('%H:%M')

    if horario_atual >= horario_refresh:
        print('HORA DE REFRESHAR A PAGINA!!!!')
        logar_site()
        time.sleep(10)
        horario_inicio = datetime.now()


def inicio():
    global browser
    global lista_anterior

    logger = logging.getLogger()
    lista_anterior = []

    # Definindo opções para o browser
    warnings.filterwarnings("ignore", category=DeprecationWarning) 
    chrome_options = webdriver.ChromeOptions() 
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument("--disable-gpu")
    #chrome_options.add_experimental_option('useAutomationExtension', False)
    #chrome_options.add_argument("--incognito") #abrir chrome no modo anônimo
    #chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    #chrome_options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    #chrome_options.add_argument("window-size=1037,547")
    #chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    #chrome_options.add_argument('disable-extensions')
    #chrome_options.add_argument('disable-popup-blocking')
    #chrome_options.add_argument('disable-infobars')
    #chrome_options.add_argument('--disable-dev-shm-usage')
    #chrome_options.add_argument('log-level=3')
    #chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36')
        

    browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options) # Chrome
    #browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())                                     # FireFox        
    #browser  = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install())                        # Brave
    #browser = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(),chrome_options=chrome_options)                     # Chromium


def logar_site():

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
        txt = open("credenciais.txt", "r", encoding="utf-8").read()
        usuario = txt.split(',')[0] 
        senha = txt.split(',')[1]

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

        #IFRAME AVIATOR
        #tela_cheia = browser.find_element_by_xpath('//*[@id="game_wrapper"]/iframe').get_attribute('src')
        c=1
        while c < 10:

            try:
                iframe = browser.find_element_by_xpath('//*[@id="game_wrapper"]/iframe')
                browser.switch_to_frame(iframe)
                break
            except:
                c+=1
                time.sleep(1)
                pass
            
        #browser.get(tela_cheia)
        #time.sleep(15)

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
        
        #MINIMIZANDO A TELA
        try:
            browser.minimize_window()
        except:
            pass

    except:
        pass                                        


def coletar_dados():
    global lista_anterior

    while True:
        try:
            # Auto Refresh
            #auto_refresh()

            lista_resultados = []
            # Pegando o histórico de resultados
            historico_velas = browser.find_elements_by_xpath('//*[@class="payout ng-star-inserted"]')
            
            ''' Inserindo velas na lista'''
            try:
                for vela in reversed(historico_velas[:5]):
                    numero = vela.text.replace('x','')
                    lista_resultados.append(numero)
            except:
                time.sleep(1)
                continue
            
            ''' VALIDANDO SE A LISTA ESTA VAZIA'''
            if lista_resultados == []:
                logar_site()
                continue
            

            if lista_anterior != lista_resultados:
            
                print(f"\nNovo Resultado:\n{lista_resultados[-1]},{result_old}")
                
                finishedAt = get_time()
                
                #ATUALIZANDO INDEX.HTML
                update(float(lista_resultados[-1]), finishedAt)

                #ATUALIZANDO O JSON
                dict_storage = {
                    "crash_point":lista_resultados[-1],
                    "finishedAt":finishedAt
                }
                try:
                    #LENDO JSON
                    with open("results.json", "r") as file_results:
                        cont_file_results = json.load(file_results)
                    cont_file_results.insert(0, dict_storage)

                    #ESCREVENDO NO JSON
                    with open("results.json", "w") as file_results:
                        json.dump(cont_file_results, file_results, indent=4)

                except:
                    with open("results.json", "w") as file_results:
                        json.dump([dict_storage], file_results, indent=4)

                print('=' * 100)
                lista_anterior = lista_resultados

                time.sleep(1)
            
            
            else:
                continue
        
            
            ''' Exceção se o jogo não estiver disponível '''
        except:
            print('Algo deu errado na funcao Coletar Dados..Refreshando...')
            logar_site()







if __name__ == '__main__':

    print()
    print('                                #################################################################')
    print('                                ################# BOT AVIATOR CATALOGADOR #######################')
    print('                                #################################################################')
    print('                                ##################### SEJA BEM VINDO ############################')
    print('                                #################################################################')
    print('                                ############# DESENVOLVIDO POR VICTOR RODRIGUES #################')
    print('                                #################################################################\n')
    print('Versão = 1.0.0')
    print('Ambiente: Produção\n\n\n')

    driver = None
    url_with_auth = None
    token = None
    token_cassino = None
    user_id = None
    user_name = None
    user_type = None
    user_cookie = None
    result_old = 0
    result_new = None
    start = True
    ctgUP0 = 0
    ctgUP1_5 = 0
    ctgUP2 = 0
    ctgUP5 = 0
    ctgUP10 = 0
    ctgUP20 = 0
    ctgUP50 = 0
    ctgUP100 = 0
    maxUP0 = 0
    maxUP1_5 = 0
    maxUP2 = 0
    maxUP5 = 0
    maxUP10 = 0
    maxUP20 = 0
    maxUP50 = 0
    maxUP100 = 0
    seq = 0
    ant = None
    seq_cor = []
    storage = []

    start_date = get_data()
    
    if start:
        clear()
        start = False



    inicio()            # Difinição do webBrowser
    logar_site()         # Logando no Site
    coletar_dados()
