from telebot.types import Message

from bot.crud.telegram_menu import telegram_menu_crud
from bot.crud.telegram_user import telegram_users_crud
from bot.db import async_session

# test
from bot.keyboard_test import build_reply_keyboard, filter_accessible_items
from bot.loader import bot_instance as bot
from bot.utils.logger import get_logger

logger = get_logger(__name__)

# geust role ID
GUEST_ROLE_ID = '67bb8356-739b-4918-9694-11eeb81f577e'


@bot.message_handler(commands=['start'])
async def handle_start(message: Message) -> None:
    """Обработчик команды /start."""
    username = message.from_user.username
    telegram_id = message.from_user.id

    user_exists = await telegram_users_crud.check_user_exists(
        telegram_id=telegram_id,
        session=async_session,
    )

    menu_items_for_guest = await telegram_menu_crud.get_parent_menu_for_role(
        session=async_session,
        role_id=GUEST_ROLE_ID,
    )
    if not user_exists:
        menu_items = menu_items_for_guest

        data = {
            'username': username,
            'role_id': GUEST_ROLE_ID,
            'telegram_id': telegram_id,
        }
        await telegram_users_crud.create_user(
            data=data,
            session=async_session,
        )
        message_to_send = (
            f'Вас нет в базе данных, '
            f'создан новый пользователь: {username} {telegram_id}'
        )
    else:
        menu_items = menu_items_for_guest

        message_to_send = (
            f'Ура мы нашли вас в базе данных: ' f'{username} {telegram_id}'
        )

    role_list = [GUEST_ROLE_ID]

    print(menu_items)

    accessible_items = await filter_accessible_items(
        menu_items, role_list, None
    )
    print(accessible_items)

    reply_markup = await build_reply_keyboard(menu_items, role_list)

    # await bot.send_message(message.chat.id, message_to_send)

    await bot.send_message(
        message.chat.id, message_to_send, reply_markup=reply_markup
    )

    logger.info(f'{message.from_user.username} запустил бота')


@bot.callback_query_handler(func=lambda call: True)
async def callback_query(call):
    print(call.data)
    if call.data:
        bot.answer_callback_query(call.id, 'Answer is Yes')
