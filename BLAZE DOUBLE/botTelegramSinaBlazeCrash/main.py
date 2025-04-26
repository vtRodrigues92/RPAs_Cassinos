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

        self.venceu = False

        self.giroAtualId = ""
        self.giroUltimoId = ""
        self.valor_saida_atual = 0
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
            # try:
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
            # except:
            #     self.bot.send_message(call.message.chat.id, "Ocorreu um erro")


    def start(self):
        self.getValoresDefault()
        while True:
            # bot.polling()
            self.bot.infinity_polling(timeout=3, long_polling_timeout=3)
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
        except:
            pass

    def sendKeyboard(self, chatId):
        markup = self.makeKeyboard()
        self.bot.send_message(chat_id=chatId,
                              text="Configurações Crash",
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

    def definirEstrategias(self, id, texto):
        try:
            linhas = re.split(r'[\n]+', texto)
            estrategias = [i.strip() for i in linhas]
            if not estrategias[0]:
                linhas.pop(0)

            for linha in estrategias:
                if "=" in linha:
                    linha = linha.replace(" =", "=").replace("= ", "=")
                    verde = "🟢🟩💚"
                    preto = "⬛🖤⚫"
                    for char in verde:
                        linha = linha.replace(char, "2")
                    for char in preto:
                        linha = linha.replace(char, "-2")
                    if len(linha.split("=")[0]) < 2:
                        self.mandarMensagem("Estratégia inválida")
                        return
                    if len(linha.split("=")[1].split(" ")) != 1:
                        self.mandarMensagem("Estratégia inválida")
                        return
                    numeros = linha.replace(",", " ").replace("=", " ").split(' ')
                    try:
                        for num in numeros:
                            value = float(num)
                    except:
                        self.mandarMensagem("Valores inválidos")
                        return
                    self.estrategias_ativas.append(linha)

                else:
                    atr = linha.split(" ")
                    if len(atr) != 3:
                        self.mandarMensagem("Estratégia inválida")
                        return
                    try:
                        qtd = int(atr[0])
                        res = float(atr[1].replace(",", "."))
                        aposta = float(atr[2].replace(",", "."))
                    except:
                        self.mandarMensagem("Valores inválidos")
                        return
                    self.estrategias_ativas.append(linha)


            # msg = "Estratégias definidas:"
            # for est in self.estrategias_ativas:
            #     if "=" in est:
            #         msg += f"\n{est}"
            #     else:
            #         atr = est.split(" ")
            #         msg += f"\nRepetindo {atr[0]} vezes resultado {atr[1]}, apostar em {atr[2]}"
            # self.enviarMensagem(id, msg)
            self.mandarMensagem("Estratégias atualizadas")
            return

        except:
            self.enviarMensagem(id, "Estratégia mal formatada")

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

    def verificaAvisoPrevio(self, lista_resultados, estrategia):
        aposta = False
        retorno = {"saida": 0, "apos": 0}
        try:
            if "=" in estrategia:
                analise = estrategia.split("=")[0].split(",")
                apos = analise[-1]
                analise.pop(-1)
                retirar = float(estrategia.split("=")[1])
                qtd = len(analise)
                if len(lista_resultados) >= qtd:
                    aposta = True
                    for x in range(qtd):
                        y = x + 1
                        res = float(analise[-y])
                        if res > 0:
                            if lista_resultados[-y] < res:
                                aposta = False
                                break
                        else:
                            if lista_resultados[-y] > -res:
                                aposta = False
                                break

            else:
                atr = estrategia.split(" ")
                qtd = int(atr[0]) - 1
                res = float(atr[1].replace(",", "."))
                apos = atr[1]
                retirar = float(atr[2].replace(",", "."))

                if len(lista_resultados) >= qtd:
                    aposta = True
                    for x in range(qtd):
                        y = x + 1
                        if res > 0:
                            if lista_resultados[-y] < res:
                                aposta = False
                                break
                        else:
                            if lista_resultados[-y] > -res:
                                aposta = False
                                break

        except:
            aposta = False
            self.mandarMensagem("Erro ao analisar estrategias")

        if aposta:
            retorno["saida"] = retirar
            retorno["apos"] = apos
            return retorno
        else:
            return retorno

    def verificaConfirmacao(self, lista_resultados, estrategia):
        aposta = False
        retorno = {"saida": 0, "apos": 0}
        try:
            if "=" in estrategia:
                analise = estrategia.split("=")[0]
                retirar = float(estrategia.split("=")[1])
                qtd = len(analise.split(","))
                apos = analise.split(",")[-1]
                if len(lista_resultados) >= qtd:
                    aposta = True
                    for x in range(qtd):
                        y = x + 1
                        res = float(analise.split(",")[-y])
                        if res > 0:
                            if lista_resultados[-y] < res:
                                aposta = False
                                break
                        else:
                            if lista_resultados[-y] > -res:
                                aposta = False
                                break

            else:
                atr = estrategia.split(" ")
                qtd = int(atr[0])
                res = float(atr[1].replace(",", "."))
                retirar = float(atr[2].replace(",", "."))
                apos = atr[1]

                if len(lista_resultados) >= qtd:
                    aposta = True
                    for x in range(qtd):
                        y = x + 1
                        if res > 0:
                            if lista_resultados[-y] < res:
                                aposta = False
                                break
                        else:
                            if lista_resultados[-y] > -res:
                                aposta = False
                                break

        except:
            aposta = False
            self.mandarMensagem("Erro ao analisar estrategias")

        if aposta:
            retorno["saida"] = retirar
            retorno["apos"] = apos
            return retorno
        else:
            return retorno


    def iniciarBlaze(self):
        self.kill = False
        s = self.blaze.getStatusCrash()
        self.giroUltimoId = s["id"]
        self.historico = self.blaze.getHistoricoCrash()
        complete = False
        if s["status"] == "complete":
            complete = True
        while True:
            if self.kill:
                self.ativo = False
                break
            status = self.blaze.getStatusCrash()
            self.ativo = True
            if status["status"] == "complete" and not complete:
                complete = True
                result = self.blaze.getUltimoResultadoCrash()
                valor = result.get("crash_point")
                self.historico.append(float(valor))
                # print(self.historico)
                self.apagarAviso()
                for est in self.estrategias_ativas:
                    aposta = self.verificaConfirmacao(self.historico.copy(), est)
                    if aposta.get("saida", "") and aposta.get("saida") > 1:
                        msg = self.mensagem_confirmacao.replace("{cor}", f"{aposta.get('saida')}") \
                            .replace("{atual}", f"{self.historico[-1]}") \
                            .replace("{perdas}", f"{self.perdas}")
                        self.enviarConfirmacao(msg)
                        self.apostar(aposta.get('saida'))
                        break

                    aviso = self.verificaAvisoPrevio(self.historico.copy(), est)
                    if aviso.get("saida", "") and aviso.get("saida") > 1:
                        msg = self.mensagem_atencao.replace("{cor}", f"{aviso.get('saida')}") \
                            .replace("{atual}", f"{aviso.get('apos')}") \
                            .replace("{perdas}", f"{self.perdas}")
                        self.enviarAviso(msg)
                        break
                time.sleep(3)

            if status["status"] == "waiting" and self.giroUltimoId != status["id"]:
                complete = False
                self.giroUltimoId = status["id"]

                time.sleep(3)

            if status["status"] == "graphing":
                time.sleep(1)
        self.mandarMensagem("Bot interrompido")
        
    def apostar(self, saida):
        self.valor_saida_atual = saida
        self.venceu = False
        self.perdas = 0
        time.sleep(5)
        complete = False
        while True:
            if self.kill:
                break
            status = self.blaze.getStatusCrash()
            if status["status"] == "complete" and not complete:
                complete = True
                self.verificaSeVenceu()

                result = self.blaze.getUltimoResultadoCrash()
                valor = float(result.get("crash_point"))
                if self.venceu:
                    self.count_win += 1
                    if self.perdas == 0:
                        self.count_g0 += 1
                    elif self.perdas == 1:
                        self.count_g1 += 1
                    elif self.perdas == 2:
                        self.count_g2 += 1
                    msg = self.mensagem_green.replace("{atual}", f"{valor}") \
                        .replace("{perdas}", f"{self.perdas}")
                    self.enviarResultado(msg)
                    self.historico = []
                    return
                elif self.perdas >= 3:
                    self.count_loss += 1
                    msg = self.mensagem_red.replace("{cor}", f"{valor}") \
                        .replace("{perdas}", f"{self.perdas}")
                    self.enviarResultado(msg)
                    self.historico = []
                    return
                self.perdas += 1

            if status["status"] == "waiting" and self.giroAtualId != status["id"]:
                self.giroAtualId = status["id"]

            if status["status"] == "graphing":
                time.sleep(1)
                complete = False


    def verificaSeVenceu(self):
        try:
            result = self.blaze.getUltimoResultadoCrash()
            valor = float(result.get("crash_point"))

            self.venceu = valor > self.valor_saida_atual
            if self.venceu:
                self.valor_saida_atual = 0
        except:
            self.bot_telegram.enviarMensagem(self.chat_id, "Falha ao obter ultimo Resultado")



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
        for canal in self.canais_ativos:
            try:
                canal.sendAviso(texto)
            except:
                self.mandarMensagem(f"Falha ao enviar aviso para o canal de ID {canal.bot_chatID}")

    def apagarAviso(self):
        for canal in self.canais_ativos:
            try:
                canal.apagarAviso()
            except:
                self.mandarMensagem(f"Falha ao apagar aviso para o canal de ID {canal.bot_chatID}")

    def enviarConfirmacao(self, texto):
        for canal in self.canais_ativos:
            try:
                canal.sendConfirmation(texto)
            except:
                self.mandarMensagem(f"Falha ao enviar confirmação para o canal de ID {canal.bot_chatID}")

    def enviarResultado(self, texto):
        for canal in self.canais_ativos:
            try:
                canal.sendResult(texto)
            except:
                self.mandarMensagem(f"Falha ao enviar resultado para o canal de ID {canal.bot_chatID}")




if __name__ == '__main__':
    bot = bot_telegram()
    bot.start()
