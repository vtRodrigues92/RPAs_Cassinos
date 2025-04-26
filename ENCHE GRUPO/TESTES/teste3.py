from turtle import update
from selenium import webdriver
import time
import warnings
from webdriver_manager.chrome import ChromeDriverManager
import logging
from debugpy import is_client_connected
import mysql.connector
from mysql.connector import Error
from psutil import users
from datetime import date, datetime, timedelta
from selenium.webdriver.support.color import Color
import pandas as pd
from columnar import columnar
import telebot
import telegram
from telegram.ext import * 
import sys
import os


#_______________________________________________________________________#____________________________________________________________________________________________________


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


browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)   
print('\n')

browser.get(r"https://blaze.com/pt/games/double")
time.sleep(10)
browser.execute_script("document.body.style.zoom='96%'")

logger = logging.getLogger()



CHAVE_API = '5434022871:AAF-mMhUcDuEID9vf-8WnLvZiFPUnjuzk-k'
canal = -1001775325949
bot = telebot.TeleBot(CHAVE_API)

stiker_win = "CAACAgEAAxkBAAEVnm5iwPYYBdxAQFKTlYGQ3j9jv85Y-wACTAMAAtPPAAFGZbJmpnCxmw8pBA"
stiker_loss = "CAACAgEAAxkBAAEVnmdiwPWDxcWA_MUfTKKXR1njG6FFvAACPgMAAlVOAAFGyMLz_Zw7B7cpBA"
stiker_branco = "CAACAgEAAxkBAAEVnntiwPZqytGHBEZHrQSgZNyVetCptwACsAMAAk1cAUYuc7wzYZVOzCkE"
stiker_alerta = "CAACAgEAAxkBAAEVnndiwPZQLlXa2IkKPghN1-tCYY3dNwAC2AIAAjkzAAFGJGqMkbmpE-MpBA"



def alerta(canal, bot):
    
    # Formatando para envio no telegram
        
    headers2 = ['     🔔 ATENTOS, POSSÍVEL ENTRADA! 🔔                               ']
    data2 = [
    ['']    
    ]
        
    table2 = columnar(data2, headers2, no_borders=True)

    message_alerta = bot.send_message(canal, table2)
    message_alerta

    
'''______________________________________________________________________________________________________________________'''


def raspagem():

    #''' Data e hora atual '''
    #current_date = datetime.today()
    #data_corrente = current_date.strftime('%Y-%m-%d')
    #hora_corrente = current_date.strftime('%H:%M')
         

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
        
    
        while contador < 5:
            
            try:
                
                proxima_rodada = browser.find_element_by_xpath('//*[@id="roulette-timer"]/div[1]').text
                proxima_rodada = proxima_rodada.split('\n')
                proxima_rodada = proxima_rodada[0]

                ''' Data e hora atual '''        
                current_date = datetime.today()
                data_corrente = current_date.strftime('%Y-%m-%d')
                hora_corrente = current_date.strftime('%H:%M')
                
                repeticoes = tb_horario.count(hora_corrente)
                
                
                if proxima_rodada == 'Blaze Girou':
                    time.sleep(3)
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
                            
                            bot.send_sticker(canal, sticker=stiker_alerta)


                            if contagem_geral == contagem_preto:
                                try:
                                    if contagem_preto == 1:
                                        print("=========================================================================================")
                                        time.sleep(3)
                                        print('Padrão formado!\n')
                                        
                                        #bot.send_sticker(chat_id=update.message.chat_id, sticker=stiker_alerta)
                                        
                                        print('Enviando sinal Telegram')
                                        print("=========================================================================================")
                                        headers = ['     ACADEMIA TRADER BLAZE 🦅📡          ']

                                        data = [
                                            [ '90% - ' + cor + cor + cor + cor_str + cor + cor + cor ],
                                            [ '10% - ⚪⚪⚪BRANCO⚪⚪⚪                            '],
                                            [''],
                                            ['🛡 PROTEÇÃO 1 - DOBRAR A APOSTA'],
                                            ['🛡 PROTEÇÃO 2 - DOBRAR A APOSTA'],
                                            [''],
                                            ["🌐 <a href='https://blaze.com/pt/games/double'>Clique para ir para a Blaze</a>"],
                                            [''],
                                            ['📈 Siga o seu gerenciamento!'],
                                            ['🧠 Bateu a meta? Sai fora do mercado!'],
                                        ]
                                        
                                        table = columnar(data, headers, no_borders=True)
                                        
                                        ''' Enviando sinal pro canal Telegram '''
                                        message_canal = bot.send_message(canal,table, parse_mode='HTML', disable_web_page_preview=True)
                                        message_canal
                                        

                                        break
                                        
                                     
                                except Exception as f:
                                        logger.error('Exception ocorrido no try do While: ' + repr(f))
                                        time.sleep(1)     
                                        continue
                                    

                            else:
                                print('Resetando....\n')
                                tb_cor = []
                                contador = 0
                                tb_cor.append(cor_str)
                                print("=========================================================================================")
                                print(tb_cor)
                                time.sleep(3)
                                
                                        
                            
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
                            
                            bot.send_sticker(canal, sticker=stiker_alerta)
                        
                            if contagem_geral == contagem_vermelho:
                                try:
                                    if contagem_vermelho == 1:
                                        print("=========================================================================================")
                                        print('Padrão formado!\n')
                                        print('Enviando sinal Telegram')
                                        print("=========================================================================================")
                                        headers = ['     ACADEMIA TRADER BLAZE 🦅📡          ']

                                        data = [
                                            [ '90% - ' + cor + cor + cor + cor_str + cor + cor + cor ],
                                            [ '10% - ⚪⚪⚪BRANCO⚪⚪⚪                            '],
                                            [''],
                                            ['🛡 PROTEÇÃO 1 - DOBRAR A APOSTA'],
                                            ['🛡 PROTEÇÃO 2 - DOBRAR A APOSTA'],
                                            [''],
                                            ["🌐 <a href='https://blaze.com/pt/games/double'>Clique para ir para a Blaze</a>"],
                                            [''],
                                            ['📈 Siga o seu gerenciamento!'],
                                            ['🧠 Bateu a meta? Sai fora do mercado!'],
                                        ]
                                        
                                        table = columnar(data, headers, no_borders=True)
                                        
                                        ''' Enviando sinal pro canal Telegram '''
                                        message_canal = bot.send_message(canal,table, parse_mode='HTML', disable_web_page_preview=True)
                                        message_canal

                                        break
                                        
                                        
                                        
                                        
                                except:
                                    continue
                            
                                
                            else:
                                print('Resetando....\n')
                                tb_cor = []
                                contador = 0
                                tb_cor.append(cor_str)
                                print("=========================================================================================")
                                print(tb_cor)
                                time.sleep(3)
                     
                            
                       
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
                            
                            bot.send_sticker(canal, sticker=stiker_alerta)

                            if contagem_geral == contagem_branco:    
                                try:
                                    if contagem_branco == 1:
                                        print("=========================================================================================")
                                        print('Padrão formado!\n')
                                        print('Enviando sinal Telegram')
                                        print("=========================================================================================")
                                        headers = ['     ACADEMIA TRADER BLAZE 🦅📡          ']

                                        data = [
                                            [ '90% - ' + cor + cor + cor + cor_str + cor + cor + cor ],
                                            [ '10% - ⚪⚪⚪BRANCO⚪⚪⚪                            '],
                                            [''],
                                            ['🛡 PROTEÇÃO 1 - DOBRAR A APOSTA'],
                                            ['🛡 PROTEÇÃO 2 - DOBRAR A APOSTA'],
                                            [''],
                                            ["🌐 <a href='https://blaze.com/pt/games/double'>Clique para ir para a Blaze</a>"],
                                            [''],
                                            ['📈 Siga o seu gerenciamento!'],
                                            ['🧠 Bateu a meta? Sai fora do mercado!'],
                                        ]
                                        
                                        table = columnar(data, headers, no_borders=True)
                                        
                                        ''' Enviando sinal pro canal Telegram '''
                                        message_canal = bot.send_message(canal,table, parse_mode='HTML', disable_web_page_preview=True)
                                        message_canal
                                        break
                                    
                                    
                
                
                
                                except:
                                    continue
                                    
                            else:
                                print('Padrão quebrado...Resetando....\n')
                                tb_cor = []
                                contador = 0
                                tb_cor.append(cor_str)
                                print("=========================================================================================")
                                print(tb_cor)
                                time.sleep(3)
                    
                    
                    
                    
                    else:
                        print('Nenhuma cor definida')
                        time.sleep(1)
                else:
                    continue

            except:
                continue
           
        
        time.sleep(3)
        contador2 = 0
        while contador2 <= 2:
            ''' IDENTIFICANDO A PROXIMA RODADA'''
            #try:
            time.sleep(1)
            try:
                proxima_rodada = browser.find_element_by_xpath('//*[@id="roulette-timer"]/div[1]').text
                proxima_rodada = proxima_rodada.split('\n')
                proxima_rodada = proxima_rodada[0]
                
                #repeticoes = tb_horario.count(hora_corrente)
                
                if proxima_rodada == 'Blaze Girou':
                    time.sleep(3)
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
                                time.sleep(3)
                                continue
                            
                            else:
                                print('WINNNNN')
                                bot.edit_message_text(table +"\n============================== \n                     WINNNN ✅", message_canal.sender_chat.id, message_canal.message_id, parse_mode='HTML', disable_web_page_preview=True)
                                time.sleep(1)
                                bot.send_sticker(canal, sticker=stiker_win)
                                print("=========================================================================================")
                                
                                time.sleep(3)
                                raspagem()
                                
                            
                            
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
                                time.sleep(3)
                                continue
                            
                            else:
                                print('WINNNNN')
                                bot.edit_message_text(table +"\n============================== \n                     WINNNN ✅", message_canal.sender_chat.id, message_canal.message_id, parse_mode='HTML', disable_web_page_preview=True)
                                time.sleep(1)
                                bot.send_sticker(canal, sticker=stiker_win)
                                print("=========================================================================================")
                                
                                time.sleep(3)
                                raspagem()
                                
                                
                                
                        
                                
                                
                                
                                
                                
                                
                    else:
                        print('WINNNNN')
                        bot.edit_message_text(table +"\n============================== \n                     WINNNN ✅", message_canal.sender_chat.id, message_canal.message_id, parse_mode='HTML', disable_web_page_preview=True)
                        time.sleep(1)
                        bot.send_sticker(chat_id=update.message.chat_id, sticker=stiker_win)
                        print("=========================================================================================")
                        
                        raspagem()
                    
            except:
                continue
                    
                    
        
        
        print('LOSS GALE2')
        bot.edit_message_text(table+"\n============================== \n                        LOSS ✖", message_canal.sender_chat.id, message_canal.message_id, parse_mode='HTML', disable_web_page_preview=True)
        time.sleep(1)
        bot.send_sticker(canal, sticker=stiker_loss)
        time.sleep(3)
        raspagem()
        
     
                            
raspagem()



