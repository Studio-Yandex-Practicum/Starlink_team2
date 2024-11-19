from loader import bot
from telebot.types import Message


@bot.message_handler(commands=['start'])
def handle_start(message: Message):
    bot.reply_to(message, 'Привет! Я бот.')
