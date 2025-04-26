import requests
import time
import random
from datetime import datetime, timedelta
import threading
from telebot import *
from telegram.ext import *



class Bot(threading.Thread):
    def __init__(self, token, id, link_afiliado, link_jogo, val, esp, confirmacao, final):
        self.ultimo = 0
        self.cantos = []
        self.telegram_bot_token = token
        self.destino = id
        self.link_afiliado = link_afiliado
        self.link_jogo = link_jogo
        self.validade = int(val)
        self.espera = int(esp)
        self.mensagem_confirmacao = confirmacao
        self.mensagem_final = final
        threading.Thread.__init__(self)


    def telegram_bot_sendtext(self, bot_message, bot):
        
        reply_markup=types.InlineKeyboardMarkup([
        [types.InlineKeyboardButton(text='Cadastre-se aqui', url=self.link_afiliado)],
        [types.InlineKeyboardButton(text='Jogue aqui', url=self.link_jogo)]
        ])

        message = bot.send_message(self.destino, bot_message, reply_markup = reply_markup)

        with open(f'enviados.txt', "a", encoding="utf8") as outfile:
            outfile.write(bot_message)
            outfile.write("\n")
        
        return message


    def telegram_bot_deletMessage(self, message_id):
        send_text = f'https://api.telegram.org/bot{self.telegram_bot_token}/deleteMessage?chat_id={self.destino}&message_id={message_id}'
        response = requests.get(send_text)
        return response.json()


    def telegram_bot_editMessage(self, message_id, text):
        send_text = f'https://api.telegram.org/bot{self.telegram_bot_token}/editMessageText?chat_id={self.destino}&message_id={message_id}&parse_mode=Markdown&text={text}&disable_web_page_preview=true'
        response = requests.get(send_text)
        return response.json()


    def telegram_bot_replyMessage(self, text, message_id):
        send_text = f'https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage?chat_id={self.destino}&reply_to_message_id={message_id}&text={text}&parse_mode=Markdown&disable_web_page_preview=true'
        response = requests.get(send_text)
        return response.json()


    def formatarTexto(self, texto, aposta):
       

        texto = texto.replace("{result}", 
                              aposta)

        return texto


    def post_api(self, status, mensagem):

        url = "https://app.bootbost.com.br/api/v1/call"
        headers = {
        'Content-Type': 'application/json'
        }

        payload = {

                'status': status, #alert | confirm | success | failure | denied
                'chat_id': [self.destino],
                'content': mensagem,
                'link_refer':[self.link_afiliado],
                'link_game_bet':[self.link_jogo]
        
        }

        requests.post(url, headers=headers, json=payload)


    def run(self):
        bot = telebot.TeleBot(self.telegram_bot_token)

        while True:
            
            lista = ['🟥','⬛','🟥','⬛','🟥','⬛','🟥','⬛','🟥','⬛','🟥','⬛','🟥','⬛']
            aposta = random.choice(lista)
            texto = self.formatarTexto(self.mensagem_confirmacao, aposta)
            #mensagemId = self.telegram_bot_sendtext(texto, bot)
            
            mensagemId = self.telegram_bot_sendtext(texto, bot)

            #POST PARA A API
            self.post_api('confirm', texto)
            
            time.sleep(self.espera)
                            
            self.telegram_bot_editMessage(mensagemId.message_id, self.mensagem_final)

            #POST PARA A API
            self.post_api('sucess', self.mensagem_final)

            time.sleep(self.validade)

