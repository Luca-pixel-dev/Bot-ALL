import logging
import os
import time
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


load_dotenv('Token.env')
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


user_last_used = {}

active_users = {}


async def tagall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    current_time = time.time()

    
    if user_id in user_last_used and (current_time - user_last_used[user_id]) < 300:
        time_left = 300 - (current_time - user_last_used[user_id])
        await update.message.reply_text(f"Ти здурів хлопаку, не флуди бо получиш бан. Почекай ще {int(time_left)} секунд.")
        return

   
    user_last_used[user_id] = current_time

    
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

   
    if user.username:
        active_users[chat_id][user.id] = user.username

def main():
   
    application = Application.builder().token(TOKEN).build()

   
    application.add_handler(MessageHandler(filters.Regex(r'@all'), tagall))

    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, track_active_users))

   
    application.run_polling()

if __name__ == '__main__':
    main()
