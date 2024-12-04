from sqlalchemy import select
from telebot.types import Message

from backend.models import EmployeeEmail, Menu, Role  # noqa
from bot.crud.fill_db import CreateDataInDB
from bot.db import async_session
from bot.loader import bot_instance as bot
from bot.utils.logger import get_logger

logger = get_logger(__name__)

emails = [
    {'email': 'kirkill2024@yandex.by'},
    {'email': 'egortesla@gmail.com'},
    {'email': 'glofik@icloud.com'},
    {'email': 'vlasoff@yandex.ru'},
    {'email': 'quickliker@outlook.com'},
]

roles = [
    {'role_name': 'Кандидат'},
    {'role_name': 'Сотрудник'},
]

menus = [
    {
        'name': 'Агенство',
        'content': 'Мы работаем в сфере медийной рекламы с 2002 года. С 2007 года являемся частью коммуникационного холдинга Родная Речь (ex. Pubilcis Russia). Ведем рекламные кампании для 75 брендов и входим в ТОП-10 агентств нашего рекламного рынка.',
    },
    {
        'name': 'Данные сотрудников',
        'content': 'Василий Быков - Директор, +7 916 123 45 67\\nАнтонина Безносикова - Главный бухгалтер, +7 977 765 43 21',
    },
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
    data = emails
    await create_data_in_db(model, data)

    model = Role
    data = roles
    await create_data_in_db(model, data)

    model = Menu
    data = menus
    for role in roles:
        role_name = role['role_name']
        data_to_extend = await generate_menu(role_name=role_name)
        data.extend(data_to_extend)
    logger.info(f'{message.from_user.username} ГЕНЕРИРОВАЛ МЕНЮ')

    message_to_send = await create_data_in_db(model, data)
    await bot.send_message(
        message.chat.id,
        message_to_send,
    )
    logger.info(f'{message.from_user.username} РАБОТАЛ С БД')


async def create_data_in_db(model, data) -> str:
    create_crud = CreateDataInDB(model)
    check_db = await create_crud.check_db_is_empty(session=async_session)
    if check_db is not None:
        message_to_send = 'База данных уже БЫЛА заполнена'
    else:
        for item in data:
            await create_crud.fill_db_from_json(
                data=item, session=async_session
            )
        message_to_send = 'База данных УСПЕШНО заполнена'
    return message_to_send


async def generate_menu(role_name: str) -> list[dict]:
    """Генерация меню."""
    async with async_session() as asession:
        role_access = await asession.execute(
            select(Role).where(Role.role_name == role_name)
        )
        role_access = role_access.scalars().first()
        role_access = role_access.unique_id
    count = 1
    menu_with_role = []
    while count < 6:
        menu_dict = {
            'name': f'Меню для {role_name} {count}',
            'content': f'Контент для {role_name} {count}',
            'role_access': role_access,
        }
        menu_with_role.append(menu_dict)
        count += 1
    return menu_with_role
