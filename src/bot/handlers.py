from telebot.types import Message

from backend.models.telegram_user import EmployeeEmail
from bot.crud.fill_db import CreateDataInDB
from bot.db import async_session
from bot.loader import bot_instance as bot
from bot.utils.logger import get_logger

logger = get_logger(__name__)

data = [
    {'email': 'kirkill2024@yandex.by'},
    {'email': 'egortesla@gmail.com'},
    {'email': 'glofik@icloud.com'},
    {'email': 'vlasoff@yandex.ru'},
    {'email': 'quickliker@outlook.com'},
]


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
    create_crud = CreateDataInDB(model)

    check_db = await create_crud.check_db_is_empty(session=async_session)
    print(check_db)
    if check_db is not None:
        message_to_send = 'База данных уже БЫЛА заполнена'
    else:
        for item in data:
            await create_crud.fill_db_from_json(
                data=item, session=async_session
            )
        message_to_send = 'База УСПЕШНО данных заполнена'

    await bot.send_message(
        message.chat.id,
        message_to_send,
    )
