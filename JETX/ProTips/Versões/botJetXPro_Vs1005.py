from webbrowser import BaseBrowser
from selenium import webdriver
import time
import warnings
from webdriver_manager.chrome import ChromeDriverManager
import logging
from datetime import datetime, timedelta
from selenium.webdriver.support.color import Color
import pandas as pd
from columnar import columnar
import telebot
from telegram.ext import *
from telebot import *
import operator



#_______________________________________________________________________#____________________________________________________________________________________________________

print()
print('                                #################################################################')
print('                                ###################   BOT JETX PRO   #########################')
print('                                #################################################################')
print('                                ##################### SEJA BEM VINDO ############################')
print('                                #################################################################')
print('                                ############# DESENVOLVIDO POR VICTOR RODRIGUES #################')
print('                                #################################################################\n')
print('Versão = 1.0.0')
print('Ambiente: Produção\n\n\n')


# Definindo opções para o browser
warnings.filterwarnings("ignore", category=DeprecationWarning) 
chrome_options = webdriver.ChromeOptions() 
chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("window-size=1037,547")
#chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
#chrome_options.add_experimental_option('useAutomationExtension', False)
#chrome_options.add_argument("--incognito") #abrir chrome no modo anônimo
#chrome_options.add_argument('--disable-blink-features=AutomationControlled')
#chrome_options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"



# CORES
vermelho = '#ff2f2f'
verde = '#4ec520'


# DATA FRAME
df = pd.DataFrame(columns = ['data','horario','hora','minuto','vela','cor','capturado' ])


# CAPTURANDO CAMPOS
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


#usuario: Fordbracom22
#senha : Fordbracom2022

time.sleep(1)
print()
print('O Programa está sendo iniciado......')

browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)   
print('\n\n')

logger = logging.getLogger()

browser.get(r"https://pi.njoybingo.com/game.do?token=733e595b-6b9c-43ff-8236-cf003da6ec17&pn=meskbet&lang=pt&game=SMARTSOFT-JetX_JetX&type=CHARGED")
browser.maximize_window()
time.sleep(10)

# acessando o iframe do jogo
while True:
    try:
        iframe = browser.find_element_by_id('game-frame')
        browser.switch_to.frame(iframe)
        break

    except:
        browser.get(r"https://pi.njoybingo.com/game.do?token=733e595b-6b9c-43ff-8236-cf003da6ec17&pn=meskbet&lang=pt&game=SMARTSOFT-JetX_JetX&type=CHARGED")
        time.sleep(10)



# Validando estrategias
def funcValidador():

    global sticker_alerta
    global vela_atual
    global contador
    global cPrint
    global cValidador
    global cVela
    global reset_contagemVela
    global estrategia
    global estrategias
    global resetar_resultados
    global contagem_vela
    global validacao
    global contador_passagem
    global alerta_free
    global alerta_vip
    global alerta_adm
    global horario_atual


    if contador == 0:
        
        print(horario_atual)
        contagem_vela.append(vela_atual)
        print(f'Resultados --> {contagem_vela}')

        for estrategia in estrategias:
            for e in enumerate(estrategia[:-2]):

                if cPrint == 0:
                    print(f'Estratégia --> {estrategia}')
                    cPrint+=1


                for v in enumerate(contagem_vela):

                    while v[0] == e[0]:
                        if '+' in e[1]:
                            resultado = operator.gt(float(v[1]), float(e[1][1:]))
                            validacao.append(resultado)
                            cValidador+=1
                            cVela+=1
                            break
                            
                        if '-' in e[1]:
                            resultado = operator.lt(float(v[1]), float(e[1][1:]))
                            validacao.append(resultado)
                            cValidador+=1
                            cVela+=1
                            break
            

            if False in validacao:
                resetar_resultados+=1
            
            if resetar_resultados == len(estrategias):
                    contagem_vela = []
                    reset_contagemVela = 0
                    resetar_resultados = 0

            print(f'Validador  --> {validacao}')
            

            if validacao.count(True) == len(estrategia[:-3]):
                if False not in validacao:
                        contador+=1
                        contador_passagem +=1
                        resetar_resultados = 0
                        cPrint = 0
                        print('====================================================================')
                        return
                    
            
            else:
                cPrint = 0
                validacao = []
            print('====================================================================')




# RASPAGEM DOS DADOS
def raspagem():

    global parar
    global browser
    global message
    global placar_win
    global placar_loss
    global vela_atual
    global cor
    global df
    global placar_win
    global placar_loss
    global placar
    global placar_semGale
    global placar_gale1
    global placar_gale2
    global placar_gale3
    global estrategias
    global estrategia
    global resultados_sinais
    global placar_estrategias
    global placar_estrategia
    global stop_loss
    global contador
    global sticker_alerta
    global cPrint
    global cValidador
    global cVela
    global reset_contagemVela
    global resetar_resultados
    global contagem_vela
    global validacao
    global contador_passagem
    global alerta
    global vela_maluca
    global table
    global canal_free
    global canal_vip
    global canal_adm
    global message_canal_free
    global message_canal_vip
    global message_canal_adm
    global alerta_free
    global alerta_vip
    global alerta_adm
    global vela_anterior
    global horario_atual


    parar=0
    contador = 0
    contador_passagem = 0
    resetar_resultados = 0
    cValidador = 0
    cVela = 0
    cPrint = 0
    reset_contagemVela = 0
    
    
    sticker_alerta = 'CAACAgEAAxkBAAEXKPBi_DTijam6We_hn2pKXO5BmfHFnwACHQIAAtUT4UcU9AABkK85ntMpBA'
    sticker_win = 'CAACAgEAAxkBAAEXPSpi_qndfx_m__I0yX8xSrAmrfHVtQACMwMAAoNx-UeWmHGI3CsNcSkE'
    sticker_win_2x = 'CAACAgEAAxkBAAEXjU9jDBBHmDTD9f1BESDMWJM6GSYVlgACKQMAAmRqYUTwE5iOtrnpgCkE'
    sticker_win_5x = 'CAACAgEAAxkBAAEXjVljDBCvp8vCTUyjJX4mHksSzHggCAACVwIAAoKKYEQIvKaBc6-faCkE'
    sticker_loss = 'CAACAgEAAxkBAAEXjVdjDBCMtqipIpA3Poiqn5bZBezo4AACJAMAAkBiYERIZ_Ehrjtk6CkE'

    contagem_cor = []
    contagem_vela = []
    validacao = []
    

    while True:

        # Validando se é uma novo dia para resetar resultados
        #data_hoje = datetime.today()
        #somaDia = timedelta(days=1)
        #data_amanha = data_hoje + somaDia
        horario_atual = datetime.today().strftime('%H:%M')

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass

        try:
            if browser.find_elements_by_class_name('game-started') == []:
                time.sleep(1)

                while True:
                    try:
                        vela_atual = browser.find_element_by_xpath('//*[@id="last100Spins"]/div[1]').text
                        str_cor = Color.from_string(browser.find_element_by_xpath('//*[@id="last100Spins"]/div[1]').value_of_css_property('color')).hex
                        break
                    except:
                        browser.get(r"https://pi.njoybingo.com/game.do?token=733e595b-6b9c-43ff-8236-cf003da6ec17&pn=meskbet&lang=pt&game=SMARTSOFT-JetX_JetX&type=CHARGED")
                        time.sleep(10)
                        # acessando o iframe do jogo
                        iframe = browser.find_element_by_id('game-frame')
                        browser.switch_to.frame(iframe)
                
                
                # Funcionalidade que valida se está capturando a mesma vela.
                if vela_anterior != vela_atual or vela_anterior == 0:
                    pass

                elif browser.find_element_by_xpath(f'//*[@id="last100Spins"]/div[1]').text == browser.find_element_by_xpath(f'//*[@id="last100Spins"]/div[2]').text:
                    print('DUAS VELAS COM O MESMO RESULTADO')
                    pass
                
                else:
                    continue


                # convertendo cor
                if str_cor == vermelho:
                    cor='vermelho'
                if str_cor == verde:
                    cor='verde'

                
                # pegando o resultado dos jogos
                contagem_cor.append(cor)
                contagem_vela.append(vela_atual)
                print(horario_atual)
                print(f'Resultados --> {contagem_vela}')

                
                # Validando se o resultado se encaixa na estratégia ( TRUE ou FALSE )
                if contador == 0:
                    for estrategia in estrategias:
                        for e in enumerate(estrategia[:-2]):

                            if cPrint == 0:
                                print(f'Estratégia --> {estrategia}')
                                cPrint+=1


                            for v in enumerate(contagem_vela):

                                while v[0] == e[0]:
                                    if '+' in e[1]:
                                        resultado = operator.gt(float(v[1]), float(e[1][1:]))
                                        validacao.append(resultado)
                                        cValidador+=1
                                        cVela+=1
                                        break
                                        
                                    if '-' in e[1]:
                                        resultado = operator.lt(float(v[1]), float(e[1][1:]))
                                        validacao.append(resultado)
                                        cValidador+=1
                                        cVela+=1
                                        break

                                    else:
                                        print('ERRO NA ESTRATÉGIA ', estrategia,'...VERIFIQUE O CADASTRO DA MESMA.')
                                        time.sleep(3)
                                        break


                        print(f'Validador  --> {validacao}')

                        if False in validacao:
                            resetar_resultados+=1
                        
                        if resetar_resultados == len(estrategias):    # Resetando contagem de vela
                                
                            reset_contagemVela = 0
                            cPrint = 0
                            resetar_resultados = 0
                            validacao = []
                            contagem_vela = [] ####
                            print('====================================================================')
                            print('TODAS AS ESTRATEGIAS COM CONDIÇÕES FALSAS! RESETANDO ANALISE! -- Resetou na primeira função \n\n ')
                            funcValidador()
                            if contador == 0:
                                validacao = []
                                cPrint = 0

                                vela_anterior = vela_atual
                                time.sleep(11)
                                break
                            else:
                                pass
                                

                        if validacao.count(True) == len(estrategia[:-3]):
                            if False not in validacao:
                                print('ENVIANDO ALERTA TELEGRAM')
                                print('====================================================================')
                                try:
                                    if canal_free != '':
                                        alerta_free = bot.send_sticker(canal_free, sticker=sticker_alerta)
                                    
                                    if canal_vip !='':
                                        alerta_vip = bot.send_sticker(canal_vip, sticker=sticker_alerta)
                                    
                                    if canal_adm !='':
                                        alerta_adm = bot.send_sticker(canal_adm, sticker=sticker_alerta)
                                    

                                    if contador == 0:
                                        contador+=1
                                        contador_passagem +=1
                                    else:
                                        pass
                                    
                                    validacao = []
                                    cPrint = 0

                                    vela_anterior = vela_atual
                                    time.sleep(11)
                                    break

                                except:
                                    pass
                            
                            else:
                                print('====================================================================')
                                validacao = []
                                cPrint = 0
                        
                        else:
                            print('====================================================================')
                            validacao = []
                            cPrint = 0
                            continue


                if len(contagem_vela) <= 10:
                    pass

                else:
                    print('====================================================================')
                    print('BUG IDENTIFICADO..REINICIANDO ANÁLISES')
                    print('====================================================================')
                    raspagem()
                        


                if contador_passagem == 2:
                    pass


                elif contador_passagem == 1:
                    contador_passagem+=1
                    continue

                else:
                    resetar_resultados = 0
                    cValidador = 0
                    cPrint = 0
                    validacao = []

                    vela_anterior = vela_atual
                    time.sleep(11)
                    continue


                # Após enviar alerta, validar se envia sinal Telegram 
                if contador == 1:
                    resetar_resultados=0 

                    for estrategia in estrategias:
                        for e in enumerate(estrategia[:-2]):

                            if cPrint == 0:
                                print(f'Estratégia --> {estrategia}')
                                cPrint+=1

                            for v in enumerate(contagem_vela):

                                while v[0] == e[0]:
                                    if '+' in e[1]:
                                        resultado = operator.gt(float(v[1]), float(e[1][1:]))
                                        validacao.append(resultado)
                                        cValidador+=1
                                        cVela+=1
                                        break
                                        
                                    if '-' in e[1]:
                                        resultado = operator.lt(float(v[1]), float(e[1][1:]))
                                        validacao.append(resultado)
                                        cValidador+=1
                                        cVela+=1
                                        break


                            if False in validacao:
                                resetar_resultados+=1
                            
                            if resetar_resultados == len(estrategias):
                                    resetar_resultados=0
                            
                            else:
                                continue

                        print(f'Validador  --> {validacao}')


                        if False in validacao:
                            reset_contagemVela +=1
            

                        if validacao.count(True) == len(estrategia[:-2]):
                            if False not in validacao:
      
                                print('ENVIANDO SINAL TELEGRAM')

                                headers = ['-✅1º CASH OUT EM ' + estrategia[-2] + '\n✅2º CASH OUT EM 2x' if estrategia[-2] == '1.5x' else '-✅1º CASH OUT EM ' + estrategia[-2] + '\n✅2º CASH OUT EM 5x']

                                data = [
                                    ['⏰ ENTRAR APÓS O RESULTADO '+ vela_atual                                                                  ],
                                    ['🔰 FAZER ATÉ ' + estrategia[-1] + ' PROTEÇÕES' if int(estrategia[-1]) > 0 else '🔰 FAZER NENHUMA PROTEÇÃO'     ],
                                    ["🌐 <a href='https://mesk.bet/casino/?game=1'>JetX</a>     "]
                                ]
                                
                                table = columnar(data, headers, no_borders=True)

                                try:
                                    # deletando o alerta
                                    # enviando sinal Telegram
                                    if canal_free != '':
                                        bot.delete_message(canal_free, alerta_free.message_id)
                                        message_canal_free = bot.send_message(canal_free,table, parse_mode='HTML', disable_web_page_preview=True)

                                    if canal_vip !='':
                                        bot.delete_message(canal_vip, alerta_vip.message_id)
                                        message_canal_vip = bot.send_message(canal_vip,table, parse_mode='HTML', disable_web_page_preview=True)

                                    if canal_adm !='':
                                        bot.delete_message(canal_adm, alerta_adm.message_id)
                                        message_canal_adm = bot.send_message(canal_adm,table, parse_mode='HTML', disable_web_page_preview=True)

                                except:
                                    pass

                                print('====================================================================')
                                break
                        
                        else:
                            print('====================================================================')
                            cPrint = 0
                            validacao = []

            
                if contador == 1 and validacao == []:
                    try:

                        if canal_free !='':
                            bot.delete_message(canal_free, alerta_free.message_id)
                            
                        if canal_vip !='':
                            bot.delete_message(canal_vip, alerta_vip.message_id)
                        
                        if canal_adm !='':
                            bot.delete_message(canal_adm, alerta_adm.message_id)

                        contador = 0
                        contador_passagem = 0
                        resetar_resultados = 0
                        cPrint = 0
                        validacao = []

                        if reset_contagemVela == len(estrategias):
                            cPrint = 0
                            validacao = []
                            reset_contagemVela = 0
                            resetar_resultados = 0
                            contador_passagem = 0
                            contagem_vela = [] ####
                            print('TODAS AS ESTRATEGIAS COM CONDIÇÕES FALSAS! RESETANDO ANALISE! -- Resetou na segunda função \n\n ')
                            continue
                        
                        vela_anterior = vela_atual
                        time.sleep(11)
                        continue
                    
                    except:
                        pass
               
                
                else:
                    break
                    
            else:
                continue

        except:
            continue


    # Rodada após o envio do sinal Telegram
    contador = 0
    validacao = []

    vela_anterior = vela_atual
    time.sleep(11)

    # Validando se foi solicitado o stop do BOT
    
    while contador <= int(estrategia[-1]):

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass


        try:
            if browser.find_elements_by_class_name('game-started') == []:
                time.sleep(1)
                vela_atual = browser.find_element_by_xpath('//*[@id="last100Spins"]/div[1]').text
                str_cor = Color.from_string(browser.find_element_by_xpath('//*[@id="last100Spins"]/div[1]').value_of_css_property('color')).hex

                # Funcionalidade que valida se está capturando a mesma vela.
                if vela_anterior != vela_atual or vela_anterior == 0:
                    pass

                elif browser.find_element_by_xpath(f'//*[@id="last100Spins"]/div[1]').text == browser.find_element_by_xpath(f'//*[@id="last100Spins"]/div[2]').text:
                    pass
                
                else:
                    continue


                print(vela_atual)

                
                if float(vela_atual) >= float(estrategia[-2].strip('Xx')):
                    
                    # validando o tipo de WIN
                    if contador == 0:
                        print('WIN SEM GALE')
                        placar_win+=1
                        placar_semGale+=1
                        resultados_sinais = placar_win + placar_loss
                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                        stop_loss.append('win')
                        for pe in placar_estrategias:
                            if pe[:-5] == estrategia:
                                pe[-5] = int(pe[-5])+1 


                    if contador == 1:
                        print('WIN GALE1')
                        placar_win+=1
                        placar_gale1+=1
                        resultados_sinais = placar_win + placar_loss
                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                        stop_loss.append('win')
                        for pe in placar_estrategias:
                            if pe[:-5] == estrategia:
                                pe[-4] = int(pe[-4])+1


                    if contador == 2:
                        print('WIN GALE2')
                        placar_win+=1
                        placar_gale2+=1
                        resultados_sinais = placar_win + placar_loss
                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)
                        
                        stop_loss.append('win')
                        for pe in placar_estrategias:
                            if pe[:-5] == estrategia:
                                pe[-3] = int(pe[-3])+1



                    if contador == 3:
                        print('WIN gale3')
                        placar_win+=1
                        placar_gale3+=1
                        resultados_sinais = placar_win + placar_loss
                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                        stop_loss.append('win')
                        for pe in placar_estrategias:
                            if pe[:-5] == estrategia:
                                pe[-2] = int(pe[-2])+1


                    # editando mensagem enviada e enviando sticker
                    try:
                        if canal_free != '':
                            bot.edit_message_text(table +"  \n============================== \n              WINNNN ✅ --- 🎯 "+ vela_atual+"x", message_canal_free.sender_chat.id, message_canal_free.message_id, parse_mode='HTML', disable_web_page_preview=True)   
                            
                            if float(vela_atual) < 5.0:
                                bot.send_sticker(canal_free, sticker=sticker_win_2x)
                            elif float(vela_atual) > 5.0:
                                bot.send_sticker(canal_free, sticker=sticker_win_5x)
                            else:
                                #bot.send_sticker(canal_free, sticker=sticker_win)
                                print('SEM FIGURINHA PARA O CHECK OUT CADASTRADO')


                        if canal_vip != '':
                            bot.edit_message_text(table +"  \n============================== \n              WINNNN ✅ --- 🎯 "+ vela_atual+"x", message_canal_vip.sender_chat.id, message_canal_vip.message_id, parse_mode='HTML', disable_web_page_preview=True)   

                            if float(vela_atual) < 5.0:
                                bot.send_sticker(canal_vip, sticker=sticker_win_2x)
                            elif float(vela_atual) > 5.0:
                                bot.send_sticker(canal_vip, sticker=sticker_win_5x)
                            else:
                                #bot.send_sticker(canal_free, sticker=sticker_win)
                                print('SEM FIGURINHA PARA O CHECK OUT CADASTRADO')


                        if canal_adm != '':
                            bot.edit_message_text(table +"  \n============================== \n              WINNNN ✅ --- 🎯 "+ vela_atual+"x", message_canal_adm.sender_chat.id, message_canal_adm.message_id, parse_mode='HTML', disable_web_page_preview=True)   

                            if float(vela_atual) < 5.0:
                                bot.send_sticker(canal_adm, sticker=sticker_win_2x)
                            elif float(vela_atual) > 5.0:
                                bot.send_sticker(canal_adm, sticker=sticker_win_5x)
                            else:
                                #bot.send_sticker(canal_free, sticker=sticker_win)
                                print('SEM FIGURINHA PARA O CHECK OUT CADASTRADO')
                        
                        
                        
                    except:
                        pass
                    
                    print('==================================================')

                    vela_anterior = vela_atual
                    time.sleep(11)
                    raspagem()
                
                else:
                    print('LOSSS')
                    print('==================================================')
                    contador+=1

                    vela_anterior = vela_atual
                    time.sleep(11)
                    continue
            else:
                continue
        
        except Exception as a:
            logger.error('Exception ocorrido no ' + repr(a))
            continue
    

    if parar != 0:
        return
    else:
        pass

    print('LOSSS GALE ',estrategia[-1])
    placar_loss +=1
    

    resultados_sinais = placar_win + placar_loss
    print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
    #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

    # Atualizando placar da estratégia
    for pe in placar_estrategias:
        if pe[:-5] == estrategia:
            pe[-1] = int(pe[-1])+1
    
    
    else:
        # editando mensagem e enviando sticker
        try:
            
            if canal_free !='':
                bot.edit_message_text(table +"\n============================== \n              LOSS ✖", message_canal_free.sender_chat.id, message_canal_free.message_id, parse_mode='HTML', disable_web_page_preview=True)
                bot.send_sticker(canal_free, sticker=sticker_loss)

            if canal_vip !='':
                bot.edit_message_text(table +"\n============================== \n              LOSS ✖", message_canal_vip.sender_chat.id, message_canal_vip.message_id, parse_mode='HTML', disable_web_page_preview=True)
                bot.send_sticker(canal_vip, sticker=sticker_loss)
            
            if canal_adm !='':
                bot.edit_message_text(table +"\n============================== \n              LOSS ✖", message_canal_adm.sender_chat.id, message_canal_adm.message_id, parse_mode='HTML', disable_web_page_preview=True)
                bot.send_sticker(canal_adm, sticker=sticker_loss)

        except:
            pass
        


    # Validando o stop_loss
    if 'win' in stop_loss:
        stop_loss = []
        stop_loss.append('loss')
    
    if stop_loss.count('loss') == 2:
        try:
        
            if canal_free !='':
                bot.send_message(canal_free, f'⛔🛑 Alunos,\nMercado instável! Aguardem a normalização do mesmo conforme indicamos no curso 📚.\n\nAtt, Diretoria Pro Tips 🤝 ')

            if canal_vip !='':
                bot.send_message(canal_vip, f'⛔🛑 Alunos,\nMercado instável! Aguardem a normalização do mesmo conforme indicamos no curso 📚.\n\nAtt, Diretoria Pro Tips 🤝 ')
            
            if canal_adm !='':
                bot.send_message(canal_adm, f'⛔🛑 Alunos,\nMercado instável! Aguardem a normalização do mesmo conforme indicamos no curso 📚.\n\nAtt, Diretoria Pro Tips 🤝 ')

            stop_loss = []
            print('STOP LOSS - ANÁLISE VOLTARÁ EM 30 MINUTOS \n\n')
            time.sleep(1800)

        except:
            pass



    print('==================================================')

    vela_anterior = vela_atual
    time.sleep(11)
    raspagem()




#________________________________________________________________________________________ TELEGRAM__________________________________________________________________________________#


print('###################### AGUARDANDO COMANDOS ######################')

global canal

CHAVE_API = '5656831413:AAHJ-2gQLbdnsVWbhp7YKcC6L2-Kt98Qawc'    
bot = telebot.TeleBot(CHAVE_API)


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
contador = 0
botStatus = 0



# LENDO TXT PARA DEFINIR VARIAVEL FREE E VIP E VALIDAÇÃO DE USUÁRIO
txt = open("canais.txt", "r")
free = txt.readlines(1)
vip = txt.readlines(2)
adm = txt.readlines(3)
ids = txt.readlines(4)

for canal in free:
    free = canal.split(' ')
    free = int(free[1])
    

for canal in vip:
    vip = canal.split(' ')
    vip = int(vip[1])


for canal in adm:
    adm = canal.split(' ')
    adm = int(adm[1])


for id in ids:
    id_usuario = id.split(' ')
    id_usuario = id_usuario[1]


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

    global contador

    if contador == 0:
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
    global contador

    print('Excluir estrategia')

    if contador == 0:
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
    global contador

    if contador == 1:
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
        pausarBot()

        print('###################### AGUARDANDO COMANDOS ######################')

        message_final = bot.reply_to(message, "🤖 Ok! Bot pausado 🛑", reply_markup=markup)



@bot.message_handler(commands=['start'])
def start(message):

    if str(message.chat.id) in id_usuario:
       

        #Add to buttons by list with ours generate_buttons function.
        #markup = generate_buttons(['/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','📊 Placar Atual','❌ Pausar Bot'], markup)
        
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message, "🤖 Bot Aviator PRO Iniciado! ✅ Escolha uma opção 👇",
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
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('◀ Voltar', '🆓 Enviar sinais Canal FREE', '🏆 Enviar sinais Canal VIP', '🆓🏆 Enviar sinais Canal FREE & VIP', '🆓🏆📋 Enviar sinais Canal FREE & VIP & ADM')

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
        canal_adm = ''
        stop_loss = []
        botStatus = 1
        vela_anterior = 0

        placar = bot.send_message(message_canal.chat.id,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%")

        print('######################### ANALISANDO AS ESTRATÉGIAS CADASTRADAS  #########################')
        print()

        raspagem()
    

    if message_canal.text in ['🏆 Enviar sinais Canal VIP']:
        
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_final = bot.reply_to(message_canal, "🤖 Ok! Ligando Bot nas configurações:\n===============================\n" + "Canal: "+ str(message_canal.text.split(' ')[4:]) + '\n Estratégia(s): \n' + str([f'{estrategia}' for estrategia in estrategias]), reply_markup = markup)
        
        print("Iniciar e enviar sinais no Canal VIP ")

        canal_free = ''
        canal_vip = vip
        canal_adm = ''
        stop_loss = []
        botStatus = 1
        vela_anterior = 0

        placar = bot.send_message(message_canal.chat.id,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%")

        print('######################### ANALISANDO AS ESTRATÉGIAS CADASTRADAS  #########################')
        print()

        raspagem()


    if message_canal.text in ['🆓🏆 Enviar sinais Canal FREE & VIP']:
        
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_final = bot.reply_to(message_canal, "🤖 Ok! Ligando Bot nas configurações:\n===============================\n" + "Canal: "+ str(message_canal.text.split(' ')[4:]) + '\n Estratégia(s): \n' + str([f'{estrategia}' for estrategia in estrategias]), reply_markup = markup)
        
        print("Iniciar e enviar sinais no Canal FREE & VIP ")

        canal_free = free
        canal_vip = vip
        canal_adm = ''
        stop_loss = []
        botStatus = 1
        vela_anterior = 0

        placar = bot.send_message(message_canal.chat.id,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%")

        print('######################### ANALISANDO AS ESTRATÉGIAS CADASTRADAS  #########################')
        print()

        raspagem()


    if message_canal.text in ['🆓🏆📋 Enviar sinais Canal FREE & VIP & ADM']:

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_final = bot.reply_to(message_canal, "🤖 Ok! Ligando Bot nas configurações:\n===============================\n" + "Canal: "+ str(message_canal.text.split(' ')[4:]) + '\n Estratégia(s): \n' + str([f'{estrategia}' for estrategia in estrategias]), reply_markup = markup)
        
        print("Iniciar e enviar sinais no Canal FREE & VIP & ADM ")

        canal_free = free
        canal_vip = vip
        canal_adm = adm
        stop_loss = []
        botStatus = 1
        vela_anterior = 0

        placar = bot.send_message(message_canal.chat.id,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%")

        print('######################### ANALISANDO AS ESTRATÉGIAS CADASTRADAS  #########################')
        print()

        raspagem()




@bot.message_handler()
def registrarEstrategia(message_estrategia):
    global estrategia
    global estrategias
    global placar_estrategia
    global placar_estrategias

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

    estrategias.append(estrategia)
    placar_estrategias.append(placar_estrategia)


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






