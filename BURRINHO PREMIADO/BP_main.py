import PySimpleGUI as sg
import json
from BP_bot import Bot

def main():
    try:
        with open("credenciais.txt", "r", encoding='utf-8-sig') as f:
            t = f.read().replace("'", '"')
            texto = json.loads(t)
            getTextos(texto)
            f.close()
    except:
        getTextos([])

def layoutTextos(token="", id="", link_afiliado="", link_jogo="", validade="", espera="", confirmacao="", final=""):
    linha = [[sg.Text('Token:', size=(9, 1)), sg.Input(token, key='token', size=(60, 5))],
            [sg.Text('ID:', size=(9, 1)), sg.Input(id, key='id', size=(60, 5))],
            [sg.Text('Link Jogo:', size=(9, 1)), sg.Input(link_jogo, key='link_jogo', size=(60, 5))],
            [sg.Text('Link Afiliado:', size=(9, 1)), sg.Input(link_afiliado, key='link_afiliado', size=(60, 5))],
            [sg.Text('validade:', size=(9, 1)), sg.Input(validade, key='val', size=(15, 5)), sg.Text('    espera:', size=(9, 1)), sg.Input(espera, key='espera', size=(15, 5))],
            [sg.Text('Mensagem inicial', size=(24, 1)), sg.Text('                 Mensagem final', size=(30, 1))],

            [sg.Multiline(confirmacao, size=(35, 8), key='confirma'), sg.Multiline(final, size=(35, 8), key='final')]]
                # [sg.HorizontalSeparator()]]
    return linha

def criarJanelaTextos():
    sg.theme('DarkGray5')
    layout = [[sg.Frame("Configurações", layout=[], key="container")],
              [sg.Button("Novo Grupo"), sg.Button("Limpar tudo")],
              [sg.Button('Confirmar', size=(70, 1))]]

    return sg.Window("Configurar", layout=layout, finalize=True, size=(600,600))

def criarJanela(grupos):
    sg.theme('DarkGray5')
    column = []
    i = 0
    for t in grupos:
        i += 1
        token = t.get("telegram_bot_token", "")
        id = t.get("id", "")
        validade = t.get("tempo_validade", "")
        espera = t.get("tempo_espera", "")
        confirmacao = t.get("texto_confirmcao", "")
        final = t.get("texto_final", "")
        link_afiliado = t.get("link_afiliado", "")
        link_jogo = t.get("link_jogo","")
        column.append([sg.Frame(f'GRUPO-{i}', layoutTextos(token, id, link_afiliado, link_jogo, validade, espera, confirmacao, final))])

    altura = i
    if i > 3:
        altura = 3
    layout = [
            [sg.Column(column, scrollable=True, vertical_scroll_only=True, size=(550 + 16, 200 * 3), key='COLUMN')],
            [sg.Button("Novo Grupo"), sg.Button("Limpar tudo")],
            [sg.Button('Confirmar', size=(70, 1))]
    ]

    window = sg.Window('Configurações', layout, size=(600,700), finalize=True)

    return window

def getTextos(json):
    grupos = json
    janela = criarJanela(grupos)

    objetos = []
    while True:
        event, values = janela.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == "Novo Grupo":
            grupos.append({})
            janela.close()
            janela = criarJanela(grupos)
            # janela.extend_layout(janela['container'], layoutTextos())
        elif event == "Limpar tudo":
            grupos = [{}]
            janela.close()
            janela = criarJanela(grupos)
            # janela.extend_layout(janela['container'], layoutTextos())
        elif event == "Confirmar":
            token_lista = []
            id_lista = []
            link_afiliado_lista = []
            link_jogo_lista = []
            validade_lista = []
            espera_lista = []
            confirma_lista = []
            final_lista = []
            print(values.items())
            for key, value in values.items():
                if "token" in key:
                    token_lista.append(value)
                elif "id" in key:
                    id_lista.append(value)
                elif "link_afiliado" in key:
                    link_afiliado_lista.append(value)
                elif "link_jogo" in key:
                    link_jogo_lista.append(value)
                elif "val" in key:
                    validade_lista.append(value)
                elif "espera" in key:
                    espera_lista.append(value)
                elif "confirma" in key:
                    confirma_lista.append(value)
                elif "final" in key:
                    final_lista.append(value)

            for token, id, link_afiliado, link_jogo, validade, espera, confirma, final in zip(token_lista, id_lista, link_afiliado_lista, link_jogo_lista, validade_lista, espera_lista, confirma_lista, final_lista):
                obj = {}
                obj["telegram_bot_token"] = token
                obj["id"] = id
                obj["link_afiliado"] = link_afiliado
                obj["link_jogo"] = link_jogo
                obj["tempo_validade"] = validade
                obj["tempo_espera"] = espera
                obj["texto_confirmcao"] = confirma
                obj["texto_final"] = final
                objetos.append(obj)
                Bot(token, id, link_afiliado, link_jogo, validade, espera, confirma, final).start()
            #print(objetos)
            if objetos:
                with open("credenciais.txt", "w", encoding='utf-8-sig') as f:
                    f.write(str(objetos))
                    janela.close()
                    f.close()
                    return True


#sg.theme_previewer()
main()
