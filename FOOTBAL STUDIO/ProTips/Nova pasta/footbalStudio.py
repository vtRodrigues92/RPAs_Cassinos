# -*- coding: utf-8 -*-
from webbrowser import BaseBrowser
from xml.dom.minidom import Document
from cv2 import CAP_PROP_INTELPERC_DEPTH_LOW_CONFIDENCE_VALUE
from selenium import webdriver
import time
import warnings
from webdriver_manager.chrome import ChromeDriverManager
import logging
from datetime import datetime, timedelta
from selenium.webdriver.support.color import Color
import pandas as pd
from columnar import columnar
import telebot
from telegram.ext import *
from telebot import *
import emoji


print()
print('                                #################################################################')
print('                                ##################   BOT FOOTBALSTUDIO   ########################')
print('                                #################################################################')
print('                                ##################### SEJA BEM VINDO ############################')
print('                                #################################################################')
print('                                ############# DESENVOLVIDO POR VICTOR RODRIGUES #################')
print('                                #################################################################\n')
print('Versão = 1.0.0')
print('Ambiente: Produção\n\n\n')



def inicio():
    global browser
    global sticker_alerta
    global sticker_win
    global sticker_loss
    global sticker_empate


    # Figurinhas
    sticker_alerta = 'CAACAgEAAxkBAAEY6YljRj8XVy-3aKgtm6JYQMPDsr3WoAACLAMAAnNOOUbJ7-WoR2DMDCoE'
    sticker_win = 'CAACAgEAAxkBAAEY6Y9jRj-wf1MIDT4IGG-nd3x5ID8AARUAAg4DAAKLsDBG6AM7UtCcA-gqBA'
    sticker_loss = 'CAACAgEAAxkBAAEY6ZFjRj_CV69fevdi0r2jRm_kCX6bXAACIQMAAsUkMUYKuQm51fo8LioE'
    sticker_empate = 'CAACAgEAAxkBAAEY6ZNjRj_bd_t6HDHhPesDgZqQpydbowACFwIAAubdMEZ8Yl-s4mnj3yoE'

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

    browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)



def logarSite():
    browser.get(r"https://pi.njoybingo.com/game.do?token=7397d9ce-67e3-4eaf-84be-76a7744311ed&pn=meskbet&lang=pt&game=EVOLUTION-topcard-nvrpqglt6teqkvaf&type=CHARGED")
    browser.maximize_window()
    time.sleep(10)


#https://pi.njoybingo.com/game.do?token=7397d9ce-67e3-4eaf-84be-76a7744311ed&pn=meskbet&lang=pt&game=EVOLUTION-topcard-nvrpqglt6teqkvaf&type=CHARGED



#macedomacedo
#Vb920115

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




def converterLetraEmCor(resultados):
    ''' Convertendo a letra em cor '''
    while True:
        try:
            lista = []
            for resultado in resultados:
                if resultado.text == 'C':
                    resultado = '🔴'
                    lista.append(resultado)
                    continue

                if resultado.text == 'V':
                    resultado = '🔵'
                    lista.append(resultado)
                    continue

                if resultado.text == 'E':
                    resultado = '🟡'
                    lista.append(resultado)
                    continue
            
            return lista
            
        except:
            resultados = browser.find_elements_by_css_selector('.historyItem--a1907')
            continue




def validarJogoPausado():
    try:
        if browser.find_elements_by_xpath('//*[@id="root"]/div/div[2]/div/div/div[10]/div[1]'):
            browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div').click()
    
    except:
        pass




def coletarDados():

    while True:

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass
        
        # Validando o horario para envio do relatório diário
        validaData()


        # Jogo Pausado
        validarJogoPausado()


        try:
            ''' Pegando Resultados do Jogo '''
            resultados = browser.find_elements_by_css_selector('.historyItem--a1907')
            ''' Lista de resultados Convertidas em cores '''
            lista_resultados = converterLetraEmCor(resultados)
            validaEstrategias(lista_resultados)

        except:
            pass




def validaEstrategias(lista_resultados):
    global estrategias
    global estrategia
    
    for estrategia in estrategias:
        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass
        # Validando o horario para envio do relatório diário
        validaData()

        # Jogo Pausado
        validarJogoPausado()
        

        sequencia_minima_alerta = len(estrategia)-2
        sequencia_minima_sinal = len(estrategia)-1

        #print ('Analisando a Estratégia --> ', estrategia)
        #print('Historico da Mesa --> ', lista_resultados[:sequencia_minima_alerta])

        ''' Verifica se os resultados da mesa batem com a estrategia para enviar o alerta '''
        if estrategia[:sequencia_minima_alerta] == lista_resultados[:sequencia_minima_alerta]:
            print('IDENTIFICADO O PADRÃO DA ESTRATÉGIA --> ', estrategia)
            print('ENVIAR ALERTA')
            enviarAlertaTelegram(sticker_alerta)
            time.sleep(1)

            ''' Verifica se a ultima condição bate com a estratégia para enviar sinal Telegram '''
            while True:
                # Jogo Pausado
                validarJogoPausado()
                
                ''' Lendo novos resultados para validação da estratégia'''
                if browser.find_elements_by_css_selector('.historyItem--a1907'):
                   resultados = browser.find_elements_by_css_selector('.historyItem--a1907')
                   ''' Função que converte as letras em cores '''
                   lista_resultados_validacao = converterLetraEmCor(resultados)

                ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
                if lista_resultados[:3] != lista_resultados_validacao[:3]:
                    ''' Verificando se o ultimo resultado da mesa está dentro da estratégia'''
                    if estrategia[:sequencia_minima_sinal] == lista_resultados_validacao[:sequencia_minima_sinal]:
                        print('PADRÃO DA ESTRATÉGIA ', estrategia, ' IDENTIFICADO!')
                        print('ENVIANDO SINAL TELEGRAM')
                        enviarSinalTelegram(lista_resultados_validacao)
                        time.sleep(1)
                        checkSinalEnviado(lista_resultados_validacao)
                        break
                        
                    else:
                        print('APAGA SINAL DE ALERTA')
                        apagaAlertaTelegram()
                        break




def enviarAlertaTelegram(sticker_alerta):
    global alerta_free
    global alerta_vip
    global alerta_adm
    global contador_passagem

    ''' Enviando mensagem Telegram '''
    try:
        if canal_free != '':
            alerta_free = bot.send_sticker(canal_free, sticker = sticker_alerta)
            
        if canal_vip !='':
            alerta_vip = bot.send_sticker(canal_vip, sticker = sticker_alerta)

        if canal_adm !='':
            alerta_adm = bot.send_sticker(canal_adm, sticker=sticker_alerta)
                                    
        contador_passagem += 1
    except:
        pass




def enviarSinalTelegram(lista_resultados_validacao):
    global alerta_free
    global alerta_vip
    global alerta_adm
    global table
    global message_canal_free
    global message_canal_vip
    global message_canal_adm
    
    headers = ['✅ APOSTAR NA ' + 'CASA 🔴' if estrategia[-1] == '🔴' else '✅ APOSTAR NO VISITANTE 🔵' ]

    data = [

        ['🌑 DEFENDER NO EMPATE 🟡'],
        ['⏰ ENTRAR APÓS ' + lista_resultados_validacao[0]],
        ['🔰 FAZER ATÉ 2 PROTEÇÕES'],
        ["🌐<a href='https://mesk.bet/casino/?cat=live'> Football Studio</a>     "],
        [''],
        ["🟢<a href='https://mesk.bet/register/meskbonus'> CADASTRE-SE AGORA</a>     "]

    ]

    table = columnar(data, headers, no_borders=True) 

    try:
        # deletando o alerta
        # enviando sinal Telegram
        if canal_free != '':
            bot.delete_message(canal_free, alerta_free.message_id)
            message_canal_free = bot.send_message(canal_free, table, parse_mode='HTML', disable_web_page_preview=True)

        if canal_vip !='':
            bot.delete_message(canal_vip, alerta_vip.message_id)
            message_canal_vip = bot.send_message(canal_vip, table, parse_mode='HTML', disable_web_page_preview=True)

        if canal_adm !='':
            bot.delete_message(canal_adm, alerta_adm.message_id)
            message_canal_adm = bot.send_message(canal_adm,table, parse_mode='HTML', disable_web_page_preview=True)


    except:
        pass




def apagaAlertaTelegram():

    try:
        if canal_free != '':
            bot.delete_message(canal_free, alerta_free.message_id)

        if canal_vip !='':
            bot.delete_message(canal_vip, alerta_vip.message_id)

        if canal_adm !='':
            bot.delete_message(canal_adm, alerta_adm.message_id)

        
        contador_passagem = 0

    except:
        pass




def checkSinalEnviado(lista_resultados_validacao):
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

    resultado_valida_sinal = []
    contador_cash = 0
    while contador_cash <= 2:

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass

        # Validando o horario para envio do relatório diário
        validaData()

        # Jogo Pausado
        validarJogoPausado()

        try:
           
            if browser.find_elements_by_css_selector('.historyItem--a1907'):
                resultados = browser.find_elements_by_css_selector('.historyItem--a1907')
                ''' Função que converte as letras em cores '''
                lista_resultados_sinal = converterLetraEmCor(resultados)

            ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
            if lista_resultados_validacao != lista_resultados_sinal:
    
                print(lista_resultados_sinal[0])
                resultado_valida_sinal.append(lista_resultados_sinal[0])

                # VALIDANDO WIN OU LOSS
                if lista_resultados_sinal[0] == estrategia[-1] or lista_resultados_sinal[0] == '🟡':
                
                    # validando o tipo de WIN
                    if contador_cash == 0:
                        print('WIN SEM GALE')
                        stop_loss.append('win')

                        # Preenchendo relatório
                        placar_win+=1
                        placar_semGale+=1
                        resultados_sinais = placar_win + placar_loss
                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                        try:
                            # Somando Win na estratégia da lista atual
                            for pe in placar_estrategias:
                                if pe[:-5] == [estrategia[1].upper()]:
                                    pe[-5] = int(pe[-5])+1
                        except:
                            pass
                        
                        
                    if contador_cash == 1:
                        print('WIN GALE1')
                        stop_loss.append('win')

                        # Preenchendo relatório
                        placar_win+=1
                        placar_gale1+=1
                        resultados_sinais = placar_win + placar_loss
                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

                        try:
                            # Somando Win na estratégia da lista atual
                            for pe in placar_estrategias:
                                if pe[:-5] == [estrategia[1].upper()]:
                                    pe[-4] = int(pe[-4])+1

                        except:
                            pass


                    if contador_cash == 2:
                        print('WIN GALE2')
                        stop_loss.append('win')
                        
                        # Preenchendo relatório
                        placar_win+=1
                        placar_gale2+=1
                        resultados_sinais = placar_win + placar_loss
                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)
                        
                        try:
                            # Somando Win na estratégia da lista atual
                            for pe in placar_estrategias:
                                    if pe[:-5] == [estrategia[1].upper()]:
                                        pe[-3] = int(pe[-3])+1
                        except:
                            pass
                        
                
                    if contador_cash == 3:
                        print('WIN gale3')
                        stop_loss.append('win')

                        # Preenchendo relatório
                        placar_win+=1
                        placar_gale3+=1
                        resultados_sinais = placar_win + placar_loss
                        print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
                        #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)
                        
                        try:
                            # Somando Win na estratégia da lista atual
                            for pe in placar_estrategias:
                                if pe[:-5] == [estrategia[1].upper()]:
                                    pe[-2] = int(pe[-2])+1
                            
                        except:
                            pass

        
                    # editando mensagem enviada
                    try:
                        if canal_free != '':
                            #bot.reply_to(message_canal_free, mensagem_green[37].replace('\n','').replace('[RESULTADO]', ' | '.join(resultados)), parse_mode='HTML')
                            bot.edit_message_text(table +"  \n============================== \n              GREEN ✅ --- 🎯 "+' | '.join(resultado_valida_sinal), message_canal_free.sender_chat.id, message_canal_free.message_id, parse_mode='HTML', disable_web_page_preview=True)   
                            
                            ''' Enviando sticker '''
                            if lista_resultados_sinal[0] == '🟡':
                                bot.send_sticker(canal_free, sticker=sticker_empate)
                            else:
                                bot.send_sticker(canal_free, sticker=sticker_win)


                        if canal_vip != '':
                            #bot.reply_to(message_canal_vip, mensagem_green[37].replace('\n','').replace('[RESULTADO]', ' | '.join(resultados)), parse_mode='HTML')
                            bot.edit_message_text(table +"  \n============================== \n              GREEN ✅ --- 🎯 "+ ' | '.join(resultado_valida_sinal), message_canal_vip.sender_chat.id, message_canal_vip.message_id, parse_mode='HTML', disable_web_page_preview=True)   
                            
                            ''' Enviando sticker '''
                            if lista_resultados_sinal[0] == '🟡':
                                bot.send_sticker(canal_vip, sticker=sticker_empate)
                            else:
                                bot.send_sticker(canal_vip, sticker=sticker_win)


                        if canal_adm != '':
                            bot.edit_message_text(table +"  \n============================== \n              GREEN ✅ --- 🎯 "+ ' | '.join(resultado_valida_sinal), message_canal_adm.sender_chat.id, message_canal_adm.message_id, parse_mode='HTML', disable_web_page_preview=True)   
                            
                            ''' Enviando sticker '''
                            if lista_resultados_sinal[0] == '🟡':
                                bot.send_sticker(canal_adm, sticker=sticker_empate)
                            else:
                                bot.send_sticker(canal_adm, sticker=sticker_win)


                    except:
                        pass
                    

                    print('='*150)
                    validador_sinal = 0
                    contador_cash = 0
                    contador_passagem = 0
                    return

            
                else:
                    print('LOSSS')
                    print('==================================================')
                    contador_cash+=1
                    lista_resultados_validacao = lista_resultados_sinal
                    continue


        except:
            continue


    if contador_cash == 3:
        print('LOSSS GALE2')
        placar_loss +=1
        stop_loss.append('loss')
        
        # editando mensagem e enviando sticker
        try:
        
            if canal_free !='':
                #bot.reply_to(message_canal_free, mensagem_green[39].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(resultados)), parse_mode = 'HTML')
                bot.edit_message_text(table +"\n============================== \n                 RED ✖"+ ' | '.join(resultado_valida_sinal), message_canal_free.sender_chat.id, message_canal_free.message_id, parse_mode='HTML', disable_web_page_preview=True)
                bot.send_sticker(canal_free, sticker=sticker_loss)


            if canal_vip !='':
                #bot.reply_to(message_canal_vip, mensagem_green[39].replace('\n','').replace('[LISTA_RESULTADOS]', ' | '.join(resultados)), parse_mode='HTML')
                bot.edit_message_text(table +"\n============================== \n                 RED ✖"+ ' | '.join(resultado_valida_sinal), message_canal_vip.sender_chat.id, message_canal_vip.message_id, parse_mode='HTML', disable_web_page_preview=True)
                bot.send_sticker(canal_vip, sticker=sticker_loss)


            if canal_adm !='':
                bot.edit_message_text(table +"\n============================== \n                 RED ✖"+ ' | '.join(resultado_valida_sinal), message_canal_adm.sender_chat.id, message_canal_adm.message_id, parse_mode='HTML', disable_web_page_preview=True)
                bot.send_sticker(canal_adm, sticker=sticker_loss)


            # Preenchendo relatório
            resultados_sinais = placar_win + placar_loss
            print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
        
        except:
            pass

        ''' Alimentando "Gestão" estratégia e roleta '''
        try:
            # Somando Win na estratégia da lista atual
            for pe in placar_estrategias:
                if pe[:-5] == [estrategia[1].upper()]:
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
        #            bot.send_message(canal_free, f'⛔🛑 Alunos,\nMercado instável! Aguardem a normalização do mesmo conforme indicamos no curso 📚.\n\nAtt, Diretoria Nivus Tips 🤝 ')
    
        #        if canal_vip !='':
        #            bot.send_message(canal_vip, f'⛔🛑 Alunos,\nMercado instável! Aguardem a normalização do mesmo conforme indicamos no curso 📚.\n\nAtt, Diretoria Nivus Tips 🤝 ')
    
        #        stop_loss = []
        #        print('STOP LOSS - ANÁLISE VOLTARÁ EM 30 MINUTOS \n\n')
        #        time.sleep(1800)
    
        #    except:
        #        pass


        print('==================================================')
        validador_sinal = 0
        contador_cash = 0
        contador_passagem = 0
        return





inicio()
logarSite()




#________________________________________________________________________________________ TELEGRAM__________________________________________________________________________________#


print('############################################ AGUARDANDO COMANDOS ############################################')

global canal

#CHAVE_API = '5651549126:AAFaVyaQkxTTVPq9WxpIBejBMR_oUPdt_5o'   # DEV
CHAVE_API = '5751909068:AAGk0YekH6DCSX_b-ree_lg91J0-A5FLgoY'  # PRODUÇÃO

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
contador_passagem = 0
botStatus = 0



# LENDO TXT PARA DEFINIR VARIAVEL FREE E VIP E VALIDAÇÃO DE USUÁRIO
txt = open("canais.txt", "r")
free = txt.readlines(1)
vip = txt.readlines(2)
adm = txt.readlines(3)
ids = txt.readlines(4)

for canal in free:
    free = canal.split(' ')
    free = int(free[1])
    

for canal in vip:
    vip = canal.split(' ')
    vip = int(vip[1])


for canal in adm:
    adm = canal.split(' ')
    adm = int(adm[1])


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

        message_estrategia = bot.reply_to(message, "🤖 Ok! Informe a sequencia de cores que o bot terá que identificar. *** A última cor será a cor da aposta ***  \n\n Ex: 🔴🔵🔵🔴🔵🟡", reply_markup=markup)
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
        markup_estrategias = generate_buttons_estrategias([''.join(estrategia) for estrategia in estrategias], markup)
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
        bot.send_message(message.chat.id, ''.join(estrategia))




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
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_excluir_estrategia = bot.reply_to(message, "🤖⛔ Estou validando uma estratégia! Tente novamente em alguns instanstes.", reply_markup=markup)

    elif botStatus == 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Bot já está pausado ", reply_markup=markup)

    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

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

    if str(message.chat.id) in id_usuario:
       

        #Add to buttons by list with ours generate_buttons function.
        #markup = generate_buttons(['/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','📊 Placar Atual','❌ Pausar Bot'], markup)
        
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message, "🤖 Bot Football Studio PRO Iniciado! ✅ Escolha uma opção 👇",
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
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            markup = markup.add('◀ Voltar', '🆓 Enviar sinais Canal FREE', '🏆 Enviar sinais Canal VIP', '📋 Enviar sinais Canal ADM', '🆓🏆 Enviar sinais Canal VIP & ADM', '🆓🏆📋 Enviar sinais Canal FREE & VIP & ADM')

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
    global canal_adm
    global placar
    global estrategia
    global stop_loss
    global botStatus
    global vela_anterior
    global reladiarioenviado
    global parar 


    if message_canal.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_canal, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)


    if message_canal.text in ['🆓 Enviar sinais Canal FREE']:

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_final = bot.reply_to(message_canal, "🤖 Ok! Ligando Bot nas configurações:\n===============================\n" + "Canal: "+ str(message_canal.text.split(' ')[4:]) + '\n Estratégia(s): \n' + str([f'{estrategia}' for estrategia in estrategias]), reply_markup = markup)
        
        print("Iniciar e enviar sinais no Canal FREE ")

        canal_free = free
        canal_vip = ''
        canal_adm = ''
        stop_loss = []
        botStatus = 1
        vela_anterior = 0
        reladiarioenviado = 0
        parar = 0

        placar = bot.send_message(message_canal.chat.id,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%")

        print('######################### ANALISANDO AS ESTRATÉGIAS CADASTRADAS  #########################')
        print()

        coletarDados()
    

    if message_canal.text in ['🏆 Enviar sinais Canal VIP']:
        
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_final = bot.reply_to(message_canal, "🤖 Ok! Ligando Bot nas configurações:\n===============================\n" + "Canal: "+ str(message_canal.text.split(' ')[4:]) + '\n Estratégia(s): \n' + str([f'{estrategia}' for estrategia in estrategias]), reply_markup = markup)
        
        print("Iniciar e enviar sinais no Canal VIP ")

        canal_free = ''
        canal_vip = vip
        canal_adm = ''
        stop_loss = []
        botStatus = 1
        vela_anterior = 0
        reladiarioenviado = 0
        parar = 0

        placar = bot.send_message(message_canal.chat.id,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%")

        print('######################### ANALISANDO AS ESTRATÉGIAS CADASTRADAS  #########################')
        print()

        coletarDados()


    if message_canal.text in ['📋 Enviar sinais Canal ADM']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_final = bot.reply_to(message_canal, "🤖 Ok! Ligando Bot nas configurações:\n===============================\n" + "Canal: "+ str(message_canal.text.split(' ')[4:]) + '\n Estratégia(s): \n' + str([f'{estrategia}' for estrategia in estrategias]), reply_markup = markup)
        
        print("Iniciar e enviar sinais no Canal ADM ")

        canal_free = ''
        canal_vip = ''
        canal_adm = adm
        stop_loss = []
        botStatus = 1
        vela_anterior = 0
        reladiarioenviado = 0
        parar = 0

        placar = bot.send_message(message_canal.chat.id,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%")

        print('######################### ANALISANDO AS ESTRATÉGIAS CADASTRADAS  #########################')
        print()

        coletarDados()


    if message_canal.text in ['🆓🏆 Enviar sinais Canal VIP & ADM']:
        
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_final = bot.reply_to(message_canal, "🤖 Ok! Ligando Bot nas configurações:\n===============================\n" + "Canal: "+ str(message_canal.text.split(' ')[4:]) + '\n Estratégia(s): \n' + str([f'{estrategia}' for estrategia in estrategias]), reply_markup = markup)
        
        print("Iniciar e enviar sinais no Canal VIP & ADM ")

        canal_free = ''
        canal_vip = vip
        canal_adm = adm
        stop_loss = []
        botStatus = 1
        vela_anterior = 0
        reladiarioenviado = 0
        parar = 0

        placar = bot.send_message(message_canal.chat.id,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%")

        print('######################### ANALISANDO AS ESTRATÉGIAS CADASTRADAS  #########################')
        print()

        coletarDados()


    if message_canal.text in ['🆓🏆📋 Enviar sinais Canal FREE & VIP & ADM']:

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start','✅ Ativar Bot','⚙ Cadastrar Estratégia','📜 Estratégias Cadastradas','🗑 Apagar Estratégia','♻ Resetar Resultados', '📊 Placar Atual','📈 Gestão','🛑 Pausar Bot')

        message_final = bot.reply_to(message_canal, "🤖 Ok! Ligando Bot nas configurações:\n===============================\n" + "Canal: "+ str(message_canal.text.split(' ')[4:]) + '\n Estratégia(s): \n' + str([f'{estrategia}' for estrategia in estrategias]), reply_markup = markup)
        
        print("Iniciar e enviar sinais no Canal FREE & VIP & ADM ")

        canal_free = free
        canal_vip = vip
        canal_adm = adm
        stop_loss = []
        botStatus = 1
        vela_anterior = 0
        reladiarioenviado = 0
        parar = 0

        placar = bot.send_message(message_canal.chat.id,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%")

        print('######################### ANALISANDO AS ESTRATÉGIAS CADASTRADAS  #########################')
        print()

        coletarDados()




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
    
    estrategia = list(estrategia)
    placar_estrategia = list(placar_estrategia)

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



