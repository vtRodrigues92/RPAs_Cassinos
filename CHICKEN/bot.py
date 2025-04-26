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


        def gerarCanto(self):

            self.cantos = (["🛎️", "🛎️", "🛎️", "🛎️","🛎️"], 
                        ["🛎️", "🛎️", "🛎️", "🛎️","🛎️"], 
                        ["🛎️", "🛎️", "🛎️", "🛎️","🛎️"], 
                        ["🛎️", "🛎️", "🛎️", "🛎️","🛎️"],
                        ["🛎️", "🛎️", "🛎️", "🛎️","🛎️"])
            
            cont_cantos = 0
        
            for canto in random.sample(self.cantos, len(self.cantos)):
                if "" in canto:
                    continue

                atual = random.randint(0, 4)
                while self.ultimo == atual:
                    atual = random.randint(0, 4)

                self.ultimo = atual
                canto[atual] = "🍗"
                
            
        def formatarTexto(self, texto):
            formatado = ""
            count = 0
            for lista_cantos in self.cantos:
                for canto in lista_cantos:
                    formatado += f"{canto}"
                formatado += "\n"
                
            texto = texto.replace("{result}", formatado)

            now = datetime.now().time()
            hora = datetime.strptime(now.strftime("%H:%M"), "%H:%M")
            hora_max = hora + timedelta(seconds=self.validade)

            texto = texto.replace("{horario}", hora.strftime("%H:%M")).replace("{validade}", hora_max.strftime("%H:%M"))
            return texto


        def run(self):
            bot = telebot.TeleBot(self.telegram_bot_token)

            while True:

                try:

                    self.gerarCanto()
                    
                    texto = self.formatarTexto(self.mensagem_confirmacao)
                    #mensagemId = self.telegram_bot_sendtext(texto, bot)
                    
                    bot.send_message(self.destino, texto)
                    
                    time.sleep(self.espera)

                    texto = self.formatarTexto(self.mensagem_final)
                                    
                    self.telegram_bot_sendtext(texto, bot)

            
                    time.sleep(self.validade)
                
                except Exception as e:
                    print(e)
                    continue



        
