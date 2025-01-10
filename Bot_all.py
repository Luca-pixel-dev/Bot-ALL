import logging
import os
import time
import json
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

load_dotenv('Token.env')
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if TOKEN is None:
    logging.error("Токен не завантажений. Перевірте файл Token.env")

user_last_used = {}
active_users = {}
COOLDOWN_PERIOD = 300  # 5 хвилин очікування
ACTIVE_USERS_FILE = "active_users.json"

# Завантаження активних користувачів із файлу
def load_active_users():
    global active_users
    if os.path.exists(ACTIVE_USERS_FILE):
        with open(ACTIVE_USERS_FILE, 'r') as file:
            active_users = json.load(file)
            logging.info("Дані про активних користувачів завантажені.")
    else:
        logging.info("Файл з активними користувачами не знайдено, створюємо новий словник.")

# Збереження активних користувачів у файл
def save_active_users():
    with open(ACTIVE_USERS_FILE, 'w') as file:
        json.dump(active_users, file)
        logging.info("Дані про активних користувачів збережені.")

async def tagall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    current_time = time.time()

    if user_id in user_last_used and (current_time - user_last_used[user_id]) < COOLDOWN_PERIOD:
        time_left = COOLDOWN_PERIOD - (current_time - user_last_used[user_id])
        await update.message.reply_text(f"Ти здурів хлопаку, не флуди бо получиш бан. Почекай ще {int(time_left)} секунд.")
        return

    user_last_used[user_id] = current_time
    logging.info(f"User {user_id} used @all command.")

    if chat_id in active_users:
        tags = " ".join([f"@{username}" for user_id, username in active_users[chat_id].items() if username])
        if tags:
            await update.message.reply_text(tags)
        else:
            await update.message.reply_text("Не вдалося знайти активних учасників з іменами користувачів для відмічання.")
    else:
        await update.message.reply_text("Немає інформації про активних учасників.")

async def track_active_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    if chat_id not in active_users:
        active_users[chat_id] = {}

    # Додаємо користувача
    if user.username:
        active_users[chat_id][user.id] = user.username
        save_active_users()  # Зберегти активних користувачів після додавання

def main():
    load_active_users()  # Завантаження даних про користувачів під час запуску

    application = Application.builder().token(TOKEN).build()

    application.add_handler(MessageHandler(filters.Regex(r'@all'), tagall))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, track_active_users))

    logging.info("Bot started.")
    application.run_polling()

if __name__ == '__main__':
    main()
