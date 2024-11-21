# -*- coding: utf-8 -*-
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackContext
from telegram.ext.filters import TEXT, COMMAND
import re

# Bot token
TOKEN = "7342363820:AAF3zh6emrgvg0aRQxqAAHrUXN_5vIqD1Dk"

# Storage for tracking user messages
last_messages = {}

# /start command handler
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hi! I am a moderator bot. I delete links and repetitive messages.")

# Message handler
async def handle_messages(update: Update, context: CallbackContext):
    # Check if the message exists
    if update.message is None or update.message.from_user is None:
        return

    user_id = update.message.from_user.id
    chat_id = update.message.chat.id
    message_text = update.message.text

    # Check for links
    if re.search(r"(https?://|www\.)", message_text):
        await update.message.delete()
        await context.bot.send_message(chat_id, f"@{update.message.from_user.username}, links are not allowed!")
        return

    # Check for repetitive messages
    if chat_id not in last_messages:
        last_messages[chat_id] = {}

    if user_id in last_messages[chat_id]:
        if last_messages[chat_id][user_id] == message_text:
            await update.message.delete()
            await context.bot.send_message(chat_id, f"@{update.message.from_user.username}, please do not repeat messages!")
            return

    # Save the message for spam tracking
    last_messages[chat_id][user_id] = message_text

# Error handler
async def error_handler(update: Update, context: CallbackContext):
    print(f"Error: {context.error}")

# Main function
def main():
    # Create the application
    application = ApplicationBuilder().token(TOKEN).build()

    # Add the /start command handler
    application.add_handler(CommandHandler("start", start))

    # Add the message handler
    application.add_handler(MessageHandler(TEXT & ~COMMAND, handle_messages))

    # Register the error handler
    application.add_error_handler(error_handler)

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
    
