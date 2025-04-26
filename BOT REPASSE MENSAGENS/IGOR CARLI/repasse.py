from telethon import TelegramClient, events
import asyncio
import ast
import telebot
from telegram.ext import *
from telebot import *
from datetime import datetime, timedelta



class RepassarMensagens(threading.Thread):
    def __init__(self, chat_id, chat_from, texto_message):
        threading.Thread.__init__(self)
        self.chat_to = chat_id
        self.chat_from = chat_from
        self.texto_message = texto_message
        

    def send_messages(self, chat_to, chat_from, id_message):
        try:
            bot.forward_message(str(chat_to), chat_from, id_message)
            #await client.send_message(chat, message)        
        except Exception as e:
            print(e)
            pass


    def run(self):

        while True:
            try:
                self.send_messages(int(self.chat_to), self.chat_from, self.texto_message)
                print(f'{datetime.today().strftime("%H:%M:%S")} -- MENSAGEM ENVIADA PARA O CANAL {self.chat_to}')
                break
            except Exception as e:
                print(e)
                
        


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


def horario_sinal():
        global sessao_ativa


        #VALIDADOR DE DATA
        def validaData():
            global data_resultado
            global horario_atual

            data_hoje = datetime.today()
            subtrai_dia = timedelta(days=-1)
            data_ontem = data_hoje + subtrai_dia
            data_resultado = data_ontem.strftime('%d/%m/%Y')
            horario_atual = datetime.today().strftime('%H:%M')

            
        while True:

            try:
                validaData()
                
                horario_atual = datetime.today().strftime('%H:%M:%S')

                #Buscando Horarios no TXT
                #horarios = open('horario_sessoes.txt', 'r', encoding='UTF-8').read()
                #Transformando texto em dicionario
                #horarios = ast.literal_eval(horarios)

                #Buscando relação de chats e mensagens no txt
                chats = open('chats.txt', 'r', encoding='UTF-8').read()
                #Transformando texto em dicionario
                chats = ast.literal_eval(chats)
                
                #Percorrendo dicionario de horarios para enviar mensagens
                for key_1, value_1 in chats.items():
                    for hora_envio in value_1[1]:
                        if horario_atual == hora_envio:
                            #Percorrendo dicionario de chats para encontrar o chat e a mensagem que será enviada
                            for key_2, value_2 in chats.items():
                                if key_2 == key_1:
                                    #Chamando Thread que envia a mensagem e dormindo 5 segundos
                                    RepassarMensagens(value_2[0], value_2[3], value_2[2]).start()
                                    time.sleep(5)
                                    
                        else:
                            continue

            except:
                pass


def pegar_chaves():
    global loop

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

    return client, CHAVE_API, loop


def listar_canais_telegram(client):
    global canais, dicionario_canal_nome
    
    try:

        dicionario_canais_telegram = {}
        dicionario_canal_nome = {}
        client.start()

        for canal in client.iter_dialogs():
            if canal.is_channel:
                if canal.id < 0:
                    dicionario_canais_telegram[canal.title] = canal.id
                    dicionario_canal_nome[canal.id] = canal.title
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
    
    for nome_chat, chat_id  in dicionario_canais_telegram.items():
        
        if chat_id == str(chat):
            nome_canal = nome_chat.title()
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
    with open('chats.txt', 'w', encoding='UTF-8') as arquivo:
        arquivo.write(str(lista_chats))

        arquivo.close()


def generate_buttons_estrategias(bts_names, markup):
    for button in bts_names:
        markup.add(types.KeyboardButton(button))
    return markup


def bot_telegram(token):

    bot = telebot.TeleBot(token)

    return bot


def registra_apelido(message_apelido):

    try:

        if message_apelido.text in ['◀ Voltar']:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','🟢 Ativar Envio de Mensagens','⚙ Cadastrar Envio', '📝 Editar info Chats', '📜 Envios Cadastrados','🗑 Apagar Envio','🛑 Pausar Envios de Mensagens')

            message_opcoes = bot.reply_to(message_apelido, "🤖 Escolha uma opção 👇",
                                    reply_markup=markup)
            return
    
        
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
        
        markup_canais = generate_buttons_estrategias([key for key, value in dicionario_canais_telegram.items()], markup)
        markup_canais.add('◀ Voltar')    

        globals()[f'apelido'] = message_apelido.text

        try:
            message_canal = bot.reply_to(message_apelido, "🤖 Ok! Insira o CHAT_ID do Canal 👇", reply_markup=markup_canais)
            bot.register_next_step_handler(message_canal, registra_canal)
        except:
            #Init keyboard markup
            markup_except = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup_except.add('◀ Voltar')   
            message_canal = bot.reply_to(message_apelido, "🤖 Ok! Insira o CHAT_ID do Canal 👇", reply_markup=markup_except)
            bot.register_next_step_handler(message_canal, registra_canal)

    except:
        message_erro = bot.reply_to(message_apelido, "🤖❌ Algo deu Errado. Tente Novamente.", reply_markup=markup)


def registrar_horario_envio(message_horario):
    global horario_sessao

    try:

        if message_horario.text in ['◀ Voltar']:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','🟢 Ativar Envio de Mensagens','⚙ Cadastrar Envio', '📝 Editar info Chats', '📜 Envios Cadastrados','🗑 Apagar Envio','🛑 Pausar Envios de Mensagens')

            message_opcoes = bot.reply_to(message_horario, "🤖 Escolha uma opção 👇",
                                    reply_markup=markup)
            return
        
        
        try:
            horario_sessao = message_horario.text.split(',')
        except:
            horario_sessao = message_horario.text

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup.add('◀ Voltar')    

        message_texto = bot.reply_to(message_horario, "🤖 Ok! Agora Insira a Mensagem que será Enviada \n **Lembrando que deva ser inserido tags HTML como:\
                                                        <b></b> para negrito\n<a></a> para links"
                                                        ,reply_markup=markup)
        
        bot.register_next_step_handler(message_texto, registra_mensagem)
    
    except:
        message_erro = bot.reply_to(message_horario, "🤖❌ Algo deu Errado. Tente Novamente.", reply_markup=markup)


def registra_canal(message_canal):
    global novo_repasse, chat_id, id_canal

    try:

        if message_canal.text in ['◀ Voltar']:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','🟢 Ativar Envio de Mensagens','⚙ Cadastrar Envio', '📝 Editar info Chats', '📜 Envios Cadastrados','🗑 Apagar Envio','🛑 Pausar Envios de Mensagens')

            message_opcoes = bot.reply_to(message_canal, "🤖 Escolha uma opção 👇",
                                    reply_markup=markup)
            return
        

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup.add('◀ Voltar')

        ##PRIMEIRO TENTAR EXCLUIR O CANAL (VALIDO PARA EDIÇÃO DE CANAL)
        try:

            #ATUALIZANDO O ARQUIVO TXT
            lista_chats = ler_arquivo_txt_chats()


            #PEGANDO O CHAT_ID DO CANAL DESTINO
            for key, values in lista_chats.items():
                if key == message_canal.text:
                    id_canal = str(values[0])


            #EXCLUIR REGISTRO DO CANAL DESTINO
            chat_excluir = message_canal.text

            #ATUALIZANDO O ARQUIVO TXT
            lista_chats = ler_arquivo_txt_chats()
            
            #REMOVENDO DADO DO DICT
            lista_chats.pop(chat_excluir)
            
            #ATUALIZANDO TXT
            atualizar_arquivo_txt_chats(lista_chats)

            for key, value in dicionario_canais_telegram.items():
                if key == id_canal or str(value) == id_canal or id_canal == str(value).replace('-',''):
                    
                    chat_id = int(str(value))
                    
                    message_destino = bot.reply_to(message_canal, "🤖✅ Tudo Certo! Agora Escolha os Horários que a Mensagem será Enviada no Formato: hora:minuto:segundo,hora:minuto:segundo\
                                                Exemplo: 13:45:09,14:10:05,08:06:15 👇", reply_markup=markup)
                    bot.register_next_step_handler(message_destino, registrar_horario_envio)
                    
                    return

        except:
            try:
            
                for key, value in dicionario_canais_telegram.items():
                    if key == message_canal.text or str(value) == message_canal.text or message_canal.text == str(value).replace('-',''):
                        
                        chat_id = int(str(value))
                        
                        message_destino = bot.reply_to(message_canal, "🤖✅ Tudo Certo! Agora Escolha os Horários que a Mensagem será Enviada no Formato: hora:minuto:segundo,hora:minuto:segundo\
                                                    Exemplo: 13:45:09,14:10:05,08:06:15 👇", reply_markup=markup)
                        bot.register_next_step_handler(message_destino, registrar_horario_envio)
                        
                        return
                
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                markup = markup.add('/start','🟢 Ativar Envio de Mensagens','⚙ Cadastrar Envio', '📝 Editar info Chats', '📜 Envios Cadastrados','🗑 Apagar Envio','🛑 Pausar Envios de Mensagens')
            
            except:
                message_erro = bot.reply_to(message_canal, "🤖❌ Não Encontrei o Chat_ID Inserido. Tente Novamente.", reply_markup=markup)

        
    except:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','🟢 Ativar Envio de Mensagens','⚙ Cadastrar Envio', '📝 Editar info Chats', '📜 Envios Cadastrados','🗑 Apagar Envio','🛑 Pausar Envios de Mensagens')

        message_erro = bot.reply_to(message_canal, "🤖❌ Algo deu Errado. Tente Novamente.", reply_markup=markup)


def registra_mensagem(message_texto):
    try:

        if message_texto.text in ['◀ Voltar']:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','🟢 Ativar Envio de Mensagens','⚙ Cadastrar Envio', '📝 Editar info Chats', '📜 Envios Cadastrados','🗑 Apagar Envio','🛑 Pausar Envios de Mensagens')

            message_opcoes = bot.reply_to(message_texto, "🤖 Escolha uma opção 👇",
                                    reply_markup=markup)
            return
        

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','🟢 Ativar Envio de Mensagens','⚙ Cadastrar Envio', '📝 Editar info Chats', '📜 Envios Cadastrados','🗑 Apagar Envio','🛑 Pausar Envios de Mensagens')
        novo_repasse = {}
        
        msg_text_id = message_texto.message_id
        chat_from =  str(message_texto.chat.id)

        novo_repasse[globals()[f'apelido']] = [chat_id, horario_sessao, msg_text_id, chat_from]

        #ATUALIZANDO O ARQUIVO TXT
        lista_chats = ler_arquivo_txt_chats()

        if lista_chats == '':
            lista_chats = novo_repasse
        else:
            lista_chats.update(novo_repasse)
        
        atualizar_arquivo_txt_chats(lista_chats)

        message_destino = bot.reply_to(message_texto, "🤖 Envio Cadastrado com Sucesso! ✅", reply_markup=markup)

        return


    except:

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','🟢 Ativar Envio de Mensagens','⚙ Cadastrar Envio', '📝 Editar info Chats', '📜 Envios Cadastrados','🗑 Apagar Envio','🛑 Pausar Envios de Mensagens')
        
        message_erro = bot.reply_to(message_texto, "🤖❌ Algo deu Errado. Tente Novamente.", reply_markup=markup)


def registrar_repasse_excluido(message_excluir_repasse):

    try:

        if message_excluir_repasse.text in ['◀ Voltar']:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','🟢 Ativar Envio de Mensagens','⚙ Cadastrar Envio', '📝 Editar info Chats', '📜 Envios Cadastrados','🗑 Apagar Envio','🛑 Pausar Envios de Mensagens')

            message_opcoes = bot.reply_to(message_excluir_repasse, "🤖 Escolha uma opção 👇",
                                    reply_markup=markup)
            return
        
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','🟢 Ativar Envio de Mensagens','⚙ Cadastrar Envio', '📝 Editar info Chats', '📜 Envios Cadastrados','🗑 Apagar Envio','🛑 Pausar Envios de Mensagens')

        
        dado_excluir = message_excluir_repasse.text
        
        #ATUALIZANDO O ARQUIVO TXT
        lista_chats = ler_arquivo_txt_chats()
        
        #REMOVENDO DADO DO DICT
        lista_chats.pop(dado_excluir)
        
        #ATUALIZANDO TXT
        atualizar_arquivo_txt_chats(lista_chats)

        message_destino = bot.reply_to(message_excluir_repasse, "🤖 Chat Removido com Sucesso! ✅", reply_markup=markup)

        return

    except:

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','🟢 Ativar Envio de Mensagens','⚙ Cadastrar Envio', '📝 Editar info Chats', '📜 Envios Cadastrados','🗑 Apagar Envio','🛑 Pausar Envios de Mensagens')

        message_erro = bot.reply_to(message_excluir_repasse, "🤖❌ Algo deu Errado. Tente Novamente.", reply_markup=markup)





if __name__ == '__main__':
    try:

        inicio()

        print('FAZENDO CONEXÃO COM TELEGRAM USANDO O NÚMERO CADASTRADO........\n\n')

        time.sleep(3)

        bot_status = 0

        client, CHAVE_API, loop = pegar_chaves()

        dicionario_canais_telegram = listar_canais_telegram(client)

        dicionario_chats_cadastrados = ler_arquivo_txt_chats()

        bot = bot_telegram(CHAVE_API)

        print('\n\nCONEXÃO REALIZADA COM SUCESSO!')

        print('\n\n\n\n################################# AGUARDANDO COMANDOS #################################')

    except:
        print('\n\nNÃO CONSEGUI REALIZAR A CONEXÃO COM OS DADOS INFORMADOS. REVEJA OS DADOS INSERIDOS.')
        print('\nENCERRANDO O PROGRAMA!! ATÉ MAIS!!!')
        exit()

    


    @bot.message_handler(commands=['⚙ Cadastrar_Envio'])
    def cadastrar_repasse(message):

        try:
        
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
            
            markup.add('◀ Voltar') 
    

            try:
                message_apelido = bot.reply_to(message, "🤖 Ok! Insira um apelido para lebrete do cadastro 👇", reply_markup=markup)
                bot.register_next_step_handler(message_apelido, registra_apelido)
            except:
                #Init keyboard markup
                markup_except = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                markup_except.add('◀ Voltar')   
                message_apelido = bot.reply_to(message, "🤖 Ok! Insira um apelido para lebrete do cadastro 👇", reply_markup=markup_except)
                bot.register_next_step_handler(message_apelido, registra_apelido)

        except:
            message_erro = bot.reply_to(message, "🤖❌ Algo deu Errado. Tente Novamente.", reply_markup=markup)


    @bot.message_handler(commands=['📝 Editar_info_Chats'])
    def editar_info_chats(message):
        try:
            #PEGANDO NOME DOS CHATS
            lista_chats = ler_arquivo_txt_chats()
            lista_nome_chats = []
            for chat in lista_chats.keys():
                lista_nome_chats.append(chat)
            
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            #Add to buttons by list with ours generate_buttons function.
            markup_estrategias = generate_buttons_estrategias([ nome_chat for nome_chat in lista_nome_chats], markup)    
            markup_estrategias.add('◀ Voltar')

            message_excluir_repasse = bot.reply_to(message, "🤖 Escolha o chat a ser editado 👇", reply_markup=markup_estrategias)
            bot.register_next_step_handler(message_excluir_repasse, registra_canal)
        
        except:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','🟢 Ativar Envio de Mensagens','⚙ Cadastrar Envio', '📝 Editar info Chats', '📜 Envios Cadastrados','🗑 Apagar Envio','🛑 Pausar Envios de Mensagens')

            message_erro = bot.reply_to(message, "🤖❌ Algo deu Errado. Tente Novamente.", reply_markup=markup)


    @bot.message_handler(commands=['📜 Envios_Cadastradas'])
    def repasses_cadastrados(message):

        try:

            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','🟢 Ativar Envio de Mensagens','⚙ Cadastrar Envio', '📝 Editar info Chats', '📜 Envios Cadastrados','🗑 Apagar Envio','🛑 Pausar Envios de Mensagens')

            bot.reply_to(message, "🤖 Ok! Listando Canais Cadastrados", reply_markup=markup)
            
            lista_chats = ler_arquivo_txt_chats()
            for chat, value in lista_chats.items():
                apelido = chat
                nome_chat = dicionario_canal_nome[value[0]]
                horario = value[1]
                texto = value[2]

                bot.send_message(message.chat.id, 
f'===========================\n\
Apelido ⏩ {apelido} \n\
Chat ⏩ {nome_chat}\n\
Horarios ⏩ {horario}\n\
ID da Mensagem ⏩ {texto}\n\
===========================', parse_mode='HTML')
        
        except:
            pass


    @bot.message_handler(commands=['🗑 Apagar_Envio'])
    def apagar_repasse(message):
        try:
            #PEGANDO NOME DOS CHATS
            lista_chats = ler_arquivo_txt_chats()
            lista_nome_chats = []
            for chat in lista_chats.keys():
                nome_chat = chat
                lista_nome_chats.append(nome_chat)
            
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
            markup = markup.add('/start','🟢 Ativar Envio de Mensagens','⚙ Cadastrar Envio', '📝 Editar info Chats', '📜 Envios Cadastrados','🗑 Apagar Envio','🛑 Pausar Envios de Mensagens')

            message_erro = bot.reply_to(message, "🤖❌ Algo deu Errado. Tente Novamente.", reply_markup=markup)


    @bot.message_handler(commands=['🛑 Pausar_Envio_Mensagem'])
    def pausar_repasses(message):
        global bot_status

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','🟢 Ativar Envio de Mensagens','⚙ Cadastrar Envio', '📝 Editar info Chats', '📜 Envios Cadastrados','🗑 Apagar Envio','🛑 Pausar Envios de Mensagens')

        bot_status = 0

        message_final = bot.reply_to(message, "🤖🔴 Repasse Pausado com Sucesso! ✅", reply_markup=markup)


    @bot.message_handler(commands=['start'])
    def start(message):

        if str(message.chat.id):
            
            #ID USUARIO
            id_usuario = message.chat.id

            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

            markup = markup.add('/start','🟢 Ativar Envio de Mensagens','⚙ Cadastrar Envio', '📝 Editar info Chats', '📜 Envios Cadastrados','🗑 Apagar Envio','🛑 Pausar Envios de Mensagens')


            message_opcoes = bot.reply_to(message, f"🤖 Olá {message.json['from']['first_name']}, você está usando o Bot que Repassa Mensagens! Escolha uma opção 👇",
                                    reply_markup=markup)
            
            #Here we assign the next handler function and pass in our response from the user. 
            bot.register_next_step_handler(message_opcoes, opcoes)
        
        else:
            message_error = bot.reply_to(message, "🤖 Você não tem permissão para acessar este Bot ❌🚫")

    
    @bot.message_handler()
    def opcoes(message_opcoes):


        if message_opcoes.text in ['⚙ Cadastrar Envio']:
            print('Cadastrar Repasse')
            cadastrar_repasse(message_opcoes)

        if message_opcoes.text in ['📝 Editar info Chats']:
            print('Editar Informações Chat')
            editar_info_chats(message_opcoes)
            

        if message_opcoes.text in['📜 Envios Cadastrados']:
            print('Repasses Cadastrados')
            repasses_cadastrados(message_opcoes)
            

        if message_opcoes.text in ['🗑 Apagar Envio']:
            print('Apagar Repasse')
            apagar_repasse(message_opcoes)

        
        if message_opcoes.text in ['🟢 Ativar Envio de Mensagens']:
            global bot_status
            global parar

            print('Ativar Bot')

            if bot_status == 1:

                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                markup = markup.add('/start','🟢 Ativar Envio de Mensagens','⚙ Cadastrar Envio', '📝 Editar info Chats', '📜 Envios Cadastrados','🗑 Apagar Envio','🛑 Pausar Envios de Mensagens')

                message_canal = bot.reply_to(message_opcoes, "🤖⛔ Bot já está ativado",
                                    reply_markup=markup)

            
            else:
                #Init keyboard markup
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                markup = markup.add('/start','🟢 Ativar Envio de Mensagens','⚙ Cadastrar Envio', '📝 Editar info Chats', '📜 Envios Cadastrados','🗑 Apagar Envio','🛑 Pausar Envios de Mensagens')

                message_canal = bot.reply_to(message_opcoes, "🤖 Repasses Iniciado com Sucesso! ",
                                        reply_markup=markup)

                bot_status = 1
                parar = 0

                print('#################################  INICIANDO OS REPASSES  #################################')
                print()
                horario_sinal()

        
        if message_opcoes.text in ['🛑 Pausar Envios de Mensagens']:
            print('Pausar Bot')
            pausar_repasses(message_opcoes)
        


    while True:
        try:
            bot.infinity_polling(timeout=600)
        except:
            bot.infinity_polling(timeout=600)



    

