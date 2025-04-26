import requests
import json

url_dados = 'https://gs.fugaso.com/magnify-admin/player/events?sessionId=3dbbe4a73409ead770b2c76a411fa&mode=external&operatorId=353350&userName=104152846&gameName=magnifyman'

def get_json_in_str(str_to_json: str):

    str_to_json = str_to_json[str_to_json.index('{"current":'):str_to_json.index('"stop":true}')+12]

    try:
        return json.loads(str_to_json)
    except:
        return False

r = requests.get(url_dados, stream=True)

for chunk in r.iter_content(chunk_size=50000):
    dados_api = chunk.decode('UTF-8')

    if '"stop":true}' in dados_api:
        print(get_json_in_str(dados_api)['current'])




