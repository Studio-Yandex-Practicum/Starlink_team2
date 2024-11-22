#from database import async_session
#from bd import Email, Role, TelegramUser
from sqlalchemy.ext.asyncio import AsyncSession
from telebot.types import Message


async def start_chek_user(
        message: Message,
) -> TelegramUser:
    """Проверка пользователя."""
    async with async_session() as session:
        user_bd = await session.query(TelegramUser).get(message.from_user.id)
    if user_bd:
        await chek_user_email(user_bd)
        return user_bd
    return await add_user(message)


async def chek_user_email(
        user_bd: TelegramUser,
) -> None:
    """Проверка почты в списке сотрудников.

    :param user_bd: объект TelegramUser.
    """
    async with async_session() as session:
        bd_email = await session.query(Email).get(bd_email.email)
        if not(bd_email):
            user_bd.role = 0
            await session.refresh(user_bd)
            await session.commit()


async def add_user(
        message: Message,
) -> TelegramUser:
    """Добавление пользователя в БД.

    :param message: объект сообщение из Telegram.
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
    async with async_session() as session:
        session.add(TelegramUser(new_user))
        await session.commit()
    return new_user
