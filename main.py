from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Bot credentials
TOKEN: Final = '7638041299:AAFoiF_urY-ASp1I9RMDTz-h7tPs78r2G70'
BOT_USERNAME: Final = '@Lineio_bot'


# Command handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, how can I help you ?")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please type something so I can respond to you")


async def custom_comand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command")


# Response handling
def handle_responde(text: str) -> str:
    # Type-sensitive language
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hey'

    if 'how are you' in processed:
        return 'Fine, how about you?'

    return 'I do not understand :('


# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    response: str = handle_responde(text)

    print('Bot:', response)
    await update.message.reply_text(response)


# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_comand))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=3)