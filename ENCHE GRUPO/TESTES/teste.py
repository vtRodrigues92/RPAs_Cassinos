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


#bot.send_message(canal, "OLÁ")

print('\n\n##### AGUARDANDO COMANDOS ######\n\n')

logger = logging.getLogger()





@bot.message_handler(commands=["start"])
def start(message):
    try:
        
        
        # Formatando para envio no telegram
        headers2 = ['     🔔ATENTOS, POSSIVEL ENTRADA!🔔                                ']
        data2 = [
        ["🌐 <a href='https://blaze.com/pt/games/double'>Clique para ir para a Blaze</a>"]
                
        ]
            
        table2 = columnar(data2, headers2, no_borders=True)

        message_alerta = bot.send_message(canal, table2, parse_mode='HTML')
        message_alerta
            
        
        
        
        
        bot.send_message(message.chat.id, '🤖 Robô iniciado 📊✅')
        message_canal = bot.send_message(canal, "Alguma coisa")
        
        bot.send_message(message.chat.id, '<a href="http://www.example.com/">inline URL</a>', parse_mode='HTML')
        #bot.send_message(chat_id=update.message.chat_id, text="<a href='https://www.google.com/'>Google</a>", parse_mode='HTML')
        
        
        message_canal
        
        
        ''' Responder mensagem '''
        bot.reply_to(message_canal, "Valeu")
        
    
        ''' editar mensagem '''
        
        bot.edit_message_text("Editei fdp", message_canal.sender_chat.id, message_canal.message_id)
    
    except Exception as f:
        logger.error('Exception ocorrido no try do While: ' + repr(f))
        time.sleep(10)
        



bot.polling()













''' DEFININDO O RESULTADO
    
bot.edit_message_text(table +"\n ======= WINNNN DE PRIMEIRA!! ✅✅ =======", message_canal.sender_chat.id, message_canal.message_id, parse_mode='HTML', disable_web_page_preview=True)
time.sleep(3)
message_canal
bot.edit_message_text(table+"\n======= WINNNN GALE1!! ✅🐔 =======", message_canal.sender_chat.id, message_canal.message_id, parse_mode='HTML', disable_web_page_preview=True)
time.sleep(3)
message_canal
bot.edit_message_text(table+"\n======= WINNNN GALE2!! ✅🐔🐔 =======", message_canal.sender_chat.id, message_canal.message_id, parse_mode='HTML', disable_web_page_preview=True)
time.sleep(3)
message_canal
bot.edit_message_text(table+"\n======= LOSS! ✖ =======", message_canal.sender_chat.id, message_canal.message_id, parse_mode='HTML', disable_web_page_preview=True)
time.sleep(3)
message_canal

time.sleep(3)

bot.reply_to(message_canal,"=================== WINNNN DE PRIMEIRA!! ✅✅ ===================")
message_canal
bot.reply_to(message_canal, "=================== WINNNN GALE1!! ✅🐔 ===================")
message_canal
bot.reply_to(message_canal, "=================== WINNNN GALE2!! ✅🐔🐔 ===================")
message_canal
bot.reply_to(message_canal, "=================== LOSS! ✖ ===================")'''

