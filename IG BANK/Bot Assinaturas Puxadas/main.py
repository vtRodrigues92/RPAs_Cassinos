import os
import time
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, CallbackQueryHandler, JobQueue, ContextTypes, Job
from database import *
from telegram.error import TelegramError
from payment import *
from subscription import *

# Carregar variáveis de ambiente
from dotenv import load_dotenv
load_dotenv()

# Cria as tabelas no banco de dados
create_tables()

GROUP_ID = os.getenv("GROUP_ID")
MASTER_USER_IDS = list(map(int, os.getenv("MASTER_USER_IDS").split(',')))
INSTAGRAM_URL = os.getenv("INSTAGRAM_URL")

# Função principal de boas-vindas com InlineKeyboard
async def start(update: Update, context: CallbackContext):
    """Responde com boas-vindas e as opções do menu usando InlineKeyboard"""
    user = update.effective_message.from_user
    user_id = user.id
    name = user.first_name
    username = user.username

    # Registra o usuário no banco de dados, se não estiver registrado
    if not get_user_by_id(user_id):
        add_user(user_id, name, username)

    # Configura o menu de acordo com o tipo de usuário
    if user_id in MASTER_USER_IDS:
        welcome_message = f"Olá, {name}! Você tem permissões de administrador.\nEscolha uma das opções abaixo:"
        keyboard = [
            [InlineKeyboardButton("Comprar Assinatura", callback_data="buy_subscription"),
             InlineKeyboardButton("Renovar Assinatura", callback_data="renew_subscription")],
            [InlineKeyboardButton("Contatar Suporte", url="https://t.me/victorr_rodrigues")],#callback_data="contact_support"),
             [InlineKeyboardButton("Instagram IG BANK", url=INSTAGRAM_URL)],#callback_data="follow_instagram")],
            [InlineKeyboardButton("Consultar Dias de Assinatura", callback_data="check_days")],
             [InlineKeyboardButton("Estatísticas do Bot", callback_data="admin_statistics")]
        ]
    else:
        welcome_message = f"Olá, {name}! Bem-vindo ao nosso serviço de assinatura.\nEscolha uma das opções abaixo:"
        keyboard = [
            [InlineKeyboardButton("Comprar Assinatura", callback_data="buy_subscription"),
             InlineKeyboardButton("Renovar Assinatura", callback_data="renew_subscription")],
            [InlineKeyboardButton("Contatar Suporte", url="https://t.me/victorr_rodrigues")],#callback_data="contact_support"),
             [InlineKeyboardButton("Instagram IG BANK", url=INSTAGRAM_URL)],#callback_data="follow_instagram")],
            [InlineKeyboardButton("Consultar Dias de Assinatura", callback_data="check_days")],
        ]
    
    # Define o teclado inline
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Envia a mensagem de boas-vindas com o teclado inline
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)
    
    # Apaga a mensagem de boas-vindas após um tempo (para não ficar no histórico)
    await update.message.delete()

# Função para lidar com a compra de assinatura
async def handle_buy_subscription(update: Update, context: CallbackContext):
    """Inicia o processo de compra de assinatura"""
    user = update.effective_message.chat
    user_id = user.id

    # Verifica o status da assinatura do usuário
    subscription_status = get_subscription_status(user_id)

    # Se o usuário já tem uma assinatura ativa, envie a data de expiração
    if subscription_status == "active":
        await update.message.reply_text("Não se preocupe! Você já tem uma assinatura ativa, válida até {data_expiração}")
        await update.message.delete()
        return

    # Se o usuário não tem assinatura, oferece o pagamento via PIX
    await handle_payment_pix(update, context)

# Função para processar pagamento via PIX
async def handle_payment_pix(update: Update, context: CallbackContext):
    """Processa o pagamento via PIX"""
    user = update.effective_message.chat
    user_id = user.id
    amount = 50.0  # Valor da assinatura

    # Processa o pagamento via PIX
    qr_code, payment_id = process_pix_payment(amount)
    
    if qr_code:
        await update.callback_query.message.reply_text(f"Para realizar o pagamento de R${amount}, escaneie o QR Code abaixo:\n{qr_code}")
        # registrando o usuario que gerou o pix - na tabela ele fica "pendente_pagamento"
        create_subscription(user_id)
        
        # chamando a função de agendamento de verificação de pagamento
        setup_payment_check(application, payment_id)

        print('ssss')
        #update_subscription(user_id, "pending", "active", f"Assinatura aguardando pagamento via PIX (Intent: )")
    
    else:
        await update.callback_query.message.reply_text(f"Algo deu erra na geração do PIX! Tente novamente em instantes ou contate o suporte.")

# Função para renovar a assinatura
async def handle_renew_subscription(update: Update, context: CallbackContext):
    """Renova a assinatura do usuário"""
    user = update.effective_message.from_user
    user_id = user.id

    # Verifica o status da assinatura
    subscription_status = get_subscription_status(user_id)

    if subscription_status == "expired":
        await update.callback_query.answer("Sua assinatura expirou. Você pode renová-la agora.")
        return await handle_buy_subscription(update, context)

    if subscription_status == "active":
        await update.callback_query.answer("Sua assinatura já está ativa. Você pode renová-la agora se desejar.")
        return await handle_buy_subscription(update, context)

    await update.callback_query.answer("Você não tem uma assinatura. Por favor, compre uma assinatura primeiro.")

# Função para lidar com o contato de suporte
async def handle_contact_support(update: Update, context: CallbackContext):

    """Envia o link de contato do usuário para o suporte"""
    support_message = f'Entre em contato com o <a href="t.me/victorr_rodrigues" >Suporte IG BANK</a>'
    
    await update.callback_query.message.reply_text(support_message, parse_mode='HTML')

# Função para enviar instagram
async def handle_follow_instagram(update: Update, context: CallbackContext):
    """Envia o link do Instagram"""
    instragram_message = f'Você pode seguir nosso Instagram aqui: <a href="{INSTAGRAM_URL}" >INSTAGRAM IG BANK</a>'
    
    await update.callback_query.message.reply_text(instragram_message, parse_mode='HTML')

# Função para exibir estatísticas para administradores
async def handle_admin_statistics(update: Update, context: CallbackContext):
    """Exibe as estatísticas do bot para usuários master"""
    user_id = update.effective_message.chat_id

    if user_id not in MASTER_USER_IDS:
        return

    # Estatísticas
    interactions = count_interactions()
    active_subscriptions = count_active_subscriptions()
    renewed_subscriptions = count_renewed_subscriptions()
    expired_subscriptions = count_expired_subscriptions()
    pix_count, _ = count_payments()  # Apenas contamos os pagamentos via PIX

    stats_message = f"""
    Estatísticas do Bot:
    
    Interações únicas por usuário:
    {interactions}
    
    Assinaturas ativas: {active_subscriptions}
    Assinaturas renovadas: {renewed_subscriptions}
    Assinaturas expiradas: {expired_subscriptions}
    
    Pagamentos via PIX: {pix_count}
    """
    await update.callback_query.message.reply_text(stats_message)

# Função de verificação do pagamento em segundo plano
async def check_payment_and_update(context: ContextTypes.DEFAULT_TYPE):
    
    payment_id = context.job.data['payment_id']  # Usando job.context para acessar os dados

    if payment_id:
        status = consult_status_payment(payment_id)
        if status == 'approved':
            # Quando o pagamento for aprovado, registrar no banco e chamar a função para lidar com o pagamento
            ##funcção registrar no banco
            await handle_payment_approved(context)
            # Cancelar o job, pois o pagamento foi aprovado
            context.job.schedule_removal()

        else:
            print(status)

# Função para enviar mensagem ao usuário e adicionar ao canal
async def handle_payment_approved(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_id = user.id
    username = user.username if user.username else "Usuário sem username"
    
    # Mensagem de confirmação
    await update.message.reply_text(f"Pagamento aprovado! {username}, sua assinatura foi ativada.")

    # Adicionar o usuário ao canal/grupo (substitua pelo GROUP_ID correto)
    await context.bot.add_chat_member(GROUP_ID, user_id)

    # Atualizar banco de dados (você pode registrar o status do pagamento aqui)
    update_subscription(user_id, "approved", "active", "Assinatura ativada com sucesso")

# Função para configurar o agendamento do Job
def setup_payment_check(application: Application, payment_id):
    # Cria um Job para ser executado após 30 segundos
    application.job_queue.run_repeating(
        check_payment_and_update,  # Função a ser executada
        interval = 30,  # Tempo de intervalo entre cada execução (30 segundos)
        data={'payment_id':payment_id}  # Dados a serem passados para a função
    )

def add_user_to_group(user_id):
    """Adiciona um usuário ao grupo"""
    application.kick_chat_member(GROUP_ID, user_id)  # Garante que o usuário não está banido
    application.invite_link(GROUP_ID, user_id)

def remove_user_from_group(user_id):
    """Remove um usuário do grupo"""
    application.kick_chat_member(GROUP_ID, user_id)

def send_message(user_id, message):
    """Envia uma mensagem para o usuário"""
    application.send_message(chat_id=user_id, text=message)

async def manage_subscriptions(context):
    """Verifica as assinaturas dos usuários e envia alertas se necessário"""
    # Aqui você pode usar um banco de dados para armazenar os usuários e suas assinaturas.
    # Por simplicidade, vamos supor que temos uma função fictícia `get_users_subscription`.
    subscriptions = [get_all_subscription()]

    for subscription in subscriptions:
        if subscription[3] == 'active':
            subscription_expiry = subscription[2]
            if check_subscription_expiry(subscription_expiry):
                # Calculando o número de dias restantes
                days_left = (subscription_expiry - time.time()) / 86400  # Convertendo segundos para dias

                # Verificando os dias restantes
                if days_left <= 3 and days_left > 2:
                    await context.bot.send_message(subscription[1], "Sua assinatura vai expirar em 3 dias!")
                elif days_left <= 2 and days_left > 1:
                    await context.bot.send_message(subscription[1], "Sua assinatura vai expirar em 2 dias!")
                elif days_left <= 1 and days_left > 0:
                    await context.bot.send_message(subscription[1], "Sua assinatura vai expirar em 1 dia!")
                elif days_left <= 0:
                    await context.bot.send_message (subscription[1], "Sua assinatura expirou!")
                    await remove_user_from_group(subscription['user_id'])
            else:
                # A assinatura já expirou, removendo o usuário
                await remove_user_from_group(subscription[1])


# Agendamento de tarefas
def setup_jobs(application: Application):
    # Verificação periódica das assinaturas expiradas
    application.job_queue.run_repeating(
        manage_subscriptions, 
        interval=86400,  # Verificar assinaturas expiradas a cada 24 horas (86400 segundos)
        first=0  # Começar imediatamente
    )


# Função para lidar com a escolha do botões inline
async def button(update: Update, context: CallbackContext):
    """Processa a escolha do botão"""
    query = update.callback_query
    await query.answer()  # Responde ao callback query (necessário para evitar erro de timeout)
    
    choice = query.data
    
    if choice == "buy_subscription":
        await handle_buy_subscription(update, context)
    elif choice == "renew_subscription":
        await handle_renew_subscription(update, context)
    elif choice == "contact_support":
        await handle_contact_support(update, context)
    elif choice == "admin_statistics":
        await handle_admin_statistics(update, context)
    elif choice == "follow_instagram":
        await handle_follow_instagram(update, context)
    else:
        await query.message.reply_text("Opção desconhecida.")


# Função para iniciar o bot e fazer o polling
def run_bot():
    global application

    """Inicia o bot e começa o polling"""
    # Cria o Application e passa o token do bot
    application = Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()

    # Registra os handlers para os comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))  # Handler para callbacks do teclado inline
    application.add_handler(CommandHandler("pix", handle_payment_pix))

    # Configuração do job de verificação de assinaturas
    setup_jobs(application)

    # Inicia o polling e espera pelas mensagens
    application.run_polling()


# Chama a função para iniciar o bot
if __name__ == "__main__":

    print('\n\n##### AGUARDANDO COMANDOS #####')
    run_bot()
