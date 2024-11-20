from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from telebot.types import Message

#from DB.model import TelegramUser, Role, Email


async def start_chek_user(
        message: Message,
        session: AsyncSession,
) -> TelegramUser:
    """Проверка пользователя."""
    user_bd = await session.query(TelegramUser).get(message.from_user.id)
    if user_bd:
        await chek_user_email(user_bd)
        return user_bd
    return await add_user(message)


async def chek_user_email(
        user_bd: TelegramUser,
        session: AsyncSession,
) -> None:
    """Проверка почты в списке сотрудников.

    :param user_bd: объект TelegramUser.
    """
    bd_email = await session.query(Email).get(bd_email.email)
    if not(bd_email):
        user_bd.role = 0
        await session.refresh(user_bd)


async def add_user(
        message: Message,
        session: AsyncSession,
) -> TelegramUser:
    """Добавление пользователя в БД.

    :param message: объект сообщение из Telegram.
    :param session: мейкер асинхронной сессии.
    """
    new_user = TelegramUser(
            UniqueID=message.from_user.id,
            Username=message.from_user.username,
            Role=0,
            Name=message.from_user.first_name,
            Last_Name = message.from_user.last_name,
            Email=0,
            Active=True,
        )
    session.add(new_user)
    return new_user
