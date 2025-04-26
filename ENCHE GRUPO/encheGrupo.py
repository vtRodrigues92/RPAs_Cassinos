from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
import csv
import traceback
import time
import random

api_id = 26323908
api_hash = '58561851bead242f382124946923c54b'
phone = '+5511941975042'
client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))


input_file = input('Insira a lista de membros: ')
users = []
with open(input_file, encoding='UTF-8') as f:
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)

chats = []
last_date = None
chunk_size = 200
groups=[]

result = client(GetDialogsRequest(
            offset_date=last_date,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=chunk_size,
            hash = 0
        ))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup == True:
            groups.append(chat)
    except:
        continue

print('Escolha o Grupo para Adicionar os Membros: ')
i=0
for group in groups:
    print(str(i) + '- ' + group.title)
    i+=1

g_index = input("Escolha um Número: ")
target_group=groups[int(g_index)]

target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)

mode = int(input("Escolha 1 para Add por UserName ou 2 para Add por ID: "))

n = 0

for user in users:
    n += 1
    if n % 50 == 0:
        time.sleep(900)
    try:
        print (f"Adicionando - {user['username']} ---- {n} / {len(users)}" )
        if mode == 1:
            if user['username'] == "":
                continue
            user_to_add = client.get_input_entity(user['username'])
        elif mode == 2:
            #user_to_add = InputPeerUser(user['id'], user['access_hash'])
            user_to_add = client.get_peer_id(user['id'])
        else:
            sys.exit("Invalid Mode Selected. Please Try Again.")
        client(InviteToChannelRequest(target_group_entity,[user_to_add]))
        print("Esperando por 60-180 segundos...")
        #time.sleep(10)
        time.sleep(random.randrange(60, 180))


    except PeerFloodError:
        print("Obtendo erro de inundação do telegram. O script está parando agora. Por favor tente novamente depois de algum tempo.")
        break

    except UserPrivacyRestrictedError:
        print("As configurações de privacidade do usuário não permitem que você faça isso.")

    except Exception as e:
        print(e)
        #traceback.print_exc()
        #print("Erro inesperado")
        continue
