# Это основной запускаемый файл.
# Заменить содержимое своим кодом.
import telebot
import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

if __name__ == '__main__':
    bot.polling()
