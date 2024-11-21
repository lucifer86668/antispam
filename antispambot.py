# -*- coding: utf-8 -*-
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackContext
from telegram.ext.filters import TEXT, COMMAND
import re

# Токен вашего бота
TOKEN = "7342363820:AAF3zh6emrgvg0aRQxqAAHrUXN_5vIqD1Dk"

# Хранилище сообщений для проверки спама
last_messages = {}

# Функция для команды /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Привет! Я бот-модератор. Я удаляю ссылки и повторяющиеся сообщения.")

# Фильтр для обработки сообщений
async def handle_messages(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    chat_id = update.message.chat.id
    message_text = update.message.text

    # Проверка на ссылки
    if re.search(r"(https?://|www\.)", message_text):
        await update.message.delete()
        await context.bot.send_message(chat_id, f"@{update.message.from_user.username}, ссылки запрещены!")
        return

    # Проверка на повторяющиеся сообщения
    if chat_id not in last_messages:
        last_messages[chat_id] = {}

    if user_id in last_messages[chat_id]:
        if last_messages[chat_id][user_id] == message_text:
            await update.message.delete()
            await context.bot.send_message(chat_id, f"@{update.message.from_user.username}, не повторяйтесь!")
            return

    # Сохранение сообщения для проверки спама
    last_messages[chat_id][user_id] = message_text

# Основная функция запуска
def main():
    # Создаем приложение
    application = ApplicationBuilder().token(TOKEN).build()

    # Обработка команды /start
    application.add_handler(CommandHandler("start", start))

    # Обработка текстовых сообщений
    application.add_handler(MessageHandler(TEXT & ~COMMAND, handle_messages))

    # Запуск приложения
    application.run_polling()

if __name__ == '__main__':
    main()
