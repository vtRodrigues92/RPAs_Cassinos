from websocket import create_connection
import json

header = {
    "user_id": "esportes-2022129235242",
    "session_token": "5501_5875_7b2230223a2231323338393036323634222c2231223a2230222c2232223a2231222c2273223a223161653463376235653736333761386564333530643739376430363534633663227d",
    "currency": "BRL", "denomination": "1", "callback_version": 2, "language": "en", "game_name": "goblinrun",
    "cashurl": "", "backurl": "https://m.estrelabet.com/",
    "hosts": ["https://socketgames-kube.evoplay.games/gamepage/"], "s": "2e3a3db380494eb0835c76ee0b2e3e89",
    "hide_currency": False, "country_code": "BR", "action_url": "socketgames-kube.evoplay.games",
    "rq_url": "socketgames-kube.evoplay.games/gamepage", "listener_url": "/listener-goblinrun", "debug": True,
    "game_path": "/gamepage/games/goblinrun/", "version": "v0.5.1", "base_path": "/gamepage/games/goblinrun/",
    "cash_url": "", "back_url": "https://m.estrelabet.com/", "userAgent": None,
    "redirect_inside_iframe": False, "show_clock": True, "show_history": True,
    "hosts_for_static": ["https://socketgames-kube.evoplay.games"], "portrait_mode_enabled": True,
    "logo_url": None
}


URL = f"wss://socketgames-kube.evoplay.games/listener-goblinrun/416/447/websocket"

ws = create_connection(URL)

ws.send(json.dumps([json.dumps(header)]))

cont = 0
ultimo_result = ''
ultimo_valor_armazenado = ''

while True:

        ultimo_result = ws.recv()

        if 'round_id' in ultimo_result:
            print(round(float(ultimo_valor_armazenado.split(':')[-1].replace('}}"]','')),1))
         

        ultimo_valor_armazenado = ultimo_result





