# from telebot.types import (
#     InlineKeyboardButton,
#     InlineKeyboardMarkup,
#     KeyboardButton,
#     ReplyKeyboardMarkup,
# )

# start_menu_keyboard = ReplyKeyboardMarkup(
#     one_time_keyboard=True,
#     resize_keyboard=True,
# ).add(KeyboardButton('О компании'),
#                        KeyboardButton('Новости'),
#                        KeyboardButton('Пройти регистрацию'))



# start_menu_with_email = ReplyKeyboardMarkup(
#     one_time_keyboard=True,
#     resize_keyboard=True,
# ).add(KeyboardButton('О компании'),
#                        KeyboardButton('Новости'),
#                        KeyboardButton('Quiz'))


# async def handle_start_command(message, session: AsyncSession): 
#     """Обрабатывает команду /start."""
#     tg_id = message.from_user.id
#     username = message.from_user.username
#     first_name = message.from_user.first_name
#     last_name = message.from_user.last_name

#     user = await session.get(TelegramUser, tg_id) 

#     if not user:
#         # Новый пользователь
#         new_user = TelegramUser(
#             tg_id=tg_id,
#             username=username,
#             first_name=first_name,
#             last_name=last_name,
#             role_id=None #  Роль по умолчанию None (гость)
#         )
#         session.add(new_user)
#         await session.commit()
#         user_role = None #  Роль нового пользователя - None
#         menu_items = await get_parent_menu_for_guest(session)
#     else:
#         user_role = await check_user_role(session, username)
#         if user_role is not None and not await check_user_email(session, username):
#             #  Если роль не None (не гость), но email не подтвержден
#             await bot.send_message(tg_id, "Ваш email не подтвержден. Вам предоставлен гостевой доступ.")
#             user_role = None #  Устанавливаем роль None (гость)
#             menu_items = await get_parent_menu_for_guest(session)
#         elif user_role is None:
#             menu_items = await get_parent_menu_for_guest(session)
#         else:
#             menu_items = await get_parent_menu_for_role(session, user_role)


#     reply_markup = await build_reply_keyboard(menu_items, [user_role] if user_role else []) # Передаем список ролей
#     await bot.send_message(tg_id, "Привет! Вот ваше меню:", reply_markup=reply_markup)


# @bot.message_handler(commands=['start'])
# async def start(message):
#     async with AsyncSession(engine) as session: 
#         await handle_start_command(message, session)


# async def handle_start_command(message, session: AsyncSession):
#     tg_id = message.from_user.id
#     username = message.from_user.username
#     first_name = message.from_user.first_name
#     last_name = message.from_user.last_name

#     user = await session.get(TelegramUser, tg_id)

#     if not user:
#         # Новый пользователь
#         new_user = TelegramUser(
#             tg_id=tg_id,
#             username=username,
#             first_name=first_name,
#             last_name=last_name,
#             role_id=None
#         )
#         session.add(new_user)
#         await session.commit()
#         user_role = None
#         menu_items = await get_parent_menu_for_guest(session)
#         message_text = "Привет! Вот ваше меню (гостевой доступ):"

#     else:
#         user_role = await check_user_role(session, username)
#         if user_role is not None and not await check_user_email(session, username):
#             # Если роль не None, но email не подтвержден
#             await bot.send_message(tg_id, "Ваш email не подтвержден. Вам предоставлен гостевой доступ.")
#             user_role = None
#             menu_items = await get_parent_menu_for_guest(session)
#             message_text = "Привет! Вот ваше меню (гостевой доступ):"

#         elif user_role is None:
#             menu_items = await get_parent_menu_for_guest(session)
#             message_text = "Привет! Вот ваше меню (гостевой доступ):"

#         else:
#             menu_items = await get_parent_menu_for_role(session, user_role)
#             message_text = f"Привет! Вот ваше меню ({user_role}):"


#     reply_markup = await build_reply_keyboard(menu_items, [user_role] if user_role else [])
#     await bot.send_message(tg_id, message_text, reply_markup=reply_markup)