# -*- coding: utf-8 -*-
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from telegram.ext.filters import TEXT as Filters
import re

# Токен вашего бота
TOKEN = "7342363820:AAF3zh6emrgvg0aRQxqAAHrUXN_5vIqD1Dk"

# Хранилище сообщений для проверки спама
last_messages = {}

# Функция для команды /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Я бот-модератор. Я удаляю ссылки и повторяющиеся сообщения.")

# Фильтр для обработки сообщений
def handle_messages(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    chat_id = update.message.chat.id
    message_text = update.message.text

    # Проверка на ссылки
    if re.search(r"(https?://|www\.)", message_text):
        update.message.delete()
        context.bot.send_message(chat_id, f"@{update.message.from_user.username}, ссылки запрещены!")
        return

    # Проверка на повторяющиеся сообщения
    if chat_id not in last_messages:
        last_messages[chat_id] = {}

    if user_id in last_messages[chat_id]:
        if last_messages[chat_id][user_id] == message_text:
            update.message.delete()
            context.bot.send_message(chat_id, f"@{update.message.from_user.username}, не повторяйтесь!")
            return

    # Сохранение сообщения для проверки спама
    last_messages[chat_id][user_id] = message_text

# Основная функция запуска
def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Обработка команды /start
    dispatcher.add_handler(CommandHandler("start", start))

    # Обработка текстовых сообщений
    dispatcher.add_handler(MessageHandler(Filters.TEXT & ~Filters.COMMAND, handle_messages))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
