import requests
import time

class Canal():
    def __init__(self, token, id):
        self.bot_token = token
        self.bot_chatID = id
        self.avisoId = 0
        self.confirmacaoId = 0

    def sendMessage(self, texto):
        self.telegram_bot_sendtext(texto)

    def sendAviso(self, texto):
        mensagem = self.telegram_bot_sendtext(texto)['result']
        self.avisoId = mensagem['message_id']

    def apagarAviso(self):
        if self.avisoId == 0:
            return
        self.telegram_bot_deletMessage(self.avisoId)
        self.avisoId = 0

    def sendConfirmation(self, texto):
        mensagem = self.telegram_bot_sendtext(texto)['result']
        self.confirmacaoId = mensagem['message_id']
        self.avisoId = 0

    def sendResult(self, texto):
        self.telegram_bot_replyMessage(texto, self.confirmacaoId)['result']
        self.confirmacaoId = 0
        self.avisoId = 0

    def telegram_bot_sendtext(self, bot_message):
        send_text = f'https://api.telegram.org/bot{self.bot_token}/sendMessage?chat_id={self.bot_chatID}&parse_mode=Markdown&text={bot_message}&disable_web_page_preview=true'
        response = requests.get(send_text)
        return response.json()

    def telegram_bot_deletMessage(self, message_id):
        send_text = f'https://api.telegram.org/bot{self.bot_token}/deleteMessage?chat_id={self.bot_chatID}&message_id={message_id}'
        response = requests.get(send_text)
        return response.json()

    def telegram_bot_editMessage(self, message_id, text):
        send_text = f'https://api.telegram.org/bot{self.bot_token}/editMessageText?chat_id={self.bot_chatID}&message_id={message_id}&text={text}'
        response = requests.get(send_text)
        return response.json()

    def telegram_bot_replyMessage(self, text, message_id):
        send_text = f'https://api.telegram.org/bot{self.bot_token}/sendMessage?chat_id={self.bot_chatID}&reply_to_message_id={message_id}&text={text}&parse_mode=Markdown&disable_web_page_preview=true'
        response = requests.get(send_text)
        return response.json()
