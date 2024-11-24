from telebot.types import Message

from bot.crud.telegram_user import telegram_users_crud
from bot.db import async_session
from bot.utils.logger import get_logger
from loader import bot_instance as bot

logger = get_logger(__name__)


@bot.message_handler(commands=['start'])
async def handle_start(message: Message) -> None:
    """Обработчик команды /start."""
    checked_user = await telegram_users_crud.check_user_exists(
        message.from_user.id,
        session=async_session,
    )
    if not checked_user:
        data = {
            'telegram_id': str(message.from_user.id),
            'username': message.from_user.username,
            'name': message.from_user.first_name,
            'last_name': message.from_user.last_name,
        }
        await telegram_users_crud.create_user(
            data=data,
            session=async_session,
        )
        await bot.send_message(
            message.chat.id,
            'Приветственное сообщение для кандидатов',
        )
    else:
        await bot.send_message(
            message.chat.id,
            'Приветственное сообщение для кандидатов',
        )
    logger.info(f'{message.from_user.username} запустил бота')
