import pstats
from selenium import webdriver
import time
import warnings
from webdriver_manager.chrome import ChromeDriverManager
import logging
from datetime import datetime, timedelta
import telebot
from telegram.ext import *
from telebot import *
import operator
import mysql.connector
from mysql.connector import Error
import random



#_______________________________________________________________________#____________________________________________________________________________________________________

print()
print('                                #################################################################')
print('                                ######################   BOT JETX   #############################')
print('                                #################################################################')
print('                                ##################### SEJA BEM VINDO ############################')
print('                                #################################################################')
print('                                ############# DESENVOLVIDO POR VICTOR RODRIGUES #################')
print('                                #################################################################\n')
print('Versão = 1.0.0')
print('Ambiente: Produção\n\n\n')

    

def alimenta_banco_appData(lista_resultados):
    global lista_anterior
    '''banco de dados
    IP: 185.239.210.5
    User: u791277084_userjetx
    Pass: 1iV6LX1od!L
    DB: u791277084_basejetx
    Tabela: app_data (histórico dos jogos), app_game (resultados dos sinais)'''

    if lista_anterior == [] or lista_anterior != lista_resultados:

        vela_atual = lista_resultados[-1]

        try:
            ''' CONECTANDO COM O BANCO '''
            db_conexao = mysql.connector.connect(host='185.239.210.5', database='u791277084_basejetx', user='u791277084_userjetx', password='1iV6LX1od!L')

            #Variavel que executa as querys
            cursor = db_conexao.cursor()

            ''' QUERY '''
            query_inserir_dados = (f"""INSERT INTO u791277084_basejetx.app_data 
                                                                    VALUES(NULL, '{datetime.now()}', '{vela_atual}', NULL)""")

            cursor.execute(query_inserir_dados)
            db_conexao.commit()

            lista_anterior = lista_resultados

        except Exception as g:
            logger.error('Exception ocorrido na conexão com o banco MYSQL: ' + repr(g))
            pass





def alimenta_banco_appGame(lista_resultados, status):
    global vela_atual
    global lista_anterior
    '''banco de dados
    IP: 185.239.210.5
    User: u791277084_userjetx
    Pass: 1iV6LX1od!L
    DB: u791277084_basejetx
    Tabela: app_data (histórico dos jogos), app_game (resultados dos sinais)'''

    vela_atual = lista_resultados_sinal[-1]

    try:
        ''' CONECTANDO COM O BANCO '''
        db_conexao = mysql.connector.connect(host='185.239.210.5', database='u791277084_basejetx', user='u791277084_userjetx', password='1iV6LX1od!L')

        #Variavel que executa as querys
        cursor = db_conexao.cursor()

        ''' QUERY '''
        query_inserir_dados = (f"""INSERT INTO u791277084_basejetx.app_data 
                                                                VALUES( NULL,'{datetime.now()}', '{vela_atual}', '{status}' )""")

        cursor.execute(query_inserir_dados)
        db_conexao.commit()

        lista_anterior = lista_resultados

    except Exception as g:
        logger.error('Exception ocorrido na conexão com o banco MYSQL: ' + repr(g))
        pass





def inicio():
    global browser
    global logger
    global lista_anterior
    

    lista_anterior = []
    logger = logging.getLogger() #Log de erro
    
    # Definindo opções para o browser
    warnings.filterwarnings("ignore", category=DeprecationWarning) 
    chrome_options = webdriver.ChromeOptions() 
    chrome_options.add_argument("--disable-gpu")
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
    while True:

        #try:
        #    alimenta_banco_appData('x0.1x')
        #except:
        #    pass

        try:
            browser.get(r"https://m.playpix.com/pt")
            browser.maximize_window()
            time.sleep(10)
            
            try:
                ''' clicando no botao entrar ''' 
                browser.find_element_by_css_selector('.btn.sign-in').click()
                time.sleep(2)
                ''' inserindo credenciais '''
                browser.find_element_by_xpath('//*[@id="root"]/div[10]/div/div/div/div/div/div[2]/form/div[1]/div[3]/div/label/input').send_keys('brabin07')
                browser.find_element_by_xpath('//*[@id="root"]/div[10]/div/div/div/div/div/div[2]/form/div[1]/div[4]/div/label/input').send_keys('Playbraba5!')
                browser.find_element_by_css_selector('.btn.a-color').click()

            except:
                pass
            

            ''' ROLANDO A PAGINA '''
            browser.execute_script("window.scrollTo(0, 750)")

            ''' Entrando no Jogo JetX'''
            time.sleep(1)
            browser.find_element_by_xpath('//*[@alt="JetX"]').click()
            time.sleep(2)
            browser.find_element_by_xpath('//*[@title="Jogar"]').click()

            a = 0
            while a < 3:

                try:
                    ''' Acessando iframe do jogo'''
                    acessarIframe()
                    
                    '''TIRANDO O SOM '''
                    if browser.find_elements_by_css_selector('.sound-popup-content-buttons a.no'):
                        browser.find_element_by_css_selector('.sound-popup-content-buttons a.no').click() 

                    ''' CLICANDO NA ABA HISTORICOS '''
                    browser.find_element_by_xpath('//*[@id="footer-menu"]/a[2]').click()

                    break

                except:
                    time.sleep(3)
                    a+=1
                    continue
            
            if browser.find_elements_by_xpath('//*[@id="footer-menu"]/a[2]'):
                break
            
            else:
                continue
    

        except:
            continue


    



def acessarIframe():
    t=0
    while t < 5:
        try:
            iframe = browser.find_element_by_id('gameFrame')
            browser.switch_to.frame(iframe)

            time.sleep(1)
            
            iframe = browser.find_element_by_id('game-frame')
            browser.switch_to.frame(iframe)

            break
        
        except:
            time.sleep(5)
            t+=1





def enviarAlertaTelegram():
    global alerta_free
    global alerta_vip
    global contador_passagem


    mensagem_alerta = '‼ <b>Possível Entrada</b> ‼\n\n' + "🚀 <b>Acesse o <a href='https://m.playpix.com/pt/'>JetX</a></b>"

    ''' Enviando mensagem Telegram '''
    try:

        if canal_free != '':
            alerta_free = bot.send_message(canal_free, mensagem_alerta, parse_mode='HTML', disable_web_page_preview=True)
            
        if canal_vip !='':
            alerta_vip = bot.send_message(canal_vip, mensagem_alerta, parse_mode='HTML', disable_web_page_preview=True)

    except:
        pass

    contador_passagem = 1





def enviarSinalTelegram(vela_atual, cash_out):
    global alerta_free
    global alerta_vip
    global table_sinal
    global message_canal_free
    global message_canal_vip
    

    ''' Estruturando mensagem '''
    mensagem_sinal = '✅ <b>Entrada Confirmada</b> ✅\n' + '😎 <b>Entre após</b> '+vela_atual+'x\n' + '🏃🏻 <b>Saia em</b> '+ cash_out + '\n\n' + "🚀 <b>Acesse o <a href='https://m.playpix.com/pt/'>JetX</a></b>"

    try:
        # deletando o alerta
        # enviando sinal Telegram
        if canal_free != '':
            try:
                bot.delete_message(canal_free, alerta_free.message_id)
            except:
                pass
            message_canal_free = bot.send_message(canal_free, mensagem_sinal, parse_mode='HTML', disable_web_page_preview=True)

        if canal_vip !='':
            try:
                bot.delete_message(canal_vip, alerta_vip.message_id)
            except:
                pass
            message_canal_vip = bot.send_message(canal_vip, mensagem_sinal, parse_mode='HTML', disable_web_page_preview=True)

    except:
        pass





def apagaAlertaTelegram():
    global contador_passagem

    try:
        if canal_free != '':
            bot.delete_message(canal_free, alerta_free.message_id)

        if canal_vip !='':
            bot.delete_message(canal_vip, alerta_vip.message_id)

    except:
        pass

    contador_passagem = 0





def validadorEstrategia(estrategia, lista_resultados, sequencia_minima):
    # Validando se o resultado se encaixa na estratégia ( TRUE ou FALSE )
    validador = []
    try:
        for e in enumerate(estrategia[:-2]): 
            for v in enumerate(lista_resultados[int(-sequencia_minima):]):

                while v[0] == e[0]:
                    if '+' in e[1]:
                        resultado = operator.gt(float(v[1]), float(e[1][1:]))
                        validador.append(resultado)
                        break
                        
                    if '-' in e[1]:
                        resultado = operator.lt(float(v[1]), float(e[1][1:]))
                        validador.append(resultado)
                        break

                    else:
                        print('ERRO NA ESTRATÉGIA ', estrategia,'...VERIFIQUE O CADASTRO DA MESMA.')
                        time.sleep(3)
                        break


        print(f'Validador  --> {validador}')
        return validador
    except:
        pass





def coletarDados():
    global estrategia

    while True:

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass
        
        ''' VALIDANDO SE A VELA PAROU DE SUBIR '''
        #try:
        #    if browser.find_elements_by_css_selector('.random-points-icon'):
        #        pass
#
        #    else:
        #        logarSite()
#
        #except:
        #    logarSite()


        while True:
            try:
                lista_resultados = []
                # Pegando o histórico de resultados
                historico_velas = browser.find_elements_by_xpath('//*[@id="last100Spins"]/div')
                
                # Validando se foi solicitado o stop do BOT
                if parar != 0:
                    break
                else:
                    pass
                
                ''' Inserindo velas na lista'''
                try:
                    for vela in reversed(historico_velas[:20]):
                        numero = vela.text
                        lista_resultados.append(numero)
                except:
                    ''' CASO NÃO MAPEIE O RESULTADO, VERIFICAR SE ESTÁ LOGADO, SE TIVER, CONSULTAR RESULTADOS NOVAMENTE ''' 
                    if browser.find_elements_by_xpath('//*[@id="last100Spins"]/div'):
                        continue

                    else:
                        logarSite()
                        break

                if lista_resultados == []:
                    logarSite()
                    continue
                
                ''' ALIMENTANDO BANCO DE DADOS APP_DATA '''
                try:

                    alimenta_banco_appData(lista_resultados)

                except:
                    pass                

                ''' Chama a função que valida a estratégia para enviar o sinal Telegram '''
                validarEstrategia(lista_resultados, estrategias)   #Lista de estrategia

                print('=' * 100)
                lista_resultados = []
                break

                ''' Exceção se o cassino não estiver disponível '''
            except Exception as a:
                logger.error('Exception ocorrido na execução: ' + repr(a))
                if browser.find_elements_by_xpath('//*[@id="last100Spins"]/div'):
                    continue
                else:
                    logarSite()





def validarEstrategia(lista_resultados, estrategias):
    global cash_out
    global gale
    global vela_atual

    try:
        for estrategia in estrategias:

            # Validando se foi solicitado o stop do BOT
            if parar != 0:
                break
            else:
                pass


            print ('Analisando a Estrategia --> ', estrategia)
            sequencia_minima_alerta = len(estrategia[:-3])
            sequencia_minima_sinal = len(estrategia[:-2])
            cash_out = estrategia[-2]
            gale = estrategia[-1]
            print('Historico_Velas --> ', lista_resultados)

            ''' VALIDADOR DE ESTRATEGIA '''
            validador = validadorEstrategia(estrategia, lista_resultados, sequencia_minima_alerta)

            ''' Validando se bateu alguma condição'''
            if validador.count(True) == int(sequencia_minima_alerta):
                print('ENVIANDO ALERTA')
                enviarAlertaTelegram()


                ''' Verifica se a ultima condição bate com a estratégia para enviar sinal Telegram '''
                while True:
                    
                    ''' Lendo novos resultados para validação da estratégia'''
                    numeros_recentes_validacao = browser.find_elements_by_xpath('//*[@id="last100Spins"]/div')
                        
                    ''' LISTA DO PROXIMO RESULTADO APOS O ALERTA'''
                    lista_proximo_resultados = []
                    try:
                        for numeroRecente in reversed(numeros_recentes_validacao[:20]):
                            numero_r = numeroRecente.text
                            lista_proximo_resultados.append(numero_r)
                    except:
                        continue

                    ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
                    if lista_resultados != lista_proximo_resultados:
                        validador = validadorEstrategia(estrategia, lista_proximo_resultados, sequencia_minima_sinal)

                        ''' ALIMENTANDO O BANCO '''
                        alimenta_banco_appData(lista_proximo_resultados)

                        ''' VALIDA SE ENVIA SINAL OU APAGA O ALERTA '''
                        if validador.count(True) == int(sequencia_minima_sinal):
                            print(lista_proximo_resultados[-1])
                            print('ENVIA SINAL TELEGRAM')
                            print('=' * 100)
                            vela_atual = lista_proximo_resultados[-1]
                            enviarSinalTelegram(vela_atual, cash_out)
                            checkSinalEnviado(lista_proximo_resultados, estrategia)
                            time.sleep(1)
                            break


                        else:
                            print('APAGA SINAL DE ALERTA')
                            print('=' * 100)
                            apagaAlertaTelegram()
                            lista_resultados = lista_proximo_resultados
                            break
            
            else:
                print('=' * 100)


    except:
        pass





def checkSinalEnviado(lista_proximo_resultados, estrategia):
    global table
    global alerta_free
    global alerta_vip
    global message_canal_free
    global message_canal_vip
    global placar_win
    global placar_semGale
    global placar_gale1
    global placar_gale2
    global placar_gale3
    global placar_loss
    global resultados_sinais
    global ultimo_horario_resultado
    global validador_sinal
    global stop_loss
    global contador_passagem
    global lista_resultados_sinal
    global lista_resultados


    resultados = []
    contador_cash = 0

    while contador_cash <= int(gale):

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass


        try:
            ''' Lendo novos resultados para validação da estratégia'''
            numeros_recentes_validacao = browser.find_elements_by_xpath('//*[@id="last100Spins"]/div')

            lista_resultados_sinal = []
            try:
                for numeroRecente in reversed(numeros_recentes_validacao[:20]):
                    numero_r = numeroRecente.text
                    lista_resultados_sinal.append(numero_r)
            except:
                continue

            ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
            if lista_proximo_resultados != lista_resultados_sinal:
                
                print(lista_resultados_sinal[-1])

                # VALIDANDO WIN OU LOSS
                if float(lista_resultados_sinal[-1]) >= float(cash_out[:-1]):
                
                    # validando o tipo de WIN
                    if contador_cash == 0:
                        print('WIN SEM GALE')

                        ''' ADD RESULTADO NA LISTA DE RESULTADOS DO SINAL '''
                        resultados.append(f'<b>{lista_resultados_sinal[-1]}</b>')

                        ''' ALIMENTANDO BANCO DE DADOS'''
                        alimenta_banco_appGame(lista_resultados_sinal, 'SG')

                        # Preenchendo relatório
                        placar_win+=1
                        placar_semGale+=1
                        resultados_sinais = placar_win + placar_loss
                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                        try:
                            # Somando Win na estratégia da lista atual
                            for pe in placar_estrategias:
                                if pe[:-5] == estrategia:
                                    pe[-5] = int(pe[-5])+1
                        except:
                            pass
                        
                        
                    if contador_cash == 1:
                        print('WIN GALE1')

                        ''' ADD RESULTADO NA LISTA DE RESULTADOS DO SINAL '''
                        resultados.append(f'<b>{lista_resultados_sinal[-1]}</b>')

                        ''' ALIMENTANDO BANCO DE DADOS'''
                        alimenta_banco_appGame(lista_resultados_sinal, 'G1')

                        # Preenchendo relatório
                        placar_win+=1
                        placar_gale1+=1
                        resultados_sinais = placar_win + placar_loss
                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                        try:
                            # Somando Win na estratégia da lista atual
                            for pe in placar_estrategias:
                                if pe[:-5] == estrategia:
                                    pe[-4] = int(pe[-4])+1

                            
                        except:
                            pass


                    if contador_cash == 2:
                        print('WIN GALE2')
                        
                        ''' ADD RESULTADO NA LISTA DE RESULTADOS DO SINAL '''
                        resultados.append(f'<b>{lista_resultados_sinal[-1]}</b>') 

                        ''' ALIMENTANDO BANCO DE DADOS'''
                        alimenta_banco_appGame(lista_resultados_sinal, 'G2')
                        
                        # Preenchendo relatório
                        placar_win+=1
                        placar_gale2+=1
                        resultados_sinais = placar_win + placar_loss
                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)
                        
                        try:
                            # Somando Win na estratégia da lista atual
                            for pe in placar_estrategias:
                                    if pe[:-5] == estrategia:
                                        pe[-3] = int(pe[-3])+1
                        except:
                            pass
                        

                
                    if contador_cash == 3:
                        print('WIN gale3')

                        ''' ADD RESULTADO NA LISTA DE RESULTADOS DO SINAL '''
                        resultados.append(f'<b>{lista_resultados_sinal[-1]}</b>')

                        ''' ALIMENTANDO BANCO DE DADOS'''
                        alimenta_banco_appGame(lista_resultados_sinal, 'G3')

                        # Preenchendo relatório
                        placar_win+=1
                        placar_gale3+=1
                        resultados_sinais = placar_win + placar_loss
                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)
                        
                        try:
                            # Somando Win na estratégia da lista atual
                            for pe in placar_estrategias:
                                if pe[:-5] == estrategia:
                                    pe[-2] = int(pe[-2])+1
                            
                        except:
                            pass
    

                    # editando mensagem enviada
                    try:

                        wa = ['GREEEN', 'GREENZÃO', 'CHAAAMA NO GREEN']
                        green_aleatorio = random.choice(wa)
                        
                        if canal_free != '':
                            try:
                                bot.reply_to(message_canal_free, f'<b>{green_aleatorio}</b> ✅✅✅ ' + ' | '.join(resultados), parse_mode='HTML')
                                #bot.edit_message_text(table_sinal+"\n============================== \n        GREEN ✅ --- 🎯" + ' | '.join(resultados), message_canal_free.sender_chat.id, message_canal_free.message_id, parse_mode='HTML', disable_web_page_preview=True)   
                                #bot.send_sticker(canal_free, sticker=sticker_win)
                            except:
                                pass

                        if canal_vip != '':
                            bot.reply_to(message_canal_vip, f'<b>{green_aleatorio}</b> ✅✅✅ ' + ' | '.join(resultados), parse_mode='HTML')
                            #bot.edit_message_text(table_sinal+"\n============================== \n        GREEN ✅ --- 🎯" + ' | '.join(resultados), message_canal_vip.sender_chat.id, message_canal_vip.message_id, parse_mode='HTML', disable_web_page_preview=True)   
                            #bot.send_sticker(canal_vip, sticker=sticker_win)

                    except:
                        pass
                    

                    print('=' * 100)
                    validador_sinal = 0
                    contador_cash = 0
                    contador_passagem = 0
                    lista_resultados = lista_resultados_sinal
                    return

            

                else:
                    print('LOSSS')
                    ''' ADD RESULTADO NA LISTA DE RESULTADOS DO SINAL '''
                    resultados.append(lista_resultados_sinal[-1])
                    print('=' * 100)
                    contador_cash+=1

                    if contador_cash == 3:
                        pass
                    else:
                        alimenta_banco_appData(lista_resultados_sinal)

                    lista_proximo_resultados = lista_resultados_sinal
                    continue


        except:
            continue


    if contador_cash == 3:
        print('LOSSS GALE2')
        ''' ALIMENTANDO BANCO DE DADOS'''
        alimenta_banco_appGame(lista_resultados_sinal, 'LS')
        placar_loss +=1
        
        # editando mensagem e enviando sticker
        try:
           
            if canal_free !='':
                try:
                    bot.reply_to(message_canal_free, '<b>RED</b> 🥵 ' + ' | '.join(resultados), parse_mode = 'HTML')
                    #bot.edit_message_text(table_sinal+"\n============================== \n        RED ✖ --- " + ' | '.join(resultados), message_canal_free.sender_chat.id, message_canal_free.message_id, parse_mode='HTML', disable_web_page_preview=True)
                    #bot.send_sticker(canal_free, sticker=sticker_loss)
                    #bot.send_sticker(canal_free, sticker=sticker_analisando_mercado)
                except:
                    pass

            if canal_vip !='':
                bot.reply_to(message_canal_vip, '<b>RED</b> 🥵 ' + ' | '.join(resultados), parse_mode = 'HTML')
                #bot.edit_message_text(table_sinal+"\n============================== \n        RED ✖ --- " + ' | '.join(resultados), message_canal_vip.sender_chat.id, message_canal_vip.message_id, parse_mode='HTML', disable_web_page_preview=True)
                #bot.send_sticker(canal_vip, sticker=sticker_loss)
                #bot.send_sticker(canal_vip, sticker=sticker_analisando_mercado)

            # Preenchendo relatório
            resultados_sinais = placar_win + placar_loss
            print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
        
        except:
            pass

        ''' Alimentando "Gestão" estratégia e roleta '''
        try:
            # Somando Win na estratégia da lista atual
            for pe in placar_estrategias:
                if pe[:-5] == estrategia:
                    pe[-1] = int(pe[-1])+1
        
        except:
            pass

        

        print('=' * 100)
        validador_sinal = 0
        contador_cash = 0
        contador_passagem = 0
        lista_resultados = lista_resultados_sinal
        return






inicio()            # Difinição do webBrowser
logarSite()         # Logando no Site


#________________________________________________________________________________________ TELEGRAM__________________________________________________________________________________#

print('\n\n')
print('####################################### AGUARDANDO COMANDOS #######################################')

global canal




# PLACAR
placar_win = 0
placar_semGale= 0
placar_gale1= 0
placar_gale2= 0
placar_gale3= 0
placar_loss = 0
resultados_sinais = placar_win + placar_loss
estrategias = []
placar_estrategias = []
estrategias_diaria = []
placar_estrategias_diaria = []
contador = 0
contador_passagem = 0
botStatus = 0
lista_ids = []


# LENDO TXT PARA DEFINIR VARIAVEL FREE E VIP E VALIDAÇÃO DE USUÁRIO
txt = open("canais.txt", "r")
free = txt.readlines(1)
vip = txt.readlines(2)
ids = txt.readlines(3)

for canal in free:
    free = canal.split(' ')
    free = int(free[1])
    

for canal in vip:
    vip = canal.split(' ')
    vip = int(vip[1])


for id in ids:
    id_usuario = id.replace('\n','').split(' ')
    id_usuario = id_usuario[1]


''' TOKEN BOT '''
txt = open("canais.txt", "r", encoding="utf-8")
arquivo = txt.readlines()
CHAVE_API = arquivo[3].split(' ')[1].split('\n')[0]
bot = telebot.TeleBot(CHAVE_API)


######################################################


global message


def generate_buttons_estrategias(bts_names, markup):
    for button in bts_names:
        markup.add(types.KeyboardButton(button))
    return markup



def pausarBot():
     while True:
        try:
            global parar
            global browser
            parar = 1
            time.sleep(1)
            break

        except:
            continue



@bot.message_handler(commands=['⚙ Cadastrar_Estratégia'])
def cadastrarEstrategia(message):

    global contador_passagem

    if contador_passagem == 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('◀ Voltar')

        message_estrategia = bot.reply_to(message, "🤖 Ok! Escolha um padrão acima ou abaixo de velas, a vela que deverá fazer CASH OUT e uma opção de GALE \n\n Ex: +1,-2,-10.35,1.5X,1", reply_markup=markup)
        bot.register_next_step_handler(message_estrategia, registrarEstrategia)
    
    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_estrategia = bot.reply_to(message, "🤖⛔ Estou validando uma estratégia! Tente novamente em alguns instanstes.", reply_markup=markup)



@bot.message_handler(commands=['🗑 Apagar_Estratégia'])
def apagarEstrategia(message):
    global estrategia
    global estrategias
    global contador_passagem

    print('Excluir estrategia')

    if contador_passagem == 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        #Add to buttons by list with ours generate_buttons function.
        markup_estrategias = generate_buttons_estrategias([f'{estrategia}' for estrategia in estrategias], markup)
        markup_estrategias.add('◀ Voltar')   


        message_excluir_estrategia = bot.reply_to(message, "🤖 Escolha a estratégia a ser excluída 👇", reply_markup=markup_estrategias)
        bot.register_next_step_handler(message_excluir_estrategia, registrarEstrategiaExcluida)
    
    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_excluir_estrategia = bot.reply_to(message, "🤖⛔ Estou validando uma estratégia! Tente novamente em alguns instanstes.", reply_markup=markup)



@bot.message_handler(commands=['📜 Estrategias_Cadastradas'])
def estrategiasCadastradas(message):
    global estrategia
    global estrategias

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    bot.reply_to(message, "🤖 Ok! Listando estratégias", reply_markup=markup)

    for estrategia in estrategias:
        #print(estrategia)
        bot.send_message(message.chat.id, f'{estrategia}')




@bot.message_handler(commands=['📊 Placar Atual'])
def placar_atual(message):
    global placar
    global resultados_sinais

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    try:
        placar = bot.reply_to(message,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", reply_markup=markup)
    except Exception as a:
        logger.error('Exception ocorrido no ' + repr(a))
        placar = bot.reply_to(message,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%", reply_markup=markup)




@bot.message_handler(commands=['♻ Resetar Resultados'])
def resetarResultados(message):
    global placar_win
    global placar_semGale
    global placar_gale1
    global placar_gale2
    global placar_gale3
    global placar_loss
    global placar
    global resultados_sinais
    global placar_estrategias

    # Resetando placar Geral (placar geral)
    placar_win = 0
    placar_semGale= 0
    placar_gale1= 0
    placar_gale2= 0
    placar_gale3= 0
    placar_loss = 0

    # Resetando placar das estrategias (Gestão)
    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    for pe in placar_estrategias:
        pe[-5], pe[-4], pe[-3], pe[-2], pe[-1] = 0,0,0,0,0
        assertividade = '0%'
    
    message_final = bot.reply_to(message, "🤖♻ Resultados resetados com sucesso ✅", reply_markup=markup)




@bot.message_handler(commands=['📈 Gestão'])
def gestao(message):
    global placar
    global resultados_sinais
    global placar_estrategias

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    
    for pe in placar_estrategias:
        total = int(pe[-5]) + int(pe[-4]) + int(pe[-3]) + int(pe[-2]) + int(pe[-1])
        soma_win = int(pe[-5]) + int(pe[-4]) + int(pe[-3]) + int(pe[-2])

        try:
            assertividade = str(round(soma_win / total*100, 1)).replace('.0',"")+"%"
        except:
            assertividade = '0%'

        bot.send_message(message.chat.id, f'🧠 {pe[:-5]} \n==========================\n 🏆= {pe[-5]}  |  🥇= {pe[-4]}  |  🥈= {pe[-3]}  |  🥉= {pe[-2]} \n\n ✅ - {soma_win} \n ❌ - {pe[-1]} \n==========================\n 🎯 {assertividade}  ', reply_markup=markup)
        
        #print(f'🧠 {pe[:-5]} \n==========================\n 🏆= {pe[-5]}  |  🥇= {pe[-4]}  |  🥈= {pe[-3]}  |  🥉= {pe[-2]} \n\n ✅ - {soma_win} \n ❌ - {pe[-1]} \n==========================\n 🎯 {assertividade}'
        #)

    


@bot.message_handler(commands=['🛑 Pausar_bot'])
def pausar(message):
    global botStatus
    global contador_passagem
    global parar

    if contador_passagem != 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_excluir_estrategia = bot.reply_to(message, "🤖⛔ Estou validando uma estratégia! Tente novamente em alguns instanstes.", reply_markup=markup)

    elif botStatus == 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Bot já está pausado ", reply_markup=markup)

    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        print('\n\n')
        print('Comando: Parar BOT')
        print('Parando o BOT....\n')
        botStatus = 0
        parar += 1
        #pausarBot()

        print('###################### AGUARDANDO COMANDOS ######################')

        message_final = bot.reply_to(message, "🤖 Ok! Bot pausado 🛑", reply_markup=markup)



@bot.message_handler(commands=['start'])
def start(message):

    if str(message.chat.id) in id_usuario:

        ''' Add id na lista de ids'''
        if str(message.chat.id) not in lista_ids:
            lista_ids.append(message.chat.id)
        else:
            pass
       

        #Add to buttons by list with ours generate_buttons function.
        #markup = generate_buttons(['/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','📊 Placar Atual','❌ Pausar Bot'], markup)
        
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message, "🤖 Bot JetX Iniciado! ✅ Escolha uma opção 👇",
                                reply_markup=markup)
        
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(message_opcoes, opcoes)
    
    else:
        message_error = bot.reply_to(message, "🤖 Você não tem permissão para acessar este Bot ❌🚫")




@bot.message_handler()
def opcoes(message_opcoes):

    if message_opcoes.text in ['⚙ Cadastrar Estratégia']:
        print('Cadastrar Estrategia')

        cadastrarEstrategia(message_opcoes)


    if message_opcoes.text in['📜 Estratégias Cadastradas']:
        print('Estrategias Cadastradas')
        estrategiasCadastradas(message_opcoes)


    if message_opcoes.text in ['🗑 Apagar Estratégia']:
        print('Apagar estrategia')
        apagarEstrategia(message_opcoes)



    if message_opcoes.text in ['✅ Ativar Bot']:
        global botStatus

        print('Ativar Bot')

        if botStatus == 1:

            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖⛔ Bot já está ativado",
                                reply_markup=markup)

        elif estrategias == []:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖⛔ Cadastre no mínimo 1 estratégia antes de iniciar",
                                reply_markup=markup)
        
        else:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            markup = markup.add('◀ Voltar', '🆓 Enviar sinais Canal FREE', '🏆 Enviar sinais Canal VIP', '🆓🏆 Enviar sinais Canal FREE & VIP')

            message_canal = bot.reply_to(message_opcoes, "🤖 Escolha para onde enviar os sinais 👇",
                                    reply_markup=markup)
            
            bot.register_next_step_handler(message_canal, escolher_canal)

    
    if message_opcoes.text in['📊 Placar Atual']:
        print('Placar Atual')
        placar_atual(message_opcoes)



    if message_opcoes.text in ['♻ Resetar Resultados']:
        print('Resetar Resultados')
        resetarResultados(message_opcoes)



    if message_opcoes.text in['📈 Gestão']:
        print('Gestão')
        gestao(message_opcoes)


    if message_opcoes.text in ['🛑 Pausar Bot']:
        print('Pausar Bot')
        pausar(message_opcoes)
    



@bot.message_handler(content_types=['text'])
def escolher_canal(message_canal):
    global canal_free
    global canal_vip
    global canal_adm
    global placar
    global estrategia
    global stop_loss
    global botStatus
    global vela_anterior
    global reladiarioenviado
    global parar
    global enviar_sinais_free


    if message_canal.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_canal, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)


    if message_canal.text in ['🆓 Enviar sinais Canal FREE']:

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_final = bot.reply_to(message_canal, "🤖 Ok! Ligando Bot nas configurações:\n===============================\n" + "Canal: "+ str(message_canal.text.split(' ')[4:]) + '\n Estratégia(s): \n' + str([f'{estrategia}' for estrategia in estrategias]), reply_markup = markup)
        
        print("Iniciar e enviar sinais no Canal FREE ")


        canal_free = free
        canal_vip = ''
        stop_loss = []
        botStatus = 1
        vela_anterior = 0
        reladiarioenviado = 0
        parar = 0
        enviar_sinais_free = 0

        ''' ALIMENTA BANCO DE DADOS '''
        #alimenta_banco_appData('0.1')

        placar = bot.send_message(message_canal.chat.id,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%")

        print('######################### ANALISANDO AS ESTRATÉGIAS CADASTRADAS  #########################')
        print()

        coletarDados()
    

    if message_canal.text in ['🏆 Enviar sinais Canal VIP']:
        
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_final = bot.reply_to(message_canal, "🤖 Ok! Ligando Bot nas configurações:\n===============================\n" + "Canal: "+ str(message_canal.text.split(' ')[4:]) + '\n Estratégia(s): \n' + str([f'{estrategia}' for estrategia in estrategias]), reply_markup = markup)
        
        print("Iniciar e enviar sinais no Canal VIP ")

        canal_free = ''
        canal_vip = vip
        stop_loss = []
        botStatus = 1
        vela_anterior = 0
        reladiarioenviado = 0
        parar = 0
        enviar_sinais_free = 0

        ''' ALIMENTA BANCO DE DADOS '''
        #alimenta_banco_appData('0.1')

        placar = bot.send_message(message_canal.chat.id,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%")

        print('######################### ANALISANDO AS ESTRATÉGIAS CADASTRADAS  #########################')
        print()

        coletarDados()


    if message_canal.text in ['🆓🏆 Enviar sinais Canal FREE & VIP']:
        
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_final = bot.reply_to(message_canal, "🤖 Ok! Ligando Bot nas configurações:\n===============================\n" + "Canal: "+ str(message_canal.text.split(' ')[4:]) + '\n Estratégia(s): \n' + str([f'{estrategia}' for estrategia in estrategias]), reply_markup = markup)
        
        print("Iniciar e enviar sinais no Canal VIP & ADM ")

        canal_free = free
        canal_vip = vip
        stop_loss = []
        botStatus = 1
        vela_anterior = 0
        reladiarioenviado = 0
        parar = 0
        enviar_sinais_free = 0

        ''' ALIMENTA BANCO DE DADOS '''
        #alimenta_banco_appData('0.1')

        placar = bot.send_message(message_canal.chat.id,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%")

        print('######################### ANALISANDO AS ESTRATÉGIAS CADASTRADAS  #########################')
        print()

        coletarDados()


    

@bot.message_handler()
def registrarEstrategia(message_estrategia):
    global estrategia
    global estrategias
    global placar_estrategia
    global placar_estrategias
    global placar_estrategias_diaria
    global estrategias_diaria

    if message_estrategia.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_estrategia, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        return

    
    estrategia = message_estrategia.text
    placar_estrategia = message_estrategia.text
    
    estrategia = estrategia.split(',')
    placar_estrategia = placar_estrategia.split(',')

    placar_estrategia.extend([0,0,0,0,0])

    # Adicionando estratégia atual
    estrategias.append(estrategia)
    placar_estrategias.append(placar_estrategia)

    # Acumulando estratégia do dia
    estrategias_diaria.append(estrategia)
    placar_estrategias_diaria.append(placar_estrategia)


    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    bot.reply_to(message_estrategia, "🤖 Estratégia cadastrada com sucesso! ✅", reply_markup=markup)





def registrarEstrategiaExcluida(message_excluir_estrategia):
    global estrategia
    global estrategias

    if message_excluir_estrategia.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_excluir_estrategia, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        return
    
    estrategia_excluir = message_excluir_estrategia.text
    
    for estrategia in estrategias:
        if estrategia_excluir == str(estrategia):
            estrategias.remove(estrategia)

    
    for pe in placar_estrategias:
        if estrategia_excluir == str(pe[:-5]):
            placar_estrategias.remove(pe)


    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    bot.reply_to(message_excluir_estrategia, "🤖 Estratégia excluída com sucesso! ✅", reply_markup=markup)





bot.infinity_polling()






