from telebot.types import Message

from backend.models import EmployeeEmail, Menu, Role
from bot.crud.fill_db import (
    create_data_in_db,
    create_data_in_db_no_check,
    generate_menu,
    generate_parent_menu,
    get_all_menu_id,
)
from bot.crud.telegram_menu import telegram_menu_crud
from bot.crud.telegram_user import telegram_users_crud
from bot.data.data import EMAILS, MENUS, ROLES
from bot.db import async_session
from bot.keyboard import build_keyboard
from bot.loader import bot_instance as bot
from bot.utils.logger import get_logger

from . import constants

logger = get_logger(__name__)
page = constants.PAGE


@bot.message_handler(commands=['start'])
async def handle_start(message: Message) -> None:
    """Обработчик команды /start."""
    global page
    page = constants.PAGE

    username = message.from_user.username
    first_name = message.from_user.first_name
    lastname = message.from_user.last_name
    telegram_id = message.from_user.id

    user_exists = await telegram_users_crud.check_user_exists(
        telegram_id=telegram_id,
        session=async_session,
    )

    role_id = None
    if not user_exists:
        data = {
            'username': username,
            'first_name': first_name,
            'last_name': lastname,
            'role_id': role_id,
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
        message_to_send = (
            f'Ура мы нашли вас в базе данных: ' f'{username} {telegram_id}'
        )

    menu_items = await telegram_users_crud.get_menu_for_user_roles(
        session=async_session,
        username=message.from_user.username,
    )

    reply_markup = await build_keyboard(menu_items=menu_items, page=page)

    await bot.send_message(
        message.chat.id,
        message_to_send,
        reply_markup=reply_markup,
    )

    logger.info(f'{message.from_user.username} запустил бота')


# ## УДАЛИТЬ # ## УДАЛИТЬ# ## УДАЛИТЬ# ## УДАЛИТЬ# ## УДАЛИТЬ# ## УДАЛИТЬ
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
        role_name = role['title']
        data_to_extend = await generate_menu(role_name=role_name)
        data.extend(data_to_extend)

    message_to_send = await create_data_in_db(model, data)

    parent_list_id = await get_all_menu_id()
    model = Menu
    data = []
    for parent_id in parent_list_id:
        for role in ROLES:
            role_name = role['title']
            data_to_extend = await generate_parent_menu(
                role_name=role_name,
                parent_id=parent_id,
            )
            data.extend(data_to_extend)
    message_to_send = await create_data_in_db_no_check(model, data)

    await bot.send_message(
        message.chat.id,
        message_to_send,
    )
    logger.info(f'{message.from_user.username} работал с базой данных')


# ## УДАЛИТЬ # ## УДАЛИТЬ# ## УДАЛИТЬ# ## УДАЛИТЬ# ## УДАЛИТЬ# ## УДАЛИТЬ


@bot.message_handler(content_types=['text'])
async def get_data_from_db(message: Message) -> None:
    """Обработчик текстовых сообщений."""
    global page

    menu_items = await telegram_users_crud.get_menu_for_user_roles(
        session=async_session,
        username=message.from_user.username,
    )

    menu_from_db = await telegram_menu_crud.get_content_by_menu_name(
        session=async_session,
        menu_name=message.text,
    )

    if menu_from_db is not None:
        unique_id = menu_from_db.unique_id
    else:
        unique_id = None

    menu_child_from_db = await telegram_menu_crud.get_menu_child_by_parent_id(
        session=async_session,
        parent_id=unique_id,
    )

    if menu_child_from_db is not None:
        if unique_id is not None:
            menu_items = await telegram_users_crud.get_menu_for_user_roles(
                session=async_session,
                username=message.from_user.username,
                parent_id=unique_id,
            )
            inline_keyboard = await build_keyboard(
                menu_items=menu_items,
                parent_id=unique_id,
                is_inline=True,
            )
            await bot.send_message(
                message.chat.id,
                text=menu_from_db.content,
                reply_markup=inline_keyboard,
            )
    else:
        await bot.send_message(
            message.chat.id,
            text=menu_from_db.content,
        )
    if message.text == constants.FORWARD_NAV_TEXT:
        page += 1
        reply_markup = await build_keyboard(
            menu_items=menu_items,
            page=page,
        )

        message_to_send = 'Переходим на след. страницу'

        await bot.send_message(
            message.chat.id,
            message_to_send,
            reply_markup=reply_markup,
        )

        logger.info(f'{message.from_user.username} перешел на стр. #{page}')
    if message.text == constants.BACK_NAV_TEXT:
        page -= 1

        reply_markup = await build_keyboard(
            menu_items=menu_items,
            page=page,
        )

        message_to_send = 'Переходим на пред. страницу'

        await bot.send_message(
            message.chat.id,
            message_to_send,
            reply_markup=reply_markup,
        )

        logger.info(f'{message.from_user.username} на перешел на стр. #{page}')


@bot.callback_query_handler(func=lambda call: True)
async def handle_callback(call):
    call_data = call.data.split('_')
    if call_data[0] == constants.SELECT_CALLBACK_PREFIX.split('_')[0]:
        message_to_send = await telegram_menu_crud.get_content_by_menu_id(
            session=async_session,
            unique_id=call_data[-1],
        )
        await bot.edit_message_text(
            text=message_to_send.content,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=call.message.reply_markup,
        )
    if call_data[0] == constants.NAV_CALLBACK_PREFIX.split('_')[0]:
        menu_from_db = await telegram_menu_crud.get_content_by_menu_id(
            session=async_session,
            unique_id=call_data[-1],
        )
        menu_items = await telegram_users_crud.get_menu_for_user_roles(
            session=async_session,
            username=call.from_user.username,
            parent_id=menu_from_db.unique_id,
        )
        inline_keyboard = await build_keyboard(
            menu_items=menu_items,
            parent_id=menu_from_db.unique_id,
            is_inline=True,
            page=int(call_data[1]),
        )
        message_to_send = f'Вы перешли на страницу {call_data[1]}'
        await bot.edit_message_text(
            text=message_to_send,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=inline_keyboard,
        )
