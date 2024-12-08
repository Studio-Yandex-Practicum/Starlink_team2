import re

# Константы для ключей MenuItem
UNIQUE_ID_KEY = 'UniqueID'
NAME_KEY = 'Name'
PARENT_KEY = 'Parent'
IS_FOLDER_KEY = 'Is_folder'
ROLES_KEY = 'Roles'

# Константы для навигации и callback_data
BACK_TEXT = '⬅ Назад'
BACK_NAV_TEXT = '« Назад'
FORWARD_NAV_TEXT = 'Вперед »'
BACK_CALLBACK_PREFIX = 'back_'
SELECT_CALLBACK_PREFIX = 'select_'
OPEN_CALLBACK_PREFIX = 'open_'
NAV_CALLBACK_PREFIX = 'menu-page_'
NOOP = 'noop'
NO_ITEMS_TEXT = 'Элементов нет'

# Константы для пагинации
ITEMS_PER_PAGE = 10
BUTTONS_PER_ROW = 2
PAGE = 1

# Константы для регистрации
REGISTER_BUTTON_TEXT = 'Зарегистрироваться'
NO_REGISTER_BUTTON_TEXT = 'Продолжить без регистрации'
REGISTER_TEXT = 'Пожалуйста, введите свою корпоративную электронную почту: '
REGISTERED = 'Вы уже зарегистрированы.'
EMAIL_ALREADY_REGISTERED = 'Этот email уже зарегистрирован.'
EMAIL_SUCCESS_REGISTERED = 'Вы успешно зарегистрировались.'
EMAIL_NOT_FOUND = 'Мы не смогли наити ваш email в базе данных.'
EMAIL_PATTERN = re.compile(
    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
)

# Константы для создания пользователя
USERNAME_KEY = 'username'
FIRST_NAME_KEY = 'first_name'
LAST_NAME_KEY = 'last_name'
TELEGRAM_ID_KEY = 'telegram_id'

# Константы стартовых сообщений
START_MESSAGE_NEW_USER = 'Вас нет в базе данных, создан новый пользователь: '
START_MESSAGE_EXIST_USER = 'Ура мы нашли вас в базе данных: '
START_MESSAGE_NO_EMAIL = (
    'Мы не нашли ваш email в базе данных. Пожалуйста, пройдите регистрацию.'
)
START_MESSAGE_NO_EMAIL_CONTINUE = 'Вы решили продолжить без регистрации.'
