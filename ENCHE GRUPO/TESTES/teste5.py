from matplotlib.style import context
from telegram import *
from telegram.ext import * 
from requests import *
import telebot
from telebot import types


CHAVE_API = '5434022871:AAF-mMhUcDuEID9vf-8WnLvZiFPUnjuzk-k'
canal = -1001775325949
bot = telebot.TeleBot(CHAVE_API)


print('\n\n##### AGUARDANDO COMANDOS ######\n\n')


#logger = logging.getLogger()



def generate_buttons(bts_names, markup):
    for button in bts_names:
        markup.add(types.KeyboardButton(button))
    return markup



@bot.message_handler(commands=['start'])
def start(message):

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(row_width=3)

    #Add to buttons by list with ours generate_buttons function.
    markup = generate_buttons(['Iniciar BOT no Canal FREE', 'Iniciar BOT no Canal VIP', 'Iniciar BOT no Canal FREE E VIP'], markup)
    message = bot.reply_to(message, "🤖 BOT Academia Trader Blaze iniciado ✅",
                            reply_markup=markup)
    
    #Here we assign the next handler function and pass in our response from the user. 
    bot.register_next_step_handler(message, opcoes)


def opcoes(message):
    if message.text in ['Iniciar BOT no Canal FREE']:
         message = bot.reply_to(message, "Ok! Iniciando BOT no Canal FREE...")
         print('Comando: Iniciar BOT no Canal FREE')
         
         global canal
         canal = -1001609828054




bot.polling()
