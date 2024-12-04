from telebot.types import Message

from backend.models import EmployeeEmail, Menu, Role
from bot.crud.fill_db import create_data_in_db, generate_menu
from bot.data.data import EMAILS, MENUS, ROLES
from bot.loader import bot_instance as bot
from bot.utils.logger import get_logger

logger = get_logger(__name__)


@bot.message_handler(commands=['start'])
async def handle_start(message: Message) -> None:
    """Обработчик команды /start."""
    await bot.send_message(
        message.chat.id,
        'Приветственное сообщение',
    )
    logger.info(f'{message.from_user.username} запустил бота')


@bot.message_handler(commands=['db'])
async def handle_db(message: Message) -> None:
    """Обработчик команды /db."""
    model = EmployeeEmail
    data = EMAILS
    await create_data_in_db(model, data)

    model = Role
    data = ROLES
    await create_data_in_db(model, data)

    model = Menu
    data = MENUS
    for role in ROLES:
        role_name = role['role_name']
        data_to_extend = await generate_menu(role_name=role_name)
        data.extend(data_to_extend)

    message_to_send = await create_data_in_db(model, data)
    await bot.send_message(
        message.chat.id,
        message_to_send,
    )
    logger.info(f'{message.from_user.username} работал с базой данных')
