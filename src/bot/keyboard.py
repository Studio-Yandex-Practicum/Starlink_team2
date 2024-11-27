from math import ceil
from typing import List, Optional, Tuple, TypedDict, Union

from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from sqlalchemy.dialects.postgresql import UUID as pg_UUID

import bot.constants as constants



class MenuItem(TypedDict):
    """Определяет структуру данных для каждого элемента меню."""

    # UniqueID: int
    UniqueID: pg_UUID
    Name: str
    Parent: Optional[int]
    Is_folder: bool
    # Roles: List[str]
    Roles: pg_UUID


async def filter_accessible_items(
        menu_items: List[MenuItem],
        user_roles: List[str],
        parent_id: Optional[int],
) -> List[MenuItem]:
    """Фильтрует список элементов меню по доступности.

    :param menu_items: Список всех элементов меню.
    :param user_roles: Список ролей пользователя.
    :param parent_id: Идентификатор родительского элемента.
        Если `None`, фильтруются элементы верхнего уровня.
    :return: Список доступных элементов меню.
    """
    return [
        item for item in menu_items
        if item[constants.PARENT_KEY] == parent_id
           and set(item[constants.ROLES_KEY]).intersection(user_roles)
    ]


async def paginate_items(
        items: List[MenuItem],
        page: int,
        items_per_page: int,
) -> Tuple[List[MenuItem], int]:
    """Разбивает список элементов на страницы и возвращает элементы страницы.

    :param items: Полный список элементов для пагинации.
    :param page: Номер текущей страницы (начиная с 1).
    :param items_per_page: Количество элементов на одной странице.
    :return: Кортеж из списка элементов текущей и общего количества страниц.
    """
    total_pages = max(1, ceil(len(items) / items_per_page))
    current_page = max(1, min(page, total_pages))
    start = (current_page - 1) * items_per_page
    end = start + items_per_page
    return items[start:end], total_pages


async def build_navigation_buttons(
        page: int,
        total_pages: int,
        parent_id: Optional[int] = None,
        is_inline: bool = False,
) -> list:
    """Создаёт кнопки навигации для клавиатуры (Reply или Inline).

    :param page: Номер текущей страницы.
    :param total_pages: Общее количество страниц.
    :param parent_id: Идентификатор родительского элемента
        для передачи в callback_data. По умолчанию `None`.
    :param is_inline: Флаг, указывающий,
        создавать ли inline-кнопки. По умолчанию `False`.
    :return: Список кнопок навигации.
    """
    buttons = []
    if total_pages > 1:
        if page > 1:
            if is_inline:
                buttons.append(
                    InlineKeyboardButton(
                        constants.BACK_NAV_TEXT,
                        callback_data=f"{constants.NAV_CALLBACK_PREFIX}"
                                      f"{page - 1}_{parent_id}",
                    ),
                )
            else:
                buttons.append(KeyboardButton(constants.BACK_NAV_TEXT))
        if page < total_pages:
            if is_inline:
                buttons.append(
                    InlineKeyboardButton(
                        constants.FORWARD_NAV_TEXT,
                        callback_data=f"{constants.NAV_CALLBACK_PREFIX}"
                                      f"{page + 1}_{parent_id}",
                    ),
                )
            else:
                buttons.append(KeyboardButton(constants.FORWARD_NAV_TEXT))
    return buttons


async def build_menu_buttons(
        menu_items: List[MenuItem],
        user_roles: List[str],
        parent_id: Optional[int] = None,
        page: int = constants.PAGE,
        items_per_page: int = constants.ITEMS_PER_PAGE,
        buttons_per_row: int = constants.BUTTONS_PER_ROW,
        is_inline: bool = False,
) -> list:
    """Создаёт список кнопок меню с учётом пагинации и доступности элементов.

    :param menu_items: Список всех элементов меню.
    :param user_roles: Список ролей пользователя.
    :param parent_id: Идентификатор родительского элемента.
        По умолчанию `None`.
    :param page: Номер текущей страницы для отображения.
        По умолчанию `PAGE`.
    :param items_per_page: Количество элементов на одной странице.
        По умолчанию `ITEMS_PER_PAGE`.
    :param buttons_per_row: Количество кнопок в одном ряду.
        По умолчанию `BUTTONS_PER_ROW`.
    :param is_inline: Флаг, указывающий, создавать ли inline-кнопки.
        По умолчанию `False`.
    :return: Список рядов кнопок для меню.
    """
    accessible_items, _ = await paginate_items(
        await filter_accessible_items(menu_items, user_roles, parent_id),
        page, items_per_page,
    )
    if not accessible_items:
        if is_inline:
            return [[InlineKeyboardButton(constants.NO_ITEMS_TEXT,
                                          callback_data=constants.NOOP)]]
        return [[KeyboardButton(constants.NO_ITEMS_TEXT)]]

    def create_button(item: MenuItem) -> Union[InlineKeyboardButton,
    KeyboardButton]:
        if is_inline:
            if item[constants.IS_FOLDER_KEY]:
                callback_data = (f"{constants.OPEN_CALLBACK_PREFIX}"
                                 f"{item[constants.UNIQUE_ID_KEY]}")
            else:
                callback_data = (f"{constants.SELECT_CALLBACK_PREFIX}"
                                 f"{item[constants.UNIQUE_ID_KEY]}")
            return InlineKeyboardButton(text=item[constants.NAME_KEY],
                                        callback_data=callback_data)
        return KeyboardButton(item[constants.NAME_KEY])

    buttons = [create_button(item) for item in accessible_items]
    return [buttons[i:i + buttons_per_row] for i in
            range(0, len(buttons), buttons_per_row)]


async def build_keyboard(
        menu_items: List[MenuItem],
        # user_roles: List[str],
        user_roles: str,
        parent_id: Optional[int] = None,
        page: int = constants.PAGE,
        items_per_page: int = constants.ITEMS_PER_PAGE,
        buttons_per_row: int = constants.BUTTONS_PER_ROW,
        is_inline: bool = False) -> Union[ReplyKeyboardMarkup,
InlineKeyboardMarkup]:
    """Создает клавиатуру (Reply или Inline) с поддержкой иерархии и пагинации.

    :param menu_items: Список всех элементов меню.
    :param user_roles: Список ролей пользователя.
    :param parent_id: Идентификатор родительского элемента. По умолчанию None.
    :param page: Номер текущей страницы для отображения. По умолчанию PAGE.
    :param items_per_page: Количество элементов на одной странице.
        По умолчанию ITEMS_PER_PAGE.
    :param buttons_per_row: Количество кнопок в одном ряду.
        По умолчанию BUTTONS_PER_ROW.
    :param is_inline: Флаг, указывающий, создавать ли inline-кнопки.
        По умолчанию False.
    :return: Объект клавиатуры: ReplyKeyboardMarkup или InlineKeyboardMarkup.
    """
    _, total_pages = await paginate_items(
        await filter_accessible_items(menu_items, user_roles, parent_id),
        page, items_per_page,
    )
    keyboard = await build_menu_buttons(
        menu_items,
        user_roles,
        parent_id,
        page,
        items_per_page,
        buttons_per_row,
        is_inline,
    )
    navigation_buttons = await build_navigation_buttons(
        page,
        total_pages,
        parent_id,
        is_inline,
    )
    if navigation_buttons:
        keyboard.append(navigation_buttons)
    if parent_id is not None:
        back_button = InlineKeyboardButton(
            constants.BACK_TEXT,
            callback_data=f"{constants.BACK_CALLBACK_PREFIX}"
                          f"{parent_id}") if is_inline else KeyboardButton(
            constants.BACK_TEXT)
        keyboard.append([back_button])

    if is_inline:
        return InlineKeyboardMarkup(keyboard)
    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for row in keyboard:
        reply_markup.row(*row)
    return reply_markup


async def build_reply_keyboard(
        menu_items: List[MenuItem],
        user_roles: List[str],
        parent_id: Optional[int] = None,
        page: int = constants.PAGE,
        items_per_page: int = constants.ITEMS_PER_PAGE,
        buttons_per_row: int = constants.BUTTONS_PER_ROW,
) -> ReplyKeyboardMarkup:
    """Создает ReplyKeyboardMarkup с поддержкой иерархии и пагинации.

    :param menu_items: Список всех элементов меню.
    :param user_roles: Список ролей пользователя.
    :param parent_id: Идентификатор родительского меню (None для корневого).
    :param page: Текущая страница.
    :param items_per_page: Максимальное количество кнопок на странице.
    :param buttons_per_row: Количество кнопок в одной строке.
    """
    return await build_keyboard(menu_items, user_roles, parent_id, page,
                          items_per_page, buttons_per_row, is_inline=False)


async def build_inline_keyboard(
        menu_items: List[MenuItem],
        user_roles: List[str],
        parent_id: Optional[int] = None,
        page: int = constants.PAGE,
        items_per_page: int = constants.ITEMS_PER_PAGE,
        buttons_per_row: int = constants.BUTTONS_PER_ROW,
) -> InlineKeyboardMarkup:
    """Создает InlineKeyboardMarkup с поддержкой иерархии и пагинации.

    :param menu_items: Список всех элементов меню.
    :param user_roles: Список ролей пользователя.
    :param parent_id: Идентификатор родительского меню (None для корневого).
    :param page: Текущая страница.
    :param items_per_page: Максимальное количество кнопок на странице.
    :param buttons_per_row: Количество кнопок в одной строке.
    """
    return await build_keyboard(menu_items, user_roles, parent_id, page,
                          items_per_page, buttons_per_row, is_inline=True)
