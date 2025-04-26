import telebot
from telebot import types
import time
from utils import Blaze
from apostar import Canal
import base64
import re
import json

class bot_telegram:
    def __init__(self):
        with open("id.txt", "r") as f:
            content = [line.strip('\n') for line in f]
            CHAVE_API = content[0]

        self.chave = str(base64.b64decode(CHAVE_API), 'utf-8')
        self.bot = telebot.TeleBot(self.chave)
        self.blaze = Blaze()
        

        self.chatId = []
        self.VER_ESTRATEGIAS = "ver_estrategias"
        self.INSERIR_ESTRATEGIAS = "inserir_estrategias"
        self.REMOVER_ESTRATEGIAS = "remover_estrategias"
        self.VER_CANAL = "ver_canal"
        self.INSERIR_CANAL = "inserir_canal"
        self.REMOVER_CANAL = "remover_canal"
        self.VER_MENSAGENS = "ver_msgs"
        self.MSG_ATENCAO = "msg_atencao"
        self.MSG_CONFIRMA = "msg_confirma"
        self.MSG_GREEN = "msg_green"
        self.MSG_RED = "msg_red"
        self.VER_PLACAR = "ver_placar"
        self.ENVIAR_PLACAR = "enviar_placar"
        self.INICIAR = "iniciar"
        self.PARAR = "parar"

        self.estrategias_ativas = []
        self.canais_ativos = []
        self.step_atual = ""

        self.mensagem_atencao = ""
        self.mensagem_confirmacao = ""
        self.mensagem_green = ""
        self.mensagem_red = ""

        self.count_win = 0
        self.count_loss = 0
        self.count_g0 = 0
        self.count_g1 = 0
        self.count_g2 = 0
        self.perdas = 0

        self.msg_placar = """📊Resultados do bot até agora:

                            *Acertos:* {count_win}
                            *Não bateu:* {count_loss}

                            *Win na 1ª entrada:* {count_win_1}
                            *Win gale 1x:* {count_win_g1}
                            *Win gale 2x:* {count_win_g2}

                            *assertividade:* {assertividade}%"""

        self.kill = False
        self.ativo = False

        self.cores_ultima_aposta = ""
        self.apostou = False
        self.venceu = False
        # self.profit = 0
        self.cor_ultimo = ""
        self.giroAtualId = ""
        self.giroUltimoId = ""
        self.historico = []


        @self.bot.message_handler(commands=["start"])
        def sendInfos(mensagem):
            self.sendKeyboard(mensagem.chat.id)
            if mensagem.chat.id not in self.chatId:
                self.chatId.append(mensagem.chat.id)


        @self.bot.message_handler(commands=["help"])
        def sendInfos(mensagem):
            msg = """{cor} - substituido por cor que deve apostar no sinal
            {atual} - substituido por cor anterior à entrada
            {perdas} - substituido por quantos gales teve no sinal"""
            self.bot.send_message(mensagem.chat.id, msg)

        @self.bot.message_handler(func=lambda message: True)
        def setConfiguracao(mensagem):
            try:
                #ESTRATEGIAS
                if self.step_atual == self.INSERIR_ESTRATEGIAS:
                    valor = mensagem.text
                    self.definirEstrategias(mensagem.chat.id, valor)
                elif self.step_atual == self.REMOVER_ESTRATEGIAS:
                    valor = mensagem.text
                    if valor not in self.estrategias_ativas:
                        self.bot.send_message(mensagem.chat.id, "Estratégia não existe")
                    else:
                        self.estrategias_ativas.remove(valor)
                        self.mandarMensagem("Estratégia removida com sucesso")
                #CANAIS
                elif self.step_atual == self.INSERIR_CANAL:
                    valor = mensagem.text
                    canal = None
                    for c in self.canais_ativos:
                        if c.bot_chatID == valor:
                            canal = c
                            break

                    if not canal:
                        new_canal = Canal(self.chave, valor)
                        self.canais_ativos.append(new_canal)
                        self.mandarMensagem("Canal adicionado com sucesso")
                    else:
                        self.bot.send_message(mensagem.chat.id, "Canal ja incluso")

                elif self.step_atual == self.REMOVER_CANAL:
                    valor = mensagem.text
                    canal = None
                    for c in self.canais_ativos:
                        if c.bot_chatID == valor:
                            canal = c
                            break

                    if not canal:
                        self.bot.send_message(mensagem.chat.id, "Canal não existe")
                    else:
                        self.canais_ativos.remove(canal)
                        self.mandarMensagem("Canal removido com sucesso")
                #MENSAGENS
                elif self.step_atual == self.MSG_ATENCAO:
                    self.mensagem_atencao = mensagem.text
                    self.mandarMensagem("Mensagem de atenção atualizada")
                elif self.step_atual == self.MSG_CONFIRMA:
                    self.mensagem_confirmacao = mensagem.text
                    self.mandarMensagem("Mensagem de confirmação atualizada")
                elif self.step_atual == self.MSG_GREEN:
                    self.mensagem_green = mensagem.text
                    self.mandarMensagem("Mensagem de green atualizada")
                elif self.step_atual == self.MSG_RED:
                    self.mensagem_red = mensagem.text
                    self.mandarMensagem("Mensagem de red atualizada")

                valores = {}
                valores["atencao"] = self.mensagem_atencao
                valores["condirmacao"] = self.mensagem_confirmacao
                valores["win"] = self.mensagem_green
                valores["loss"] = self.mensagem_red
                valores["estrategias"] = self.estrategias_ativas

                canais = []
                for canal in self.canais_ativos:
                    canais.append(canal.bot_chatID)
                valores["canais"] = canais

                with open("configuracoes.txt", "w", encoding='utf-8-sig') as f:
                    f.write(str(valores))
                    f.close()
            except:
                self.bot.send_message(mensagem.chat.id, "Ocorreu um erro")
            self.step_atual = ""
            self.sendKeyboard(mensagem.chat.id)


        @self.bot.callback_query_handler(func=lambda call: True)
        def handle_query(call):
            try:
                #ESTRATEGIAS
                if call.data == self.VER_ESTRATEGIAS:
                    msg = "Estratégias ativas:\n"
                    for est in self.estrategias_ativas:
                        msg += f"{est}\n"
                    self.bot.edit_message_text(chat_id=call.message.chat.id,
                                           text=msg,
                                           message_id=call.message.message_id)

                    self.sendKeyboard(call.message.chat.id)

                elif call.data == self.INSERIR_ESTRATEGIAS:
                    self.step_atual = self.INSERIR_ESTRATEGIAS
                    self.bot.edit_message_text(chat_id=call.message.chat.id,
                                           text="Informe a estratégia para inserir",
                                           message_id=call.message.message_id)

                elif call.data == self.REMOVER_ESTRATEGIAS:
                    self.step_atual = self.REMOVER_ESTRATEGIAS
                    self.bot.edit_message_text(chat_id=call.message.chat.id,
                                           text="Informe a estratégia para remover",
                                           message_id=call.message.message_id)
                #CANAIS
                elif call.data == self.VER_CANAL:
                    msg = "Canais ativos:\n"
                    for est in self.canais_ativos:
                        msg += f"{est.bot_chatID}\n"
                    self.bot.edit_message_text(chat_id=call.message.chat.id,
                                           text=msg,
                                           message_id=call.message.message_id)

                    self.sendKeyboard(call.message.chat.id)

                elif call.data == self.INSERIR_CANAL:
                    self.step_atual = self.INSERIR_CANAL
                    self.bot.edit_message_text(chat_id=call.message.chat.id,
                                           text="Informe o id do canal para inserir",
                                           message_id=call.message.message_id)

                elif call.data == self.REMOVER_CANAL:
                    self.step_atual = self.REMOVER_CANAL
                    self.bot.edit_message_text(chat_id=call.message.chat.id,
                                           text="Informe o id do canal para remover",
                                           message_id=call.message.message_id)
                #MENSAGENS
                elif call.data == self.VER_MENSAGENS:
                    msg = f"Aviso prévio:\n{self.mensagem_atencao} \n\n\n"
                    msg += f"Confirmação aposta:\n{self.mensagem_confirmacao} \n\n\n"
                    msg += f"Vitória:\n{self.mensagem_green} \n\n\n"
                    msg += f"Derrota:\n{self.mensagem_red} \n\n\n"
                    self.bot.edit_message_text(chat_id=call.message.chat.id,
                                           text=msg,
                                           message_id=call.message.message_id)

                    self.sendKeyboard(call.message.chat.id)

                elif call.data == self.MSG_ATENCAO:
                    self.step_atual = self.MSG_ATENCAO
                    self.bot.edit_message_text(chat_id=call.message.chat.id,
                                           text="Informe a mensagem de ATENÇÃO",
                                           message_id=call.message.message_id)

                elif call.data == self.MSG_CONFIRMA:
                    self.step_atual = self.MSG_CONFIRMA
                    self.bot.edit_message_text(chat_id=call.message.chat.id,
                                           text="Informe a mensagem de CONFIRMAÇÃO",
                                           message_id=call.message.message_id)

                elif call.data == self.MSG_GREEN:
                    self.step_atual = self.MSG_GREEN
                    self.bot.edit_message_text(chat_id=call.message.chat.id,
                                           text="Informe a mensagem de GREEN",
                                           message_id=call.message.message_id)

                elif call.data == self.MSG_RED:
                    self.step_atual = self.MSG_RED
                    self.bot.edit_message_text(chat_id=call.message.chat.id,
                                           text="Informe a mensagem de RED",
                                           message_id=call.message.message_id)
                # PLACAR
                elif call.data == self.VER_PLACAR:
                    msg = self.formatarMensagem(self.msg_placar)
                    self.bot.edit_message_text(chat_id=call.message.chat.id,
                                               text=msg,
                                               message_id=call.message.message_id)

                    self.sendKeyboard(call.message.chat.id)

                elif call.data == self.ENVIAR_PLACAR:
                    msg = self.formatarMensagem(self.msg_placar)
                    self.enviarMensagemCanal(msg)
                    self.bot.edit_message_text(chat_id=call.message.chat.id,
                                               text="Placar enviado para os grupos",
                                               message_id=call.message.message_id)
                    time.sleep(1)
                    self.sendKeyboard(call.message.chat.id)
                # COMANDOS
                elif call.data == self.INICIAR:
                    self.bot.edit_message_text(chat_id=call.message.chat.id,
                                               text="Bot iniciando",
                                               message_id=call.message.message_id)
                    time.sleep(1)
                    self.ativo = True
                    self.mandarMensagem("Bot iniciado")
                    self.sendKeyboard(call.message.chat.id)
                    self.iniciarBlaze()

                elif call.data == self.PARAR:
                    self.kill = True
                    self.bot.edit_message_text(chat_id=call.message.chat.id,
                                               text="Bot parando",
                                               message_id=call.message.message_id)
                    time.sleep(2)
                    self.sendKeyboard(call.message.chat.id)
            except:
                self.bot.send_message(call.message.chat.id, "Ocorreu um erro")
                self.iniciarBlaze()


    def start(self):
        self.getValoresDefault()
        while True:
            # bot.polling()
            self.bot.infinity_polling(timeout=1, long_polling_timeout=1)
            self.bot.infinity_polling(True)

    def getValoresDefault(self):
        try:
            with open("configuracoes.txt", "r", encoding='utf-8-sig') as f:
                t = f.read().replace("'", '"')
                texto = json.loads(t)
                f.close()

            if texto:
                self.mensagem_atencao = texto.get("atencao", "")
                self.mensagem_confirmacao = texto.get("condirmacao", "")
                self.mensagem_green = texto.get("win", "")
                self.mensagem_red = texto.get("loss", "")
                self.estrategias_ativas = texto.get("estrategias", [])
                for canal in texto.get("canais", []):
                    self.canais_ativos.append(Canal(self.chave, canal))
        except: pass

    def sendKeyboard(self, chatId):
        markup = self.makeKeyboard()
        self.bot.send_message(chat_id=chatId,
                              text="Configurações",
                              reply_markup=markup,
                              parse_mode='HTML')

    def makeKeyboard(self):
        atencao = "configurada" if self.mensagem_atencao else "configurar"
        confirma = "configurada" if self.mensagem_confirmacao else "configurar"
        green = "configurada" if self.mensagem_green else "configurar"
        red = "configurada" if self.mensagem_red else "configurar"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text=f"VER ESTRATÉGIAS 🎲", callback_data=self.VER_ESTRATEGIAS))
        markup.add(
            types.InlineKeyboardButton(text=f"INSERIR ESTRATÉGIA", callback_data=self.INSERIR_ESTRATEGIAS),
            types.InlineKeyboardButton(text=f"REMOVER ESTRATÉGIA", callback_data=self.REMOVER_ESTRATEGIAS)
        )

        markup.add(types.InlineKeyboardButton(text=f"VER CANAIS 🔔", callback_data=self.VER_CANAL))
        markup.add(
            types.InlineKeyboardButton(text=f"INSERIR CANAL", callback_data=self.INSERIR_CANAL),
            types.InlineKeyboardButton(text=f"REMOVER CANAL", callback_data=self.REMOVER_CANAL)
        )

        markup.add(types.InlineKeyboardButton(text=f"VER MENSAGENS ✉", callback_data=self.VER_MENSAGENS))
        markup.add(
            types.InlineKeyboardButton(text=f"MENSAGEM ATENÇÃO ‼ {atencao}", callback_data=self.MSG_ATENCAO),
            types.InlineKeyboardButton(text=f"MENSAGEM CONFIRMAÇÃO 🔝 {confirma}", callback_data=self.MSG_CONFIRMA)
        )
        markup.add(
            types.InlineKeyboardButton(text=f"MENSAGEM GREEN ✅ {green}", callback_data=self.MSG_GREEN),
            types.InlineKeyboardButton(text=f"MENSAGEM RED ❌ {red}", callback_data=self.MSG_RED)
        )

        markup.add(
            types.InlineKeyboardButton(text=f"VER PLACAR 📊", callback_data=self.VER_PLACAR),
            types.InlineKeyboardButton(text=f"ENVIAR PLACAR 📲", callback_data=self.ENVIAR_PLACAR)
        )
        if not self.ativo:
            markup.add(
                types.InlineKeyboardButton(text=f"INICIAR 🟢", callback_data=self.INICIAR)
            )
        else:
            markup.add(
                types.InlineKeyboardButton(text=f"PARAR 🔴", callback_data=self.PARAR)
            )


        return markup

    def definirEstrategias(self, id, pEstrategias):
        pEstrategias = re.split(r'[\n\t\f\v\r ]+', pEstrategias)
        if not pEstrategias[0]:
            pEstrategias.pop(0)
        for estrategia in pEstrategias:
            # estrategia = self.formatEstrategia(estrategia, '=', ',', 1)
            est = estrategia.split("=")
            if len(est[0]) < 2:
                self.bot.send_message(id, "As estratégias devem ter mais de 2 cores. Garanta que não há espaços dentro da mesma estratégia\nEstratégias não inseridas")
                return
            if not est[1]:
                self.bot.send_message(id, "Cor de entrada na estratégia não identificada. Garanta que não há espaços dentro da mesma estratégia\nEstratégias não inseridas")
                return
            for item in est[0].split(","):
                if item not in ["p", "b", "v"]:
                    self.bot.send_message(id, "As estratégias devem conter apenas 'p', 'v', e 'b'\nEstratégias não inseridas")
                    return
            # for item in est[1].split(","):
            if est[1] not in ["p", "b", "v"]:
                    self.bot.send_message(id, "As estratégias devem conter apenas 'p', 'v', e 'b'\nEstratégias não inseridas")
                    return
            if estrategia not in self.estrategias_ativas:
                self.estrategias_ativas.append(estrategia)
                self.bot.send_message(id, "Estratégia adicionado com sucesso")
            else:
                self.bot.send_message(id, "Estratégia ja ativo")
        msg = "Estratégias padrões definidas:\n"
        for est in self.estrategias_ativas:
            msg += f"{est} \n"
        self.mandarMensagem(msg)
        time.sleep(2)

    def formatarMensagem(self, frase):
        soma = self.count_win + self.count_loss
        soma = 1 if soma == 0 else soma
        assertividade = round(self.count_win / soma * 100, 2)

        frase = frase.replace("{count_win}", f"{self.count_win}")
        frase = frase.replace("{count_loss}", f"{self.count_loss}")
        frase = frase.replace("{count_win_1}", f"{self.count_g0}")
        frase = frase.replace("{count_win_g1}", f"{self.count_g1}")
        frase = frase.replace("{count_win_g2}", f"{self.count_g2}")
        frase = frase.replace("{assertividade}", f"{assertividade}")
        return frase

    def verificaAvisoPrevio(self, lista_resultados, lista_estrategia):
        lista_estrategia.pop(-1)
        if len(lista_resultados) > len(lista_estrategia):
            remover = len(lista_resultados) - len(lista_estrategia)
            for _ in range(remover):
                lista_resultados.pop(0)

        return lista_estrategia == lista_resultados

    def verificaSeAposta(self, lista_resultados, lista_estrategia):

        if len(lista_resultados) > len(lista_estrategia):
            remover = len(lista_resultados) - len(lista_estrategia)
            for _ in range(remover):
                lista_resultados.pop(0)

        return lista_estrategia == lista_resultados
    
    def addResultadoHistorico(self, cor, count=0):

        if cor in ["p", "b", "v"]:
            self.cor_ultimo = cor
            if (len(self.historico)) > 19:
                self.historico.pop(0)
            self.historico.append(cor)
        elif count < 2:
            time.sleep(1)
            # result = self.blaze.getResultado(self.giroUltimoId)
            result = self.blaze.getUltimoResultado()
            cor = f"{result.get('color')}".replace("0", "b").replace("1", "v").replace("2", "p")
            c = count + 1
            self.addResultadoHistorico(cor, c)
        else:
            print("não foi possivel obter o ultimo resultado")
            print(self.giroUltimoId)
            self.historico.append(cor)

    def formatarCor(self, cor):
        retorno = cor.replace("p", "⬛").replace("v", "🟥")
        return retorno

    def iniciarBlaze(self):
        self.kill = False
        s = self.blaze.getStatusRoleta()
        self.giroUltimoId = s["id"]
        self.historico = self.blaze.getHistorico()
        complete = False
        if s["status"] == "complete":
            complete = True
        while True:
            if self.kill:
                self.ativo = False
                break
            status = self.blaze.getStatusRoleta()
            self.ativo = True
            if status["status"] == "complete" and not complete:
                complete = True
                # result = self.blaze.getResultado(self.giroUltimoId)
                result = self.blaze.getUltimoResultado()
                cor = f"{result.get('color')}".replace("0", "b").replace("1", "v").replace("2", "p")
                self.addResultadoHistorico(cor)
                self.apagarAviso()
                for est in self.estrategias_ativas:
                    estrategia_lista = est.split("=")[0].split(",")
                    if self.verificaSeAposta(self.historico.copy(), estrategia_lista.copy()):
                        msg = self.mensagem_confirmacao.replace("{cor}", self.formatarCor(est.split("=")[1])) \
                            .replace("{atual}", self.formatarCor(estrategia_lista[-1])) \
                            .replace("{perdas}", f"{self.perdas}")
                        self.enviarConfirmacao(msg)
                        self.apostar(est.split("=")[1])
                    elif self.verificaAvisoPrevio(self.historico.copy(), estrategia_lista.copy()):
                        msg = self.mensagem_atencao.replace("{cor}", self.formatarCor(est.split("=")[1])) \
                            .replace("{atual}", self.formatarCor(estrategia_lista[-1])) \
                            .replace("{perdas}", f"{self.perdas}")
                        self.enviarAviso(msg)
                time.sleep(3)

            if status["status"] == "waiting" and self.giroUltimoId != status["id"]:
                complete = False
                self.giroUltimoId = status["id"]

                time.sleep(3)

            if status["status"] == "rolling":
                time.sleep(3)
        self.mandarMensagem("Bot interrompido")
        
    def apostar(self, cores):
        self.cores_ultima_aposta = f"b {cores}"
        self.venceu = False
        self.perdas = 0
        time.sleep(15)
        complete = False
        while True:
            if self.kill:
                break
            status = self.blaze.getStatusRoleta()
            if status["status"] == "complete" and not complete:
                complete = True
                time.sleep(3)

            if status["status"] == "waiting" and self.giroAtualId != status["id"]:
                self.verificaSeVenceu()

                if self.venceu:
                    self.count_win += 1
                    if self.perdas == 0:
                        self.count_g0 += 1
                    elif self.perdas == 1:
                        self.count_g1 += 1
                    elif self.perdas == 2:
                        self.count_g2 += 1
                    msg = self.mensagem_green.replace("{cor}", self.formatarCor(self.cor_ultimo))\
                        .replace("{perdas}", f"{self.perdas}")
                    self.enviarResultado(msg)
                    self.historico = []
                    return
                elif self.perdas >= 3:
                    self.count_loss += 1
                    msg = self.mensagem_red.replace("{cor}", self.formatarCor(self.cor_ultimo))\
                        .replace("{perdas}", f"{self.perdas}")
                    self.enviarResultado(msg)
                    self.historico = []
                    return
                self.perdas += 1
                self.giroAtualId = status["id"]

            if status["status"] == "rolling":
                time.sleep(4)

    def verificaSeVenceu(self):
        result = self.blaze.getUltimoResultado()
        self.cor_ultimo = f"{result.get('color')}".replace("0", "b").replace("1", "v").replace("2", "p")
        cor = self.cor_ultimo.lower()

        self.venceu = cor in self.cores_ultima_aposta.lower()
        if self.venceu:
            self.cores_ultima_aposta = ""

    def mandarMensagem(self, texto):
        for chat in self.chatId:
            self.bot.send_message(chat, texto)

    def enviarMensagemCanal(self, texto):
        for canal in self.canais_ativos:
            try:
                canal.sendMessage(texto)
            except:
                self.mandarMensagem(f"Falha ao enviar mensagem para o canal de ID {canal.bot_chatID}")

    def enviarAviso(self, texto):

        try:

            for canal in self.canais_ativos:
                try:
                    
                    canal.post_api('alert', texto, canal.bot_chatID)
                    canal.sendAviso(texto)

                except:
                    self.mandarMensagem(f"Falha ao enviar aviso para o canal de ID {canal.bot_chatID}")
        
        except Exception as e:
            print(e)

    def apagarAviso(self):

        try:
            
            for canal in self.canais_ativos:
                try:
                    
                    status = canal.apagarAviso()

                    if status != 0:
                        texto = ['Entrada Não Confirmada']
                    
                        canal.post_api('denied', texto, canal.bot_chatID)
                        self.avisoId = 0

                except:
                    self.mandarMensagem(f"Falha ao apagar aviso para o canal de ID {canal.bot_chatID}")

        except Exception as e:
            print(e)
        
    def enviarConfirmacao(self, texto):
        
        for canal in self.canais_ativos:

            try:
                canal.post_api('confirm', texto, canal.bot_chatID)
                canal.sendConfirmation(texto)
            except:
                self.mandarMensagem(f"Falha ao enviar confirmação para o canal de ID {canal.bot_chatID}")

    def enviarResultado(self, texto):

        for canal in self.canais_ativos:
            try:
                canal.post_api('success', texto, canal.bot_chatID)
                canal.sendResult(texto)
            except:
                self.mandarMensagem(f"Falha ao enviar placar para o canal de ID {canal.bot_chatID}")




if __name__ == '__main__':
    bot = bot_telegram()
    bot.start()
