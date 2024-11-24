from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from dotenv import load_dotenv
from backend.core.config import settings

load_dotenv()

engine = create_async_engine(
    f'postgresql+asyncpg://{settings.postgres_user}:'
    f'{settings.postgres_password}@{settings.postgres_host}/'
    f'{settings.postgres_db_name}',
)
session = engine.connect()
