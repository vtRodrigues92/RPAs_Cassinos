# subscription.py
import time
from database import add_subscription, update_subscription, get_subscription_status, get_user_by_id
from main import *

def create_subscription(user_id):
    """Cria uma assinatura para o usuário"""
    add_subscription(user_id, 'pending_payment', 0)
    
def renew_subscription(user_id, payment_method):
    """Renova a assinatura do usuário"""
    # Extende a assinatura por 30 dias adicionais
    subscription_status = get_subscription_status(user_id)
    if subscription_status == 'expired':
        expiry_timestamp = time.time() + 30 * 86400
        update_subscription(user_id, 'active', expiry_timestamp, 'Assinatura renovada')
    return True

def create_expiry_timestamp():  
    expiry_timestamp = time.time() + 30 * 86400  # 30 dias de assinatura
    return expiry_timestamp

def check_subscription_expiry(expiry_timestamp):
    """Verifica se a assinatura está prestes a expirar"""
    current_time = time.time()
    if expiry_timestamp <= current_time:
        return True
    return False
