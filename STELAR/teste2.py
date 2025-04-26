import requests










user = 'Fordbracom2022'
password = 'Gabriel@2022'

urlLogin = "https://odin.prod.sportingtech.com/api/user/login"
payloadLogin = '{"requestBody":{"username":"' + user + '","email":null,"phone":null,"keepLoggedIn":null,"password":"' + password + '","loginType":1},"languageId":23,"device":"d"}'

headersLogin = {"Content-Type": "application/json",
                "Origin":"https://m.estrelabet.com",
                "Referer":"https://m.estrelabet.com/"}

dadosLogin = requests.post(urlLogin, data=payloadLogin, headers=headersLogin)

print(dadosLogin.text,'\n\n')