import time
import logging
from datetime import datetime, timedelta
import telebot
from telegram.ext import *
from telebot import *
import os
import ast
import warnings
#from webdriver_manager.firefox import GeckoDriverManager
import requests
import json

#_______________________________________________________________________#____________________________________________________________________________________________________

print()
print('                                #################################################################')
print('                                ###################     BOT SPACEMAN    #########################')
print('                                #################################################################')
print('                                ##################### SEJA BEM VINDO ############################')
print('                                #################################################################')
print('                                ############# DESENVOLVIDO POR VICTOR RODRIGUES #################')
print('                                #################################################################\n')
print('Versão = 2.0.0')
print('Ambiente: Produção\n\n\n')



    
def logar():
    global header
    global usuario
    global senha


    ''' Inserindo login e senha '''
    ''' Lendo o arquivo txt config-mensagens '''
    txt = open("canais.txt", "r", encoding="utf-8")
    mensagem_login = txt.readlines()
    usuario = mensagem_login[2].replace('\n','').split('= ')[1] 
    senha = mensagem_login[3].replace('\n','').split('= ')[1]


    URL = 'https://backoffice.mesk.bet/api/auth/login'

    header = {
    'Content-Type': 'application/json'
    }

    payload = {"email":usuario,
               "password":senha}
    
    token = requests.post(URL, headers=header, json=payload).json()['token']

    return token


def puxar_dados_acesso(token_autorizacao):
    global username

    header = {
                'Content-Type': 'application/json',
                "authorization": f"bearer {token_autorizacao}"
                }
    
    payload = {"email":usuario,
               "password":senha
               }
    

    URL = 'https://backoffice.mesk.bet/api/auth/me'

    uuid_usuário = requests.post(URL, headers=header, json=payload).json()['player']['uuid']
    username = requests.post(URL, headers=header, json=payload).json()['username']

    return uuid_usuário, username


def acessar_game(uuid_usuário):

    #LOCATION PRAGMATICPLAY
    URL_FORNECEDOR = f'https://pi.njoybingo.com/game.do?token={uuid_usuário}&pn=meskbet&lang=pt&game=PRPLAY-1301&type=CHARGED'
    location = requests.get(URL_FORNECEDOR, allow_redirects=False).headers.get('location')
    
    #SEGUNDO LOCATION
    location2 = requests.get(location, allow_redirects=False).headers.get('location')
    

    header = {
    "Content-Type": "application/json",
    "referer": "https://mesk.bet/"
    }

    #Usando o Token gerado pelo FORNECEDOR para Acessar o GAME e pegar o TOKEN para ter acesso aos dados do GAME
    #URL_GAME = f'https://wac.paconassa.com/?game=LUVASG&token={token_fornecedor}&pn=meskbet&lang=pt&type=CHARGED'
    jsession_id = requests.get(location2, allow_redirects=False).headers.get('location').split('JSESSIONID=')[1].split('&')[0]

    return jsession_id


def processo_pegar_jsessionid():
        global token_autorizacao, uuid_usuário, username, jsession_id

        token_autorizacao = logar()
        uuid_usuário, username = puxar_dados_acesso(token_autorizacao)
        jsession_id = acessar_game(uuid_usuário)

        return jsession_id


# GERA TXT DO PLACAR
def placar():
    global placar_win
    global placar_semGale
    global placar_gale1
    global placar_gale2
    global placar_loss
    global placar_geral
    global asserividade, placar_2x
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
                placar_2x = int(arq_placar[6].split(',')[1])
            

            except:
                pass

            
    else:
        # Criar um arquivo com a data atual
        with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
            arquivo.write("win,0\nsg,0\ng1,0\ng2,0\nloss,0\nass,0\npl2x,0")

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
                placar_2x = int(arq_placar[6].split(',')[1])
            
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
    global logger
    global lista_anterior
    global horario_inicio
    
    horario_inicio = datetime.now()

    lista_anterior = []
    logger = logging.getLogger()

    # Definindo opções para o browser
    warnings.filterwarnings("ignore", category=DeprecationWarning) 

         
def enviar_alerta(estrategia):
    global contador_passagem

    ''' Lendo o arquivo txt canais '''
    txt = open("canais.txt", "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[12].replace('canais= ','').replace('\n','')
    canais = ast.literal_eval(canais) # Convertendo string em dicionario 

    ''' Lendo o arquivo txt config-mensagens '''
    txt = open("config-mensagens.txt", "r", encoding="utf-8")
    mensagem_alerta = txt.readlines()

    ''' Enviando mensagem Telegram '''
    try:
        for key, value in canais.items():
            try:
                ''' Mensagem '''
                table_alerta = mensagem_alerta[0].replace('\n','') + '\n\n' + \
                               mensagem_alerta[2].replace('\n','') + '\n\n' + \
                               mensagem_alerta[4].replace('\n','').replace('[OPERADOR]', 'maior' if estrategia[-3][0] == '+' else 'menor').replace('[ULTIMA_CONDICAO]', estrategia[-3][1:]) + '\n\n' + \
                               mensagem_alerta[6].replace('\n','').replace('[LINK_JOGO]', value[0]) + '\n\n' + \
                               mensagem_alerta[8].replace('\n','').replace('[LINK_CADASTRO]', value[1])

                globals()[f'alerta_{key}'] = bot.send_message(key, table_alerta, parse_mode='HTML', disable_web_page_preview=True)  #Variavel Dinâmica
           
            except:
                pass

    except:
        pass

    contador_passagem = 1


def enviar_sinal(vela_atual, estrategia):
    global table_sinal

    ''' Lendo o arquivo txt canais '''
    txt = open("canais.txt", "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[12].replace('canais= ','').replace('\n','')
    canais = ast.literal_eval(canais) # Convertendo string em dicionario 

    ''' Lendo o arquivo txt config-mensagens '''
    txt = open("config-mensagens.txt", "r", encoding="utf-8")
    mensagem_sinal = txt.readlines()

    ''' Enviando mensagem Telegram '''
    try:
        for key, value in canais.items():
            try:
                # Estruturando mensgaem
                table_sinal = mensagem_sinal[17].replace('\n','') + '\n\n' + \
                              mensagem_sinal[19].replace('\n','').replace('[VELA_ATUAL]', vela_atual) + '\n\n' + \
                              mensagem_sinal[21].replace('\n','').replace('[CASH_OUT]', estrategia[-2]) + '\n\n' + \
                              mensagem_sinal[23].replace('\n','') + '\n\n' + \
                              mensagem_sinal[25].replace('\n','').replace('[LINK_JOGO]', value[0]) + '\n\n' + \
                              mensagem_sinal[27].replace('\n','').replace('[LINK_CADASTRO]', value[1])
                              
                bot.delete_message(key, globals()[f'alerta_{key}'].message_id)
                globals()[f'sinal_{key}'] = bot.send_message(key, table_sinal, parse_mode='HTML', disable_web_page_preview=True)
            
            except:
                pass
    
    except:
        pass


def apagar_alerta():
    global contador_passagem

    ''' Lendo o arquivo txt canais '''
    txt = open("canais.txt", "r", encoding="utf-8")
    arquivo = txt.readlines()
    canais = arquivo[12].replace('canais= ','').replace('\n','')
    canais = ast.literal_eval(canais) # Convertendo string em dicionario 

    try:
        for key, value in canais.items():
            try:
                bot.delete_message(key, globals()[f'alerta_{key}'].message_id)
            except:
                pass
    except:
        pass

    contador_passagem = 0


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


def coletar_dados():
    global estrategia
    global lista_resultados, url_spaceman


    jsession_id = processo_pegar_jsessionid()

    
    while True:
        try:
            # Auto Refresh
            #auto_refresh()

            # Validando data para envio do relatório diário
            #validaData()
            
            # Validando se foi solicitado o stop do BOT
            if parar != 0:
                break
            else:
                pass

            
            # Pegando o histórico de resultados
            try:
                
                url_spaceman = f'https://gs9.pragmaticplaylive.net/api/ui/statisticHistory?tableId=spacemanyxe123nh&numberOfGames=500&JSESSIONID={jsession_id}&game_mode=lobby_desktop'
                session = requests.session()
                response = session.get(url_spaceman)

                if response.status_code == 403:
                    jsession_id = processo_pegar_jsessionid()
                    continue

                historico_velas = json.loads(response.content)

                lista_resultados = []
                for vela in historico_velas["history"][:10]:
                    numero = vela["gameResult"]
                    lista_resultados.append(numero)

                #Revertendo a Lista
                lista_resultados = list(reversed(lista_resultados))       

            except Exception as e:
                print(e)
                time.sleep(30)
                continue
            

            ''' VALIDANDO SE TEM DADO VAZIO NA LISTA'''
            if '' in lista_resultados:
                continue

            ''' VALIDANDO SE A LISTA ESTA VAZIA'''
            if lista_resultados == []:
                #logar_site()
                continue

            
            # Validando se foi solicitado o stop do BOT
            if parar != 0:
                break
            else:
                pass
            

            print(datetime.now().strftime('%H:%M'))
            ''' Chama a função que valida a estratégia para enviar o sinal Telegram '''
            validar_estrategia(estrategias, session)   #Lista de estrategia

            print('=' * 100)
            lista_resultados = []
            time.sleep(10)
            

            ''' Exceção se o jogo não estiver disponível '''
        except Exception as e:
            print(e)
            jsession_id = processo_pegar_jsessionid()
            continue
            

def validar_estrategia(estrategias, session):
    global gale
    global vela_atual
    global lista_resultados, url_spaceman

    try:
        for estrategia in estrategias:

            # Validando se foi solicitado o stop do BOT
            if parar != 0:
                break
            else:
                pass


            print ('Analisando a Estrategia --> ', estrategia)

            sequencia_minima_alerta = len(estrategia[:-3])
            sequencia_minima_sinal = len(estrategia[:-2])


            print('Historico_Velas --> ', lista_resultados)

            ''' VALIDADOR DE ESTRATEGIA '''
            validador = validador_estrategia(estrategia, lista_resultados, sequencia_minima_alerta)

            ''' Validando se bateu alguma condição'''
            if validador.count(True) == int(sequencia_minima_alerta):
                print('ENVIANDO ALERTA')
                enviar_alerta(estrategia)


                ''' Verifica se a ultima condição bate com a estratégia para enviar sinal Telegram '''
                while True:
                    
                    # Relatório de Placar
                    #validaData()

                    # Validando se foi solicitado o stop do BOT
                    if parar != 0:
                        break
                    else:
                        pass
                    
                    ''' Lendo novos resultados para validação da estratégia'''
                    response = session.get(url_spaceman)

                    if response.status_code == 403:
                        jsession_id = processo_pegar_jsessionid()
                        url_spaceman = f'https://gs9.pragmaticplaylive.net/api/ui/statisticHistory?tableId=spacemanyxe123nh&numberOfGames=500&JSESSIONID={jsession_id}&game_mode=lobby_desktop'
                        session = requests.session()
                        continue

                    historico_velas = json.loads(response.content)

                    lista_proximo_resultados = []
                    for vela in historico_velas["history"][:10]:
                        numero = vela["gameResult"]
                        lista_proximo_resultados.append(numero)

                    #Revertendo a Lista
                    lista_proximo_resultados = list(reversed(lista_proximo_resultados)) 

                    print(lista_proximo_resultados)

                    if '' in lista_proximo_resultados:
                        continue
                    

                    ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
                    if lista_resultados != lista_proximo_resultados:
                        validador = validador_estrategia(estrategia, lista_proximo_resultados, sequencia_minima_sinal)

                        ''' ALIMENTANDO O BANCO '''
                        #alimenta_banco_painel(lista_proximo_resultados)

                        ''' VALIDA SE ENVIA SINAL OU APAGA O ALERTA '''
                        if validador.count(True) == int(sequencia_minima_sinal):
                            print(lista_proximo_resultados[-1])
                            print('ENVIA SINAL TELEGRAM')
                            print('=' * 100)
                            vela_atual = lista_proximo_resultados[-1]
                            enviar_sinal(vela_atual, estrategia)
                            checar_sinal_enviado(lista_proximo_resultados, estrategia, session)
                            time.sleep(1)
                            break


                        else:
                            print('APAGA SINAL DE ALERTA')
                            print('=' * 100)
                            apagar_alerta()
                            lista_resultados = lista_proximo_resultados
                            break
                    else:
                        time.sleep(5)

            else:
                print('=' * 100)


    except:
        print('APAGA SINAL DE ALERTA')
        print('=' * 100)
        apagar_alerta()
        lista_resultados = lista_proximo_resultados


def checar_sinal_enviado(lista_proximo_resultados, estrategia, session):
    global table
    global message_canal
    global resultados_sinais
    global ultimo_horario_resultado
    global validador_sinal
    global stop_loss
    global contador_passagem
    global lista_resultados_sinal
    global placar_win
    global placar_semGale
    global placar_gale1
    global placar_gale2
    global placar_loss
    global placar_geral
    global asserividade
    global data_hoje
    global placar_2x
    global lista_resultados, url_spaceman


    resultados = []
    contador_cash = 0
    gale = estrategia[-1]

    while contador_cash <= int(gale):

        # Validando data para envio do relatório diário
        #validaData()

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass


        try:
            '''' Lendo novos resultados para validação da estratégia'''
            response = session.get(url_spaceman)

            if response.status_code == 403:
                    jsession_id = processo_pegar_jsessionid()
                    url_spaceman = f'https://gs9.pragmaticplaylive.net/api/ui/statisticHistory?tableId=spacemanyxe123nh&numberOfGames=500&JSESSIONID={jsession_id}&game_mode=lobby_desktop'
                    session = requests.session()
                    continue
            
            historico_velas = json.loads(response.content)

            lista_resultados_sinal = []
            for vela in historico_velas["history"][:10]:
                numero = vela["gameResult"]
                lista_resultados_sinal.append(numero)

            #Revertendo a Lista
            lista_resultados_sinal = list(reversed(lista_resultados_sinal)) 

            if '' in lista_resultados_sinal:
                continue
            

            ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
            if lista_proximo_resultados != lista_resultados_sinal:

                resultados.append(lista_resultados_sinal[-1])
                
                print(lista_resultados_sinal[-1])
                #alimenta_banco_painel(lista_resultados_sinal)
            
                # VALIDANDO WIN OU LOSS
                if float(lista_resultados_sinal[-1]) >= float(estrategia[-2].strip('xX')):
                    
                    #Verificando se a vela é maior que 2x
                    if float(lista_resultados_sinal[-1]) >= 2: 
                        placar_2x +=1


                    if contador_cash == 0:
                        print('WIN SEM GALE')
                        stop_loss.append('win')

                        # Atualizando placar e Alimentando o arquivo txt
                        placar_win +=1
                        placar_semGale +=1
                        placar_geral = placar_win + placar_loss

                        try:
                            with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                                arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}\npl2x,{placar_2x}")
                        except:
                            pass
                            
                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")

                        # Somando Win na estratégia da lista atual
                        for pe in placar_estrategias:
                            if pe[:-5] == estrategia:
                                pe[-5] = int(pe[-5])+1

                        

                    if contador_cash == 1:
                        print('WIN GALE1')
                        stop_loss.append('win')

                        # Atualizando placar e Alimentando o arquivo txt
                        placar_win +=1
                        placar_gale1 +=1
                        placar_geral = placar_win + placar_loss

                        try:
                            with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                                arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}\npl2x,{placar_2x}")
                        except:
                            pass

                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                        # Somando Win na estratégia da lista atual
                        for pe in placar_estrategias:
                            if pe[:-5] == estrategia:
                                pe[-4] = int(pe[-4])+1



                    if contador_cash == 2:
                        print('WIN GALE2')
                        stop_loss.append('win')
                        
                        # Atualizando placar e Alimentando o arquivo txt
                        placar_win +=1
                        placar_gale2 +=1
                        placar_geral = placar_win + placar_loss

                        try:
                            with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                                arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}\npl2x,{placar_2x}")
                        except:
                            pass
                            
                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)
                        
                        # Somando Win na estratégia da lista atual
                        for pe in placar_estrategias:
                            if pe[:-5] == estrategia:
                                pe[-3] = int(pe[-3])+1


                    if int(gale) > 2:
                        # Somando WIN no Placar Geral
                        placar_win +=1


                    # respondendo a mensagem do sinal e condição para enviar sticker
                    try:
                        ''' Lendo o arquivo txt canais '''
                        txt = open("canais.txt", "r", encoding="utf-8")
                        arquivo = txt.readlines()
                        canais = arquivo[12].replace('canais= ','').replace('\n','')
                        canais = ast.literal_eval(canais) # Convertendo string em dicionario 
                    
                        ''' Lendo o arquivo txt config-mensagens '''
                        txt = open("config-mensagens.txt", "r", encoding="utf-8")
                        mensagem_green = txt.readlines()
                        

                        for key, value in canais.items():
                            try:
                                
                                msg_green = mensagem_green[32].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(resultados)) + '\n' +\
                                            mensagem_green[33].replace('\n','').replace('[GREEN]',str(placar_win)).replace('[LOSS]', str(placar_loss))+'\n'+\
                                            mensagem_green[34].replace('\n','').replace('[GREEN_SG]',str(placar_semGale))+'\n'+\
                                            mensagem_green[35].replace('\n','').replace('[GREEN_G1]',str(placar_gale1))+'\n'+\
                                            mensagem_green[36].replace('\n','').replace('[GREEN_G2]',str(placar_gale2))+'\n'+\
                                            mensagem_green[37].replace('\n','').replace('[MAIOR_2X]', str(placar_2x))+'\n'+\
                                            mensagem_green[38].replace('\n','').replace('[ASSERTIVIDADE]', str(round(placar_win / (placar_geral)*100, 0)))


                                bot.reply_to(globals()[f'sinal_{key}'], msg_green,  parse_mode='HTML')
                            
                            except:
                                pass
                            
                    except:
                        pass
                    
                    print('=' * 100)
                    validador_sinal = 0
                    contador_cash = 0
                    contador_passagem = 0
                    lista_resultados = lista_resultados_sinal
                    return
        
                else:
                    print('LOSSS')
                    print('=' * 100)
                    contador_cash+=1
                    lista_proximo_resultados = lista_resultados_sinal
                    continue
        
        except:
            continue


    if contador_cash > int(gale):
        print('LOSSS GALE ',estrategia[-1])

        # Preenchendo arquivo txt
        placar_loss +=1
        placar_geral = placar_win + placar_loss

        try:
            with open(f"placar/{data_hoje}.txt", 'w') as arquivo:
                arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}\npl2x,{placar_2x}")
        except:
            pass    
        
        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / placar_geral,"%")
            
        # editando mensagem
        try:
            ''' Lendo o arquivo txt canais '''
            txt = open("canais.txt", "r", encoding="utf-8")
            arquivo = txt.readlines()
            canais = arquivo[12].replace('canais= ','').replace('\n','')
            canais = ast.literal_eval(canais) # Convertendo string em dicionario 
            
            ''' Lendo o arquivo txt config-mensagens '''
            txt = open("config-mensagens.txt", "r", encoding="utf-8")
            mensagem_green = txt.readlines()

            for key, value in canais.items():
                try:

                    msg_loss = mensagem_green[42].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(resultados)) + '\n' +\
                                mensagem_green[43].replace('\n','').replace('[GREEN]',str(placar_win)).replace('[LOSS]', str(placar_loss))+'\n'+\
                                mensagem_green[44].replace('\n','').replace('[GREEN_SG]',str(placar_semGale))+'\n'+\
                                mensagem_green[45].replace('\n','').replace('[GREEN_G1]',str(placar_gale1))+'\n'+\
                                mensagem_green[46].replace('\n','').replace('[GREEN_G2]',str(placar_gale2))+'\n'+\
                                mensagem_green[47].replace('\n','').replace('[MAIOR_2X]', str(placar_2x))+'\n'+\
                                mensagem_green[48].replace('\n','').replace('[ASSERTIVIDADE]', str(round(placar_win / (placar_geral)*100, 0)))

                    bot.reply_to(globals()[f'sinal_{key}'], msg_loss, parse_mode='HTML')
                
                except:
                    pass
            
        except:
            pass


        # Atualizando placar da estratégia
        for pe in placar_estrategias:
            if pe[:-5] == estrategia:
                pe[-1] = int(pe[-1])+1

        
        
        print('=' * 100)
        validador_sinal = 0
        contador_cash = 0
        contador_passagem = 0
        lista_resultados = lista_resultados_sinal
        return






inicio()            # Difinição do webBrowser
#logar_site()         # Logando no Site
placar()             # Chamando o Placar


#________________________________________________________________________________________ TELEGRAM__________________________________________________________________________________#


print('\n\n')
print('############################################ AGUARDANDO COMANDOS ############################################')



# PLACAR
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
botStatus = 0
contador_passagem = 0
lista_estrategias = []



# LENDO TXT PARA DEFINIR VARIAVEL DE CANAIS E VALIDAÇÃO DE USUÁRIO
txt = open("canais.txt", "r", encoding="utf-8")
arquivo = txt.readlines()
usuario = arquivo[2].split(' ')[1]
senha = arquivo[3].split(' ')[1].split('\n')[0]
CHAVE_API = arquivo[7].split(' ')[1].split('\n')[0]

ids = arquivo[11].split(' ')[1].split('\n')[0]
canais = arquivo[12].split(' ')[1].split('\n')[0].split((','))


bot = telebot.TeleBot(CHAVE_API)

global message





''' FUNÇÕES BOT ''' ##



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




@bot.message_handler(commands=['⚙ Cadastrar_Estratégia'])
def cadastrarEstrategia(message):

    global contador_passagem

    if contador_passagem == 0:
        #Init keyboard markup
        markup_tipo = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
        
        markup_tipo = markup_tipo.add('◀ Voltar', 'NOVA ESTRATÉGIA')    

        message_tipo_estrategia = bot.reply_to(message, "🤖 Ok! Escolha cadastrar uma nova estratégia 👇", reply_markup=markup_tipo)
        bot.register_next_step_handler(message_tipo_estrategia, registrarTipoEstrategia)
    
    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

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
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_excluir_estrategia = bot.reply_to(message, "🤖⛔ Estou validando uma estratégia! Tente novamente em alguns instanstes.", reply_markup=markup)


@bot.message_handler(commands=['📜 Estrategias_Cadastradas'])
def estrategiasCadastradas(message):
    global estrategia
    global estrategias

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    bot.reply_to(message, "🤖 Ok! Listando estratégias", reply_markup=markup)

    for estrategia in estrategias:
        #print(estrategia)
        bot.send_message(message.chat.id, f'{estrategia}')


@bot.message_handler(commands=['📊 Placar Atual'])
def placar_atual(message):
    global placar
    global resultados_sinais

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

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
    markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

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
    markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    
    for pe in placar_estrategias:
        total = int(pe[-5]) + int(pe[-4]) + int(pe[-3]) + int(pe[-2]) + int(pe[-1])
        soma_win = int(pe[-5]) + int(pe[-4]) + int(pe[-3]) + int(pe[-2])

        try:
            assertividade = str(round(soma_win / total*100, 1)).replace('.0',"")+"%"
        except:
            assertividade = '0%'

        bot.send_message(message.chat.id, f'🧠 {pe[:-5]} \n==========================\n 🏆= {pe[-5]}  |  🥇= {pe[-4]}  |  🥈= {pe[-3]}  |  🥉= {pe[-2]} \n\n ✅ - {soma_win} \n ❌ - {pe[-1]} \n==========================\n 🎯 {assertividade}  ', reply_markup=markup)
        

@bot.message_handler(commands=['🛑 Pausar_bot'])
def pausar(message):
    global botStatus
    global contador_passagem

    

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
        pausarBot()

        message_final = bot.reply_to(message, "🤖 Ok! Bot pausado 🛑", reply_markup=markup)
        
        print('###################### AGUARDANDO COMANDOS ######################')


@bot.message_handler(commands=['start'])
def start(message):

    if str(message.chat.id) in ids:

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message, "🤖 Bot Spaceman Iniciado! ✅ Escolha uma opção 👇",
                                reply_markup=markup)
        
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(message_opcoes, opcoes)
    
    else:
        message_error = bot.reply_to(message, "🤖 Você não tem permissão para acessar este Bot ❌🚫")


@bot.message_handler()
def opcoes(message_opcoes):
    global message_canal
    global estrategia
    global stop_loss
    global botStatus
    global parar
    global reladiarioenviado
    global contador_outra_oportunidade
    global browser
    global dicionario_estrategia_usuario
    global contador_passagem


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
        global message_canal
        global parar

        print('Ativar Bot')

        if botStatus == 1:

            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖⛔ Bot já está ativado",
                                reply_markup=markup)

        else:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖 Ok! Bot Ativado com sucesso! ✅ Em breve receberá sinais nos canais informados no arquivo auxiliar! ",
                                    reply_markup=markup)
            
            botStatus = 1
            reladiarioenviado = 0
            parar=0
            contador_passagem = 0
            stop_loss = []

            print('##################################################  INICIANDO AS ANÁLISES  ##################################################')
            print()
            
            # CADASTRANDO ESTRATEGIAS DO TXT
            cadastrar_estrategias_txt()
            coletar_dados()

    
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
    

@bot.message_handler()
def registrarTipoEstrategia(message_tipo_estrategia):
    global resposta_usuario

    if message_tipo_estrategia.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_tipo_estrategia, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)
        return


    else:

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

        resposta_usuario = message_tipo_estrategia.text.lower()
        print(resposta_usuario)
         
        markup_nova_estrategia = markup.add('◀ Voltar')

        message_nova_estrategia = bot.reply_to(message_tipo_estrategia, "🤖 Ok! Escolha um padrão acima ou abaixo de velas, a vela que deverá fazer CASH OUT e uma opção de GALE \n\n Ex: +2,-2,-10.35,1.5X,2", reply_markup=markup_nova_estrategia)
        bot.register_next_step_handler(message_nova_estrategia, registrarEstrategia)


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
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

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


    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    bot.reply_to(message_estrategia, "🤖 Estratégia cadastrada com sucesso! ✅", reply_markup=markup)


def registrarEstrategiaExcluida(message_excluir_estrategia):
    global estrategia
    global estrategias

    if message_excluir_estrategia.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')
        
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


    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    bot.reply_to(message_excluir_estrategia, "🤖 Estratégia excluída com sucesso! ✅", reply_markup=markup)


def cadastrar_estrategias_txt():
    global estrategias

    with open('estrategias.txt', 'r', encoding='UTF-8') as arquivo:

        estrategias_txt = arquivo.read()
        estrategias_txt = ast.literal_eval(estrategias_txt)

        estrategias = []

        for estrategia_txt in estrategias_txt:
                
                estrategias.append(estrategia_txt)
                placar_estrategia = [estrategia_txt[1]]
                placar_estrategia.extend([0,0,0,0,0])
                placar_estrategias.append(placar_estrategia)


    

bot.infinity_polling()






