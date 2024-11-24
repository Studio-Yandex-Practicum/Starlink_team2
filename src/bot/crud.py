from sqlalchemy import select

import constants
import keyboard

from src.backend.models.menu import Menu
from src.backend.models.telegram_user import TelegramUser


async def check_user_email(session, user_id):
    """
    Проверяет, есть ли у пользователя email.

    :param session: Сессия базы данных.
    :param user_id: Идентификатор пользователя.
    :return: True, если у пользователя есть email, иначе False.
    """
    result = await session.execute(
        select(TelegramUser)
        .where(TelegramUser.id == user_id)
        .where(TelegramUser.email_id.isnot(None))
    )
    return result.scalar() is not None


async def check_user_role(session, user_id):
    """
    Проверяет, есть ли у пользователя роль.

    :param session: Сессия базы данных.
    :param user_id: Идентификатор пользователя.
    :return: True, если у пользователя есть роль, иначе False.
    """
    result = await session.execute(
        select(TelegramUser)
        .where(TelegramUser.id == user_id)
        .where(TelegramUser.role_id.isnot(None))
    )
    return result.scalar() is not None


async def fetch_menu_items(session, parent_id=None, role_access=None):
    """
    Получает элементы меню на основе родительского ID и доступности по роли.

    :param session: Сессия базы данных.
    :param parent_id: Идентификатор родительского элемента меню (по
        умолчанию None).
    :param role_access: Список ролей для фильтрации доступных элементов меню
        (по умолчанию None).
    :return: Список элементов меню в формате словарей.
    """
    query = select(Menu).where(Menu.parent == parent_id)
    if role_access is not None:
        query = query.where(Menu.role_access.in_(role_access))
    else:
        query = query.where(Menu.role_access.is_(None))
    result = await session.execute(query)
    return [
        {
            constants.UNIQUE_ID_KEY: menu.unique_id,
            constants.NAME_KEY: menu.name,
            constants.PARENT_KEY: menu.parent,
            constants.IS_FOLDER_KEY: menu.is_folder,
            constants.ROLES_KEY: [menu.role_access] if menu.role_access else []
        }
        for menu in result.scalars().all()
    ]


async def fetch_and_build_inline_keyboard(session, user_roles, parent_id=None):
    """
    Получение дочернего меню для сотрудников с учетом доступности по роли.

    :param session: Сессия базы данных.
    :param user_roles: Список ролей пользователя.
    :param parent_id: Идентификатор родительского элемента меню (по
        умолчанию None).
    :return: InlineKeyboard клавиатура с дочерними элементами меню.
    """
    menu_items = await fetch_menu_items(session, parent_id, user_roles)
    return await keyboard.build_inline_keyboard(menu_items, user_roles,
                                                parent_id)


async def fetch_and_build_guest_inline_keyboard(session, parent_id=None):
    """
    Получение дочернего меню для гостей.

    :param session: Сессия базы данных.
    :param parent_id: Идентификатор родительского элемента меню (по
        умолчанию None).
    :return:InlineKeyboard клавиатура с дочерними элементами меню
        для гостей.
    """
    menu_items = await fetch_menu_items(session, parent_id)
    return await keyboard.build_inline_keyboard(menu_items, [], parent_id)


async def fetch_and_build_reply_keyboard(session, user_roles):
    """
    Получение родительского меню для сотрудников с учетом доступности по роли.

    :param session: Сессия базы данных.
    :param user_roles: Список ролей пользователя.
    :return: ReplyKeyboard клавиатура с родительскими элементами меню для
        сотрудников.
    """
    menu_items = await fetch_menu_items(session, 0, user_roles)
    return await keyboard.build_reply_keyboard(menu_items, user_roles)


async def fetch_and_build_guest_reply_keyboard(session):
    """
    Получение родительского меню для гостей.

    :param session: Сессия базы данных.
    :return: ReplyKeyboard клавиатура с родительскими элементами меню для
        гостей.
    """
    menu_items = await fetch_menu_items(session, 0)
    return await keyboard.build_reply_keyboard(menu_items, [])
