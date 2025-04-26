from selenium import webdriver
import time
import warnings
#from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import telebot
from telegram.ext import *
from telebot import *
import ast
import os
import requests, json
from websocket import create_connection


print()
print('                                #################################################################')
print('                                ################         BOT JETX        ########################')
print('                                #################################################################')
print('                                ##################### SEJA BEM VINDO ############################')
print('                                #################################################################')
print('                                ############# DESENVOLVIDO POR VICTOR RODRIGUES #################')
print('                                #################################################################\n')
print('Versão = 1.0.0')
print('Ambiente: Produção\n\n\n')



def pegar_evosessionid():
    #LOGIN
    URL = 'https://api.nexus-casino.io/auth/login'

    header = {
    'Content-Type': 'application/json',
    "Origin":"https://diskbets.com",
    "Referer":"https://diskbets.com/",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    payload = '{"email":"master_jetx11@gmail.com","password":"Fordbracom","redirect":false,"tenant":"65df634597fd946e4fb62c75"}'
    
    response = requests.post(URL, headers=header, data=payload)
    
    token_autorizacao = response.json()['token']

    print('Token Autorização - '+ token_autorizacao)
    
    #### ENTRANDO NO GAME

    #REQUISIÇÃO1
    URL = 'https://api.nexus-casino.io/games/play'

    payload = {"slug":"jetx","slugProvider":"smartsoft","currency":"BRL","deviceType":"desktop"}

    header = {
        "Accept":"application/json, text/javascript, */*; q=0.01",
        "Authorization":token_autorizacao,
        "Origin":"https://diskbets.com",
        "Referer":"https://diskbets.com/",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
            }
    
    response = requests.post(URL, data=payload, headers=header)

    url_1 = json.loads(response.content)['url']

    print(url_1)

    #REQUISIÇÃO2

    headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Referer":"https://diskbets.com/",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }

    response = requests.get(url_1, headers=headers, allow_redirects=False)

    url_2 = response.headers.get('location')

    print(url_2)

    #REQUISIÇÃO3

    response = requests.get(url_2)

    url_3 = response.text.split('RedirectUrl(')[2].split(')//]]')[0].replace("'",'')

    print(url_3)

    headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Referer":"https://diskbets.com/",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }

    response = requests.get(url_3, headers=headers, allow_redirects=False)

    token = response.headers.get('location').split('aspx?Token=')[1]

    print(token)

    return token

    #'[{"f":true' -- Websocket



def conectar_websocket(token):
    global URL
    global ws
    global cont
    global ultimo_result
    global ultimo_valor_armazenado


    header = {
      
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "no-cache",
    "Connection": "Upgrade",
    "Host": "eu-server-w4.ssgportal.com",
    "Origin": "https://eu-server-w4.ssgportal.com",
    "Pragma": "no-cache",
    "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
    "Sec-WebSocket-Key": "YsGPbXggRuETc8BUnIuKxA==",
    "Sec-WebSocket-Version": "13",
    "Upgrade": "websocket",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"

    }

   
    #f'wss://wac.evo-games.com/public/topcard/player/game/TopCard000000001/socket?messageFormat=json&instance=409uj-qo2wix3z5rclnkzu-nvrpqglt6teqkvaf&tableConfig=nvrpqglt6teqkvaf&EVOSESSIONID={evosessionid}&client_version=6.20230323.70223.23049-6a8fb42f8b'
    #URL=f'wss://belloatech.evo-games.com/public/topcard/player/game/TopCard000000001/socket?messageFormat=json&instance=o6q2h6-rhjuf7mokioplhho-TopCard000000001&tableConfig=&EVOSESSIONID={evosessionid}&client_version=6.20230823.71249.29885-78ea79aff8'
    #URL=f'wss://eu-server-w99.ssgportal.com/JetX/signalr/connect?transport=webSockets&clientProtocol=1.5&token={token}&group=JetX&connectionToken=lJBSUbb2v7WEha0PE9xt4p7IZWgQY0CoWGIUh7NHAgP%2FNdZ%2FDsVD0ELE1PioR4FhilXb8%2FResKhlG%2BjOLxHTMg%2BT22veVgk0bM1S6rVydJteUIDxzdARM%2FLMwgpxWhFz&connectionData=%5B%7B%22name%22%3A%22h%22%7D%5D&tid=10'

    URL=f'wss://eu-server-w4.ssgportal.com/JetXNode700/signalr/connect?transport=webSockets&clientProtocol=1.5&token={token}8&group=JetX&connectionToken=D75sNKFZ1YeKwk7dyF8E9Dhid2ZAdstbzWmzIWxCvYpUsYRfmnVZw%2FFDTItmLxjmm5cgm5Xckehit4zeovY5eV03qsR9cxDdM3eWhLNh2yj5bsMV9FzFW92SVqVFVzsb&connectionData=%5B%7B%22name%22%3A%22h%22%7D%5D&tid=7'
    
    ws = create_connection(URL, verify = False)

    ws.send(json.dumps([json.dumps(header)]))

    cont = 0
    ultimo_result = ''
    ultimo_valor_armazenado = ''



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



# ENVIA PLACAR CANAIS TELEGRAM
def envia_placar():

    try:
        placar()

        ''' Lendo o arquivo txt canais '''
        txt = open("canais.txt", "r", encoding="utf-8")
        arquivo = txt.readlines()
        canais = arquivo[12].replace('canais= ','').replace('\n','')
        canais = ast.literal_eval(canais) # Convertendo string em dicionario 

        ''' Enviando mensagem Telegram '''
        try:
            for key, value in canais.items():
                try:
                    globals()[f'placar_{key}'] = bot.send_message(key,\
        "📊 Placar Atual do dia "+data_hoje+":\n\
        =====================\n\
        😍 WIN - "+str(placar_win)+"\n\
        🏆 WIN S/ GALE - "+str(placar_semGale)+"\n\
        🥇 WIN GALE1 - "+str(placar_gale1)+"\n\
        🥈 WIN GALE2 - "+str(placar_gale2)+"\n\
        😭 LOSS - "+str(placar_loss)+"\n\
        =====================\n\
        🎯 Assertividade "+ asserividade)
        #Variavel Dinâmica
                except:
                    pass

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

    if horario_atual == '11:55' and reladiarioenviado == 0 or horario_atual == '23:55' and reladiarioenviado == 0:
        envia_placar()
        reladiarioenviado +=1

    
    if horario_atual == '11:56' and reladiarioenviado == 1 or horario_atual == '23:56' and reladiarioenviado == 1:
        reladiarioenviado = 0

    # Condição que zera o placar quando o dia muda
    if horario_atual == '00:00' and reladiarioenviado == 0:
        placar()
        reladiarioenviado +=1

    # Condição que zera o placar quando o dia muda
    if horario_atual == '00:01' and reladiarioenviado == 1:
        reladiarioenviado = 0

    
def inicio():
    global horario_inicio
    global seq_green
    global lista_resultados

    lista_resultados = []
    horario_inicio = datetime.now()
    seq_green = 0
    

def validador_estrategia(estrategia, lista_resultados, sequencia_minima):
    # Validando se o resultado se encaixa na estratégia ( TRUE ou FALSE )
    validador = []
    try:
        for e in enumerate(estrategia[:-2]): 
            for v in enumerate(lista_resultados[int(-sequencia_minima):]):

                while v[0] == e[0]:
                    if '+' in e[1]:
                        if float(v[1]) > float(e[1][1:]):
                            validador.append(True)
                            break
                        else:
                            validador.append(False)
                            break

                        
                    if '-' in e[1]:
                        if float(v[1]) < float(e[1][1:]):
                            validador.append(True)
                            break
                        else:
                            validador.append(False)
                            break


                    else:
                        print('ERRO NA ESTRATÉGIA ', estrategia,'...VERIFIQUE O CADASTRO DA MESMA.')
                        time.sleep(3)
                        break

        print(f'Validador  --> {validador}')
        return validador
    except:
        pass


def coletarDados():

    global token

    token = pegar_evosessionid()

    while True:

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass
        
        # Validando o horario para envio do relatório diário
        validaData()


        try:
            # Validando se foi solicitado o stop do BOT
            if parar != 0:
                break
            else:
                pass
            
            # Validando o horario para envio do relatório diário
            validaData()

            # Pegando o histórico de resultados
            try:

                conectar_websocket(token)

                while True:
                    
                    ultimo_result = ws.recv()

                    if '[{"f":true' in ultimo_result:

                        resultado_atual = json.loads(ultimo_result)['M'][0]['A'][0]['v']

                        lista_resultados.append(resultado_atual)
                        
                        print(datetime.now().strftime('%H:%M'))

                        ''' Chama a função que valida a estratégia para enviar o sinal Telegram '''
                        validarEstrategia(lista_resultados, estrategias)

                        #Separador
                        print('=' * 100)
                
        
                    ultimo_valor_armazenado = ultimo_result  
                                        
                
            except Exception as e:
                print(e)
                token = pegar_evosessionid()
                continue
                

        except Exception as e:
            print(e)
            print('ERRO NO PRIMEIRO TRY DA FUNÇÃO PEGAR DADOS')
            

def validarEstrategia(lista_resultados, estrategias):
    
    global cash_out
    global gale
    global vela_atual
    global response
    global estrategia

    try:
        for estrategia in estrategias:

            # Validando se foi solicitado o stop do BOT
            if parar != 0:
                break
            else:
                pass


            # Validando o horario para envio do relatório diário
            validaData()

            print ('Analisando a Estrategia --> ', estrategia)
            sequencia_minima_alerta = len(estrategia[:-3])
            sequencia_minima_sinal = len(estrategia[:-2])
            cash_out = estrategia[-2]
            gale = estrategia[-1]
            print('Historico_Velas --> ', lista_resultados)

            ''' VALIDADOR DE ESTRATEGIA '''
            validador = validador_estrategia(estrategia, lista_resultados, sequencia_minima_alerta)

            ''' Validando se bateu alguma condição'''
            if validador.count(True) == int(sequencia_minima_alerta):
                print('ENVIANDO ALERTA')
                enviarAlertaTelegram()
                

                ''' Verifica se a ultima condição bate com a estratégia para enviar sinal Telegram '''
                while True:
                    
                    try:

                        # Pegando o histórico de resultados
                        ultimo_result = ws.recv()

                        if '[{"f":true' in ultimo_result:

                            resultado_atual = json.loads(ultimo_result)['M'][0]['A'][0]['v']

                            lista_resultados.append(resultado_atual)
                            
                        else:
                            continue
                    
                        ''' VALIDANDO SE TEM DADO VAZIO NA LISTA'''
                        if '' in lista_resultados:
                            continue

                
                        validador = validador_estrategia(estrategia, lista_resultados, sequencia_minima_sinal)

                        if validador.count(True) == int(sequencia_minima_sinal):
                            print(lista_resultados[-1])
                            print('ENVIA SINAL TELEGRAM')
                            vela_atual = lista_resultados[-1]
                            enviarSinalTelegram()
                            checkSinalEnviado(lista_resultados)
                            time.sleep(1)
                            break


                        else:
                            print('APAGA SINAL DE ALERTA')
                            apagaAlertaTelegram()
                            break

                    except:
                       continue
            
            else:
                print('=' * 150)


    except:
        pass


def enviarAlertaTelegram():
    global contador_passagem

    ''' Lendo o arquivo txt canais '''
    txt = open(r"arquivos_txt\canais.txt", "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[7].replace('canais= ','').replace('\n','')
    canais = ast.literal_eval(canais) # Convertendo string em dicionario 

    ''' Lendo o arquivo txt '''
    with open('arquivos_txt/alerta.txt',"r", encoding="utf-8") as arquivo:
        message_alerta = arquivo.read()


    ''' Enviando mensagem Telegram '''
    try:
        for key,value in canais.items():
            try:
                
                ''' Mensagem '''
                globals()[f'alerta_{key}'] = bot.send_message(key, message_alerta
                                                                    .replace('[LINK_AFILIADO]', value[0])
                                                                    , parse_mode='HTML', disable_web_page_preview=True)  #Variavel Dinâmica
            
            except:
                pass

    except:
        pass

    contador_passagem = 1


def enviarSinalTelegram():
    global table_sinal
    
    ''' Lendo o arquivo txt canais '''
    txt = open(r"arquivos_txt\canais.txt", "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[7].replace('canais= ','').replace('\n','')
    canais = ast.literal_eval(canais) # Convertendo string em dicionario 

    ''' Lendo o arquivo txt config-mensagens '''
    with open('arquivos_txt/sinal.txt',"r", encoding="utf-8") as arquivo:
        message_sinal = arquivo.read()

    ''' Enviando mensagem Telegram '''
    try:
        for key, value in canais.items():
            try:
                
                ''' Mensagem '''
                bot.delete_message(key, globals()[f'alerta_{key}'].message_id)
                globals()[f'sinal_{key}'] = bot.send_message(key, message_sinal
                                                                  .replace('[VELA_ATUAL]', str(vela_atual))
                                                                  .replace('[CASHOUT]', estrategia[-2])
                                                                  .replace('[LINK_AFILIADO]', value[0])
                                                                  , parse_mode='HTML', disable_web_page_preview=True)
            
            except:
                pass
    
    except:
        pass


def apagaAlertaTelegram():
    global contador_passagem

    ''' Lendo o arquivo txt canais '''
    txt = open(r"arquivos_txt\canais.txt", "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[7].replace('canais= ','').replace('\n','')
    canais = ast.literal_eval(canais) # Convertendo string em dicionario 

    try:
        for key,value in canais.items():
            try:
                bot.delete_message(key, globals()[f'alerta_{key}'].message_id)
            except:
                pass
    except:
        pass

    contador_passagem = 0


def mensagem_gale(contador_cash):

    ''' Lendo o arquivo txt canais '''
    txt = open(r"arquivos_txt\canais.txt", "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[7].replace('canais= ','').replace('\n','')
    canais = ast.literal_eval(canais) # Convertendo string em dicionario 
    
    ''' Lendo o arquivo txt config-mensagens '''
    with open('arquivos_txt/gale.txt',"r", encoding="utf-8") as arquivo:
        message_gale = arquivo.read()
            
    for key, value in canais.items():
        try:
            
            globals()[f'gale_{key}'] = bot.send_message(key, message_gale.replace('[GALE]','1º' if contador_cash == 1 else '2º'), parse_mode='HTML')
        
        except:
            pass

    time.sleep(5)

    ''' APAGANDO MENSAGEM DE GALE '''
    ''' Lendo o arquivo txt canais '''
    txt = open(r"arquivos_txt\canais.txt", "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[7].replace('canais= ','').replace('\n','')
    canais = ast.literal_eval(canais) # Convertendo string em dicionario 

    try:
        for key,value in canais.items():
            try:
                bot.delete_message(key, globals()[f'gale_{key}'].message_id)
            except:
                pass
    except:
        pass


def mensagem_seq_green(sequencia_green):
    try:
        msg_seq_green = open('arquivos_txt/seq_green.txt', 'r', encoding='UTF-8').read()

        ''' Lendo o arquivo txt canais '''
        txt = open(r"arquivos_txt\canais.txt", "r", encoding="utf-8")
        arquivo = txt.readlines()
        canais = arquivo[7].replace('canais= ','').replace('\n','')
        canais = ast.literal_eval(canais) # Convertendo string em dicionario 
        
        for key, value in canais.items():
            try:
                
                bot.send_message(key, msg_seq_green.replace('[SEQ]', str(sequencia_green)), parse_mode='HTML')
            
            except:
                pass
    
    except:pass


def mensagem_assertividade():
    try:
        placar()

        msg_assertividade = open('arquivos_txt/msg_placar.txt', 'r', encoding='UTF-8').read()

        ''' Lendo o arquivo txt canais '''
        txt = open(r"arquivos_txt\canais.txt", "r", encoding="utf-8")
        arquivo = txt.readlines()
        canais = arquivo[7].replace('canais= ','').replace('\n','')
        canais = ast.literal_eval(canais) # Convertendo string em dicionario 
        
        for key, value in canais.items():
            try:
                
                globals()[f'gale_{key}'] = bot.send_message(key, msg_assertividade
                                                                 .replace('[WINS]', str(placar_win))
                                                                 .replace('[LOSS]', str(placar_loss))
                                                                 .replace('[ASSERTIVIDADE]', asserividade) #str(round((a/b)*100,2))
                                                                 , parse_mode='HTML')
            
            except:
                pass
    
    except:pass


def checkSinalEnviado(lista_resultados):
    global alerta_free
    global alerta_vip
    global message_canal_free
    global message_canal_vip
    global placar_win
    global placar_semGale
    global placar_gale1
    global placar_gale2
    global placar_gale3
    global placar_loss
    global resultados_sinais
    global ultimo_horario_resultado
    global validador_sinal
    global stop_loss
    global estrategia
    global contador_passagem
    global lista_resultados_sinal
    global table
    global contador_cash, seq_green, placar_geral, asserividade, gale

    resultado_valida_sinal = []
    contador_cash = 0
    
    while contador_cash <= int(estrategia[-1]):

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass

        # Validando o horario para envio do relatório diário
        validaData()

        try:
           
            ultimo_result = ws.recv()

            if '[{"f":true' in ultimo_result:

                resultado_atual = json.loads(ultimo_result)['M'][0]['A'][0]['v']

                lista_resultados.append(resultado_atual)
                
                print(resultado_atual)
    
                # VALIDANDO WIN OU LOSS
                if float(lista_resultados[-1]) >= float(cash_out[:-1]):
                
                    # validando o tipo de WIN
                    if contador_cash == 0:
                        print('WIN SEM GALE')
                        stop_loss.append('win')

                        # Atualizando placar e Alimentando o arquivo txt
                        placar_win +=1
                        placar_semGale +=1
                        placar_geral = placar_win + placar_loss

                        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                            arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}")
                        
                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                        try:
                            # Somando Win na estratégia da lista atual
                            for pe in placar_estrategias:
                                if pe[:-5] == estrategia:
                                    pe[-5] = int(pe[-5])+1
                        except:
                            pass
                        
                        
                    if contador_cash == 1:
                        print('WIN GALE1')
                        stop_loss.append('win')

                        # Atualizando placar e Alimentando o arquivo txt
                        placar_win +=1
                        placar_gale1 +=1
                        placar_geral = placar_win + placar_loss
                        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                            arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}")
                         

                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                        try:
                            # Somando Win na estratégia da lista atual
                            for pe in placar_estrategias:
                                if pe[:-5] == estrategia:
                                    pe[-4] = int(pe[-4])+1

                        except:
                            pass


                    if contador_cash == 2:
                        print('WIN GALE2')
                        stop_loss.append('win')
                        
                        # Atualizando placar e Alimentando o arquivo txt
                        placar_win +=1
                        placar_gale2 +=1
                        placar_geral = placar_win + placar_loss
                        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                            arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}")
                
                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)
                        
                        try:
                            # Somando Win na estratégia da lista atual
                            for pe in placar_estrategias:
                                    if pe[:-5] == estrategia:
                                        pe[-3] = int(pe[-3])+1
                        except:
                            pass
                        
                
                    # editando mensagem enviada
                    try:
                        ''' Lendo o arquivo txt canais '''
                        txt = open(r"arquivos_txt\canais.txt", "r", encoding="utf-8")
                        arquivo = txt.readlines()
                        canais = arquivo[7].replace('canais= ','').replace('\n','')
                        canais = ast.literal_eval(canais) # Convertendo string em dicionario 

                        if lista_resultados[-1] == 'E':
                            
                            message_green = 'GREENZADA no empate! 🟢'

                        else:
                            ''' Lendo o arquivo txt config-mensagens '''
                            with open('arquivos_txt/green.txt',"r", encoding="utf-8") as arquivo:
                                message_green = arquivo.read()


                        for key, value in canais.items():
                            try:
                                
                                bot.reply_to(globals()[f'sinal_{key}'], message_green
                                                                                     .replace('[VELA_ATUAL]', str(lista_resultados[-1]))
                                                                                     .replace('[LINK_AFILIADO]', value[0]),
                                                                                     parse_mode='HTML')

                            except:
                                pass

                        seq_green +=1

                        #Valida sequencia de green
                        if seq_green >= 5:
                                
                            mensagem_seq_green(seq_green)

                        
                        #Enviando mensagem de Assertividade
                        mensagem_assertividade()

                        

                    except:
                        pass
                    

                    print('='*150)
                    validador_sinal = 0
                    contador_cash = 0
                    contador_passagem = 0
                    
                    #intervalo entre sinais
                    time.sleep(intervalo_sinais)


                    return

            
                else:
                    print('LOSSS')
                    print('==================================================')
                    contador_cash+=1

                    if int(estrategia[-1]) > 0 and contador_cash <= int(estrategia[-1]):

                        mensagem_gale(contador_cash)

                    
                    continue

            
        except:
            continue


    if contador_cash > int(estrategia[-1]):
        print(f'LOSSS gale {gale}')
        placar_loss +=1
        stop_loss.append('loss')
        
        # Preenchendo arquivo txt
        placar_geral = placar_win + placar_loss
        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
            arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}")
        
        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
                        
        # editando mensagem
        try:
            ''' Lendo o arquivo txt canais '''
            txt = open(r"arquivos_txt\canais.txt", "r", encoding="utf-8")
            arquivo = txt.readlines()
            canais = arquivo[7].replace('canais= ','').replace('\n','')
            canais = ast.literal_eval(canais) # Convertendo string em dicionario 
            
            ''' Lendo o arquivo txt config-mensagens '''
            with open('arquivos_txt/red.txt',"r", encoding="utf-8") as arquivo:
                message_red = arquivo.read()

            for key,value in canais.items():
                try:
                    
                    bot.reply_to(globals()[f'sinal_{key}'], message_red, parse_mode = 'HTML')
                
                except:
                    pass

        
        except:
            pass


        ''' Alimentando "Gestão" estratégia '''
        try:
            # Somando Win na estratégia da lista atual
            for pe in placar_estrategias:
                if pe[:-5] == estrategia:
                    pe[-1] = int(pe[-1])+1
            
        except:
            pass

        

        # Validando o stop_loss
        if 'win' in stop_loss:
            stop_loss = []
            stop_loss.append('loss')
        

        #if stop_loss.count('loss') == 2:
        #    try:
        #    
        #        if canal_free !='':
        #            bot.send_message(canal_free, f'⛔🛑 Alunos,\nMercado instável! Aguardem a normalização do mesmo conforme indicamos no curso 📚.\n\nAtt, Diretoria Pro Tips 🤝 ')
#
        #        if canal_vip !='':
        #            bot.send_message(canal_vip, f'⛔🛑 Alunos,\nMercado instável! Aguardem a normalização do mesmo conforme indicamos no curso 📚.\n\nAtt, Diretoria Pro Tips 🤝 ')
#
        #        stop_loss = []
        #        print('STOP LOSS - ANÁLISE VOLTARÁ EM 30 MINUTOS \n\n')
        #        time.sleep(1800)
#
        #    except:
        #        pass
#
        mensagem_assertividade()

        print('=' * 100)
        validador_sinal = 0
        contador_cash = 0
        contador_passagem = 0
        seq_green = 0

        #intervalo entre sinais
        time.sleep(intervalo_sinais)

        return




inicio()
placar()
#pegar_evosessionid()

#_____________________________________________________________________________________ TELEGRAM__________________________________________________________________________________#


print('\n\n')
print('############################################ AGUARDANDO COMANDOS ############################################')


# VARIAVEIS
#placar_win = 0
#placar_semGale= 0
#placar_gale1= 0
#placar_gale2= 0
#placar_gale3= 0
#placar_loss = 0
#resultados_sinais = placar_win + placar_loss
estrategias = []
placar_estrategias = []
estrategias_diaria = []
placar_estrategias_diaria = []
contador = 0
contador_passagem = 0
botStatus = 0
gale = 0
intervalo_sinais = 0



# LENDO TXT PARA DEFINIR VARIAVEL FREE E VIP E VALIDAÇÃO DE USUÁRIO
txt = open(r"arquivos_txt\canais.txt", "r", encoding="utf-8")
arquivo = txt.readlines()
CHAVE_API = arquivo[2].split(' ')[1].split('\n')[0]

ids = arquivo[6].split(' ')[1].split('\n')[0]
canais = arquivo[7].split(' ')[1].split('\n')[0].split((','))
bot = telebot.TeleBot(CHAVE_API)


# LENDO TXT DE ESTRATEGIAS
try:
    txt_estrategias = open("arquivos_txt/estrategias.txt", 'r', encoding='UTF-8').read()
    lista_estrategias_txt = ast.literal_eval(txt_estrategias)

    if txt_estrategias == '':
        pass

    else:
        #ADD estrategia na lista de estrategias
        for estrategia in lista_estrategias_txt:
            estrategias.append(estrategia)
except:
    pass


#LENDO ARQUIVO DE GALE
txt_qntd_gale = open('arquivos_txt/qntd_gale.txt', 'r', encoding='UTF-8').read()

if txt_qntd_gale == '':
    pass

else: gale = int(txt_qntd_gale) 

#LENDO ARQUIVO DE INTERVALO DE SINAIS
txt_intervalo_sinais = open('arquivos_txt/intervalo_sinais.txt', 'r', encoding='UTF-8').read()

if txt_intervalo_sinais == '':
    pass

else: intervalo_sinais = int(txt_intervalo_sinais) 



######################################################


global message


def generate_buttons_estrategias(bts_names, markup):
    for button in bts_names:
        markup.add(types.KeyboardButton(button))
    return markup



def pausarBot():
     while True:
        try:
            global parar
            global browser
            parar = 1
            time.sleep(1)
            break

        except:
            continue



@bot.message_handler(commands=['🔁 Cadastrar/Editar_Gale'])
def cadastrarGale(message):

    global gale

    try:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
        markup = markup.add(f'Gale = {gale}',
                            '◀ Voltar')

        message_gale = bot.reply_to(message, "🤖 Ok! Informe a quantidade de Gale 🔁", reply_markup=markup)
        bot.register_next_step_handler(message_gale, registra_gale)
    

    except:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia', '🔁 Cadastrar/Editar Gale', '⏳ Intervalo Sinais', '📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_gale = bot.reply_to(message, "⚠️ Algo inesperado aconteceu. Tente novamente em alguns instanstes.", reply_markup=markup)


@bot.message_handler(commands=['⏳ Intervalo_Sinais'])
def cadastrarIntervalo(message):

    global intervalo_sinais

    try:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
        markup = markup.add(f'Intervalo = {intervalo_sinais}',
                            '◀ Voltar')

        message_intervalo = bot.reply_to(message, "🤖 Ok! Informe o intervalo entre os sinais (em segundos)", reply_markup=markup)
        bot.register_next_step_handler(message_intervalo, registra_intervalo_sinais)
    

    except:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia', '🔁 Cadastrar/Editar Gale', '⏳ Intervalo Sinais', '📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_gale = bot.reply_to(message, "⚠️ Algo inesperado aconteceu. Tente novamente em alguns instanstes.", reply_markup=markup)



@bot.message_handler(commands=['⚙ Cadastrar_Estratégia'])
def cadastrarEstrategia(message):

    global contador_passagem

    if contador_passagem == 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('◀ Voltar')

        message_estrategia = bot.reply_to(message, "🤖 Ok! Escolha um padrão acima ou abaixo de velas, a vela que deverá fazer CASH OUT e uma opção de GALE \n\n Ex: +1,-2,-10.35,1.5X,1", reply_markup=markup)
        bot.register_next_step_handler(message_estrategia, registrarEstrategia)
    
    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia', '🔁 Cadastrar/Editar Gale', '⏳ Intervalo Sinais', '📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_estrategia = bot.reply_to(message, "🤖⛔ Estou validando uma estratégia! Tente novamente em alguns instanstes.", reply_markup=markup)



@bot.message_handler(commands=['🗑 Apagar_Estratégia'])
def apagarEstrategia(message):
    global estrategia
    global estrategias
    global contador_passagem

    print('Excluir estrategia')

    if contador_passagem == 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        #Add to buttons by list with ours generate_buttons function.
        markup_estrategias = generate_buttons_estrategias([f'{estrategia}' for estrategia in estrategias], markup)
        markup_estrategias.add('◀ Voltar')   


        message_excluir_estrategia = bot.reply_to(message, "🤖 Escolha a estratégia a ser excluída 👇", reply_markup=markup_estrategias)
        bot.register_next_step_handler(message_excluir_estrategia, registrarEstrategiaExcluida)
    
    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia', '🔁 Cadastrar/Editar Gale', '⏳ Intervalo Sinais', '📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_excluir_estrategia = bot.reply_to(message, "🤖⛔ Estou validando uma estratégia! Tente novamente em alguns instanstes.", reply_markup=markup)



@bot.message_handler(commands=['📜 Estrategias_Cadastradas'])
def estrategiasCadastradas(message):
    global estrategia
    global estrategias

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia', '🔁 Cadastrar/Editar Gale', '⏳ Intervalo Sinais', '📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','🛑 Pausar Bot')

    bot.reply_to(message, "🤖 Ok! Listando estratégias", reply_markup=markup)

    for estrategia in estrategias:
        #print(estrategia)
        bot.send_message(message.chat.id, f'{estrategia}')



@bot.message_handler(commands=['📊 Placar Atual'])
def placar_atual(message):
    global placar
    global resultados_sinais

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia', '🔁 Cadastrar/Editar Gale', '⏳ Intervalo Sinais', '📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','🛑 Pausar Bot')

    try:
        placar()

        resposta = bot.reply_to(message,\
        "📊 Placar Atual do dia "+data_hoje+":\n\
        =====================\n\
        😍 WIN - "+str(placar_win)+"\n\
        🏆 WIN S/ GALE - "+str(placar_semGale)+"\n\
        🥇 WIN GALE1 - "+str(placar_gale1)+"\n\
        🥈 WIN GALE2 - "+str(placar_gale2)+"\n\
        😭 LOSS - "+str(placar_loss)+"\n\
        =====================\n\
        🎯 Assertividade "+ asserividade,\
         reply_markup=markup)
        
    except Exception as a:
        logger.error('Exception ocorrido no ' + repr(a))
        #placar = bot.reply_to(message,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%", reply_markup=markup)
        pass



@bot.message_handler(commands=['♻ Resetar Resultados'])
def resetarResultados(message):
    global placar_win
    global placar_semGale
    global placar_gale1
    global placar_gale2
    global placar_gale3
    global placar_loss
    global placar
    global resultados_sinais
    global placar_estrategias

    # Resetando placar Geral (placar geral)
    placar_win = 0
    placar_semGale= 0
    placar_gale1= 0
    placar_gale2= 0
    placar_gale3= 0
    placar_loss = 0

    # Resetando placar das estrategias (Gestão)
    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia', '🔁 Cadastrar/Editar Gale', '⏳ Intervalo Sinais', '📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','🛑 Pausar Bot')

    for pe in placar_estrategias:
        pe[-5], pe[-4], pe[-3], pe[-2], pe[-1] = 0,0,0,0,0
        assertividade = '0%'
    
    message_final = bot.reply_to(message, "🤖♻ Resultados resetados com sucesso ✅", reply_markup=markup)



@bot.message_handler(commands=['📈 Gestão'])
def gestao(message):
    global placar
    global resultados_sinais
    global placar_estrategias

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia', '🔁 Cadastrar/Editar Gale', '⏳ Intervalo Sinais', '📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','🛑 Pausar Bot')

    
    for pe in placar_estrategias:
        total = int(pe[-5]) + int(pe[-4]) + int(pe[-3]) + int(pe[-2]) + int(pe[-1])
        soma_win = int(pe[-5]) + int(pe[-4]) + int(pe[-3]) + int(pe[-2])

        try:
            assertividade = str(round(soma_win / total*100, 1)).replace('.0',"")+"%"
        except:
            assertividade = '0%'

        bot.send_message(message.chat.id, '🧠 '+''.join(pe[:-5]) + f'\n==========================\n 🏆= {pe[-5]}  |  🥇= {pe[-4]}  |  🥈= {pe[-3]}  |  🥉= {pe[-2]} \n\n ✅ - {soma_win} \n ❌ - {pe[-1]} \n==========================\n 🎯 {assertividade}  ', reply_markup=markup)
        
        #print(f'🧠 {pe[:-5]} \n==========================\n 🏆= {pe[-5]}  |  🥇= {pe[-4]}  |  🥈= {pe[-3]}  |  🥉= {pe[-2]} \n\n ✅ - {soma_win} \n ❌ - {pe[-1]} \n==========================\n 🎯 {assertividade}'
        #)



@bot.message_handler(commands=['🛑 Pausar_bot'])
def pausar(message):
    global botStatus
    global contador_passagem
    global parar

    if contador_passagem != 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia', '🔁 Cadastrar/Editar Gale', '⏳ Intervalo Sinais', '📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_excluir_estrategia = bot.reply_to(message, "🤖⛔ Estou validando uma estratégia! Tente novamente em alguns instanstes.", reply_markup=markup)

    elif botStatus == 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia', '🔁 Cadastrar/Editar Gale', '⏳ Intervalo Sinais', '📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Bot já está pausado ", reply_markup=markup)

    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia', '🔁 Cadastrar/Editar Gale', '⏳ Intervalo Sinais', '📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        print('\n\n')
        print('Comando: Parar BOT')
        print('Parando o BOT....\n')
        botStatus = 0
        parar += 1
        #pausarBot()

        print('###################### AGUARDANDO COMANDOS ######################')

        message_final = bot.reply_to(message, "🤖 Ok! Bot pausado 🛑", reply_markup=markup)



@bot.message_handler(commands=['start'])
def start(message):

    if str(message.chat.id) in ids:

        #Add to buttons by list with ours generate_buttons function.
        #markup = generate_buttons(['/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','📊 Placar Atual','❌ Pausar Bot'], markup)
        
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia', '🔁 Cadastrar/Editar Gale', '⏳ Intervalo Sinais', '📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message, "🤖 Bot Jet X Iniciado! ✅ Escolha uma opção 👇",
                                reply_markup=markup)
        
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(message_opcoes, opcoes)
    
    else:
        message_error = bot.reply_to(message, "🤖 Você não tem permissão para acessar este Bot ❌🚫")



@bot.message_handler()
def opcoes(message_opcoes):

    if message_opcoes.text in ['⚙ Cadastrar Estratégia']:
        print('Cadastrar Estrategia')

        cadastrarEstrategia(message_opcoes)


    if message_opcoes.text in['📜 Estratégias Cadastradas']:
        print('Estrategias Cadastradas')
        estrategiasCadastradas(message_opcoes)


    if message_opcoes.text in ['🗑 Apagar Estratégia']:
        print('Apagar estrategia')
        apagarEstrategia(message_opcoes)



    if message_opcoes.text in ['✅ Ativar Bot']:
        global botStatus
        global placar
        global estrategia
        global stop_loss
        global botStatus
        global reladiarioenviado
        global parar

        print('Ativar Bot')

        if botStatus == 1:

            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia', '🔁 Cadastrar/Editar Gale', '⏳ Intervalo Sinais', '📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖⛔ Bot já está ativado",
                                reply_markup=markup)

        elif estrategias == []:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia', '🔁 Cadastrar/Editar Gale', '⏳ Intervalo Sinais', '📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖⛔ Cadastre no mínimo 1 estratégia antes de iniciar",
                                reply_markup=markup)
        
        else:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia', '🔁 Cadastrar/Editar Gale', '⏳ Intervalo Sinais', '📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','🛑 Pausar Bot')

            message_final = bot.reply_to(message_opcoes, "🤖 Ok! Bot Ativado com sucesso! ✅ Em breve receberá sinais nos canais informados no arquivo auxiliar!", reply_markup = markup)
            
            stop_loss = []
            botStatus = 1
            vela_anterior = 0
            reladiarioenviado = 0
            parar = 0
    
            print('######################### ANALISANDO AS ESTRATÉGIAS CADASTRADAS  #########################')
            print()

            coletarDados()
            
    
    if message_opcoes.text in['📊 Placar Atual']:
        print('Placar Atual')
        placar_atual(message_opcoes)


    if message_opcoes.text in ['♻ Resetar Resultados']:
        print('Resetar Resultados')
        resetarResultados(message_opcoes)


    if message_opcoes.text in['📈 Gestão']:
        print('Gestão')
        gestao(message_opcoes)


    if message_opcoes.text in ['🛑 Pausar Bot']:
        print('Pausar Bot')
        pausar(message_opcoes)
    

    if message_opcoes.text in ['🔁 Cadastrar/Editar Gale']:
        print('Cadastrar Gale')
        cadastrarGale(message_opcoes)
        
    
    if message_opcoes.text in ['⏳ Intervalo Sinais']:
        print('Intervalo Sinais')
        cadastrarIntervalo(message_opcoes)



@bot.message_handler()
def registrarEstrategia(message_estrategia):
    global estrategia
    global estrategias
    global placar_estrategia
    global placar_estrategias
    global placar_estrategias_diaria
    global estrategias_diaria

    if message_estrategia.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia', '🔁 Cadastrar/Editar Gale', '⏳ Intervalo Sinais', '📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_estrategia, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        return

    
    estrategia = message_estrategia.text
    placar_estrategia = message_estrategia.text
    
    estrategia = estrategia.split(',')
    placar_estrategia = placar_estrategia.split(',')

    placar_estrategia.extend([0,0,0,0,0])

    # Adicionando estratégia atual
    estrategias.append(estrategia)
    placar_estrategias.append(placar_estrategia)

    # Acumulando estratégia do dia
    estrategias_diaria.append(estrategia)
    placar_estrategias_diaria.append(placar_estrategia)

    #Escrevendo estrategia no TXT
    estrategias_salvas = open('arquivos_txt/estrategias.txt', 'r', encoding='UTF-8').read()
    if estrategias_salvas == '':
        with open('arquivos_txt/estrategias.txt', 'w', encoding='UTF-8') as arquivo:
            arquivo.write(str(estrategias))
            arquivo.close()
    
    else:
        estrategias_salvas = ast.literal_eval(estrategias_salvas)
        estrategias_salvas.append(estrategia)
        with open('arquivos_txt/estrategias.txt', 'w', encoding='UTF-8') as arquivo:
            arquivo.write(str(estrategias))
            arquivo.close()
        
            
    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia', '🔁 Cadastrar/Editar Gale', '⏳ Intervalo Sinais', '📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','🛑 Pausar Bot')

    bot.reply_to(message_estrategia, "🤖 Estratégia cadastrada com sucesso! ✅", reply_markup=markup)


def registrarEstrategiaExcluida(message_excluir_estrategia):
    global estrategia
    global estrategias

    if message_excluir_estrategia.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia', '🔁 Cadastrar/Editar Gale', '⏳ Intervalo Sinais', '📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_excluir_estrategia, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        return
    
    estrategia_excluir = message_excluir_estrategia.text
    
    for estrategia in estrategias:
        if estrategia_excluir == str(estrategia):
            estrategias.remove(estrategia)

    
    for pe in placar_estrategias:
        if estrategia_excluir == str(pe[:-5]):
            placar_estrategias.remove(pe)

    #ATUALIZANDO ARQUIVO TXT DE ESTRATEGIAS
    txt_estrategias = open('arquivos_txt/estrategias.txt', 'w', encoding='UTF-8').write(str(estrategias))


    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia', '🔁 Cadastrar/Editar Gale', '⏳ Intervalo Sinais', '📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','🛑 Pausar Bot')

    bot.reply_to(message_excluir_estrategia, "🤖 Estratégia excluída com sucesso! ✅", reply_markup=markup)


def registra_gale(message_gale):

    global gale
    
    if message_gale.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia', '🔁 Cadastrar/Editar Gale', '⏳ Intervalo Sinais', '📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_gale, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        return

    else:

        gale = int(message_gale.text)

        #ATUALIZANDO TXT DE GALE
        txt_qntd_gale = open('arquivos_txt/qntd_gale.txt', 'w', encoding='UTF-8').write(str(gale))

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia', '🔁 Cadastrar/Editar Gale', '⏳ Intervalo Sinais', '📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        bot.reply_to(message_gale, "🤖 Gale cadastrado com sucesso ✅", reply_markup=markup)


def registra_intervalo_sinais(message_intervalo):

    global intervalo_sinais
    
    if message_intervalo.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia', '🔁 Cadastrar/Editar Gale', '⏳ Intervalo Sinais', '📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_intervalo, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        return

    else:

        intervalo_sinais = int(message_intervalo.text)

        #ATUALIZANDO TXT DE GALE
        txt_intervalo_sinais = open('arquivos_txt/intervalo_sinais.txt', 'w', encoding='UTF-8').write(str(intervalo_sinais))

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia', '🔁 Cadastrar/Editar Gale', '⏳ Intervalo Sinais', '📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','🛑 Pausar Bot')

        bot.reply_to(message_intervalo, "🤖 Intervalo cadastrado com sucesso ✅", reply_markup=markup)




while True:
    try:
        bot.infinity_polling(timeout=600)
    except:
        bot.infinity_polling(timeout=600)


