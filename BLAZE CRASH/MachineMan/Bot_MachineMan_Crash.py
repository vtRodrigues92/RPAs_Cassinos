from webbrowser import BaseBrowser
from selenium import webdriver
import time
import warnings
from webdriver_manager.chrome import ChromeDriverManager
import logging
from datetime import datetime, timedelta
from selenium.webdriver.support.color import Color
from columnar import columnar
import telebot
from telegram.ext import *
from telebot import *
from webdriver_manager.firefox import GeckoDriverManager


#_______________________________________________________________________#____________________________________________________________________________________________________

print()
print('                                #################################################################')
print('                                ################   BOT CRASH MACHINE MAN   ######################')
print('                                #################################################################')
print('                                ##################### SEJA BEM VINDO ############################')
print('                                #################################################################')
print('                                ############# DESENVOLVIDO POR VICTOR RODRIGUES #################')
print('                                #################################################################\n')
print('Versão = 1.0.0')
print('Ambiente: Produção\n\n\n')



# Definindo opções para o browser
warnings.filterwarnings("ignore", category=DeprecationWarning) 
chrome_options = webdriver.ChromeOptions() 
chrome_options.add_argument("--disable-gpu")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])


time.sleep(1)
print()
print('O Programa está sendo iniciado......')

#browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
browser = webdriver.Firefox(executable_path=GeckoDriverManager().install()) 
print('\n\n')

logger = logging.getLogger()

browser.get(r"https://historicosblaze.com/blaze/crashes")
browser.maximize_window()
time.sleep(10)

# CORES
preto = '#423f3f'
verde = '#04d47c'

# STICKERS
sticker_alerta = 'CAACAgEAAxkBAAEYWgRjLReOUhPEQHizLtwE7r_rTRLXLAACVwEAAoJIEUTynFz2UlgL_ykE'
sticker_loss = 'CAACAgEAAxkBAAEYWgtjLRgt52xdgttoF3cAAdsT8D61TGsAAsIAAwcGeEfsdNWEZ5dStSkE'
sticker_bobeira1 = 'CAACAgEAAxkBAAEYWgljLRfNUHhEteQG3FwpPHOU1cL_TAACjwEAAljYEUSUGgHvT6acRSkE'
sticker_bobeira2 = 'CAACAgEAAxkBAAEYWhJjLRmRuis-_URX7J7EyS8E9ehRvwACBQEAAmZPeUeVJPXPvaNuHCkE'
sticker_bobeira3 = 'CAACAgEAAxkBAAEYWhVjLRm1wnOw4I8PR_MKmjBXN-gCCAACLQEAAmBveEelGZ3x9j49yCkE'
sticker_win = 'CAACAgEAAxkBAAEYWg1jLRj9uJvALP_TGieiU2FeX21jJAACYgEAAqWT8EZTyuWYlMLxDCkE'
sticker_win_g1 = 'CAACAgEAAxkBAAEYWg9jLRlINpDqH9zDy162_j1VVEiGKgACWgEAAuXv-EY4vv3kfOz5yikE'
sticker_win_g2 = ''


# RELATÓRIO DIÁRIO
def relaDiario():
    global placar
    global resultados_sinais
    global data_resultado
    global placar_win
    global placar_semGale
    global placar_gale1
    global placar_gale2
    global placar_gale3
    global placar_loss


    # PLACAR CONSOLIDADO
    try:
        placar_1 = bot.send_message(1476864287,"📊 Resultados do dia "+data_resultado+"\n==============================\n")
        placar_2 = bot.send_message(1476864287,"😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%")
    
    except Exception as a:
        logger.error('Exception ocorrido no ' + repr(a))
        placar_1 = bot.send_message(1476864287,"📊 Resultados do dia "+data_resultado+"\n==============================\n")
        placar_2 = bot.send_message(1476864287,"😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%")



    # ZERANDO PLACAR E ATUALIZANDO A LISTA DE ESTRATEGIAS DIARIAS
    # Resetando placar Geral (placar geral) e lista de estratégia diária
    placar_win = 0
    placar_semGale= 0
    placar_gale1= 0
    placar_gale2= 0
    placar_gale3= 0
    placar_loss = 0


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


# CAPTURANDO DATA E HORA DO SISTEMA
def capturarHorarioAtual():
    global data_atual
    global horario_atual
    global hora_atual
    global minuto_atual
    global horario_sistema

    data_atual = datetime.today().strftime('%Y-%m-%d')
    horario_atual = datetime.today().strftime('%H:%M')
    horario_sistema = datetime.today().strftime('%H:%M:%S')
    hora_atual = horario_atual[0:2]
    minuto_atual = horario_atual[3:]
    return data_atual, horario_atual, hora_atual, minuto_atual, horario_sistema


# GERANDO A PROBABILIDADE
def gerarProbabilidade():
    global velas_crash
    global cores_crashes
    global horarios_crash
    global prob_preto
    global prob_verde
    global parar
    global browser

    while True:
        try:
            # Validando se foi solicitado o stop do BOT
            if parar != 0:
                return
            else:
                pass

            #Chamado a função que captura o horario do sistema
            capturarHorarioAtual()

            cores_crashes = []
            velas_crash = []
            horarios_crash = []

            try:
                crashes = len(browser.find_elements_by_xpath('//*[@id="crashes"]/div')) #LEITURA DOS CRASHES
            except Exception as a:
                logger.error('Exception ocorrido no ' + repr(a))
                crashes = len(browser.find_elements_by_xpath('//*[@id="crashes"]/div')) #LEITURA DOS CRASHES

            #Percorrendo resultados
            for crash in range(1, crashes):
                cor = Color.from_string(browser.find_element_by_xpath(f'//*[@id="crashes"]/div[{crash}]/div[3]/span').value_of_css_property('background-color')).hex
                vela = browser.find_element_by_xpath(f'//*[@id="crashes"]/div[{crash}]/div[3]/span').text
                horario_crash = browser.find_element_by_xpath(f'//*[@id="crashes"]/div[{crash}]/div[3]/div').text

                #Se o hora atual for igual ou maior que o horado crash, mapeia a cor para gerar a probabilidade
                if hora_atual == horario_crash[:2]:

                    if cor == preto:
                        cores_crashes.append(preto)
                        velas_crash.append(vela)
                        horarios_crash.append(horario_crash)

                    elif cor == verde:
                        cores_crashes.append(verde)
                        velas_crash.append(vela)
                        horarios_crash.append(horario_crash)

                    else:
                        print('Não consegui definir a cor')
                    
                else:
                    break
            

            prob_preto = str(round(cores_crashes.count(preto)/len(cores_crashes)*100))
            prob_verde = str(round(cores_crashes.count(verde)/len(cores_crashes)*100))
            print('Total de velas analisadas:', len(cores_crashes), '| Contagem preto:', cores_crashes.count(preto), "| Contagem Verde:", cores_crashes.count(verde), "| Probabilidade: preto:", str(round(cores_crashes.count(preto)/len(cores_crashes)*100)).replace('.0',""),"% verde:", str(round(cores_crashes.count(verde)/len(cores_crashes)*100)).replace('.0',""),"%")
            print('====================================================================')
            #return prob_preto, prob_verde
            break
        
        except:
            continue


# IDENTIFICANDO A MENOR VELA
def pegarMenorVela():
    global pos_vela
    global parar


    # Validando se foi solicitado o stop do BOT
    if parar != 0:
        return
    else:
        pass

    mv = float(10000)
    for v in enumerate(velas_crash):
        if float(v[1].replace('X',"")) <= mv:
            mv = float(v[1].replace('X',""))
            pos_vela = v[0]
            
    return pos_vela


# FAZENDO BACKTEST COM CRASHES ANTERIORES APLICANDO A ESTRATÉGIA
def gerarBacktest():
    global horario_alerta
    global horario_sinal
    global ultimo_horario_resultado
    global dois_minutos
    global parar
    global contador_outra_oportunidade
    global horario_menor_vela


    # Validando se foi solicitado o stop do BOT
    if parar != 0:
        return
    else:
        pass

    
    horario_menor_vela = datetime.strptime(horarios_crash[pos_vela], '%H:%M:%S')
    um_minuto = timedelta(minutes=1)
    dois_minutos = timedelta(minutes=2)
    tres_minutos = timedelta(minutes=3)

    horario_alerta = (horario_menor_vela + dois_minutos).strftime('%H:%M:%S')
    horario_sinal = (horario_menor_vela + tres_minutos).strftime('%H:%M:%S')
   
    backtest = []
    horario_resultados = []
    contador_horario_lista = 0
    contador_passagem = 0
    win = 0
    proximo_sinal = horario_sinal #variavel que começa com o proximo horario após o sinal da menor vela


    for crash in reversed(range(0, pos_vela)):
        try:
            #Lógica para verificar se existe o horario somado+3. Se não tiver, acrescenta+1 no horario do proximo sinal
            if contador_passagem == 0:
                contador_passagem+=1
                for horario_crash in horarios_crash:
                    if proximo_sinal[:-3] == horario_crash[:-3]:
                        contador_horario_lista+=1
                        break
                    else:
                        continue
            
                if contador_horario_lista == 0:
                    proximo_sinal = (datetime.strptime(proximo_sinal,'%H:%M:%S') + um_minuto).strftime('%H:%M:%S')


           
            #Se o horario do sinal menor+3 minutos for igual horario do proximo sinal, pega o resultado(Win,Loss)
            if proximo_sinal[:-3] == horarios_crash[crash][:-3]:
                #Se o horario corresponder com a estratégia, valida se o crash foi verde(win), se não faz MG2
                if cores_crashes[crash] == '#04d47c' or velas_crash[crash] >= '1.50X':
                    backtest.append('win')
                    horario_resultados.append(horarios_crash[crash])
                    win += 1
                    contador_passagem = 0
                    contador_horario_lista = 0
                    proximo_sinal = datetime.strptime(horarios_crash[crash],'%H:%M:%S')
                    proximo_sinal = (proximo_sinal + tres_minutos).strftime('%H:%M:%S')
                    continue

                if cores_crashes[crash-1] == '#04d47c' or velas_crash[crash] >= '1.50X':
                    backtest.append('win-g1')
                    horario_resultados.append(horarios_crash[crash-1])
                    win += 1
                    contador_passagem = 0
                    contador_horario_lista = 0
                    proximo_sinal = datetime.strptime(horarios_crash[crash-1],'%H:%M:%S')
                    proximo_sinal = (proximo_sinal + tres_minutos).strftime('%H:%M:%S')
                    continue
                
                if cores_crashes[crash-2] == '#04d47c' or velas_crash[crash] >= '1.50X':
                    backtest.append('win-g2')
                    horario_resultados.append(horarios_crash[crash-2])
                    win += 1
                    contador_passagem = 0
                    contador_horario_lista = 0
                    proximo_sinal = datetime.strptime(horarios_crash[crash-2],'%H:%M:%S')
                    proximo_sinal = (proximo_sinal + tres_minutos).strftime('%H:%M:%S')
                    continue

                else:
                    backtest.append('loss')
                    horario_resultados.append(horarios_crash[crash-2])
                    contador_passagem = 0
                    contador_horario_lista = 0
                    proximo_sinal = datetime.strptime(horarios_crash[crash-2],'%H:%M:%S')
                    proximo_sinal = (proximo_sinal + tres_minutos).strftime('%H:%M:%S')
                    continue


        except:
            print('Backtest não está disponível no momento, tente novamente mais tarde.')
    
    try:
        ultimo_horario_resultado = horario_resultados[-1]
    except:
        print('Não tivemos resultados até o momento. Utilizando o horario da menor vela como base')
        ultimo_horario_resultado = horario_menor_vela.strftime('%H:%M:%S')


    if contador_outra_oportunidade == 0:
        try:
            backteste_telegram = bot.send_message(int(id_usuario.replace('[','').replace(']','')),'Resultado do Backtest:\n ========================= \n ⏲ ' + str(horario_menor_vela.strftime('%H:%M:%S')) +' - ' + str(ultimo_horario_resultado) + '\n 🚦 Quantidade de sinais - '+ str(len(backtest)) + '\n 🏆 Win - ' + str(backtest.count('win')) + '\n 🥇 WinG1 - ' + str(backtest.count('win-g1')) + '\n 🥈 WinG2 - ' + str(backtest.count('win-g2')) + '\n 😭 Loss - ' + str(backtest.count('loss')) + '\n ========================= \n 🎯 Assertividade - ' + str(round(win/len(backtest)*100,1))+'%')
            print('\nResultado do Backtest:\n Quantidade de sinais -->', len(backtest),'\n Win -->', backtest.count('win'),'\n WinG1 -->', backtest.count('win-g1'),'\n WinG2 -->', backtest.count('win-g2'),'\n Loss -->', backtest.count('loss'),'\n Assertividade -->',str(round(win/len(backtest)*100,1)),'%')
            print('====================================================================')
        except:
            backteste_telegram = bot.send_message(int(id_usuario.replace('[','').replace(']','')),'Resultado do Backtest:\n ========================= \n ⏲ ' + str(horario_menor_vela.strftime('%H:%M:%S')) +' - ' + str(ultimo_horario_resultado) + '\n 🚦 Quantidade de sinais - '+ str(len(backtest)) + '\n 🏆 Win - ' + str(backtest.count('win')) + '\n 🥇 WinG1 - ' + str(backtest.count('win-g1')) + '\n 🥈 WinG2 - ' + str(backtest.count('win-g2')) + '\n 😭 Loss - ' + str(backtest.count('loss')) + '\n ========================= \n 🎯 Assertividade - 0%')
            print('\nResultado do Backtest:\n Quantidade de sinais -->', len(backtest),'\n Win -->', backtest.count('win'),'\n WinG1 -->', backtest.count('win-g1'),'\n WinG2 -->', backtest.count('win-g2'),'\n Loss -->', backtest.count('loss'),'\n Assertividade --> 0%')
            print('====================================================================')

# 1708255972 id cliente
# 1476864287 id DEV
    
    return ultimo_horario_resultado
    

# ENVIADO ALERTA NO CANAL TELEGRAM
def enviarAlertaTelegram():
    global alerta_free
    global alerta_vip

    try:
        if canal_free != '':
            alerta_free = bot.send_sticker(canal_free, sticker=sticker_alerta)
        
        if canal_vip !='':
            alerta_vip = bot.send_sticker(canal_vip, sticker=sticker_alerta)
    
    except:
        print('Erro ao enviar Alerta -- Contate o Desenvolvedor')


# ENVIADO SINAL NO CANAL TELEGRAM
def enviarSinalTelegram():
    global alerta_free
    global alerta_vip
    global table
    global message_canal_free
    global message_canal_vip

    headers = ['🚀 Entrada Confirmada 🚀                                                    ']

    data = [
        ['🔝 Entrar Agora'                    ],
        ["💻 <a href='https://blaze.com/pt/games/crash'>Crash</a>"   ],
        ['⏱ Saída: 1.50x / 2.0x'],
        ['🗝 Até Duas Proteções'],
        ['✏ Cuidado com o Gerenciamento ✏']
    ]
    
    table = columnar(data, headers, no_borders=True)

    try:
        # deletando o alerta
        # enviando sinal Telegram
        if canal_free != '':
            bot.delete_message(canal_free, alerta_free.message_id)
            message_canal_free = bot.send_message(canal_free,table, parse_mode='HTML', disable_web_page_preview=True)

        if canal_vip !='':
            bot.delete_message(canal_vip, alerta_vip.message_id)
            message_canal_vip = bot.send_message(canal_vip,table, parse_mode='HTML', disable_web_page_preview=True)

    except:
        pass


# VALIDANDO SE O SINAL ENVIADO FOI WIN OU LOSS
def validarSinalEnviado():
    global table
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


    aguardaSinalAcabar = 0
    contador_cash = 0
    ultima_vela = browser.find_element_by_xpath(f'//*[@id="crashes"]/div[1]/div[3]/span').text

    while contador_cash <= 2:

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass

        # Validando data para envio do relatório diário
        validaData()

        try:

            vela_atual = browser.find_element_by_xpath(f'//*[@id="crashes"]/div[1]/div[3]/span').text
            horario_crash_atual = browser.find_element_by_xpath(f'//*[@id="crashes"]/div[1]/div[3]/div').text


            # Funcionalidade que valida se está capturando a mesma vela.
            if ultima_vela != vela_atual:
                vela_repetida = 0
                if aguardaSinalAcabar == 0:
                    aguardaSinalAcabar = 1
                    ultima_vela = vela_atual
                    continue
                
                else:
                    pass

        
            elif browser.find_element_by_xpath(f'//*[@id="crashes"]/div[1]/div[3]/span').text == browser.find_element_by_xpath(f'//*[@id="crashes"]/div[2]/div[3]/span').text and vela_repetida == 0:
                if validador < 3:
                    time.sleep(1)
                    print('entrei aqui pq acho que o valor é repetido.. Validando: ', validador)
                    validador += 1
                    continue
                else:
                    print('MESMO RESULTADO DUAS VEZES NESSE MOMENTO')
                    vela_repetida +=1
                    validador = 0
                    pass
            
            else:
                continue



            # VALIDANDO WIN OU LOSS
            print(vela_atual, '-', horario_crash_atual)                                   

            if vela_atual >= '1.50X':
                
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


                if contador_cash == 1:
                    print('WIN GALE1')
                    stop_loss.append('win')

                    # Preenchendo relatório
                    placar_win+=1
                    placar_gale1+=1
                    resultados_sinais = placar_win + placar_loss
                    print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
                    #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)



                if contador_cash == 2:
                    print('WIN GALE2')
                    stop_loss.append('win')
                    
                    # Preenchendo relatório
                    placar_win+=1
                    placar_gale2+=1
                    resultados_sinais = placar_win + placar_loss
                    print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
                    #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)
                    
            

                if contador_cash == 3:
                    print('WIN gale3')
                    stop_loss.append('win')

                    # Preenchendo relatório
                    placar_win+=1
                    placar_gale3+=1
                    resultados_sinais = placar_win + placar_loss
                    print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
                    #bot.edit_message_text("📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade "+ str(round(placar_win / resultados_sinais*100, 1)).replace('.0',"")+"%", placar.chat.id, placar.message_id)

    


                # editando mensagem enviada e enviando sticker
                try:
                    if canal_free != '':
                        
                        bot.edit_message_text(table +"  \n============================== \n              WINNNN ✅ --- 🎯 "+ vela_atual, message_canal_free.sender_chat.id, message_canal_free.message_id, parse_mode='HTML', disable_web_page_preview=True)   
                        
                        if contador_cash == 0:
                            bot.send_sticker(canal_free, sticker=sticker_win)

                        elif contador_cash == 1:
                            bot.send_sticker(canal_free, sticker=sticker_win_g1)
                        
                        else:
                            bot.send_message(canal_free, '*💵💵 WIN NO GALE2 💵💵*\nESSA FOI POR POUCO !❤️‍🔥')
                    

                    if canal_vip != '':
                        bot.edit_message_text(table +"  \n============================== \n              WINNNN ✅ --- 🎯 "+ vela_atual, message_canal_vip.sender_chat.id, message_canal_vip.message_id, parse_mode='HTML', disable_web_page_preview=True)   
                        
                        if contador_cash == 0:
                            bot.send_sticker(canal_vip, sticker=sticker_win)
                        
                        elif contador_cash == 1:
                            bot.send_sticker(canal_vip, sticker=sticker_win_g1)
                        
                        else:
                            bot.send_message(canal_vip, '*💵💵 WIN NO GALE2 💵💵*\nESSA FOI POR POUCO !❤️‍🔥')



                    # CONDIÇÃO PARA ENVIAR O GIF DO PATO E FIGURINHA DE BOBEIRA
                    if stop_loss.count('win') == 5 or stop_loss.count('win') == 10 or stop_loss.count('win') == 15:
                        try:

                            if canal_free !='':
                                bot.send_video(canal_free, video=open('money-donald-duck.mp4', 'rb'), supports_streaming=True)
                                bot.send_sticker(canal_free, sticker=sticker_bobeira1)
                                bot.send_sticker(canal_free, sticker=sticker_bobeira2)
                                bot.send_sticker(canal_free, sticker=sticker_bobeira3)


                            if canal_vip !='':
                                bot.send_video(canal_vip, video=open('money-donald-duck.mp4', 'rb'), supports_streaming=True)
                                bot.send_sticker(canal_vip, sticker=sticker_bobeira1)
                                bot.send_sticker(canal_vip, sticker=sticker_bobeira2)
                                bot.send_sticker(canal_vip, sticker=sticker_bobeira3)


                        except:
                            pass


                except:
                    pass
                
                print('==================================================')
                validador_sinal = 0
                contador_cash = 0
                ultimo_horario_resultado = horario_crash_atual
                aplicarEstrategia()

            
            else:
                print('LOSSS')
                print('==================================================')
                contador_cash+=1
                if contador_cash <= 2:
                    ultima_vela = vela_atual ####################
                    validador = 0
                else:
                    pass

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
                bot.edit_message_text(table +"\n============================== \n              LOSS ✖", message_canal_free.sender_chat.id, message_canal_free.message_id, parse_mode='HTML', disable_web_page_preview=True)
                bot.send_sticker(canal_free, sticker=sticker_loss)


            if canal_vip !='':
                bot.edit_message_text(table +"\n============================== \n              LOSS ✖", message_canal_vip.sender_chat.id, message_canal_vip.message_id, parse_mode='HTML', disable_web_page_preview=True)
                bot.send_sticker(canal_vip, sticker=sticker_loss)
            

            # Preenchendo relatório
            resultados_sinais = placar_win + placar_loss
            print("Placar Atual: WIN ",placar_win," X ",placar_loss," LOSS --- Assertividade de: ", placar_win / resultados_sinais,"%")
        

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
        ultimo_horario_resultado = horario_crash_atual
        aplicarEstrategia()



# APLICANDO A ESTRATEGIA 
def aplicarEstrategia():
    global ultimo_horario_resultado
    global validador_sinal
    global contador_outra_oportunidade
    global horario_ultimo_crash

    print(ultimo_horario_resultado)
    
    while True:

        # Validando se foi solicitado o stop do BOT
        if parar != 0:
            break
        else:
            pass


        # Atualizando o horario do sistema
        capturarHorarioAtual()

        horario_sinal = (datetime.strptime(ultimo_horario_resultado,'%H:%M:%S') + dois_minutos).strftime('%H:%M:%S')
        horario_sinal = horario_sinal[:6]+'59'
        horario_alerta = horario_sinal[:6]+'40'

        horario_ultimo_crash = browser.find_element_by_xpath(f'//*[@id="crashes"]/div[1]/div[3]/div').text
        ultima_vela = browser.find_element_by_xpath(f'//*[@id="crashes"]/div[1]/div[3]/span').text

        if horario_sistema >= horario_alerta and horario_sistema > horario_sinal:
            if contador_outra_oportunidade == 0:
                print('Horário do Sinal já passou. Aguardando outra oportunidade.')
                contador_outra_oportunidade += 1

            gerarProbabilidade()
            pegarMenorVela()
            gerarBacktest()
            aplicarEstrategia()

        if horario_sistema >= horario_alerta and horario_sistema < horario_sinal:
            # Validando probabilidade do verde antes de enviar o alerta
            gerarProbabilidade()

            # Se a probabilidade do verde for igual ou maior que o preto, envia alerta e sinal Telegram
            if prob_preto < '70':
                #ENVIANDO PROBABILIDADE TELEGRAM
                try:

                    if canal_free != '': 
                        bot.send_message(canal_free,'⏲ '+ str(horario_menor_vela.strftime('%H:%M:%S')) +' - ' + str(horario_ultimo_crash) + '\n =====================\n 🎰 Total de Crash - ' + str(len(cores_crashes)) + '\n ⬛ - ' + str(cores_crashes.count(preto)) + ' | ' + str(round(cores_crashes.count(preto)/len(cores_crashes)*100)).replace('.0',"") + "% \n 🟩 - " + str(cores_crashes.count(verde)) + ' | ' + str(round(cores_crashes.count(verde)/len(cores_crashes)*100)).replace('.0',"") + "%")

                    if canal_vip != '':
                        bot.send_message(canal_vip,'⏲ '+ str(horario_menor_vela.strftime('%H:%M:%S')) +' - ' + str(horario_ultimo_crash) + '\n =====================\n 🎰 Total de Crash - ' + str(len(cores_crashes)) + '\n ⬛ - ' + str(cores_crashes.count(preto)) + ' | ' + str(round(cores_crashes.count(preto)/len(cores_crashes)*100)).replace('.0',"") + "% \n 🟩 - " + str(cores_crashes.count(verde)) + ' | ' + str(round(cores_crashes.count(verde)/len(cores_crashes)*100)).replace('.0',"") + "%")

                except:
                    pass


                print('ENVIANDO ALERTA TELEGRAM')
                validador_sinal = 1
                contador_outra_oportunidade = 0
                print('====================================================================')
                enviarAlertaTelegram()

                while True:
                    # Validando se foi solicitado o stop do BOT
                    if parar != 0:
                        break
                    else:
                        pass

                    capturarHorarioAtual()
                    if horario_sistema >= horario_sinal:
                        print('ENVIANDO SINAL TELEGRAM')
                        print('====================================================================')
                        enviarSinalTelegram()
                        validarSinalEnviado()


            else:
                print('Probabilidade não está a favor pra enviar o sinal...Aguardando o próximo horário.')
                ultimo_horario_resultado = horario_ultimo_crash
                print('====================================================================')
                continue
        
            



#________________________________________________________________________________________ TELEGRAM__________________________________________________________________________________#


print('###################### AGUARDANDO COMANDOS ######################')

global canal
global bot
global placar_win
global placar_semGale
global placar_gale1
global placar_gale2
global placar_gale3
global placar_loss
global resultados_sinais

#CHAVE_API = '5590315584:AAFvdXwCsLAwbDwJbSitVcPSgzKQQYO-748' # DEV
CHAVE_API = '5798408552:AAF-HyDxLlj_07r-O6JgtKT5HZetxtAeKJ4' # PRODUÇÃO

bot = telebot.TeleBot(CHAVE_API)

# PLACAR
placar_win = 0
placar_semGale= 0
placar_gale1= 0
placar_gale2= 0
placar_gale3= 0
placar_loss = 0
resultados_sinais = placar_win + placar_loss
contador = 0
botStatus = 0
contador_passagem = 0
validador_sinal = 0
parar = 0



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
    global parar
    global browser

    while True:
        try:
            parar = 1
            return 

        except:
            continue




@bot.message_handler(commands=['🧮 Percentual Cores'])
def enviarPercentualCores(message):
    global cores_crashes
    global prob_preto
    global prob_verde
    global validador_sinal
    global horario_menor_vela
    global horario_ultimo_crash

    if validador_sinal != 0:

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start', '✅ Ativar Bot', '♻ Resetar Resultados', '📊 Placar Atual', '🧮 Percentual Cores', '🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Estou validando um Sinal. Tente novamente em alguns instanstes.", reply_markup=markup)
    else:

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start', '✅ Ativar Bot', '♻ Resetar Resultados', '📊 Placar Atual', '🧮 Percentual Cores', '🛑 Pausar Bot')

        prob = bot.reply_to(message, '⏲ '+ str(horario_menor_vela.strftime('%H:%M:%S')) +' - ' + str(horario_ultimo_crash) + '\n =====================\n 🎰 Total de Crash - ' + str(len(cores_crashes)) + '\n ⬛ - ' + str(cores_crashes.count(preto)) + ' | ' + str(round(cores_crashes.count(preto)/len(cores_crashes)*100)).replace('.0',"") + "% \n 🟩 - " + str(cores_crashes.count(verde)) + ' | ' + str(round(cores_crashes.count(verde)/len(cores_crashes)*100)).replace('.0',"") + "%", reply_markup=markup)
        


@bot.message_handler(commands=['📊 Placar Atual'])
def placar_atual(message):
    global placar
    global resultados_sinais

    #Init keyboard markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup = markup.add('/start', '✅ Ativar Bot', '♻ Resetar Resultados', '📊 Placar Atual', '🧮 Percentual Cores', '🛑 Pausar Bot')

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
    markup = markup.add('/start', '✅ Ativar Bot', '♻ Resetar Resultados', '📊 Placar Atual', '🧮 Percentual Cores', '🛑 Pausar Bot')
    
    message_final = bot.reply_to(message, "🤖♻ Resultados resetados com sucesso ✅", reply_markup=markup)




@bot.message_handler(commands=['🛑 Pausar_bot'])
def pausar(message):
    global botStatus
    global validador_sinal
    global browser
    global parar

    if validador_sinal != 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start', '✅ Ativar Bot', '♻ Resetar Resultados', '📊 Placar Atual', '🧮 Percentual Cores', '🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Estou validando um Sinal. Tente novamente em alguns instanstes.", reply_markup=markup)

    elif botStatus == 0:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start', '✅ Ativar Bot', '♻ Resetar Resultados', '📊 Placar Atual', '🧮 Percentual Cores', '🛑 Pausar Bot')

        message_final = bot.reply_to(message, "🤖⛔ Bot já está pausado ", reply_markup=markup)

    else:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start', '✅ Ativar Bot', '♻ Resetar Resultados', '📊 Placar Atual', '🧮 Percentual Cores', '🛑 Pausar Bot')

        print('\n\n')
        print('Pausar Bot')
        print('Parando o Bot....\n')
        botStatus = 0
        parar = 1
        #pausarBot()

        message_final = bot.reply_to(message, "🤖 Ok! Bot pausado 🛑", reply_markup=markup)
        
        print('###################### AGUARDANDO COMANDOS ######################')
        
        return




@bot.message_handler(commands=['start'])
def start(message):

    if str(message.chat.id) in id_usuario:
       
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start', '✅ Ativar Bot', '♻ Resetar Resultados', '📊 Placar Atual', '🧮 Percentual Cores', '🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message, "🤖 Bot Crash Machine Man Iniciado! ✅ Escolha uma opção 👇",
                                reply_markup=markup)
        
        #Here we assign the next handler function and pass in our response from the user. 
        bot.register_next_step_handler(message_opcoes, opcoes)
    
    else:
        message_error = bot.reply_to(message, "🤖 Você não tem permissão para acessar este Bot ❌🚫")





@bot.message_handler()
def opcoes(message_opcoes):

    if message_opcoes.text in ['✅ Ativar Bot']:
        global botStatus
        global message_canal

        print('Ativar Bot')

        if botStatus == 1:

            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('/start', '✅ Ativar Bot', '♻ Resetar Resultados', '📊 Placar Atual', '🧮 Percentual Cores', '🛑 Pausar Bot')

            message_canal = bot.reply_to(message_opcoes, "🤖⛔ Bot já está ativado",
                                reply_markup=markup)

        else:
            #Init keyboard markup
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup = markup.add('◀ Voltar', '📋 Enviar sinais Canal FREE', '🏆 Enviar sinais Canal VIP', '📋🏆 Enviar sinais Canal FREE & VIP')

            message_canal = bot.reply_to(message_opcoes, "🤖 Escolha para onde enviar os sinais 👇",
                                    reply_markup=markup)
            
            bot.register_next_step_handler(message_canal, escolher_canal)

    
    if message_opcoes.text in['📊 Placar Atual']:
        print('Placar Atual')
        placar_atual(message_opcoes)



    if message_opcoes.text in ['♻ Resetar Resultados']:
        print('Resetar Resultados')
        resetarResultados(message_opcoes)



    if message_opcoes.text in ['🛑 Pausar Bot']:
        print('Pausar Bot')
        pausar(message_opcoes)

    
    if message_opcoes.text in ['🧮 Percentual Cores']:
        print('Percentual de cores')
        enviarPercentualCores(message_opcoes)

    

    

@bot.message_handler(content_types=['text'])
def escolher_canal(message_canal):
    global canal_free
    global canal_vip
    global placar
    global estrategia
    global stop_loss
    global botStatus
    global parar
    global reladiarioenviado
    global contador_outra_oportunidade
    global browser


    if message_canal.text in ['◀ Voltar']:
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start', '✅ Ativar Bot', '♻ Resetar Resultados', '📊 Placar Atual', '🧮 Percentual Cores', '🛑 Pausar Bot')

        message_opcoes = bot.reply_to(message_canal, "🤖 Escolha uma opção 👇",
                                reply_markup=markup)


    if message_canal.text in ['📋 Enviar sinais Canal FREE']:

        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start', '✅ Ativar Bot', '♻ Resetar Resultados', '📊 Placar Atual', '🧮 Percentual Cores', '🛑 Pausar Bot')

        message_final = bot.reply_to(message_canal, "🤖 Ok! Ligando Bot no Canal "+ str(message_canal.text.split(' ')[4:]), reply_markup = markup)
        
        print("Iniciar e enviar sinais no Canal FREE ")


        canal_free = free
        canal_vip = ''
        stop_loss = []
        botStatus = 1
        reladiarioenviado = 0
        contador_outra_oportunidade = 0
        parar=0


        #placar = bot.send_message(message_canal.chat.id,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%")

        print('#########################  INICIANDO AS ANÁLISES  #########################')
        print()
        gerarProbabilidade()
        pegarMenorVela()
        gerarBacktest()
        aplicarEstrategia()

        
    
    if message_canal.text in ['🏆 Enviar sinais Canal VIP']:
        
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start', '✅ Ativar Bot', '♻ Resetar Resultados', '📊 Placar Atual', '🧮 Percentual Cores', '🛑 Pausar Bot')

        message_final = bot.reply_to(message_canal, "🤖 Ok! Ligando Bot no Canal "+ str(message_canal.text.split(' ')[4:]), reply_markup = markup)

        print("Iniciar e enviar sinais no Canal VIP ")

        canal_free = ''
        canal_vip = vip
        stop_loss = []
        botStatus = 1
        reladiarioenviado = 0
        contador_outra_oportunidade = 0
        parar=0

        #placar = bot.send_message(message_canal.chat.id,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%")

        print('#########################  INICIANDO AS ANÁLISES  #########################')
        print()
        gerarProbabilidade()
        pegarMenorVela()
        gerarBacktest()
        aplicarEstrategia()


    if message_canal.text in ['📋🏆 Enviar sinais Canal FREE & VIP']:
        
        #Init keyboard markup
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = markup.add('/start', '✅ Ativar Bot', '♻ Resetar Resultados', '📊 Placar Atual', '🧮 Percentual Cores', '🛑 Pausar Bot')

        message_final = bot.reply_to(message_canal, "🤖 Ok! Ligando Bot no Canal "+ str(message_canal.text.split(' ')[4:]), reply_markup = markup)
        print("Iniciar e enviar sinais no Canal FREE & VIP ")

        canal_free = free
        canal_vip = vip
        stop_loss = []
        botStatus = 1
        reladiarioenviado = 0
        contador_outra_oportunidade = 0
        parar=0

        #placar = bot.send_message(message_canal.chat.id,"📊 Placar Atual:\n==================\n😍 WIN - "+str(placar_win)+"\n🏆 WIN S/ GALE - "+str(placar_semGale)+"\n🥇 WIN GALE1 - "+str(placar_gale1)+"\n🥈 WIN GALE2 - "+str(placar_gale2)+"\n🥉 WIN GALE3 - "+str(placar_gale3)+"\n😭 LOSS - "+str(placar_loss)+"\n==================\n🎯 Assertividade - 0%")

        print('#########################  INICIANDO AS ANÁLISES  #########################')
        print()
        gerarProbabilidade()
        pegarMenorVela()
        gerarBacktest()
        aplicarEstrategia()





bot.infinity_polling()


