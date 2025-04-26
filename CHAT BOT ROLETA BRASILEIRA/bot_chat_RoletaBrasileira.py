from selenium import webdriver
import time
import warnings
#from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from datetime import datetime, timedelta
import telebot
from telegram.ext import *
from telebot import *
import logging
import os


print()
print('                                #################################################################')
print('                                #############    CHAT BOT ROLETA BRASILEIRA    ##################')
print('                                #################################################################')
print('                                ##################### SEJA BEM VINDO ############################')
print('                                #################################################################')
print('                                ############# DESENVOLVIDO POR VICTOR RODRIGUES #################')
print('                                #################################################################\n')
print('Versão = 2.0.0')
print('Ambiente: Produção\n\n\n')

parar = 0


def auto_refresh():
    global horario_inicio

    horario_atual = datetime.today().strftime('%H:%M')
    tres_hora = timedelta(hours=1)
    horario_mais_tres = horario_inicio + tres_hora
    horario_refresh = horario_mais_tres.strftime('%H:%M')

    if horario_atual == horario_refresh:
        print('HORA DE REFRESHAR A PAGINA!!!!')
        logarSite()
        time.sleep(10)
        horario_inicio = datetime.now()


def inicio():
    global browser
    global url_roleta_brasileira
    global logger
    global horario_inicio
    global site_inicio

    horario_inicio = datetime.now()

    logger = logging.getLogger()

    site_inicio = r'https://launcher.betfair.com/?gameId=live-rolet-brasileria-cptl&returnURL=https%3A%2F%2Fcasino.betfair.com%2Fpt-br%2Fp%2Fcassino-ao-vivo&launchProduct=gaming&RPBucket=gaming&mode=real&dataChannel=ecasino&switchedToPopup=true'
    url_roleta_brasileira = 'https://www.esportiva.bet/#/game/casinolive?st=&p=0&t=1&g=playtech:RoletaBrasileria'

    # Definindo opções para o browser
    warnings.filterwarnings("ignore", category=DeprecationWarning) 
    chrome_options = webdriver.ChromeOptions() 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Opção para executar o prgrama em primeiro ou segundo plano
    escolha = int(input('Deseja que o programa mostre o navegador? [1]SIM [2]NÃO --> '))
    print()
    time.sleep(1)
    if escolha == 1:
        print('O programa será executado mostrando o navegador.\n')
    else:
        print('O programa será executado com o navegador oculto.\n')
        chrome_options.add_argument("--headless")

    #browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
    browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())


def logarSite():
    browser.get(site_inicio)
    try:
        browser.maximize_window()
    except:
        pass
    
    time.sleep(10)
    ''' Inserindo login e senha '''
    ''' Lendo o arquivo txt config-mensagens '''
    txt = open("canais.txt", "r", encoding="utf-8")
    mensagem_login = txt.readlines()
    usuario = mensagem_login[2].replace('\n','').split('= ')[1] 
    senha = mensagem_login[3].replace('\n','').split('= ')[1]
    ''' Mapeando elementos para inserir credenciais '''
    try:
        browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click() #cookies
    except:
        pass

    try:
        browser.find_element_by_xpath('//*[@id="username"]').send_keys(usuario) #Inserindo login
        browser.find_element_by_xpath('//*[@id="password"]').send_keys(senha) #Inserindo senha
        browser.find_element_by_xpath('//*[@id="login"]').click() #Clicando no btn login
        time.sleep(10)
    except:
        pass


def preparar_chat():

    contador = 0
    while contador <10:

        try:

            browser.find_element_by_xpath('//*[@class="desktop-chat__toggle-button"]').click()
            break
        
        except:
            contador+=1
            time.sleep(3)
            continue
    

def enviar_mensagem():
    
    sequencial = 0

    while True:

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass

        # Auto Refresh
        auto_refresh()
        
        contador_mensagem = 1
        
        while contador_mensagem <= 3:
            
            try:
                if contador_mensagem == 1:
                    
                    try:
                        browser.find_element_by_xpath('//*[@class="chat-input chat-input-layout chat-input_placeholder needsclick"]').send_keys('#'+str(sequencial)+message1)
                        sequencial+=1
                    except:
                        browser.find_element_by_xpath('//*[@class="chat-input chat-input-layout needsclick"]').send_keys('#'+str(sequencial)+message1)
                        sequencial+=1

                    print(datetime.now(), '\n', message1, '\n\n', '='*100, '\n\n')

                    time.sleep(1)
                    browser.find_element_by_xpath('//*[@class="chat-controls-button__icon"]').click()
                    contador_mensagem+=1
                    time.sleep(30)

                elif contador_mensagem == 2:
                    
                    try:
                        browser.find_element_by_xpath('//*[@class="chat-input chat-input-layout chat-input_placeholder needsclick"]').send_keys('#'+str(sequencial)+message2)
                        sequencial+=1
                    except:
                        browser.find_element_by_xpath('//*[@class="chat-input chat-input-layout needsclick"]').send_keys('#'+str(sequencial)+message2)
                        sequencial+=1

                    print(datetime.now(), '\n', message2, '\n\n', '='*100, '\n\n')
                    time.sleep(1)
                    browser.find_element_by_xpath('//*[@class="chat-controls-button__icon"]').click()
                    contador_mensagem+=1
                    time.sleep(30)

                elif contador_mensagem == 3:
                    
                    try:
                        browser.find_element_by_xpath('//*[@class="chat-input chat-input-layout chat-input_placeholder needsclick"]').send_keys('#'+str(sequencial)+message3)
                        sequencial+=1
                    except:
                        browser.find_element_by_xpath('//*[@class="chat-input chat-input-layout needsclick"]').send_keys('#'+str(sequencial)+message3)
                        sequencial+=1

                    print(datetime.now(), '\n', message3, '\n\n', '='*100, '\n\n')
                    time.sleep(1)
                    browser.find_element_by_xpath('//*[@class="chat-controls-button__icon"]').click()
                    contador_mensagem+=1
                    time.sleep(30)

            except:
                pass
        


#Enviar Mensagem
#browser.find_element_by_xpath('//*[@class="chat-input chat-input-layout chat-input_placeholder needsclick"]').send_keys("Hope Hope")
    

inicio()       # Difinição do webBrowser
logarSite()    # Logando no Site 
preparar_chat() # Preparando chat para enviar mensagem


#________________________________________________________________________________________ TELEGRAM__________________________________________________________________________________#



print('################################### AGUARDANDO COMANDOS ###################################')

global canais
global bot
global placar_win
global placar_semGale
global placar_gale1
global placar_gale2
global placar_gale3
global placar_loss
global resultados_sinais
global message1, message2, message3


# PLACAR
#placar_win = 0
#placar_semGale= 0
#placar_gale1= 0
#placar_gale2= 0
#placar_gale3= 0
#placar_loss = 0
#resultados_sinais = placar_win + placar_loss
estrategias = []
placar_estrategia = []
placar_estrategias = []
estrategias_diaria = []
placar_estrategias_diaria = []
contador = 0
botStatus = 0
validador_sinal = 0
parar = 0
dic_estrategia_usuario = {}
lista_seq_minima = []
lista_onde_apostar = []
lista_roletas = []
placar_roletas = []
roletas_diaria = []
placar_roletas_diaria = []
contador_passagem = 0
lista_ids = []
lista_estrategias = []
dicionario_roletas = {}
message1 = None
message2 = None
message3 = None



# LENDO TXT PARA DEFINIR VARIAVEL DE CANAIS E VALIDAÇÃO DE USUÁRIO
txt = open("canais.txt", "r", encoding="utf-8")
arquivo = txt.readlines()
CHAVE_API = arquivo[7].split(' ')[1].split('\n')[0]

ids = arquivo[11].split(' ')[1].split('\n')[0]


bot = telebot.TeleBot(CHAVE_API)


global message



''' FUNÇÕES BOT ''' ##



def generate_buttons_estrategias(bts_names, markup):
    for button in bts_names:
        markup.add(types.KeyboardButton(button))
    return markup





def pausarBot():
    global parar
    global browser

    while True:
        try:
            parar = 1
            return 

        except:
            continue


@bot.message_handler(commands=['⚙🧠 Cadastrar_Mensagem'])
def cadastrarEstrategia(message):
    global contador_passagem

    #Init keyboard markup
    markup_appm = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
    
    markup_appm.add('◀ Voltar')    

    message_chat1 = bot.reply_to(message, "🤖 Ok! Escreva a Mensagem que Será Enviada no CHAT da Roleta ", reply_markup=markup_appm)
    bot.register_next_step_handler(message_chat1, registrar_message1)
    

@bot.message_handler(commands=['📝🧠 Editar_Mensagema'])
def editar_estrategia(message):
    global estrategia
    global estrategias
    global contador_passagem

    try:
    
        #Add to buttons by list with ours generate_buttons function.
        markup_estrategia = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        
        markup_estrategia.add(

                              f'Mensagem1 = {message1}',
                              f'Mensagem2 = {message2}',
                              f'Mensagem3 = {message3}',
                              '◀ Voltar'
                              
                              )


        message_editar_estrategia = bot.reply_to(message, "🤖 Escolha Qual Mensagem Será Editada 👇", reply_markup=markup_estrategia)
        bot.register_next_step_handler(message_editar_estrategia, editar_campo_escolhido)
    
    except:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('✅ Ativar Bot', '⚙ Cadastrar Mensagem', '📝 Editar Mensagem', '📜 Mensagem Cadastrada', '🛑 Pausar Bot')

        message_editar_estrategia = bot.reply_to(message, "🤖 Algo deu Errado. Tente Novamente 🙁.", reply_markup=markup)


@bot.message_handler(commands=['🧠📜 Mensagem_Cadastrada'])
def estrategiasCadastradas(message):
    global estrategia
    global estrategias
    global lista_estrategias

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup = markup.add('✅ Ativar Bot', '⚙ Cadastrar Mensagem', '📝 Editar Mensagem', '📜 Mensagem Cadastrada', '🛑 Pausar Bot')

    try:

        mensagens_cadastrada = 'Mensagem1 = '+ message1 + '\n' + ("="*25) + '\n\n' +\
                                'Mensagem2 = '+ message2 + '\n' + ("="*25) + '\n\n' +\
                                'Mensagem3 = '+ message3 + '\n' + ("="*25) + '\n\n'
                                
        bot.reply_to(message, "🤖 Ok! Mostrando Estratégia Cadastrada.👇", reply_markup=markup)

        bot.send_message(message.chat.id, mensagens_cadastrada)

    except:
        bot.reply_to(message, "🤖 Nenhuma Mensagem cadastrada ❌", reply_markup=markup)


@bot.message_handler(commands=['🛑 Pausar_bot'])
def pausar(message):
    global botStatus
    global contador_passagem
    global browser
    global parar

    if contador_passagem != 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('✅ Ativar Bot', '⚙ Cadastrar Mensagem', '📝 Editar Mensagem', '📜 Mensagem Cadastrada', '🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Estou validando um Sinal. Tente novamente em alguns instanstes.", reply_markup=markup)

    elif botStatus == 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('✅ Ativar Bot', '⚙🧠 Cadastrar Estratégia', '📝🧠 Editar Estratégia', '🧠📜 Estratégia Cadastrada', '🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Bot já está pausado ", reply_markup=markup)

    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('✅ Ativar Bot', '⚙🧠 Cadastrar Estratégia', '📝🧠 Editar Estratégia', '🧠📜 Estratégia Cadastrada', '🛑 Pausar Bot')

        botStatus = 0
        parar = 1
        #pausarBot()

        print('\n\n')
        print('Pausar Bot')
        print('Parando o Bot....\n')

        message_final = bot.reply_to(message, "🤖 Ok! Bot pausado 🛑", reply_markup=markup)

        print('\n\n')
        print('############################################ AGUARDANDO COMANDOS ############################################')
        
        return


@bot.message_handler(commands=['start', 'iniciar', 'começar'])
def start(message):

    if str(message.chat.id) in ids:

        ''' Add id na lista de ids'''
        if str(message.chat.id) not in lista_ids:
            lista_ids.append(message.chat.id)
        else:
            pass
       
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('✅ Ativar Bot', '⚙ Cadastrar Mensagem', '📝 Editar Mensagem', '📜 Mensagem Cadastrada', '🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message, "🤖 Bot Chat Roleta Brasileira! ✅ Escolha uma opção 👇",
                                    reply_markup=markup)
        
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(message_opcoes, opcoes)
    
    else:
        message_error = bot.reply_to(message, "🤖 Você não tem permissão para acessar este Bot ❌🚫")


@bot.message_handler()
def opcoes(message_opcoes):

    if message_opcoes.text in ['✅ Ativar Bot']:
        global botStatus
        global parar
        global reladiarioenviado
        global browser
        global contador_passagem

        print('Ativar Bot')

        try:

            if botStatus == 1:

                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
                markup = markup.add('✅ Ativar Bot', '⚙ Cadastrar Mensagem', '📝 Editar Mensagem', '📜 Mensagem Cadastrada', '🛑 Pausar Bot')

                message_canal = bot.reply_to(message_opcoes, "🤖⛔ Bot já está ativado",
                                    reply_markup=markup)


            elif message1 == '' or message1 == None:
                #Init keyboard markup
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
                markup = markup.add('✅ Ativar Bot', '⚙ Cadastrar Mensagem', '📝 Editar Mensagem', '📜 Mensagem Cadastrada', '🛑 Pausar Bot')

                message_canal = bot.reply_to(message_opcoes, "🤖⛔ Cadastre ou Termine de Cadastrar a Mensagem! ",
                                    reply_markup=markup)

            
            else:
                #Init keyboard markup
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
                markup = markup.add('✅ Ativar Bot', '⚙ Cadastrar Mensagem', '📝 Editar Mensagem', '📜 Mensagem Cadastrada', '🛑 Pausar Bot')

                message_canal = bot.reply_to(message_opcoes, "🤖 Bot Ativado com sucesso! ✅",
                                        reply_markup=markup)
                
                botStatus = 1
                reladiarioenviado = 0
                parar=0
                contador_passagem = 0

                print('#############################  INICIANDO O ENVIO DAS MENSAGENS  #############################')
                print()

                enviar_mensagem() # Analisando os Dados

        except:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            markup = markup.add('✅ Ativar Bot', '⚙ Cadastrar Mensagem', '📝 Editar Mensagem', '📜 Mensagem Cadastrada', '🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖⛔ Cadastre ou Termine de Cadastrar a Estratégia! ",
                                reply_markup=markup)

       

    

    if message_opcoes.text in ['🛑 Pausar Bot']:
        print('Pausar Bot')
        pausar(message_opcoes)

    
    if message_opcoes.text in ['⚙ Cadastrar Mensagem']:
        print('Cadastrar Mensagem')
        cadastrarEstrategia(message_opcoes)


    if message_opcoes.text in ['📜 Mensagem Cadastrada']:
        print('Mensagem Cadastrada')
        estrategiasCadastradas(message_opcoes)


    if message_opcoes.text in ['📝 Editar Mensagem']:
        print('Editar Mensagem')
        editar_estrategia(message_opcoes)




@bot.message_handler()
def registrar_message1(message_chat1):
    global message1

    if message_chat1.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('✅ Ativar Bot', '⚙🧠 Cadastrar Mensagem', '📝🧠 Editar Mensagem', '🧠📜 Mensagem Cadastrada', '🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_chat1, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        return


    else:

        #Init keyboard markup
        markup_mensagem1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

        message1 = message_chat1.text
        print('texo -- >', message1)
    
        markup_mensagem1.add('SIM', 'NÃO')

        pergunta_cadastro = bot.reply_to(message_chat1, "🤖 Ok! Deseja Cadastrar Outra Mensagem?", reply_markup=markup_mensagem1)
        bot.register_next_step_handler(pergunta_cadastro, pergunta)


def registrar_message2(message_chat2):
    global message2

    if message_chat2.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('✅ Ativar Bot', '⚙ Cadastrar Mensagem', '📝 Editar Mensagem', '📜 Mensagem Cadastrada', '🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_chat2, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        return

    else:
        markup_mensagem2 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

        message2 = message_chat2.text
        print('Mensagem2 = ', message2)

        markup_mensagem2.add('SIM', 'NÃO')

        pergunta_cadastro = bot.reply_to(message_chat2, "🤖 Ok! Deseja Cadastrar Outra Mensagem?", reply_markup=markup_mensagem2)
        bot.register_next_step_handler(pergunta_cadastro, pergunta)


def registrar_message3(message_chat3):
    global message3

    if message_chat3.text in ['◀ Voltar']:
        #Init keyboard markup
        markup_cg_ft = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True) 
        markup_cg_ft.add('◀ Voltar')

        message_valor_cg_ht = bot.reply_to(message_chat3, "🤖 Ok! Escreva Novamente a Segunda Mensagem ", reply_markup=markup_cg_ft)
        bot.register_next_step_handler(message_valor_cg_ht, registrar_message2)


    else:
        markup_mensagem3 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup_mensagem3.add('✅ Ativar Bot', '⚙ Cadastrar Mensagem', '📝 Editar Mensagem', '📜 Mensagem Cadastrada', '🛑 Pausar Bot')

        message3 = message_chat3.text
        print('Mensagem3 = ', message3)

        message_final = bot.reply_to(message_chat3, "🤖 Estratégia Cadastrada com Sucesso! ✅", reply_markup=markup_mensagem3)


def editar_campo_escolhido(message_editar_estrategia):
    global resposta_usuario

    if message_editar_estrategia.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('✅ Ativar Bot', '⚙ Cadastrar Mensagem', '📝 Editar Mensagem', '📜 Mensagem Cadastrada', '🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_editar_estrategia, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        
        return
    

    else:
        resposta_usuario = message_editar_estrategia.text.split(' = ')

        #Init keyboard markup
        markup_novo_valor = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup_novo_valor.add('◀ Voltar')

        message_novo_valor = bot.reply_to(message_editar_estrategia, "🤖 Ok! Agora, Insira a Nova Mensagem ", reply_markup=markup_novo_valor)
        bot.register_next_step_handler(message_novo_valor, gravar_novo_valor)


def gravar_novo_valor(message_novo_valor):
    global message1, message2, message3

    if message_novo_valor.text in ['◀ Voltar']:
        #Add to buttons by list with ours generate_buttons function.
        markup_estrategia = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup_estrategia.add(

                              f'Mensagem1 = {message1}',
                              f'Mensagem2 = {message2}',
                              f'Mensagem3 = {message3}',
                              '◀ Voltar'
                              
                              )

        message_editar_estrategia = bot.reply_to(message, "🤖 Escolha Qual Mensagem Será Editada 👇", reply_markup=markup_estrategia)
        bot.register_next_step_handler(message_editar_estrategia, editar_campo_escolhido)



    if resposta_usuario[0] == 'Mensagem1':
        if message_novo_valor.text == 'Vazio' or message_novo_valor.text == 'vazio': message1 = None 
        else: message1 = message_novo_valor.text
    
    if resposta_usuario[0] == 'Mensagem2':
        if message_novo_valor.text == 'Vazio' or message_novo_valor.text == 'vazio': message2 = None 
        else: message2 = message_novo_valor.text
    

    if resposta_usuario[0] == 'Mensagem3':
        if message_novo_valor.text == 'Vazio' or message_novo_valor.text == 'vazio': message3 = None 
        else: message3 = message_novo_valor.text
    
    

    #Init keyboard markup
    markup_estrategia = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup_estrategia.add(

                              f'Mensagem1 = {message1}',
                              f'Mensagem2 = {message2}',
                              f'Mensagem3 = {message3}',
                              '◀ Voltar'
                              
                              )

    message_editar_estrategia = bot.reply_to(message_novo_valor, "🤖 Mensagem Editada com sucesso! ✅", reply_markup=markup_estrategia)
    bot.register_next_step_handler(message_editar_estrategia, editar_campo_escolhido)


def pergunta(resposta):
    global message1, message2, message3

    if resposta.text == 'SIM' and message2 == None:
        
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True) 
        markup.add('◀ Voltar')

        message_chat2 = bot.reply_to(resposta, "🤖 Boa! Então Escreva a Proxima Mensagem", reply_markup=markup)
        bot.register_next_step_handler(message_chat2, registrar_message2)
    
    elif resposta.text == 'SIM' and message2 != None:

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True) 
        markup.add('◀ Voltar')

        message_chat3 = bot.reply_to(resposta, "🤖 Boa! Então Escreva a Proxima Mensagem", reply_markup=markup)
        bot.register_next_step_handler(message_chat3, registrar_message3)
    

    else:

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('✅ Ativar Bot', '⚙ Cadastrar Mensagem', '📝 Editar Mensagem', '📜 Mensagem Cadastrada', '🛑 Pausar Bot')

        message_final = bot.reply_to(resposta, "🤖 Estratégia Cadastrada com Sucesso! ✅", reply_markup=markup)




bot.infinity_polling()