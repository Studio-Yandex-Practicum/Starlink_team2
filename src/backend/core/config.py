from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


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
    - postgres_port: порт для подключения к базе данных PostgreSQL.
    - postgres_db: имя базы данных PostgreSQL.
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


settings = Settings()
