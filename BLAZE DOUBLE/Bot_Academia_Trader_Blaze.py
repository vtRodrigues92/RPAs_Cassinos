from selenium import webdriver
import time
import warnings
from webdriver_manager.chrome import ChromeDriverManager
import logging
from datetime import datetime
from selenium.webdriver.support.color import Color
import pandas as pd
from columnar import columnar
import telebot
from telegram.ext import * 
from telebot import types


#_______________________________________________________________________#____________________________________________________________________________________________________

print()
print('                                #################################################################')
print('                                #### ACADEMIA TRADER BLAZE - BOT DE SINAIS DA BLAZE(DOUBLE) ####')
print('                                #################################################################')
print('                                ##################### SEJA BEM VINDO ############################')
print('                                #################################################################')
print('                                ############# DESENVOLVIDO POR VICTOR RODRIGUES #################')
print('                                #################################################################\n')
print('Versão = 0.0.2')
print('Ambiente: Produção\n\n\n')



# Definindo opções para o browser
warnings.filterwarnings("ignore", category=DeprecationWarning) 
chrome_options = webdriver.ChromeOptions() 
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("window-size=1037,547")
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_experimental_option('useAutomationExtension', False)
#chrome_options.add_argument("--incognito") #abrir chrome no modo anônimo
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
#chrome_options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"


logger = logging.getLogger()



#========================================================= ESTRATEGIAS #========================================================= 



def iniciar():

    global parar
    global browser
    
    parar = 0
    

    time.sleep(1)
    print()
    print('O Programa está sendo iniciado......')


    browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)   
    print('\n\n')


    #print('Versão localizada e configurada com sucesso.\n\n\n')
    #print('O Programa está sendo iniciado......\n\n\n')


    browser.get(r"https://blaze.com/pt/games/double")
    time.sleep(10)
    browser.execute_script("document.body.style.zoom='96%'")

    logger = logging.getLogger()



def cincoPorUm():

    print('######################### INICIANDO ANÁLISE DAS CORES, APLICANDO A ESTRATÉGIA TENDÊNCIA 5 #########################')
    print()

    global parar
    global browser
    global message
    global placar_win
    global placar_loss

    parar = 0

    ''' STIKERS '''
    stiker_win = "CAACAgEAAxkBAAEVnm5iwPYYBdxAQFKTlYGQ3j9jv85Y-wACTAMAAtPPAAFGZbJmpnCxmw8pBA"
    stiker_loss = "CAACAgEAAxkBAAEVnmdiwPWDxcWA_MUfTKKXR1njG6FFvAACPgMAAlVOAAFGyMLz_Zw7B7cpBA"
    stiker_branco = "CAACAgEAAxkBAAEVnntiwPZqytGHBEZHrQSgZNyVetCptwACsAMAAk1cAUYuc7wzYZVOzCkE"
    stiker_alerta = "CAACAgEAAxkBAAEVnndiwPZQLlXa2IkKPghN1-tCYY3dNwAC2AIAAjkzAAFGJGqMkbmpE-MpBA"

    ''' Cores '''
    preto = '#262f3c'
    vermelho = '#f12c4c'
    branco = '#ffffff'
    
    tb_horario = []
    data = pd.DataFrame(columns = ["horario", "cor", "numero"])
    tb_cor = []
    
    
    '''Leitura dos resultados''' 

    
    

    contador = 0
        
    while True:


        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass



        while contador < 5:

            # Validando se foi solicitado o stop do BOT
            if parar != 0:
                break
            else:
                pass

            try:
                
                time.sleep(1)
                proxima_rodada = browser.find_element_by_xpath('//*[@id="roulette-timer"]/div[1]').text
                proxima_rodada = proxima_rodada.split('\n')
                proxima_rodada = proxima_rodada[0]

                ''' Data e hora atual '''        
                current_date = datetime.today()
                data_corrente = current_date.strftime('%Y-%m-%d')
                hora_corrente = current_date.strftime('%H:%M')
                
                repeticoes = tb_horario.count(hora_corrente)
                
                
                if proxima_rodada == 'Blaze Girou':
                    time.sleep(2)
                    if not repeticoes == 2 :
                        cor = Color.from_string(browser.find_element_by_xpath('//*[@id="roulette-recent"]/div/div[1]/div[1]/div/div').value_of_css_property('background-color')).hex
                        
                        if cor != branco:
                            numero = int(browser.find_element_by_xpath('//*[@id="roulette-recent"]/div/div[1]/div[1]/div/div').text)
                            
                            
                        if cor == preto:
                            cor = '⚫'
                            cor_str = 'PRETO'
                            print('Resultado: ', hora_corrente, '- preto -', numero)
                            print()
                            #tb_horario.append(hora_corrente)
                            #data = data.append({'horario':hora_corrente, 'cor':'preto', 'numero':numero}, ignore_index=True)
                            tb_cor.append(cor_str)
                            #print(data)
                            #print(tb_horario)
                            print(tb_cor)
                            
                            contagem_geral = len(tb_cor)
                            contagem_preto = tb_cor.count('PRETO')
                            
                            if contagem_geral == contagem_preto:
                                try:
                                    if contagem_preto == 1:
                                        print("=========================================================================================\n")
                                        time.sleep(4)
                                        continue
                                
                                    if contagem_preto == 2:
                                        contador+=1
                                        print("=========================================================================================\n")
                                        time.sleep(4)
                                        continue

                                    if contagem_preto == 3:
                                        contador+=1
                                        print("=========================================================================================\n")
                                        time.sleep(4)
                                        continue

                                    if contagem_preto == 4:
                                        print('Enviando alerta')
                                        
                                        try:
                                            if canal_free != '':
                                                alerta_free = bot.send_sticker(canal_free, sticker=stiker_alerta)
                                        except:
                                            pass
                                        
                                        try:
                                            if canal_vip != '':
                                                alerta_vip = bot.send_sticker(canal_vip, sticker=stiker_alerta)
                                        
                                        except:
                                            pass

                                        

                                        print("=========================================================================================\n")
                                        time.sleep(4)
                                        continue

                                    
                                    if contagem_preto == 5:
                                        print('Padrão formado!')
                                        print('Enviando sinal Telegram')

                                        alerta = ''
                                        cor = '🔴'
                                        cor_str = 'VERMELHO'
                                        
                                        print("=========================================================================================\n")
                                        headers = ['     ACADEMIA TRADER BLAZE 🦅📡                                                    ']

                                        data = [
                                            [ '70% - ' + cor + cor + cor + cor_str + cor + cor + cor ],
                                            [ '30% - ⚪⚪⚪BRANCO⚪⚪⚪                            '],
                                            [''],
                                            ['🛡 PROTEÇÃO 1 - DOBRAR A APOSTA'],
                                            ['🛡 PROTEÇÃO 2 - DOBRAR A APOSTA'],
                                            [''],
                                            ["🌐 <a href='https://blaze.com/pt/games/double'>Link para a Blaze</a>"],
                                            [''],
                                            ['📈 Siga o seu gerenciamento!'],
                                            ['🧠 Bateu a meta? Sai fora do mercado!'],
                                        ]
                                        
                                        table = columnar(data, headers, no_borders=True)
                                        
                                        ''' Enviando sinal pro canal Telegram '''
                                        try:
                                            if canal_free != '':
                                                message_canal_free = bot.send_message(canal_free,table, parse_mode='HTML', disable_web_page_preview=True)
                                                pass
                                        
                                        except:
                                            pass
                                        
                                        try:
                                            if canal_vip != '':
                                                message_canal_vip = bot.send_message(canal_vip,table, parse_mode='HTML', disable_web_page_preview=True)
                                                break
                                            else:
                                                break

                                        except:
                                            break
                                        
                                except:
                                    continue
                                    

                            else:
                                print('Resetando.....')
                                print("=========================================================================================\n")

                                try:
                                    if canal_free != '':
                                        bot.delete_message(canal_free, alerta_free.message_id)
                                    
                                except:
                                    pass

                                try:    
                                    if canal_vip != '':
                                        bot.delete_message(canal_vip, alerta_vip.message_id)
                                
                                except:
                                    pass
                            
                            
                            tb_cor = []
                            contador = 0
                            tb_cor.append(cor_str)
                            print(tb_cor)
                            print("=========================================================================================\n")
                            time.sleep(3)
                            continue
                                
                                        
                            
                        if cor == vermelho:
                            cor = '🔴'
                            cor_str = 'VERMELHO'
                            print('Resultado: ', hora_corrente,'- vermelho -', numero)
                            print()
                            #tb_horario.append(hora_corrente)
                            #data = data.append({'horario':hora_corrente, 'cor':'vermelho', 'numero':numero}, ignore_index=True)
                            tb_cor.append(cor_str)
                            #print(data)
                            #print(tb_horario)
                            print(tb_cor)
                            
                            contagem_geral = len(tb_cor)
                            contagem_vermelho = tb_cor.count('VERMELHO')
                            
                        
                            if contagem_geral == contagem_vermelho:
                                try:
                                    if contagem_vermelho == 1:
                                        print("=========================================================================================\n")
                                        contador+=1
                                        time.sleep(4)
                                        continue

                                    if contagem_vermelho == 2:
                                        contador+=1
                                        print("=========================================================================================\n")
                                        time.sleep(4)
                                        continue

                                    if contagem_vermelho == 3:
                                        contador+=1
                                        print("=========================================================================================\n")
                                        time.sleep(4)
                                        continue

                                    if contagem_vermelho == 4:
                                        print('Enviando alerta')

                                        try:
                                            if canal_free != '':
                                                alerta_free = bot.send_sticker(canal_free, sticker=stiker_alerta)
                                        except:
                                            pass
                                        
                                        try:
                                            if canal_vip != '':
                                                alerta_vip = bot.send_sticker(canal_vip, sticker=stiker_alerta)
                                            
                                        except:
                                            pass

                                        print("=========================================================================================\n")
                                        time.sleep(4)
                                        continue
                                    
        
                                    if contagem_vermelho == 5:
                                        print('Padrão formado!')
                                        print('Enviando sinal Telegram')

                                        alerta = ''
                                        cor = '⚫'
                                        cor_str = 'PRETO'
                                        
                                        print("=========================================================================================\n")
                                        headers = ['     ACADEMIA TRADER BLAZE 🦅📡                                                    ']

                                        data = [
                                            [ '70% - ' + cor + cor + cor + cor_str + cor + cor + cor ],
                                            [ '30% - ⚪⚪⚪BRANCO⚪⚪⚪                            '],
                                            [''],
                                            ['🛡 PROTEÇÃO 1 - DOBRAR A APOSTA'],
                                            ['🛡 PROTEÇÃO 2 - DOBRAR A APOSTA'],
                                            [''],
                                            ["🌐 <a href='https://blaze.com/pt/games/double'>Link para a Blaze</a>"],
                                            [''],
                                            ['📈 Siga o seu gerenciamento!'],
                                            ['🧠 Bateu a meta? Sai fora do mercado!'],
                                        ]
                                        
                                        table = columnar(data, headers, no_borders=True)
                                        

                                        ''' Enviando sinal pro canal Telegram '''
                                        try:
                                            if canal_free !='':
                                                message_canal_free = bot.send_message(canal_free,table, parse_mode='HTML', disable_web_page_preview=True)
                                                pass
                                        
                                        except:
                                            pass
                                        
                                        try:
                                            if canal_vip !='':
                                                message_canal_vip = bot.send_message(canal_vip,table, parse_mode='HTML', disable_web_page_preview=True)
                                                break
                                            
                                            else:
                                                break
                                        
                                        except:
                                            break

                                                                            
                                        
                                except:
                                    continue
                            

                                
                            else:
                                print('Resetando.....')
                                print("=========================================================================================\n")

                                try:
                                    if canal_free !='' :
                                        bot.delete_message(canal_free, alerta_free.message_id)
                                    
                                except:
                                    pass

                                try:    
                                    if canal_vip !='':
                                        bot.delete_message(canal_vip, alerta_vip.message_id)
                                
                                except:
                                    pass
                            
                            
                            tb_cor = []
                            contador = 0
                            tb_cor.append(cor_str)
                            print(tb_cor)
                            print("=========================================================================================\n")
                            time.sleep(3)
                            continue
                    
                            
                    
                        if cor == branco:
                            cor = '⚪'
                            cor_str = 'BRANCO'
                            print('Resultado: ', hora_corrente,'- branco')
                            print()
                            #tb_horario.append(hora_corrente)
                            #data = data.append({'horario':hora_corrente, 'cor':'branco'}, ignore_index=True)
                            tb_cor.append(cor_str)
                            print(tb_cor)
                            
                            contagem_geral = len(tb_cor)
                            contagem_branco = tb_cor.count('BRANCO')
                            
                            if contagem_geral == contagem_branco:    
                                try:
                                    if contagem_branco == 1:
                                        print("=========================================================================================\n")
                                        time.sleep(4)
                                        continue

                                    if contagem_branco == 2:
                                        contador+=1
                                        print("=========================================================================================\n")
                                        time.sleep(4)
                                        continue

                                    if contagem_branco == 3:
                                        contador+=1
                                        print("=========================================================================================\n")
                                        time.sleep(4)
                                        continue

                                    if contagem_branco == 4:
                                        print('Enviando alerta')

                                        try:
                                            if canal_free !='':
                                                alerta_free = bot.send_sticker(canal_free, sticker=stiker_alerta)
                                                time.sleep(1)
                                        except:
                                            pass
                                        
                                        try:
                                            if canal_vip !='':
                                                alerta_vip = bot.send_sticker(canal_vip, sticker=stiker_alerta)
                                        
                                        except:
                                            pass

                                        print("=========================================================================================\n")
                                        time.sleep(4)
                                        continue

                                    if contagem_branco == 5:
                                        print('Padrão formado!')
                                        print('Enviando sinal Telegram')

                                        alerta = ''
                                        cor = '⚪'
                                        cor_str = 'BRANCO'

                                        print("=========================================================================================\n")
                                        headers = ['     ACADEMIA TRADER BLAZE 🦅📡                                                    ']

                                        data = [
                                            [ '70% - ' + cor + cor + cor + cor_str + cor + cor + cor ],
                                            [ '30% - ⚪⚪⚪BRANCO⚪⚪⚪                            '],
                                            [''],
                                            ['🛡 PROTEÇÃO 1 - DOBRAR A APOSTA'],
                                            ['🛡 PROTEÇÃO 2 - DOBRAR A APOSTA'],
                                            [''],
                                            ["🌐 <a href='https://blaze.com/pt/games/double'>Link para a Blaze</a>"],
                                            [''],
                                            ['📈 Siga o seu gerenciamento!'],
                                            ['🧠 Bateu a meta? Sai fora do mercado!'],
                                        ]
                                        
                                        table = columnar(data, headers, no_borders=True)
                                        
                                        ''' Enviando sinal pro canal Telegram '''
                                        try:
                                            if canal_free !='':
                                                message_canal_free = bot.send_message(canal_free,table, parse_mode='HTML', disable_web_page_preview=True)
                                                pass
                                        
                                        except:
                                            pass
                                        
                                        try:
                                            if canal_vip !='':
                                                message_canal_vip = bot.send_message(canal_vip,table, parse_mode='HTML', disable_web_page_preview=True)
                                                break
                                        
                                        except:
                                            break

                                    
                                except:
                                    continue
                                    
                            else:
                                print('Resetando.....')
                                print("=========================================================================================\n")

                                try:
                                    if canal_free !='':
                                        bot.delete_message(canal_free, alerta_free.message_id)
                                    
                                except:
                                    pass

                                try:    
                                    if canal_vip !='':
                                        bot.delete_message(canal_vip, alerta_vip.message_id)
                                
                                except:
                                    pass
                            
                            
                            tb_cor = []
                            contador = 0
                            tb_cor.append(cor_str)
                            print(tb_cor)
                            print("=========================================================================================\n")
                            time.sleep(3)
                            continue
                            
                            
                    
                        else:
                            print('Nenhuma cor definida')
                            time.sleep(1)
                else:
                    continue

            except:
                #logger.error('Exception ocorrido no try do While: ' + repr(e))
                time.sleep(1)
                continue   
        
        
        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass

        time.sleep(3)
        contador2 = 0
        while contador2 <= 2:

            # Validando se foi solicitado o stop do BOT
            if parar != 0:
                break
            else:
                pass
            

            ''' IDENTIFICANDO A PROXIMA RODADA'''
            #try:
            try:
                proxima_rodada = browser.find_element_by_xpath('//*[@id="roulette-timer"]/div[1]').text
                proxima_rodada = proxima_rodada.split('\n')
                proxima_rodada = proxima_rodada[0]
                
                #repeticoes = tb_horario.count(hora_corrente)
                
                if proxima_rodada == 'Blaze Girou':
                    time.sleep(2)
                    cor = Color.from_string(browser.find_element_by_xpath('//*[@id="roulette-recent"]/div/div[1]/div[1]/div/div').value_of_css_property('background-color')).hex


                    ''' VERIFICANDO WIN OU LOSS '''
                
                    if cor != branco:                    
                        numero = int(browser.find_element_by_xpath('//*[@id="roulette-recent"]/div/div[1]/div[1]/div/div').text)


                        if cor == preto:
                            cor = '⚫'
                            cor_str = 'PRETO'
                            print('Resultado: ', hora_corrente, '- preto -', numero)
                            print()
                            #tb_horario.append(hora_corrente)
                            #data = data.append({'horario':hora_corrente, 'cor':'preto', 'numero':numero}, ignore_index=True)
                            
                            tb_cor.append(cor_str)
                            print(tb_cor)

                            contagem_geral = len(tb_cor)
                            contagem_preto = tb_cor.count('PRETO')
                        
                            
                            if contagem_geral == contagem_preto:
                                print('LOSS')
                                print("=========================================================================================")
                                contador2+=1
                                time.sleep(4)
                                continue
                            
                            else:
                                print('WINNNNN')
                                placar_win +=1
                                resultados_sinais = placar_win + placar_loss
                                print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
                                bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN "+str(placar_win)+"\n😭 LOSS "+str(placar_loss)+"\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)
                                
                                try:
                                    if canal_free !='':
                                        bot.edit_message_text(table +"\n============================== \n                     WINNNN ✅", message_canal_free.sender_chat.id, message_canal_free.message_id, parse_mode='HTML', disable_web_page_preview=True)
                                        bot.send_sticker(canal_free, sticker=stiker_win)
                                
                                except:
                                    pass
                                
                                try:
                                    if canal_vip !='':
                                        bot.edit_message_text(table +"\n============================== \n                     WINNNN ✅", message_canal_vip.sender_chat.id, message_canal_vip.message_id, parse_mode='HTML', disable_web_page_preview=True)
                                        bot.send_sticker(canal_vip, sticker=stiker_win)
                                    
                                except:
                                    pass
                                
                

                                print("=========================================================================================")
                                time.sleep(4)
                                
                                cincoPorUm()
                            
                            
                        if cor == vermelho:
                            cor = '🔴'
                            cor_str = 'VERMELHO'
                            print('Resultado: ', hora_corrente,'- vermelho -', numero)
                            print()
                            #tb_horario.append(hora_corrente)
                            #data = data.append({'horario':hora_corrente, 'cor':'preto', 'numero':numero}, ignore_index=True)
                            
                            tb_cor.append(cor_str)
                            print(tb_cor)

                            contagem_geral = len(tb_cor)
                            contagem_vermelho = tb_cor.count('VERMELHO')
                        
                            
                            if contagem_geral == contagem_vermelho:
                                print('LOSS')
                                print("=========================================================================================")
                                contador2+=1
                                time.sleep(4)
                                continue
                            
                            else:
                                print('WINNNNN')
                                placar_win +=1
                                resultados_sinais = placar_win + placar_loss
                                print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
                                bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN "+str(placar_win)+"\n😭 LOSS "+str(placar_loss)+"\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                                try:
                                    if canal_free !='':
                                        bot.edit_message_text(table +"\n============================== \n                     WINNNN ✅", message_canal_free.sender_chat.id, message_canal_free.message_id, parse_mode='HTML', disable_web_page_preview=True)
                                        bot.send_sticker(canal_free, sticker=stiker_win)
                                
                                except:
                                    pass
                                
                                try: 
                                    if canal_vip !='':
                                        bot.edit_message_text(table +"\n============================== \n                     WINNNN ✅", message_canal_vip.sender_chat.id, message_canal_vip.message_id, parse_mode='HTML', disable_web_page_preview=True)
                                        bot.send_sticker(canal_vip, sticker=stiker_win)
                                
                                except:
                                    pass


                                print("=========================================================================================")
                                time.sleep(4)
                            
                                cincoPorUm()
                        
                                
                                
                    else:

                        cor = '⚪'
                        cor_str = 'BRANCO'
                        print('Resultado: ', hora_corrente, '- branco -', '0')
                        print()        
                        tb_cor.append(cor_str)
                        print(tb_cor)


                        print('WINNNNN')
                        placar_win +=1
                        resultados_sinais = placar_win + placar_loss
                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
                        bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN "+str(placar_win)+"\n😭 LOSS "+str(placar_loss)+"\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                        try:
                            if canal_free !='':
                                bot.edit_message_text(table +"\n============================== \n                     WINNNN ✅", message_canal_free.sender_chat.id, message_canal_free.message_id, parse_mode='HTML', disable_web_page_preview=True)
                                bot.send_sticker(canal_free, sticker=stiker_branco)
                        
                        except:
                            pass
                        
                        try:
                            if canal_vip !='':
                                bot.edit_message_text(table +"\n============================== \n                     WINNNN ✅", message_canal_vip.sender_chat.id, message_canal_vip.message_id, parse_mode='HTML', disable_web_page_preview=True)
                                time.sleep(1)
                                bot.send_sticker(canal_vip, sticker=stiker_branco)
                        
                        except:
                            pass
                        

                        print("=========================================================================================")
                        time.sleep(4)
                        
                        cincoPorUm()
                    
            except:
                #logger.error('Exception ocorrido no try do While: ' + repr(f))
                time.sleep(1)
                continue       
        


        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass

        
        print('LOSS GALE2')
        placar_loss +=1
        resultados_sinais = placar_win + placar_loss
        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")        
        bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN "+str(placar_win)+"\n😭 LOSS "+str(placar_loss)+"\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

        try:
            if canal_free !='':
                bot.edit_message_text(table+"\n============================== \n                        LOSS ✖", message_canal_free.sender_chat.id, message_canal_free.message_id, parse_mode='HTML', disable_web_page_preview=True)
                bot.send_sticker(canal_free, sticker=stiker_loss)
        
        except:
            pass
        
        try:
            if canal_vip !='':
                bot.edit_message_text(table+"\n============================== \n                        LOSS ✖", message_canal_vip.sender_chat.id, message_canal_vip.message_id, parse_mode='HTML', disable_web_page_preview=True)
                bot.send_sticker(canal_vip, sticker=stiker_loss)
        
        except:
            pass

        print("=========================================================================================")
        time.sleep(4)
        cincoPorUm()
        
        

def tresPorUm():

    print('######################### INICIANDO ANÁLISE DAS CORES, APLICANDO A ESTRATÉGIA TENDÊNCIA 3 #########################')
    print()



    global parar
    global browser
    global message
    global placar_win
    global placar_loss

    parar = 0

    ''' STIKERS '''
    stiker_win = "CAACAgEAAxkBAAEVnm5iwPYYBdxAQFKTlYGQ3j9jv85Y-wACTAMAAtPPAAFGZbJmpnCxmw8pBA"
    stiker_loss = "CAACAgEAAxkBAAEVnmdiwPWDxcWA_MUfTKKXR1njG6FFvAACPgMAAlVOAAFGyMLz_Zw7B7cpBA"
    stiker_branco = "CAACAgEAAxkBAAEVnntiwPZqytGHBEZHrQSgZNyVetCptwACsAMAAk1cAUYuc7wzYZVOzCkE"
    stiker_alerta = "CAACAgEAAxkBAAEVnndiwPZQLlXa2IkKPghN1-tCYY3dNwAC2AIAAjkzAAFGJGqMkbmpE-MpBA"

    ''' Cores '''
    preto = '#262f3c'
    vermelho = '#f12c4c'
    branco = '#ffffff'
    
    tb_horario = []
    data = pd.DataFrame(columns = ["horario", "cor", "numero"])
    tb_cor = []
    
    
    '''Leitura dos resultados''' 

    

    contador = 0
        
    while True:


        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass



        while contador < 5:

            # Validando se foi solicitado o stop do BOT
            if parar != 0:
                break
            else:
                pass

            try:
                
                time.sleep(1)
                proxima_rodada = browser.find_element_by_xpath('//*[@id="roulette-timer"]/div[1]').text
                proxima_rodada = proxima_rodada.split('\n')
                proxima_rodada = proxima_rodada[0]

                ''' Data e hora atual '''        
                current_date = datetime.today()
                data_corrente = current_date.strftime('%Y-%m-%d')
                hora_corrente = current_date.strftime('%H:%M')
                
                repeticoes = tb_horario.count(hora_corrente)
                
                
                if proxima_rodada == 'Blaze Girou':
                    time.sleep(2)
                    if not repeticoes == 2 :
                        cor = Color.from_string(browser.find_element_by_xpath('//*[@id="roulette-recent"]/div/div[1]/div[1]/div/div').value_of_css_property('background-color')).hex
                        
                        if cor != branco:
                            numero = int(browser.find_element_by_xpath('//*[@id="roulette-recent"]/div/div[1]/div[1]/div/div').text)
                            
                            
                        if cor == preto:
                            cor = '⚫'
                            cor_str = 'PRETO'
                            print('Resultado: ', hora_corrente, '- preto -', numero)
                            print()
                            #tb_horario.append(hora_corrente)
                            #data = data.append({'horario':hora_corrente, 'cor':'preto', 'numero':numero}, ignore_index=True)
                            tb_cor.append(cor_str)
                            #print(data)
                            #print(tb_horario)
                            print(tb_cor)
                            
                            contagem_geral = len(tb_cor)
                            contagem_preto = tb_cor.count('PRETO')
                            
                            if contagem_geral == contagem_preto:
                                try:
                                    if contagem_preto == 1:
                                        print("=========================================================================================\n")
                                        time.sleep(4)
                                        continue

                                    if contagem_preto == 2:
                                        print('Enviando alerta')
                                        
                                        try:
                                            if canal_free != '':
                                                alerta_free = bot.send_sticker(canal_free, sticker=stiker_alerta)
                                        except:
                                            pass
                                        
                                        try:
                                            if canal_vip != '':
                                                alerta_vip = bot.send_sticker(canal_vip, sticker=stiker_alerta)
                                        
                                        except:
                                            pass

                                        

                                        print("=========================================================================================\n")
                                        time.sleep(4)
                                        continue

                                    
                                    if contagem_preto == 3:
                                        print('Padrão formado!')
                                        print('Enviando sinal Telegram')

                                        alerta = ''
                                        cor = '🔴'
                                        cor_str = 'VERMELHO'
                                        
                                        print("=========================================================================================\n")
                                        headers = ['     ACADEMIA TRADER BLAZE 🦅📡                                                    ']

                                        data = [
                                            [ '70% - ' + cor + cor + cor + cor_str + cor + cor + cor ],
                                            [ '30% - ⚪⚪⚪BRANCO⚪⚪⚪                            '],
                                            [''],
                                            ['🛡 PROTEÇÃO 1 - DOBRAR A APOSTA'],
                                            ['🛡 PROTEÇÃO 2 - DOBRAR A APOSTA'],
                                            [''],
                                            ["🌐 <a href='https://blaze.com/pt/games/double'>Link para a Blaze</a>"],
                                            [''],
                                            ['📈 Siga o seu gerenciamento!'],
                                            ['🧠 Bateu a meta? Sai fora do mercado!'],
                                        ]
                                        
                                        table = columnar(data, headers, no_borders=True)
                                        
                                        ''' Enviando sinal pro canal Telegram '''
                                        try:
                                            if canal_free != '':
                                                message_canal_free = bot.send_message(canal_free,table, parse_mode='HTML', disable_web_page_preview=True)
                                                pass
                                        
                                        except:
                                            pass
                                        
                                        try:
                                            if canal_vip != '':
                                                message_canal_vip = bot.send_message(canal_vip,table, parse_mode='HTML', disable_web_page_preview=True)
                                                break
                                            else:
                                                break

                                        except:
                                            break
                                        
                                except:
                                    continue
                                    

                            else:
                                print('Resetando.....')
                                print("=========================================================================================\n")

                                try:
                                    if canal_free != '':
                                        bot.delete_message(canal_free, alerta_free.message_id)
                                    
                                except:
                                    pass

                                try:    
                                    if canal_vip != '':
                                        bot.delete_message(canal_vip, alerta_vip.message_id)
                                
                                except:
                                    pass
                            
                            
                            tb_cor = []
                            contador = 0
                            tb_cor.append(cor_str)
                            print(tb_cor)
                            print("=========================================================================================\n")
                            time.sleep(4)
                            continue
                                
                                        
                            
                        if cor == vermelho:
                            cor = '🔴'
                            cor_str = 'VERMELHO'
                            print('Resultado: ', hora_corrente,'- vermelho -', numero)
                            print()
                            #tb_horario.append(hora_corrente)
                            #data = data.append({'horario':hora_corrente, 'cor':'vermelho', 'numero':numero}, ignore_index=True)
                            tb_cor.append(cor_str)
                            #print(data)
                            #print(tb_horario)
                            print(tb_cor)
                            
                            contagem_geral = len(tb_cor)
                            contagem_vermelho = tb_cor.count('VERMELHO')
                            
                        
                            if contagem_geral == contagem_vermelho:
                                try:
                                    if contagem_vermelho == 1:
                                        print("=========================================================================================\n")
                                        contador+=1
                                        time.sleep(4)
                                        continue


                                    if contagem_vermelho == 2:
                                        print('Enviando alerta')

                                        try:
                                            if canal_free != '':
                                                alerta_free = bot.send_sticker(canal_free, sticker=stiker_alerta)
                                        except:
                                            pass
                                        
                                        try:
                                            if canal_vip != '':
                                                alerta_vip = bot.send_sticker(canal_vip, sticker=stiker_alerta)
                                            
                                        except:
                                            pass

                                        print("=========================================================================================\n")
                                        time.sleep(4)
                                        continue
                                    
        
                                    if contagem_vermelho == 3:
                                        print('Padrão formado!')
                                        print('Enviando sinal Telegram')

                                        alerta = ''
                                        cor = '⚫'
                                        cor_str = 'PRETO'
                                        
                                        print("=========================================================================================\n")
                                        headers = ['     ACADEMIA TRADER BLAZE 🦅📡                                                    ']

                                        data = [
                                            [ '70% - ' + cor + cor + cor + cor_str + cor + cor + cor ],
                                            [ '30% - ⚪⚪⚪BRANCO⚪⚪⚪                            '],
                                            [''],
                                            ['🛡 PROTEÇÃO 1 - DOBRAR A APOSTA'],
                                            ['🛡 PROTEÇÃO 2 - DOBRAR A APOSTA'],
                                            [''],
                                            ["🌐 <a href='https://blaze.com/pt/games/double'>Link para a Blaze</a>"],
                                            [''],
                                            ['📈 Siga o seu gerenciamento!'],
                                            ['🧠 Bateu a meta? Sai fora do mercado!'],
                                        ]
                                        
                                        table = columnar(data, headers, no_borders=True)
                                        

                                        ''' Enviando sinal pro canal Telegram '''
                                        try:
                                            if canal_free !='':
                                                message_canal_free = bot.send_message(canal_free,table, parse_mode='HTML', disable_web_page_preview=True)
                                                pass
                                        
                                        except:
                                            pass
                                        
                                        try:
                                            if canal_vip !='':
                                                message_canal_vip = bot.send_message(canal_vip,table, parse_mode='HTML', disable_web_page_preview=True)
                                                break
                                            
                                            else:
                                                break
                                        
                                        except:
                                            break

                                                                            
                                        
                                except:
                                    continue
                            

                                
                            else:
                                print('Resetando.....')
                                print("=========================================================================================\n")

                                try:
                                    if canal_free !='' :
                                        bot.delete_message(canal_free, alerta_free.message_id)
                                    
                                except:
                                    pass

                                try:    
                                    if canal_vip !='':
                                        bot.delete_message(canal_vip, alerta_vip.message_id)
                                
                                except:
                                    pass
                            
                            
                            tb_cor = []
                            contador = 0
                            tb_cor.append(cor_str)
                            print(tb_cor)
                            print("=========================================================================================\n")
                            time.sleep(4)
                            continue
                    
                            
                    
                        if cor == branco:
                            cor = '⚪'
                            cor_str = 'BRANCO'
                            print('Resultado: ', hora_corrente,'- branco')
                            print()
                            #tb_horario.append(hora_corrente)
                            #data = data.append({'horario':hora_corrente, 'cor':'branco'}, ignore_index=True)
                            tb_cor.append(cor_str)
                            print(tb_cor)
                            
                            contagem_geral = len(tb_cor)
                            contagem_branco = tb_cor.count('BRANCO')
                            
                            if contagem_geral == contagem_branco:    
                                try:
                                    if contagem_branco == 1:
                                        print("=========================================================================================\n")
                                        time.sleep(4)
                                        continue


                                    if contagem_branco == 2:
                                        print('Enviando alerta')

                                        try:
                                            if canal_free !='':
                                                alerta_free = bot.send_sticker(canal_free, sticker=stiker_alerta)
                                                time.sleep(1)
                                        except:
                                            pass
                                        
                                        try:
                                            if canal_vip !='':
                                                alerta_vip = bot.send_sticker(canal_vip, sticker=stiker_alerta)
                                        
                                        except:
                                            pass

                                        print("=========================================================================================\n")
                                        time.sleep(4)
                                        continue

                                    if contagem_branco == 3:
                                        print('Padrão formado!')
                                        print('Enviando sinal Telegram')

                                        alerta = ''
                                        cor = '⚪'
                                        cor_str = 'BRANCO'

                                        print("=========================================================================================\n")
                                        headers = ['     ACADEMIA TRADER BLAZE 🦅📡                                                    ']

                                        data = [
                                            [ '70% - ' + cor + cor + cor + cor_str + cor + cor + cor ],
                                            [ '30% - ⚪⚪⚪BRANCO⚪⚪⚪                            '],
                                            [''],
                                            ['🛡 PROTEÇÃO 1 - DOBRAR A APOSTA'],
                                            ['🛡 PROTEÇÃO 2 - DOBRAR A APOSTA'],
                                            [''],
                                            ["🌐 <a href='https://blaze.com/pt/games/double'>Link para a Blaze</a>"],
                                            [''],
                                            ['📈 Siga o seu gerenciamento!'],
                                            ['🧠 Bateu a meta? Sai fora do mercado!'],
                                        ]
                                        
                                        table = columnar(data, headers, no_borders=True)
                                        
                                        ''' Enviando sinal pro canal Telegram '''
                                        try:
                                            if canal_free !='':
                                                message_canal_free = bot.send_message(canal_free,table, parse_mode='HTML', disable_web_page_preview=True)
                                                pass
                                        
                                        except:
                                            pass
                                        
                                        try:
                                            if canal_vip !='':
                                                message_canal_vip = bot.send_message(canal_vip,table, parse_mode='HTML', disable_web_page_preview=True)
                                                break
                                        
                                        except:
                                            break

                                    
                                except:
                                    continue
                                    
                            else:
                                print('Resetando.....')
                                print("=========================================================================================\n")

                                try:
                                    if canal_free !='':
                                        bot.delete_message(canal_free, alerta_free.message_id)
                                    
                                except:
                                    pass

                                try:    
                                    if canal_vip !='':
                                        bot.delete_message(canal_vip, alerta_vip.message_id)
                                
                                except:
                                    pass
                            
                            
                            tb_cor = []
                            contador = 0
                            tb_cor.append(cor_str)
                            print(tb_cor)
                            print("=========================================================================================\n")
                            time.sleep(4)
                            continue
                            
                            
                    
                        else:
                            print('Nenhuma cor definida')
                            time.sleep(1)
                else:
                    continue

            except:
                #logger.error('Exception ocorrido no try do While: ' + repr(e))
                time.sleep(1)
                continue   
        
        
        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass

        time.sleep(3)
        contador2 = 0
        while contador2 <= 2:

            # Validando se foi solicitado o stop do BOT
            if parar != 0:
                break
            else:
                pass
            

            ''' IDENTIFICANDO A PROXIMA RODADA'''
            #try:
            try:
                proxima_rodada = browser.find_element_by_xpath('//*[@id="roulette-timer"]/div[1]').text
                proxima_rodada = proxima_rodada.split('\n')
                proxima_rodada = proxima_rodada[0]
                
                #repeticoes = tb_horario.count(hora_corrente)
                
                if proxima_rodada == 'Blaze Girou':
                    time.sleep(2)
                    cor = Color.from_string(browser.find_element_by_xpath('//*[@id="roulette-recent"]/div/div[1]/div[1]/div/div').value_of_css_property('background-color')).hex


                    ''' VERIFICANDO WIN OU LOSS '''
                
                    if cor != branco:                    
                        numero = int(browser.find_element_by_xpath('//*[@id="roulette-recent"]/div/div[1]/div[1]/div/div').text)


                        if cor == preto:
                            cor = '⚫'
                            cor_str = 'PRETO'
                            print('Resultado: ', hora_corrente, '- preto -', numero)
                            print()
                            #tb_horario.append(hora_corrente)
                            #data = data.append({'horario':hora_corrente, 'cor':'preto', 'numero':numero}, ignore_index=True)
                            
                            tb_cor.append(cor_str)
                            print(tb_cor)

                            contagem_geral = len(tb_cor)
                            contagem_preto = tb_cor.count('PRETO')
                        
                            
                            if contagem_geral == contagem_preto:
                                print('LOSS')
                                print("=========================================================================================")
                                contador2+=1
                                time.sleep(4)
                                continue
                            
                            else:
                                print('WINNNNN')
                                placar_win +=1
                                resultados_sinais = placar_win + placar_loss
                                print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
                                bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN "+str(placar_win)+"\n😭 LOSS "+str(placar_loss)+"\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)
                                
                                try:
                                    if canal_free !='':
                                        bot.edit_message_text(table +"\n============================== \n                     WINNNN ✅", message_canal_free.sender_chat.id, message_canal_free.message_id, parse_mode='HTML', disable_web_page_preview=True)
                                        bot.send_sticker(canal_free, sticker=stiker_win)
                                
                                except:
                                    pass
                                
                                try:
                                    if canal_vip !='':
                                        bot.edit_message_text(table +"\n============================== \n                     WINNNN ✅", message_canal_vip.sender_chat.id, message_canal_vip.message_id, parse_mode='HTML', disable_web_page_preview=True)
                                        bot.send_sticker(canal_vip, sticker=stiker_win)
                                    
                                except:
                                    pass
                                
                

                                print("=========================================================================================")
                                time.sleep(4)
                                
                                tresPorUm()
                            
                            
                        if cor == vermelho:
                            cor = '🔴'
                            cor_str = 'VERMELHO'
                            print('Resultado: ', hora_corrente,'- vermelho -', numero)
                            print()
                            #tb_horario.append(hora_corrente)
                            #data = data.append({'horario':hora_corrente, 'cor':'preto', 'numero':numero}, ignore_index=True)
                            
                            tb_cor.append(cor_str)
                            print(tb_cor)

                            contagem_geral = len(tb_cor)
                            contagem_vermelho = tb_cor.count('VERMELHO')
                        
                            
                            if contagem_geral == contagem_vermelho:
                                print('LOSS')
                                print("=========================================================================================")
                                contador2+=1
                                time.sleep(4)
                                continue
                            
                            else:
                                print('WINNNNN')
                                placar_win +=1
                                resultados_sinais = placar_win + placar_loss
                                print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
                                bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN "+str(placar_win)+"\n😭 LOSS "+str(placar_loss)+"\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                                try:
                                    if canal_free !='':
                                        bot.edit_message_text(table +"\n============================== \n                     WINNNN ✅", message_canal_free.sender_chat.id, message_canal_free.message_id, parse_mode='HTML', disable_web_page_preview=True)
                                        bot.send_sticker(canal_free, sticker=stiker_win)
                                
                                except:
                                    pass
                                
                                try: 
                                    if canal_vip !='':
                                        bot.edit_message_text(table +"\n============================== \n                     WINNNN ✅", message_canal_vip.sender_chat.id, message_canal_vip.message_id, parse_mode='HTML', disable_web_page_preview=True)
                                        bot.send_sticker(canal_vip, sticker=stiker_win)
                                
                                except:
                                    pass


                                print("=========================================================================================")
                                time.sleep(4)
                            
                                tresPorUm()
                        
                                
                                
                    else:

                        cor = '⚪'
                        cor_str = 'BRANCO'
                        print('Resultado: ', hora_corrente, '- branco -', '0')
                        print()        
                        tb_cor.append(cor_str)
                        print(tb_cor)


                        print('WINNNNN')
                        placar_win +=1
                        resultados_sinais = placar_win + placar_loss
                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
                        bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN "+str(placar_win)+"\n😭 LOSS "+str(placar_loss)+"\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                        try:
                            if canal_free !='':
                                bot.edit_message_text(table +"\n============================== \n                     WINNNN ✅", message_canal_free.sender_chat.id, message_canal_free.message_id, parse_mode='HTML', disable_web_page_preview=True)
                                bot.send_sticker(canal_free, sticker=stiker_branco)
                        
                        except:
                            pass
                        
                        try:
                            if canal_vip !='':
                                bot.edit_message_text(table +"\n============================== \n                     WINNNN ✅", message_canal_vip.sender_chat.id, message_canal_vip.message_id, parse_mode='HTML', disable_web_page_preview=True)
                                time.sleep(1)
                                bot.send_sticker(canal_vip, sticker=stiker_branco)
                        
                        except:
                            pass
                        

                        print("=========================================================================================")
                        time.sleep(4)
                        
                        tresPorUm()
                    
            except:
                #logger.error('Exception ocorrido no try do While: ' + repr(f))
                time.sleep(1)
                continue       
        


        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass

        
        print('LOSS GALE2')
        placar_loss +=1
        resultados_sinais = placar_win + placar_loss
        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")        
        bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN "+str(placar_win)+"\n😭 LOSS "+str(placar_loss)+"\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

        try:
            if canal_free !='':
                bot.edit_message_text(table+"\n============================== \n                        LOSS ✖", message_canal_free.sender_chat.id, message_canal_free.message_id, parse_mode='HTML', disable_web_page_preview=True)
                bot.send_sticker(canal_free, sticker=stiker_loss)
        
        except:
            pass
        
        try:
            if canal_vip !='':
                bot.edit_message_text(table+"\n============================== \n                        LOSS ✖", message_canal_vip.sender_chat.id, message_canal_vip.message_id, parse_mode='HTML', disable_web_page_preview=True)
                bot.send_sticker(canal_vip, sticker=stiker_loss)
        
        except:
            pass

        print("=========================================================================================")
        time.sleep(4)
        tresPorUm()
        
        





#________________________________________________________________________________________ TELEGRAM__________________________________________________________________________________#


print('###################### AGUARDANDO COMANDOS ######################')



CHAVE_API ='5434022871:AAF-mMhUcDuEID9vf-8WnLvZiFPUnjuzk-k'                               # teste-->'1929964993:AAFe7Qqu4jQFLnyOxau8PLGo7Q-Yu2kAQHs'   # oficial --> 5434022871:AAF-mMhUcDuEID9vf-8WnLvZiFPUnjuzk-k
#canal = -1001609828054#, '-1001775325949']   #1609828054    TESTE #1775325949 #OFICIAL -1001711794178
bot = telebot.TeleBot(CHAVE_API)


# PLACAR
placar_win = 0
placar_loss = 0
resultados_sinais = placar_win + placar_loss


global canal
global placar


# LENDO TXT PARA DEFINIR VARIAVEL FREE E VIP E VALIDAÇÃO DE USUÁRIO
txt = open("canais.txt", "r")
free = txt.readlines(1)
vip = txt.readlines(2)
ids = txt.readlines(3)

for canal in free:
    free=canal.split(' ')
    free = int(free[1])
    

for canal in vip:
    vip=canal.split(' ')
    vip = int(vip[1])


for id in ids:
    id_usuario = id.split(' ')
    id_usuario = id_usuario[1]


######################################################



def restart_program():
     while True:
        try:
            global parar
            global browser
            parar = 1
            browser.close()
            time.sleep(1)
            break
        except:
            continue

    

def generate_buttons(bts_names, markup):
    for button in bts_names:
        markup.add(types.KeyboardButton(button))
    return markup



@bot.message_handler(commands=['stop'])
def parar(message):
    if str(message.chat.id) in id_usuario:
        message_final = bot.reply_to(message, "🤖 Ok! Bot parado ❌")
        print('\n\n')
        print('Comando: Parar BOT')
        print('Parando o BOT....\n')
        restart_program()

        print('###################### AGUARDANDO COMANDOS ######################')

    else:
        message_error = bot.reply_to(message, "🤖 Você não tem permissão para acessar este Bot ❌🚫")





@bot.message_handler(commands=['start'])
def start(message):

    if str(message.chat.id) in id_usuario:
        
        #Add to buttons by list with ours generate_buttons function.
        message = bot.reply_to(message, "🤖 Bot Academia Trader Blaze iniciado ✅")
        #Add to buttons by list with ours generate_buttons function.
        markup = types.ReplyKeyboardMarkup(row_width=2)
        markup = generate_buttons(['/start','📈 Estratégia Tendência 5', '📈 Estratégia Tendência 3', ' VAGO', 'VAGO','/stop'], markup)
        message_estrategia = bot.send_message(message.chat.id, "🤖 Escolha a estratégia a ser usada 👇",
                                            reply_markup=markup)

        bot.register_next_step_handler(message_estrategia, opcoes_estrategias)
    
    else:
        message_error = bot.reply_to(message, "🤖 Você não tem permissão para acessar este Bot ❌🚫")
        


       

@bot.message_handler()
def opcoes_estrategias(message_estrategia):

    global canal_free
    global canal_vip
    global canal_free_vip
    global placar
    global estrategia
    

    if str(message_estrategia.chat.id) in id_usuario:
        
        if message_estrategia.text in ['📈 Estratégia Tendência 5']:
            print('Estratégia Tendência 5')
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(row_width=2)
            #Add to buttons by list with ours generate_buttons function.
            markup = generate_buttons(['/start','🆓 Canal FREE', '🏆 Canal VIP', '🆓🏆 Canal FREE E VIP', '/stop'], markup)
            message_canal = bot.reply_to(message_estrategia, "🤖 Escolha para onde enviar os sinais 👇",
                                    reply_markup=markup)
            
            estrategia = message_estrategia.text
            bot.register_next_step_handler(message_canal, escolher_canal)
            
            
        if message_estrategia.text in ['📈 Estratégia Tendência 3']:
            print('Estratégia Tendência 3')
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(row_width=2)
            #Add to buttons by list with ours generate_buttons function.
            markup = generate_buttons(['/start','🆓 Canal FREE', '🏆 Canal VIP', '🆓🏆 Canal FREE E VIP', '/stop'], markup)
            message_canal = bot.reply_to(message_estrategia, "🤖 Escolha para onde enviar os sinais 👇",
                                    reply_markup=markup)
            
            estrategia = message_estrategia.text
            bot.register_next_step_handler(message_canal, escolher_canal)


        if message_estrategia.text in['VAGO']:
            print('ESCOLHEU VAGO')
            pass
    
    else:
        message_error = bot.reply_to(message_estrategia, "🤖 Você não tem permissão para acessar este Bot ❌🚫")




@bot.message_handler()
def escolher_canal(message_canal):

    if str(message_canal.chat.id) in id_usuario:
        global canal_free
        global canal_vip
        global canal_free_vip
        global placar
        

        if message_canal.text in ['🆓 Canal FREE']:
            message_final = bot.reply_to(message_canal, "🤖 Ok! Iniciando Bot nas configurações:\n==========================\n" + estrategia + "\n" +message_canal.text)
            print('Comando: Iniciar BOT no Canal FREE')
            print('Iniciando BOT no Canal FREE\n')
            canal_free = free
            canal_vip = ''
            

            placar = bot.send_message(message_canal.chat.id,"📊 Placar Atual:\n==================\n😍 WIN "+str(placar_win)+"\n😭 LOSS "+str(placar_loss)+"\n🎯 Assertividade 0%")

            iniciar()
            if estrategia == '📈 Estratégia Tendência 3':
                tresPorUm()
            else:    
                cincoPorUm()

        if message_canal.text in ['🏆 Canal VIP']:
            message_final = bot.reply_to(message_canal, "🤖 Ok! Iniciando Bot nas configurações:\n==========================\n" + estrategia + "\n" +message_canal.text)
            print('Comando: Iniciar BOT no Canal VIP')
            print('Iniciando BOT no Canal VIP\n')
            canal_vip = vip
            canal_free = ''

            placar = bot.send_message(message_canal.chat.id,"📊 Placar Atual:\n==================\n😍 WIN "+str(placar_win)+"\n😭 LOSS "+str(placar_loss)+"\n🎯 Assertividade 0%")

            iniciar()
            if estrategia == '📈 Estratégia Tendência 3':
                tresPorUm()
            else:    
                cincoPorUm()
    
        if message_canal.text in ['🆓🏆 Canal FREE E VIP']:
            message_final = bot.reply_to(message_canal, "🤖 Ok! Iniciando Bot nas configurações:\n==========================\n" + estrategia + "\n" +message_canal.text)
            print('Comando: Iniciar BOT no Canal FREE E VIP')
            print('Iniciando BOT no Canal FREE E VIP\n')
            canal_free = free
            canal_vip = vip           #[-1001711794178, -1001558037901]
            
            placar = bot.send_message(message_canal.chat.id,"📊 Placar Atual:\n==================\n😍 WIN "+str(placar_win)+"\n😭 LOSS "+str(placar_loss)+"\n🎯 Assertividade 0%")

            iniciar()
            if estrategia == '📈 Estratégia Tendência 3':
                tresPorUm()
            else:    
                cincoPorUm()
    

    else:
        message_error = bot.reply_to(message_canal, "🤖 Você não tem permissão para acessar este Bot ❌🚫")
    
    


bot.infinity_polling()