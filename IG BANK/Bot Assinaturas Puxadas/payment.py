# payment.py
import requests, uuid, mercadopago
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Defina sua chave de acesso
chave = os.getenv("MP_SECRET_KEY")

"""Processa o pagamento via PIX e retorna o QR Code"""
def process_pix_payment(amount):
    try:
        # Criar uma preferência de pagamento via PIX
        data = {
            "transaction_amount": 100.0,
            "payment_method_id": "pix",
            "description": "Pagamento via PIX",
            "payer": {
                "email": "cliente@exemplo.com"
            }
        }

        headers = {
            'Authorization': f'Bearer {chave}',
            'Content-Type': 'application/json',
            'x-idempotency-key': uuid.uuid4().hex
        }

        response = requests.post('https://api.mercadopago.com/v1/payments', json=data, headers=headers)
        payment_data = response.json()

        # Retorna o QR Code gerado
        qr_code = payment_data['point_of_interaction']['transaction_data']['qr_code']
        payment_id = payment_data['id']

        return qr_code, payment_id

        

    except Exception as e:
        print(f"Erro ao processar pagamento via PIX: {e}")
        return None, None


def consult_status_payment(payment_id):

    # URL para obter detalhes do pagamento
    status_url = f'https://api.mercadopago.com/v1/payments/{payment_id}'
    
    # cabeçalho pra consulta
    headers = {
            'Authorization': f'Bearer {chave}',
            'Content-Type': 'application/json',
        }
    
    # requisiçao
    response = requests.get(status_url, headers=headers)

    if response.status_code == 200:
        payment_info = response.json()
        status = payment_info['status']  # status pode ser 'approved', 'pending', 'rejected', etc.
        #print(f'Status do pagamento: {status}')
        return status
    else:
        print('Erro ao verificar status do pagamento', response.text)
        return None
    

