from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

start_menu_keyboard = ReplyKeyboardMarkup().add(KeyboardButton('О компании'),
                       KeyboardButton('Новости'),
                       KeyboardButton('Пройти регистрацию'))



start_menu_with_email = ReplyKeyboardMarkup().add(KeyboardButton('О компании'),
                       KeyboardButton('Новости'),
                       KeyboardButton('Quiz'))
