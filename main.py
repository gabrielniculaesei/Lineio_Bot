import os
import telebot

API_KEY = os.getenv('API_KEY')  
print(API_KEY)  
bot = telebot.TeleBot("7638041299:AAFoiF_urY-ASp1I9RMDTz-h7tPs78r2G70")



@bot.message_handler(commands=['Greet'])
def greet(message):  # Correct indentation
    bot.send_message(message.chat.id, "Hey! Hows it going?")

bot.polling()
