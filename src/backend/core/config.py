import os

from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from pydantic_settings import BaseSettings

load_dotenv()

base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, '..', 'templates')
templates = Jinja2Templates(directory=template_dir)


class Settings(BaseSettings):
    """Класс Settings представляет настройки приложения.

    Атрибуты:
    - app_title: заголовок приложения.
    - app_description: описание приложения.
    - app_version: версия приложения.
    - postgres_user: имя пользователя для подключения к базе данных PostgreSQL.
    - postgres_password: пароль пользователя для подключения к базе данных
    PostgreSQL.
    - postgres_host: хост для подключения к базе данных PostgreSQL.
    - postgres_db_name: имя базы данных PostgreSQL.
    - postgres_url: url для подключения к базе данных PostgreSQL.
    - email_length: максимальная длина адреса электронной почты.
    - role_name_min_length: минимальная длина названия роли.
    - role_name_max_length: максимальная длина названия роли.
    - username_max_length: максимальная длина имени пользователя.
    - quiz_name_length: максимальная длина названия опроса.
    - menu_name_length: максимальная длина названия меню.
    - menu_image_link_length: максимальная длина ссылки на изображение меню.
    """

    app_title: str
    app_description: str
    app_version: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str
    postgres_db: str
    email_length: int = 256
    role_name_min_length: int = 1
    role_name_max_length: int = 256
    username_max_length: int = 256

    quiz_name_length: int = 256
    menu_name_length: int = 256
    image_link_min_length: int = 10
    image_link_max_length: int = 256
    content_min_length: int = 10
    content_max_length: int = 256
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    COOKIE_NAME: str = "access_token"
    SECRET_KEY: str = "secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    NOT_AUTHENTICATED: str

    ROLES_PREFIX: str = '/roles'
    ROLES_TAGS: list = ['Роли', 'Roles']
    USERS_PREFIX: str = '/users'
    USERS_TAGS: list = ['Пользователи', 'Users']
    MENUS_PREFIX: str = '/menus'
    MENUS_TAGS: list = ['Построитель меню', 'Menus']

    @property
    def postgres_url(self):
        return (f'postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@'
                f'{self.postgres_host}:{self.postgres_port}/{self.postgres_db}')


settings = Settings()
