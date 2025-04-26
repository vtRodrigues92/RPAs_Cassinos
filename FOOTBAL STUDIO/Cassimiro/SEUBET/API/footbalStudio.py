from selenium import webdriver
import time
import warnings
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import telebot
from telegram.ext import *
from telebot import *
import ast
import os
import requests, json


print()
print('                                #################################################################')
print('                                ################## BOT FUTEBOL STUDIO PT-BR  ####################')
print('                                #################################################################')
print('                                ##################### SEJA BEM VINDO ############################')
print('                                #################################################################')
print('                                ############# DESENVOLVIDO POR VICTOR RODRIGUES #################')
print('                                #################################################################\n')
print('Versão = 1.0.0')
print('Ambiente: Produção\n\n\n')



def pegar_evosessionid():
    #LOGIN
    URL = 'https://luva.bet/api/client/clients:login-with-form'

    header = {
        "method":"POST",
        "path":"/api/client/clients:login-with-form",
        "scheme":"https",
        "accept":"application/json",
        "accept-language":"pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control":"no-cache",
        "content-length":"3404",
        "cookie":"SessionToken=dde75a68-9807-4501-89d7-e27f30c79641; __cf_bm=EIJg69_zGBiYI.AYKoK09nuDr8HmHF6r7yypys3J4Lc-1731679606-1.0.1.1-PXmH3dIsQBZ2h_09J38rmVLB_qiAaWVEJRRGECoYHYlJWxOMELakoTfSNg0ejLf0run7XdwXBo5sP34vwFNwNQ; cf_clearance=.THCiR.Fz5THIwMro5vrNjUKUukKjvY8ZnLwdfVB8Yg-1731679607-1.2.1.1-3POwESOVeOYe85AbVU_LdckZ_H0Sp_3qvSCFOnbWHF5uJr50IDjAzEJddLf2TnBGfMhrAyENMQWOj43AMXHIcvM0BHyF.S8kIa76csLeZUTEAYT7rdswldTH64KSGqMmI.v4LlPcngMRrX4LYYZIk80.bymyaH_kVtd_kSWumXKV4ew2TqEnOPHSN1Chvc8oTkU8xO9CBbSZhWK7C0w8oRBxE64_FChzH4yVoeDaVuAnhOdlJEuymR33Kfpc4gfRWdxuBu0VaH42BF9O7zy7PiPmSCXuh4YaMOeHIhEAY6AbsLNsV.VLL9PcW8x8UwKWBVhPh89YPtFBEehD0cIpfkhIF8MKwGA8LjjwOqXVg0Vp5KuJbIiM_xuXRBS6YvdYoVEjRRP8FZ8slVFiJ19F_A; _gcl_au=1.1.172133234.1731679608; _ga=GA1.1.1145380204.1731679609; _clck=yqgzzw%7C2%7Cfqw%7C0%7C1780; FPID=FPID2.2.Se%2FgfIg3TSebvlRBilQzLpd%2FT%2FaVdKpEW5mDP6KpY9A%3D.1731679609; FPLC=IqQWaZJDaGTJHdGZ%2BSIT8t44t7Y7Cvg85xgHeiaEFK7ebYJCDnb4HbM7UZkLAMqgMpVj0X3Qdm%2FAmClh%2Fh7p2BdEHtTIg2yjePn9rvvxdXAW7MdFv7iDuFBLb7j%2BcQ%3D%3D; _fbp=fb.1.1731679609184.1236395910; _sp_srt_ses.ae99=*; __smartico_ls_id=ea204445-5f4c-4ae2-87ab-07884ddb3280; __smartico_ls_create_t=1731679797379; _gtmeec=eyJlbSI6ImI2MDI0M2M5ZGNmZTgwMTk4ZmZhODcyZWM3MWM0OGQxZTc5MWVhNGQ2MjdlMjRiYmJiN2FhODI3NTdkM2MxZjAiLCJwaCI6IjA3MWZkNDVmYjFlNTYwMmU0MjhlNGU0NzFkNjI5ZGU3YjgzN2ZjNjg0OTFhNDc4ZTg5YmJlNTk5NGZkNGViODEiLCJjdCI6ImYxYjVjYjgxM2MyMjZmZDI1ODNlZGYyNzVmNTFiZmZmMGE3MGMxNjJjOWVlODFiZGE1OTVlMGU1ZGEyMTNlNGYiLCJzdCI6Ijg2MDQ4MThhZjRkMjFiYmZjMDhhODJhNjhmM2FiNDY2NmQ2ODkzYWFmODgxMzQ1MDQ1MzAyODJkOWZhZTgxOGQiLCJjb3VudHJ5IjoiODg1MDM2YTBkYTNkZmYzYzNlMDViYzc5YmY0OTM4MmIxMmJjNTA5ODUxNGVkNTdjZTA4NzVhYmExYWEyYzQwZCIsImV4dGVybmFsX2lkIjoiMTYyODQ5ODIzNSJ9; user_id=1628498235; _ga_TXYW9LGGJG=GS1.1.1731679608.1.1.1731679923.0.1.1336043890; _sp_srt_id.ae99=74dcb8f6-6e74-4c25-94d5-db481077d095.1731679610.1.1731679924..9a7f7874-1f3b-4ca7-b6af-4b22794f9984....0; __smartico_ls_use_t=1731680026997; _clsk=1bresn7%7C1731680034982%7C18%7C0%7Ck.clarity.ms%2Fcollect; _ga_G55NSV822S=GS1.1.1731679625.1.1.1731680044.0.0.1222638944; _ga_FHT1R7RSLF=GS1.1.1731679609.1.1.1731680044.2.0.1536170679; crmback-session=U2FsdGVkX188PguTwsCiQsYkAtv5zvcBZNl0+GIujIBOQRpG57kset+YxDGtnaR8qDz4F4/3tdlKQSn0AYECBQ==",
        "authority":"luva.bet",
        "device":"desktop",
        "origin":"https://luva.bet",
        "referer":"https://luva.bet/casino?cmd=signin&path=loginMultichannel",
        "sec-ch-ua":'"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile":"?0",
        "sec-ch-ua-platform":"Windows",
        "sec-fetch-dest":"empty",
        "sec-fetch-mode":"cors",
        "sec-fetch-site":"same-origin",
        "Content-Type": "application/json",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "version":"3.17.12",
        "x-locale":"BR_PT",
        "x-project-id":"136"
    }

    payload = '{"id":"4155","values":{"CAPTCHA_INPUT":"","MULTICHANNEL":"victor.o.rodrigues11@gmail.com","PASSWORD":"Fordbracom2024"},"fingerprint":"W3sia2V5IjoidXNlckFnZW50IiwidmFsdWUiOiJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvMTMxLjAuMC4wIFNhZmFyaS81MzcuMzYifSx7ImtleSI6IndlYmRyaXZlciIsInZhbHVlIjpmYWxzZX0seyJrZXkiOiJsYW5ndWFnZSIsInZhbHVlIjoicHQtQlIifSx7ImtleSI6ImNvbG9yRGVwdGgiLCJ2YWx1ZSI6MjR9LHsia2V5IjoiZGV2aWNlTWVtb3J5IiwidmFsdWUiOjh9LHsia2V5IjoiaGFyZHdhcmVDb25jdXJyZW5jeSIsInZhbHVlIjo4fSx7ImtleSI6InNjcmVlblJlc29sdXRpb24iLCJ2YWx1ZSI6Wzc2OCwxMzY2XX0seyJrZXkiOiJhdmFpbGFibGVTY3JlZW5SZXNvbHV0aW9uIiwidmFsdWUiOls3MjAsMTM2Nl19LHsia2V5IjoidGltZXpvbmVPZmZzZXQiLCJ2YWx1ZSI6MTgwfSx7ImtleSI6InRpbWV6b25lIiwidmFsdWUiOiJBbWVyaWNhL1Nhb19QYXVsbyJ9LHsia2V5Ijoic2Vzc2lvblN0b3JhZ2UiLCJ2YWx1ZSI6dHJ1ZX0seyJrZXkiOiJsb2NhbFN0b3JhZ2UiLCJ2YWx1ZSI6dHJ1ZX0seyJrZXkiOiJpbmRleGVkRGIiLCJ2YWx1ZSI6dHJ1ZX0seyJrZXkiOiJhZGRCZWhhdmlvciIsInZhbHVlIjpmYWxzZX0seyJrZXkiOiJvcGVuRGF0YWJhc2UiLCJ2YWx1ZSI6ZmFsc2V9LHsia2V5IjoiY3B1Q2xhc3MiLCJ2YWx1ZSI6Im5vdCBhdmFpbGFibGUifSx7ImtleSI6InBsYXRmb3JtIiwidmFsdWUiOiJXaW4zMiJ9LHsia2V5IjoicGx1Z2lucyIsInZhbHVlIjpbWyJQREYgVmlld2VyIiwiUG9ydGFibGUgRG9jdW1lbnQgRm9ybWF0IixbWyJhcHBsaWNhdGlvbi9wZGYiLCJwZGYiXSxbInRleHQvcGRmIiwicGRmIl1dXSxbIkNocm9tZSBQREYgVmlld2VyIiwiUG9ydGFibGUgRG9jdW1lbnQgRm9ybWF0IixbWyJhcHBsaWNhdGlvbi9wZGYiLCJwZGYiXSxbInRleHQvcGRmIiwicGRmIl1dXSxbIkNocm9taXVtIFBERiBWaWV3ZXIiLCJQb3J0YWJsZSBEb2N1bWVudCBGb3JtYXQiLFtbImFwcGxpY2F0aW9uL3BkZiIsInBkZiJdLFsidGV4dC9wZGYiLCJwZGYiXV1dLFsiTWljcm9zb2Z0IEVkZ2UgUERGIFZpZXdlciIsIlBvcnRhYmxlIERvY3VtZW50IEZvcm1hdCIsW1siYXBwbGljYXRpb24vcGRmIiwicGRmIl0sWyJ0ZXh0L3BkZiIsInBkZiJdXV0sWyJXZWJLaXQgYnVpbHQtaW4gUERGIiwiUG9ydGFibGUgRG9jdW1lbnQgRm9ybWF0IixbWyJhcHBsaWNhdGlvbi9wZGYiLCJwZGYiXSxbInRleHQvcGRmIiwicGRmIl1dXV19LHsia2V5Ijoid2ViZ2xWZW5kb3JBbmRSZW5kZXJlciIsInZhbHVlIjoiR29vZ2xlIEluYy4gKEludGVsKX5BTkdMRSAoSW50ZWwsIEludGVsKFIpIFVIRCBHcmFwaGljcyA2MjAgKDB4MDAwMDNFQTApIERpcmVjdDNEMTEgdnNfNV8wIHBzXzVfMCwgRDNEMTEpIn0seyJrZXkiOiJhZEJsb2NrIiwidmFsdWUiOmZhbHNlfSx7ImtleSI6Imhhc0xpZWRMYW5ndWFnZXMiLCJ2YWx1ZSI6ZmFsc2V9LHsia2V5IjoiaGFzTGllZFJlc29sdXRpb24iLCJ2YWx1ZSI6ZmFsc2V9LHsia2V5IjoiaGFzTGllZE9zIiwidmFsdWUiOmZhbHNlfSx7ImtleSI6Imhhc0xpZWRCcm93c2VyIiwidmFsdWUiOmZhbHNlfSx7ImtleSI6InRvdWNoU3VwcG9ydCIsInZhbHVlIjpbMCxmYWxzZSxmYWxzZV19LHsia2V5IjoiZm9udHMiLCJ2YWx1ZSI6WyJBcmlhbCIsIkFyaWFsIEJsYWNrIiwiQXJpYWwgTmFycm93IiwiQm9vayBBbnRpcXVhIiwiQm9va21hbiBPbGQgU3R5bGUiLCJDYWxpYnJpIiwiQ2FtYnJpYSIsIkNhbWJyaWEgTWF0aCIsIkNlbnR1cnkiLCJDZW50dXJ5IEdvdGhpYyIsIkNlbnR1cnkgU2Nob29sYm9vayIsIkNvbWljIFNhbnMgTVMiLCJDb25zb2xhcyIsIkNvdXJpZXIiLCJDb3VyaWVyIE5ldyIsIkdlb3JnaWEiLCJIZWx2ZXRpY2EiLCJJbXBhY3QiLCJMdWNpZGEgQnJpZ2h0IiwiTHVjaWRhIENhbGxpZ3JhcGh5IiwiTHVjaWRhIENvbnNvbGUiLCJMdWNpZGEgRmF4IiwiTHVjaWRhIEhhbmR3cml0aW5nIiwiTHVjaWRhIFNhbnMiLCJMdWNpZGEgU2FucyBUeXBld3JpdGVyIiwiTHVjaWRhIFNhbnMgVW5pY29kZSIsIk1pY3Jvc29mdCBTYW5zIFNlcmlmIiwiTW9ub3R5cGUgQ29yc2l2YSIsIk1TIEdvdGhpYyIsIk1TIFBHb3RoaWMiLCJNUyBSZWZlcmVuY2UgU2FucyBTZXJpZiIsIk1TIFNhbnMgU2VyaWYiLCJNUyBTZXJpZiIsIlBhbGF0aW5vIExpbm90eXBlIiwiU2Vnb2UgUHJpbnQiLCJTZWdvZSBTY3JpcHQiLCJTZWdvZSBVSSIsIlNlZ29lIFVJIExpZ2h0IiwiU2Vnb2UgVUkgU2VtaWJvbGQiLCJTZWdvZSBVSSBTeW1ib2wiLCJUYWhvbWEiLCJUaW1lcyIsIlRpbWVzIE5ldyBSb21hbiIsIlRyZWJ1Y2hldCBNUyIsIlZlcmRhbmEiLCJXaW5nZGluZ3MiLCJXaW5nZGluZ3MgMiIsIldpbmdkaW5ncyAzIl19LHsia2V5IjoiYXVkaW8iLCJ2YWx1ZSI6IjEyNC4wNDM0NzUyNzUxNjA3NCJ9XQ=="}'
    
    response = requests.post(URL, headers=header, data=payload)
    
    token_autorizacao = response.json()['token']

    
    #### ENTRANDO NO GAME
    #REQUISIÇÃO1
    URL = 'https://backoffice.mesk.bet/api/casino/softgaming/auth'

    payload = {"game_id": "14601"}

    header = {
        "Accept":"application/json, text/plain, */*",
        "Authorization":f"bearer {token_autorizacao}",
        "Origin":"https://mesk.bet",
        "Referer":"https://mesk.bet/",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
            }
    
    response = requests.post(URL, json=payload, headers=header)

    url_1 = json.loads(response.content)['url']

    #REQUISIÇÃO2
    URL = f'{url_1}&ref=https://mesk.bet'

    response = requests.get(URL)

    url_2 = json.loads(response.content)['data']

    #REQUISIÇÃO3
    URL = url_2

    headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Cookie":"cdn=https://static.egcdn.com; lang=en; locale=en-GB; EVOSESSIONID=rkimpvrwoyoblpe3rkimqshnmany7wcf4588b17809d39462ac1b30cfa2d31d5476bcf0169e16227c",
        "Host":"live.wirebankers.com",
        "Referer":"https://mesk.bet/",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }
    response = requests.get(URL, headers=headers, allow_redirects=False)

    evosessionid = response.headers.get('Set-Cookie').split('; Path')[0]

    return evosessionid


def conectar_websocket(evosessionid):
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
    "Host": "live.wirebankers.com",
    "Origin": "https://live.wirebankers.com",
    "Pragma": "no-cache",
    "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
    "Sec-WebSocket-Key": "D2s4bxoyJd6bkXUC7ZlTSw==",
    "Sec-WebSocket-Version": "13",
    "Upgrade": "websocket",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"

    }

   
    #f'wss://wac.evo-games.com/public/topcard/player/game/TopCard000000001/socket?messageFormat=json&instance=409uj-qo2wix3z5rclnkzu-nvrpqglt6teqkvaf&tableConfig=nvrpqglt6teqkvaf&EVOSESSIONID={evosessionid}&client_version=6.20230323.70223.23049-6a8fb42f8b'
    #URL=f'wss://belloatech.evo-games.com/public/topcard/player/game/TopCard000000001/socket?messageFormat=json&instance=o6q2h6-rhjuf7mokioplhho-TopCard000000001&tableConfig=&EVOSESSIONID={evosessionid}&client_version=6.20230823.71249.29885-78ea79aff8'
    URL=f'wss://live.wirebankers.com/public/topdice/player/game/TopDice000000001/socket?messageFormat=json&instance=bpm5u3-rklp3va5uuvroxj6-TopDice000000001&tableConfig=&{evosessionid}&client_version=6.20230915.71003.31229-7e3bf070cd'

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

    

def auto_refresh():
    global horario_inicio

    horario_atual = datetime.today().strftime('%H:%M')
    tres_hora = timedelta(hours=1)
    horario_mais_tres = horario_inicio + tres_hora
    horario_refresh = horario_mais_tres.strftime('%H:%M')

    if horario_atual == horario_refresh:
        print('HORA DE REFRESHAR A PAGINA!!!!')
        logar_site()
        time.sleep(10)
        horario_inicio = datetime.now()



def inicio():
    global browser
    global horario_inicio
    global seq_green

    horario_inicio = datetime.now()
    seq_green = 0
    
    # Definindo opções para o browser
    warnings.filterwarnings("ignore", category=DeprecationWarning) 
    chrome_options = webdriver.ChromeOptions() 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])


    browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)



def logar_site():
    #browser.get(r"https://pi.njoybingo.com/game.do?token=7d10f64b-e3db-4fb8-a8f7-330ff4d0d407&pn=meskbet&lang=pt&game=EVOLUTION-topcard-nvrpqglt6teqkvaf&type=CHARGED")  #PRODUÇÃO
    ##browser.get(r"https://pi.njoybingo.com/game.do?token=18298495-0dce-4997-944e-f52c78717619&pn=meskbet&lang=pt&game=EVOLUTION-topcard-nvrpqglt6teqkvaf&type=CHARGED")  #DEV
    #browser.maximize_window()
    #time.sleep(10)

    browser.get(r"https://f12.bet/login.php")
    browser.maximize_window()
    time.sleep(10)

    ''' Inserindo login e senha '''
    ''' Lendo o arquivo txt config-mensagens '''
    txt = open(r"arquivos_txt\canais.txt", "r", encoding="utf-8")
    mensagem_login = txt.readlines()
    usuario = mensagem_login[12].replace('\n','').split(' ')[1]
    senha = mensagem_login[13].replace('\n','').split(' ')[1]

    ''' Mapeando elementos para inserir credenciais '''
    try:
        
        browser.find_element_by_xpath('//*[@class="btn_general login_btn"]').click()  #Clicando no botão Entrar
        browser.find_element_by_xpath('//*[@class="login_field_holder"]//*[@type="text"]').send_keys(usuario)  #Inserindo login
        browser.find_element_by_xpath('//*[@class="login_field_holder"]//*[@type="password"]').send_keys(senha) #Inserindo senha
        browser.find_element_by_xpath('//*[@class="fhtxt"]//*[@type="submit"]').click() #Clicando no btn login
        time.sleep(4)

        ''' Verificando se o login foi feito com sucesso'''
        t3 = 0
        while t3 < 20:
            if browser.find_elements_by_xpath('//*[@class="deposit_area"]'):
                break
            else:
                t3+=1
    except:
        pass

    ''' Entrando no ambiente '''
    try:
        browser.get(r'https://sambabet.com/casino/game/43960-futebol-studio-ao-vivo')
        time.sleep(10)

        acessar_iframes()

        tela_cheia = browser.find_element_by_xpath('//*[@id="evolution_iframe"]').get_attribute('src')
        
        browser.get(tela_cheia)
        time.sleep(10)


    except:
        pass


def acessar_iframes():
    try:

        iframe1 = browser.find_element_by_id('casinogame')
        browser.switch_to_frame(iframe1)
        time.sleep(1)

        iframe2 = browser.find_element_by_id('lobbyFrameContainer')
        browser.switch_to_frame(iframe2)
        time.sleep(1)

        
    except:pass


def gerarListaResultados(resultados):
    ''' Convertendo a letra em cor '''
    while True:
        try:
            lista = []
            for resultado in reversed(resultados[:10]):
                lista.append(resultado.text)
                #if resultado.text == 'C':
                #    resultado = '\U0001F534'
                #    lista.append(resultado)
                #    continue
#
                #if resultado.text == 'V':
                #    resultado = '\U0001F535'
                #    lista.append(resultado)
                #    continue
#
                #if resultado.text == 'E':
                #    resultado = '\U0001F7E1'
                #    lista.append(resultado)
                #    continue
          
            return lista
            
        except:
            validarJogoPausado()
            resultados = browser.find_elements_by_css_selector('.historyItem--a1907')
            continue


def validarJogoPausado():
    try:

        #Acessando Iframe
        try:
            
            iframe3 = browser.find_element_by_xpath('/html/body/div[5]/div[2]/iframe')
            browser.switch_to_frame(iframe3)

        except:pass


        terminou_sessao = browser.find_elements_by_css_selector('.contentElement--e8ecb')
        for sessao in terminou_sessao:
            if sessao.text == 'Você foi desconectado. Feche esta janela e conecte novamente para jogar.':
                logar_site()


        sessao_expirada = browser.find_elements_by_css_selector('.titleContainer--fe91d')
        for sessao in sessao_expirada:
            if sessao.text == 'SESSÃO EXPIRADA':
                logar_site()


        att_pagina = browser.find_elements_by_css_selector('.content--c7c5e')
        for pagina in att_pagina:
            if pagina.text == 'Please refresh the page to re-enter the game on this device':
                logar_site()

        jogo_pausado = browser.find_elements_by_xpath('//*[@class="label--75060"]')
        for jogo in jogo_pausado:
            if jogo.text == 'JOGO PAUSADO POR INATIVIDADE':
                browser.find_element_by_xpath('//*[@class="wrapper--b9e82"]').click()


    except:
        pass

    try:
        if browser.find_element_by_xpath('//*[@class="label--75060"]').text == 'JOGO PAUSADO POR INATIVIDADE':
            browser.find_element_by_xpath('//*[@class="wrapper--b9e82"]').click()
    
    except:
        try:
            if browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div[10]/div[1]/span').text == 'GAME PAUSED DUE TO INACTIVITY':
                browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div').click()

        except:
            try:
                if browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div[10]/div[1]/span').text == 'GAME PAUSED DUE TO INACTIVITY':
                    browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div').click()
            except:
                try:
                    if browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div[5]/div/div/div/div[1]/div[2]').text == 'Your balance is too low to join this table.':
                        logar_site()
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


        #Auto Refresh
        auto_refresh()

        #Acessando Iframe
        try:
            
            iframe3 = browser.find_element_by_xpath('/html/body/div[5]/div[2]/iframe')
            browser.switch_to_frame(iframe3)

        except:pass


        try:
            ''' Pegando Resultados do Jogo '''
            resultados = browser.find_elements_by_css_selector('.historyItem--a1907')
            ''' Lista de resultados Convertidas em cores '''
            lista_resultados = gerarListaResultados(resultados)
            print(lista_resultados)

            if lista_resultados == []:
                logar_site()
                continue
            else:
                pass

            validaEstrategias(lista_resultados)

        except:
            logar_site()
            continue
            

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
        #validarJogoPausado()
        
        sequencia_minima_alerta = len(estrategia)-2
        sequencia_minima_sinal = len(estrategia)-1

        #print ('Analisando a Estratégia --> ', estrategia)
        #print('Historico da Mesa --> ', lista_resultados[:sequencia_minima_alerta])

        ''' Verifica se os resultados da mesa batem com a estrategia para enviar o alerta '''
        if estrategia[:sequencia_minima_alerta] == lista_resultados[-sequencia_minima_alerta:]:
            print('IDENTIFICADO O PADRÃO DA ESTRATÉGIA --> ', estrategia)
            print('ENVIAR ALERTA')
            enviarAlertaTelegram()
            time.sleep(1)

            ''' Verifica se a ultima condição bate com a estratégia para enviar sinal Telegram '''
            while True:
                # Jogo Pausado
                validarJogoPausado()
                
                try:
                    ''' Lendo novos resultados para validação da estratégia'''
                    if browser.find_elements_by_css_selector('.historyItem--a1907'):
                        resultados = browser.find_elements_by_css_selector('.historyItem--a1907')

                    ''' Função que converte as letras em cores '''
                    lista_resultados_validacao = gerarListaResultados(resultados)

                    ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
                    if lista_resultados != lista_resultados_validacao:
                        ''' Verificando se o ultimo resultado da mesa está dentro da estratégia'''
                        if estrategia[:sequencia_minima_sinal] == lista_resultados_validacao[-sequencia_minima_sinal:]:
                            print('PADRÃO DA ESTRATÉGIA ', estrategia, ' CONFIRMADO!')
                            print('ENVIANDO SINAL TELEGRAM')
                            enviarSinalTelegram()
                            time.sleep(1)
                            checkSinalEnviado(lista_resultados_validacao)
                            break
                            
                        else:
                            print('APAGA SINAL DE ALERTA')
                            apagaAlertaTelegram()
                            break
                        
                except:
                    logar_site()


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
                                                                  .replace('[APOSTA]', 'AMARELO 💛' if estrategia[-1] == 'C' else ' AZUL 💙' if estrategia[-1] == 'V' else 'EMPATE 💚' )
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

    time.sleep(8)

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
    global contador_cash, seq_green, placar_geral, asserividade, gale

    resultado_valida_sinal = []
    contador_cash = 0
    
    while contador_cash <= gale:

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
                lista_resultados_sinal = gerarListaResultados(resultados)

            ''' Valida se a lista de resultados atual é a mesma da lista definida antes de enviar o alerta'''
            if lista_resultados_validacao != lista_resultados_sinal:
    
                print(lista_resultados_sinal[-1])

                if lista_resultados_sinal[-1] == 'V':
                    resultado_valida_sinal.append('🟦')

                if lista_resultados_sinal[-1] == 'C':
                    resultado_valida_sinal.append('🟥')
                
                if lista_resultados_sinal[-1] == 'E':
                    resultado_valida_sinal.append('🟨')

                #resultado_valida_sinal.append(lista_resultados_sinal[-1])

                # VALIDANDO WIN OU LOSS
                if lista_resultados_sinal[-1] == estrategia[-1] or lista_resultados_sinal[-1] == 'E':
                
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

                        if lista_resultados_sinal[-1] == 'E':
                            
                            message_green = 'GREENZADA no empate! 🟢'

                        else:
                            ''' Lendo o arquivo txt config-mensagens '''
                            with open('arquivos_txt/green.txt',"r", encoding="utf-8") as arquivo:
                                message_green = arquivo.read()


                        for key, value in canais.items():
                            try:
                                
                                bot.reply_to(globals()[f'sinal_{key}'], message_green, parse_mode='HTML')

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
                    lista_resultados = lista_resultados_sinal

                    #intervalo entre sinais
                    time.sleep(intervalo_sinais)


                    return

            
                else:
                    print('LOSSS')
                    print('==================================================')
                    contador_cash+=1

                    if gale > 0:
                        mensagem_gale(contador_cash)

                    lista_resultados_validacao = lista_resultados_sinal
                    continue


        except:
            continue


    if contador_cash > gale:
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
        lista_resultados = lista_resultados_sinal
        seq_green = 0

        #intervalo entre sinais
        time.sleep(intervalo_sinais)

        return




#inicio()
#logar_site()
#placar()
pegar_evosessionid()




#________________________________________________________________________________________ TELEGRAM__________________________________________________________________________________#

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

        message_estrategia = bot.reply_to(message, "🤖 Ok! Informe a sequencia de LETRAS (V,C,E) que o bot terá que identificar. *** A última LETRA será a da aposta ***  \n\n Ex: VVVVVVC  / CCCCCV", reply_markup=markup)
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
        markup_estrategias = generate_buttons_estrategias([''.join(estrategia) for estrategia in estrategias], markup)
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
        bot.send_message(message.chat.id, ''.join(estrategia))


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

        message_opcoes = bot.reply_to(message, "🤖 Bot Football Studio Iniciado! ✅ Escolha uma opção 👇",
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
    
    estrategia = list(estrategia)
    placar_estrategia = list(placar_estrategia)

    placar_estrategia.extend([0,0,0,0,0])

    # Adicionando estratégia atual
    estrategias.append(estrategia)
    placar_estrategias.append(placar_estrategia)

    # Acumulando estratégia do dia
    estrategias_diaria.append(estrategia)
    placar_estrategias_diaria.append(placar_estrategia)

    #ESCREVENDO ESTRATEGIA NO TXT DE ESTRATEGIAS
    txt_estrategias = open('arquivos_txt/estrategias.txt', 'w', encoding='UTF-8').write(str(estrategias))


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
    
    estrategia_excluir = list(message_excluir_estrategia.text)
    
    for estrategia in estrategias:
        if estrategia_excluir == estrategia:
            estrategias.remove(estrategia)

    
    for pe in placar_estrategias:
        if estrategia_excluir == pe[:-5]:
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


