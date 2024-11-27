from telebot.types import Message

from bot.crud.telegram_menu import telegram_menu_crud
from bot.crud.telegram_user import telegram_users_crud
from bot.db import async_session
from bot.keyboard import build_reply_keyboard
#from bot.test_keyboard import start_menu_keyboard, start_menu_with_email
from bot.utils.logger import get_logger
from loader import bot_instance as bot

logger = get_logger(__name__)


@bot.message_handler(commands=['start'])
async def handle_start(message: Message) -> None:
    """Обработчик команды /start."""
    username = message.from_user.username
    checked_user = await telegram_users_crud.get_user_by_username(
        username=message.from_user.username,
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
        user_role = None
        message_text = 'Приветственное сообщение для новых кандидатов'
        menu_items = await telegram_menu_crud.get_parent_menu_for_guest(
            session=async_session,
        )
    else:
        if await telegram_users_crud.check_user_email(
            session=async_session,
            username=message.from_user.username,
        ):
            user_role = await telegram_users_crud.check_user_role(
                session=async_session,
                username=username,
            )
            message_text = 'Приветственное сообщение для работников с Email'
            menu_items = await telegram_menu_crud.get_parent_menu_for_role(
                session=async_session,
                role_id=checked_user.role_id,
            )
        else:
            user_role = None
            message_text = 'Приветственное сообщение для работников без Email'
            menu_items = await telegram_menu_crud.get_parent_menu_for_guest(
                session=async_session,
            )

    keyboard = await build_reply_keyboard(
        menu_items=menu_items,
        user_roles=[user_role] if user_role else [None]
    )
    await bot.send_message(
        message.from_user.id,
        message_text,
        reply_markup=keyboard,
    )

    logger.info(f'{message.from_user.username} запустил бота')
