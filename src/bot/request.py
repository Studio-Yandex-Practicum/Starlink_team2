from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from telebot.types import Message

#from DB.model import TelegramUser, Role

async def chek_user_role(
        message: Message,
        session: AsyncSession 
) -> Role:
    """Прверка роли пользователя,
    если пользователя нет, то создается запись в БД,
    Возвращает роль
    :param message: объект сообщение из Telegram
    :param session: мейкер асинхронной сессии

    """
    db_tg_user = await session.scalar(
        select(TelegramUser).where(TelegramUser.tg_id==message.from_user.id)
    )
    if db_tg_user:
        return db_tg_user.role
    return add_user(message)

def chek_email(
        tg_id: int
) -> bool:
    """Проверка почты в списке сотрудников"""
    pass

async def add_user(
        message: Message,
        session: AsyncSession
):
    """Добавление пользователя в БД
    :param message: объект сообщение из Telegram
    :param session: мейкер асинхронной сессии"""

    session.add(
        TelegramUser(
            UniqueID=message.from_user.id,
            Username=message.from_user.username,
            Role=0,
            Name=message.from_user.first_name,
            Last_Name = message.from_user.last_name,
            Email=chek_email(),
            Active=True
        )
    )
    pass