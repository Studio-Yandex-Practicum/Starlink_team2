from telebot.types import Message

from bot.crud.telegram_menu import telegram_menu_crud
from bot.crud.telegram_user import telegram_users_crud
from bot.db import async_session
from bot.keyboard import build_reply_keyboard
from bot.test_keyboard import start_menu_keyboard, start_menu_with_email
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
            'Приветственное сообщение для новых кандидатов',
            reply_markup=start_menu_keyboard,
            )
    else:
        if await telegram_users_crud.check_user_email(
            session=async_session,
            username=message.from_user.username,
        ):
            await bot.send_message(
                message.chat.id,
                'Приветственное сообщение для работников с Email',
                reply_markup=start_menu_with_email,
            )
        else:
            keyboard = await build_reply_keyboard(
                await telegram_menu_crud.get_parent_menu_for_guest(
                    session=async_session,
                ),
                user_roles=await telegram_users_crud.get_user_list_roles(
                    session=async_session,
                    username=message.from_user.username,
                )
            )
            await bot.send_message(
                message.chat.id,
                f'С возращением {message.from_user.username}!',
                reply_markup=keyboard,
            )

    logger.info(f'{message.from_user.username} запустил бота')
