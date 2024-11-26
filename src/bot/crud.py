from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.menu import Menu
from backend.models.telegram_user import TelegramUser


async def get_child_menu_for_role(session: AsyncSession,
                                  parent_id: int,
                                  role_id: Optional[str] = None) -> List[Menu]:
    """Получает дочерние элементы меню для inlineKeyboard с учетом роли.

    :param session: Асинхронная сессия базы данных.
    :param parent_id: Идентификатор родительского элемента меню.
    :param role_id: Идентификатор роли пользователя.
        Если None, то возвращаются элементы без учета роли.
    :return: Список дочерних элементов меню.
    """
    query = select(Menu).where(Menu.parent == parent_id)
    if role_id:
        query = query.where(Menu.role_access == role_id)
    result = await session.execute(query)
    return result.scalars().all()


async def get_child_menu_for_guest(session: AsyncSession,
                                   parent_id: int) -> List[Menu]:
    """Получает дочерние элементы меню для inlineKeyboard для гостей.

    :param session: Асинхронная сессия базы данных.
    :param parent_id: Идентификатор родительского элемента меню.
    :return: Список дочерних элементов меню для гостей.
    """
    query = select(Menu).where(Menu.parent == parent_id,
                               Menu.role_access.is_(None))
    result = await session.execute(query)
    return result.scalars().all()


async def get_parent_menu_for_role(
        session: AsyncSession,
        role_id: Optional[str] = None) -> List[Menu]:
    """Получает родительские элементы меню для replyKeyboard с учетом роли.

    :param session: Асинхронная сессия базы данных.
    :param role_id: Идентификатор роли пользователя.
        Если None, то возвращаются элементы без учета роли.
    :return: Список родительских элементов меню.
    """
    query = select(Menu).where(Menu.parent == 0)
    if role_id:
        query = query.where(Menu.role_access == role_id)
    result = await session.execute(query)
    return result.scalars().all()


async def get_parent_menu_for_guest(session: AsyncSession) -> List[Menu]:
    """Получает родительские элементы меню для replyKeyboard для гостей.

    :param session: Асинхронная сессия базы данных.
    :return: Список родительских элементов меню для гостей.
    """
    query = select(Menu).where(Menu.parent == 0, Menu.role_access.is_(None))
    result = await session.execute(query)
    return result.scalars().all()


# async def check_user_email(session: AsyncSession,
#                            username: str) -> bool:
#     """Проверяет наличие email у пользователя.

#     :param session: Асинхронная сессия базы данных.
#     :param username: Имя пользователя Telegram.
#     :return: True, если у пользователя есть email, иначе False.
#     """
#     query = select(TelegramUser).where(TelegramUser.username == username)
#     result = await session.execute(query)
#     user = result.scalar_one_or_none()
#     return user.email_id is not None if user else False


# async def check_user_role(session: AsyncSession,
#                           username: str) -> Optional[str]:
#     """Проверяет роль пользователя.

#     :param session: Асинхронная сессия базы данных.
#     :param username: Имя пользователя Telegram.
#     :return: Идентификатор роли пользователя,
#         если пользователь найден, иначе None.
#     """
#     query = select(TelegramUser).where(TelegramUser.username == username)
#     result = await session.execute(query)
#     user = result.scalar_one_or_none()
#     return user.role_id if user else None
