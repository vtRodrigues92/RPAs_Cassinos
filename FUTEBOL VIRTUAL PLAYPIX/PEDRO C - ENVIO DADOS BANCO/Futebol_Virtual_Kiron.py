import requests, json
import mysql.connector
from mysql.connector import Error
import logging
from datetime import datetime, timedelta
import time


def getDataItalianLeague():
    global match_italian_old, match_italian_old_1

    try:
        URL = 'https://games1.playbetman.com/Home/GetEventsWithUpdatedPrimaryMarkets'

        payload = '{"operatorGuid":"514e3877-45b4-4098-81b0-5cd15140197f","sessionGuid":"5f5ed762-2bfd-4412-b819-369c91d91dff","name":"ItalianFastLeagueFootballSingleMatch","feedId":"25","offset":-10800,"languageCode":"en","primaryMarketClassIds":["201","16","203"],"bettingLayoutEnumValue":"1","expandedParentEventIds":null,"nextEventCount":""}'
        
        headers = {
            "Content-Type":"application/json; charset=UTF-8",
            "Origin":"https://games1.playbetman.com",
            "Referer":"https://games1.playbetman.com/?o=e373ae56-2c47-4ae0-950d-09b4db90aa2d&dp=1&l=en&c=BRL&eg=Lobby&hu=https://games.playpix.com/GoToHome?Id=www.playpix.com",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "X-Requested-With":"XMLHttpRequest"
        }

        response = requests.post(URL, headers=headers, data=payload)
        
        ###Coletando Dados para comparação
        team_home = json.loads(response.content)['Data'][0]['FootballMatch']['HomeTeam']
        team_visitors = json.loads(response.content)['Data'][0]['FootballMatch']['AwayTeam']
        
        italian_event_id = json.loads(response.content)['Data'][0]['EventId']

        if  italian_event_id not in list_event_id:

            league = json.loads(response.content)['Data'][0]['TypeName']
            data_match = json.loads(response.content)['Data'][0]['StartDateTimeAsWords'].split(' ')[0]
            start_hour_match = json.loads(response.content)['Data'][0]['StartTimeAsWords']
            finish_hour_match = json.loads(response.content)['Data'][0]['FinishTimeAsWords']
            scoreboard = f'{json.loads(response.content)["Data"][0]["FootballMatch"]["HomeScore"]} x {json.loads(response.content)["Data"][0]["FootballMatch"]["AwayScore"]}'
            over_2_5 = json.loads(response.content)['Data'][0]['PrimaryMarkets'][1]['FootballMatchSelections'][0]['Odds']
            under_2_5 = json.loads(response.content)['Data'][0]['PrimaryMarkets'][1]['FootballMatchSelections'][1]['Odds']
            over_3_5 = json.loads(response.content)['Data'][0]['PrimaryMarkets'][2]['FootballMatchSelections'][0]['Odds']
            under_3_5 = json.loads(response.content)['Data'][0]['PrimaryMarkets'][2]['FootballMatchSelections'][1]['Odds']

            print(f'{datetime.now().strftime("%H:%M")} \n{league} | {data_match} | {start_hour_match} | {finish_hour_match} | {team_home} | {team_visitors} | {scoreboard} | {over_2_5} | {under_2_5} | {over_3_5} | {under_3_5}')

            #### Registrando no Banco
            postDataInBD(team_home, team_visitors, league, data_match, start_hour_match, finish_hour_match,scoreboard,over_2_5,under_2_5,over_3_5,under_3_5)

            print('=' * 100)

            list_event_id.append(italian_event_id)


    except:pass


def getDataEnglishLeague():
    global match_english_old, match_english_old_1

    try:

        URL = 'https://games1.playbetman.com/Home/GetEventsWithUpdatedPrimaryMarkets'

        payload = '{"operatorGuid":"514e3877-45b4-4098-81b0-5cd15140197f","sessionGuid":"400fa729-ac95-4bdf-b0d5-e9c39749f8ba","name":"EnglishFastLeagueFootballSingleMatch","feedId":"25","offset":-10800,"languageCode":"en","primaryMarketClassIds":["201","16","203"],"bettingLayoutEnumValue":"1","expandedParentEventIds":null,"nextEventCount":""}'
        
        headers = {
            "Content-Type":"application/json; charset=UTF-8",
            "Origin":"https://games1.playbetman.com",
            "Referer":"https://games1.playbetman.com/?o=e373ae56-2c47-4ae0-950d-09b4db90aa2d&dp=1&l=en&c=BRL&eg=Lobby&hu=https://games.playpix.com/GoToHome?Id=www.playpix.com",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "X-Requested-With":"XMLHttpRequest"
        }

        response = requests.post(URL, headers=headers, data=payload)
        
        ###Coletando Dados para comparação
        team_home = json.loads(response.content)['Data'][0]['FootballMatch']['HomeTeam']
        team_visitors = json.loads(response.content)['Data'][0]['FootballMatch']['AwayTeam']
        
        english_event_id = json.loads(response.content)['Data'][0]['EventId']
        
        if  english_event_id not in list_event_id:

            league = json.loads(response.content)['Data'][0]['TypeName']
            data_match = json.loads(response.content)['Data'][0]['StartDateTimeAsWords'].split(' ')[0]
            start_hour_match = json.loads(response.content)['Data'][0]['StartTimeAsWords']
            finish_hour_match = json.loads(response.content)['Data'][0]['FinishTimeAsWords']
            scoreboard = f'{json.loads(response.content)["Data"][0]["FootballMatch"]["HomeScore"]} x {json.loads(response.content)["Data"][0]["FootballMatch"]["AwayScore"]}'
            over_2_5 = json.loads(response.content)['Data'][0]['PrimaryMarkets'][1]['FootballMatchSelections'][0]['Odds']
            under_2_5 = json.loads(response.content)['Data'][0]['PrimaryMarkets'][1]['FootballMatchSelections'][1]['Odds']
            over_3_5 = json.loads(response.content)['Data'][0]['PrimaryMarkets'][2]['FootballMatchSelections'][0]['Odds']
            under_3_5 = json.loads(response.content)['Data'][0]['PrimaryMarkets'][2]['FootballMatchSelections'][1]['Odds']

            print(f'{datetime.now().strftime("%H:%M")} \n{league} | {data_match} | {start_hour_match} | {finish_hour_match} | {team_home} | {team_visitors} | {scoreboard} | {over_2_5} | {under_2_5} | {over_3_5} | {under_3_5}')

            #### Registrando no Banco
            postDataInBD(team_home, team_visitors, league, data_match, start_hour_match, finish_hour_match,scoreboard,over_2_5,under_2_5,over_3_5,under_3_5)

            print('=' * 100)

            list_event_id.append(english_event_id)


    except:pass


def getDataSpanishLeague():
    global match_spanish_old, match_spanish_old_1

    try:
        URL = 'https://games1.playbetman.com/Home/GetEventsWithUpdatedPrimaryMarkets'

        payload = '{"operatorGuid":"514e3877-45b4-4098-81b0-5cd15140197f","sessionGuid":"400fa729-ac95-4bdf-b0d5-e9c39749f8ba","name":"SpanishFastLeagueFootballSingleMatch","feedId":"25","offset":-10800,"languageCode":"en","primaryMarketClassIds":["201","16","203"],"bettingLayoutEnumValue":"1","expandedParentEventIds":null,"nextEventCount":""}'
        
        headers = {
            "Content-Type":"application/json; charset=UTF-8",
            "Origin":"https://games1.playbetman.com",
            "Referer":"https://games1.playbetman.com/?o=e373ae56-2c47-4ae0-950d-09b4db90aa2d&dp=1&l=en&c=BRL&eg=Lobby&hu=https://games.playpix.com/GoToHome?Id=www.playpix.com",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "X-Requested-With":"XMLHttpRequest"
        }

        response = requests.post(URL, headers=headers, data=payload)
        
        ###Coletando Dados para comparação
        team_home = json.loads(response.content)['Data'][0]['FootballMatch']['HomeTeam']
        team_visitors = json.loads(response.content)['Data'][0]['FootballMatch']['AwayTeam']
        #team_home_1 = json.loads(response.content)['Data'][1]['FootballMatch']['HomeTeam']
        #team_visitors_1 = json.loads(response.content)['Data'][1]['FootballMatch']['AwayTeam']

        spanish_event_id = json.loads(response.content)['Data'][0]['EventId']

        if  spanish_event_id not in list_event_id:
            
            league = json.loads(response.content)['Data'][0]['TypeName']
            data_match = json.loads(response.content)['Data'][0]['StartDateTimeAsWords'].split(' ')[0]
            start_hour_match = json.loads(response.content)['Data'][0]['StartTimeAsWords']
            finish_hour_match = json.loads(response.content)['Data'][0]['FinishTimeAsWords']
            scoreboard = f'{json.loads(response.content)["Data"][0]["FootballMatch"]["HomeScore"]} x {json.loads(response.content)["Data"][0]["FootballMatch"]["AwayScore"]}'
            over_2_5 = json.loads(response.content)['Data'][0]['PrimaryMarkets'][1]['FootballMatchSelections'][0]['Odds']
            under_2_5 = json.loads(response.content)['Data'][0]['PrimaryMarkets'][1]['FootballMatchSelections'][1]['Odds']
            over_3_5 = json.loads(response.content)['Data'][0]['PrimaryMarkets'][2]['FootballMatchSelections'][0]['Odds']
            under_3_5 = json.loads(response.content)['Data'][0]['PrimaryMarkets'][2]['FootballMatchSelections'][1]['Odds']

            print(f'{datetime.now().strftime("%H:%M")} \n{league} | {data_match} | {start_hour_match} | {finish_hour_match} | {team_home} | {team_visitors} | {scoreboard} | {over_2_5} | {under_2_5} | {over_3_5} | {under_3_5}')

            #### Registrando no Banco
            postDataInBD(team_home, team_visitors, league, data_match, start_hour_match, finish_hour_match,scoreboard,over_2_5,under_2_5,over_3_5,under_3_5)

            print('=' * 100)

            list_event_id.append(spanish_event_id)
            #match_spanish_old_1 = f'{team_home_1}x{team_visitors_1}'

    except:pass


def postDataInBD(team_home, team_visitors, league, data_match, start_hour_match, finish_hour_match,scoreboard,over_2_5,under_2_5,over_3_5,under_3_5):
    #banco de dados
    HOST = '162.240.147.7'
    USER = 'easycoanalytics_storage'
    PASS = ',jr2BCU}E7n]7VB?HR'
    DB =  'easycoanalytics_storage'
    TABELA = 'results_virtual_futebol_kiron'

    try:
        #CONECTANDO COM O BANCO '''
        db_conexao = mysql.connector.connect(host=HOST, database=DB, user=USER, password=PASS)

        #Variavel que executa as querys
        cursor = db_conexao.cursor()

        ''' QUERY '''
        query_inserir_dados = (f"""INSERT INTO {TABELA} 
                                VALUES(NULL, NULL, '{league}', '{data_match}', '{start_hour_match}', '{finish_hour_match}', '{team_home}', '{team_visitors}', '{scoreboard}', '{over_2_5}', '{under_2_5}', '{over_3_5}', '{under_3_5}')""")

        cursor.execute(query_inserir_dados)
        db_conexao.commit()

    except Exception as g:
        logger.error('Exception ocorrido na conexão com o banco MYSQL: ' + repr(g))
        pass



if __name__ == '__main__':
    
    list_event_id = []
    logger = logging.getLogger()

    print('\n\nINICIANDO COLETA DOS DADOS......\n')
    print('='*100)

    while True:
        
        getDataItalianLeague()
        getDataEnglishLeague()
        getDataSpanishLeague()

        time.sleep(2)





