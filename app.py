from flask import Flask, request, jsonify
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
import json

app = Flask(__name__)

# Твои данные
TOKEN = "7516332250:AAGm9AjkXNBHKC9vcMXpCBXr-q5a_AXtXVk"
YOUR_ID = "5603062555"
bot = Bot(token=TOKEN)

# Хранилище сообщений (в памяти сервера)
messages = []

# === Обработка сообщений от Миши (через бота) ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = update.message.text
    if user_id == YOUR_ID:  # только твой ID сохраняется
        messages.append(f"Миша: {text}")
        # Можно также отправить ответное уведомление на сайт (если нужно)

# Настройка бота (polling)
application = Application.builder().token(TOKEN).build()
application.add_handler(MessageHandler(filters.TEXT & filters.User(user_id=YOUR_ID), handle_message))

# Запуск бота в фоновом режиме (без блокировки Flask)
import threading
def run_bot():
    application.run_polling()

threading.Thread(target=run_bot, daemon=True).start()

# === API для сайта ===
@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    text = data.get('text')
    if text:
        bot.send_message(chat_id=YOUR_ID, text=text)
        messages.append(f"Я: {text}")
        return jsonify({"status": "ok"})
    return jsonify({"status": "error"}), 400

@app.route('/get_messages', methods=['GET'])
def get_messages():
    return jsonify(messages[-50:])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
