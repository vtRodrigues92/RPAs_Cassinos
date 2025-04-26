import requests
import time
from datetime import datetime, timedelta
import threading
from telethon import TelegramClient, events
import asyncio
from telegram.ext import *
from telebot import *



class Bot(threading.Thread):
    def __init__(self, token, id, val, esp, confirmacao, final):
        self.ultimo = 0
        self.cantos = []
        self.telegram_bot_token = token
        self.destino = id
        self.validade = int(val)
        self.espera = int(esp)
        self.mensagem_confirmacao = confirmacao
        self.mensagem_final = final
        threading.Thread.__init__(self)

    def pegar_chaves(self):
        with open ('senhas.txt', 'r', encoding='UTF-8') as file:
            arquivo = file.readlines()

            api_id = arquivo[0].split(' ')[1].replace('\n','')
            api_hash = arquivo[1].split(' ')[1].replace('\n','')
            phone = arquivo[2].split(' ')[1].replace('\n','')
            CHAVE_API = arquivo[3].split(' ')[1]

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        client = TelegramClient(phone, api_id, api_hash, loop=loop)

        sessao = 'Repassar Mensagem'

        return client, CHAVE_API


    def listar_canais_telegram(self, client):
        global canais
        
        try:

            dicionario_canais_telegram = {}
            client.start()

            for canal in client.iter_dialogs():
                if canal.is_channel:
                    if canal.id < 0:
                        dicionario_canais_telegram[canal.title] = canal.id
                        #print(f'Grupo: {canal.title}')
                        #print(f'id: {canal.id}')
                    
                    #else:
                    #    print(f'Nome: {canal.title}')
                    #    print(f'id: {canal.id}')
                    #print('-------------------')
                
            client.disconnect()

            return dicionario_canais_telegram
        
        except Exception as e:
            print(e)


    def telegram_bot_sendtext(self, bot_message):
        send_text = f'https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage?chat_id={self.destino}&parse_mode=Markdown&text={bot_message}&disable_web_page_preview=true'
        print(send_text)
        response = requests.get(send_text)
        # print(response.json())
        with open(f'enviados.txt', "a", encoding="utf8") as outfile:
            outfile.write(bot_message)
            outfile.write("\n")
        return response.json()


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


    def get_canais(self):
        
        global dicionario_canais_telegram
        
        try:

            dicionario_canais_telegram = {}

            for canal in client.iter_dialogs():
                if canal.is_channel:
                    if canal.id < 0:
                        dicionario_canais_telegram[canal.title] = canal.id
                        #print(f'Grupo: {canal.title}')
                        #print(f'id: {canal.id}')
                    
                    #else:
                    #    print(f'Nome: {canal.title}')
                    #    print(f'id: {canal.id}')
                    #print('-------------------')
                
            return dicionario_canais_telegram
    
        except:pass


    def login(self):
        global client

        with open ('senhas.txt', 'r', encoding='UTF-8') as file:
            arquivo = file.readlines()

            api_id = arquivo[0].split(' ')[1].replace('\n','')
            api_hash = arquivo[1].split(' ')[1].replace('\n','')
            phone = arquivo[2].split(' ')[1].replace('\n','')
            CHAVE_API = arquivo[3].split(' ')[1]

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        client = TelegramClient(phone, api_id, api_hash)
        client.start()


    async def send_messages(self, chat, message):
        
        await client.send_message(chat, message)

    
    def run(self):

        ##client, CHAVE_API = self.pegar_chaves()

        self.login()
        #dicionario_canais_telegram = self.listar_canais_telegram(client)
        #canais = self.get_canais()

        while True:
            try:
                
                #mensagemId = self.telegram_bot_sendtext(self.mensagem_confirmacao)
                self.loop.run_until_complete(self.send_messages(int(self.destino), self.mensagem_confirmacao))

                #self.send_messages(canais, self.destino, 'Hi', )

                time.sleep(self.validade)

                self.loop.run_until_complete(self.send_messages(int(self.destino), self.mensagem_confirmacao))

                #mensagemId = self.telegram_bot_sendtext(self.mensagem_final)

                time.sleep(self.espera)

            except:
                pass

