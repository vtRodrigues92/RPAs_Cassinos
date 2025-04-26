from __future__ import print_function
import time
from datetime import datetime, timedelta
import requests
#import os.path
#from google.auth.transport.requests import Request
#from google.oauth2.credentials import Credentials
#from google_auth_oauthlib.flow import InstalledAppFlow
#from googleapiclient.discovery import build
#from googleapiclient.errors import HttpError
import gspread
from oauth2client.service_account import ServiceAccountCredentials


#_______________________________________________________________________#____________________________________________________________________________________________________

print()
print('                                #################################################################')
print('                                %###################   BOT CATALOGADOR  #########################')
print('                                #################################################################')
print('                                ##################### SEJA BEM VINDO ############################')
print('                                #################################################################')
print('                                ############# DESENVOLVIDO POR VICTOR RODRIGUES #################')
print('                                #################################################################\n')
print('Versão = 1.0.0')
print('Ambiente: Produção\n\n\n')



print('#################  INICIANDO COLETA DOS DADOS DA BLAZE DOUBLE #################')
'\n\n\n'



def proximo_dia():
    global data_amanha
    
    try:
        um_dia = timedelta(days=1)
        data_amanha = data_hoje + um_dia

        return data_amanha
    except Exception as e:
        print("ERRO NA FUNÇÃO PROXIMO DIA --- ", e)



def acessa_planilha():
    global aba
    global planilha

    # Tente Selecionar a Aba com a Data de Hoje
    try:

        # Manipulando a Planilha    
        planilha = client.open("RecFibonacci")
        # Manipulando a Aba da Planilha
        aba = planilha.worksheet(data_hoje.strftime('%d-%m-%Y'))

    # Se Não Encontrar, Criar uma Aba com a Data de Hoje
    except:
        
        try:

            # Manipulando a Planilha    
            planilha = client.open("RecFibonacci")
            # Selecionando a Planilha Modelo
            planilha_modelo = planilha.worksheet('Planilha Modelo')

            #Duplicando Planilha Modelo
            planilha.duplicate_sheet(planilha_modelo.id, new_sheet_name = data_hoje.strftime('%d-%m-%Y'))

            # Manipulando a Aba da Planilha
            aba = planilha.worksheet(data_hoje.strftime('%d-%m-%Y'))

        except Exception as e:
            print("ERRO NA FUNÇÃO ACESSA_PLANILHA --- ", e)



def formata_hora(hora_resultado_roleta):

    try:
        #Convertendo a data e hora da rodada
        data_hora_inicial = datetime.strptime(hora_resultado_roleta[:-5],'%Y-%m-%dT%H:%M:%S')
        diminui_tres_horas = timedelta(hours=3)

        data_hora_final = (data_hora_inicial-diminui_tres_horas)

        return data_hora_final.strftime('%d-%m-%Y'),\
               data_hora_final.strftime('%H:%M:%S')
    
    except Exception as e:
        print("ERRO NA FUNÇÃO FORMATA_HORA --- ", e)
        pass



def duplica_planilha_modelo():

    try:
        planilha_modelo = planilha.worksheet('Planilha Modelo')

        #Duplicando Planilha Modelo
        planilha.duplicate_sheet(planilha_modelo.id, new_sheet_name = data_hoje.strftime('%d-%m-%Y'))
    except Exception as e:
        print("ERRO NA FUNÇÃO DUPLICA_PLANILHA_MODELO --- ", e)



def verifica_data(data_resultado):
    global planilha
    global aba
    global contagem_total_colunas
    global contagem_total_linhas
    global coluna_atual
    global linha_atual
    global data_hoje
    global data_amanha


    if data_resultado == data_amanha.strftime('%d-%m-%Y'):
        
        try:

            # Manipulando a Planilha    
            planilha = client.open("RecFibonacci")
            # Selecionando a Planilha Modelo
            planilha_modelo = planilha.worksheet('Planilha Modelo')

            #Duplicando Planilha Modelo
            planilha.duplicate_sheet(planilha_modelo.id, new_sheet_name = data_amanha.strftime('%d-%m-%Y'))

            # Manipulando a Aba da Planilha
            aba = planilha.worksheet(data_amanha.strftime('%d-%m-%Y'))

            # Pegando a Data Atual
            data_hoje = datetime.today().date()

            # Att data do dia seguinte
            data_amanha = proximo_dia()


        except Exception as e:
            print("ERRO NA FUNÇÃO VERIFICA_DATA --- ", e)

         

def conectar_googleSheet():
    global client 
    global data_hoje
    
    try:
    
        # use creds to create a client to interact with the Google Drive API
        scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)

        # Pegando a Data Atual
        data_hoje = datetime.today().date()
    
    except Exception as e:
        print("ERRO NA FUNÇÃO CONECTAR GOOGLE_SHEET --- ", e)



def coletar_dados():

    api_blaze_double = 'https://blaze.com/api/roulette_games/current'

    while True:      

            try:

                lista_resultados = []
                # Pegando o histórico de resultados
                resultado_roletta = requests.get(api_blaze_double).json()
                
                #Validando se a requisição retornou NULL
                if resultado_roletta['status'] != 'complete': continue

                #Convertendo os índices da cor em nome das cores
                if resultado_roletta['color'] == 1: cor = "Vermelho" 
                
                elif resultado_roletta['color'] == 2: cor = "Preto" 
                
                else: cor = "Branco"

                #Pegando o Número da Roletta
                numero = resultado_roletta['roll']
                #Pegando a Hora do Resultado da Roleta
                hora_resultado_roleta = resultado_roletta['created_at']
                #Formatando a Hora do Resultado da Roleta para HORA
                data_resultado, hora_resultado = formata_hora(hora_resultado_roleta)

                # Antes de Inserir as Informaçoes na Planilha, Validar se o Dia Mudou para Criar Outra Planilha
                verifica_data(data_resultado)

                #Inserindo Dados na Planilha
                inserir_dados_planilha(numero, hora_resultado)

                time.sleep(10)

            except Exception as e:
                print("ERRO NA FUNÇÃO COLETAR DADOS --- ", e)
                time.sleep(5)


#aba.cell(aba.findall("m00")[0].row, aba.findall("m00")[0].col).value
#aba.cell(aba.findall("m00")[0].row+2, aba.findall("m00")[0].col).value

def inserir_dados_planilha(numero, hora_resultado):
    global contagem_total_colunas
    global contagem_total_linhas
    global coluna_atual
    global linha_atual
    global planilha
    global aba

    # Criando uma Nova Aba na Planilha
    #planilha.add_worksheet(title="A worksheet", rows=100, cols=20)

    # Mostrando Todos os Valores da Aba Selecionada
    #todos_valores = aba.get_all_values()

    while True:

        try:
            
            # Identificando o Lugar na Planilha para inserir a Informação 
            celula_base_minuto = aba.findall("m"+hora_resultado[3:5])
            celula_base_hora =  aba.findall("h"+hora_resultado[0:2])

            if int(hora_resultado[-2:]) < 30:
                # Inserindo a Informação na Celula Identificada
                aba.update_cell((celula_base_minuto[0].row+celula_base_hora[0].row-2), celula_base_minuto[0].col, numero)

            else:
                # Inserindo a Informação na Celula Identificada
                aba.update_cell((celula_base_minuto[0].row+celula_base_hora[0].row-2), celula_base_minuto[0].col+1, numero)


            print(hora_resultado, '------ Número', numero)

            break
        
        except Exception as e:
            print("ERRO NA FUNÇÃO INSERIR_DADOS_PLANILHA --- ", e)





    

    #if aba.cell(linha_atual, contagem_total_colunas).value == None:
    #    coluna_atual +=1
    #    return
    
    #elif linha_atual == contagem_total_linhas and coluna_atual == contagem_total_colunas:
    #     pass #CRIAR FUNÇÃO PARA CRIAR OUTRA ABA

    #else:
    #    coluna_atual = 2
    #    linha_atual += 1




if __name__ == '__main__':
    conectar_googleSheet()
    proximo_dia()
    acessa_planilha()
    coletar_dados()
