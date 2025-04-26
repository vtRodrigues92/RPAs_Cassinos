import requests
import json

webhook_url = 'https://d181-177-12-182-121.sa.ngrok.io/webhook'

data = { 'name': 'DevOps Journey', 
         'Channel URL': 'test url' }

r = requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})