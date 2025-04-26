import random
from datetime import datetime, timedelta
from telegram.ext import *
from telebot import *
import ast


def gerar_horarios_aleatorios():
    # Lista para armazenar os horários gerados
    horarios = []
    
    # Gerar horários aleatórios
    for _ in range(5):
        horario_inicial = datetime.strptime('09:00', '%H:%M')
        horario_final = datetime.strptime('23:00', '%H:%M')
        horario_1 = horario_inicial + timedelta(minutes=random.randint(0, (horario_final - horario_inicial).seconds // 60))
        horario_2 = horario_1 + timedelta(minutes=random.randint(1, 60))
        
        horarios.append((horario_1.strftime('%H:%M'), horario_2.strftime('%H:%M')))

        horarios = sorted(horarios)
    
    return horarios


def formatar_horarios(horarios):
    texto_formatado = "🎁🚩 Horário Pagante 🚩🎁\n\n"
    
    for horario in horarios:
        texto_formatado += f"⏰{horario[0]:<10}⏰{horario[1]}\n"
    
    texto_formatado += "\n🟢FORTUNE DRAGON 👁\n🟢FORTUNE TINGER🐯\n🟢FORTUNE MOUSE FORTUNE MOUSE🐭\n🟢FORTUNE MOUSE FORTUNE OX 🐂\n🟢FORTUNE MOUSE FORTUNE RABITT 🐇\n\n"
    texto_formatado += "➡️HORÁRIOS MUITO ASSERTIVOS POR ISSO TEM POUCOS!🚩\n➡️USE O GERENCIAMENTO DE BANCA✅\n➡️ASSERTIVIDADE DE 🟠🟠🟠\n➡️AQUECE 1 MINUTO ANTES🔥\n➡️GANHOU PAROU❌"
    
    return texto_formatado


def enviar_horarios_telegram(texto):
    global contador_passagem

    '''Lendo o arquivo txt canais '''
    txt = open("chats.txt", "r", encoding="utf-8")
    arquivo = txt.read()
    canais = ast.literal_eval(arquivo) # Convertendo string em dicionario 

    # Enviando Mensagem Telegram
    horario_inicial = datetime.now()
    
    try:
        for key, value in canais.items():
            try:
               
                globals()[f'alerta_{key}'] = bot.send_message(key, texto, parse_mode='HTML', disable_web_page_preview=True)
                
                time.sleep(0.2)

            except:
                print('NÃO CONSEGUI ENVIAR A MENSAGEM PARA O CANAL', key)

    except:
        pass

    print('MENSAGEM ENVIADA PARA TODOS OS CANAIS EM ---> ', datetime.now() - horario_inicial)



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
    if horario_atual == '08:00' and reladiarioenviado == 0:

        # Gerar horários aleatórios
        horarios_aleatorios = gerar_horarios_aleatorios()

        # Formatar os horários
        texto_formatado = formatar_horarios(horarios_aleatorios)

        # Envia texto para o Telegram
        enviar_horarios_telegram(texto_formatado)

        reladiarioenviado +=1

    # Condição que zera o placar quando o dia muda
    if horario_atual == '08:01' and reladiarioenviado == 1:
        reladiarioenviado = 0







if __name__=='__main__':

    print('                                #################################################################')
    print('                                ###################     BOT HORARIOS     #########################')
    print('                                #################################################################')
    print('                                ##################### SEJA BEM VINDO ############################')
    print('                                #################################################################')
    print('                                ############# DESENVOLVIDO POR VICTOR RODRIGUES #################')
    print('                                #################################################################\n')
    print('Versão = 2.0.0')
    print('Ambiente: Produção\n\n\n')

    # LENDO TXT PARA DEFINIR VARIAVEL DE CANAIS E VALIDAÇÃO DE USUÁRIO
    CHAVE_API = open("token_bot_telegram.txt", "r", encoding="utf-8").read()
    
    bot = telebot.TeleBot(CHAVE_API)

    reladiarioenviado = 0

    print( f"Bot Ativado as {datetime.today()}")

    while True:
        try:
            validaData()
            time.sleep(10)
        except Exception as e:
            print(e)

    
    
    