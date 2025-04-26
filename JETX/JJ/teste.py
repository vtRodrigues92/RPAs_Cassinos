import mysql.connector
from mysql.connector import Error
import logging


logger = logging.getLogger() #Log de erro


try: 
    db_conexao = mysql.connector.connect(host='185.239.210.5', port=3306, database='u791277084_basejetx', user='u791277084_userjetx', password='1iV6LX1od!L')
    print('conectado')

except Exception as g:

    logger.error('Exception ocorrido na conexão com o banco MYSQL: ' + repr(g))



'tc27v1u4GI'


'''banco de dados
    IP: 185.239.210.5
    User: u791277084_userjetx
    Pass: 1iV6LX1od!L
    DB: u791277084_basejetx
    Tabela: app_data (histórico dos jogos), app_game (resultados dos sinais)'''