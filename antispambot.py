# -*- coding: utf-8 -*-
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackContext
from telegram.ext.filters import TEXT
import re

# Bot token
TOKEN = "7342363820:AAF3zh6emrgvg0aRQxqAAHrUXN_5vIqD1Dk"

# Storage for tracking user messages
last_messages = {}

# /start command handler
async def start(update: Update, context: CallbackContext):
    """Handles the /start command in private chats."""
    if update.message:
        await update.message.reply_text(
            "Hi! I am a moderator bot. I delete links and repetitive messages."
        )

# Handler for personal chat messages
async def handle_user_messages(update: Update, context: CallbackContext):
    """Handles messages in private chats."""
    if update.message is None or update.message.from_user is None:
        return

    user_id = update.message.from_user.id
    chat_id = update.message.chat.id
    message_text = update.message.text

    # Check for links
    if re.search(r"(https?://|www\.)", message_text):
        await update.message.delete()
        await context.bot.send_message(chat_id, "Links are not allowed!")
        return

    # Check for repetitive messages
    if chat_id not in last_messages:
        last_messages[chat_id] = {}

    if user_id in last_messages[chat_id]:
        if last_messages[chat_id][user_id] == message_text:
            await update.message.delete()
            await context.bot.send_message(chat_id, "Please do not repeat messages!")
            return

    # Save the message for spam tracking
    last_messages[chat_id][user_id] = message_text

# Handler for channel posts
async def handle_channel_post(update: Update, context: CallbackContext):
    """Handles messages in channels."""
    if update.channel_post is None:
        return

    chat_id = update.channel_post.chat_id
    message_text = update.channel_post.text

    # Check for links in the message
    if message_text and re.search(r"(https?://|www\.)", message_text):
        await update.channel_post.delete()
        await context.bot.send_message(chat_id, "Links are not allowed in this channel!")

# Error handler
async def error_handler(update: Update, context: CallbackContext):
    """Logs errors."""
    print(f"Error: {context.error}")

# Main function
def main():
    """Sets up and runs the bot."""
    application = ApplicationBuilder().token(TOKEN).build()

    # Add handlers for private chats
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(TEXT, handle_user_messages))

    # Add handler for channel posts
    application.add_handler(MessageHandler(TEXT, handle_channel_post))

    # Register the error handler
    application.add_error_handler(error_handler)

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
