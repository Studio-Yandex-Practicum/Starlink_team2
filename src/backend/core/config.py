from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    app_title: str
    app_description: str
    app_version: str


settings = Settings()
