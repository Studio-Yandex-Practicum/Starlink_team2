from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    app_title: str
    app_description: str
    app_version: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_db_name: str


settings = Settings()
