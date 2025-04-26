from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
import logging
from datetime import datetime, timedelta
import telebot
from telegram.ext import *
from telebot import *
import os
import ast
import warnings
from threading import *
#from selenium.webdriver import FirefoxProfile, Firefox, DesiredCapabilities
#from webdriver_manager.firefox import GeckoDriverManager
#from selenium.webdriver.firefox.options import Options



print()
print('                                #################################################################')
print('                                ################   BOT FUTEBOL REAL BET365   ####################')
print('                                #################################################################')
print('                                ##################### SEJA BEM VINDO ############################')
print('                                #################################################################')
print('                                ############# DESENVOLVIDO POR VICTOR RODRIGUES #################')
print('                                #################################################################\n')
print('Versão = 1.0.0')
print('Ambiente: Produção\n\n\n')






class CheckSinalThread(Thread):
    def run(self):
        for a in range(1,10):
            print(a)
            time.sleep(1)






# GERA TXT DO PLACAR
def placar():
    global placar_win
    global placar_semGale
    global placar_gale1
    global placar_gale2
    global placar_loss
    global placar_geral
    global asserividade
    global data_hoje
    global lista_sinais_enviados

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
                asserividade = arq_placar[5].split(',')[1]+"%"
            
            except:
                pass

            
    else:
        # Cria Lista de Sinais Enviados
        lista_sinais_enviados = []

        # Criar um arquivo com a data atual
        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
            arquivo.write("win,0\nsg,0\ng1,0\ng2,0\nloss,0\nass,0")

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
                asserividade = arq_placar[5].split(',')[1]+"%"
            
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
            for key, value in canais.items():
                try:
                    globals()[f'placar_{key}'] = bot.send_message(key,\
        "📊 Placar Atual do dia "+data_hoje+":\n\
        =====================\n\
        😍 WIN - "+str(placar_win)+"\n\
        🏆 WIN S/ GALE - "+str(placar_semGale)+"\n\
        🥇 WIN GALE1 - "+str(placar_gale1)+"\n\
        🥈 WIN GALE2 - "+str(placar_gale2)+"\n\
        😭 LOSS - "+str(placar_loss)+"\n\
        =====================\n\
        🎯 Assertividade "+ asserividade)
        #Variavel Dinâmica
                except:
                    pass

        except:
            pass

    except Exception as a:
        logger.error('Exception ocorrido no ' + repr(a))
        #placar = bot.reply_to(message,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%", reply_markup=markup)
        pass




# VALIDADOR DE DATA
def validaData():
    global data_resultado
    global reladiarioenviado
    global horario_atual

    data_hoje = datetime.today()
    subtrai_dia = timedelta(days=-1)
    data_ontem = data_hoje + subtrai_dia
    data_resultado = data_ontem.strftime('%d/%m/%Y')
    horario_atual = datetime.today().strftime('%H:%M')

    if horario_atual == '11:55' and reladiarioenviado == 0 or horario_atual == '23:55' and reladiarioenviado == 0:
        envia_placar()
        reladiarioenviado +=1

    
    if horario_atual == '11:56' and reladiarioenviado == 1 or horario_atual == '23:56' and reladiarioenviado == 1:
        reladiarioenviado = 0

    # Condição que zera o placar quando o dia muda
    if horario_atual == '00:00' and reladiarioenviado == 0:
        placar()
        reladiarioenviado +=1

    # Condição que zera o placar quando o dia muda
    if horario_atual == '00:01' and reladiarioenviado == 1:
        reladiarioenviado = 0

    


# AUTO REFRESH
def auto_refresh():
    global horario_inicio

    horario_atual = datetime.today().strftime('%H:%M')
    tres_hora = timedelta(hours=3)
    horario_mais_tres = horario_inicio + tres_hora
    horario_refresh = horario_mais_tres.strftime('%H:%M')

    if horario_atual == horario_refresh:
        print('HORA DE REFRESHAR A PAGINA!!!!')
        logar_site()
        time.sleep(2)
        horario_inicio = datetime.now()




def manipula_aba():

    try:
        # Abre uma nova aba e vai para o site do SO
        browser.execute_script("window.open('https://www.bet365.com/#/IP/B1', '_blank')")
        time.sleep(15)

        #Fechando a Aba Ativa
        browser.close()

        # Muda de aba
        browser.switch_to_window(browser.window_handles[0])

    except:
        pass




def inicio():
    global sticker_alerta
    global sticker_win
    global sticker_win_2x
    global sticker_win_5x
    global sticker_loss
    global logger
    global browser
    global lista_anterior
    global horario_inicio
    global lista_sinais_enviados


    horario_inicio = datetime.now()

    lista_anterior = []
    lista_sinais_enviados = []
    logger = logging.getLogger()

    # Definindo opções para o browser
    warnings.filterwarnings("ignore", category=DeprecationWarning) 

    # Definindo opções para o browser

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
    #profile = FirefoxProfile()
    #profile.set_preference("dom.webdriver.enabled", False)
    #profile.set_preference('useAutomationExtension', False)
    #desired = DesiredCapabilities.FIREFOX

    browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)                      # Chrome
    #browser = webdriver.Firefox(executable_path=GeckoDriverManager().install(), firefox_profile=profile, desired_capabilities=desired)            # FireFox        
    #browser  = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install())                       # Brave
    #browser = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(),chrome_options=chrome_options)                     # Chromium




def logar_site():

    #logger = logging.getLogger()
    browser.get(r"https://www.bet365.com/#/IP/B1")
    try:
        browser.maximize_window()
    except:
        pass


    time.sleep(10)
    manipula_aba()

    c=0
    while c < 10:
        if browser.find_elements_by_xpath('//*[@class="iip-IntroductoryPopup_Cross"]') or browser.find_elements_by_xpath('//*[@class="ovm-MediaIconContainer_Buttons "]'):
            break
        else:
            time.sleep(10)
            c+=1

    # PopUp
    try:
        browser.find_element_by_xpath('//*[@class="iip-IntroductoryPopup_Cross"]').click()
    except:
        pass

    # Cookies
    try:
        browser.find_element_by_xpath('//*[@class="ccm-CookieConsentPopup_Accept "]').click()
    except:
        pass


                    

def coletar_dados():
    global estrategia
    global appm_time1
    global cg_time1
    global appm_time2
    global cg_time2
    global tempo_jogo
    global time1
    global time2
    global placar_time1
    global placar_time2
    global placar_jogo
    global ataq_perig_time1
    global ataq_perig_time2
    global chutes_nogol_time1
    global chutes_nogol_time2
    global finalizacoes_time1
    global finalizacoes_time2
    global escanteio_time1
    global escanteio_time2

    while True:

        # Validando data para envio do relatório diário
        validaData()

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass
        
    
        while True:
            try:
                # Auto Refresh
                auto_refresh()

                # Validando data para envio do relatório diário
                validaData()
                
                # Validando se foi solicitado o stop do BOT
                if parar != 0:
                    break
                else:
                    pass

            
                jogos = browser.find_elements_by_xpath('//*[@class="ovm-MediaIconContainer "]')

                ''' VALIDANDO SE A LISTA ESTA VAZIA'''
                if jogos == []:
                    logar_site()
                    continue


                for jogo in jogos:

                    # Validando se foi solicitado o stop do BOT
                    if parar != 0:
                        break
                    else:
                        pass

                    try:

                        # Entrando nas Estatisticas do Jogo
                        jogo.click()
                        time.sleep(1.5)

                        # Pegando o Nome e Placar dos Jogos
                        try:
                            # Placar Normal
                            placar_jogo = browser.find_elements_by_xpath('//*[@class="lsb-ScoreBasedScoreboardAggregate "]')[0].text.split('\n')

                            ### VALIDANDO SE O JOGO É VIRTUAL (E-SOCCER) OU FEMININO
                            if 'Esports' in browser.find_element_by_xpath('//*[@class="lsb-ScoreBasedScoreboardAggregate "]').text or\
                                'Women'  in browser.find_element_by_xpath('//*[@class="lsb-ScoreBasedScoreboardAggregate "]').text or\
                              'Femenino' in browser.find_element_by_xpath('//*[@class="lsb-ScoreBasedScoreboardAggregate "]').text: 
                                continue

                            else:
                                pass

                        except:
                            # Placar com Agregado
                            placar_jogo = browser.find_element_by_xpath('//*[@class="lsb-ScoreBasedScoreboardAggregate lsb-ScoreBasedScoreboardAggregate-aggscore "]').text.split('\n')
                            del(placar_jogo[1])
                            del(placar_jogo[2])
                            del(placar_jogo[3])

                            ### VALIDANDO SE O JOGO É VIRTUAL (E-SOCCER)
                            if 'Esports' in browser.find_element_by_xpath('//*[@class="lsb-ScoreBasedScoreboardAggregate lsb-ScoreBasedScoreboardAggregate-aggscore "]').text:
                                continue
                            else:
                                pass



                        # Pegando Tempo de Jogo
                        try:
                            tempo_jogo = browser.find_elements_by_xpath('//*[@class="ml1-SoccerClock_Clock "]')[0].text

                            if tempo_jogo == '':
                                tempo_jogo = browser.find_elements_by_xpath('//*[@class="ml1-FixtureInfo_SubItems "]')[0].text.replace('\n',' ')

                        except:
                            try:
                                # CASO SEJA O ICONE PLAY,CLICAR NO CAMPO
                                browser.find_element_by_css_selector('.lv-ButtonBar_MatchLive').click()
                                                                           
                                tempo_jogo = browser.find_elements_by_xpath('//*[@class="ml1-SoccerClock_Clock "]')[0].text

                                if tempo_jogo == '':
                                    tempo_jogo = browser.find_elements_by_xpath('//*[@class="ml1-FixtureInfo_SubItems "]')[0].text.replace('\n',' ')


                            except:
                                tempo_jogo = browser.find_elements_by_xpath('//*[@class="ml1-FixtureInfo_SubItems "]')[0].text.replace('\n',' ')


                        # Validando se o Jogo Ainda não Começou
                        if 'Chute Inicial' in tempo_jogo:
                            print(datetime.now().strftime('%H:%M'),'\n',\
                            'Partida ----- ',placar_jogo,'\n',\
                            tempo_jogo)

                            print('=' * 100)
                            continue


                        # Pegando os Dados Para Validar o Funil
                        # TIME1
                        time1 = placar_jogo[0]
                        placar_time1 = placar_jogo[1]
                        ataq_perig_time1 = int(browser.find_elements_by_xpath('//*[@class="ml1-WheelChartAdvanced_Team1Text "]')[1].text)
                        finalizacoes_time1 = int(browser.find_elements_by_xpath('//*[@class="ml1-ProgressBarAdvancedDual_SideLabel "]')[0].text)
                        chutes_nogol_time1 = int(browser.find_elements_by_xpath('//*[@class="ml1-ProgressBarAdvancedDual_SideLabel "]')[1].text)
                        escanteio_time1 = int(browser.find_elements_by_xpath('//*[@class="ml1-StatsColumnAdvanced_MiniValue "]')[0].text)
                        try:
                            appm_time1 = round(ataq_perig_time1 / int(tempo_jogo[:2]),2)
                        except:
                            appm_time1 = 0

                        cg_time1 = finalizacoes_time1 + escanteio_time1
                        
                        # TIME2
                        time2 = placar_jogo[3]
                        placar_time2 = placar_jogo[2]
                        ataq_perig_time2 = int(browser.find_elements_by_xpath('//*[@class="ml1-WheelChartAdvanced_Team2Text "]')[1].text)
                        finalizacoes_time2 = int(browser.find_elements_by_xpath('//*[@class="ml1-ProgressBarAdvancedDual_SideLabel "]')[2].text)
                        chutes_nogol_time2 = int(browser.find_elements_by_xpath('//*[@class="ml1-ProgressBarAdvancedDual_SideLabel "]')[3].text)
                        escanteio_time2 = int(browser.find_elements_by_xpath('//*[@class="ml1-StatsColumnAdvanced_MiniValue "]')[-3].text)
                        appm_time2 = round(ataq_perig_time2 / int(tempo_jogo[:2]),2)
                        cg_time2 = finalizacoes_time2 + escanteio_time2
                        
                        print(datetime.now().strftime('%H:%M'),'\n',\
                            'Partida --------------- ', placar_jogo,'\n',\
                            'Tempo ------------------', tempo_jogo,'\n',\
                            'Ataques Perigosos ----- ', str(ataq_perig_time1) + ' x ' + str(ataq_perig_time2),'\n',\
                            'APPM -------------------', str(appm_time1) + ' x ' + str(appm_time2), '\n',\
                            'CG ---------------------', str(cg_time1) + ' x ' + str(cg_time2))


                        # Validando se foi solicitado o stop do BOT
                        if parar != 0:
                            break
                        else:
                            pass


                        # Validando Qual Time tem a Maior Quantidade de Ataques Perigosos e Validando a Estratégia
                        if ataq_perig_time1 > ataq_perig_time2:
                            ataque_perigoso = int(browser.find_elements_by_xpath('//*[@class="ml1-WheelChartAdvanced_Team1Text "]')[1].text)
                            #posse_bola = int(browser.find_elements_by_xpath('//*[@class="ml1-WheelChartAdvanced_Team1Text "]')[2].text)
                            finalizacoes = int(browser.find_elements_by_xpath('//*[@class="ml1-ProgressBarAdvancedDual_SideLabel "]')[0].text)
                            #chutes_gol = int(browser.find_elements_by_xpath('//*[@class="ml1-ProgressBarAdvancedDual_SideLabel "]')[1].text)
                            escanteio = int(browser.find_elements_by_xpath('//*[@class="ml1-StatsColumnAdvanced_MiniValue "]')[0].text)
                            placar_referencia = placar_time1

                            ''' Chama a função que valida a estratégia para enviar o sinal Telegram '''
                            validador_time1(ataque_perigoso, finalizacoes, escanteio, tempo_jogo, placar_referencia, time1)


                        elif ataq_perig_time1 == ataq_perig_time2:
                            print('ATAQUES PERIGOSOS IGUAIS!')


                        else:
                            ataque_perigoso = int(browser.find_elements_by_xpath('//*[@class="ml1-WheelChartAdvanced_Team2Text "]')[1].text)
                            finalizacoes = int(browser.find_elements_by_xpath('//*[@class="ml1-ProgressBarAdvancedDual_SideLabel "]')[2].text)
                            #chutes_gol = int(browser.find_elements_by_xpath('//*[@class="ml1-ProgressBarAdvancedDual_SideLabel "]')[3].text)
                            escanteio = int(browser.find_elements_by_xpath('//*[@class="ml1-StatsColumnAdvanced_MiniValue "]')[-3].text)
                            placar_referencia = placar_time2

                            ''' Chama a função que valida a estratégia para enviar o sinal Telegram '''
                            validador_time2(ataque_perigoso, finalizacoes, escanteio, tempo_jogo, placar_referencia)

                        
                        #validar_estrategia(ataque_perigoso, finalizacoes, escanteio, tempo_jogo, placar_referencia)

                        print('=' * 100)

                    except:
                        continue
            

                ''' Exceção se o jogo não estiver disponível '''
            except:
                print('Algo deu errado na funcao Coletar Dados..Refreshando...')
                logar_site()




def validador_time1(ataque_perigoso, finalizacoes, escanteio, tempo_jogo, placar_referencia, time1):
    
    try:
        # CALCULO DO FUNIL PARA O TIME QUE TEM O MAIOR APPM
        appm = round(ataque_perigoso / int(tempo_jogo[:2]),2) # = OU > 1 
        cg = finalizacoes + escanteio # > 10 NO HT E MAIOR QUE 15 NO FT
        dif_placar = int(placar_referencia) - int(placar_time2)

        #______________ ESTRATÉGIA _____________#

        # VALIDAÇÃO DO FUNIL HT ( PRIMEIRO TEMPO )
        if appm >= usuario_appm and cg >= usuario_cg_ht and\
           int(tempo_jogo[:-3]) >= usuario_tempo_inicial_ht and\
           int(tempo_jogo[:-3]) <= usuario_tempo_final_ht and\
           dif_placar >= -1 and dif_placar <= 0 and  placar_jogo[0]+' x '+placar_jogo[3]+' x '+'HT' not in lista_sinais_enviados:
            
            enviarSinalTelegram(cg, appm, time1)
            #thread = CheckSinalThread()
            #thread.start()

            lista_sinais_enviados.append(placar_jogo[0]+' x '+placar_jogo[3]+' x '+'HT')


        # VALIDAÇÃO DO FUNIL FT ( SEGUNDO TEMPO )
        if appm >= usuario_appm and cg > usuario_cg_ft and\
           int(tempo_jogo[:-3]) >= usuario_tempo_inicial_ft and\
           int(tempo_jogo[:-3]) < usuario_tempo_final_ft  and\
           dif_placar >= -1 and dif_placar <= 0 and  placar_jogo[0]+' x '+placar_jogo[3]+' x '+'FT' not in lista_sinais_enviados:

            enviarSinalTelegram(cg, appm)
            #thread = CheckSinalThread()
            #thread.start()
            
            lista_sinais_enviados.append(placar_jogo[0]+' x '+placar_jogo[3]+' x '+'FT')

    except:
        pass




def validador_time2(ataque_perigoso, finalizacoes, escanteio, tempo_jogo, placar_referencia):

    try:
        # CALCULO DO FUNIL PARA O TIME QUE TEM O MAIOR APPM
        appm = round(ataque_perigoso / int(tempo_jogo[:2]),2) # = OU > 1 
        cg = finalizacoes + escanteio # > 10 NO HT E MAIOR QUE 15 NO FT
        dif_placar = int(placar_referencia) - int(placar_time1)

        #______________ ESTRATÉGIA _____________#

        # VALIDAÇÃO DO FUNIL HT ( PRIMEIRO TEMPO )
        if appm >= usuario_appm and cg >= usuario_cg_ht and\
           int(tempo_jogo[:-3]) >= usuario_tempo_inicial_ht and int(tempo_jogo[:-3]) <= usuario_tempo_final_ht and\
           dif_placar >= -1 and dif_placar <= 0 and\
           placar_jogo[0]+' x '+placar_jogo[3]+' x '+'HT' not in lista_sinais_enviados:

            enviarSinalTelegram(cg, appm, time2)
            #val += 1
            #thread = CheckSinalThread()
            #thread.start()

            lista_sinais_enviados.append(placar_jogo[0]+' x '+placar_jogo[3]+' x '+'HT')


        # VALIDAÇÃO DO FUNIL FT ( SEGUNDO TEMPO )
        if appm >= usuario_appm and cg > usuario_cg_ft and\
           int(tempo_jogo[:-3]) > usuario_tempo_inicial_ft and int(tempo_jogo[:-3]) < usuario_tempo_final_ft and\
           dif_placar >= -1 and dif_placar <= 0 and\
           placar_jogo[0]+' x '+placar_jogo[3]+' x '+'FT' not in lista_sinais_enviados:
     
            enviarSinalTelegram(cg, appm)
            #thread = CheckSinalThread()
            #thread.start()

            lista_sinais_enviados.append(placar_jogo[0]+' x '+placar_jogo[3]+' x '+'FT')

    except:
        pass




def pegar_link_jogo(time1, time2):
    
    try:

        aposta_escanteio = None
        aposta_gol = None 
        
        link_jogos = browser.find_elements_by_xpath('//*[@class="ovm-FixtureDetailsTwoWay_TeamName "]')
        
        for link in link_jogos:
            if time1 in link.text or time2 in link.text:
                link_jogo = link
                break

        link_jogo.click()
        time.sleep(0.5)
        url_jogo = browser.current_url

        # Verificando se tem as opções de aposta Escanteio e Gol
        opcoes_aposta = browser.find_elements_by_xpath('//*[@class="ipe-GridHeaderTabLink ipe-GridHeaderTabLink_Wide "]')
        for aposta in opcoes_aposta:
            if aposta.text == 'Gols' or aposta.text == 'Goals' or aposta.text == 'Goles':
                aposta_gol = aposta.text

            if aposta.text == 'Escanteios/Cartões' or aposta.text == 'Corners/Cards' or aposta.text == 'Córners/Tarjetas':
                aposta_escanteio = aposta.text

        browser.back()

        return url_jogo, aposta_escanteio, aposta_gol

    except:
        pass

    
    
    
def enviarSinalTelegram(cg, appm, time_referencia):
    global table_sinal

    try:
        
        # PEGANDO O LINK DO JOGO
        url_jogo, aposta_escanteio, aposta_gol = pegar_link_jogo(time1, time2)
        
        if aposta_escanteio != None and aposta_gol != None:

            print('ENVIA SINAL TELEGRAM')

            ''' Lendo o arquivo txt canais '''
            txt = open("canais.txt", "r", encoding="utf-8")
            arquivo = txt.readlines()
            canais = arquivo[7].replace('canais= ','').replace('\n','')
            canais = ast.literal_eval(canais) # Convertendo string em dicionario 

            ''' Estruturando mensagem '''
            txt = open("config-mensagens.txt", "r", encoding="utf-8")
            mensagem_sinal = txt.readlines()
            
            ''' Enviando mensagem Telegram '''
            try:
                for key, value in canais.items():
                    try:
                        table_sinal = mensagem_sinal[0].replace('\n','') + '\n\n' +\
                                      mensagem_sinal[2].replace('\n','') + '\n' +\
                                      mensagem_sinal[3].replace('\n','').replace('[TEMPO_JOGO]', tempo_jogo) + '\n' +\
                                      mensagem_sinal[4].replace('\n','').replace('[PLACAR_TIME1]', placar_time1).replace('[PLACAR_TIME2]', placar_time2) + '\n' +\
                                      mensagem_sinal[5].replace('\n','').replace('[AP_TIME1]', str(ataq_perig_time1)).replace('[AP_TIME2]', str(ataq_perig_time2)) + '\n' +\
                                      mensagem_sinal[6].replace('\n','').replace('[CHUTES_TIME1]', str((chutes_nogol_time1+finalizacoes_time1))).replace('[CHUTES_TIME2]', str((chutes_nogol_time2+finalizacoes_time2))) + '\n' +\
                                      mensagem_sinal[7].replace('\n','').replace('[ESCANTEIO_TIME1]', str(escanteio_time1)).replace('[ESCANTEIO_TIME2]', str(escanteio_time2)) + '\n\n' +\
                                      mensagem_sinal[9].replace('\n','').replace('[TIME_REFERENCIA]', time_referencia+' Pressionando') + '\n\n' +\
                                      mensagem_sinal[11].replace('\n','').replace('[LINK_JOGO]', url_jogo) + '\n\n' +\
                                      mensagem_sinal[13].replace('\n','').replace('[TIME1]', time1).replace('[TIME2]', time2)
                    
                        ''' ENVIANDO SINAL TELEGRAM PARA O CANAL NO LOOP FOR CORRENTE '''
                        globals()[f'sinal_{key}'] = bot.send_message(key, table_sinal, parse_mode='HTML', disable_web_page_preview=True)
                    
                    except Exception as e:
                        print(e)
                        pass
            
            except:
                pass
        
        else:
            pass

    except:
        pass







if __name__=='__main__':

    inicio()
    logar_site()
    


print('########################### AGUARDANDO COMANDOS ###########################')

global canais
global bot
global placar_win
global placar_semGale
global placar_gale1
global placar_gale2
global placar_gale3
global placar_loss
global resultados_sinais


# PLACAR
#placar_win = 0
#placar_semGale= 0
#placar_gale1= 0
#placar_gale2= 0
#placar_gale3= 0
#placar_loss = 0
#resultados_sinais = placar_win + placar_loss
estrategias = []
placar_estrategia = []
placar_estrategias = []
estrategias_diaria = []
placar_estrategias_diaria = []
contador = 0
botStatus = 0
validador_sinal = 0
parar = 0
dic_estrategia_usuario = {}
lista_seq_minima = []
lista_onde_apostar = []
lista_roletas = []
placar_roletas = []
roletas_diaria = []
placar_roletas_diaria = []
contador_passagem = 0
lista_ids = []
lista_estrategias = []
dicionario_roletas = {}



# LENDO TXT PARA DEFINIR VARIAVEL DE CANAIS E VALIDAÇÃO DE USUÁRIO
txt = open("canais.txt", "r", encoding="utf-8")
arquivo = txt.readlines()
CHAVE_API = arquivo[2].split(' ')[1].split('\n')[0]

ids = arquivo[6].split(' ')[1].split('\n')[0]


bot = telebot.TeleBot(CHAVE_API)


global message



''' FUNÇÕES BOT ''' ##



def generate_buttons_estrategias(bts_names, markup):
    for button in bts_names:
        markup.add(types.KeyboardButton(button))
    return markup





def pausarBot():
    global parar
    global browser

    while True:
        try:
            parar = 1
            return 

        except:
            continue





@bot.message_handler(commands=['⚙🧠 Cadastrar_Estratégia'])
def cadastrarEstrategia(message):
    global contador_passagem

    if contador_passagem == 0:
        #Init keyboard markup
        markup_appm = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
        
        markup_appm.add('◀ Voltar')    

        message_valor_appm = bot.reply_to(message, "🤖 Ok! Digite um Valor para o APPM ", reply_markup=markup_appm)
        bot.register_next_step_handler(message_valor_appm, registrar_appm)
    

    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙🧠 Cadastrar Estratégia', '⚙🎰 Cadastrar Roletas', '🧠📜 Estratégias Cadastradas', '🎰📜 Roletas Cadastradas', '🗑🧠 Apagar Estratégia', '🗑🎰 Apagar Roleta', '⏲ Ultimos Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_estrategia = bot.reply_to(message, "🤖⛔ Estou validando uma estratégia! Tente novamente em alguns instanstes.", reply_markup=markup)






@bot.message_handler(commands=['📝🧠 Editar_Estratégia'])
def editar_estrategia(message):
    global estrategia
    global estrategias
    global contador_passagem

    try:
    
        #Add to buttons by list with ours generate_buttons function.
        markup_estrategia = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup_estrategia.add(f'APPM = {usuario_appm}',
                              f'CG|HT = {usuario_cg_ht}',
                              f'CG|FT = {usuario_cg_ft}',
                              f'TEMPO INICIAL HT = {usuario_tempo_inicial_ht}',
                              f'TEMPO FINAL HT = {usuario_tempo_final_ht}',
                              f'TEMPO INICIAL FT = {usuario_tempo_inicial_ft}',
                              f'TEMPO FINAL FT = {usuario_tempo_final_ft}',
                              '◀ Voltar')


        message_editar_estrategia = bot.reply_to(message, "🤖 Escolha Qual Condição da Estratégia Será Editada 👇", reply_markup=markup_estrategia)
        bot.register_next_step_handler(message_editar_estrategia, editar_campo_escolhido)
    
    except:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('✅ Ativar Bot', '⚙🧠 Cadastrar Estratégia', '📝🧠 Editar Estratégia', '🧠📜 Estratégia Cadastrada', '🛑 Pausar Bot')

        message_editar_estrategia = bot.reply_to(message, "🤖 Algo deu Errado. Tente Novamente 🙁.", reply_markup=markup)






@bot.message_handler(commands=['🧠📜 Estratégia_Cadastrada'])
def estrategiasCadastradas(message):
    global estrategia
    global estrategias
    global lista_estrategias

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup = markup.add('✅ Ativar Bot', '⚙🧠 Cadastrar Estratégia', '📝🧠 Editar Estratégia', '🧠📜 Estratégia Cadastrada', '🛑 Pausar Bot')

    try:

        estrategia_cadastrada = 'APPM = '+ str(usuario_appm) + '\n' +\
                                'CG|HT = '+ str(usuario_cg_ht) + '\n' +\
                                'CG|FT = '+ str(usuario_cg_ft) + '\n' +\
                                'TEMPO HT INICAL E FINAL = '+ str(usuario_tempo_inicial_ht) + "' - " + str(usuario_tempo_final_ht) + "'" + '\n' +\
                                'TEMPO FT INICIAL E FINAL = '+ str(usuario_tempo_inicial_ft) + "' - " + str(usuario_tempo_final_ft) + "'"
        
        bot.reply_to(message, "🤖 Ok! Mostrando Estratégia Cadastrada.👇", reply_markup=markup)

        bot.send_message(message.chat.id, estrategia_cadastrada)

    except:
        bot.reply_to(message, "🤖 Nenhuma estratégia cadastrada ❌", reply_markup=markup)






@bot.message_handler(commands=['🛑 Pausar_bot'])
def pausar(message):
    global botStatus
    global contador_passagem
    global browser
    global parar

    if contador_passagem != 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('✅ Ativar Bot', '⚙🧠 Cadastrar Estratégia', '📝🧠 Editar Estratégia', '🧠📜 Estratégia Cadastrada', '🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Estou validando um Sinal. Tente novamente em alguns instanstes.", reply_markup=markup)

    elif botStatus == 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('✅ Ativar Bot', '⚙🧠 Cadastrar Estratégia', '📝🧠 Editar Estratégia', '🧠📜 Estratégia Cadastrada', '🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Bot já está pausado ", reply_markup=markup)

    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('✅ Ativar Bot', '⚙🧠 Cadastrar Estratégia', '📝🧠 Editar Estratégia', '🧠📜 Estratégia Cadastrada', '🛑 Pausar Bot')

        botStatus = 0
        parar = 1
        #pausarBot()

        print('\n\n')
        print('Pausar Bot')
        print('Parando o Bot....\n')

        message_final = bot.reply_to(message, "🤖 Ok! Bot pausado 🛑", reply_markup=markup)

        print('\n\n')
        print('############################################ AGUARDANDO COMANDOS ############################################')
        
        return






@bot.message_handler(commands=['start', 'iniciar', 'começar'])
def start(message):

    if str(message.chat.id) in ids:

        ''' Add id na lista de ids'''
        if str(message.chat.id) not in lista_ids:
            lista_ids.append(message.chat.id)
        else:
            pass
       
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('✅ Ativar Bot', '⚙🧠 Cadastrar Estratégia', '📝🧠 Editar Estratégia', '🧠📜 Estratégia Cadastrada', '🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message, "🤖 Bot Futebol Ao Vivo Ativado! ✅ Escolha uma opção 👇",
                                    reply_markup=markup)
        
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(message_opcoes, opcoes)
    
    else:
        message_error = bot.reply_to(message, "🤖 Você não tem permissão para acessar este Bot ❌🚫")






@bot.message_handler()
def opcoes(message_opcoes):

    if message_opcoes.text in ['✅ Ativar Bot']:
        global botStatus
        global parar
        global reladiarioenviado
        global browser
        global contador_passagem

        print('Ativar Bot')

        try:

            if botStatus == 1:

                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
                markup = markup.add('✅ Ativar Bot', '⚙🧠 Cadastrar Estratégia', '📝🧠 Editar Estratégia', '🧠📜 Estratégias Cadastradas', '🛑 Pausar Bot')

                message_canal = bot.reply_to(message_opcoes, "🤖⛔ Bot já está ativado",
                                    reply_markup=markup)


            elif usuario_tempo_final_ft == '':
                #Init keyboard markup
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
                markup = markup.add('✅ Ativar Bot', '⚙🧠 Cadastrar Estratégia', '📝🧠 Editar Estratégia', '🧠📜 Estratégias Cadastradas', '🛑 Pausar Bot')

                message_canal = bot.reply_to(message_opcoes, "🤖⛔ Cadastre ou Termine de Cadastrar a Estratégia! ",
                                    reply_markup=markup)

            
            else:
                #Init keyboard markup
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
                markup = markup.add('✅ Ativar Bot', '⚙🧠 Cadastrar Estratégia', '📝🧠 Editar Estratégia', '🧠📜 Estratégias Cadastradas', '🛑 Pausar Bot')

                message_canal = bot.reply_to(message_opcoes, "🤖 Ok! Bot Ativado com sucesso! ✅ Em breve receberá sinais nos canais informados no arquivo auxiliar! ",
                                        reply_markup=markup)
                
                botStatus = 1
                reladiarioenviado = 0
                parar=0
                contador_passagem = 0

                print('##################################################  INICIANDO AS ANÁLISES  ##################################################')
                print()

                coletar_dados() # Analisando os Dados

        except:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            markup = markup.add('✅ Ativar Bot', '⚙🧠 Cadastrar Estratégia', '📝🧠 Editar Estratégia', '🧠📜 Estratégias Cadastradas', '🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖⛔ Cadastre ou Termine de Cadastrar a Estratégia! ",
                                reply_markup=markup)

       

    

    if message_opcoes.text in ['🛑 Pausar Bot']:
        print('Pausar Bot')
        pausar(message_opcoes)

    
    if message_opcoes.text in ['⚙🧠 Cadastrar Estratégia']:
        print('Cadastrar Estratégia')
        cadastrarEstrategia(message_opcoes)


    if message_opcoes.text in ['🧠📜 Estratégia Cadastrada']:
        print('Estratégias Cadastradas')
        estrategiasCadastradas(message_opcoes)


    if message_opcoes.text in ['📝🧠 Editar Estratégia']:
        print('Editar Estratégia')
        editar_estrategia(message_opcoes)






@bot.message_handler()
def registrar_appm(message_valor_appm):
    global usuario_appm

    if message_valor_appm.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('✅ Ativar Bot', '⚙🧠 Cadastrar Estratégia', '📝🧠 Editar Estratégia', '🧠📜 Estratégia Cadastrada', '🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_valor_appm, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        return


    else:

        #Init keyboard markup
        markup_cg_ht = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

        usuario_appm = float(message_valor_appm.text)
        print('APPM = ', usuario_appm)
    
        markup_cg_ht.add('◀ Voltar')

        message_valor_cg_ht = bot.reply_to(message_valor_appm, "🤖 Ok! Agora, Insira um Valor para o Total da Soma do CG no HT(Primeiro Tempo) ", reply_markup=markup_cg_ht)
        bot.register_next_step_handler(message_valor_cg_ht, registrar_cg_ht)






def registrar_cg_ht(message_valor_cg_ht):
    global usuario_cg_ht

    if message_valor_cg_ht.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('✅ Ativar Bot', '⚙🧠 Cadastrar Estratégia', '📝🧠 Editar Estratégia', '🧠📜 Estratégia Cadastrada', '🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_valor_cg_ht, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        return


    else:
        markup_cg_ft = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

        usuario_cg_ht = int(message_valor_cg_ht.text)
        print('CG HT = ', usuario_cg_ht)

        markup_cg_ft.add('◀ Voltar')
        message_valor_cg_ft = bot.reply_to(message_valor_cg_ht, "🤖 Boa! Agora, Insira um Valor para o Total da Soma do CG no FT(Segundo Tempo) ", reply_markup=markup_cg_ft)
        bot.register_next_step_handler(message_valor_cg_ft, registrar_cg_ft)






def registrar_cg_ft(message_valor_cg_ft):
    global usuario_cg_ft

    if message_valor_cg_ft.text in ['◀ Voltar']:
        #Init keyboard markup
        markup_cg_ft = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True) 
        markup_cg_ft.add('◀ Voltar')

        message_valor_cg_ht = bot.reply_to(message_valor_cg_ft, "🤖 Ok! Agora, Insira um Valor para o Total da Soma do CG no HT(Primeiro Tempo) ", reply_markup=markup_cg_ft)
        bot.register_next_step_handler(message_valor_cg_ht, registrar_cg_ht)


    else:
        markup_tempo_ht = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup_tempo_ht.add('◀ Voltar')

        usuario_cg_ft = int(message_valor_cg_ft.text)
        print('CG FT = ', usuario_cg_ft)

        message_tempo_ht = bot.reply_to(message_valor_cg_ft, "🤖 Perfeito! Agora, Insira o Intervalo de Tempo Inicial e Final do HT(Primeiro Tempo), Ex: 25,40 ", reply_markup=markup_tempo_ht)
        bot.register_next_step_handler(message_tempo_ht, registrar_tempo_ht)






def registrar_tempo_ht(message_tempo_ht):
    global usuario_tempo_inicial_ht
    global usuario_tempo_final_ht


    if message_tempo_ht.text in ['◀ Voltar']:
        #Init keyboard markup
        markup_cg_ft = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True) 
        markup_cg_ft.add('◀ Voltar')

        message_valor_cg_ft = bot.reply_to(message_valor_cg_ft, "🤖 Ok! Agora, Insira um Valor para o Total da Soma do CG para o FT(Segundo Tempo) ", reply_markup=markup_cg_ft)
        bot.register_next_step_handler(message_valor_cg_ft, registrar_cg_ft)


    else:
        markup_tempo_ft = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup_tempo_ft.add('◀ Voltar')

        usuario_tempo_inicial_ht = int(message_tempo_ht.text.split(',')[0])
        usuario_tempo_final_ht = int(message_tempo_ht.text.split(',')[1])
        print('TEMPO INICIAL HT = ', usuario_tempo_inicial_ht, 'TEMPO FINAL HT = ', usuario_tempo_final_ht)

        message_tempo_ft = bot.reply_to(message_tempo_ht, "🤖 Perfeito! Agora, Insira o Intervalo de Tempo Inicial e Final do FT(Segundo Tempo), Ex: 55,70 ", reply_markup=markup_tempo_ft)
        bot.register_next_step_handler(message_tempo_ft, registrar_tempo_ft)






def registrar_tempo_ft(message_tempo_ft):
    global usuario_tempo_inicial_ft
    global usuario_tempo_final_ft


    if message_tempo_ft.text in ['◀ Voltar']:
        #Init keyboard markup
        markup_tempo_ht = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True) 
        markup_tempo_ht.add('◀ Voltar')

        message_tempo_ht = bot.reply_to(message_tempo_ft, "🤖 Ok! Agora, Insira o Intervalo de Tempo Inicial e Final do HT(Primeiro Tempo), Ex: 25,40 ", reply_markup=markup_tempo_ht)
        bot.register_next_step_handler(message_tempo_ht, registrar_tempo_ht)


    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('✅ Ativar Bot', '⚙🧠 Cadastrar Estratégia', '📝🧠 Editar Estratégia', '🧠📜 Estratégia Cadastrada', '🛑 Pausar Bot')

        usuario_tempo_inicial_ft = int(message_tempo_ft.text.split(',')[0])
        usuario_tempo_final_ft = int(message_tempo_ft.text.split(',')[1])
        print('TEMPO INICIAL FT = ', usuario_tempo_inicial_ft, 'TEMPO FINAL FT = ', usuario_tempo_final_ft)

        message_final = bot.reply_to(message_tempo_ft, "🤖 Estratégia Cadastrada com Sucesso! ✅", reply_markup=markup)






def editar_campo_escolhido(message_editar_estrategia):
    global resposta_usuario

    if message_editar_estrategia.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('✅ Ativar Bot', '⚙🧠 Cadastrar Estratégia', '📝🧠 Editar Estratégia', '🧠📜 Estratégia Cadastrada', '🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_editar_estrategia, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        
        return
    

    else:
        resposta_usuario = message_editar_estrategia.text.split(' = ')

        #Init keyboard markup
        markup_novo_valor = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup_novo_valor.add('◀ Voltar')

        message_novo_valor = bot.reply_to(message_editar_estrategia, "🤖 Ok! Agora, Insira o Novo Valor ", reply_markup=markup_novo_valor)
        bot.register_next_step_handler(message_novo_valor, gravar_novo_valor)






def gravar_novo_valor(message_novo_valor):
    global usuario_appm, usuario_cg_ht, usuario_cg_ft, usuario_tempo_inicial_ht, usuario_tempo_final_ht, usuario_tempo_inicial_ft, usuario_tempo_final_ft

    if message_novo_valor.text in ['◀ Voltar']:
        #Add to buttons by list with ours generate_buttons function.
        markup_estrategia = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup_estrategia.add(f'APPM = {usuario_appm}',
                              f'CG|HT = {usuario_cg_ht}',
                              f'CG|FT = {usuario_cg_ft}',
                              f'TEMPO INICIAL HT = {usuario_tempo_inicial_ht}',
                              f'TEMPO FINAL HT = {usuario_tempo_final_ht}',
                              f'TEMPO INICIAL FT = {usuario_tempo_inicial_ft}',
                              f'TEMPO FINAL FT = {usuario_tempo_final_ft}',
                              '◀ Voltar')

        message_editar_estrategia = bot.reply_to(message, "🤖 Escolha Qual Condição da Estratégia Será Editada 👇", reply_markup=markup_estrategia)
        bot.register_next_step_handler(message_editar_estrategia, editar_campo_escolhido)



    if resposta_usuario[0] == 'APPM':
        usuario_appm = float(message_novo_valor.text)
    
    if resposta_usuario[0] == 'CG|HT':
        usuario_cg_ht = int(message_novo_valor.text)

    if resposta_usuario[0] == 'CG|FT':
        usuario_cg_ft = int(message_novo_valor.text)
    
    if resposta_usuario[0] == 'TEMPO INICIAL HT':
        usuario_tempo_inicial_ht = int(message_novo_valor.text)
    
    if resposta_usuario[0] == 'TEMPO FINAL HT':
        usuario_tempo_final_ht = int(message_novo_valor.text)

    if resposta_usuario[0] == 'TEMPO INICIAL FT':
        usuario_tempo_inicial_ft = int(message_novo_valor.text)

    if resposta_usuario[0] == 'TEMPO FINAL FT':
        usuario_tempo_final_ft = int(message_novo_valor.text)



    #Init keyboard markup
    markup_estrategia = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup_estrategia.add(f'APPM = {usuario_appm}',
                            f'CG|HT = {usuario_cg_ht}',
                            f'CG|FT = {usuario_cg_ft}',
                            f'TEMPO INICIAL HT = {usuario_tempo_inicial_ht}',
                            f'TEMPO FINAL HT = {usuario_tempo_final_ht}',
                            f'TEMPO INICIAL FT = {usuario_tempo_inicial_ft}',
                            f'TEMPO FINAL FT = {usuario_tempo_final_ft}',
                            '◀ Voltar')

    message_editar_estrategia = bot.reply_to(message_novo_valor, "🤖 Estratégia Editada com sucesso! ✅", reply_markup=markup_estrategia)
    bot.register_next_step_handler(message_editar_estrategia, editar_campo_escolhido)





bot.infinity_polling()