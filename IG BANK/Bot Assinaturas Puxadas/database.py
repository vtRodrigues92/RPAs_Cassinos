import sqlite3
import time
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

DB_NAME = os.getenv("DB_NAME", "subscriptions.db")

# Função para conectar no banco
def connect_db():
    """Conecta ao banco de dados SQLite"""
    return sqlite3.connect(DB_NAME)

# Função para criar Tabela
def create_tables():
    """Cria as tabelas no banco de dados se não existirem"""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        username TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        expiry_timestamp INTEGER NOT NULL,
        payment_status TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
        
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        user_id INTEGER,
        method TEXT,
        amount REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        timestamp INTEGER DEFAULT CURRENT_TIMESTAMP
        
    )
    """)
    conn.commit()
    conn.close()

# Função para adicionar um novo usuário
def add_user(user_id, name, username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO users (user_id, name, username) VALUES (?, ?, ?)
    """, (user_id, name, username))
    conn.commit()
    conn.close()

# Função para buscar todas as assinaturas
def get_all_subscription():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM subscriptions
    """),
    all_subscription = cursor.fetchone()
    conn.close()
    return all_subscription

# Função para buscar um usuário pelo ID
def get_user_by_id(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM users WHERE user_id = ?
    """, (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

# Função para adicionar uma nova assinatura
def add_subscription(user_id, status, expiry_timestamp):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO subscriptions (user_id, payment_status, expiry_timestamp) VALUES (?, ?, ?)
    """, (user_id, status, expiry_timestamp))
    conn.commit()
    conn.close()

# Função para atualizar o status da assinatura
def update_subscription(user_id, status, expiry_timestamp, comment):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE subscriptions SET status = ?, expiry_timestamp = ?, comment = ? WHERE user_id = ?
    """, (status, expiry_timestamp, comment, user_id))
    conn.commit()
    conn.close()

# Função para obter o status da assinatura do usuário
def get_subscription_status(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT payment_status FROM subscriptions WHERE user_id = ?
    """, (user_id,))
    status = cursor.fetchone()
    conn.close()
    return status[0] if status else None

# Função para registrar o pagamento
def add_payment(user_id, payment_method, amount):
    conn = connect_db()
    cursor = conn.cursor()
    timestamp = int(time.time())
    cursor.execute("""
    INSERT INTO payments (user_id, payment_method, amount, timestamp) VALUES (?, ?, ?, ?)
    """, (user_id, payment_method, amount, timestamp))
    conn.commit()
    conn.close()

# Função para contar as interações
def count_interactions():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT COUNT(DISTINCT user_id) FROM interactions
    """)
    count = cursor.fetchone()[0]
    conn.close()
    return count

# Função para contar assinaturas ativas
def count_active_subscriptions():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT COUNT(*) FROM subscriptions WHERE status = 'active'
    """)
    count = cursor.fetchone()[0]
    conn.close()
    return count

# Função para contar assinaturas renovadas
def count_renewed_subscriptions():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT COUNT(*) FROM subscriptions WHERE comment = 'Assinatura renovada'
    """)
    count = cursor.fetchone()[0]
    conn.close()
    return count

# Função para contar assinaturas expiradas
def count_expired_subscriptions():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT COUNT(*) FROM subscriptions WHERE status = 'expired'
    """)
    count = cursor.fetchone()[0]
    conn.close()
    return count

# Função para contar pagamentos via PIX e Cartão
def count_payments():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT COUNT(*) FROM payments WHERE payment_method = 'PIX'
    """)
    pix_count = cursor.fetchone()[0]
    
    cursor.execute("""
    SELECT COUNT(*) FROM payments WHERE payment_method = 'Cartão de Crédito'
    """)
    card_count = cursor.fetchone()[0]
    conn.close()
    return pix_count, card_count
