from selenium import webdriver
import time
import warnings
from webdriver_manager.chrome import ChromeDriverManager
import logging
from datetime import datetime, timedelta
from columnar import columnar
import telebot
from telegram.ext import *
from telebot import *
import operator


#_______________________________________________________________________#____________________________________________________________________________________________________

print()
print('                                #################################################################')
print('                                #####################   BOT CRASH PRO   #########################')
print('                                #################################################################')
print('                                ##################### SEJA BEM VINDO ############################')
print('                                #################################################################')
print('                                ############# DESENVOLVIDO POR VICTOR RODRIGUES #################')
print('                                #################################################################\n')
print('Versão = 1.0.0')
print('Ambiente: Produção\n\n\n')



def auto_refresh():
    global horario_inicio

    horario_atual = datetime.today().strftime('%H:%M')
    uma_hora = timedelta(hours=1)
    horario_mais_uma = horario_inicio + uma_hora
    horario_refresh = horario_mais_uma.strftime('%H:%M')

    if horario_atual >= horario_refresh:
        print('HORARIO DE REFRESHAR A PAGINA!')
        logar_site()
        horario_inicio = datetime.now()
        




def verificar_stop_loss():
    global status_stop_loss

    try:

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            return
        else:
            pass

        campos()
        horario_atual = datetime.today().strftime('%H:%M')
        trinta_minutos = timedelta(minutes=30)
        horario_mais_trinta = horario_stop_loss + trinta_minutos
        horario_ativar_analise = horario_mais_trinta.strftime('%H:%M')

        if horario_atual >= horario_ativar_analise:
            status_stop_loss = 0
            coletar_dados()

        else:
            time.sleep(3)

    except:
        pass






def inicio():
    global sticker_alerta
    global sticker_win
    global sticker_loss
    global logger
    global browser
    global lista_anterior
    global horario_inicio

    horario_inicio = datetime.now()

    sticker_alerta = 'CAACAgEAAxkBAAEXKPBi_DTijam6We_hn2pKXO5BmfHFnwACHQIAAtUT4UcU9AABkK85ntMpBA'
    sticker_win = 'CAACAgEAAxkBAAEYhNFjNJLQ2YQtCNyuKbGzoUl2wDBc7QACjwEAAnR6oEcjYniQyrJQoSoE'
    sticker_loss = 'CAACAgEAAxkBAAEYfYBjM5LmbWxXEgefe_MmSjntoMZ_ZgACJAMAAn0bsEYLSD9LZs7UrSoE'

    lista_anterior = []
    logger = logging.getLogger()

    # Definindo opções para o browser
    warnings.filterwarnings("ignore", category=DeprecationWarning) 
    chrome_options = webdriver.ChromeOptions() 
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Opção para executar o prgrama em primeiro ou segundo plano
    escolha = int(input('Deseja que o programa seja executado em primeiro[1] ou segundo[2] plano? --> '))
    print()
    time.sleep(1)

    if escolha == 1:
        print('O programa será executado em primeiro plano.\n')
    else:
        print('O programa será executado em segundo plano.\n')
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
    

    browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)






def logar_site():

    while True:
        try:

            #usuario: Fordbracom22
            #senha : Fordbracom2022
            browser.get(r"https://blaze.com/pt/games/crash")
            time.sleep(10)
            break

        except:
            continue






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






# RELATÓRIO DIÁRIO
def relaDiario():
    global placar
    global resultados_sinais
    global placar_estrategias_diaria
    global data_resultado
    global placar_win
    global placar_semGale
    global placar_gale1
    global placar_gale2
    global placar_gale3
    global placar_loss


    # PLACAR CONSOLIDADO
    try:
        placar_1 = bot.send_message(1020479327,"📊 Resultados do dia "+data_resultado+"\n==============================\n")
        placar_2 = bot.send_message(1020479327,"😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%")
    
    except Exception as a:
        logger.error('Exception ocorrido no ' + repr(a))
        placar_1 = bot.send_message(1020479327,"📊 Resultados do dia "+data_resultado+"\n==============================\n")
        placar_2 = bot.send_message(1020479327,"😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%")


    # PLACAR POR ESTRATEGIA
    for pe in placar_estrategias_diaria:
        total = int(pe[-5]) + int(pe[-4]) + int(pe[-3]) + int(pe[-2]) + int(pe[-1])
        soma_win = int(pe[-5]) + int(pe[-4]) + int(pe[-3]) + int(pe[-2])

        try:
            assertividade = str(round(soma_win / total*100, 1)).replace('.0',"")+"%"
        except:
            assertividade = '0%'

        bot.send_message(1020479327, f'🧠 {pe[:-5]} \n==========================\n 🏆= {pe[-5]}  |  🥇= {pe[-4]}  |  🥈= {pe[-3]}  |  🥉= {pe[-2]} \n\n ✅ - {soma_win} \n ❌ - {pe[-1]} \n==========================\n 🎯 {assertividade}')
        

    # ZERANDO PLACAR E ATUALIZANDO A LISTA DE ESTRATEGIAS DIARIAS
    # Resetando placar Geral (placar geral) e lista de estratégia diária
    placar_win = 0
    placar_semGale= 0
    placar_gale1= 0
    placar_gale2= 0
    placar_gale3= 0
    placar_loss = 0
    placar_estrategias_diaria = []
    estrategias_diaria = []


    # Resetando placar das estrategias (Gestão)
    for pe in placar_estrategias:
        pe[-5], pe[-4], pe[-3], pe[-2], pe[-1] = 0,0,0,0,0
        assertividade = '0%'
        placar_estrategias_diaria.append(pe) # Atualizando o placar das estratégias diária
    

    # Atualizando as estratégias diárias com as estratégias atuais
    for e in estrategias:
        estrategias_diaria.append(e)






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

    if horario_atual == '00:00' and reladiarioenviado == 0:
        relaDiario()
        reladiarioenviado +=1

    
    if horario_atual == '00:01' and reladiarioenviado == 1:
        reladiarioenviado = 0







def enviar_alerta():
    global alerta_free
    global alerta_vip
    global alerta_adm
    global contador_passagem

    try:

        if canal_free != '':
            alerta_free = bot.send_sticker(canal_free, sticker=sticker_alerta)
        
        if canal_vip !='':
            alerta_vip = bot.send_sticker(canal_vip, sticker=sticker_alerta)
        
        
    except:
        pass
    
    contador_passagem = 1






def enviar_sinal(vela_atual):
    global alerta_free
    global alerta_vip
    global table
    global message_canal_free
    global message_canal_vip

    try:

        headers = [' ✅ CASH OUT EM ' + estrategia[-2] + '                                                   ']

        data = [
            ['⏰ ENTRAR APÓS O RESULTADO '+ vela_atual                    ],
            ['🔰 FAZER ATÉ ' + estrategia[-1] + ' PROTEÇÕES' if int(estrategia[-1]) > 0 else '🔰 FAZER NENHUMA PROTEÇÃO'],
            ["🌐 <a href='https://blaze.com/pt/games/crash'>Site do Crash</a>     "]
        ]
        
        table = columnar(data, headers, no_borders=True)

        # deletando o alerta
        # enviando sinal Telegram
        if canal_free != '':
            bot.delete_message(canal_free, alerta_free.message_id)
            message_canal_free = bot.send_message(canal_free, table, parse_mode='HTML', disable_web_page_preview=True)

        if canal_vip !='':
            bot.delete_message(canal_vip, alerta_vip.message_id)
            message_canal_vip = bot.send_message(canal_vip, table, parse_mode='HTML', disable_web_page_preview=True)

    except:
        pass

    



def apagar_alerta():
    global contador_passagem

    try:

        if canal_free != '':
            bot.delete_message(canal_free, alerta_free.message_id)

        if canal_vip !='':
            bot.delete_message(canal_vip, alerta_vip.message_id)

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
                        resultado = operator.gt(float(v[1]), float(e[1][1:]))
                        validador.append(resultado)
                        break
                        
                    if '-' in e[1]:
                        resultado = operator.lt(float(v[1]), float(e[1][1:]))
                        validador.append(resultado)
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

    while True:

        # Validando data para envio do relatório diário
        validaData()

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass


        ''' VALIDANDO SE O STOP LOSS ESTÁ ATIVADO '''
        if status_stop_loss == 1:
            verificar_stop_loss()
        
        else:
            pass
        
        ''' VALIDANDO SE A VELA PAROU DE SUBIR '''
        #try:
        #    if browser.find_elements_by_css_selector('.random-points-icon'):
        #        pass
#
        #    else:
        #        logarSite()
#
        #except:
        #    logarSite()


        while True:
            try:

                # Validando data para envio do relatório diário
                validaData()

                lista_resultados = []
                # Pegando o histórico de resultados
                historico_velas = browser.find_elements_by_css_selector('#crash-recent span')
                #'#crash-recent .entries'
                
                # Validando se foi solicitado o stop do BOT
                if parar != 0:
                    break
                else:
                    pass
                
                ''' Inserindo velas na lista'''
                try:
                    for vela in reversed(historico_velas[:10]):
                        numero = vela.text.replace('X','')
                        lista_resultados.append(numero)
                except:
                    ''' CASO NÃO MAPEIE O RESULTADO, VERIFICAR SE ESTÁ LOGADO, SE TIVER, CONSULTAR RESULTADOS NOVAMENTE ''' 
                    if browser.find_elements_by_css_selector('#crash-recent span'):
                        continue

                    else:
                        print('Refresh em ==>' + horario_atual)
                        print('Erro ao incluir resultados na lista na funcao Coletar Dados')
                        logar_site()
                        break

                if lista_resultados == []:
                    print('Refresh em ==>' + horario_atual)
                    print('Erro de lista de resultados vazia na funcao Coletar Dados')
                    logar_site()
                    continue
                
                ''' ALIMENTANDO BANCO DE DADOS '''
                #try:
                #    #alimenta_banco_painel(lista_resultados)
                #except:
                #    pass
                
                # Validando se foi solicitado o stop do BOT

                if parar != 0:
                    break
                else:
                    pass
                

                print(horario_atual)

                ''' Chama a função que valida a estratégia para enviar o sinal Telegram '''
                validar_estrategia(lista_resultados, estrategias)   #Lista de estrategia

                print('=' * 100)
                lista_resultados = []
                break

                ''' Exceção se o cassino não estiver disponível '''
            except Exception as a:
                print('Refresh em ==>' + horario_atual)
                print('Erro ao pegar lista de resultados na funcao Coletar Dados')
                logar_site()







def validar_estrategia(lista_resultados, estrategias):
    global gale
    global vela_atual

    try:
        for estrategia in estrategias:

            # Validando se foi solicitado o stop do BOT
            if parar != 0:
                break
            else:
                pass

            #''' VALIDANDO SE O STOP LOSS ESTÁ ATIVADO '''
            #if status_stop_loss == 1:
            #    verificar_stop_loss()
            #
            #else:
            #    pass


            print ('Analisando a Estrategia --> ', estrategia)

            sequencia_minima_alerta = len(estrategia[:-3])
            sequencia_minima_sinal = len(estrategia[:-2])

            print('Historico_Velas --> ', lista_resultados)

            ''' VALIDADOR DE ESTRATEGIA '''
            validador = validador_estrategia(estrategia, lista_resultados, sequencia_minima_alerta)

            ''' Validando se bateu alguma condição'''
            if validador.count(True) == int(sequencia_minima_alerta) and status_stop_loss == 0:
                print('ENVIANDO ALERTA')
                enviar_alerta()


                ''' Verifica se a ultima condição bate com a estratégia para enviar sinal Telegram '''
                while True:

                    try:

                        # Validando se foi solicitado o stop do BOT
                        if parar != 0:
                            break
                        else:
                            pass
                        
                        ''' Lendo novos resultados para validação da estratégia'''
                        numeros_recentes_validacao = browser.find_elements_by_css_selector('#crash-recent span')
                            
                        ''' LISTA DO PROXIMO RESULTADO APOS O ALERTA'''
                        lista_proximo_resultados = []
                        try:
                            for numeroRecente in reversed(numeros_recentes_validacao[:10]):
                                numero_r = numeroRecente.text.replace('X','')
                                lista_proximo_resultados.append(numero_r)
                        except:
                            continue
                        
                        print(lista_proximo_resultados)

                        ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
                        if lista_resultados != lista_proximo_resultados:
                            validador = validador_estrategia(estrategia, lista_proximo_resultados, sequencia_minima_sinal)

                            ''' ALIMENTANDO O BANCO '''
                            #alimenta_banco_painel(lista_proximo_resultados)

                            ''' VALIDA SE ENVIA SINAL OU APAGA O ALERTA '''
                            if validador.count(True) == int(sequencia_minima_sinal) and status_stop_loss == 0:
                                print(lista_proximo_resultados[-1])
                                print('ENVIA SINAL TELEGRAM')
                                print('=' * 100)
                                vela_atual = lista_proximo_resultados[-1]
                                enviar_sinal(vela_atual)
                                checar_sinal_enviado(lista_proximo_resultados, estrategia)
                                time.sleep(1)
                                break


                            else:
                                print('APAGA SINAL DE ALERTA')
                                print('=' * 100)
                                apagar_alerta()
                                lista_resultados = lista_proximo_resultados
                                break

                    except:
                        continue

            
            else:
                print('=' * 100)


    except:
        pass







def checar_sinal_enviado(lista_proximo_resultados, estrategia):
    global table
    global table_free
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
    global contador_passagem
    global lista_resultados_sinal
    global lista_resultados
    global horario_stop_loss
    global status_stop_loss



    contador_cash = 0

    while contador_cash <= int(estrategia[-1]):

        # Validando data para envio do relatório diário
        validaData()

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass


        try:

            try:
                ''' Lendo novos resultados para validação da estratégia'''
                numeros_recentes_validacao = browser.find_elements_by_css_selector('#crash-recent span')
            
            except:
                print('Refresh em ==>' + horario_atual)
                print('Erro ao pegar lista de resultados na funcao Checar Sinal')
                logar_site()
                continue


            lista_resultados_sinal = []
            try:
                for numeroRecente in reversed(numeros_recentes_validacao[:10]):
                    numero_r = numeroRecente.text.replace('X','')
                    lista_resultados_sinal.append(numero_r)
            except:
                continue


            if lista_resultados_sinal == []:
                print('Refresh em ==>' + horario_atual)
                print('Erro de lista vazia na funcao Coletar Dados')
                logar_site()
                continue


            ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
            if lista_proximo_resultados != lista_resultados_sinal:
                
                print(lista_resultados_sinal[-1])
                #alimenta_banco_painel(lista_resultados_sinal)
            
                # VALIDANDO WIN OU LOSS
                if float(lista_resultados_sinal[-1]) >= float(estrategia[-2].strip('xX')):

                    # validando o tipo de WIN
                    if contador_cash == 0:
                        print('WIN SEM GALE')
                        stop_loss.append('win')

                        if canal_vip !='':
                            placar_win+=1
                            placar_semGale+=1
                            resultados_sinais = placar_win + placar_loss
                            print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
                            #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                            for pe in placar_estrategias:
                                if pe[:-5] == estrategia:
                                    pe[-5] = int(pe[-5])+1 


                    if contador_cash == 1:
                        print('WIN GALE1')
                        stop_loss.append('win')

                        if canal_vip !='':
                            placar_win+=1
                            placar_gale1+=1
                            resultados_sinais = placar_win + placar_loss
                            print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
                            #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                            for pe in placar_estrategias:
                                if pe[:-5] == estrategia:
                                    pe[-4] = int(pe[-4])+1


                    if contador_cash == 2:
                        print('WIN GALE2')
                        stop_loss.append('win')
                        
                        if canal_vip != '':
                            placar_win+=1
                            placar_gale2+=1
                            resultados_sinais = placar_win + placar_loss
                            print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
                            #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)
                            
                            
                            for pe in placar_estrategias:
                                if pe[:-5] == estrategia:
                                    pe[-3] = int(pe[-3])+1



                    if contador_cash == 3:
                        print('WIN gale3')
                        stop_loss.append('win')

                        if canal_vip !='':
                            placar_win+=1
                            placar_gale3+=1
                            resultados_sinais = placar_win + placar_loss
                            print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
                            #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                            
                            for pe in placar_estrategias:
                                if pe[:-5] == estrategia:
                                    pe[-2] = int(pe[-2])+1


                    # editando mensagem enviada e enviando sticker
                    try:

                        if canal_free != '':
                            bot.edit_message_text(table +"  \n======================= \n           GREEN ✅ --- 🎯 "+ lista_resultados_sinal[-1]+"x", message_canal_free.sender_chat.id, message_canal_free.message_id, parse_mode='HTML', disable_web_page_preview=True)   
                            bot.send_sticker(canal_free, sticker=sticker_win)


                        if canal_vip != '':
                            bot.edit_message_text(table +"  \n======================= \n           GREEN ✅ --- 🎯 "+ lista_resultados_sinal[-1]+"x", message_canal_vip.sender_chat.id, message_canal_vip.message_id, parse_mode='HTML', disable_web_page_preview=True)   
                            bot.send_sticker(canal_vip, sticker=sticker_win)



                        # CONDIÇÃO PARA ENVIAR O GIF DO PATO
                        if stop_loss.count('win') == 20:
                            try:
            
                                if canal_free !='':
                                    bot.send_video(canal_free, video=open('money-donald-duck.mp4', 'rb'), supports_streaming=True)

                                if canal_vip !='':
                                    bot.send_video(canal_vip, video=open('money-donald-duck.mp4', 'rb'), supports_streaming=True)

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
    

    if parar != 0:
        return
    else:
        pass


    if contador_cash > int(estrategia[-1]):
        print('LOSSS GALE ',estrategia[-1])
        placar_loss +=1
        stop_loss.append('loss')
    

        if canal_vip != '':
            resultados_sinais = placar_win + placar_loss
            print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
            #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)


            # Atualizando placar da estratégia
            for pe in placar_estrategias:
                if pe[:-5] == estrategia:
                    pe[-1] = int(pe[-1])+1
        
        

        # editando mensagem e enviando sticker
        try:
            
            if canal_free !='':
                bot.edit_message_text(table +"\n======================= \n              RED ✖", message_canal_free.sender_chat.id, message_canal_free.message_id, parse_mode='HTML', disable_web_page_preview=True)
                bot.send_sticker(canal_free, sticker=sticker_loss)

            if canal_vip !='':
                bot.edit_message_text(table +"\n======================= \n              RED ✖", message_canal_vip.sender_chat.id, message_canal_vip.message_id, parse_mode='HTML', disable_web_page_preview=True)
                bot.send_sticker(canal_vip, sticker=sticker_loss)

        except:
            pass

        
        

        # Validando o stop_loss
        if 'win' in stop_loss:
            stop_loss = []
            stop_loss.append('loss')
        
        if stop_loss.count('loss') == 2:
            try:
            
                if canal_free !='':
                    bot.send_message(canal_free, f'⛔🛑 Alunos,\nMercado instável! Aguardem a normalização do mesmo conforme indicamos no curso 📚.\n\nAtt, Diretoria Pro Tips 🤝 ')

                if canal_vip !='':
                    bot.send_message(canal_vip, f'⛔🛑 Alunos,\nMercado instável! Aguardem a normalização do mesmo conforme indicamos no curso 📚.\n\nAtt, Diretoria Pro Tips 🤝 ')

                stop_loss = []
                print('STOP LOSS - ANÁLISE VOLTARÁ EM 30 MINUTOS \n\n')
                
                status_stop_loss = 1
                horario_stop_loss = datetime.now()

            except:
                pass
        
        print('=' * 100)
        validador_sinal = 0
        contador_cash = 0
        contador_passagem = 0
        lista_resultados = lista_resultados_sinal
        return




inicio()            # Difinição do webBrowser
logar_site()         # Logando no Site







#________________________________________________________________________________________ TELEGRAM__________________________________________________________________________________#

print('\n\n')
print('###################### AGUARDANDO COMANDOS ######################')

global canal
global bot

#CHAVE_API = '5651549126:AAFaVyaQkxTTVPq9WxpIBejBMR_oUPdt_5o' # DEV
CHAVE_API = '5524000360:AAGy69YHN-hLXYlKcf1W01pLdLFq6QbeNoU' # PRODUÇÃO

bot = telebot.TeleBot(CHAVE_API)

# PLACAR
placar_win = 0
placar_semGale= 0
placar_gale1= 0
placar_gale2= 0
placar_gale3= 0
placar_loss = 0
resultados_sinais = placar_win + placar_loss
estrategias = []
placar_estrategias = []
estrategias_diaria = []
placar_estrategias_diaria = []
contador = 0
botStatus = 0
contador_passagem = 0



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
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('◀ Voltar')

        message_estrategia = bot.reply_to(message, "🤖 Ok! Escolha um padrão acima ou abaixo de velas, a vela que deverá fazer CASH OUT e uma opção de GALE \n\n Ex: +1,-2,-10.35,1.5X,1", reply_markup=markup)
        bot.register_next_step_handler(message_estrategia, registrarEstrategia)
    
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
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

    try:
        placar = bot.reply_to(message,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", reply_markup=markup)
    except Exception as a:
        logger.error('Exception ocorrido no ' + repr(a))
        placar = bot.reply_to(message,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%", reply_markup=markup)




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
        
        #print(f'🧠 {pe[:-5]} \n==========================\n 🏆= {pe[-5]}  |  🥇= {pe[-4]}  |  🥈= {pe[-3]}  |  🥉= {pe[-2]} \n\n ✅ - {soma_win} \n ❌ - {pe[-1]} \n==========================\n 🎯 {assertividade}'
        #)

    


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
        contador_passagem = 0
        pausarBot()

        message_final = bot.reply_to(message, "🤖 Ok! Bot pausado 🛑", reply_markup=markup)
        
        print('###################### AGUARDANDO COMANDOS ######################')




@bot.message_handler(commands=['start'])
def start(message):

    if str(message.chat.id) in id_usuario:
       

        #Add to buttons by list with ours generate_buttons function.
        #markup = generate_buttons(['/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','📊 Placar Atual','❌ Pausar Bot'], markup)
        
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message, "🤖 Bot Crash PRO Iniciado! ✅ Escolha uma opção 👇",
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
        global message_canal

        print('Ativar Bot')

        if botStatus == 1:

            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖⛔ Bot já está ativado",
                                reply_markup=markup)

        elif estrategias == []:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖⛔ Cadastre no mínimo 1 estratégia antes de iniciar",
                                reply_markup=markup)
        
        else:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('◀ Voltar', '📋 Enviar sinais Canal ADM', '🏆 Enviar sinais Canal VIP', '📋🏆 Enviar sinais Canal ADM & VIP')

            message_canal = bot.reply_to(message_opcoes, "🤖 Escolha para onde enviar os sinais 👇",
                                    reply_markup=markup)
            
            bot.register_next_step_handler(message_canal, escolher_canal)

    
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
    



@bot.message_handler(content_types=['text'])
def escolher_canal(message_canal):
    global canal_free
    global canal_vip
    global placar
    global estrategia
    global stop_loss
    global botStatus
    global seq_vela_maluca
    global vela_anterior
    global reladiarioenviado
    global parar 
    global status_stop_loss


    if message_canal.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_canal, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)

    if message_canal.text in ['📋 Enviar sinais Canal ADM']:

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_final = bot.reply_to(message_canal, "🤖 Ok! Ligando Bot nas configurações:\n===============================\n" + "Canal: "+ str(message_canal.text.split(' ')[4:]) + '\n Estratégia(s): \n' + str([f'{estrategia}' for estrategia in estrategias]), reply_markup = markup)
        
        print("Iniciar e enviar sinais no Canal FREE ")


        canal_free = free
        canal_vip = ''
        stop_loss = []
        botStatus = 1
        seq_vela_maluca = 0
        vela_anterior = 0
        reladiarioenviado = 0
        parar = 0
        status_stop_loss = 0

        placar = bot.send_message(message_canal.chat.id,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%")

        print('######################### ANALISANDO AS ESTRATÉGIAS CADASTRADAS  #########################')
        print()

        coletar_dados()
    

    if message_canal.text in ['🏆 Enviar sinais Canal VIP']:
        
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_final = bot.reply_to(message_canal, "🤖 Ok! Ligando Bot nas configurações:\n===============================\n" + "Canal: "+ str(message_canal.text.split(' ')[4:]) + '\n Estratégia(s): \n' + str([f'{estrategia}' for estrategia in estrategias]), reply_markup = markup)
        
        print("Iniciar e enviar sinais no Canal VIP ")

        canal_free = ''
        canal_vip = vip
        stop_loss = []
        botStatus = 1
        seq_vela_maluca = 0
        vela_anterior = 0
        reladiarioenviado = 0
        parar = 0
        status_stop_loss = 0

        placar = bot.send_message(message_canal.chat.id,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%")

        print('######################### ANALISANDO AS ESTRATÉGIAS CADASTRADAS  #########################')
        print()

        coletar_dados()


    if message_canal.text in ['📋🏆 Enviar sinais Canal ADM & VIP']:
        
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_final = bot.reply_to(message_canal, "🤖 Ok! Ligando Bot nas configurações:\n===============================\n" + "Canal: "+ str(message_canal.text.split(' ')[4:]) + '\n Estratégia(s): \n' + str([f'{estrategia}' for estrategia in estrategias]), reply_markup = markup)
        
        print("Iniciar e enviar sinais no Canal FREE & VIP ")

        canal_free = free
        canal_vip = vip
        stop_loss = []
        botStatus = 1
        seq_vela_maluca = 0
        vela_anterior = 0
        reladiarioenviado = 0
        parar = 0
        status_stop_loss = 0

        placar = bot.send_message(message_canal.chat.id,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%")

        print('######################### ANALISANDO AS ESTRATÉGIAS CADASTRADAS  #########################')
        print()

        coletar_dados()




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





bot.infinity_polling()






