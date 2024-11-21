# -*- coding: utf-8 -*-
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackContext
from telegram.ext.filters import TEXT
import re

# Bot token
TOKEN = "7342363820:AAF3zh6emrgvg0aRQxqAAHrUXN_5vIqD1Dk"

# Function to delete links in channels
async def handle_channel_post(update: Update, context: CallbackContext):
    if update.channel_post is None:
        return

    chat_id = update.channel_post.chat_id
    message_text = update.channel_post.text

    # Check for links in the message
    if re.search(r"(https?://|www\.)", message_text):
        await update.channel_post.delete()
        await context.bot.send_message(chat_id, "Links are not allowed in this channel!")

# Error handler
async def error_handler(update: Update, context: CallbackContext):
    print(f"Error: {context.error}")

# Main function
def main():
    # Create the application
    application = ApplicationBuilder().token(TOKEN).build()

    # Add a handler for channel posts
    application.add_handler(MessageHandler(TEXT, handle_channel_post))

    # Register the error handler
    application.add_error_handler(error_handler)

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
