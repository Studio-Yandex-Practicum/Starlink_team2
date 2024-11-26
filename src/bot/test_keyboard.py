from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

start_menu_keyboard = ReplyKeyboardMarkup(
    one_time_keyboard=True,
    resize_keyboard=True,
).add(KeyboardButton('О компании'),
                       KeyboardButton('Новости'),
                       KeyboardButton('Пройти регистрацию'))



start_menu_with_email = ReplyKeyboardMarkup(
    one_time_keyboard=True,
    resize_keyboard=True,
).add(KeyboardButton('О компании'),
                       KeyboardButton('Новости'),
                       KeyboardButton('Quiz'))
