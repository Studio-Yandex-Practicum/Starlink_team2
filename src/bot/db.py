from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from backend.core.config import settings

load_dotenv()

engine = create_async_engine(
    f'postgresql+asyncpg://{settings.postgres_user}:'
    f'{settings.postgres_password}@{settings.postgres_host}/'
    f'{settings.postgres_db}',
    echo=True,
)
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
