import time
from datetime import datetime, timedelta
import telebot
from telegram.ext import *
from telebot import *
import ast
from websocket import create_connection
import json, os
import requests
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class PegarResultadosBacBo(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)


    def inicio(self):
        global horario_inicio
        global lista_resultados

        horario_inicio = datetime.now()
        lista_resultados = []


    def pegar_evosessionid(self):
        
        while True:

            try:

                #LOGIN
                URL = 'https://arbety.eway.dev:3013/api/auth/signin'

                header = {
                'Content-Type': 'application/json'
                }

                payload = {"email":"raphaugf@hotmail.com",
                        "password":"PHbacbo#23"}
                
                response = requests.post(URL, headers=header, json=payload, verify=False)
                
                token_autorizacao = response.json()['access_token']

                
                #### ENTRANDO NO GAME
                #REQUISIÇÃO1
                URL = 'https://arbety.eway.dev:3000/api/sports/login'

                payload = {"game_id": "19c5259b23df4693a6d1fc41f33b3987"}

                header = {
                    "Accept":"application/json, text/plain, */*",
                    "Authorization":token_autorizacao,
                    "Host":"arbety.eway.dev:3000",
                    "Origin":"https://www.arbety.com",
                    "Referer":"https://www.arbety.com/",
                    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
                    "X-Access-Token":token_autorizacao
                    }
                
                response = requests.post(URL, json=payload, headers=header, verify=False)

                url_entry_params = json.loads(response.content)['game_url'].split('":"')[1].split('"}')[0]

                #REQUISIÇÃO2
                URL = url_entry_params

                response = requests.get(URL, allow_redirects=False)

                location = 'https://tmkybox.evo-games.com'+response.headers.get('Location')

                #REQUISIÇÃO3
                headers = {
                    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "Cookie":"cdn=https://static.egcdn.com; lang=bp; locale=pt-BR; EVOSESSIONID=rleug2e4au4av7zrrm5kswlek36m5yde6f244ded283c9592b0eaeceba743f902835f77076681aca9",
                    "Host":"tmkybox.evo-games.com",
                    "Referer":"https://www.arbety.com/",
                    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
                }
                response = requests.get(location, headers=headers, allow_redirects=False, verify=False)

                evosessionid = response.headers.get('Set-Cookie').split('; Path')[0]

                return evosessionid
            
            except:
                time.sleep(10)
                continue


    def conectar_websocket(self, evosessionid):
        global URL
        global ws
        global cont
        global ultimo_result
        global ultimo_valor_armazenado

        try:

            header = {
            
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "no-cache",
            "Connection": "Upgrade",
            'Cookie':f'cdn=https://static.egcdn.com; lang=bp; locale=pt-BR; {evosessionid}',
            "Host": "tmkybox.evo-games.com",
            "Origin": "https://tmkybox.evo-games.com",
            "Pragma": "no-cache",
            "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
            "Sec-WebSocket-Key": "DZusu8fi4fe4fEauO1hOtQ==",
            "Sec-WebSocket-Version": "13",
            "Upgrade": "websocket",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

            }

            URL = f'wss://tmkybox.evo-games.com/public/bacbo/player/game/BacBo00000000001/socket?messageFormat=json&instance=ek3mkv-rm5nswxwyrvqkkpz-BacBo00000000001&tableConfig=&{evosessionid}&client_version=6.20231213.182434.35996-724ad3d6c5'
            #URL = f'wss://belloatech.evo-games.com/public/bacbo/player/game/BacBo00000000001/socket?messageFormat=json&instance=pe7y9k-rhjuf7mokioplhho-BacBo00000000001&tableConfig=&EVOSESSIONID={evosessionid}&client_version=6.20230823.71249.29885-78ea79aff8'
            
            ws = create_connection(URL, verify=False)

            ws.send(json.dumps([json.dumps(header)]))

            cont = 0
            ultimo_result = ''
            ultimo_valor_armazenado = ''

        except Exception as e:
            print('ERRO NA FUNÇÃO CONECTAR WEBSOCKET----', e)


    def formata_dados(self, ultimo_result):
        ''' Convertendo a letra em cor '''
        # Pegando Resultado da rodada no arquivo JSON
        resultado = json.loads(ultimo_result)['args']['history'][-1]['winner']
                
        if resultado == 'Player':
            resultado = 'P'
            
        if resultado == 'Banker':
            resultado = 'B'
            
        if resultado == 'Tie':
            resultado = 'T'
            
        return resultado

 
    def coletarDados(self):
        global evosessionid
        global lista_resultados

        ultimo_historico = ''
        evosessionid = self.pegar_evosessionid()

        while True:
            
            #OLHANDO A DATA PARA ATUALIZAÇÃO DO PLACAR
            validaData()

            try:
    
                # Pegando o histórico de resultados
                try:

                    self.conectar_websocket(evosessionid)

                    while True:
                        
                        #OLHANDO A DATA PARA ATUALIZAÇÃO DO PLACAR
                        validaData()

                        ultimo_result = ws.recv()

                        if 'bacbo.road' in ultimo_result:

                            #VALIDANDO SE O DADO JÁ FOI REFISTRADO
                            #historico = json.loads(ultimo_result)['args']['history']
                            #if historico.index(json.loads(ultimo_result)['args']['history'][-1]) == ultimo_historico:
                            #    continue


                            resultado_atual = self.formata_dados(ultimo_result)
                            lista_resultados.append(resultado_atual)
                            
                            if len(lista_resultados) > 10:
                                lista_resultados = lista_resultados[-10:]
                          
                            self.gravar_dados_txt(lista_resultados)

                            #ultimo_historico = json.loads(ultimo_result)['args']['history'].index(json.loads(ultimo_result)['args']['history'][-1])

                            
                        ultimo_valor_armazenado = ultimo_result

                                             
                    
                except Exception as e:
                    print(e)
                    evosessionid = self.pegar_evosessionid()
                    continue
        
            except Exception as e:
                print(e)
                #print('ERRO NO PRIMEIRO TRY DA FUNÇÃO PEGAR DADOS')
                continue


    def gravar_dados_txt(self, lista_resultados):

        with open('arquivos_txt/resultados.txt', 'w', encoding='UTF-8') as arquivo:
            arquivo.write(str(lista_resultados))

        with open('arquivos_txt/resultados_bot.txt', 'w', encoding='UTF-8') as arquivo:
            arquivo.write(str(lista_resultados))


    def run(self):
        self.inicio()
        self.coletarDados()


class EnviaSinalTelegram(threading.Thread):

    def __init__(self, chat_id, markup, solicitacao_usuario):

        self.chatid = chat_id
        self.markup = markup
        self.tipo_sinal_usuario = solicitacao_usuario
        
        threading.Thread.__init__(self)


    def envia_menssagem(self, chat_id, texto, markup):

        try:

            message = bot.send_message(chat_id, texto, parse_mode='HTML', disable_web_page_preview=True, reply_markup=markup)

            return message
        
        except:

            error = bot.send_message(chat_id, "🤖 Algo deu Errado na Solicitação. Tente novamente mais tarde.", parse_mode='HTML', disable_web_page_preview=True, reply_markup=markup)


    def responde_mensagem(self, chat_id, texto, markup):

        mensagem = bot.reply_to(globals()[f'sinal_{chat_id}'], texto, parse_mode='HTML', disable_web_page_preview=True, reply_markup=markup)
        
        return mensagem


    def analisa_estrategias(self):

        while True:

            ### Lendo txt de estrategias
            lista_estrategias = ler_arquivo_txt('estrategias.txt')

            for key, value in lista_estrategias.items():
                
                try:

                    with open('arquivos_txt/resultados.txt', 'r', encoding='UTF-8') as arquivo_resultados:
                        ultimos_resultados = ast.literal_eval(arquivo_resultados.read())

                    sequencia_minima_sinal = len(value)-2

                    if value[:sequencia_minima_sinal] == ultimos_resultados[-sequencia_minima_sinal:] and\
                       value[-1] == '1' and self.tipo_sinal_usuario == 'Solicitar Entrada Premium 🎲' or\
                       value[:sequencia_minima_sinal] == ultimos_resultados[-sequencia_minima_sinal:] and\
                       value[-1] == '2' and self.tipo_sinal_usuario == 'Solicitar Entrada 🎲':
                        
                        ultimo_resultado = ultimos_resultados[-1]
                        aposta = value[-2]
                        globals()[f'sinal_{self.chatid}'] = self.envia_menssagem(self.chatid, msg_sinal.replace('[NOME_ESTRATEGIA]', key.title())\
                                                                                                       .replace('[ULTIMO_RESULTADO]', '🔵' if ultimo_resultado == 'P' else '🔴' if ultimo_resultado == 'B' else '🟡')\
                                                                                                       .replace('[APOSTA]', '🔵' if aposta == 'P' else '🔴' if aposta == 'B' else '🟡')\
                                                                                                       .replace('[GALE]', '1 Gale' if value[-1] == '1' else '2 Gales'),\
                                                                                                        self.markup)
                        time.sleep(10)
                        self.check_sinal_enviado(key, value, ultimos_resultados)
                        return
                        
            
                except Exception as e:
                    #print(e)
                    time.sleep(1)
        

    def check_sinal_enviado(self, nome_da_estrategia, estrategia, ultimos_resultados):
        
        contador_cash = 0
        gale = int(estrategia[-1])
        resultado_valida_sinal = []
        nome_estrategia = nome_da_estrategia

        while contador_cash <= gale:

            try:
                with open('arquivos_txt/resultados.txt', 'r', encoding='UTF-8') as arquivo_resultados:
                    resultados = ast.literal_eval(arquivo_resultados.read())


                if ultimos_resultados != resultados:
                    if resultados[-1] == 'T':
                        resultado_valida_sinal.append('🟡')

                    if resultados[-1] == 'B':
                        resultado_valida_sinal.append('🔴')
                    
                    if resultados[-1] == 'P':
                        resultado_valida_sinal.append('🔵')

                        
                    # VALIDANDO WIN OU LOSS
                    if resultados[-1] == estrategia[-2] or resultados[-1] == 'T':
                    
                        # Editando mensagem enviada
                        try:

                            try:
                                if contador_cash == 0:
                                    resposta = self.responde_mensagem(self.chatid, msg_green.replace('[LISTA_RESULTADOS]', ' '.join(resultado_valida_sinal))\
                                                                                .replace('[NOME_ESTRATEGIA]', nome_estrategia), self.markup)
                                
                                elif contador_cash == 1:

                                    bot.delete_message(self.chatid, globals()[f'gale1_{self.chatid}'].message_id)
                                    resposta = self.responde_mensagem(self.chatid, msg_green.replace('[LISTA_RESULTADOS]', ' '.join(resultado_valida_sinal))\
                                                                                .replace('[NOME_ESTRATEGIA]', nome_estrategia), self.markup)
                               
                                elif contador_cash == 2:

                                    #bot.delete_message(self.chatid, globals()[f'gale1_{self.chatid}'].message_id)
                                    bot.delete_message(self.chatid, globals()[f'gale2_{self.chatid}'].message_id)
                                    resposta = self.responde_mensagem(self.chatid, msg_green.replace('[LISTA_RESULTADOS]', ' '.join(resultado_valida_sinal))\
                                                                                .replace('[NOME_ESTRATEGIA]', nome_estrategia), self.markup)
                                

                                time.sleep(0.1)

                            except:
                                pass
                        
                
                        except:
                            pass
                        

                        contador_cash = 0
                        remover_solicitacao_entrada(self.chatid)
                        return

                
                    else:
                        if contador_cash == 0:

                            globals()[f'gale1_{self.chatid}'] = self.responde_mensagem(self.chatid, msg_gale1, self.markup)

                        elif contador_cash == 1:

                            bot.delete_message(self.chatid, globals()[f'gale1_{self.chatid}'].message_id)
                            globals()[f'gale2_{self.chatid}'] = self.responde_mensagem(self.chatid, msg_gale2, self.markup)
                        
                        contador_cash+=1
                        ultimos_resultados = resultados
                        continue
                
           
            except Exception as e:
                #print(e)
                continue

        if contador_cash > gale :
            
            try:
                
                bot.delete_message(self.chatid, globals()[f'gale2_{self.chatid}'].message_id)
                resposta = self.responde_mensagem(self.chatid, msg_red.replace('[LISTA_RESULTADOS]', ' '.join(resultado_valida_sinal))\
                                                                            .replace('[NOME_ESTRATEGIA]', nome_estrategia), self.markup)
                time.sleep(0.1)

            except:
                pass
            
            
            contador_cash = 0
            remover_solicitacao_entrada(self.chatid)
            return


    def run(self):
        global msg_sinal, msg_sem_gale, msg_gale1, msg_sem_gale, msg_gale2,msg_green,msg_red

        msg_analisando = ler_arquivo_txt('analisando.txt')
        msg_sinal = ler_arquivo_txt('sinal.txt')
        msg_green = ler_arquivo_txt('msg_green.txt')
        msg_gale1 = ler_arquivo_txt('msg_gale1.txt')
        msg_gale2 = ler_arquivo_txt('msg_gale2.txt')
        msg_red = ler_arquivo_txt('msg_red.txt')
        analise = self.envia_menssagem(self.chatid, msg_analisando, self.markup)
        self.analisa_estrategias()


class MapearResultados(threading.Thread):
    def __init__(self):

        threading.Thread.__init__(self)


    def analisa_estrategias(self):


        while True:

            ### Lendo txt de estrategias
            lista_estrategias = ler_arquivo_txt('estrategias_bot.txt')

            for key, value in lista_estrategias.items():
                
                try:

                    with open('arquivos_txt/resultados_bot.txt', 'r', encoding='UTF-8') as arquivo_resultados:
                        ultimos_resultados = ast.literal_eval(arquivo_resultados.read())

                    sequencia_minima_sinal = len(value)-2

                    if value[:sequencia_minima_sinal] == ultimos_resultados[-sequencia_minima_sinal:] and\
                       value[-1] == '1' or\
                       value[:sequencia_minima_sinal] == ultimos_resultados[-sequencia_minima_sinal:] and\
                       value[-1] == '2':
                        
                        print('Sinal enviado -- ')

                        time.sleep(10)
                        self.check_sinal_enviado(key, value, ultimos_resultados)
                        
            
                except Exception as e:
                    #print(e)
                    time.sleep(1)
        

    def check_sinal_enviado(self, nome_da_estrategia, estrategia, ultimos_resultados):
        global placar_win, placar_gale1, placar_semGale, placar_geral, placar_gale1, placar_gale2, placar_loss,\
               placar_win_mensal, placar_gale1_mensal, placar_semGale_mensal, placar_geral_mensal, placar_gale1_mensal, placar_gale2_mensal, placar_loss_mensal

        contador_cash = 0
        gale = int(estrategia[-1])
        resultado_valida_sinal = []
        nome_estrategia = nome_da_estrategia

        while contador_cash <= gale:

            try:
                with open('arquivos_txt/resultados_bot.txt', 'r', encoding='UTF-8') as arquivo_resultados:
                    resultados = ast.literal_eval(arquivo_resultados.read())

                if ultimos_resultados != resultados:
                    
                    # VALIDANDO WIN OU LOSS
                    if resultados[-1] == estrategia[-2] or resultados[-1] == 'T':
                    
                        # validando o tipo de WIN
                        if contador_cash == 0:
                            
                            # Atualizando placar e Alimentando o arquivo txt
                            placar_win +=1
                            placar_semGale +=1
                            placar_geral = placar_win + placar_loss

                            placar_win_mensal +=1
                            placar_semGale_mensal +=1
                            placar_geral_mensal = placar_win_mensal + placar_loss_mensal
                            

                            with open(f"placar/diario/{data_hoje}.txt", 'w') as arquivo:
                                arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}")
                            
                            with open(f"placar/mensal/{mes_hoje}.txt", 'w') as arquivo:
                                arquivo.write(f"win,{placar_win_mensal}\nsg,{placar_semGale_mensal}\ng1,{placar_gale1_mensal}\ng2,{placar_gale2_mensal}\nloss,{placar_loss_mensal}\nass,{str(round(placar_win_mensal / (placar_geral_mensal)*100, 0)).replace('.0','')}")
                            
                            self.atualizar_placares(nome_estrategia, 0)


                        if contador_cash == 1:
                    
                            # Atualizando placar e Alimentando o arquivo txt
                            placar_win +=1
                            placar_gale1 +=1
                            placar_geral = placar_win + placar_loss

                            placar_win_mensal +=1
                            placar_semGale_mensal +=1
                            placar_geral_mensal = placar_win_mensal + placar_loss_mensal
                            

                            with open(f"placar/diario/{data_hoje}.txt", 'w') as arquivo:
                                arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}")
                            
                            with open(f"placar/mensal/{mes_hoje}.txt", 'w') as arquivo:
                                arquivo.write(f"win,{placar_win_mensal}\nsg,{placar_semGale_mensal}\ng1,{placar_gale1_mensal}\ng2,{placar_gale2_mensal}\nloss,{placar_loss_mensal}\nass,{str(round(placar_win_mensal / (placar_geral_mensal)*100, 0)).replace('.0','')}")
                            
                            self.atualizar_placares(nome_estrategia, 1)


                        if contador_cash == 2:
                            
                            # Atualizando placar e Alimentando o arquivo txt
                            placar_win +=1
                            placar_gale2 +=1
                            placar_geral = placar_win + placar_loss

                            placar_win_mensal +=1
                            placar_semGale_mensal +=1
                            placar_geral_mensal = placar_win_mensal + placar_loss_mensal
                            

                            with open(f"placar/diario/{data_hoje}.txt", 'w') as arquivo:
                                arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}")
                            
                            with open(f"placar/mensal/{mes_hoje}.txt", 'w') as arquivo:
                                arquivo.write(f"win,{placar_win_mensal}\nsg,{placar_semGale_mensal}\ng1,{placar_gale1_mensal}\ng2,{placar_gale2_mensal}\nloss,{placar_loss_mensal}\nass,{str(round(placar_win_mensal / (placar_geral_mensal)*100, 0)).replace('.0','')}")
                            
                            self.atualizar_placares(nome_estrategia, 2)

                
                        contador_cash = 0
                        return

                
                    else:
                        contador_cash+=1
                        ultimos_resultados = resultados
                        continue
                
           
            except Exception as e:
                #print(e)
                continue

        if contador_cash > gale :

            # Preenchendo arquivo txt
            placar_loss +=1
            placar_geral = placar_win + placar_loss
            
            placar_loss_mensal +=1
            placar_geral_mensal = placar_win_mensal + placar_loss_mensal
            
            with open(f"placar/diario/{data_hoje}.txt", 'w') as arquivo:
                arquivo.write(f"win,{placar_win}\nsg,{placar_semGale}\ng1,{placar_gale1}\ng2,{placar_gale2}\nloss,{placar_loss}\nass,{str(round(placar_win / (placar_geral)*100, 0)).replace('.0','')}")


            with open(f"placar/mensal/{mes_hoje}.txt", 'w') as arquivo:
                arquivo.write(f"win,{placar_win_mensal}\nsg,{placar_semGale_mensal}\ng1,{placar_gale1_mensal}\ng2,{placar_gale2_mensal}\nloss,{placar_loss_mensal}\nass,{str(round(placar_win_mensal / (placar_geral_mensal)*100, 0)).replace('.0','')}")
                                       
            
            self.atualizar_placares(nome_estrategia, 3)

            contador_cash = 0
            return


    def atualizar_placares(self, estrategia, gale):

        # Atualizando placar_estrategia e Alimentando o arquivo TXT
        lista_placar_estrategias_diario = open(f'placar estrategias/diario/{data_hoje}.txt', 'r', encoding='UTF-8').read()
        lista_placar_estrategias_mensal = open(f'placar estrategias/mensal/{mes_hoje}.txt', 'r', encoding='UTF-8').read()
        lista_placar_estrategias_diario = ast.literal_eval(lista_placar_estrategias_diario)
        lista_placar_estrategias_mensal = ast.literal_eval(lista_placar_estrategias_mensal)

        try:

            # Somando Win no placar diario da estratégia
            for key, value in lista_placar_estrategias_diario.items():
                if key == estrategia:
                    value[gale] = int(value[gale])+1
                    break
            
            ## Atualizando o TXT de placar diario
            with open(f'placar estrategias/diario/{data_hoje}.txt', 'w', encoding='UTF-8') as file:
                file.write(str(lista_placar_estrategias_diario))
                file.close()

        except:
            pass

        try:
            # Somando Win no placar mensal da estratégia
            for key, value in lista_placar_estrategias_mensal.items():
                if key == estrategia:
                    value[gale] = int(value[gale])+1
                    break

            ## Atualizando o TXT de placar mensal
            with open(f'placar estrategias/mensal/{mes_hoje}.txt', 'w', encoding='UTF-8') as file:
                file.write(str(lista_placar_estrategias_mensal))
                file.close()


        except:
            pass

    

    def run(self):

        self.analisa_estrategias()




def chama_markup(id_usuario):

    lista_assinantes = ler_arquivo_txt('assinantes.txt')

    if str(id_usuario) in ids_masters:

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup_master = markup.add('/start',
                            '⚙ Cadastrar Estratégia',
                            '📜 Estratégias Cadastradas',
                            '🗑 Apagar Estratégia',
                            'Solicitar Entrada 🎲',
                            'Solicitar Entrada Premium 🎲',
                            '📊 Placar Atual')

        return markup_master

    elif str(id_usuario) in lista_assinantes:
        
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup_assinantes = markup.add('Solicitar Entrada 🎲',
                            'Solicitar Entrada Premium 🎲')

        return markup_assinantes
        

def valida_qntd_entradas(id_usuario, entrada_andamento):
    global contador, id_usuario_2

    id_usuario_2 = id_usuario
    lista_contador_entradas = os.listdir('contagem_entrada')    

    ###VALIDA SE O CHAT ID NÃO ESTÁ NA RELAÇÃO
    if f'{str(id_usuario)}.txt' not in lista_contador_entradas:
        with open(f'contagem_entrada/{id_usuario}.txt', 'w', encoding='UTF-8') as arq_usuario:
            arq_usuario.write('1')
            arq_usuario.close()

        enviar_entrada(id_usuario)

    elif f'{str(id_usuario)}.txt' in lista_contador_entradas:
        with open(f'contagem_entrada/{id_usuario}.txt', 'r', encoding='UTF-8') as arq_usuario:
            contador = arq_usuario.read()

            if int(contador) == 3:
                #Init keyboard markup
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
                markup = markup.add('SIM','NÃO','◀ Voltar')

                with open ('arquivos_txt/msg_aviso_sinal.txt', 'r', encoding='UTF-8') as file:
                    msg = file.read()

                mensagem_aviso = bot.send_message(id_usuario, msg, parse_mode='HTML', reply_markup=markup)
                bot.register_next_step_handler(mensagem_aviso, valida_resposta_usuario)

                return
            

            else:
                contador = int(contador)+1
                with open(f'contagem_entrada/{id_usuario}.txt', 'w', encoding='UTF-8') as arq_usuario:
                    arq_usuario.write(str(contador))
                    arq_usuario.close()
                
                enviar_entrada(id_usuario)
                
                
def valida_resposta_usuario(mensagem_aviso):
    global contador

    if mensagem_aviso.text == 'SIM':
        
        contador = int(contador)+1
        with open(f'contagem_entrada/{id_usuario_2}.txt', 'w', encoding='UTF-8') as arq_usuario:
            arq_usuario.write(str(contador))
            arq_usuario.close()
        
        enviar_entrada(id_usuario_2)
        

    elif mensagem_aviso.text == '◀ Voltar' or mensagem_aviso.text == 'NÃO' :

        lista_assinantes = ler_arquivo_txt('assinantes.txt')

        if str(mensagem_aviso.chat.id) in ids_masters:
        
                #Init keyboard markup
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                markup = markup.add('/start',
                                    '⚙ Cadastrar Estratégia',
                                    '📜 Estratégias Cadastradas',
                                    '🗑 Apagar Estratégia',
                                    'Solicitar Entrada 🎲',
                                    'Solicitar Entrada Premium 🎲',
                                    '📊 Placar Atual')

                
                remover_solicitacao_entrada(mensagem_aviso.chat.id)

                message_opcoes = bot.reply_to(mensagem_aviso, f"🤖 Escolha uma opção 👇",
                                        reply_markup=markup)
                
                #Here we assign the next handler function and pass in our response from the user. 
                bot.register_next_step_handler(message_opcoes, opcoes)
        

        elif str(mensagem_aviso.chat.id) in lista_assinantes:
            
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add(   
                                'Solicitar Entrada 🎲',
                                'Solicitar Entrada Premium 🎲')

            
            remover_solicitacao_entrada(mensagem_aviso.chat.id)

            message_opcoes = bot.reply_to(mensagem_aviso, f"🤖 Escolha uma opção 👇",
                                    reply_markup=markup)
            
            #Here we assign the next handler function and pass in our response from the user. 
            bot.register_next_step_handler(message_opcoes, opcoes)


#ZERANDO A CONTAGEM DE ENTRADA DO DIA
def zerar_contagem_entrada():
    try:
        contagem_solicitacoes = os.listdir('contagem_entrada')

        if contagem_solicitacoes == []:
            pass
        
        for arquivo in contagem_solicitacoes: 
            os.remove(f'contagem_entrada/{arquivo}')

    except:
        pass
    

# GERA TXT DO PLACAR DIÁRIO
def placar_diario():
    global placar_win
    global placar_semGale
    global placar_gale1
    global placar_gale2
    global placar_loss
    global placar_geral
    global asserividade
    global data_hoje

    data_hoje = datetime.today().strftime('%d-%m-%Y')
    arquivos_placares = os.listdir(r"placar/diario")
    arquivos_placar_estrategia = os.listdir(r"placar estrategias/diario")

    if f'{data_hoje}.txt' in arquivos_placares:
        # Carregar arquivo de placar
        with open(f"placar/diario/{data_hoje}.txt", 'r') as arquivo:
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
        with open(f"placar/diario/{data_hoje}.txt", 'w') as arquivo:
            arquivo.write("win,0\nsg,0\ng1,0\ng2,0\nloss,0\nass,0")

        # Ler o arquivo de placar criado
        with open(f"placar/diario/{data_hoje}.txt", 'r') as arquivo:
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

    
    ###### PLACAR DAS ESTRATEGIAS
    if f'{data_hoje}.txt' in arquivos_placar_estrategia:
        pass

    else:
        dict_placar_estrategias = {}
        dict_temporario = {} 
        arquivo_estrategias = ler_arquivo_txt('estrategias.txt')

        for key, value in arquivo_estrategias.items():

            dict_placar_estrategias[key] = [0,0,0,0,0]
            dict_temporario.update(dict_placar_estrategias)

        # Criar um arquivo com a data atual
        with open(f"placar estrategias/diario/{data_hoje}.txt", 'w') as arquivo:
            arquivo.write(str(dict_temporario))
            arquivo.close()


# GERA TXT DO PLACAR MENSAL
def placar_mensal():
    global placar_win_mensal
    global placar_semGale_mensal
    global placar_gale1_mensal
    global placar_gale2_mensal
    global placar_loss_mensal
    global placar_geral_mensal
    global asserividade_mensal
    global mes_hoje

    mes_hoje = datetime.today().strftime('%m-%Y')
    arquivos_placares = os.listdir(r"placar/mensal")
    arquivos_placar_estrategia = os.listdir(r"placar estrategias/mensal")


    if f'{mes_hoje}.txt' in arquivos_placares:
        # Carregar arquivo de placar
        with open(f"placar/mensal/{mes_hoje}.txt", 'r') as arquivo:
            try:

                arq_placar = arquivo.readlines()
                placar_win_mensal = int(arq_placar[0].split(',')[1])
                placar_semGale_mensal = int(arq_placar[1].split(',')[1])
                placar_gale1_mensal = int(arq_placar[2].split(',')[1])
                placar_gale2_mensal = int(arq_placar[3].split(',')[1])
                placar_loss_mensal = int(arq_placar[4].split(',')[1])
                placar_geral_mensal = int(placar_win_mensal) + int(placar_loss_mensal)
                asserividade_mensal = arq_placar[5].split(',')[1]+"%"
            
            except:
                pass

            
    else:
        # Criar um arquivo com a data atual
        with open(f"placar/mensal/{mes_hoje}.txt", 'w') as arquivo:
            arquivo.write("win,0\nsg,0\ng1,0\ng2,0\nloss,0\nass,0")

        # Ler o arquivo de placar criado
        with open(f"placar/mensal/{mes_hoje}.txt", 'r') as arquivo:
            try:

                arq_placar = arquivo.readlines()
                placar_win_mensal = int(arq_placar[0].split(',')[1])
                placar_semGale_mensal = int(arq_placar[1].split(',')[1])
                placar_gale1_mensal = int(arq_placar[2].split(',')[1])
                placar_gale2_mensal = int(arq_placar[3].split(',')[1])
                placar_loss_mensal = int(arq_placar[4].split(',')[1])
                placar_geral_mensal = int(placar_win_mensal) + int(placar_loss_mensal)
                asserividade_mensal = arq_placar[5].split(',')[1]+"%"
            
            except:
                pass


    ###### PLACAR DAS ESTRATEGIAS
    if f'{mes_hoje}.txt' in arquivos_placar_estrategia:
        pass

    else:
        dict_placar_estrategias = {}
        dict_temporario = {} 
        arquivo_estrategias = ler_arquivo_txt('estrategias.txt')

        for key, value in arquivo_estrategias.items():

            dict_placar_estrategias[key] = [0,0,0,0,0]
            dict_temporario.update(dict_placar_estrategias)

        # Criar um arquivo com a data atual
        with open(f"placar estrategias/mensal/{mes_hoje}.txt", 'w') as arquivo:
            arquivo.write(str(dict_temporario))
            arquivo.close()


# VALIDADOR DE DATA
def validaData():
    global data_resultado
    global reladiarioenviado
    global horario_atual, proximo_mes, mes_atual

    data_hoje = datetime.today()

    try:
        proximo_mes = proximo_mes.strftime('%m/%Y')
    except:pass

    subtrai_dia = timedelta(days=-1)
    data_ontem = data_hoje + subtrai_dia
    data_resultado = data_ontem.strftime('%d/%m/%Y')
    horario_atual = datetime.today().strftime('%H:%M')

    # Condição que zera o placar quando o dia muda
    if horario_atual == '00:00' and reladiarioenviado == 0:
        placar_diario()
        zerar_contagem_entrada()
        reladiarioenviado +=1

    # Condição que zera o placar quando o dia muda
    if horario_atual == '00:01' and reladiarioenviado == 1:
        reladiarioenviado = 0

    #Condição que zera o placar do mês
    if mes_atual.strftime('%m/%Y') == proximo_mes:
        placar_mensal()
        time.sleep(1)
        mes_atual = datetime.today()
        soma_mes =  timedelta(days=35)
        proximo_mes = mes_atual+soma_mes
        

def ler_arquivo_txt(arquivo):

    with open(f'arquivos_txt/{arquivo}', 'r', encoding='UTF-8') as file:

        dados = file.read()

        if arquivo == 'api_bot_telegram.txt':
            lista_dados = dados

        elif '{' in dados and '}' in dados:
            lista_dados = ast.literal_eval(dados)

        elif dados == '':

            lista_dados = ''
        
        elif ',' in dados:
        
            lista_dados = dados.split(',') 


        else:
            lista_dados = dados
            
    return lista_dados


def bot_telegram(token):

    bot = telebot.TeleBot(token)

    return bot


def generate_buttons_estrategias(bts_names, markup):
    for button in bts_names:
        markup.add(types.KeyboardButton(button))
    return markup


def valida_solicitacao_entrada(id):

    registro_solicitacoes_entrada = os.listdir('pedidos_entrada')

    if registro_solicitacoes_entrada != []:

        if f'{str(id)}.txt' in registro_solicitacoes_entrada:
            
            markup = chama_markup(id)
            bot.send_message(id, "Aguarde mais um pouco, Robô analisando o Mercado.🤖", reply_markup=markup)

            return True

        else:
        
            pedido = str(id)

        with open(f'pedidos_entrada/{pedido}.txt', 'w', encoding='UTF-8') as arq_pedidos:

            arq_pedidos.close()

        return False
                        
    else:
            
        pedido = str(id)

        with open(f'pedidos_entrada/{pedido}.txt', 'w', encoding='UTF-8') as arq_pedidos:

            arq_pedidos.close()

        return False
            

def remover_solicitacao_entrada(id):
    
    lista_solicitacoes = os.listdir('pedidos_entrada')

    try:
        if lista_solicitacoes == []:
            pass
        
        elif f'{str(id)}.txt' in lista_solicitacoes:
            os.remove(f'pedidos_entrada/{str(id)}.txt')

    except:
        pass


def enviar_entrada(id_usuario):
    
    lista_assinantes = os.listdir('usuarios')
    usuario_validado = None
    perfil_usuario = None

    if str(id_usuario) in ids_masters:
    
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup_master = markup.add('/start',
                                '⚙ Cadastrar Estratégia',
                                '📜 Estratégias Cadastradas',
                                '🗑 Apagar Estratégia',
                                'Solicitar Entrada 🎲',
                                'Solicitar Entrada Premium 🎲',
                                '📊 Placar',
                                '📈 Gestão Estratégia')

            EnviaSinalTelegram(id_usuario, markup_master, solicitacao_usuario).start()

            print(f'{datetime.now().strftime("%H:%M")} ----- Master {id_usuario} Solicitou uma Entrada.')

            return

    
    for assinante in lista_assinantes:

        with open(f'usuarios/{assinante}', 'r', encoding='UTF-8') as file_assinante:
            dados_assinante = file_assinante.read()
            dados_assinante = ast.literal_eval(dados_assinante)
        
        for key, value in dados_assinante.items():
            if key==str(id_usuario):
                usuario_validado = True
                perfil_usuario = value
                break
        
        
    if usuario_validado == True and perfil_usuario == 'premium':

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup_premium = markup.add(   
                            'Solicitar Entrada 🎲',
                            'Solicitar Entrada Premium 🎲')

        EnviaSinalTelegram(id_usuario, markup_premium, solicitacao_usuario).start()


    elif usuario_validado == True and perfil_usuario == 'basico':

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup_basico = markup.add(   
                            'Solicitar Entrada 🎲'
                            )

        EnviaSinalTelegram(id_usuario, markup_basico, solicitacao_usuario).start()


    elif usuario_validado == True and perfil_usuario == 'bloqueado':

        bot.send_message(id_usuario, 
                                        f"🤖 Infelizmente você está bloqueado para usar a IA. Procure o Suporte e ative/renove seu acesso!")


    else:

        message_error = bot.send_message(id_usuario,  "🤖 Você não tem permissão para acessar este Bot ❌🚫")


    print(f'{datetime.now().strftime("%H:%M")} ----- {id_usuario} Solicitou uma Entrada.')


def registra_estrategia(message_estrategia):

    try:
    
        nova_estrategia = {}
        lista_temporaria = []
        lista_estrategias = ler_arquivo_txt('estrategias.txt')
        resp_usuario = message_estrategia.text.split(':')
        
        for i in resp_usuario[1]:
            if i != ',':
                lista_temporaria.append(i)

        nova_estrategia[resp_usuario[0]] = lista_temporaria

        lista_estrategias.update(nova_estrategia)

        ###ATUALIZANDO ARQUIVO ESTRATEGIAS
        with open('arquivos_txt/estrategias.txt', 'w', encoding='UTF-8') as file:
            file.write(str(lista_estrategias))
            file.close()

        with open('arquivos_txt/estrategias_bot.txt', 'w', encoding='UTF-8') as file:
            file.write(str(lista_estrategias))
            file.close()

        #ATUALIZANDO ARQUIVO PLACAR DAS ESTRATEGIAS
        registra_placar_estrategia(resp_usuario[0])

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start',
                                '⚙ Cadastrar Estratégia',
                                '📜 Estratégias Cadastradas',
                                '🗑 Apagar Estratégia',
                                'Solicitar Entrada 🎲',
                                'Solicitar Entrada Premium 🎲',
                                '📊 Placar',
                                '📈 Gestão Estratégia')

        success = bot.reply_to(message_estrategia, "✅ Estratégia Cadastrada com Sucesso!")

    except:

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start',
                                '⚙ Cadastrar Estratégia',
                                '📜 Estratégias Cadastradas',
                                '🗑 Apagar Estratégia',
                                'Solicitar Entrada 🎲',
                                'Solicitar Entrada Premium 🎲',
                                '📊 Placar',
                                '📈 Gestão Estratégia')

        message_erro = bot.reply_to(message_estrategia, "🤖❌ Algo deu Errado. Tente Novamente.", reply_markup=markup)


def registra_placar_estrategia(nome_estrategia):

    try:

        dict_placar_estrategia = {}
        lista_placar_estrategias_diario = open(f'/placar estrategias/diario/{data_hoje}.txt', 'r', encoding='UTF-8').read()
        lista_placar_estrategias_mensal = open(f'/placar estrategias/mensal/{mes_hoje}.txt', 'r', encoding='UTF-8').read()
        lista_placar_estrategias_diario = ast.literal_eval(lista_placar_estrategias_diario)
        lista_placar_estrategias_mensal = ast.literal_eval(lista_placar_estrategias_mensal)

        dict_placar_estrategia[nome_estrategia[0]] = [0,0,0,0,0]

        lista_placar_estrategias_diario.update(dict_placar_estrategia)
        lista_placar_estrategias_mensal.update(dict_placar_estrategia)

        ###ATUALIZANDO ARQUIVO PLACAR ESTRATEGIAS DIARIO
        with open(f'/placar estrategias/diario/{data_hoje}.txt', 'w', encoding='UTF-8') as file:
            file.write(str(lista_placar_estrategias_diario))
            file.close()

        ###ATUALIZANDO ARQUIVO PLACAR ESTRATEGIAS MENSAL
        with open(f'/placar estrategias/mensal/{mes_hoje}.txt', 'w', encoding='UTF-8') as file:
            file.write(str(lista_placar_estrategias_mensal))
            file.close()

    except Exception as e:
        print(e)
        

def registrar_estrategia_excluida(message_excluir_estrategia):
    
    try:

        if message_excluir_estrategia.text == '◀ Voltar':
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start',
                                '⚙ Cadastrar Estratégia',
                                '📜 Estratégias Cadastradas',
                                '🗑 Apagar Estratégia',
                                'Solicitar Entrada 🎲',
                                'Solicitar Entrada Premium 🎲',
                                '📊 Placar',
                                '📈 Gestão Estratégia')

            menu_inicial = bot.reply_to(message_excluir_estrategia, "Escolha uma opção 👇", reply_markup=markup)

            

        else:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start',
                                    '⚙ Cadastrar Estratégia',
                                    '📜 Estratégias Cadastradas',
                                    '🗑 Apagar Estratégia',
                                    'Solicitar Entrada 🎲',
                                    'Solicitar Entrada Premium 🎲',
                                    '📊 Placar Atual')


            ############## EXCLUINDO ESTRATEGIA ##############
            lista_estrategias = ler_arquivo_txt('estrategias.txt')
            resp_usuario = message_excluir_estrategia.text

            for key, value in lista_estrategias.items():
                if resp_usuario == key:
                    lista_estrategias.pop(key)
                    break

            ###ATUALIZANDO ARQUIVO ESTRATEGIAS
            with open('arquivos_txt/estrategias.txt', 'w', encoding='UTF-8') as file:
                file.write(str(lista_estrategias))
                file.close()

            with open('arquivos_txt/estrategias_bot.txt', 'w', encoding='UTF-8') as file:
                file.write(str(lista_estrategias))
                file.close()

            ############## EXCLUINDO PLACAR DA ESTRATEGIA ##############
            lista_placar_estrategias_diario = open(f'/placar estrategias/diario/{data_hoje}.txt', 'r', encoding='UTF-8')
            lista_placar_estrategias_diario = ast.literal_eval(lista_placar_estrategias_diario)

            for key, value in lista_placar_estrategias_diario.items():
                if resp_usuario == key:
                    lista_placar_estrategias_diario.pop(key)
                    break

            ###ATUALIZANDO ARQUIVO PLACAR ESTRATEGIAS
            with open(f'/placar estrategias/diario/{data_hoje}.txt', 'w', encoding='UTF-8') as file:
                file.write(str(lista_placar_estrategias_diario))
                file.close()
            
            
            success = bot.reply_to(message_excluir_estrategia, "✅ Estratégia Excluída com Sucesso!", reply_markup=markup)


    except:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start',
                                '⚙ Cadastrar Estratégia',
                                '📜 Estratégias Cadastradas',
                                '🗑 Apagar Estratégia',
                                'Solicitar Entrada 🎲',
                                'Solicitar Entrada Premium 🎲',
                                '📊 Placar',
                                '📈 Gestão Estratégia')

        
        message_erro = bot.reply_to(message_excluir_estrategia, "🤖❌ Algo deu Errado. Tente Novamente.", reply_markup=markup)


def liberar_acesso(message_novo_cliente):
    try:
        dado_novo_usuario = {}
        usuario_id = str(message_novo_cliente.chat.id)
        usuario_email = message_novo_cliente.text
        tipo_acesso = 'basico'
        dado_novo_usuario[usuario_id] = tipo_acesso

        #REGISTRANDO USUARIO NO ARQUIVO
        lista_usuarios = os.listdir('usuarios')

        if usuario_email not in lista_usuarios:
            with open(f'usuarios/{usuario_email}.txt', 'w', encoding='UTF-8') as arq_usuario:
                arq_usuario.write(str(dado_novo_usuario))
                arq_usuario.close()

            with open(f'novos usuarios/{usuario_email}.txt', 'w', encoding='UTF-8') as arq_usuario:
                arq_usuario.write(str(dado_novo_usuario))
                arq_usuario.close()

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add(   
                            'Solicitar Entrada 🎲')

           
        message_opcoes = bot.reply_to(message_novo_cliente, f"🤖 Acesso Liberado com Sucesso! Escolha uma opção 👇",
                                reply_markup=markup)
        
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(message_opcoes, opcoes)

    
    except Exception as e:
        print(e)


def enviar_placar_periodo(escolher_periodo):
    try:

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start',
                                    '⚙ Cadastrar Estratégia',
                                    '📜 Estratégias Cadastradas',
                                    '🗑 Apagar Estratégia',
                                    'Solicitar Entrada 🎲',
                                    'Solicitar Entrada Premium 🎲',
                                    '📊 Placar',
                                    '📈 Gestão Estratégia')
        
        if escolher_periodo.text == 'DIÁRIO':
            placar_diario()

            texto_placar = open('arquivos_txt//texto_placar_diario.txt', 'r', encoding='UTF-8').read()

            resposta = bot.reply_to(escolher_periodo, texto_placar
                                            .replace('[DATA_ATUAL]', data_hoje)
                                            .replace('[TOTAL_WIN]', str(placar_win))
                                            .replace('[TOTAL_LOSS]', str(placar_loss))
                                            .replace('[TOTAL_SEM_GALE]', str(placar_semGale))
                                            .replace('[TOTAL_WIN_GALE]', str(placar_gale1+placar_gale2))
                                            .replace('[WIN_GALE_1]', str(placar_gale1))
                                            .replace('[WIN_GALE_2]', str(placar_gale2))
                                            .replace('[PORCENTAGEM]', asserividade)
                                            ,reply_markup=markup)
            

        elif escolher_periodo.text == 'MENSAL':
            placar_mensal()

            texto_placar = open('arquivos_txt//texto_placar_mensal.txt', 'r', encoding='UTF-8').read()

            resposta = bot.reply_to(escolher_periodo, texto_placar
                                            .replace('[MES_ATUAL]', mes_hoje)
                                            .replace('[TOTAL_WIN]', str(placar_win))
                                            .replace('[TOTAL_LOSS]', str(placar_loss))
                                            .replace('[TOTAL_SEM_GALE]', str(placar_semGale))
                                            .replace('[TOTAL_WIN_GALE]', str(placar_gale1+placar_gale2))
                                            .replace('[WIN_GALE_1]', str(placar_gale1))
                                            .replace('[WIN_GALE_2]', str(placar_gale2))
                                            .replace('[PORCENTAGEM]', asserividade)
                                            ,reply_markup=markup)


        
    except Exception as e:
        print(e)
        bot.send_message(escolher_periodo, "🤖⚠️ Algo inesperado aconteceu. Tente novamente")

            
def enviar_placar_estrategia(escolher_periodo):
    try:

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
        markup = markup.add('/start',
                                    '⚙ Cadastrar Estratégia',
                                    '📜 Estratégias Cadastradas',
                                    '🗑 Apagar Estratégia',
                                    'Solicitar Entrada 🎲',
                                    'Solicitar Entrada Premium 🎲',
                                    '📊 Placar',
                                    '📈 Gestão Estratégia')
        
        if escolher_periodo.text == 'DIÁRIO':

            lista_placar_estrategias = open(f'placar estrategias/diario/{data_hoje}.txt', 'r', encoding='UTF-8').read()
            lista_placar_estrategias = ast.literal_eval(lista_placar_estrategias)
            arquivo_temp = os.listdir(r"arquivos_txt")
            
            resposta = bot.reply_to(escolher_periodo, '🤖 Gerando relatório. Por favor aguarde.', reply_markup=markup)

            for key, value in lista_placar_estrategias.items():
                total = int(value[0]) + int(value[1]) + int(value[2]) + int(value[3])
                soma_win = int(value[0]) + int(value[1]) + int(value[2])
                texto_placar_estrategia = open('arquivos_txt/texto_placar_estrategias_diario.txt', 'r', encoding='UTF-8').read()

                try:
                    assertividade = str(round(soma_win / total*100, 1)).replace('.0',"")+"%"
                except:
                    assertividade = '0%'
                

                texto = texto_placar_estrategia\
                        .replace('[DATA_ATUAL]', data_hoje)\
                        .replace('[NOME_ESTRATEGIA]', key.upper())\
                        .replace('[TOTAL_WIN]', str(soma_win))\
                        .replace('[TOTAL_LOSS]', str(value[3]))\
                        .replace('[TOTAL_SEM_GALE]', str(value[0]))\
                        .replace('[TOTAL_WIN_GALE]', str(value[1]+value[2]))\
                        .replace('[WIN_GALE_1]', str(value[1]))\
                        .replace('[WIN_GALE_2]', str(value[2]))\
                        .replace('[PORCENTAGEM]', assertividade)+'\n\n'


                if 'temp.txt' in arquivo_temp:
                    with open('arquivos_txt/temp.txt', 'a', encoding='UTF-8') as file:
                        file.write(texto)
                        file.close()
                else:
                    with open('arquivos_txt/temp.txt', 'w', encoding='UTF-8') as file:
                        file.write(texto)
                        file.close()
                    
                    arquivo_temp = os.listdir(r"arquivos_txt")


            envio_documento = bot.send_document(escolher_periodo.json['from']['id'], open('arquivos_txt/temp.txt', 'rb'))

            #### APAGANDO O ARQUIVO TEMP
            for arquivo in arquivo_temp:
                if arquivo == 'temp.txt':
                    os.remove('arquivos_txt/temp.txt')

        
        elif escolher_periodo.text == 'MENSAL':

            lista_placar_estrategias = open(f'placar estrategias/mensal/{mes_hoje}.txt', 'r', encoding='UTF-8').read()
            lista_placar_estrategias = ast.literal_eval(lista_placar_estrategias)
            arquivo_temp = os.listdir(r"arquivos_txt")
            
            resposta = bot.reply_to(escolher_periodo, '🤖 Gerando relatório. Por favor aguarde.', reply_markup=markup)

            for key, value in lista_placar_estrategias.items():
                total = int(value[0]) + int(value[1]) + int(value[2]) + int(value[3])
                soma_win = int(value[0]) + int(value[1]) + int(value[2])
                texto_placar_estrategia = open('arquivos_txt/texto_placar_estrategias_mensal.txt', 'r', encoding='UTF-8').read()

                try:
                    assertividade = str(round(soma_win / total*100, 1)).replace('.0',"")+"%"
                except:
                    assertividade = '0%'
                

                texto = texto_placar_estrategia\
                        .replace('[MES_ATUAL]', mes_hoje)\
                        .replace('[NOME_ESTRATEGIA]', key.upper())\
                        .replace('[TOTAL_WIN]', str(soma_win))\
                        .replace('[TOTAL_LOSS]', str(value[3]))\
                        .replace('[TOTAL_SEM_GALE]', str(value[0]))\
                        .replace('[TOTAL_WIN_GALE]', str(value[1]+value[2]))\
                        .replace('[WIN_GALE_1]', str(value[1]))\
                        .replace('[WIN_GALE_2]', str(value[2]))\
                        .replace('[PORCENTAGEM]', assertividade)+'\n\n'


                if 'temp.txt' in arquivo_temp:
                    with open('arquivos_txt/temp.txt', 'a', encoding='UTF-8') as file:
                        file.write(texto)
                        file.close()
                else:
                    with open('arquivos_txt/temp.txt', 'w', encoding='UTF-8') as file:
                        file.write(texto)
                        file.close()
                    
                    arquivo_temp = os.listdir(r"arquivos_txt")
                

            envio_documento = bot.send_document(escolher_periodo.json['from']['id'], open('arquivos_txt/temp.txt', 'rb'))

            #### APAGANDO O ARQUIVO TEMP
            for arquivo in arquivo_temp:
                if arquivo == 'temp.txt':
                    os.remove('arquivos_txt/temp.txt')
                


    except:
        pass






if __name__=='__main__':

    print()
    print('                                #################################################################')
    print('                                #####################  BOT IA BAC BO ############################')
    print('                                #################################################################')
    print('                                ##################### SEJA BEM VINDO ############################')
    print('                                #################################################################')
    print('                                ############# DESENVOLVIDO POR VICTOR RODRIGUES #################')
    print('                                #################################################################\n')
    print('Versão = 1.0.0')
    print('Ambiente: Produção\n\n\n')


    print('INICIANDO COLETA DE RESULTADOS DA MESA BACBO....\n\n\n')

    #DEFININDO MÊS QUE ZERA O PLACAR
    mes_atual = datetime.today()
    soma_mes =  timedelta(days=30)
    proximo_mes = mes_atual+soma_mes

    reladiarioenviado = 0

    placar_diario()
    placar_mensal()

    PegarResultadosBacBo().start()
    MapearResultados().start()

    time.sleep(5)

    ids_masters = ler_arquivo_txt('ids_masters.txt')

    CHAVE_API = ler_arquivo_txt('api_bot_telegram.txt')

    bot = bot_telegram(CHAVE_API)

    print('REGISTRANDO COMANDOS SOLICITADOS PARA O BOT.....\n\n\n')





@bot.message_handler(commands=['📊 Placar'])
def placar_atual_geral(message):
    global resultados_sinais


    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup = markup.add('DIÁRIO','MENSAL')

    escolher_periodo = (bot.reply_to(message, '🤖 Opa! Escolha o período do placar', reply_markup=markup))

    bot.register_next_step_handler(escolher_periodo, enviar_placar_periodo)



@bot.message_handler(commands=['📈 Gestão_Estratégia'])
def placar_atual_estrategia(message):
    global resultados_sinais
    global placar_estrategias


    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    markup = markup.add('DIÁRIO','MENSAL')

    escolher_periodo = (bot.reply_to(message, '🤖 Opa! Escolha o período de análise', reply_markup=markup))

    bot.register_next_step_handler(escolher_periodo, enviar_placar_estrategia)


@bot.message_handler(commands=['⚙ Cadastrar_Estratégia'])
def cadastrarEstrategia(message):

    message_estrategia = bot.reply_to(message, "🤖 Insira a Estratégia Conforme Exemplo: \n\
                                                        nomeestrategia:P,P,P,P,B  👇")
    
    bot.register_next_step_handler(message_estrategia, registra_estrategia)
    
    
@bot.message_handler(commands=['🗑 Apagar_Estratégia'])
def apagarEstrategia(message):
    
    lista_estrategias = ler_arquivo_txt('estrategias.txt')
    
    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #Add to buttons by list with ours generate_buttons function.
    markup_estrategias = generate_buttons_estrategias([key for key, value in lista_estrategias.items()], markup)
    markup_estrategias.add('◀ Voltar')   

    message_excluir_estrategia = bot.reply_to(message, "🤖 Escolha a estratégia a ser excluída 👇", reply_markup=markup_estrategias)
    bot.register_next_step_handler(message_excluir_estrategia, registrar_estrategia_excluida)
    
    
@bot.message_handler(commands=['📜 Estrategias_Cadastradas'])
def estrategiasCadastradas(message):
    
    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup = markup.add('/start',
                            '⚙ Cadastrar Estratégia',
                            '📜 Estratégias Cadastradas',
                            '🗑 Apagar Estratégia',
                            'Solicitar Entrada 🎲',
                            'Solicitar Entrada Premium 🎲',
                            '📊 Placar Atual')

    bot.reply_to(message, "🤖 Ok! Listando estratégias", reply_markup=markup)

    lista_estrategias = ler_arquivo_txt('estrategias.txt')
    
    for key, value in lista_estrategias.items():
        #print(estrategia)
        bot.send_message(message.chat.id, f'{key}:{value}')


@bot.message_handler(commands=['start'])
def start(message):
        
    lista_assinantes = os.listdir('usuarios')
    usuario_validado = None
    perfil_usuario = None

    if str(message.chat.id) in ids_masters:
    
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start',
                                '⚙ Cadastrar Estratégia',
                                '📜 Estratégias Cadastradas',
                                '🗑 Apagar Estratégia',
                                'Solicitar Entrada 🎲',
                                'Solicitar Entrada Premium 🎲',
                                '📊 Placar',
                                '📈 Gestão Estratégia')

            message_opcoes = bot.reply_to(message, f"🤖 Olá Master {message.json['from']['first_name']}! Escolha uma opção 👇",
                                    reply_markup=markup)
            
            #Here we assign the next handler function and pass in our response from the user. 
            bot.register_next_step_handler(message_opcoes, opcoes)

            return

    
    ###VALIDANDO PERFIL DO USUARIO
    for assinante in lista_assinantes:

        with open(f'usuarios/{assinante}', 'r', encoding='UTF-8') as file_assinante:
            dados_assinante = file_assinante.read()
            dados_assinante = ast.literal_eval(dados_assinante)
        
        for key, value in dados_assinante.items():
            if key==str(message.chat.id):
                usuario_validado = True
                perfil_usuario = value
                break
        

    if usuario_validado == True and perfil_usuario == 'premium':

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add(   
                            'Solicitar Entrada 🎲',
                            'Solicitar Entrada Premium 🎲')

        message_opcoes = bot.reply_to(message, f"🤖 Olá {message.json['from']['first_name']}! Escolha uma opção 👇",
                                reply_markup=markup)
    
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(message_opcoes, opcoes)


    elif usuario_validado == True and perfil_usuario == 'basico':

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add(   
                            'Solicitar Entrada 🎲'
                            )

        message_opcoes = bot.reply_to(message, f"🤖 Olá {message.json['from']['first_name']}! Escolha uma opção 👇",
                                reply_markup=markup)
    
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(message_opcoes, opcoes)


    elif usuario_validado == True and perfil_usuario == 'bloqueado':

        bot.send_message(message.chat.id, 
                                        f"🤖 Olá, {message.json['from']['first_name']}! Infelizmente você está bloqueado para usar a IA. Procure o Suporte e ative/renove seu acesso!")


    else:

        bot.send_message(message.chat.id, 
                                        f"🤖 Olá, {message.json['from']['first_name']}! Seja bem vindo(a) a Inteligência Artificial BAC BO do Mágico!\n\
                                        Seu ID é o {message.chat.id}")
        time.sleep(2)

        message_novo_cliente = bot.send_message(message.chat.id, "🤖 Não encontrei seus dados na minha base de acessos. Favor informe seu e-mail para acessar a IA.")
        
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(message_novo_cliente, liberar_acesso)


@bot.message_handler()
def opcoes(message_opcoes):

    if message_opcoes.text in['📊 Placar']:

        if str(message_opcoes.chat.id) in ids_masters:

            placar_atual_geral(message_opcoes)
        
        else:

            message_error = bot.reply_to(message_opcoes, "🤖 Você não tem permissão para acessar este Bot ❌🚫")


    if message_opcoes.text in ['📈 Gestão Estratégia']:
        
        if str(message_opcoes.chat.id) in ids_masters:

            placar_atual_estrategia(message_opcoes)
        
        else:

            message_error = bot.reply_to(message_opcoes, "🤖 Você não tem permissão para acessar este Bot ❌🚫")


    if message_opcoes.text in ['⚙ Cadastrar Estratégia']:
        
        if str(message_opcoes.chat.id) in ids_masters:
        
            cadastrarEstrategia(message_opcoes)
        
        else:

            message_error = bot.reply_to(message_opcoes, "🤖 Você não tem permissão para acessar este Bot ❌🚫")


    if message_opcoes.text in['📜 Estratégias Cadastradas']:

        if str(message_opcoes.chat.id) in ids_masters:
            print('Estrategias Cadastradas')
            estrategiasCadastradas(message_opcoes)

        
        else:

            message_error = bot.reply_to(message_opcoes, "🤖 Você não tem permissão para acessar este Bot ❌🚫")


    if message_opcoes.text in ['🗑 Apagar Estratégia']:

        
        if str(message_opcoes.chat.id) in ids_masters:
        
            print('Apagar estrategia')
            apagarEstrategia(message_opcoes)
        
        
        else:

            message_error = bot.reply_to(message_opcoes, "🤖 Você não tem permissão para acessar este Bot ❌🚫")


    if message_opcoes.text in ['Solicitar Entrada 🎲'] or message_opcoes.text in ['Solicitar Entrada Premium 🎲']:
        global solicitacao_usuario

        solicitacao_usuario = message_opcoes.text
        entrada_andamento = valida_solicitacao_entrada(message_opcoes.json['from']['id'])

        if entrada_andamento == False:
            valida_qntd_entradas(message_opcoes.json['from']['id'], entrada_andamento)

  




while True:
    try:
       
       bot.infinity_polling(timeout=100000, long_polling_timeout=10000)


    except:
        bot.infinity_polling(True)
        continue

