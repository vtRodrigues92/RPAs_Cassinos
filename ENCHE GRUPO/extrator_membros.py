from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import csv

api_id = 15861134
api_hash = '158e599541366a97380bcc1474fc7bb2'
phone = '+5521994025776'
client = TelegramClient(phone, api_id, api_hash)

client.start()

#if not client.is_user_authorized():
#    client.send_code_request(phone)
#    client.sign_in(phone, input('Enter the code: '))



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

for chat in client.iter_dialogs():
    try:
        #if chat.megagroup == True:
        groups.append(chat)
    except:
        continue

print('Choose a group to scrape members from:')
i=0
for g in groups:
    print(str(i) + '- ' + g.title)
    i+=1

g_index = input("Enter a Number: ")
target_group=groups[int(g_index)]

print('Fetching Members...')
all_participants = []
all_participants = client.get_participants(target_group, limit=8000)

''' CRIAR UMA FUNÇÃO PARA QUE NÃO SALVE MEMBRO REPETIDO NO TXT '''

print('Saving In file...')
with open(f"members_{target_group.title}.csv","w",encoding='UTF-8') as f:
    writer = csv.writer(f,delimiter=",",lineterminator="\n")
    writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
    for user in all_participants:
        if user.username != None:
            username= user.username
        else:
            continue
        if user.first_name:
            first_name= user.first_name
        else:
            first_name= ""
        if user.last_name:
            last_name= user.last_name
        else:
            last_name= ""
        name= (first_name + ' ' + last_name).strip()
        writer.writerow([username,user.id,user.access_hash,target_group.title, target_group.id])      
print('Members scraped successfully.')
