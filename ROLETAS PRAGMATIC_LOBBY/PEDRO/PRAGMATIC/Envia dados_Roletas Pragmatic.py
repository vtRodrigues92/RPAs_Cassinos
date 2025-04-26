from selenium import webdriver
import time
import warnings
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import logging
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import mysql.connector
from mysql.connector import Error
import threading


print()
print('                                #################################################################')
print('                                ###########   BOT DADOS PARA ROLETAS PRAGMATIC  #################')
print('                                #################################################################')
print('                                ##################### SEJA BEM VINDO ############################')
print('                                #################################################################')
print('                                ############# DESENVOLVIDO POR VICTOR RODRIGUES #################')
print('                                #################################################################\n')
print('Versão = 1.0.0')
print('Ambiente: Produção\n\n\n')




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
        TABELA = 'results_lobby_pragmatic'

        horario_inicial = datetime.now()

        try:
            #CONECTANDO COM O BANCO '''
            db_conexao = mysql.connector.connect(host=HOST, database=DB, user=USER, password=PASS)

            #Variavel que executa as querys
            cursor = db_conexao.cursor()

            ''' QUERY '''
            query_inserir_dados = (f"""INSERT INTO {TABELA} VALUES(NULL, '{self.data}', '{self.hora}', '{self.nome_fornecedor}', '{self.nome_cassino}', '{self.ultimo_resultado}', '{self.cor}')""")

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
    tres_hora = timedelta(minutes=25)
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


def formatar_resultados_pragmatic(roleta):  

    lista_resultados = []
    numero_anterior = 0

    try:

        resultados = roleta.text.split('\n')[3:]
        for numero in resultados:

            if 'x' in numero:
                #Se tiver Multiplo (100x) na lista, remove o ultimo numero add e add o ultimo numero com o multiplicador
                #Removendo item da lista
                lista_resultados.remove(numero_anterior)
                #Add resultado com múltiplo na lista
                lista_resultados.append(f'{numero_anterior} ({numero})')
                #Atulizando o numero anterior
                numero_anterior = numero

            elif 'VIP' in numero or 'NEW' in numero or 'Russian Roulette' in numero:
                continue


            else:
                lista_resultados.append(numero)
                numero_anterior = numero


        return lista_resultados
    
    except:
        pass


def nomeDosCassinos(nome_cassino):
    global cassinos
    global nome_dos_cassinos

    nome_dos_cassinos = [
        
        ('Mega Roulette'),
        ('Roulette 1 - Azure'),
        ('PowerUP Roulette'),
        ('Speed Roulette 1'),
        ('Roulette 10 - Ruby'),
        ('Speed Auto-Roulette 1'),
        ('Auto-Roulette 1'),
        ('Roulette 2'),
        ('Roulette 9 - The Club'),
        ('Roulette 6 - Turkish'),
        ('Roulette 3 - Macao'),
        ('Speed Roulette 2'),
        ('Roulette 8 - Indian'),
        ('Roulette 5 - German'),
        ('Roulette 7 - Italian'),
        ('Roulette 14 - Spanish'),
        ('Türkçe Lightning Rulet'),
        ('XXXtreme Lightning Roulette'),
        ('Lightning Roulette'),
        ('Ruletka Live'),
        ('Instant Roulette'),
        #('VIP Roulette'),
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
        ('Roleta ao Vivo'),
        ('Auto Mega Roulette')

        ]

    cassinos = [

        ('Mega Roulette',''),
        ('Roulette 1 - Azure',''),
        ('PowerUP Roulette',''),
        ('Speed Roulette 1',''),
        ('Roulette 10 - Ruby',''),
        ('Speed Auto-Roulette 1',''),
        ('Auto-Roulette 1',''),
        ('Roulette 2',''),
        ('Roulette 9 - The Club',''),
        ('Roulette 6 - Turkish',''),
        ('Roulette 3 - Macao',''),
        ('Speed Roulette 2',''),
        ('Roulette 8 - Indian',''),
        ('Roulette 5 - German',''),
        ('Roulette 7 - Italian',''),
        ('Roulette 14 - Spanish',''),
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
        ('Roleta ao Vivo',''),
        ('Auto Mega Roulette','')

    ]


def inicio():
    global browser
    global lobby_cassinos
    global logger
    global horario_inicio
    global dicionario_resultados

    dicionario_resultados = {}
    horario_inicio = datetime.now()
    logger = logging.getLogger()

    # Definindo opções para o browser
    warnings.filterwarnings("ignore", category=DeprecationWarning) 
    chrome_options = webdriver.ChromeOptions() 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)


def logarSite():

    browser.get('https://www.arbety.com/home?modal=login')
    try:
        browser.maximize_window()
    except:
        pass
    
    time.sleep(10)
    ''' Inserindo login e senha '''
    ''' Lendo o arquivo txt config-mensagens '''
    #txt = open('arquivos_txt\\canais.txt', "r", encoding="utf-8")
    #mensagem_login = txt.readlines()
    #usuario = mensagem_login[2].replace('\n','').split('= ')[1] 
    #senha = mensagem_login[3].replace('\n','').split('= ')[1]

    while True:
        try:
            
            #browser.find_element_by_xpath('//*[@class="ml-1 caption v-btn v-btn--outlined theme--dark v-size--default"]').click()
            #time.sleep(2)
            browser.find_element_by_name('email').send_keys('pedro.cletoooo@hotmail.com') 
            time.sleep(2)
            #Inserindo senha
            browser.find_element_by_name('current-password').send_keys('pedro123')
            time.sleep(2) 
            #Clicando no btn login
            browser.find_element_by_xpath('//*[@type="submit"]').click()         
            time.sleep(2)
            break

        except:
            break
            #print('ERRO AO INSERIR LOGIN -- CONTATE O DESENVOLVEDOR')

    ''' Verificando se o login foi feito com sucesso'''
    t3 = 0
    while t3 < 20:
        if browser.find_elements_by_id('balance'):
            break
        else:
            t3+=1

    #Acessando o Lobby da Pragmatic
    browser.get('https://www.arbety.com/games/external/0cd292ec4e38445c8976579594d5d1d4')

    time.sleep(20)

    #acessando iframe
    c=0
    while c < 10:

        try:
            iframe = browser.find_element_by_xpath('//*[@class="external-game"]')
            browser.switch_to_frame(iframe)
            break

        except:
            c+=1
            time.sleep(2)


def coletarResultados():
    
    elemento_roletas = '//*[@id="ROULETTE"]/*[name()="li"]'
    #'evolution':['https://www.arbety.com/games/external/5564f22a260c4e8daa807eed6e68d065','//*[@class="GridListItem--b95c7"]']}
    
    #evolution = 0

    while True:

        try:

            # Auto Refresh
            auto_refresh()

            ''' Elemento das roletas e historico de resultados '''
            roletas = browser.find_elements_by_xpath(elemento_roletas)

            if roletas == []:
                logarSite()
                continue

            else:
                pass

            #Percorrendo as roletas com historico
            for roleta in roletas:

                #Primeiramente verificando se a roleta está aberta
                if roleta.text.split('\n')[0] == 'Will be opened at':
                    continue
        
                #COLETANDO INFORMAÇÕES
                #Historico de resultados da Roleta
                historico_roleta = formatar_resultados_pragmatic(roleta) # Formata o historico em lista

                #Dados do Cassino
                try:
                    data = datetime.now().strftime('%d/%m/%y')
                    hora = datetime.now().strftime('%H:%M')
                    nome_fornecedor = 'Pragmatic'
                    nome_cassino = roleta.text.split('\n')[2] if roleta.text.split('\n')[0] != 'VIP' and roleta.text.split('\n')[0] !='NEW' else roleta.text.split('\n')[3]
                    ultimo_resultado = historico_roleta[0]
                    cor = pegar_cor(ultimo_resultado)
                except:
                    pass

                #Após mapear os dados da roleta, verificar se o dado atual é igual ao ultimo dado registrado para não duplicar dados no banco
                try:
                    if dicionario_resultados == {}:
                        print(datetime.now().strftime('%H:%M'))
                        print(f'{data} | {hora} | {nome_fornecedor} | {nome_cassino} | {ultimo_resultado} | {cor}')
                        #Chama função para enviar dados para o banco
                        enviarDadosBanco(data, hora, nome_fornecedor, nome_cassino, ultimo_resultado, cor).start()
                        print('Registrado no Banco....')

                        #Atualiza dicionario de ultimos resultados
                        dicionario_resultados[nome_cassino] = historico_roleta

                        print('=' * 100)

                    elif dicionario_resultados[nome_cassino] == historico_roleta:

                        continue
                    
                    else:

                        print(datetime.now().strftime('%H:%M'))
                        print(f'{data} | {hora} | {nome_fornecedor} | {nome_cassino} | {ultimo_resultado} | {cor}')
                        #Chama função para enviar dados para o banco
                        enviarDadosBanco(data, hora, nome_fornecedor, nome_cassino, ultimo_resultado, cor).start()
                        print('Registrado no Banco....')

                        #Atualiza dicionario de ultimos resultados
                        dicionario_resultados[nome_cassino] = historico_roleta

                        print('=' * 100)

                except KeyError:
                    print(datetime.now().strftime('%H:%M'))
                    print(f'{data} | {hora} | {nome_fornecedor} | {nome_cassino} | {ultimo_resultado} | {cor}')
                    #Chama função para enviar dados para o banco
                    enviarDadosBanco(data, hora, nome_fornecedor, nome_cassino, ultimo_resultado, cor).start()
                    print('Registrado no Banco....')

                    #Atualiza dicionario de ultimos resultados
                    dicionario_resultados[nome_cassino] = historico_roleta

                    print('=' * 100)
            
        except:

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
