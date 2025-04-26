import telebot 
from telethon.sync import TelegramClient 
from telethon.tl.types import InputPeerUser, InputPeerChannel 
from telethon import TelegramClient, sync, events
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.types import InputChannelEmpty
from telethon import TelegramClient
from telethon.tl.types.messages import Messages
from telethon.tl.types.contacts import Contacts
from telethon.sync import TelegramClient
from telethon import functions, types
import time
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import csv
   
api_id = '15861134'
api_hash = '158e599541366a97380bcc1474fc7bb2'
token = '5434022871:AAF-mMhUcDuEID9vf-8WnLvZiFPUnjuzk-k'
phone = '+5521994025776'
name = ''
chat = int(input('INSIRA O CHAT DO GRUPO/CANAL --> '))
   
bot = TelegramClient('bot', api_id, api_hash).start(bot_token=token)


# Show all user IDs in a chat
#for user in bot.iter_participants(chat):
#    print(user.first_name,\
#         user.phone, \
#         user.last_name )
#    time.sleep(5)


# PEGANDO GRUPOS E CANAIS
chats = []
last_date = None
chunk_size = 200
groups=[]
 
result = bot(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)


for chat in chats:
    try:
        if chat.megagroup== True:
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
all_participants = bot.get_participants(target_group, aggressive=True)


print('Saving In file...')
with open("members.csv","w",encoding='UTF-8') as f:
    writer = csv.writer(f,delimiter=",",lineterminator="\n")
    writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
    for user in all_participants:
        if user.username:
            username= user.username
        else:
            username= ""
        if user.first_name:
            first_name= user.first_name
        else:
            first_name= ""
        if user.last_name:
            last_name= user.last_name
        else:
            last_name= ""
        name= (first_name + ' ' + last_name).strip()
        writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])      
print('Members scraped successfully.')


print('Saving In file...')
with open("members.csv","w",encoding='UTF-8') as f:
    writer = csv.writer(f,delimiter=",",lineterminator="\n")
    writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
    for user in all_participants:
        if user.username:
            username= user.username
        else:
            username= ""
        if user.first_name:
            first_name= user.first_name
        else:
            first_name= ""
        if user.last_name:
            last_name= user.last_name
        else:
            last_name= ""
        name= (first_name + ' ' + last_name).strip()
        writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])      
print('Members scraped successfully.')


#bot.connect() 
  
#if not bot.is_user_authorized(): 
   
#    client.send_code_request(phone) 
      
    
#    client.sign_in(phone, input('Enter the code: ')) 
   
   
#try: 
    
#    with TelegramClient(name, api_id,api_hash) as client:
#        result = client(functions.contacts.GetContactsRequest(
#            hash=0
#        ))
#        print(result.stringify())
#    
    
    #contatos = client.get_peer_id()
    
    #receiver = InputPeerUser(, 0) 
  
    
    #lient.send_message(receiver, "aaaa", parse_mode='html') 


#except Exception as e: 
#      
#    
#    print(e); 
#client.disconnect() 





