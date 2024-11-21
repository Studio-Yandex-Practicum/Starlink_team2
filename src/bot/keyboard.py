from math import ceil
from typing import List, Optional, Tuple, TypedDict, Union

from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from src.bot.constants import (
    BACK_CALLBACK_PREFIX,
    BACK_NAV_TEXT,
    BACK_TEXT,
    BUTTONS_PER_ROW,
    FORWARD_NAV_TEXT,
    IS_FOLDER_KEY,
    ITEMS_PER_PAGE,
    NAME_KEY,
    NAV_CALLBACK_PREFIX,
    NOOP,
    NO_ITEMS_TEXT,
    OPEN_CALLBACK_PREFIX,
    PAGE,
    PARENT_KEY,
    ROLES_KEY,
    SELECT_CALLBACK_PREFIX,
    UNIQUE_ID_KEY,
)


class MenuItem(TypedDict):
    """Определяет структуру данных для каждого элемента меню."""

    UniqueID: int
    Name: str
    Parent: Optional[int]
    Is_folder: bool
    Roles: List[str]


def filter_accessible_items(
        menu_items: List[MenuItem],
        user_roles: List[str],
        parent_id: Optional[int],
) -> List[MenuItem]:
    """Фильтрует список элементов меню по доступности
    для пользователя и по указанному родительскому идентификатору.

    :param menu_items: Список всех элементов меню.
    :param user_roles: Список ролей пользователя.
    :param parent_id: Идентификатор родительского элемента.
        Если `None`, фильтруются элементы верхнего уровня.
    :return: Список доступных элементов меню.
    """
    return [
        item for item in menu_items
        if item[PARENT_KEY] == parent_id
           and set(item[ROLES_KEY]).intersection(user_roles)
    ]


def paginate_items(
        items: List[MenuItem],
        page: int,
        items_per_page: int,
) -> Tuple[List[MenuItem], int]:
    """Разбивает список элементов на страницы и возвращает элементы
    текущей страницы вместе с общим количеством страниц.

    :param items: Полный список элементов для пагинации.
    :param page: Номер текущей страницы (начиная с 1).
    :param items_per_page: Количество элементов на одной странице.
    :return: Кортеж из списка элементов текущей страницы и
        общего количества страниц.
    """
    total_items = len(items)
    total_pages = max(1, ceil(total_items / items_per_page))
    current_page = max(1, min(page, total_pages))
    start = (current_page - 1) * items_per_page
    end = start + items_per_page
    return items[start:end], total_pages


def build_navigation_buttons(
        page: int,
        total_pages: int,
        parent_id: Optional[int] = None,
        is_inline: bool = False,
) -> list:
    """Создаёт кнопки навигации для клавиатуры (Reply или Inline)
    с учётом текущей страницы и общего количества страниц.

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
                        BACK_NAV_TEXT,
                        callback_data=f"{NAV_CALLBACK_PREFIX}"
                                      f"{page - 1}_{parent_id}",
                    ),
                )
            else:
                buttons.append(KeyboardButton(BACK_NAV_TEXT))
        if page < total_pages:
            if is_inline:
                buttons.append(
                    InlineKeyboardButton(
                        FORWARD_NAV_TEXT,
                        callback_data=f"{NAV_CALLBACK_PREFIX}"
                                      f"{page + 1}_{parent_id}",
                    ),
                )
            else:
                buttons.append(KeyboardButton(FORWARD_NAV_TEXT))
    return buttons


def build_menu_buttons(
        menu_items: List[MenuItem],
        user_roles: List[str],
        parent_id: Optional[int] = None,
        page: int = PAGE,
        items_per_page: int = ITEMS_PER_PAGE,
        buttons_per_row: int = BUTTONS_PER_ROW,
        is_inline: bool = False,
) -> list:
    """Создаёт список кнопок для меню с учётом
    пагинации и доступности элементов.

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
    accessible_items, total_pages = paginate_items(
        filter_accessible_items(menu_items, user_roles, parent_id),
        page, items_per_page,
    )
    if not accessible_items:
        button_constructor = InlineKeyboardButton if is_inline else (
            KeyboardButton)
        return [[button_constructor(NO_ITEMS_TEXT, callback_data=NOOP)]]

    def create_button(item):
        if is_inline:
            callback_data = (
                f"{OPEN_CALLBACK_PREFIX}{item[UNIQUE_ID_KEY]}"
                if item[IS_FOLDER_KEY]
                else f"{SELECT_CALLBACK_PREFIX}{item[UNIQUE_ID_KEY]}"
            )
            return InlineKeyboardButton(text=item[NAME_KEY],
                                        callback_data=callback_data)
        return KeyboardButton(item[NAME_KEY])

    buttons = [create_button(item) for item in accessible_items]
    return [buttons[i:i + buttons_per_row] for i in range(0, len(buttons),
                                                          buttons_per_row)]


def build_keyboard(
        menu_items: List[MenuItem],
        user_roles: List[str],
        parent_id: Optional[int] = None,
        page: int = PAGE,
        items_per_page: int = ITEMS_PER_PAGE,
        buttons_per_row: int = BUTTONS_PER_ROW,
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
    accessible_items, total_pages = paginate_items(
        filter_accessible_items(menu_items, user_roles, parent_id),
        page, items_per_page,
    )
    keyboard = build_menu_buttons(
        menu_items,
        user_roles,
        parent_id,
        page,
        items_per_page,
        buttons_per_row,
        is_inline,
    )
    navigation_buttons = build_navigation_buttons(
        page,
        total_pages,
        parent_id,
        is_inline,
    )
    if navigation_buttons:
        keyboard.append(navigation_buttons)
    if parent_id is not None:
        back_button = InlineKeyboardButton(
            BACK_TEXT,
            callback_data=f"{BACK_CALLBACK_PREFIX}"
                          f"{parent_id}") if is_inline else KeyboardButton(
            BACK_TEXT)
        keyboard.append([back_button])

    if is_inline:
        return InlineKeyboardMarkup(keyboard)
    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for row in keyboard:
        reply_markup.row(*row)
    return reply_markup


def build_reply_keyboard(
        menu_items: List[MenuItem],
        user_roles: List[str],
        parent_id: Optional[int] = None,
        page: int = PAGE,
        items_per_page: int = ITEMS_PER_PAGE,
        buttons_per_row: int = BUTTONS_PER_ROW,
) -> ReplyKeyboardMarkup:
    """Создает ReplyKeyboardMarkup с поддержкой иерархии и пагинации.

    :param menu_items: Список всех элементов меню.
    :param user_roles: Список ролей пользователя.
    :param parent_id: Идентификатор родительского меню (None для корневого).
    :param page: Текущая страница.
    :param items_per_page: Максимальное количество кнопок на странице.
    :param buttons_per_row: Количество кнопок в одной строке.
    """
    return build_keyboard(menu_items, user_roles, parent_id, page,
                          items_per_page, buttons_per_row, is_inline=False)


def build_inline_keyboard(
        menu_items: List[MenuItem],
        user_roles: List[str],
        parent_id: Optional[int] = None,
        page: int = PAGE,
        items_per_page: int = ITEMS_PER_PAGE,
        buttons_per_row: int = BUTTONS_PER_ROW,
) -> InlineKeyboardMarkup:
    """Создает InlineKeyboardMarkup с поддержкой иерархии и пагинации.

    :param menu_items: Список всех элементов меню.
    :param user_roles: Список ролей пользователя.
    :param parent_id: Идентификатор родительского меню (None для корневого).
    :param page: Текущая страница.
    :param items_per_page: Максимальное количество кнопок на странице.
    :param buttons_per_row: Количество кнопок в одной строке.
    """
    return build_keyboard(menu_items, user_roles, parent_id, page,
                          items_per_page, buttons_per_row, is_inline=True)
