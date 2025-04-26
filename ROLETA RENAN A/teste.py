import requests
import json


URL = 'https://eu-server.ssgportal.com/GameLauncher/Loader.aspx?GameCategory=JetX&GameName=JetX&ReturnUrl&Token=62275c68-7152-4dc0-b582-9d6c4cf86d0e&PortalName=meskbet&skin=meskjet'

header = {

        "Referer":"https://mesk.bet/",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"

}


res = requests.get(URL, headers=header)

print(res)