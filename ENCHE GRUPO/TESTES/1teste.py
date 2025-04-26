from webbrowser import BaseBrowser
from selenium import webdriver
import time
import warnings
from webdriver_manager.chrome import ChromeDriverManager
import logging
from datetime import datetime
from selenium.webdriver.support.color import Color
import pandas as pd
from columnar import columnar
import telebot
from telegram.ext import * 
from telebot import types
import sys
import os
import mysql.connector
from mysql.connector import Error




logger = logging.getLogger()



# ALIMENTANDO O BANCO
def alimentaBanco():
    try:
        
        db_conexao = mysql.connector.connect(host='localhost.robozaosheik.net', database='robozaos_dbaviator', user='robozaos_dados', password='@Aviator22')
        print('conectou')

    except Exception as g:

        logger.error('Exception ocorrido na conexão com o banco MYSQL: ' + repr(g))


    ''' Variavel que executa as querys '''
    #cursor = db_conexao.cursor()


alimentaBanco()