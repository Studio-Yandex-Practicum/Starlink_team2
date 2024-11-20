from math import ceil
from typing import List, Optional, TypedDict

import telebot
from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


class MenuItem(TypedDict):
    """Определяет структуру данных для каждого элемента меню."""

    UniqueID: int
    Name: str
    Parent: Optional[int]
    Is_folder: bool
    Roles: List[str]


def build_reply_keyboard(
    menu_items: List[MenuItem],
    user_roles: List[str],
    parent_id: Optional[int] = None,
    page: int = 1,
    items_per_page: int = 10,
    buttons_per_row: int = 2,
) -> ReplyKeyboardMarkup:
    """Создает ReplyKeyboardMarkup с поддержкой иерархии и пагинации.

    :param menu_items: Список словарей с ключами 'UniqueID',
    'Name', 'Parent', 'Is_folder' и 'Roles'.
    :param user_roles: Список ролей пользователя.
    :param parent_id: Идентификатор родительского меню (None для корневого).
    :param page: Текущая страница.
    :param items_per_page: Максимальное количество кнопок на странице.
    :param buttons_per_row: Количество кнопок в одной строке.
    """
    accessible_items = [
        item for item in menu_items
        if item['Parent'] == parent_id and any(
            role in user_roles for role in item['Roles'])
    ]
    total_items = len(accessible_items)
    total_pages = ceil(total_items / items_per_page) if items_per_page else 1
    page = max(1, min(page, total_pages))
    start = (page - 1) * items_per_page
    end = start + items_per_page
    current_items = accessible_items[start:end]
    buttons = [KeyboardButton(item['Name']) for item in current_items]
    keyboard = [
        buttons[i:i + buttons_per_row] for i in
        range(0, len(buttons), buttons_per_row)
    ]
    nav_buttons = []
    if total_pages > 1:
        if page > 1:
            nav_buttons.append(KeyboardButton("« Назад"))
        if page < total_pages:
            nav_buttons.append(KeyboardButton("Вперед »"))
        if nav_buttons:
            keyboard.append(nav_buttons)
    if parent_id is not None:
        keyboard.append([KeyboardButton("⬅ Назад")])
    return ReplyKeyboardMarkup(resize_keyboard=True,
                               one_time_keyboard=False)


def build_inline_keyboard(
        menu_items: List[MenuItem],
        user_roles: List[str],
        parent_id: Optional[int] = None,
        page: int = 1,
        items_per_page: int = 10,
        buttons_per_row: int = 2,
        callback_prefix: str = 'menu_page_',
) -> InlineKeyboardMarkup:
    """Создает InlineKeyboardMarkup с поддержкой иерархии и пагинации.

    :param menu_items: Список словарей с ключами 'UniqueID',
    'Name', 'Parent', 'Is_folder' и 'Roles'.
    :param user_roles: Список ролей пользователя.
    :param parent_id: Идентификатор родительского меню (None для корневого).
    :param page: Текущая страница.
    :param items_per_page: Максимальное количество кнопок на странице.
    :param buttons_per_row: Количество кнопок в одной строке.
    :param callback_prefix: Префикс для callback_data навигационных кнопок.
    """
    accessible_items = [
        item for item in menu_items
        if item['Parent'] == parent_id and any(
            role in user_roles for role in item['Roles'])
    ]
    total_items = len(accessible_items)
    total_pages = ceil(total_items / items_per_page)
    page = max(1, min(page, total_pages)) if total_pages > 0 else 1
    start = (page - 1) * items_per_page
    end = start + items_per_page
    current_items = accessible_items[start:end]
    buttons = [
        InlineKeyboardButton(
            text=item['Name'],
            callback_data=f"select_{item['UniqueID']}" if not item[
                'Is_folder'] else f"open_{item['UniqueID']}",
        )
        for item in current_items
    ]
    keyboard = [buttons[i:i + buttons_per_row] for i in
                range(0, len(buttons), buttons_per_row)]
    nav_buttons = []
    if total_pages > 1:
        if page > 1:
            nav_buttons.append(
                InlineKeyboardButton(
                    "« Назад",
                    callback_data=f"{callback_prefix}{page - 1}_{parent_id}"))
        if page < total_pages:
            nav_buttons.append(
                InlineKeyboardButton(
                    "Вперед »",
                    callback_data=f"{callback_prefix}{page + 1}_{parent_id}"))
        if nav_buttons:
            keyboard.append(nav_buttons)
    if parent_id is not None:
        keyboard.append([InlineKeyboardButton(
            "⬅ Назад", callback_data=f"back_{parent_id}")])
    return telebot.types.InlineKeyboardMarkup(keyboard=keyboard)
