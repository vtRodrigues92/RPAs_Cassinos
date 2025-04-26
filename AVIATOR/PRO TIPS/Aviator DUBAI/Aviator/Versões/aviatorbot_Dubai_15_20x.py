from webbrowser import BaseBrowser
from selenium import webdriver
import time
import warnings
from webdriver_manager.chrome import ChromeDriverManager
import logging
from datetime import datetime
from selenium.webdriver.support.color import Color
import pandas as pd
from columnar import columnar
import telebot
from telegram.ext import * 
from telebot import types
import sys
import os
import mysql.connector
from mysql.connector import Error


#_______________________________________________________________________#____________________________________________________________________________________________________

print()
print('                                #################################################################')
print('                                ######## TECNOLOGIA DUBAI - BOT DE SINAIS PARA O AVIATOR ########')
print('                                #################################################################')
print('                                ##################### SEJA BEM VINDO ############################')
print('                                #################################################################')
print('                                ############# DESENVOLVIDO POR VICTOR RODRIGUES #################')
print('                                #################################################################\n')
print('Versão = 0.0.2')
print('Ambiente: Produção\n\n\n')


# Definindo opções para o browser
warnings.filterwarnings("ignore", category=DeprecationWarning) 
chrome_options = webdriver.ChromeOptions() 
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("window-size=1037,547")
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_experimental_option('useAutomationExtension', False)
#chrome_options.add_argument("--incognito") #abrir chrome no modo anônimo
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
#chrome_options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"


#logger = logging.getLogger()


# CORES
roxo = '#6b07d2'
azul = '#005d91'
rosa =  '#900087'


# DATA FRAME
df = pd.DataFrame(columns = ['data','horario','hora','minuto','vela','cor','capturado' ])

# CAPTURANDO CAMPOS
def campos():
    global data_atual
    global horario_atual
    global hora
    global minuto
    global capturado

    data_atual = datetime.today().strftime('%Y-%m-%d')
    horario_atual = datetime.today().strftime('%H:%M')
    hora = horario_atual[0:2]
    minuto = horario_atual[3:]
    capturado = 1
    return data_atual, horario_atual, hora, minuto, capturado


#usuario: Fordbracom22
#senha : Fordbracom2022

def inicio():

    global browser
    global parar

    parar = 0

    time.sleep(1)
    print()
    print('O Programa está sendo iniciado......')

    browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)   
    print('\n\n')

    logger = logging.getLogger()
    browser.get(r"https://sgame-aviator.gamecontentprovider.com/?user=37505&token=ce2042c6-4415-4d7e-8941-0c61e751e8d5&lang=en&currency=BRL&return_url=&operator=1627")
    browser.maximize_window()
    time.sleep(10)


    print('######################### INICIANDO ANÁLISE DOS DADOS #########################')
    print()




# RASPAGEM DOS DADOS
def raspagem():

    global parar
    global browser
    global message
    global placar_win
    global placar_loss

    parar=0

    sticker_alerta = 'CAACAgEAAxkBAAEWqhti6eEyOdo2d55acAMYWfSdTDiVRgACFQMAAqawUUc81K68DzAeBikE'
    sticker_win = 'CAACAgEAAxkBAAEWqh5i6eFbKJdN91c_cGJLk4d4xpwrIQACOQMAAnoIUEdpWNtAT7_NaCkE'

    global vela
    global cor
    global df
    global placar_win
    global placar_loss
    global placar
    
    contagem_cor = []
    contagem_vela = []


    while True:

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass


        try:
            flew_away = browser.find_element_by_xpath('/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[2]/app-play-board/div/div[2]/app-dom-container/div/div/div[1]').text.split('\n')
            
            if flew_away[0] == 'FLEW AWAY!':
                time.sleep(3)
                vela = browser.find_element_by_xpath('/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]/div/app-payout-item[1]/div').text
                str_cor =  Color.from_string(browser.find_element_by_xpath('/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]/div/app-payout-item[1]/div').value_of_css_property('background-color')).hex

                
                if str_cor == roxo:
                    cor = 'roxo'
                    contagem_cor.append(cor)
                    contagem_vela.append(vela)
                    print(cor, vela)
                    print(contagem_cor)


                    if contagem_cor.count('roxo') == 1 and len(contagem_cor) != 1:
                        try:

                            if canal_free !='':
                                bot.delete_message(canal_free, alerta.message_id)
                            
                            if canal_vip !='':
                                bot.delete_message(canal_vip, alerta.message_id)
                    
                        except:
                            pass
                        contagem_cor = []
                        contagem_cor.append(cor)


                    if contagem_cor.count('roxo') == 1 and len(contagem_cor) == 1:
                        
                        print('ENVIANDO ALERTA')
                        alerta = bot.send_sticker(canal_free, sticker=sticker_alerta)
                        print('==================================================')

                        continue


                    if contagem_cor.count('roxo') == 2 and len(contagem_cor) == 2:
                        print('ENVIANDO SINAL TELEGRAM')

                        headers = [' 🤖 ENTRADA CONFIRMADA 🛫📡                                                    ']

                        data = [
                            ['⏰ ENTRAR APÓS O RESULTADO '+ vela ],
                            ['🏃‍♂️ SAIR NO 2.0x'],
                            ['🔰 FAZER ATÉ 3 RECUPERAÇÕES'],
                            ["🌐 <a href='https://forra.bet/sports/play-casino2?gameid=6109'>Acessar o site do Aviator</a>"]
                        ]
                        
                        table = columnar(data, headers, no_borders=True)

                        try:

                            if canal_free != '': 
                                message_canal_free = bot.send_message(canal_free,table, parse_mode='HTML', disable_web_page_preview=True)

                            if canal_vip !='':
                                message_canal_vip = bot.send_message(canal_vip,table, parse_mode='HTML', disable_web_page_preview=True)

                        except:
                            pass


                        print('==================================================')
                        time.sleep(3)
                        break
                    else:
                        try:

                            if canal_free !='':
                                bot.delete_message(canal_free, alerta.message_id)
                        
                            if canal_vip !='':
                                bot.delete_message(canal_vip, alerta.message_id)
                    
                        except:
                            pass

                    contagem_cor = []
                    time.sleep(3)
                    continue


                if str_cor == azul:
                    cor = 'azul'
                    contagem_cor.append(cor)
                    contagem_vela.append(vela)
                    print(cor, vela)
                    print(contagem_cor)
                    
                    if contagem_cor.count('azul') == 1 and len(contagem_cor) != 1:
                        try:

                            if canal_free !='':
                                bot.delete_message(canal_free, alerta.message_id)
                        
                            if canal_vip !='':
                                bot.delete_message(canal_vip, alerta.message_id)
                    
                        except:
                            pass
                        contagem_cor = []
                        contagem_cor.append(cor)

                    if contagem_cor.count('azul') == 2 and len(contagem_cor) == 2:
                        print('ENVIANDO ALERTA')
                        alerta = bot.send_sticker(canal_free, sticker=sticker_alerta)
                        print('==================================================')

                        continue


                    if contagem_cor.count('azul') == 3 and len(contagem_cor) == 3:
                        print('ENVIANDO SINAL TELEGRAM')

                        headers = [' 🤖 ENTRADA CONFIRMADA 🛫📡                                                    ']

                        data = [
                            ['⏰ ENTRAR APÓS O RESULTADO '+ vela ],
                            ['🏃‍♂️ SAIR NO 1.50x'],
                            ['🔰 FAZER ATÉ 3 RECUPERAÇÕES'],
                            ["🌐 <a href='https://forra.bet/sports/play-casino2?gameid=6109'>Acessar o site do Aviator</a>"]
                        ]
                        
                        table = columnar(data, headers, no_borders=True)

                        try:

                            if canal_free != '': 
                                message_canal_free = bot.send_message(canal_free,table, parse_mode='HTML', disable_web_page_preview=True)

                            if canal_vip !='':
                                message_canal_vip = bot.send_message(canal_vip,table, parse_mode='HTML', disable_web_page_preview=True)

                        except:
                            pass


                        print('==================================================')
                        time.sleep(3)
                        break
                    else:
                        print('==================================================')
                        time.sleep(3)
                        continue
                
                else:
                    try:

                        if canal_free !='':
                            bot.delete_message(canal_free, alerta.message_id)
                        
                        if canal_vip !='':
                            bot.delete_message(canal_vip, alerta.message_id)
                    
                    except:
                        pass

                    contagem_cor = []
                    time.sleep(3)
                    continue

        except:
            continue


    # Rodada após o envio do sinal Telegram
    contador = 0
    
    while contador <= 3:

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass


        try:
            flew_away = browser.find_element_by_xpath('/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[2]/app-play-board/div/div[2]/app-dom-container/div/div').text.split('\n')
            
            if flew_away[0] == 'FLEW AWAY!':
                time.sleep(3)
                vela = browser.find_element_by_xpath('/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]/div/app-payout-item[1]/div').text
                str_cor_r =  Color.from_string(browser.find_element_by_xpath('/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]/div/app-payout-item[1]/div').value_of_css_property('background-color')).hex
                vela = vela.strip('x')                                      

                if str_cor == azul and float(vela) >=1.5 or str_cor == roxo and float(vela) >= 2.0:
                    print('WINNNN')
                    placar_win +=1
                    resultados_sinais = placar_win + placar_loss
                    print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
                    bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN "+str(placar_win)+"\n😭 LOSS "+str(placar_loss)+"\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                    try:
                        if canal_free != '':
                            bot.edit_message_text(table +"  \n============================== \n              WINNNN ✅ --- 🎯 "+ vela+"x", message_canal_free.sender_chat.id, message_canal_free.message_id, parse_mode='HTML', disable_web_page_preview=True)   
                            bot.send_sticker(canal_free, sticker=sticker_win)

                        if canal_vip != '':
                            bot.edit_message_text(table +"  \n============================== \n              WINNNN ✅ --- 🎯 "+ vela+"x", message_canal_vip.sender_chat.id, message_canal_vip.message_id, parse_mode='HTML', disable_web_page_preview=True)   
                            bot.send_sticker(canal_vip, sticker=sticker_win)

                    except:
                        pass

                    print('==================================================')
                    break
                
                else:
                    print('LOSSS')
                    print('==================================================')
                    contador+=1
                    continue
            else:
                continue
        
        except:
            continue
    
    if contador == 4:
        print('LOSSS GALE3')
        placar_loss +=1
        resultados_sinais = placar_win + placar_loss
        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
        bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN "+str(placar_win)+"\n😭 LOSS "+str(placar_loss)+"\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

        try:
            
            if canal_free !='':
                bot.edit_message_text(table +"\n============================== \n              LOSS ✖", message_canal_free.sender_chat.id, message_canal_free.message_id, parse_mode='HTML', disable_web_page_preview=True)

            if canal_vip !='':
                bot.edit_message_text(table +"\n============================== \n              LOSS ✖", message_canal_vip.sender_chat.id, message_canal_vip.message_id, parse_mode='HTML', disable_web_page_preview=True)
        
        except:
            pass

        print('==================================================')

    raspagem()








#________________________________________________________________________________________ TELEGRAM__________________________________________________________________________________#


print('###################### AGUARDANDO COMANDOS ######################')

global canal

CHAVE_API ='5585661404:AAGGmNWC1RC3tsEU9cCMvkiI-A6EDSvtH_4'                 # teste-->'1929964993:AAFe7Qqu4jQFLnyOxau8PLGo7Q-Yu2kAQHs'   # oficial --> 5434022871:AAF-mMhUcDuEID9vf-8WnLvZiFPUnjuzk-k
#canal = -1001614937782           #OPL - -1001569116756     #, '-1001775325949']   #1609828054    TESTE #1775325949 #OFICIAL -1001711794178
bot = telebot.TeleBot(CHAVE_API)


# PLACAR
placar_win = 0
placar_loss = 0
resultados_sinais = placar_win + placar_loss



# LENDO TXT PARA DEFINIR VARIAVEL FREE E VIP E VALIDAÇÃO DE USUÁRIO
txt = open("canais.txt", "r")
free = txt.readlines(1)
vip = txt.readlines(2)
ids = txt.readlines(3)

for canal in free:
    free = canal.split(' ')
    free = int(free[1])
    

for canal in vip:
    vip=canal.split(' ')
    vip = int(vip[1])


for id in ids:
    id_usuario = id.split(' ')
    id_usuario = id_usuario[1]


######################################################


global message


def restart_program():
     while True:
        try:
            global parar
            global browser
            parar = 1
            browser.close()
            time.sleep(1)
            break
        except:
            continue



def generate_buttons(bts_names, markup):
    for button in bts_names:
        markup.add(types.KeyboardButton(button))
    return markup



@bot.message_handler(commands=['stop'])
def parar(message):
    if str(message.chat.id) in id_usuario:
        message_final = bot.reply_to(message, "🤖 Ok! Bot parado ❌")
        print('\n\n')
        print('Comando: Parar BOT')
        print('Parando o BOT....\n')
        restart_program()

        print('###################### AGUARDANDO COMANDOS ######################')

    else:
        message_error = bot.reply_to(message, "🤖 Você não tem permissão para acessar este Bot ❌🚫")



@bot.message_handler(commands=['start'])
def start(message):

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(row_width=2)

    #Add to buttons by list with ours generate_buttons function.
    markup = generate_buttons(['/start','Enviar sinais Canal FREE','Enviar sinais Canal VIP','Enviar sinais Canal FREE & VIP','/stop'], markup)
    message = bot.reply_to(message, "🤖 Bot Aviator Iniciado! ✅ Escolha uma opção 👇",
                            reply_markup=markup)
    
    #Here we assign the next handler function and pass in our response from the user. 
    #bot.register_next_step_handler(message, opcoes(message))





@bot.message_handler(content_types=['text'])
def opcoes(message):

    global canal_free
    global canal_vip

    global placar

    if message.text in ['Enviar sinais Canal FREE']:
        bot.send_message(message.chat.id, "🤖 Ok! Enviando sinais no Canal FREE ✅")
        
        print("Iniciar e enviar sinais no Canal FREE ")

        canal_free = free
        canal_vip = ''

        placar = bot.send_message(message.chat.id,"📊 Placar Atual:\n==================\n😍 WIN "+str(placar_win)+"\n😭 LOSS "+str(placar_loss)+"\n🎯 Assertividade 0%")

        inicio()
        raspagem()
    

    if message.text in ['Enviar sinais Canal VIP']:
        bot.send_message(message.chat.id, "🤖 Ok! Enviando sinais no Canal VIP ✅")
        
        print("Iniciar e enviar sinais no Canal VIP ")

        canal_free = ''
        canal_vip = vip

        placar = bot.send_message(message.chat.id,"📊 Placar Atual:\n==================\n😍 WIN "+str(placar_win)+"\n😭 LOSS "+str(placar_loss)+"\n🎯 Assertividade 0%")

        inicio()
        raspagem()


    if message.text in ['Enviar sinais Canal FREE & VIP']:
        bot.send_message(message.chat.id, "🤖 Ok! Enviando sinais no Canal FREE & VIP ✅")
        
        print("Iniciar e enviar sinais no Canal FREE & VIP ")

        canal_free = free
        canal_vip = vip

        placar = bot.send_message(message.chat.id,"📊 Placar Atual:\n==================\n😍 WIN "+str(placar_win)+"\n😭 LOSS "+str(placar_loss)+"\n🎯 Assertividade 0%")

        inicio()
        raspagem()







bot.infinity_polling()
