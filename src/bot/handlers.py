from telebot.types import Message

from backend.models import EmployeeEmail, Menu, Role
from bot.crud.fill_db import create_data_in_db, generate_menu
from bot.crud.telegram_menu import telegram_menu_crud
from bot.crud.telegram_user import telegram_users_crud
from bot.data.data import EMAILS, MENUS, ROLES
from bot.db import async_session
from bot.keyboard import build_reply_keyboard
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
    name = message.from_user.first_name
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
            'name': name,
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

    menu_items = await get_menu_for_user_roles(
        username=message.from_user.username,
    )

    reply_markup = await build_reply_keyboard(menu_items=menu_items, page=page)

    await bot.send_message(
        message.chat.id, message_to_send, reply_markup=reply_markup,
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


@bot.message_handler(content_types=['text'])
async def get_data_from_db(message: Message) -> None:
    """Обработчик текстовых сообщений."""
    global page

    menu_items = await get_menu_for_user_roles(
        username=message.from_user.username,
    )

    text_from_db = await telegram_menu_crud.get_content_by_menu_name(
        session=async_session,
        menu_name=message.text,
    )

    if text_from_db is not None:
        await bot.send_message(
            message.chat.id,
            text=text_from_db,
        )
    elif message.text == constants.FORWARD_NAV_TEXT:
        page += 1
        reply_markup = await build_reply_keyboard(
            menu_items=menu_items, page=page,
        )

        message_to_send = 'Переходим на след. страницу'

        await bot.send_message(
            message.chat.id, message_to_send, reply_markup=reply_markup,
        )

        logger.info(f'{message.from_user.username} перешел на стр. #{page}')
    elif message.text == constants.BACK_NAV_TEXT:
        page -= 1

        reply_markup = await build_reply_keyboard(
            menu_items=menu_items, page=page,
        )

        message_to_send = 'Переходим на пред. страницу'

        await bot.send_message(
            message.chat.id, message_to_send, reply_markup=reply_markup,
        )

        logger.info(f'{message.from_user.username} на перешел на стр. #{page}')


async def get_menu_for_user_roles(username: str) -> list[dict] | None:
    """Функция для получения меню для пользователя."""
    user_role_id = await telegram_users_crud.get_user_role(
        session=async_session,
        username=username,
    )

    # тестовые роли для проверки работы бота
    test_role_id_1 = await telegram_menu_crud.get_role_id_by_name(
        session=async_session,
        role_name='Кандидат',
    )
    test_role_id_2 = await telegram_menu_crud.get_role_id_by_name(
        session=async_session,
        role_name='Сотрудник',
    )

    role_id_list = [user_role_id, test_role_id_1, test_role_id_2]
    menu_items = []
    for role in role_id_list:
        menu_item = await telegram_menu_crud.get_menu_for_role(
            session=async_session,
            role_id=role,
        )
        menu_items.extend(menu_item)
    return menu_items
