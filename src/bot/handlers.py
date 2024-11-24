from loader import bot_instance as bot

from telebot.types import Message

from bot.utils.logger import get_logger
from bot.crud.telegram_user import telegram_users_crud
from backend.core.db import AsyncSessionLocal as get_async_session
from bot.db import async_session
logger = get_logger(__name__)


@bot.message_handler(commands=['start'])
async def handle_start(message: Message) -> None:
    
    """Обработчик команды /start."""
    
    print(f'{await telegram_users_crud.check_user_exists(message.from_user.id, session=async_session)}')
    await bot.send_message(
        message.chat.id,
        'Приветственное сообщение для кандидатов',
    )
    logger.info(f'{message.from_user.username} запустил бота')
