from typing import Final
from telegram import Update, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import random

# Bot credentials
TOKEN: Final = '7638041299:AAFoiF_urY-ASp1I9RMDTz-h7tPs78r2G70'
BOT_USERNAME: Final = '@Lineio_bot'

# NewsAPI credentials
NEWS_API_KEY: Final = 'fd8ce53f456946cd83b6b99d9463fcb6' 
NEWS_API_URL: Final = 'https://newsapi.org/v2/top-headlines'


# Fetch news from NewsAPI
def fetch_news(category: str):
    params = {
        'category': category,
        'apiKey': NEWS_API_KEY,
        'country': 'us',  # Adjust to your desired country
    }
    response = requests.get(NEWS_API_URL, params=params).json()
    articles = response.get('articles', [])
    if articles:
        # Pick a random article
        article = random.choice(articles)
        title = article['title']
        description = article['description']
        url = article['url']
        image_url = article.get('urlToImage')
        return title, description, url, image_url
    return None, None, None, None


# Command handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please specify a category like sports, technology, or politics.")
        return

    category = context.args[0].lower()
    title, description, url, image_url = fetch_news(category)
    
    if title:
        response_message = f"Here is a random top news in *{category.capitalize()}*:\n\n" \
                           f"*{title}*\n{description}\n\n[Read more]({url})"
        if image_url:
            await update.message.reply_photo(photo=image_url, caption=response_message, parse_mode='Markdown')
        else:
            await update.message.reply_text(response_message, parse_mode='Markdown')
    else:
        await update.message.reply_text(f"No news found for the category: {category}")


# Handle category messages directly (without `/start`)
async def handle_category_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    category = update.message.text.lower()
    valid_categories = ["sports", "technology", "politics"]
    
    if category in valid_categories:
        title, description, url, image_url = fetch_news(category)
        if title:
            response_message = f"Here is a random top news in *{category.capitalize()}*:\n\n" \
                               f"*{title}*\n{description}\n\n[Read more]({url})"
            if image_url:
                await update.message.reply_photo(photo=image_url, caption=response_message, parse_mode='Markdown')
            else:
                await update.message.reply_text(response_message, parse_mode='Markdown')
        else:
            await update.message.reply_text(f"No news found for the category: {category}")
    else:
        await update.message.reply_text(f"Unknown category: {category}. Available categories are: sports, technology, politics.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Type a category like 'sports', 'technology', or 'politics' to get the latest news.")


# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    await update.message.reply_text(f"I didn't understand: {text}")

#Custom command
async def custom_comand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command")

# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_comand))

    # Messages: Handle category messages like "sports"
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_category_message))

    # Messages: Handle general text messages (for unrecognized inputs)
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval=3)
