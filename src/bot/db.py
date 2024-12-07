from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from backend.core.config import settings

load_dotenv()

user = settings.postgres_user
password = settings.postgres_password
host = settings.postgres_host
port = settings.postgres_port
db_name = settings.postgres_db

url = f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}'

engine = create_async_engine(url)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
