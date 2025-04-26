import datetime as dt
import random
from telegram.ext import *
from telebot import *
import ast

# Função para validar horario do envio de sinais pagantes
def validar_horario_envio():
    global reladiarioenviado
    
    # Obter a hora atual
    agora = dt.datetime.now()

    # Definir os horários das listas de sinais
    horarios = [
        (dt.time(12, 0), dt.time(14, 0), "Lista de sinais da manhã:"),
        (dt.time(18, 0), dt.time(20, 0), "Lista de sinais da tarde:"),
        (dt.time(24, 00), dt.time(2, 0), "Lista de sinais da noite:")
    ]

    # Enviar as listas de sinais de acordo com o horário atual
    for inicio, fim, mensagem in horarios:
        if inicio.strftime('%H:%M') == agora.time().strftime('%H:%M') < fim.strftime('%H:%M') and reladiarioenviado == 0:
            # Gerar horários aleatórios dentro do intervalo
            sinais = []
            while len(sinais) < 6:  # Gerar 6 horários aleatórios
                hora_aleatoria = random.randint(inicio.hour, fim.hour - 1)
                minuto_aleatorio = random.randint(0, 59)
                horario_aleatorio = dt.time(hora_aleatoria, minuto_aleatorio)
                if inicio <= horario_aleatorio < fim:  # Verificar se o horário está dentro do intervalo
                    sinais.append(horario_aleatorio)
            sinais.sort()  # Ordenar os horários
            sinais_formatados = "\n".join([f"⏰{horario.hour:02}:{horario.minute:02}" for horario in sinais])
            
            # Formatando mensagem #
            texto_formatado = "🎁🚩 Horário Pagante 🚩🎁\n\n"
            texto_formatado += "Já deixem tudo certo ⚠️\n\n"
            texto_formatado += "💫PLATAFORMA / CRIAR CONTA (https://go.aff.7k-partners.com/zx2zk80x) 💫\n\n"
            texto_formatado += f'{sinais_formatados}\n\n'
            texto_formatado += "\n🟢FORTUNE DRAGON 👁\n🟢FORTUNE TINGER🐯\n🟢FORTUNE MOUSE FORTUNE MOUSE🐭\n🟢FORTUNE MOUSE FORTUNE OX 🐂\n🟢FORTUNE MOUSE FORTUNE RABITT 🐇\n\n"
            texto_formatado += "➡️HORÁRIOS MUITO ASSERTIVOS POR ISSO TEM POUCOS!🚩\n➡️USE O GERENCIAMENTO DE BANCA✅\n➡️ASSERTIVIDADE DE 🟠🟠🟠\n➡️AQUECE 1 MINUTO ANTES🔥\n➡️GANHOU PAROU❌"

            enviar_horarios_telegram(texto_formatado)

            reladiarioenviado +=1
            #update.message.reply_text(f"{mensagem}\n{sinais_formatados}")
            break


        if agora.time().strftime('%H:%M') > inicio.strftime('%H:%M') < fim.strftime('%H:%M') and reladiarioenviado == 1:
            reladiarioenviado = 0
            

# Enviar Mensagem Telegram
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



if __name__ == '__main__':

    print('                                #################################################################')
    print('                                ###################   BOT HORARIOS #2  ##########################')
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

    #print( f"Bot Ativado as {datetime.today()}")
    while True:
        validar_horario_envio()
        time.sleep(3)