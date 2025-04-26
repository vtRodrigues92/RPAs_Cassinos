from telethon import TelegramClient, events
import asyncio
import ast, os
import telebot
from telegram.ext import *
from telebot import *
from datetime import datetime, timedelta


class HorarioSessao(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)


    def horario_sinal(self):
        global sessao_ativa, contagem_sinais, qntd_sinais_sessao, reladiarioenviado

        
        # ENVIA PLACAR CANAIS TELEGRAM
        def envia_placar(chat_id):

            try:
                placar()

                try:
                    msg_placar = bot.send_message(chat_id,\
        "📊 Placar Atual do dia "+data_hoje+":\n\
        =====================\n\
        ✅ WIN - "+str(placar_win)+"\n\
        ❌ RED - "+str(placar_loss))
                    
        #Variavel Dinâmica
                except:
                    pass


            except Exception as a:
                logger.error('Exception ocorrido no ' + repr(a))
                #placar = bot.reply_to(message,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%", reply_markup=markup)
                pass
    

        # VALIDADOR DE DATA
        def validaData():
            global data_resultado
            global reladiarioenviado
            global horario_atual

            data_hoje = datetime.today()
            subtrai_dia = timedelta(days=-1)
            data_ontem = data_hoje + subtrai_dia
            data_resultado = data_ontem.strftime('%d/%m/%Y')
            horario_atual = datetime.today().strftime('%H:%M')

            # Condição que zera o placar quando o dia muda
            if horario_atual == '00:00' and reladiarioenviado == 0:
                placar()
                reladiarioenviado +=1

            # Condição que zera o placar quando o dia muda
            if horario_atual == '00:01' and reladiarioenviado == 1:
                reladiarioenviado = 0


        # GERA TXT DO PLACAR
        def placar():
            global placar_win
            global placar_semGale
            global placar_gale1
            global placar_gale2
            global placar_loss
            global placar_geral
            global asserividade
            global data_hoje

            data_hoje = datetime.today().strftime('%d-%m-%Y')
            arquivos_placares = os.listdir(r"placar/")

            if f'{data_hoje}.txt' in arquivos_placares:
                # Carregar arquivo de placar
                with open(f"placar/{data_hoje}.txt", 'r') as arquivo:
                    try:

                        arq_placar = arquivo.readlines()
                        placar_win = int(arq_placar[0].split(',')[1])
                        placar_semGale = int(arq_placar[1].split(',')[1])
                        placar_gale1 = int(arq_placar[2].split(',')[1])
                        placar_gale2 = int(arq_placar[3].split(',')[1])
                        placar_loss = int(arq_placar[4].split(',')[1])
                        placar_geral = int(placar_win) + int(placar_loss)
                        asserividade = arq_placar[5].split(',')[1]+"%"
                    
                    except:
                        pass

                    
            else:
                # Criar um arquivo com a data atual
                with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                    arquivo.write("win,0\nsg,0\ng1,0\ng2,0\nloss,0\nass,0")

                # Ler o arquivo de placar criado
                with open(f"placar/{data_hoje}.txt", 'r') as arquivo:
                    try:

                        arq_placar = arquivo.readlines()
                        placar_win = int(arq_placar[0].split(',')[1])
                        placar_semGale = int(arq_placar[1].split(',')[1])
                        placar_gale1 = int(arq_placar[2].split(',')[1])
                        placar_gale2 = int(arq_placar[3].split(',')[1])
                        placar_loss = int(arq_placar[4].split(',')[1])
                        placar_geral = int(placar_win) + int(placar_loss)
                        asserividade = arq_placar[5].split(',')[1]+"%"
                    
                    except:
                        pass

        reladiarioenviado = 0
        sessao_ativa = False
        contagem_sinais = 0
        placar()

        while True:

            validaData()
            
            horario_atual = datetime.today().strftime('%H:%M')


            with open ('horario_sessoes.txt', encoding='UTF-8') as arquivo: 
                horarios = arquivo.read().split(',')

            with open ('qnt_sinais_sessao.txt', encoding='UTF-8') as arquivo: 
                qntd_sinais_sessao = arquivo.read()        

            with open ('inicio_sessao.txt', encoding='UTF-8') as arquivo: 
                msg_inicio_sessao = arquivo.read()

            with open ('fim_sessao.txt', encoding='UTF-8') as arquivo: 
                msg_fim_sessao = arquivo.read()


            for horario in horarios:
                if horario_atual == horario and sessao_ativa == False:

                    contagem_sinais = 1
                    sessao_ativa = True

                    for origem, destino in dicionario_chats.items():
                        if destino[1] == 'SIM':
                            bot.send_message(destino[0], msg_inicio_sessao, parse_mode='HTML', disable_web_page_preview=True)

                    print('Sessão Ativada!!')
                
                else:
                    continue


            #Validação pra Finalizar Sessão
            if contagem_sinais > int(qntd_sinais_sessao) and sessao_ativa == True:

                for origem, destino in dicionario_chats.items():
                        if destino[1] == 'SIM':
                            envia_placar(destino[0])
                            bot.send_message(destino[0], msg_fim_sessao, parse_mode='HTML', disable_web_page_preview=True)
                
                sessao_ativa = False
                contagem_sinais = 1    
            
            time.sleep(5)
        

    def run(self):
        self.horario_sinal()


class RepassarMensagens(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client


    def atualizar_placar(self):
        try:

            # Atualizando placar e Alimentando o arquivo txt
            with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}")

        except Exception as e:
            print(e)
 

    def repassar_mensagens(self):
            global sessao_ativa, contagem_sinais, dicionario_chats, placar_win, placar_loss, placar_geral

            #LENDO ARQUIVO DE CHATS
            dicionario_chats = ler_arquivo_txt_chats()

            #print('Monitoramento Iniciado...')
            client = self.get_or_create_eventloop()
            #client = TelegramClient(sessao, api_id, api_hash)
        
            #RECEBE UMA NOVA MENSAGEM
            @client.on(events.NewMessage(chats = [key for key,value in dicionario_chats.items()]))
            async def enviar_mensagem(event):
                global sessao_ativa, contagem_sinais, placar_win, placar_loss, placar_geral
                
                try:

                    if bot_status == 1:
                        
                        for origem, destino in dicionario_chats.items():

                            if event.chat_id == origem:
                                #Verificando se o repasse tem horario de sessao
                                if destino[1] == 'NAO':    
                                    globals()[f'nova_mensagem_{origem}'] =  await client.send_message(destino[0], event.message, link_preview=False)

                                elif destino[1] == 'SIM':
                                    if contagem_sinais <= int(qntd_sinais_sessao):
                                        if sessao_ativa == True and contagem_sinais <= int(qntd_sinais_sessao):
                                            globals()[f'nova_mensagem_{origem}'] =  await client.send_message(destino[0], event.message, link_preview=False)
                                            #Contagem de Placar

                                        if sessao_ativa == True and "GREEN" in event.message.text or \
                                           sessao_ativa == True and "WIN" in event.message.text:
                                        
                                            placar_win+=1
                                            placar_geral = placar_win + placar_loss
                                            self.atualizar_placar()
                                            contagem_sinais+=1

                                        elif sessao_ativa == True and "RED" in event.message.text or\
                                             sessao_ativa == True and "LOSS" in event.message.text or\
                                             sessao_ativa == True and "loss" in event.message.text:
                                            
                                            placar_loss +=1
                                            placar_geral = placar_win + placar_loss
                                            self.atualizar_placar()
                                            contagem_sinais+=1

                                        
                                
                                    else:
                                        sessao_ativa = False
                                        print('Sessão Desativada!!')

                    else:
                        client.disconnect()

                except Exception as e:
                    print(e)

            #EDITA A ULTIMA MENSAGEM ENVIADA
            @client.on(events.MessageEdited(chats = [key for key,value in dicionario_chats.items()]))
            async def editar_mensagem(event):
                global sessao_ativa, contagem_sinais, placar_win, placar_loss, placar_geral

                try:

                    if bot_status == 1:

                        for origem, destino in dicionario_chats.items():

                            if event.chat_id == origem:
                                #Verificando se o repasse tem horario de sessao
                                if destino[1] == 'NAO':
                                    await client.edit_message(destino[0], globals()[f'nova_mensagem_{origem}'].id, event.message.message.text, link_preview=False)

                                elif destino[1] == 'SIM':
                                    if sessao_ativa == True and contagem_sinais <= int(qntd_sinais_sessao):
                                        await client.edit_message(destino[0], globals()[f'nova_mensagem_{origem}'].id, event.message.text, link_preview=False)
                                        #Contagem de Placar
                                        if "Green" in event.message.text or "GREEN" in event.message.text or "WIN" in event.message.text:
                                            placar_win+=1
                                            placar_geral = placar_win + placar_loss
                                            self.atualizar_placar()
                                            contagem_sinais+=1

                                        elif "RED" in event.message.text or "LOSS" in event.message.text or "loss" in event.message.text:
                                            placar_loss +=1
                                            placar_geral = placar_win + placar_loss
                                            self.atualizar_placar()
                                            contagem_sinais+=1


                    else:
                        client.disconnect()

                except Exception as e:
                    print(e)
                    pass

            #DELETA A ULTIMA MENSAGEM ENVIADA
            @client.on(events.MessageDeleted(chats = [key for key,value in dicionario_chats.items()]))
            async def apagar_mensagem(event):
                
                try:
                    
                    if bot_status == 1:

                        for origem, destino in dicionario_chats.items():
                            if event.chat_id == origem:
                                await client.delete_messages(destino[0], globals()[f'nova_mensagem_{origem}'].id)
                    
                    else:
                        client.disconnect()

                except Exception as e:
                    print(e)
                    pass
            
            client.start()
            client.run_until_disconnected()


    def get_or_create_eventloop(self):
        try:
            return asyncio.get_event_loop()
        except RuntimeError as ex:
            if "There is no current event loop in thread" in str(ex):
                with open ('senhas.txt', 'r', encoding='UTF-8') as file:
                    arquivo = file.readlines()

                    api_id = arquivo[0].split(' ')[1].replace('\n','')
                    api_hash = arquivo[1].split(' ')[1].replace('\n','')
                    token = arquivo[2].split(' ')[1].replace('\n','')
                    phone = arquivo[3].split(' ')[1].replace('\n','')
                    sessao = 'Repassar Mensagem'

                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    client = TelegramClient(phone, api_id, api_hash, loop=loop)

                    return client


    def run(self):
        self.repassar_mensagens()



def inicio():
    print()
    print('                                #################################################################')
    print('                                #################  BOT REPASSE MENSAGENS  #######################')
    print('                                #################################################################')
    print('                                ##################### SEJA BEM VINDO ############################')
    print('                                #################################################################')
    print('                                ############# DESENVOLVIDO POR VICTOR RODRIGUES #################')
    print('                                #################################################################\n')
    print('Versão = 1.0.0')
    print('Ambiente: Produção\n\n\n\n')


def pegar_chaves():
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


def listar_canais_telegram(client):
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


def pegar_nome_canais(chat):
    
    for canal in canais:
        
        if canal.id < 0 and canal.id == chat:
            nome_canal = canal.title
            break
            

    return nome_canal


def ler_arquivo_txt_chats():
    with open('chats.txt', 'r', encoding='UTF-8') as file:
        chats = file.read()
        if chats == '':

            dicionario_chats = ''
        
        else:

            dicionario_chats = ast.literal_eval(chats)

    return dicionario_chats


def atualizar_arquivo_txt_chats(lista_chats):
    with open('chats.txt', 'w') as arquivo:
        arquivo.write(str(lista_chats))

        arquivo.close()


def generate_buttons_estrategias(bts_names, markup):
    for button in bts_names:
        markup.add(types.KeyboardButton(button))
    return markup


def bot_telegram(token):

    bot = telebot.TeleBot(token)

    return bot


def registra_horario_repasse(message_horario):
    global horario_sessao

    try:
        horario_sessao = message_horario.text

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        
        markup_canais = generate_buttons_estrategias([key for key, value in dicionario_canais_telegram.items()], markup)
        markup_canais.add('◀ Voltar')    

        message_origem = bot.reply_to(message_horario, "🤖 Ok! Escolha Escolha o CANAL ORIGEM Abaixo ou Insira o CHAT_ID do Canal 👇", reply_markup=markup)
        bot.register_next_step_handler(message_origem, registra_canal_origem)
    
    except:
        message_erro = bot.reply_to(message_horario, "🤖❌ Algo deu Errado. Tente Novamente.", reply_markup=markup)


def registra_canal_origem(message_origem):
    global novo_repasse

    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup_canais = generate_buttons_estrategias([key for key, value in dicionario_canais_telegram.items()], markup)
        markup_canais.add('◀ Voltar')
    
    
        for key, value in dicionario_canais_telegram.items():
            if key == message_origem.text or str(value) == message_origem.text or message_origem.text == str(value).replace('-',''):
                globals()[f'origem'] = int(str(value))
                
                message_destino = bot.reply_to(message_origem, "🤖✅ Tudo Certo! Agora Escolha o Canal Destino Abaixo ou Insira o CHAT_ID 👇", reply_markup=markup_canais)
                bot.register_next_step_handler(message_destino, registra_canal_destino)
                
                return
        
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','🟢 Ativar Repasses de Mensagens','⚙ Cadastrar Repasse','📜 Repasses Cadastrados','🗑 Apagar Repasse','⏰ Horário Sessões','🚦 Sinais por Sessão','📝 MSG Inicio Sessão','🗒️ MSG Fim Sessão', '🛑 Pausar Repasses')

        message_erro = bot.reply_to(message_origem, "🤖❌ Não Encontrei o Chat_ID Inserido. Tente Novamente.", reply_markup=markup)

        
    except:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','🟢 Ativar Repasses de Mensagens','⚙ Cadastrar Repasse','📜 Repasses Cadastrados','🗑 Apagar Repasse','⏰ Horário Sessões','🚦 Sinais por Sessão','📝 MSG Inicio Sessão','🗒️ MSG Fim Sessão', '🛑 Pausar Repasses')

        message_erro = bot.reply_to(message_origem, "🤖❌ Algo deu Errado. Tente Novamente.", reply_markup=markup)


def registra_canal_destino(message_destino):
    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','🟢 Ativar Repasses de Mensagens','⚙ Cadastrar Repasse','📜 Repasses Cadastrados','🗑 Apagar Repasse','⏰ Horário Sessões','🚦 Sinais por Sessão','📝 MSG Inicio Sessão','🗒️ MSG Fim Sessão', '🛑 Pausar Repasses')

        novo_repasse = {}
        for key, value in dicionario_canais_telegram.items():
            if key == message_destino.text or str(value) == message_destino.text or message_destino.text == str(value).replace('-',''):
                novo_repasse[globals()[f'origem']] = [int(str(value)),horario_sessao]

                #ATUALIZANDO O ARQUIVO TXT
                lista_chats = ler_arquivo_txt_chats()
                
                if lista_chats == '':
                    lista_chats = novo_repasse
                else:
                    lista_chats.update(novo_repasse)
                
                atualizar_arquivo_txt_chats(lista_chats)

                message_destino = bot.reply_to(message_destino, "🤖 Repasse Cadastrado com Sucesso! ✅", reply_markup=markup)

                return

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','🟢 Ativar Repasses de Mensagens','⚙ Cadastrar Repasse','📜 Repasses Cadastrados','🗑 Apagar Repasse','⏰ Horário Sessões','🚦 Sinais por Sessão','📝 MSG Inicio Sessão','🗒️ MSG Fim Sessão', '🛑 Pausar Repasses')

        message_erro = bot.reply_to(message_destino, "🤖❌ Não Encontrei o Chat_ID Inserido. Tente Novamente.", reply_markup=markup)


    except:

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','🟢 Ativar Repasses de Mensagens','⚙ Cadastrar Repasse','📜 Repasses Cadastrados','🗑 Apagar Repasse','⏰ Horário Sessões','🚦 Sinais por Sessão','📝 MSG Inicio Sessão','🗒️ MSG Fim Sessão', '🛑 Pausar Repasses')

        message_erro = bot.reply_to(message_destino, "🤖❌ Algo deu Errado. Tente Novamente.", reply_markup=markup)


def registrar_repasse_excluido(message_excluir_repasse):

    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','🟢 Ativar Repasses de Mensagens','⚙ Cadastrar Repasse','📜 Repasses Cadastrados','🗑 Apagar Repasse','⏰ Horário Sessões','🚦 Sinais por Sessão','📝 MSG Inicio Sessão','🗒️ MSG Fim Sessão', '🛑 Pausar Repasses')

        for key, value in dicionario_canais_telegram.items():
            if key == message_excluir_repasse.text.split(' | ')[0]:
                dado_excluir = int(str(value))
                break

        #ATUALIZANDO O ARQUIVO TXT
        lista_chats = ler_arquivo_txt_chats()
        
        #REMOVENDO DADO DO DICT
        lista_chats.pop(dado_excluir)
        
        #ATUALIZANDO TXT
        atualizar_arquivo_txt_chats(lista_chats)

        message_destino = bot.reply_to(message_excluir_repasse, "🤖 Repasse Removido com Sucesso! ✅", reply_markup=markup)

        return

    except:

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','🟢 Ativar Repasses de Mensagens','⚙ Cadastrar Repasse','📜 Repasses Cadastrados','🗑 Apagar Repasse','⏰ Horário Sessões','🚦 Sinais por Sessão','📝 MSG Inicio Sessão','🗒️ MSG Fim Sessão', '🛑 Pausar Repasses')

        message_erro = bot.reply_to(message_excluir_repasse, "🤖❌ Algo deu Errado. Tente Novamente.", reply_markup=markup)


def registrar_horario_sessoes(message_editar_valor):
    
    if message_editar_valor.text == '◀ Voltar':
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','🟢 Ativar Repasses de Mensagens','⚙ Cadastrar Repasse','📜 Repasses Cadastrados','🗑 Apagar Repasse','⏰ Horário Sessões','🚦 Sinais por Sessão','📝 MSG Inicio Sessão','🗒️ MSG Fim Sessão', '🛑 Pausar Repasses')

        message_opcoes = bot.reply_to(message_editar_valor, "🤖 Escolha uma opção 👇",
                                    reply_markup=markup)
            
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(message_opcoes, opcoes)
    
    else:
        try:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','🟢 Ativar Repasses de Mensagens','⚙ Cadastrar Repasse','📜 Repasses Cadastrados','🗑 Apagar Repasse','⏰ Horário Sessões','🚦 Sinais por Sessão','📝 MSG Inicio Sessão','🗒️ MSG Fim Sessão', '🛑 Pausar Repasses')

            with open ('horario_sessoes.txt', 'w', encoding='UTF-8') as arquivo: 
                        arquivo.write(message_editar_valor.text)

            message_sucess = bot.reply_to(message_editar_valor, "🤖 Horarios Editados com Sucesso! ✅", reply_markup=markup)
            
        except:
            pass


def registrar_qntd_sinais(message_editar_valor):

    if message_editar_valor.text == '◀ Voltar':
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','🟢 Ativar Repasses de Mensagens','⚙ Cadastrar Repasse','📜 Repasses Cadastrados','🗑 Apagar Repasse','⏰ Horário Sessões','🚦 Sinais por Sessão','📝 MSG Inicio Sessão','🗒️ MSG Fim Sessão', '🛑 Pausar Repasses')

        message_opcoes = bot.reply_to(message_editar_valor, "🤖 Escolha uma opção 👇",
                                    reply_markup=markup)
            
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(message_opcoes, opcoes)
    
    else:
        try:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','🟢 Ativar Repasses de Mensagens','⚙ Cadastrar Repasse','📜 Repasses Cadastrados','🗑 Apagar Repasse','⏰ Horário Sessões','🚦 Sinais por Sessão','📝 MSG Inicio Sessão','🗒️ MSG Fim Sessão', '🛑 Pausar Repasses')

            with open ('qnt_sinais_sessao.txt', 'w', encoding='UTF-8') as arquivo: 
                        arquivo.write(message_editar_valor.text)

            message_sucess = bot.reply_to(message_editar_valor, "🤖 Quantidade de Sinais Editado com Sucesso! ✅", reply_markup=markup)
            
        except:
            pass


def registrar_msg_inicio_sessao(message_editar_msg):

    if message_editar_msg.text == '◀ Voltar':
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','🟢 Ativar Repasses de Mensagens','⚙ Cadastrar Repasse','📜 Repasses Cadastrados','🗑 Apagar Repasse','⏰ Horário Sessões','🚦 Sinais por Sessão','📝 MSG Inicio Sessão','🗒️ MSG Fim Sessão', '🛑 Pausar Repasses')

        message_opcoes = bot.reply_to(message_editar_msg, "🤖 Escolha uma opção 👇",
                                    reply_markup=markup)
            
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(message_opcoes, opcoes)
    
    else:
        try:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','🟢 Ativar Repasses de Mensagens','⚙ Cadastrar Repasse','📜 Repasses Cadastrados','🗑 Apagar Repasse','⏰ Horário Sessões','🚦 Sinais por Sessão','📝 MSG Inicio Sessão','🗒️ MSG Fim Sessão', '🛑 Pausar Repasses')

            with open ('inicio_sessao.txt', 'w', encoding='UTF-8') as arquivo: 
                        arquivo.write(message_editar_msg.text)

            message_sucess = bot.reply_to(message_editar_msg, "🤖 Mensgem Editada com Sucesso! ✅", reply_markup=markup)
            
        except:
            pass


def registrar_msg_fim_sessao(message_editar_msg):

    if message_editar_msg.text == '◀ Voltar':
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','🟢 Ativar Repasses de Mensagens','⚙ Cadastrar Repasse','📜 Repasses Cadastrados','🗑 Apagar Repasse','⏰ Horário Sessões','🚦 Sinais por Sessão','📝 MSG Inicio Sessão','🗒️ MSG Fim Sessão', '🛑 Pausar Repasses')

        message_opcoes = bot.reply_to(message_editar_msg, "🤖 Escolha uma opção 👇",
                                    reply_markup=markup)
            
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(message_opcoes, opcoes)
    
    else:
        try:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','🟢 Ativar Repasses de Mensagens','⚙ Cadastrar Repasse','📜 Repasses Cadastrados','🗑 Apagar Repasse','⏰ Horário Sessões','🚦 Sinais por Sessão','📝 MSG Inicio Sessão','🗒️ MSG Fim Sessão', '🛑 Pausar Repasses')

            with open ('fim_sessao.txt', 'w', encoding='UTF-8') as arquivo: 
                        arquivo.write(message_editar_msg.text)

            message_sucess = bot.reply_to(message_editar_msg, "🤖 Mensgem Editada com Sucesso! ✅", reply_markup=markup)
            
        except:
            pass





if __name__ == '__main__':
    try:

        inicio()

        print('FAZENDO CONEXÃO COM TELEGRAM USANDO O NÚMERO CADASTRADO........\n\n')

        time.sleep(3)

        bot_status = 0

        client, CHAVE_API = pegar_chaves()

        dicionario_canais_telegram = listar_canais_telegram(client)

        dicionario_chats_cadastrados = ler_arquivo_txt_chats()

        bot = bot_telegram(CHAVE_API)

        print('\n\nCONEXÃO REALIZADA COM SUCESSO!')

        print('\n\n\n\n################################# AGUARDANDO COMANDOS #################################')

    except:
        print('\n\nNÃO CONSEGUI REALIZAR A CONEXÃO COM OS DADOS INFORMADOS. REVEJA OS DADOS INSERIDOS.')
        print('\nENCERRANDO O PROGRAMA!! ATÉ MAIS!!!')
        exit()

    


    @bot.message_handler(commands=['⚙ Cadastrar_Repasse'])
    def cadastrar_repasse(message):

        try:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
            
            markup.add('SIM','NAO','◀ Voltar')    

            message_horario = bot.reply_to(message, "🤖 Ok! O Repasse terá Horarios de Sessões 👇", reply_markup=markup)
            bot.register_next_step_handler(message_horario, registra_horario_repasse)
        
        except:
            message_erro = bot.reply_to(message, "🤖❌ Algo deu Errado. Tente Novamente.", reply_markup=markup)


    @bot.message_handler(commands=['📜 Repasses_Cadastradas'])
    def repasses_cadastrados(message):

        try:

            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','🟢 Ativar Repasses de Mensagens','⚙ Cadastrar Repasse','📜 Repasses Cadastrados','🗑 Apagar Repasse','⏰ Horário Sessões','🚦 Sinais por Sessão','📝 MSG Inicio Sessão','🗒️ MSG Fim Sessão', '🛑 Pausar Repasses')

            bot.reply_to(message, "🤖 Ok! Listando Repasses Cadastrados", reply_markup=markup)
            
            lista_chats = ler_arquivo_txt_chats()
            for chat_origem, chat_destino in lista_chats.items():

                nome_chat_origem = pegar_nome_canais(chat_origem)
                nome_chat_destino = pegar_nome_canais(chat_destino[0])

                bot.send_message(message.chat.id, 
f'===========================\n\
Canal Origem  ⏩ {nome_chat_origem}\n\
Canal Destino ⏩ {nome_chat_destino}\n\
Sessão de Repasses ⏩ {chat_destino[1]}\n\
===========================')
        
        except:
            pass


    @bot.message_handler(commands=['🗑 Apagar_Repasse'])
    def apagar_repasse(message):
        try:
            #PEGANDO NOME DOS CHATS
            lista_chats = ler_arquivo_txt_chats()
            lista_nome_chats = []
            for chat_origem, chat_destino in lista_chats.items():
                nome_chat_origem = pegar_nome_canais(chat_origem)
                nome_chat_destino = pegar_nome_canais(chat_destino[0])
                lista_nome_chats.append(nome_chat_origem+' | '+nome_chat_destino)
            
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            #Add to buttons by list with ours generate_buttons function.
            markup_estrategias = generate_buttons_estrategias([ nome_chat for nome_chat in lista_nome_chats ], markup)    
            markup_estrategias.add('◀ Voltar')

            message_excluir_repasse = bot.reply_to(message, "🤖 Escolha o Repasse a ser excluído 👇", reply_markup=markup_estrategias)
            bot.register_next_step_handler(message_excluir_repasse, registrar_repasse_excluido)
        
        except:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','🟢 Ativar Repasses de Mensagens','⚙ Cadastrar Repasse','📜 Repasses Cadastrados','🗑 Apagar Repasse','⏰ Horário Sessões','🚦 Sinais por Sessão','📝 MSG Inicio Sessão','🗒️ MSG Fim Sessão', '🛑 Pausar Repasses')

            message_erro = bot.reply_to(message, "🤖❌ Algo deu Errado. Tente Novamente.", reply_markup=markup)


    @bot.message_handler(commands=['🛑 Pausar_Repasses'])
    def pausar_repasses(message):
        global bot_status

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','🟢 Ativar Repasses de Mensagens','⚙ Cadastrar Repasse','📜 Repasses Cadastrados','🗑 Apagar Repasse','⏰ Horário Sessões','🚦 Sinais por Sessão','📝 MSG Inicio Sessão','🗒️ MSG Fim Sessão', '🛑 Pausar Repasses')

        bot_status = 0

        message_final = bot.reply_to(message, "🤖🔴 Repasse Pausado com Sucesso! ✅", reply_markup=markup)


    @bot.message_handler(commands=['start'])
    def start(message):

        if str(message.chat.id):
            
            #ID USUARIO
            id_usuario = message.chat.id

            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','🟢 Ativar Repasses de Mensagens','⚙ Cadastrar Repasse','📜 Repasses Cadastrados','🗑 Apagar Repasse','⏰ Horário Sessões','🚦 Sinais por Sessão','📝 MSG Inicio Sessão','🗒️ MSG Fim Sessão', '🛑 Pausar Repasses')

            message_opcoes = bot.reply_to(message, f"🤖 Olá {message.json['from']['first_name']}, você está usando o Bot que Repassa Mensagens! Escolha uma opção 👇",
                                    reply_markup=markup)
            
            #Here we assign the next handler function and pass in our response from the user. 
            bot.register_next_step_handler(message_opcoes, opcoes)
        
        else:
            message_error = bot.reply_to(message, "🤖 Você não tem permissão para acessar este Bot ❌🚫")

    
    @bot.message_handler()
    def opcoes(message_opcoes):


        if message_opcoes.text in ['⚙ Cadastrar Repasse']:
            print('Cadastrar Repasse')
            cadastrar_repasse(message_opcoes)
            

        if message_opcoes.text in['📜 Repasses Cadastrados']:
            print('Repasses Cadastrados')
            repasses_cadastrados(message_opcoes)
            

        if message_opcoes.text in ['🗑 Apagar Repasse']:
            print('Apagar Repasse')
            apagar_repasse(message_opcoes)

        
        if message_opcoes.text in ['⏰ Horário Sessões']:
            
            try:

                with open ('horario_sessoes.txt', encoding='UTF-8') as arquivo: 
                    horario_sessoes = arquivo.read()

            except:pass

            try:
                #Init keyboard markup
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
                markup = markup.add(
                                    horario_sessoes,
                                    '◀ Voltar'
                                    )

                message_editar_valor = bot.reply_to(message_opcoes, "🤖 Perfeito! Segue Horário das Sessões. Para Editar, Insira a Nova Lista de Horários 👇",
                                        reply_markup=markup)
            
                #Here we assign the next handler function and pass in our response from the user. 
                bot.register_next_step_handler(message_editar_valor, registrar_horario_sessoes)
            
            except:
                message_error = bot.reply_to(message_opcoes, "🤖❌ Algo deu Errado. Tente Novamente.")

        
        if message_opcoes.text in ['🚦 Sinais por Sessão']:
            try:

                with open ('qnt_sinais_sessao.txt', encoding='UTF-8') as arquivo: 
                    qntd_sinais_sessao = arquivo.read()

            except:pass

            try:
                #Init keyboard markup
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
                markup = markup.add(
                                    qntd_sinais_sessao,
                                    '◀ Voltar'
                                    )

                message_editar_valor = bot.reply_to(message_opcoes, "🤖 Perfeito! Segue Quantidade de Sinais Por Sessão. Para Editar, Insira o Novo Valor 👇",
                                        reply_markup=markup)
            
                #Here we assign the next handler function and pass in our response from the user. 
                bot.register_next_step_handler(message_editar_valor, registrar_qntd_sinais)
            
            except:
                message_error = bot.reply_to(message_opcoes, "🤖❌ Algo deu Errado. Tente Novamente.")

        
        if message_opcoes.text in ['📝 MSG Inicio Sessão']:
            try:

                with open ('inicio_sessao.txt', encoding='UTF-8') as arquivo: 
                    msg_inicio_sessao = arquivo.read()

            except:pass

            try:
                #Init keyboard markup
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
                markup = markup.add(
                                    msg_inicio_sessao,
                                    '◀ Voltar'
                                    )

                message_editar_msg = bot.reply_to(message_opcoes, "🤖 Perfeito! Segue a Mensagem Enviada no Inicio da Sessão. Para Editar, Insira o Novo Valor 👇",
                                        reply_markup=markup)
                
                msg = bot.send_message(message_opcoes.json['from']['id'], msg_inicio_sessao)
            
                #Here we assign the next handler function and pass in our response from the user. 
                bot.register_next_step_handler(message_editar_msg, registrar_msg_inicio_sessao)
            
            except:
                message_error = bot.reply_to(message_opcoes, "🤖❌ Algo deu Errado. Tente Novamente.")

            
        if message_opcoes.text in ['🗒️ MSG Fim Sessão']:
            try:

                with open ('fim_sessao.txt', encoding='UTF-8') as arquivo: 
                    msg_fim_sessao = arquivo.read()

            except:pass

            try:
                #Init keyboard markup
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
                markup = markup.add(
                                    msg_fim_sessao,
                                    '◀ Voltar'
                                    )

                message_editar_msg = bot.reply_to(message_opcoes, "🤖 Perfeito! Segue a Mensagem Enviada no Inicio da Sessão. Para Editar, Insira o Novo Valor 👇",
                                        reply_markup=markup)
                

                msg = bot.send_message(message_opcoes.json['from']['id'], msg_fim_sessao)
            
                #Here we assign the next handler function and pass in our response from the user. 
                bot.register_next_step_handler(message_editar_msg, registrar_msg_fim_sessao)
            
            except:
                message_error = bot.reply_to(message_opcoes, "🤖❌ Algo deu Errado. Tente Novamente.")


        if message_opcoes.text in ['🟢 Ativar Repasses de Mensagens']:
            global bot_status
            global parar

            print('Ativar Bot')

            if bot_status == 1:

                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                markup = markup.add('/start','🟢 Ativar Repasses de Mensagens','⚙ Cadastrar Repasse','📜 Repasses Cadastrados','🗑 Apagar Repasse','⏰ Horário Sessões','🚦 Sinais por Sessão','📝 MSG Inicio Sessão','🗒️ MSG Fim Sessão', '🛑 Pausar Repasses')

                message_canal = bot.reply_to(message_opcoes, "🤖⛔ Bot já está ativado",
                                    reply_markup=markup)

            
            else:
                #Init keyboard markup
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                markup = markup.add('/start','🟢 Ativar Repasses de Mensagens','⚙ Cadastrar Repasse','📜 Repasses Cadastrados','🗑 Apagar Repasse','⏰ Horário Sessões','🚦 Sinais por Sessão','📝 MSG Inicio Sessão','🗒️ MSG Fim Sessão', '🛑 Pausar Repasses')

                message_canal = bot.reply_to(message_opcoes, "🤖 Repasses Iniciado com Sucesso! ",
                                        reply_markup=markup)

                bot_status = 1
                parar = 0

                print('#################################  INICIANDO OS REPASSES  #################################')
                print()
                RepassarMensagens(client).start()
                HorarioSessao().start()

        
        if message_opcoes.text in ['🛑 Pausar Repasses']:
            print('Pausar Bot')
            pausar_repasses(message_opcoes)
        











    bot.infinity_polling()



    

