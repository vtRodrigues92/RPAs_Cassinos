import telebot, ast
from telegram.ext import *
from telebot import *
from datetime import datetime, timedelta





def inicio():
    print()
    print('                                #################################################################')
    print('                                #############  BOT MENSAGENS PERSONALIZADAS  ####################')
    print('                                #################################################################')
    print('                                ##################### SEJA BEM VINDO ############################')
    print('                                #################################################################')
    print('                                ############# DESENVOLVIDO POR VICTOR RODRIGUES #################')
    print('                                #################################################################\n')
    print('Versão = 1.0.0')
    print('Ambiente: Produção\n\n\n\n')


def enviar_mensagem(id_usuario):

    while True:
        try:

            ### VALIDANDO SE FOI SOLICITADO O STOP DO BOT
            if parar != 0:
                break


            ### LENDO CANAIS CADASTRADOS
            lista_canais = ler_arquivo_txt('canais.txt')
            ### LENDO MENSAGEM CADASTRADA
            with open ('mensagem.txt', encoding='UTF-8') as arquivo: 
                mensagem = arquivo.read()
            ### LENDO BOTÕES CADASTRADOS
            lista_botoes = ler_arquivo_txt('botoes.txt')
            keyboard = []
            for key, value in lista_botoes.items():
                keyboard.append([types.InlineKeyboardButton(key, url=value)])

            reply_markup = types.InlineKeyboardMarkup(keyboard)

            ### ENVIANDO MENSAGEM PARA O CANAL
            for key, value in lista_canais.items():
                for canal in value:
                    try:
                        bot.send_message(canal, mensagem, parse_mode='HTML', reply_markup=reply_markup)
                    except:
                        bot.send_message(id_usuario, f"⚠️ NÃO CONSEGUI ENVIAR MENSAGEM PARA O CANAL {canal}")
                
            time.sleep(intervalo)

        except:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','🟢 Ativar Envio de Mensagem', 
                                '🧩 Cadastrar Canal', 
                                '🗒️ Canais Cadastrados',
                                '🗑 Apagar Canal',
                                '⚙ Cadastrar Botão', 
                                '📜 Botões Cadastrados', 
                                '🗑 Apagar Botão', 
                                '📝 MSG Cadastrada', 
                                '📝 Editar MSG Cadastrada',
                                f'⏱️ Intervalo de Envio = {intervalo}',
                                '🛑 Pausar Envio de Mensagem')

            message_erro = bot.send_message(id_usuario, "🤖❌ Algo deu Errado. Tente Novamente.", reply_markup=markup)
            break


def pegar_chaves():
    with open ('senhas.txt', 'r', encoding='UTF-8') as file:
        
        arquivo = file.readlines()
        CHAVE_API = arquivo[0].split(' ')[1]

    return CHAVE_API


def bot_telegram(token):

    bot = telebot.TeleBot(token)

    return bot


def generate_buttons_estrategias(bts_names, markup):
    for button in bts_names:
        markup.add(types.KeyboardButton(button))
    return markup


def ler_arquivo_txt(arquivo):
    with open(arquivo, 'r', encoding='UTF-8') as file:
        canais = file.read()
        if canais == '':

            dicionario = ''
        
        else:

            dicionario = ast.literal_eval(canais)

    return dicionario


def atualizar_arquivo_txt(arquivo, lista):
    with open(arquivo, 'w', encoding='UTF-8') as arquivo:
        arquivo.write(str(lista))
        arquivo.close()


def registra_canal(message_canal):

    try:

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','🟢 Ativar Envio de Mensagem', 
                                    '🧩 Cadastrar Canal', 
                                    '🗒️ Canais Cadastrados',
                                    '🗑 Apagar Canal',
                                    '⚙ Cadastrar Botão', 
                                    '📜 Botões Cadastrados', 
                                    '🗑 Apagar Botão', 
                                    '📝 MSG Cadastrada', 
                                    '📝 Editar MSG Cadastrada',
                                    f'⏱️ Intervalo de Envio = {intervalo}',
                                    '🛑 Pausar Envio de Mensagem')

        novo_canal = {}
        
        #ATUALIZANDO O ARQUIVO TXT
        lista_canais = ler_arquivo_txt('canais.txt')
        
        if lista_canais == '':
            
            novo_canal['canais'] = [message_canal.text]
            lista_canais = novo_canal

        else:
            for key, value in lista_canais.items():
                lista_canais = value
                lista_canais.append(message_canal.text)
                novo_canal[key] = lista_canais
                break
        
        atualizar_arquivo_txt('canais.txt', novo_canal)

        message_final = bot.reply_to(message_canal, "🤖 Canal Cadastrado com Sucesso! ✅", reply_markup=markup)

        return


    except:

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','🟢 Ativar Envio de Mensagem', 
                                    '🧩 Cadastrar Canal', 
                                    '🗒️ Canais Cadastrados',
                                    '🗑 Apagar Canal',
                                    '⚙ Cadastrar Botão', 
                                    '📜 Botões Cadastrados', 
                                    '🗑 Apagar Botão', 
                                    '📝 MSG Cadastrada', 
                                    '📝 Editar MSG Cadastrada',
                                    f'⏱️ Intervalo de Envio = {intervalo}',
                                    '🛑 Pausar Envio de Mensagem')

        message_erro = bot.reply_to(message_canal, "🤖❌ Algo deu Errado. Tente Novamente.", reply_markup=markup)


def registrar_canal_excluido(message_excluir_canal):

    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','🟢 Ativar Envio de Mensagem', 
                                    '🧩 Cadastrar Canal', 
                                    '🗒️ Canais Cadastrados',
                                    '🗑 Apagar Canal',
                                    '⚙ Cadastrar Botão', 
                                    '📜 Botões Cadastrados', 
                                    '🗑 Apagar Botão', 
                                    '📝 MSG Cadastrada', 
                                    '📝 Editar MSG Cadastrada',
                                    f'⏱️ Intervalo de Envio = {intervalo}',
                                    '🛑 Pausar Envio de Mensagem')

        
        #ATUALIZANDO O ARQUIVO TXT
        lista_canais = ler_arquivo_txt('canais.txt')

        for key, value in lista_canais.items():
            for canal in value:
                if canal == message_excluir_canal.text:
                    value.remove(message_excluir_canal.text)
                    break
        
       
        #ATUALIZANDO TXT
        atualizar_arquivo_txt('canais.txt', lista_canais)

        message_destino = bot.reply_to(message_excluir_canal, "🤖 Canal Removido com Sucesso! ✅", reply_markup=markup)

        return

    except:

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','🟢 Ativar Envio de Mensagem', 
                                    '🧩 Cadastrar Canal', 
                                    '🗒️ Canais Cadastrados',
                                    '🗑 Apagar Canal',
                                    '⚙ Cadastrar Botão', 
                                    '📜 Botões Cadastrados', 
                                    '🗑 Apagar Botão', 
                                    '📝 MSG Cadastrada', 
                                    '📝 Editar MSG Cadastrada',
                                    f'⏱️ Intervalo de Envio = {intervalo}',
                                    '🛑 Pausar Envio de Mensagem')

        message_erro = bot.reply_to(message_excluir_canal, "🤖❌ Algo deu Errado. Tente Novamente.", reply_markup=markup)


def registra_botao(message_botao):

    try:

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','🟢 Ativar Envio de Mensagem', 
                                    '🧩 Cadastrar Canal', 
                                    '🗒️ Canais Cadastrados',
                                    '🗑 Apagar Canal',
                                    '⚙ Cadastrar Botão', 
                                    '📜 Botões Cadastrados', 
                                    '🗑 Apagar Botão', 
                                    '📝 MSG Cadastrada', 
                                    '📝 Editar MSG Cadastrada',
                                    f'⏱️ Intervalo de Envio = {intervalo}',
                                    '🛑 Pausar Envio de Mensagem')

        novo_botao = {}
        dados = message_botao.text.split(',')
        novo_botao[dados[0]] = dados[1]

        #ATUALIZANDO O ARQUIVO TXT
        lista_botoes = ler_arquivo_txt('botoes.txt')
        
        if lista_botoes == '':
            
            lista_botoes = novo_botao

        else:
            lista_botoes.update(novo_botao)
            

        atualizar_arquivo_txt('botoes.txt', lista_botoes)

        message_final = bot.reply_to(message_botao, "🤖 Botão Adicionado com Sucesso! ✅", reply_markup=markup)

        return


    except:

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','🟢 Ativar Envio de Mensagem', 
                                    '🧩 Cadastrar Canal', 
                                    '🗒️ Canais Cadastrados',
                                    '🗑 Apagar Canal',
                                    '⚙ Cadastrar Botão', 
                                    '📜 Botões Cadastrados', 
                                    '🗑 Apagar Botão', 
                                    '📝 MSG Cadastrada', 
                                    '📝 Editar MSG Cadastrada',
                                    f'⏱️ Intervalo de Envio = {intervalo}',
                                    '🛑 Pausar Envio de Mensagem')

        message_erro = bot.reply_to(message_botao, "🤖❌ Algo deu Errado. Tente Novamente.", reply_markup=markup)


def registrar_botao_excluido(message_excluir_botao):

    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','🟢 Ativar Envio de Mensagem', 
                                    '🧩 Cadastrar Canal', 
                                    '🗒️ Canais Cadastrados',
                                    '🗑 Apagar Canal',
                                    '⚙ Cadastrar Botão', 
                                    '📜 Botões Cadastrados', 
                                    '🗑 Apagar Botão', 
                                    '📝 MSG Cadastrada', 
                                    '📝 Editar MSG Cadastrada',
                                    f'⏱️ Intervalo de Envio = {intervalo}',
                                    '🛑 Pausar Envio de Mensagem')

        
        #ATUALIZANDO O ARQUIVO TXT
        lista_botoes = ler_arquivo_txt('botoes.txt')

        for key, value in lista_botoes.items():
            if key == message_excluir_botao.text:
                lista_botoes.pop(key)
                break
        
       
        #ATUALIZANDO TXT
        atualizar_arquivo_txt('botoes.txt', lista_botoes)

        message_destino = bot.reply_to(message_excluir_botao, "🤖 Botão Removido com Sucesso! ✅", reply_markup=markup)

        return

    except:

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','🟢 Ativar Envio de Mensagem', 
                                    '🧩 Cadastrar Canal', 
                                    '🗒️ Canais Cadastrados',
                                    '🗑 Apagar Canal',
                                    '⚙ Cadastrar Botão', 
                                    '📜 Botões Cadastrados', 
                                    '🗑 Apagar Botão', 
                                    '📝 MSG Cadastrada', 
                                    '📝 Editar MSG Cadastrada',
                                    f'⏱️ Intervalo de Envio = {intervalo}',
                                    '🛑 Pausar Envio de Mensagem')

        message_erro = bot.reply_to(message_excluir_botao, "🤖❌ Algo deu Errado. Tente Novamente.", reply_markup=markup)


def registrar_nova_mensagem(message_editar_msg):

    if message_editar_msg.text == '◀ Voltar':
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','🟢 Ativar Envio de Mensagem', 
                                    '🧩 Cadastrar Canal', 
                                    '🗒️ Canais Cadastrados',
                                    '🗑 Apagar Canal',
                                    '⚙ Cadastrar Botão', 
                                    '📜 Botões Cadastrados', 
                                    '🗑 Apagar Botão', 
                                    '📝 MSG Cadastrada', 
                                    '📝 Editar MSG Cadastrada',
                                    f'⏱️ Intervalo de Envio = {intervalo}',
                                    '🛑 Pausar Envio de Mensagem')
        
        message_opcoes = bot.reply_to(message_editar_msg, "🤖 Escolha uma opção 👇",
                                    reply_markup=markup)
            
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(message_opcoes, opcoes)
    
    else:
        try:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','🟢 Ativar Envio de Mensagem', 
                                '🧩 Cadastrar Canal', 
                                '🗒️ Canais Cadastrados',
                                '🗑 Apagar Canal',
                                '⚙ Cadastrar Botão', 
                                '📜 Botões Cadastrados', 
                                '🗑 Apagar Botão', 
                                '📝 MSG Cadastrada', 
                                '📝 Editar MSG Cadastrada',
                                f'⏱️ Intervalo de Envio = {intervalo}',
                                '🛑 Pausar Envio de Mensagem')
            
            with open ('mensagem.txt', 'w', encoding='UTF-8') as arquivo: 
                        arquivo.write(message_editar_msg.text)

            message_sucess = bot.reply_to(message_editar_msg, "🤖 Mensgem Editada com Sucesso! ✅", reply_markup=markup)
            
        except:
            pass


def registrar_novo_intervalo(message_editar_valor):
    global intervalo

    try:
        if message_editar_valor.text == '◀ Voltar':
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','🟢 Ativar Envio de Mensagem', 
                                '🧩 Cadastrar Canal', 
                                '🗒️ Canais Cadastrados',
                                '🗑 Apagar Canal',
                                '⚙ Cadastrar Botão', 
                                '📜 Botões Cadastrados', 
                                '🗑 Apagar Botão', 
                                '📝 MSG Cadastrada', 
                                '📝 Editar MSG Cadastrada',
                                f'⏱️ Intervalo de Envio = {intervalo}',
                                '🛑 Pausar Envio de Mensagem')
            
            message_opcoes = bot.reply_to(message_editar_valor, "🤖 Escolha uma opção 👇",
                                        reply_markup=markup)
                
            #Here we assign the next handler function and pass in our response from the user. 
            bot.register_next_step_handler(message_opcoes, opcoes)

        else:

            intervalo = int(message_editar_valor.text)

            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','🟢 Ativar Envio de Mensagem', 
                                    '🧩 Cadastrar Canal', 
                                    '🗒️ Canais Cadastrados',
                                    '🗑 Apagar Canal',
                                    '⚙ Cadastrar Botão', 
                                    '📜 Botões Cadastrados', 
                                    '🗑 Apagar Botão', 
                                    '📝 MSG Cadastrada', 
                                    '📝 Editar MSG Cadastrada',
                                    f'⏱️ Intervalo de Envio = {intervalo}',
                                    '🛑 Pausar Envio de Mensagem')

            message_success = bot.reply_to(message_editar_valor, "🤖 Intervalo Editado com Sucesso ✅",
                                    reply_markup=markup)
            
    except:

        message_error = bot.reply_to(message_editar_valor, "🤖❌ Algo deu Errado. Tente Novamente.")


def pausar_bot():
     while True:
        try:
            global parar
            parar = 1
            time.sleep(1)
            break

        except:
            continue




if __name__ == '__main__':
    try:
        inicio()

        bot_status = 0
        intervalo = 60

        CHAVE_API = pegar_chaves()

        bot = bot_telegram(CHAVE_API)

        

        print('\n\n\n\n################################# AGUARDANDO COMANDOS #################################')

    except:
        print('\n\nNÃO CONSEGUI REALIZAR A CONEXÃO COM OS DADOS INFORMADOS. REVEJA OS DADOS INSERIDOS.')
        print('\nENCERRANDO O PROGRAMA!! ATÉ MAIS!!!')
        exit()

    


    @bot.message_handler(commands=['🧩 Cadastrar_Canal'])
    def cadastrar_canal(message):

        try:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
            
            markup.add('◀ Voltar')    

            message_canal = bot.reply_to(message, "🤖 Ok! Insira o CHAT_ID do Canal 👇", reply_markup=markup)
            bot.register_next_step_handler(message_canal, registra_canal)
        
        except:
            message_erro = bot.reply_to(message, "🤖❌ Algo deu Errado. Tente Novamente.", reply_markup=markup)


    @bot.message_handler(commands=['🗒️ Canais_Cadastrados'])
    def canais_cadastrados(message):

        try:

            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','🟢 Ativar Envio de Mensagem', 
                                '🧩 Cadastrar Canal', 
                                '🗒️ Canais Cadastrados',
                                '🗑 Apagar Canal',
                                '⚙ Cadastrar Botão', 
                                '📜 Botões Cadastrados', 
                                '🗑 Apagar Botão', 
                                '📝 MSG Cadastrada', 
                                '📝 Editar MSG Cadastrada',
                                f'⏱️ Intervalo de Envio = {intervalo}',
                                '🛑 Pausar Envio de Mensagem')

            bot.reply_to(message, "🤖 Ok! Listando os Canais Cadastrados", reply_markup=markup)
            
            lista_canais = ler_arquivo_txt('canais.txt')
            
            for key, value in lista_canais.items():
                for canal in value:
                
                    bot.send_message(message.chat.id, 
                                     
f'===========================\n\
{canal}\n\
===========================')

        
        except:
            pass


    @bot.message_handler(commands=['🗑 Apagar_Canal'])
    def apagar_canal(message):
        try:
            #PEGAR LISTA DE CANAIS
            lista_canais = ler_arquivo_txt('canais.txt')

            for key, value in lista_canais.items():
                canais = value
                break

            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            #Add to buttons by list with ours generate_buttons function.
            markup_estrategias = generate_buttons_estrategias([ canal for canal in canais ], markup)    
            markup_estrategias.add('◀ Voltar')

            message_excluir_canal = bot.reply_to(message, "🤖 Escolha o Canal a ser excluído 👇", reply_markup=markup_estrategias)
            bot.register_next_step_handler(message_excluir_canal, registrar_canal_excluido)
        
        except:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','🟢 Ativar Envio de Mensagem', 
                                '🧩 Cadastrar Canal', 
                                '🗒️ Canais Cadastrados',
                                '🗑 Apagar Canal',
                                '⚙ Cadastrar Botão', 
                                '📜 Botões Cadastrados', 
                                '🗑 Apagar Botão', 
                                '📝 MSG Cadastrada', 
                                '📝 Editar MSG Cadastrada',
                                f'⏱️ Intervalo de Envio = {intervalo}',
                                '🛑 Pausar Envio de Mensagem')

            message_erro = bot.reply_to(message, "🤖❌ Algo deu Errado. Tente Novamente.", reply_markup=markup)


    @bot.message_handler(commands=['⚙ Cadastrar_Botão'])
    def cadastrar_botao(message):

        try:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
            
            markup.add('◀ Voltar')    

            message_botao = bot.reply_to(message, "🤖 Ok! Insira o Texto do Botão e o Link de Redirecionamento Separado por Vírgula ( EX: Jogo123,www.jogo123.com ) 👇", reply_markup=markup)
            bot.register_next_step_handler(message_botao, registra_botao)
        
        except:
            message_erro = bot.reply_to(message, "🤖❌ Algo deu Errado. Tente Novamente.", reply_markup=markup)


    @bot.message_handler(commands=['📜 Botões_Cadastrados'])
    def botoes_cadastrados(message):

        try:

            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','🟢 Ativar Envio de Mensagem', 
                                '🧩 Cadastrar Canal', 
                                '🗒️ Canais Cadastrados',
                                '🗑 Apagar Canal',
                                '⚙ Cadastrar Botão', 
                                '📜 Botões Cadastrados', 
                                '🗑 Apagar Botão', 
                                '📝 MSG Cadastrada', 
                                '📝 Editar MSG Cadastrada',
                                f'⏱️ Intervalo de Envio = {intervalo}',
                                '🛑 Pausar Envio de Mensagem')

            bot.reply_to(message, "🤖 Ok! Listando os Botões Cadastrados", reply_markup=markup)
            
            lista_botoes = ler_arquivo_txt('botoes.txt')

            keyboard = []
            for key, value in lista_botoes.items():
                keyboard.append([types.InlineKeyboardButton(key, url=value)])

            reply_markup = types.InlineKeyboardMarkup(keyboard)

            msg = bot.send_message(message.chat.id, '🤖', reply_markup=reply_markup)

        
        except:
            pass

        
    @bot.message_handler(commands=['🗑 Apagar_Botão'])
    def apagar_botao(message):
        try:
            #PEGAR LISTA DE CANAIS
            lista_botoes = ler_arquivo_txt('botoes.txt')

            #for key, value in lista_botoes.items():
            #    canais = value
            #    break

            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            #Add to buttons by list with ours generate_buttons function.
            markup_botoes = generate_buttons_estrategias([ key for key,value in lista_botoes.items() ], markup)    
            markup_botoes.add('◀ Voltar')

            message_excluir_botao = bot.reply_to(message, "🤖 Escolha o Botão a ser excluído 👇", reply_markup=markup_botoes)
            bot.register_next_step_handler(message_excluir_botao, registrar_botao_excluido)
        
        except:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','🟢 Ativar Envio de Mensagem', 
                                '🧩 Cadastrar Canal', 
                                '🗒️ Canais Cadastrados',
                                '🗑 Apagar Canal',
                                '⚙ Cadastrar Botão', 
                                '📜 Botões Cadastrados', 
                                '🗑 Apagar Botão', 
                                '📝 MSG Cadastrada', 
                                '📝 Editar MSG Cadastrada',
                                f'⏱️ Intervalo de Envio = {intervalo}',
                                '🛑 Pausar Envio de Mensagem')

            message_erro = bot.reply_to(message, "🤖❌ Algo deu Errado. Tente Novamente.", reply_markup=markup)


    @bot.message_handler(commands=['🛑 Pausar_Envio_de_Mensagem'])
    def pausar_envio_mensagem(message):

        if botStatus == 0:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

            message_final = bot.reply_to(message, "🤖⛔ Bot já está pausado ", reply_markup=markup)

        else:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

            print('\n\n')
            print('Pausar Bot')
            print('Parando o Bot....\n')
            botStatus = 0
            pausar_bot()

            message_final = bot.reply_to(message, "🤖 Ok! Bot pausado 🛑", reply_markup=markup)
            
            print('###################### AGUARDANDO COMANDOS ######################')


    @bot.message_handler(commands=['start'])
    def start(message):

        if str(message.chat.id):
            
            #ID USUARIO
            id_usuario = message.chat.id

            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','🟢 Ativar Envio de Mensagem', 
                                '🧩 Cadastrar Canal', 
                                '🗒️ Canais Cadastrados',
                                '🗑 Apagar Canal',
                                '⚙ Cadastrar Botão', 
                                '📜 Botões Cadastrados', 
                                '🗑 Apagar Botão', 
                                '📝 MSG Cadastrada', 
                                '📝 Editar MSG Cadastrada',
                                f'⏱️ Intervalo de Envio = {intervalo}',
                                '🛑 Pausar Envio de Mensagem')

            message_opcoes = bot.reply_to(message, f"🤖 Olá {message.json['from']['first_name']}, Você Está Usando o Bot de Mensagens Personalizadas! Escolha uma opção 👇",
                                    reply_markup=markup)
            
            #Here we assign the next handler function and pass in our response from the user. 
            bot.register_next_step_handler(message_opcoes, opcoes)
        
        else:
            message_error = bot.reply_to(message, "🤖 Você não tem permissão para acessar este Bot ❌🚫")

    
    @bot.message_handler()
    def opcoes(message_opcoes):

        if message_opcoes.text in ['🧩 Cadastrar Canal']:
            print('Cadastrar Canal')
            cadastrar_canal(message_opcoes)


        if message_opcoes.text in ['🗒️ Canais Cadastrados']:
            print('🗒️ Canais cadastrados')
            canais_cadastrados(message_opcoes)


        if message_opcoes.text in ['🗑 Apagar Canal']:
            print('Apagar Canal')
            apagar_canal(message_opcoes)


        if message_opcoes.text in ['⚙ Cadastrar Botão']:
            print('Cadastrar Botão')
            cadastrar_botao(message_opcoes)
            

        if message_opcoes.text in['📜 Botões Cadastrados']:
            print('Botões Cadastrados')
            botoes_cadastrados(message_opcoes)
            

        if message_opcoes.text in ['🗑 Apagar Botão']:
            print('Apagar Botão')
            apagar_botao(message_opcoes)

        
        if message_opcoes.text in ['📝 MSG Cadastrada']:
            try:

                with open ('mensagem.txt', encoding='UTF-8') as arquivo: 
                    mensagem = arquivo.read()

            except:pass

            try:
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                markup = markup.add('/start','🟢 Ativar Envio de Mensagem', 
                                '🧩 Cadastrar Canal', 
                                '🗒️ Canais Cadastrados',
                                '🗑 Apagar Canal',
                                '⚙ Cadastrar Botão', 
                                '📜 Botões Cadastrados', 
                                '🗑 Apagar Botão', 
                                '📝 MSG Cadastrada', 
                                '📝 Editar MSG Cadastrada',
                                f'⏱️ Intervalo de Envio = {intervalo}',
                                '🛑 Pausar Envio de Mensagem')

                message_editar_msg = bot.reply_to(message_opcoes, "🤖 Segue a Mensagem que Será Enviada para os Membros. 👇",
                                        reply_markup=markup)
                
                
                ### BOTÕES ###
                lista_botoes = ler_arquivo_txt('botoes.txt')

                keyboard = []
                for key, value in lista_botoes.items():
                    keyboard.append([types.InlineKeyboardButton(key, url=value)])

                reply_markup = types.InlineKeyboardMarkup(keyboard)


                ## ENVIANDO MENSAGEM
                msg = bot.send_message(message_opcoes.json['from']['id'], mensagem, parse_mode='HTML', reply_markup=reply_markup)
            
            
            except:
                message_error = bot.reply_to(message_opcoes, "🤖❌ Algo deu Errado. Tente Novamente.")

            
        if message_opcoes.text in ['📝 Editar MSG Cadastrada']:
            try:

                with open ('mensagem.txt', encoding='UTF-8') as arquivo: 
                    mensagem = arquivo.read()

            except:pass

            try:
                #Init keyboard markup
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
                markup = markup.add(
                                    '◀ Voltar'
                                    )
    
                message_editar_msg = bot.reply_to(message_opcoes, "🤖 Perfeito! Segue a Mensagem Atual. Para Editar, Insira o Novo Texto 👇",
                                        reply_markup=markup)
                
                msg = bot.send_message(message_opcoes.json['from']['id'], mensagem)
            
                #Here we assign the next handler function and pass in our response from the user. 
                bot.register_next_step_handler(message_editar_msg, registrar_nova_mensagem)
            
            except:
                message_error = bot.reply_to(message_opcoes, "🤖❌ Algo deu Errado. Tente Novamente.")


        if message_opcoes.text in [f'⏱️ Intervalo de Envio = {intervalo}']:
            try:

                #Init keyboard markup
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
                markup = markup.add('◀ Voltar')

                message_editar_valor = bot.reply_to(message_opcoes, "🤖 Insira o Novo Valor em Segundos 👇",
                                        reply_markup=markup)

                #Here we assign the next handler function and pass in our response from the user. 
                bot.register_next_step_handler(message_editar_valor, registrar_novo_intervalo)
            
            except:
                message_error = bot.reply_to(message_opcoes, "🤖❌ Algo deu Errado. Tente Novamente.")


        if message_opcoes.text in ['🟢 Ativar Envio de Mensagem']:
            global bot_status
            global parar

            print('Ativar Bot')

            if bot_status == 1:

                #Init keyboard markup
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                markup = markup.add('/start','🟢 Ativar Envio de Mensagem', 
                                '🧩 Cadastrar Canal', 
                                '🗒️ Canais Cadastrados',
                                '🗑 Apagar Canal',
                                '⚙ Cadastrar Botão', 
                                '📜 Botões Cadastrados', 
                                '🗑 Apagar Botão', 
                                '📝 MSG Cadastrada', 
                                '📝 Editar MSG Cadastrada',
                                f'⏱️ Intervalo de Envio = {intervalo}',
                                '🛑 Pausar Envio de Mensagem')
                
                message_canal = bot.reply_to(message_opcoes, "🤖⛔ Bot já está ativado",
                                    reply_markup=markup)

            
            else:
                #Init keyboard markup
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                markup = markup.add('/start','🟢 Ativar Envio de Mensagem', 
                                '🧩 Cadastrar Canal', 
                                '🗒️ Canais Cadastrados',
                                '🗑 Apagar Canal',
                                '⚙ Cadastrar Botão', 
                                '📜 Botões Cadastrados', 
                                '🗑 Apagar Botão', 
                                '📝 MSG Cadastrada', 
                                '📝 Editar MSG Cadastrada',
                                f'⏱️ Intervalo de Envio = {intervalo}',
                                '🛑 Pausar Envio de Mensagem')
                
                message_canal = bot.reply_to(message_opcoes, "🤖 Repasses Iniciado com Sucesso! ✅",
                                        reply_markup=markup)

                bot_status = 1
                parar = 0

                print('#################################  INICIANDO OS REPASSES  #################################')
                print()
                enviar_mensagem(message_opcoes.chat.id)
                
        
        if message_opcoes.text in ['🛑 Pausar Envio de Mensagem']:
            print('Pausar Bot')
            pausar_envio_mensagem(message_opcoes)
        





    while True:
        try:
            bot.infinity_polling(timeout=1, long_polling_timeout=1)
            bot.infinity_polling(True)
        except:
            continue



    