from selenium import webdriver
import time
import warnings
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import logging
import threading
import mysql.connector
from mysql.connector import Error


print()
print('                                #################################################################')
print('                                ##############  ROLETAS PLAYPIX ENVIO BANCO   ###################')
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
class enviarDadosBanco(threading.Thread):
    
    def __init__(self, data, hora, nome_fornecedor, nome_cassino, ultimo_resultado, cor):
        self.data = data
        self.hora = hora
        self.nome_fornecedor = nome_fornecedor
        self.nome_cassino = nome_cassino
        self.ultimo_resultado = ultimo_resultado
        self.cor = cor
        threading.Thread.__init__(self)
    
    def run(self):
        #banco de dados
        HOST = '162.240.147.7'
        USER = 'easycoanalytics_storage'
        PASS = ',jr2BCU}E7n]7VB?HR'
        DB =  'easycoanalytics_storage'
        TABELA = 'results_lobby_creedroomz'

        horario_inicial = datetime.now()

        try:
            #CONECTANDO COM O BANCO '''
            db_conexao = mysql.connector.connect(host=HOST, database=DB, user=USER, password=PASS)

            #Variavel que executa as querys
            cursor = db_conexao.cursor()

            ''' QUERY '''
            query_inserir_dados = (f"""INSERT INTO {TABELA} 
                                   VALUES(NULL, '{self.data}', 
                                                '{self.hora}', 
                                                '{self.nome_fornecedor}', 
                                                '{self.nome_cassino}', 
                                                '{self.ultimo_resultado}', 
                                                '{self.cor}')""")

            cursor.execute(query_inserir_dados)
            db_conexao.commit()

        except Exception as g:
            logger.error('Exception ocorrido na conexão com o banco MYSQL: ' + repr(g))
            pass
        
        print(datetime.now().strftime('%H:%M'))
        print(f'{self.data} | {self.hora} | {self.nome_fornecedor} | {self.nome_cassino} | {self.ultimo_resultado} | {self.cor} -- Registrado no banco com sucesso.')
        print('VELOCIDADE DE REGISTRO NO BANCO ---> ', datetime.now() - horario_inicial)
        print('=' * 100)



def auto_refresh():
    global horario_inicio

    data_atual = datetime.now().date().strftime('%d/%m/%Y')
    horario_atual = datetime.today().strftime('%H:%M')
    tres_hora = timedelta(hours=1)
    horario_mais_tres = horario_inicio + tres_hora
    horario_refresh = horario_mais_tres.strftime('%H:%M')

    if horario_atual >= horario_refresh and data_atual == horario_mais_tres.date().strftime('%d/%m/%Y'):
        print('HORA DE REFRESHAR A PAGINA!!!!')
        logarSite()
        time.sleep(10)
        horario_inicio = datetime.now()


def pegar_cor(resultado):

    cor_numeros = {
            'Vermelho': ['1', '3', '5', '7', '9', '12', '14', '16', '18', '19', '21', '23', '25', '27', '30', '32', '34', '36'],
            'Preto': ['2', '4', '6', '8', '10', '11', '13', '15', '17', '20', '22', '24', '26', '28', '29', '31', '33', '35'],
            'Verde': ['0','00']
            }
    
    for cor, lista_numeros in cor_numeros.items():
        if 'x' in resultado:
            if resultado.split(' ')[0] in lista_numeros:
                return cor
        
        else:
            if resultado in lista_numeros:
                return cor


def formatar_resultados(roleta):  

    lista_resultados = []

    try:

        resultados = roleta.text.split('\n')[:-2]
        for numero in resultados:

            if 'new' in numero or 'New' in numero or 'Hot' in numero:
                continue

            if 'x' not in numero:
                lista_resultados.append(numero)
            
        
        return lista_resultados
    
    except:
        pass


def nomeDosCassinos(nome_cassino):
    global cassinos
    global nome_dos_cassinos

    nome_dos_cassinos = [
        
        ('Roulette A'),
        ('Richie Roulette'),
        ('Fast Roulette'),
        ('Roulette A Aurum'),
        ('Roulette FTV'),
        ('Roulette POPOK'),
        ('Auto Roulette SPEED'),
        ('Roulette AUTO'),
        ('Roulette VISION A Aurum'),
        ('Roulette C'),
        ('Roulette D'),
        ('Roulette F'),
        ('Roulette B'),
        ('Roulette VISION B Aurum')
        
        ]

    cassinos = [
        
        ('Roulette A',''),
        ('Richie Roulette',''),
        ('Fast Roulette',''),
        ('Roulette A Aurum',''),
        ('Roulette FTV',''),
        ('Roulette POPOK',''),
        ('Auto Roulette SPEED',''),
        ('Roulette AUTO',''),
        ('Roulette VISION A Aurum',''),
        ('Roulette C',''),
        ('Roulette D',''),
        ('Roulette F',''),
        ('Roulette B',''),
        ('Roulette VISION B Aurum','')

    ]

    #try:
    #    for c in cassinos:
    #        if c[0] == nome_roleta:
    #            url_cassino = c[1]
    #            break
        
    #    return url_cassino
    #except:
    #    pass


def inicio():
    global browser
    global lobby_cassinos
    global logger
    global horario_inicio
    global lista_anterior
    global url
    global headers
    global dicionario_resultados

    dicionario_resultados = {}
    lista_anterior = []
    horario_inicio = datetime.now()
    logger = logging.getLogger()

    lobby_cassinos = 'https://www.playpix.com/pt/live-casino/home/-1/VGS?openGames=110-real&gameNames=Roulette'

    # Definindo opções para o browser
    warnings.filterwarnings("ignore", category=DeprecationWarning) 
    chrome_options = webdriver.ChromeOptions() 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)


def logarSite():
    
    try:
        browser.get(lobby_cassinos)
        browser.maximize_window()
    except:
        pass
    
    time.sleep(10)
    ''' Inserindo login e senha '''
    ''' Mapeando elementos para inserir credenciais '''
    try:
        browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click() #cookies
    except:
        pass

    try:
        browser.find_element_by_name('username').send_keys('cletoguii@gmail.com')                                                       
        time.sleep(3)
        browser.find_element_by_name('password').send_keys('Teste123')                                                         
        time.sleep(3)
        browser.find_element_by_xpath('//*[@id="root"]/div[6]/div/div/div/div/div/div[2]/form/div[1]/div[6]/div').click()
        time.sleep(20)
    except:
        pass

    
    #ACESSANDO EM TELA CHEIA
    try:
        tela_cheia = browser.find_element_by_xpath('//*[@id="root"]/div[3]/div[1]/div[1]/div/iframe').get_attribute('src')
        time.sleep(1)
        browser.get(tela_cheia)
        time.sleep(10)
    except:
        pass

    #ACESSANDO O IFRAME
    cont=0
    while cont<10:
        try:
            iframe = browser.find_element_by_id('gameFrame')
            browser.switch_to_frame(iframe)
            break
        except:
            time.sleep(3)
            cont+=1

    #clicando no filtro Roullette
    try:
        browser.find_element_by_xpath('//*[@class="l-button l-button-md l-button-center l-button-filter"]').click()
    except:pass       


def coletarResultados():
    global horario_atual

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

        # Auto Refresh
        auto_refresh()

        # VALIDAR SE FOI DESCONECTADO
        if browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[6]/div/div[2]/div[2]/button') or browser.find_elements_by_xpath('//*[@id="root"]/div/div[3]/div[5]/div/div[2]/div/div[3]/button'):
            browser.refresh()
            logarSite()
            continue

        try:
            ''' Elemento das roletas e historico de resultados '''
            roletas = browser.find_elements_by_xpath('//*[@class="lobby-table "]')

            if roletas == []:
                logarSite()

            else:
                pass

            ''' Percorrendo as roletas com historico'''
            for roleta in roletas:
                
                #COLETANDO INFORMAÇÕES
                #Historico de resultados da Roleta
                historico_roleta = formatar_resultados(roleta) # Formata o historico em lista
                
                #Dados do Cassino
                try:
                    data = datetime.now().strftime('%d/%m/%y')
                    hora = datetime.now().strftime('%H:%M')
                    nome_fornecedor = 'CreedRoomz'
                    nome_cassino = roleta.text.split('\n')[-2]
                    ultimo_resultado = historico_roleta[0]
                    cor = pegar_cor(ultimo_resultado)
                except:
                    pass

                #Após mapear os dados da roleta, verificar se o dado atual é igual ao ultimo dado registrado para não duplicar dados no banco
                try:
                    if dicionario_resultados == {}:
                        #print(datetime.now().strftime('%H:%M'))
                        #print(f'{data} | {hora} | {nome_fornecedor} | {nome_cassino} | {ultimo_resultado} | {cor}')
                        #Chama função para enviar dados para o banco
                        enviarDadosBanco(data, hora, nome_fornecedor, nome_cassino, ultimo_resultado, cor).start()
                        
                        #Atualiza dicionario de ultimos resultados
                        dicionario_resultados[nome_cassino] = historico_roleta

                        
                    elif dicionario_resultados[nome_cassino] == historico_roleta:

                        continue
                    
                    else:

                        #print(f'{data} | {hora} | {nome_fornecedor} | {nome_cassino} | {ultimo_resultado} | {cor}')
                        #Chama função para enviar dados para o banco
                        enviarDadosBanco(data, hora, nome_fornecedor, nome_cassino, ultimo_resultado, cor).start()
                        
                        #Atualiza dicionario de ultimos resultados
                        dicionario_resultados[nome_cassino] = historico_roleta

                        
                except KeyError:
                    #print(datetime.now().strftime('%H:%M'))
                    #print(f'{data} | {hora} | {nome_fornecedor} | {nome_cassino} | {ultimo_resultado} | {cor}')
                    
                    #Chama função para enviar dados para o banco
                    enviarDadosBanco(data, hora, nome_fornecedor, nome_cassino, ultimo_resultado, cor).start()
                    
                    #Atualiza dicionario de ultimos resultados
                    dicionario_resultados[nome_cassino] = historico_roleta


        except Exception as e:
            print(e)
            logarSite()
            continue 
    




if __name__ == '__main__':

    while True:
        try:

            print('\n\nPREPARANDO O AMBIENTE....')

            inicio()
            logarSite()

            print('\n\nINICIANDO COLETA DOS DADOS......\n\n')

            print('=' * 100)

            coletarResultados()

        except Exception as e:
            print(f'Erro inesperado -- {e} -- Reiniciando em 30 segundos.....')
            time.sleep(30)

