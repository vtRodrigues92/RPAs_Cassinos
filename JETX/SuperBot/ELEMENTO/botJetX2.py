from selenium import webdriver
import time
import warnings
from webdriver_manager.chrome import ChromeDriverManager
import logging
from datetime import datetime, timedelta
#from columnar import columnar
import telebot
from telegram.ext import *
from telebot import *
import operator



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





def enviarMensagemInicial():

    sticker_bomdia = 'CAACAgEAAxkBAAEZNeljUb4K7DScTpyazJyHEyYQfayZPAACGwEAAiOsQEdOdQcRWtPpiSoE'
    sticker_boatarde = 'CAACAgEAAxkBAAEZNfNjUb59H5J_raAHCHtAqXcWwC3eNgACYgEAAknIQEfrrW2_MWvXgCoE'
    sticker_boanoite = 'CAACAgEAAxkBAAEZNgtjUcbEqvfy7Z9rVP-aAAKwtQ4OYQACXwEAAj2jOEe9IRhLA4HPtCoE'
    sticker_paunamaquina = 'CAACAgEAAxkBAAEZQ05jVEqd-osGOqAnVyOHbm9fO8_tAgACEwEAAjcaOUePJ8C8DOk-CSoE'

    txt = open("config-mensagens.txt", "r", encoding="utf-8")
    mensagem = txt.readlines()
    

    if horario_atual > '00:00' and horario_atual <= '12:00':
        bot.send_sticker(canal_free, sticker=sticker_bomdia)

    if horario_atual > '12:00' and horario_atual <= '18:00':
        bot.send_sticker(canal_free, sticker=sticker_boatarde)

    if horario_atual > '18:00' and horario_atual <= '23:59':
        bot.send_sticker(canal_free, sticker=sticker_boanoite)

    bot.send_message(canal_free, mensagem[28] + mensagem[29] + mensagem[30] + mensagem[31] + mensagem[32] + mensagem[33] + mensagem[34] + mensagem[35] + mensagem[36] + mensagem[37] + mensagem[38] + mensagem[39], parse_mode='HTML', disable_web_page_preview=True)
    bot.send_video(canal_free, video=open('videoaula.mp4', 'rb'), supports_streaming=True)
    bot.send_message(canal_free, mensagem[42] + mensagem[43] + mensagem[44] + mensagem[45] + mensagem[46] + mensagem[47] + mensagem[48] + mensagem[49] + mensagem[50] + mensagem[51] + mensagem[52] + mensagem[53] + mensagem[54] + mensagem[55] +mensagem[56] + mensagem[57] + mensagem[58] + mensagem[59], parse_mode='HTML', disable_web_page_preview=True)
    bot.send_sticker(canal_free, sticker=sticker_paunamaquina)
    bot.send_sticker(canal_free, sticker=sticker_analisando_mercado)



    

# RELATÓRIO DIÁRIO
def relaDiario():
    global placar
    global resultados_sinais
    global placar_estrategias_diaria
    global data_resultado
    global placar_win
    global placar_semGale
    global placar_gale1
    global placar_gale2
    global placar_gale3
    global placar_loss


    
    # PLACAR CONSOLIDADO
    try:
        placar_1 = bot.send_message(5212321500,"📊 Resultados do dia "+data_resultado+"\n=========================\n")
        placar_2 = bot.send_message(5212321500,"😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%")

    except Exception as a:
        logger.error('Exception ocorrido no ' + repr(a))
        placar_1 = bot.send_message(5212321500,"📊 Resultados do dia "+data_resultado+"\n=========================\n")
        placar_2 = bot.send_message(5212321500,"😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%")


    # PLACAR POR ESTRATEGIA
    for pe in placar_estrategias_diaria:
        total = int(pe[-5]) + int(pe[-4]) + int(pe[-3]) + int(pe[-2]) + int(pe[-1])
        soma_win = int(pe[-5]) + int(pe[-4]) + int(pe[-3]) + int(pe[-2])

        try:
            assertividade = str(round(soma_win / total*100, 1)).replace('.0',"")+"%"
        except:
            assertividade = '0%'

        bot.send_message(5212321500, f'🧠 {pe[:-5]} \n==========================\n 🏆= {pe[-5]}  |  🥇= {pe[-4]}  |  🥈= {pe[-3]}  |  🥉= {pe[-2]} \n\n ✅ - {soma_win} \n ❌ - {pe[-1]} \n==========================\n 🎯 {assertividade}')
        

    # ZERANDO PLACAR E ATUALIZANDO A LISTA DE ESTRATEGIAS DIARIAS
    # Resetando placar Geral (placar geral) e lista de estratégia diária
    placar_win = 0
    placar_semGale= 0
    placar_gale1= 0
    placar_gale2= 0
    placar_gale3= 0
    placar_loss = 0
    placar_estrategias_diaria = []
    estrategias_diaria = []


    # Resetando placar das estrategias (Gestão)
    for pe in placar_estrategias:
        pe[-5], pe[-4], pe[-3], pe[-2], pe[-1] = 0,0,0,0,0
        assertividade = '0%'
        placar_estrategias_diaria.append(pe) # Atualizando o placar das estratégias diária
    

    # Atualizando as estratégias diárias com as estratégias atuais
    for e in estrategias:
        estrategias_diaria.append(e)




# VALIDADOR DE DATA
def validaData():
    global data_resultado
    global reladiarioenviado
    global horario_atual
    global enviar_sinais_free

    txt = open("canais.txt", "r", encoding="utf-8")
    arquivo = txt.readlines()

    txt = open("config-mensagens.txt", "r", encoding="utf-8")
    mensagem = txt.readlines()


    ativar_sinais_free = ativar_sinais_free = arquivo[6].replace('LIGAR = ','').replace('\n','').split(',')
    desativar_sinais_free = arquivo[7].replace('DESLIGAR = ','').replace('\n','').split(',')

    data_hoje = datetime.today()
    subtrai_dia = timedelta(days=-1)
    data_ontem = data_hoje + subtrai_dia
    data_resultado = data_ontem.strftime('%d/%m/%Y')
    horario_atual = datetime.today().strftime('%H:%M')

    if horario_atual == '00:00' and reladiarioenviado == 0:
        relaDiario()
        reladiarioenviado +=1

    
    if horario_atual == '00:01' and reladiarioenviado == 1:
        reladiarioenviado = 0

    
    if horario_atual in ativar_sinais_free and enviar_sinais_free == 0:
        enviar_sinais_free = 1
        print('LIGANDO BOT NO CANAL FREE')
        enviarMensagemInicial()
    

    if horario_atual in desativar_sinais_free and enviar_sinais_free == 1:
        enviar_sinais_free = 0
        print('DESLIGANDO BOT NO CANAL FREE')

        ''' EXCLUINDO MENSAGENS DE ALERTA OU SINAL ENVIADO ANTES DO DESLIGAMENTO'''
        try:
            bot.delete_message(canal_free, alerta_free.message_id)
        except:
            try:
                bot.delete_message(canal_free, message_canal_free.message_id)
            except:
                pass

        #mensagem[0].replace('\n','') + '\n' + mensagem[1].replace('\n','') + '\n' + mensagem[2].replace('\n','')
        bot.send_message(canal_free, mensagem[0] + mensagem[1] + mensagem[2], parse_mode='HTML')
        #mensagem[5].replace('\n','') + '\n' + mensagem[6].replace('\n','') + '\n' + mensagem[7].replace('\n','') + '\n' + mensagem[8].replace('\n','') + '\n' + mensagem[9].replace('\n','')
        bot.send_message(canal_free, mensagem[5] + mensagem[6] + mensagem[7] + mensagem[8] + mensagem[9], parse_mode='HTML')
        bot.send_message(canal_free, mensagem[12] + mensagem[13] + mensagem[14] + mensagem[15] + mensagem[16] + mensagem[17] + mensagem[18] + mensagem[19] + mensagem[20] + mensagem[21] + mensagem[22] + mensagem[23] + mensagem[24], parse_mode='HTML')




def inicio():
    global browser
    global vermelho
    global verde
    global logger
    global sticker_analisando_mercado
    global sticker_win
    global sticker_loss


    sticker_analisando_mercado = 'CAACAgEAAxkBAAEZLdNjUI2MLFv8oXPCRnOHTCrNPZld6AAC6AEAAu9iQEcdP6tgwPFxGCoE'
    sticker_win = 'CAACAgEAAxkBAAEZLddjUI3nEuteSzgmijam0ICZVIQjogACawEAApB-OEd7mbO0uHFqTioE'
    sticker_loss = 'CAACAgEAAxkBAAEZLdtjUI4f20oeZztHyxOy0ZbIafGqUQACxgADWw45R4wfFmxZUfh4KgQ'

    logger = logging.getLogger() #Log de erro
    # CORES
    vermelho = '#ff2f2f'
    verde = '#4ec520'

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


'https://1wlgur.top/bets/home'
'https://1wlgur.top/casino/play/mrslotty_smartsoft-jetx'

#https://eu-server.ssgportal.com/JetX/JetX/Loader.aspx?Gametype=&GameName=JetX&StartPage=Board&Token=2dca704c-783a-4211-a578-0c4f969543f7&Lang=pt&ReturnURL=https%3A%2F%2F1wlgur.top%2Fcasino&Skin=

#robodojetx@gmail.com
#Robozinho

def logarSite():
    while True:
        try:

            #browser.get(r"https://1wlgur.top/casino/")
            #time.sleep(10)
            
            browser.get(r"https://1wlgur.top/bets/home")
            browser.maximize_window()
            time.sleep(10)
            #
            
            #input(' INSIRA O LOGIN E SENHA, DEPOIS APERTE ENTER PARA CONTINUAR ----> ')
            
            usuario = 'robodojetx@gmail.com'
            senha = 'Robozinho'
        #   
            try:
                ''' Mapeando elementos para inserir credenciais '''
                browser.find_element_by_css_selector('.button.secondary').click() #Clicando no botão Entrar
                time.sleep(3)
                browser.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[2]/div[1]/div/div[2]/div/div/form/div[3]/div[1]/div/div/input').send_keys(usuario) #Inserindo login
                time.sleep(3)
                browser.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[2]/div[1]/div/div[2]/div/div/form/div[3]/div[2]/div/div[1]/input').send_keys(senha) #Inserindo senha
                time.sleep(3)
                browser.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[2]/div[1]/div/div[2]/div/div/form/div[5]/button').click() #Clicando no btn login
                time.sleep(3)
                #
                ''' Verificando se o login foi feito com sucesso'''
                t3 = 0
                while t3 < 20:
                    if browser.find_elements_by_css_selector('.header-balance__value[data-v-76c10270]'):
                        break
                    else:
                        time.sleep(3)
                        t3+=1
            
            except:
                pass
        #
#
#
            ''' Entrando no ambiente '''
            browser.get(r"https://1wlgur.top/casino/play/mrslotty_smartsoft-jetx")
            time.sleep(10)
            iframe = browser.find_element_by_xpath('//*[@id="casino"]/main/div/div/div[2]/div/iframe')
            link_tela_cheia = iframe.get_attribute('src')
            browser.get(link_tela_cheia)
            time.sleep(10)

            ''' Acessando iframe do jogo'''
            acessarIframe()
            break


        except:
            continue


def acessarIframe():
    t=0
    while t < 10:
        try:
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


    headers_alerta = ['⚠️ ATENÇÃO, POSSÍVEL SINAL ⚠️']
    data_alerta = [

        ["<a href='https://1wlgur.top/'>Aposte aqui: JETX</a>"],
        ['Aguarde confirmação']

    ]

    table_alerta = '⚠️ ATENÇÃO, POSSÍVEL SINAL ⚠️'+'\n\n'+\
                   "<a href='https://1wlgur.top/'>Aposte aqui: JETX</a>"+'\n'\
                   'Aguarde confirmação'

    ''' Enviando mensagem Telegram '''
    try:

        if canal_free != '' and enviar_sinais_free == 1:
            alerta_free = bot.send_message(canal_free, table_alerta, parse_mode='HTML', disable_web_page_preview=True)
            
        if canal_vip !='':
            alerta_vip = bot.send_message(canal_vip, table_alerta, parse_mode='HTML', disable_web_page_preview=True)

    except:
        pass


def enviarSinalTelegram(vela_atual, cash_out):
    global alerta_free
    global alerta_vip
    global table_sinal
    global message_canal_free
    global message_canal_vip
    

    ''' Estruturando mensagem '''
    table_sinal = '🚀  ENTRADA CONFIRMADA 🚀'+'\n\n'+\
                  '👉 Entrar após: '+vela_atual+'x'+'\n'+\
                  '🏃🏻 Sair em: '+ cash_out +'\n'+\
                  "🖥 <a href='https://1wlgur.top/'>APOSTE AQUI</a>"


    try:
        # deletando o alerta
        # enviando sinal Telegram
        if canal_free != '' and enviar_sinais_free == 1:
            try:
                bot.delete_message(canal_free, alerta_free.message_id)
            except:
                pass
            message_canal_free = bot.send_message(canal_free, table_sinal, parse_mode='HTML', disable_web_page_preview=True)

        if canal_vip !='':
            try:
                bot.delete_message(canal_vip, alerta_vip.message_id)
            except:
                pass
            message_canal_vip = bot.send_message(canal_vip, table_sinal, parse_mode='HTML', disable_web_page_preview=True)

    except:
        pass


def apagaAlertaTelegram():
    global contador_passagem

    try:
        if canal_free != '' and enviar_sinais_free == 1:
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
    global gale
    global cash_out
    global estrategia

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
                lista_resultados = []
                # Pegando o histórico de resultados
                historico_velas = browser.find_elements_by_css_selector('aside#left .history .row')
                
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
                    if browser.find_elements_by_css_selector('aside#left .history .row'):
                        continue

                    else:
                        logarSite()
                        break
                        


                ''' VALIDA SE BATER A ESTRATEGIA FORA DA LISTA '''
                if lista_resultados[-1] == '1.09' or lista_resultados[-1] == '1.19' or lista_resultados[-1] == '1.49':
                    print('ESTRATEGIA SECRETA! ENVIANDO SINAL TELEGRAM')
                    estrategia = ['ESTRATÉGIA EXTRA']
                    gale = 2
                    cash_out = '1.5x'
                    enviarSinalTelegram(lista_resultados[-1], '1.5')
                    checkSinalEnviado(lista_resultados, estrategia)
                    time.sleep(1)
                    continue

                ''' Chama a função que valida a estratégia para enviar o sinal Telegram '''
                validarEstrategia(lista_resultados, estrategias)   #Lista de estrategia

                print('=' * 220)
                lista_resultados = []
                break

                ''' Exceção se o cassino não estiver disponível'''
            except:
                if browser.find_elements_by_css_selector('aside#left .history .row'):
                    continue
                else:
                    logarSite()


def validarEstrategia(lista_resultados, estrategias):
    global cash_out
    global gale
    global vela_atual

    try:
        for estrategia in estrategias:

            if estrategia == ['ESTRATÉGIA EXTRA']:
                continue
            
            # Validando se foi solicitado o stop do BOT
            if parar != 0:
                break
            else:
                pass

            # Validando o horario para envio do relatório diário
            validaData()

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
                    numeros_recentes_validacao = browser.find_elements_by_css_selector('aside#left .history .row')
                        
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

                        if validador.count(True) == int(sequencia_minima_sinal):
                            print(lista_proximo_resultados[-1])
                            print('ENVIA SINAL TELEGRAM')
                            vela_atual = lista_proximo_resultados[-1]
                            enviarSinalTelegram(vela_atual, cash_out)
                            checkSinalEnviado(lista_proximo_resultados, estrategia)
                            time.sleep(1)
                            break


                        else:
                            print('APAGA SINAL DE ALERTA')
                            apagaAlertaTelegram()
                            lista_resultados = lista_proximo_resultados
                            break
            
            else:
                print('=' * 220)


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

        # Validando o horario para envio do relatório diário
        validaData()

        try:
            ''' Lendo novos resultados para validação da estratégia'''
            numeros_recentes_validacao = browser.find_elements_by_css_selector('aside#left .history .row')

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
                resultados.append(lista_resultados_sinal[-1]+'x')

                # VALIDANDO WIN OU LOSS
                if float(lista_resultados_sinal[-1]) >= float(cash_out[:-1]):
                
                    # validando o tipo de WIN
                    if contador_cash == 0:
                        print('WIN SEM GALE')
                        stop_loss.append('win')

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
                        stop_loss.append('win')

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
                        stop_loss.append('win')
                        
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
                        stop_loss.append('win')

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
                        
                        if canal_free != '' and enviar_sinais_free == 1:
                            try:
                                bot.reply_to(message_canal_free, '✅✅✅✅ GREEN ✅✅✅✅' + '\n🎯' + ' | '.join(resultados), parse_mode='HTML')
                                #bot.edit_message_text(table_sinal+"\n============================== \n        GREEN ✅ --- 🎯" + ' | '.join(resultados), message_canal_free.sender_chat.id, message_canal_free.message_id, parse_mode='HTML', disable_web_page_preview=True)   
                                bot.send_sticker(canal_free, sticker=sticker_win)
                            except:
                                pass

                        if canal_vip != '':
                            bot.reply_to(message_canal_vip, '✅✅✅✅ GREEN ✅✅✅✅' + '\n🎯' + ' | '.join(resultados), parse_mode='HTML')
                            #bot.edit_message_text(table_sinal+"\n============================== \n        GREEN ✅ --- 🎯" + ' | '.join(resultados), message_canal_vip.sender_chat.id, message_canal_vip.message_id, parse_mode='HTML', disable_web_page_preview=True)   
                            bot.send_sticker(canal_vip, sticker=sticker_win)

                    except:
                        pass
                    

                    print('==================================================')
                    validador_sinal = 0
                    contador_cash = 0
                    contador_passagem = 0
                    lista_resultados = lista_resultados_sinal
                    return

            

                else:
                    print('LOSSS')
                    print('==================================================')
                    contador_cash+=1
                    lista_proximo_resultados = lista_resultados_sinal
                    continue


        except:
            continue


    if contador_cash == 3:
        print('LOSSS GALE2')
        placar_loss +=1
        stop_loss.append('loss')
        
        # editando mensagem e enviando sticker
        try:
           
            if canal_free !='' and enviar_sinais_free == 1:
                try:
                    bot.reply_to(message_canal_free, '🔻🔻🔻 RED 🔻🔻🔻' + '\n🎯' + ' | '.join(resultados), parse_mode = 'HTML')
                    #bot.edit_message_text(table_sinal+"\n============================== \n        RED ✖ --- " + ' | '.join(resultados), message_canal_free.sender_chat.id, message_canal_free.message_id, parse_mode='HTML', disable_web_page_preview=True)
                    bot.send_sticker(canal_free, sticker=sticker_loss)
                    bot.send_sticker(canal_free, sticker=sticker_analisando_mercado)
                except:
                    pass

            if canal_vip !='':
                bot.reply_to(message_canal_vip, '🔻🔻🔻 RED 🔻🔻🔻' + '\n🎯' + ' | '.join(resultados), parse_mode='HTML')
                #bot.edit_message_text(table_sinal+"\n============================== \n        RED ✖ --- " + ' | '.join(resultados), message_canal_vip.sender_chat.id, message_canal_vip.message_id, parse_mode='HTML', disable_web_page_preview=True)
                bot.send_sticker(canal_vip, sticker=sticker_loss)
                bot.send_sticker(canal_vip, sticker=sticker_analisando_mercado)

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

        
        
        # Validando o stop_loss
        if 'win' in stop_loss:
            stop_loss = []
            stop_loss.append('loss')
        


        #if stop_loss.count('loss') == 2:
        #    try:
        #    
        #        if canal_free !='':
        #            bot.send_message(canal_free, f'⛔🛑 Alunos,\nMercado instável! Aguardem a normalização do mesmo conforme indicamos no curso 📚.\n\nAtt, Diretoria Nivus Tips 🤝 ')
    
        #        if canal_vip !='':
        #            bot.send_message(canal_vip, f'⛔🛑 Alunos,\nMercado instável! Aguardem a normalização do mesmo conforme indicamos no curso 📚.\n\nAtt, Diretoria Nivus Tips 🤝 ')
    
        #        stop_loss = []
        #        print('STOP LOSS - ANÁLISE VOLTARÁ EM 30 MINUTOS \n\n')
        #        time.sleep(1800)
    
        #    except:
        #        pass


        print('==================================================')
        validador_sinal = 0
        contador_cash = 0
        contador_passagem = 0
        lista_resultados = lista_resultados_sinal
        return






inicio()            # Difinição do webBrowser
logarSite()         # Logando no Site


#________________________________________________________________________________________ TELEGRAM__________________________________________________________________________________#

print('\n\n')
print('###################### AGUARDANDO COMANDOS ######################')

global canal


#CHAVE_API = '5651549126:AAFaVyaQkxTTVPq9WxpIBejBMR_oUPdt_5o'   # DEV
#CHAVE_API = '5698820535:AAGS8-wEVPDHioAJ5wAiKUn5SAKDwjXUFHw'  # PRODUÇÃO
#


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

''' ADD A ESTRATÉGIA EXTRA NA LISTA DE ESTRATÉGIAS '''
estrategia_extra = ['ESTRATÉGIA EXTRA']
placar_estrategia_extra = ['ESTRATÉGIA EXTRA']
placar_estrategia_extra.extend([0,0,0,0,0])

estrategias.append(estrategia_extra)
placar_estrategias.append(placar_estrategia_extra)




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

        placar = bot.send_message(message_canal.chat.id,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%")

        print('######################### ANALISANDO AS ESTRATÉGIAS CADASTRADAS  #########################')
        print()

        bot.send_sticker(canal_vip, sticker = sticker_analisando_mercado)
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

        placar = bot.send_message(message_canal.chat.id,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%")

        print('######################### ANALISANDO AS ESTRATÉGIAS CADASTRADAS  #########################')
        print()

        bot.send_sticker(canal_vip, sticker = sticker_analisando_mercado)
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






