import json
import sys
import time
import asyncio
import requests
from requests.adapters import HTTPAdapter, Retry

class Blaze:
    def __init__(self):
        print('blaze')


    def make_request(self, url, headers, post=None, req_type="GET"):
        """
        Make a request to the given url with the given headers.

        Args:
            url (str): The url to make the request to.
            headers (dict): The headers to use in the request.
            post (dict): The post data to use in the request.

        Returns:
            The response from the request.
        """
        session = requests.Session()
        retry = Retry(total=5, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
        session.mount("http://", HTTPAdapter(max_retries=retry))
        session.mount("https://", HTTPAdapter(max_retries=retry))
        if req_type == "GET":
            response = session.get(url, headers=headers)
        elif req_type == "POST" and post is not None:
            response = session.post(url, headers=headers, data=post)
        elif req_type == "PUT" and post is not None:
            response = session.put(url, headers=headers, data=post)

        return response


    def get_history_data(self):
        """
        Get the data from the double data page.

        Returns:
            The data from the double data page.
        """
        url = "https://blaze.com/api/roulette_games/recent"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NDg1MzE5NiwiYmxvY2tzIjpbXSwiaWF0IjoxNjQ4NjExNjM2LCJleHAiOjE2NTM3OTU2MzZ9.QjBeuzSGVG5jl2yiVJvEsEA5VURX_RIcPJRpsZPbfEk",
            "x-client-language": "pt",
            "x-client-version": "5fe52546",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
        }
        response = self.make_request(url, headers)
        return response.json()


    def get_roulete_data(self):
        """
        Get the data from the roulete page.

        Returns:
            The data from the roulete page.
        """
        url = "https://blaze.com/api/roulette_games/current"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NDg1MzE5NiwiYmxvY2tzIjpbXSwiaWF0IjoxNjQ4NjExNjM2LCJleHAiOjE2NTM3OTU2MzZ9.QjBeuzSGVG5jl2yiVJvEsEA5VURX_RIcPJRpsZPbfEk",
            "x-client-language": "pt",
            "x-client-version": "5fe52546",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
        }
        response = self.make_request(url, headers)
        return response.json()


    def make_bet(self, color, value, token, wallet_id):
        """
        Make a bet on the roulete.

        """
        url = "https://blaze.com/api/roulette_bets"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Authorization": f"Bearer {token}",
            "content-type": "application/json;charset=UTF-8",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "origin": "https://blaze.com",
            "referer": "https://blaze.com/pt/games/double",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="101", "Opera";v="87"',
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36 OPR/87.0.4390.36",
            "x-client-language": "pt",
            "x-client-version": "64d23215",
            "content-type": "application/json;charset=UTF-8"
        }

        data = {}
        data["amount"] = round(float("{:,.2f}".format(value)), 2)
        data["currency_type"] = "BRL"
        data["color"] = color
        data["free_bet"] = False
        data["wallet_id"] = wallet_id
        bet_payload = json.dumps(data)

        response = self.make_request(url, headers, bet_payload, req_type="POST")
        if response.status_code == 200:
            # print(f"[Bot] - Aposta: {'WHITE'if color == 0 else 'BLACK' if color == 2 else 'RED'} - Valor: R$ {data['amount']} Confirmada!")
            # ultimaApostaId = ultimoResultadoId
            # corAposta = color
            return True
        else:
            error_message = response.json()["error"]
            with open("Erros_aposta.txt", "a") as f:
                f.write(f"{error_message} - cor = {color} - valor = {value}\n")
            # print(error_message)
            # print(f"[Bot] - Aposta: {'WHITE'if color == 0 else 'BLACK' if color == 2 else 'RED'} - Valor: R$ {data['amount']} Erro!")
            return False


    def get_user_info(self, token):
        """
        Get the user info.

        Returns:
            The user info.
        """
        url = "https://blaze.com/api/users/me"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Authorization": f"Bearer {token}",
            "x-client-language": "pt",
            "x-client-version": "5fe52546",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
        }
        user_data_request = self.make_request(url, headers)

        url = "https://blaze.com/api/wallets"
        wallet_data_request = self.make_request(url, headers)

        user_data = {}
        if user_data_request.status_code == 200 or wallet_data_request.status_code == 200:
            account_data = user_data_request.json()
            wallet_data = wallet_data_request.json()
            user_data["username"] = account_data["username"]
            user_data["balance"] = "{:,.2f}".format(float(wallet_data[0]["balance"]))
            user_data["wallet_id"] = wallet_data[0]["id"]
            user_data["tax_id"] = account_data["tax_id"]
            return user_data


    def get_blaze_token(self, email, password):
        """
        Get the blaze token.

        Args:
            email (str): The email.
            password (str): The password.
        """
        url = "https://blaze.com/api/auth/password"
        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json;charset=UTF-8",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "origin": "https://blaze.com",
            "referer": "https://blaze.com/pt/?modal=auth&tab=login",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
            "x-captcha-response": "%",
            "x-client-language": "pt",
            "x-client-version": "c9d9c023",
        }
        data = {}
        data["username"] = email
        data["password"] = password

        payload = json.dumps(data)
        response = self.make_request(url, headers, payload, req_type="PUT")
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            return False


    def get_bet_result(self, id):
        """
        Get the bet result.

        Args:
            id (str): The bet id.

        Returns:
            The bet result.
        """
        url = f"https://blaze.com/api/roulette_games/{id}?page=1"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NDg1MzE5NiwiYmxvY2tzIjpbXSwiaWF0IjoxNjQ4NjExNjM2LCJleHAiOjE2NTM3OTU2MzZ9.QjBeuzSGVG5jl2yiVJvEsEA5VURX_RIcPJRpsZPbfEk",
            "x-client-language": "pt",
            "x-client-version": "5fe52546",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
        }
        response = self.make_request(url, headers)
        return response.json()

    def get_history_crash(self):
        url = "https://blaze.com/api/crash_games/recent"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NDg1MzE5NiwiYmxvY2tzIjpbXSwiaWF0IjoxNjQ4NjExNjM2LCJleHAiOjE2NTM3OTU2MzZ9.QjBeuzSGVG5jl2yiVJvEsEA5VURX_RIcPJRpsZPbfEk",
            "x-client-language": "pt",
            "x-client-version": "5fe52546",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
        }
        response = self.make_request(url, headers)
        return response.json()

    def get_crash_data(self):
        url = "https://blaze.com/api/crash_games/current"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NDg1MzE5NiwiYmxvY2tzIjpbXSwiaWF0IjoxNjQ4NjExNjM2LCJleHAiOjE2NTM3OTU2MzZ9.QjBeuzSGVG5jl2yiVJvEsEA5VURX_RIcPJRpsZPbfEk",
            "x-client-language": "pt",
            "x-client-version": "5fe52546",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
        }
        response = self.make_request(url, headers)
        return response.json()

    def make_bet_crash(self, numero, value, token, wallet):
        url = "https://blaze.com/api/crash/round/enter"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Authorization": f"Bearer {token}",
            "content-type": "application/json;charset=UTF-8",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "origin": "https://blaze.com",
            "referer": "https://blaze.com/pt/games/crash",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="101", "Opera";v="87"',
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36 OPR/87.0.4390.36",
            "x-client-language": "pt",
            "x-client-version": "64d23215",
            "content-type": "application/json;charset=UTF-8"
        }

        data = {}
        data["amount"] = round(float("{:,.2f}".format(value)), 2)
        data["currency_type"] = "BRL"
        data["auto_cashout_at"] = float(numero)
        data["wallet_id"] = wallet
        bet_payload = json.dumps(data)

        response = self.make_request(url, headers, bet_payload, req_type="POST")
        time.sleep(1)
        if response.status_code == 200:
            return True
        else:
            error_message = response.json()["error"]
            with open("Erros_aposta.txt", "a") as f:
                f.write(f"{error_message} - retirar em = {numero} - valor = {value}\n")
            return False

    def get_bet_result_crash(self, id):
        url = f"https://blaze.com/api/crash_games/{id}?page=1"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NDg1MzE5NiwiYmxvY2tzIjpbXSwiaWF0IjoxNjQ4NjExNjM2LCJleHAiOjE2NTM3OTU2MzZ9.QjBeuzSGVG5jl2yiVJvEsEA5VURX_RIcPJRpsZPbfEk",
            "x-client-language": "pt",
            "x-client-version": "5fe52546",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
        }
        response = self.make_request(url, headers)
        return response.json()


    def getToken(self, email, senha):
        token = self.get_blaze_token(email, senha)
        return token


    def getUser(self, token):
        #loop = asyncio.get_event_loop()
        return self.get_user_info(token)


    def apostar(self, cor, valor, token, wallet_id):
        # 0 = branco / 1 = vermelho / 2 = preto
        return self.make_bet(cor, valor, token, wallet_id)


    def getHistorico(self):
        hist = self.get_history_data()

        historicoCores = [f"{result.get('color')}".replace("0", "b").replace("1", "v").replace("2", "p")
                          for result in hist]
        # inverte lista
        historicoCores = historicoCores[::-1]
        return historicoCores


    def getUltimoResultado(self):
        hist = self.get_history_data()
        return hist[0]


    def getStatusRoleta(self):
        # waiting - rolling - complete
        return self.get_roulete_data()


    def getResultado(self, id):
        return self.get_bet_result(id)

    def getHistoricoCrash(self):
        hist = self.get_history_crash()

        historicoCores = [float(result.get('crash_point')) for result in hist]
        #inverte lista
        historicoCores = historicoCores[::-1]
        return historicoCores

    def getStatusCrash(self):
        #waiting - graphing - complete
        return self.get_crash_data()


    def getUltimoResultadoCrash(self):
        hist = self.get_history_crash()
        return hist[0]

    def getResultadoCrash(self, id):
        return self.get_bet_result_crash(id)

    def apostarCrash(self, numero, valor, token, wallet):
        return self.make_bet_crash(numero, valor, token, wallet)




