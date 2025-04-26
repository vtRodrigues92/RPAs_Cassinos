from cgitb import html
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



######## CONFIGURAÇÕES TELEGRAM ########

CHAVE_API = '5434022871:AAF-mMhUcDuEID9vf-8WnLvZiFPUnjuzk-k'
canal = -1001775325949
bot = telebot.TeleBot(CHAVE_API)




def start():
    
    # Formatando para envio no telegram
    headers2 = ['     🔔ATENTOS, POSSIVEL ENTRADA!🔔                                ']
    data2 = [
    ["🌐 <a href='https://blaze.com/pt/games/double'>Clique para ir para a Blaze</a>"]
            
    ]
        
    table2 = columnar(data2, headers2, no_borders=True)

    message_canal = bot.send_message(canal, table2, parse_mode='HTML')
    
    print(message_canal)
    
    print('enviei')
    
    return message_canal       


    
def resposta(*args):
           
    edit_message = bot.edit_message_text("Editei fdp", message_canal.sender_chat.id, message_canal.message_id)

    edit_message
    
    print('respondi')

start()

return start()



'''RESULTADO SEM GALE'''
                    
                    ''' IDENTIFICANDO A PROXIMA RODADA'''
                    
                    while True:
                        time.sleep(1)
                        proxima_rodada = browser.find_element_by_xpath('//*[@id="roulette-timer"]/div[1]').text
                        proxima_rodada = proxima_rodada.split('\n')
                        proxima_rodada = proxima_rodada[0]
                        
                        repeticoes = tb_horario.count(hora_corrente)
                        
                        
                        if proxima_rodada == 'Blaze Girou':
                            time.sleep(3)
                        
                            if not repeticoes == 2:
                                cor = Color.from_string(browser.find_element_by_xpath('//*[@id="roulette-recent"]/div/div[1]/div[1]/div/div').value_of_css_property('background-color')).hex
                        
                                if cor != branco:
                                    numero = int(browser.find_element_by_xpath('//*[@id="roulette-recent"]/div/div[1]/div[1]/div/div').text)
                                else:
                                    # WIN SEM GALE
                                    bot.edit_message_text(table +"\n === WINNNN DE PRIMEIRA!! ✅✅ ===", message_canal.sender_chat.id, message_canal.message_id, parse_mode='HTML', disable_web_page_preview=True)
                                    
                                    time.sleep(3)
                                    break
                
                                if cor == vermelho or cor == branco:
                                    #message_canal = bot.send_message(canal,table, parse_mode='HTML', disable_web_page_preview=True)
                                    bot.edit_message_text(table +"\n ======= WINNNN DE PRIMEIRA!! ✅✅ =======", message_canal.sender_chat.id, message_canal.message_id, parse_mode='HTML', disable_web_page_preview=True)

                                    time.sleep(3)
                                    break
                            
                                # RESULTADO GALE1
                                
                                else:
                                    while True:
                                        #time.sleep(20)
                                        ''' IDENTIFICANDO A PROXIMA RODADA'''
                                        proxima_rodada = browser.find_element_by_xpath('//*[@id="roulette-timer"]/div[1]').text
                                        proxima_rodada = proxima_rodada.split('\n')
                                        proxima_rodada = proxima_rodada[0]
                                        
                                        repeticoes = tb_horario.count(hora_corrente)
                                        
                                        
                                        if proxima_rodada == 'Blaze Girou':
                                            time.sleep(3)
                                            if not repeticoes == 2:
                                                cor = Color.from_string(browser.find_element_by_xpath('//*[@id="roulette-recent"]/div/div[1]/div[1]/div/div').value_of_css_property('background-color')).hex

                                                if cor != branco:
                                                    numero = int(browser.find_element_by_xpath('//*[@id="roulette-recent"]/div/div[1]/div[1]/div/div').text)
                                                else:
                                                    # WIN GALE 1
                                                    resultado_gale1(table, message_canal)
                                                    time.sleep(3)
                                                    break
                                                if cor == vermelho or cor == branco:
                                                    #message_canal = bot.send_message(canal,table, parse_mode='HTML', disable_web_page_preview=True)
                                                    #bot.edit_message_text(table +"\n ======= WINNNN GALE1 ✅🐔 =======", message_canal.sender_chat.id, message_canal.message_id, parse_mode='HTML', disable_web_page_preview=True)
                                                    resultado_gale1(table, message_canal)
                                                    time.sleep(3)
                                                    break
                                                        
                                        # RESULTADO GALE 2

                                                else:
                                                    while True:
                                                        #time.sleep(20)
                                                        ''' IDENTIFICANDO A PROXIMA RODADA'''
                                                        proxima_rodada = browser.find_element_by_xpath('//*[@id="roulette-timer"]/div[1]').text
                                                        proxima_rodada = proxima_rodada.split('\n')
                                                        proxima_rodada = proxima_rodada[0]
                                                        
                                                        repeticoes = tb_horario.count(hora_corrente)
                                                        
                                                        
                                                        if proxima_rodada == 'Blaze Girou':
                                                            time.sleep(3)
                                                            if not repeticoes == 2:
                                                                cor = Color.from_string(browser.find_element_by_xpath('//*[@id="roulette-recent"]/div/div[1]/div[1]/div/div').value_of_css_property('background-color')).hex

                                                                if cor != branco:
                                                                    numero = int(browser.find_element_by_xpath('//*[@id="roulette-recent"]/div/div[1]/div[1]/div/div').text)
                                                                else:    
                                                                    # WIN GALE 2
                                                                    resultado_gale2(table, message_canal)
                                                                    #message_canal = bot.send_message(canal,table, parse_mode='HTML', disable_web_page_preview=True)
                                                                    #bot.edit_message_text(table+"\n======= LOSS ✖ =======", message_canal.sender_chat.id, message_canal.message_id, parse_mode='HTML', disable_web_page_preview=True)
                                                                    time.sleep(3)
                                                                    break
                                                                    
                                                                    
                                                                if cor == vermelho or cor == branco:
                                                                    #bot.edit_message_text(table +"\n ======= WINNNN GALE2!! ✅🐔🐔 =======", message_canal.sender_chat.id, message_canal.message_id, parse_mode='HTML', disable_web_page_preview=True)
                                                                    resultado_gale2(table, message_canal)
                                                                    time.sleep(3)
                                                                    break
                                                                else:
                                                                    bot.edit_message_text(table+"\n======= LOSS ✖ =======", message_canal.sender_chat.id, message_canal.message_id, parse_mode='HTML', disable_web_page_preview=True)
                                                                    #resultado_loss(table, message_canal)
                                                                    time.sleep(3)
                                                                    break
                                                                    
                
                
















# ''' DEFININDO O RESULTADO '''
        
#bot.edit_message_text(table +"\n ======= WINNNN DE PRIMEIRA!! ✅✅ =======", message_canal.sender_chat.id, message_canal.message_id, parse_mode='HTML', disable_web_page_preview=True)
#time.sleep(3)
#message_canal
#bot.edit_message_text(table+"\n======= WINNNN GALE1!! ✅🐔 =======", message_canal.sender_chat.id, message_canal.message_id, parse_mode='HTML', disable_web_page_preview=True)
#time.sleep(3)
#message_canal
#bot.edit_message_text(table+"\n======= WINNNN GALE2!! ✅🐔🐔 =======", message_canal.sender_chat.id, message_canal.message_id, parse_mode='HTML', disable_web_page_preview=True)
#time.sleep(3)
#message_canal
#bot.edit_message_text(table+"\n======= LOSS! ✖ =======", message_canal.sender_chat.id, message_canal.message_id, parse_mode='HTML', disable_web_page_preview=True)
#time.sleep(3)
#message_canal

#time.sleep(3)

#bot.reply_to(message_canal,"=================== WINNNN DE PRIMEIRA!! ✅✅ ===================")
#message_canal
#bot.reply_to(message_canal, "=================== WINNNN GALE1!! ✅🐔 ===================")
#message_canal
#bot.reply_to(message_canal, "=================== WINNNN GALE2!! ✅🐔🐔 ===================")
#message_canal
#bot.reply_to(message_canal, "=================== LOSS! ✖ ===================")







#________________________________________________________



''' FUNÇÃO SE CAIR NO VERMELHO '''
            
            if cor == vermelho:
                cor = '🔴'
                tb_cor.append(cor_str)
                
                contagem_vermelho = tb_cor.count('VERMELHO') # EXCLUIR
                
                if contagem_geral ==  1: #contagem_vermelho:
                    #print(data)
                    #print(tb_horario)
                    print(tb_cor)
                    print('Padrão formado!')
                    print('Enviando sinal Telegram')
                    
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
                    
                    #sinal_telegram(cor, cor_str, canal, bot, table)
                    time.sleep(3)
                else:
                    print('Padrão quebrado! Continuando as Análises!')
                    tb_cor = []    
                    contador = 0
                    break
                    
                    
                '''RESULTADO SEM GALE'''
                
                '''IDENTIFICANDO A PROXIMA RODADA'''
                
                while True:
                    time.sleep(1)
                    proxima_rodada = browser.find_element_by_xpath('//*[@id="roulette-timer"]/div[1]').text
                    proxima_rodada = proxima_rodada.split('\n')
                    proxima_rodada = proxima_rodada[0]
                    
                    #repeticoes = tb_horario.count(hora_corrente)
                    
                    
                    if proxima_rodada == 'Blaze Girou':
                        time.sleep(3)
                        if not repeticoes == 2:
                            cor = Color.from_string(browser.find_element_by_xpath('//*[@id="roulette-recent"]/div/div[1]/div[1]/div/div').value_of_css_property('background-color')).hex
                    
                            if cor != branco:
                                numero = int(browser.find_element_by_xpath('//*[@id="roulette-recent"]/div/div[1]/div[1]/div/div').text)
                            else:
                                # WIN SEM GALE
                                
                                bot.edit_message_text(table +"\n === WINNNN DE PRIMEIRA!! ✅✅ ===", message_canal.sender_chat.id, message_canal.message_id, parse_mode='HTML', disable_web_page_preview=True)
                                
                                #resultado_sgale(table, message_canal)
                                time.sleep(3)
                                break
            
                            if cor == preto or cor == branco:    
                                #message_canal = bot.send_message(canal,table, parse_mode='HTML', disable_web_page_preview=True)
                                #resultado_sgale(table, message_canal)
                                bot.edit_message_text(table +"\n === WINNN DE PRIMEIRA! ✅✅ ===", message_canal.sender_chat.id, message_canal.message_id, parse_mode='HTML', disable_web_page_preview=True)

                                #bot.edit_message_text(table +"\n ======= WINNNN DE PRIMEIRA!! ✅✅ =======", message_canal.sender_chat.id, message_canal.message_id, parse_mode='HTML', disable_web_page_preview=True)
                                break
                        
                            # RESULTADO GALE 1
                                            
                            else:
                                #time.sleep(20)
                                ''' IDENTIFICANDO A PROXIMA RODADA'''
                
                                while True:
                                    proxima_rodada = browser.find_element_by_xpath('//*[@id="roulette-timer"]/div[1]').text
                                    proxima_rodada = proxima_rodada.split('\n')
                                    proxima_rodada = proxima_rodada[0]
                                    
                                    #repeticoes = tb_horario.count(hora_corrente)
                                    
                                    
                                    if proxima_rodada == 'Blaze Girou':
                                        time.sleep(3)
                                        if not repeticoes == 2:
                                            cor = Color.from_string(browser.find_element_by_xpath('//*[@id="roulette-recent"]/div/div[1]/div[1]/div/div').value_of_css_property('background-color')).hex

                                            if cor != branco:
                                                numero = int(browser.find_element_by_xpath('//*[@id="roulette-recent"]/div/div[1]/div[1]/div/div').text)
                                            else:
                                                # WIN GALE 1
                                                resultado_gale1(table, message_canal)
                                                time.sleep(3)
                                                break
                                            if cor == preto or cor == branco:    
                                                #message_canal = bot.send_message(canal,table, parse_mode='HTML', disable_web_page_preview=True)
                                                resultado_gale1(table, message_canal)
                                                
                                                #bot.edit_message_text(table +"\n ======= WINNNN GALE1 ✅🐔 =======", message_canal.sender_chat.id, message_canal.message_id, parse_mode='HTML', disable_web_page_preview=True)
                                                time.sleep(3)
                                                break
                                                    
                                    # RESULTADO GALE 2

                                            else:
                                                #time.sleep(20)
                                                ''' IDENTIFICANDO A PROXIMA RODADA'''

                                                while True:
                                                    proxima_rodada = browser.find_element_by_xpath('//*[@id="roulette-timer"]/div[1]').text
                                                    proxima_rodada = proxima_rodada.split('\n')
                                                    proxima_rodada = proxima_rodada[0]
                                                    
                                                    #repeticoes = tb_horario.count(hora_corrente)
                                                    
                                                    
                                                    if proxima_rodada == 'Blaze Girou':
                                                        time.sleep(3)
                                                        if not repeticoes == 2:
                                                            cor = Color.from_string(browser.find_element_by_xpath('//*[@id="roulette-recent"]/div/div[1]/div[1]/div/div').value_of_css_property('background-color')).hex

                                                            if cor != branco:
                                                                numero = int(browser.find_element_by_xpath('//*[@id="roulette-recent"]/div/div[1]/div[1]/div/div').text)
                                                            else:    
                                                                # WIN GALE 2
                                                                resultado_gale2(table, message_canal)
                                                                #bot.edit_message_text(table+"\n======= LOSS ✖ =======", message_canal.sender_chat.id, message_canal.message_id, parse_mode='HTML', disable_web_page_preview=True)
                                                                time.sleep(3)
                                                                break
                                                                
                                                            if cor == preto or cor == branco:
                                                                #message_canal = bot.send_message(canal,table, parse_mode='HTML', disable_web_page_preview=True)
                                                                resultado_gale2(table, message_canal)
                                                                #bot.edit_message_text(table +"\n ======= WINNNN GALE1 ✅🐔 =======", message_canal.sender_chat.id, message_canal.message_id, parse_mode='HTML', disable_web_page_preview=True)
                                                                time.sleep(3)
                                                                break
                                                            else:
                                                                bot.edit_message_text(table+"\n======= LOSS ✖ =======", message_canal.sender_chat.id, message_canal.message_id, parse_mode='HTML', disable_web_page_preview=True)
                                                                #resultado_loss(table, message_canal)
                                                                time.sleep(3)
                                                                break
    #except Exception as f:
        #    logger.error('Exception ocorrido no try do While: ' + repr(f))
        #    time.sleep(1)                                                   
                                                                    
                                                                    
                                                                    
                                                                    
    else:                                                      
        
        ''' SE O ALERTA NÃO ACONTECER, RESETAR A TABELA DE CORES '''
        print('\n\n')
        print('Padrão quebrado! Reiniciando Análises!!')
        tb_cor = []    
        contador = 0
                       
                        
            


