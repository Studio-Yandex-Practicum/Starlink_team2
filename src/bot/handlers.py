import aiofiles
import telebot
from telebot.states.asyncio.context import StateContext
from telebot.types import CallbackQuery, Message, ReplyParameters

from backend.utils.parser_csv import (
    MILESTONERUSSIA_PATTERN,
    STARLINKRUSSIA_PATTERN,
)
from bot.crud.telegram_menu import telegram_menu_crud
from bot.crud.telegram_user import telegram_users_crud
from bot.db import async_session
from bot.keyboard import build_keyboard, build_register_keyboard
from bot.loader import bot_instance as bot
from bot.states import MailRegistrationState
from bot.utils.logger import get_logger

from . import constants

logger = get_logger(__name__)
page = constants.PAGE
bot.add_custom_filter(telebot.asyncio_filters.TextMatchFilter())


@bot.message_handler(commands=['start'])
async def handle_start(message: Message) -> None:
    """Обработчик команды /start."""
    global page
    page = constants.PAGE

    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    telegram_id = message.from_user.id

    user_exists = await telegram_users_crud.check_user_exists(
        telegram_id=telegram_id,
        session=async_session,
    )

    if not user_exists:
        data = {
            constants.USERNAME_KEY: username,
            constants.FIRST_NAME_KEY: first_name,
            constants.LAST_NAME_KEY: last_name,
            constants.TELEGRAM_ID_KEY: telegram_id,
        }
        await telegram_users_crud.create_user(
            data=data,
            session=async_session,
        )
        message_to_send = constants.START_MESSAGE_NEW_USER + username
        await bot.send_message(
            message.chat.id,
            message_to_send,
        )
    else:
        message_to_send = constants.START_MESSAGE_EXIST_USER + username
    check_user_email = await telegram_users_crud.check_user_email(
        session=async_session,
        username=username,
    )
    if check_user_email is False:
        message_to_send = constants.START_MESSAGE_NO_EMAIL
        reply_markup = await build_register_keyboard()
    else:
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


@bot.message_handler(text=[constants.REGISTER_BUTTON_TEXT])
async def email_register_message(
    message: Message,
    state: StateContext,
) -> None:
    """Функция обработки регистрации по email."""
    await state.set(MailRegistrationState.mail)
    await bot.send_message(
        message.chat.id,
        constants.REGISTER_TEXT,
        reply_parameters=ReplyParameters(message_id=message.message_id),
    )


@bot.message_handler(state=MailRegistrationState.mail)
async def email_register_method(
    message: Message,
    state: StateContext,
) -> None:
    """Функция обработки регистрации по email."""
    if message.text.count('@') != 1 or (
        not MILESTONERUSSIA_PATTERN.search(message.text)
        and not STARLINKRUSSIA_PATTERN.search(message.text)
    ):
        await bot.send_message(
            message.chat.id,
            constants.EMAIL_WITH_WRONG_PATTERN,
        )
    else:
        await email_register(message)
    await state.delete()


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

    if menu_from_db is not None and menu_from_db.content == '':
        text_to_send = constants.NO_CONTENT_TEXT
    else:
        text_to_send = menu_from_db.content

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
                text=text_to_send,
                reply_markup=inline_keyboard,
            )
    else:
        await bot.send_message(
            message.chat.id,
            text=text_to_send,
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

        logger.info(
            f'{message.from_user.username} на перешел на стр. #{page}',
        )
    if message.text == constants.NO_REGISTER_BUTTON_TEXT:
        reply_markup = await build_keyboard(
            menu_items=menu_items,
            page=constants.PAGE,
        )
        message_to_send = constants.START_MESSAGE_NO_EMAIL_CONTINUE

        await bot.send_message(
            message.chat.id,
            message_to_send,
            reply_markup=reply_markup,
        )
    # if message.text == constants.REGISTER_BUTTON_TEXT:
    #     message_to_send = constants.REGISTER_TEXT
    #     message = await bot.send_message(
    #         message.chat.id,
    #         message_to_send,
    #     )
    # if re.match(constants.EMAIL_PATTERN, message.text):
    #     await email_register(message)


async def email_register(message: Message) -> None:
    """Функция обработки регистрации по email."""
    check_user_email = await telegram_users_crud.check_user_email(
        session=async_session,
        username=message.from_user.username,
    )
    if check_user_email is True:
        await bot.send_message(
            message.chat.id,
            constants.REGISTERED,
        )
    else:
        email_id = await telegram_users_crud.get_email_id_from_db(
            session=async_session,
            email=message.text,
        )
        if email_id is not None:
            add_email = await telegram_users_crud.add_email_to_telegram_user(
                session=async_session,
                username=message.from_user.username,
                email_id=email_id.unique_id,
            )
            if add_email is not None:
                menu_items = (
                    await telegram_users_crud.get_menu_for_user_roles(
                        session=async_session,
                        username=message.from_user.username,
                    )
                )
                reply_markup = await build_keyboard(
                    menu_items=menu_items,
                    page=constants.PAGE,
                )
                await bot.send_message(
                    message.chat.id,
                    constants.EMAIL_SUCCESS_REGISTERED,
                    reply_markup=reply_markup,
                )
            else:
                await bot.send_message(
                    message.chat.id,
                    constants.EMAIL_ALREADY_REGISTERED,
                )
        else:
            await bot.send_message(
                message.chat.id,
                constants.EMAIL_NOT_FOUND,
            )


@bot.callback_query_handler(func=lambda call: True)
async def handle_callback(call: CallbackQuery) -> None:
    """Функция обработки callback-запросов."""
    call_data = call.data.split('_')
    if call_data[0] == constants.SELECT_CALLBACK_PREFIX.split('_')[0]:
        menu_from_db = await telegram_menu_crud.get_content_by_menu_id(
            session=async_session,
            unique_id=call_data[-1],
        )
        if menu_from_db is not None and menu_from_db.content == '':
            message_to_send = constants.NO_CONTENT_TEXT
        else:
            message_to_send = menu_from_db.content
        if menu_from_db.image_link:
            await bot.send_photo(
                chat_id=call.message.chat.id,
                photo=await aiofiles.open(
                    f'backend/static/images/{menu_from_db.image_link}',
                    'rb',
                ),
                caption=message_to_send,
                reply_markup=call.message.reply_markup,
            )
        await bot.edit_message_text(
            text=message_to_send,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=call.message.reply_markup,
        )
    if (
        call_data[0] == constants.NAV_CALLBACK_PREFIX.split('_')[0]
        or call_data[0] == constants.OPEN_CALLBACK_PREFIX.split('_')[0]
    ):
        menu_from_db = await telegram_menu_crud.get_content_by_menu_id(
            session=async_session,
            unique_id=call_data[-1],
        )
        menu_items = await telegram_users_crud.get_menu_for_user_roles(
            session=async_session,
            username=call.from_user.username,
            parent_id=menu_from_db.unique_id,
        )
        if menu_from_db is not None and menu_from_db.content == '':
            message_to_send = constants.NO_CONTENT_TEXT
        else:
            message_to_send = menu_from_db.content
        if len(call_data) > 2:
            page = int(call_data[1])
            message_to_send = f'Вы перешли на страницу {page}'
        else:
            page = constants.PAGE
        inline_keyboard = await build_keyboard(
            menu_items=menu_items,
            parent_id=menu_from_db.unique_id,
            is_inline=True,
            page=page,
        )
        await bot.edit_message_text(
            text=message_to_send,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=inline_keyboard,
        )
