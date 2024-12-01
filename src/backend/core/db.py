from typing import AsyncGenerator
from uuid import uuid4

from dotenv import load_dotenv
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID as pg_UUID  # noqa
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker
from contextlib import asynccontextmanager

from backend.core.config import settings

load_dotenv()


class PreBase:
    """Класс PreBase является базовым классом для всех моделей в приложении.

    Атрибуты:
    - __tablename__: имя таблицы в базе данных, которое формируется из имени
    класса в нижнем регистре с добавлением 's'.
    - unique_id: уникальный идентификатор модели, который генерируется
    автоматически при создании экземпляра модели.

    Методы:
    - __tablename__: возвращает имя таблицы в базе данных.
    """

    @declared_attr
    def __tablename__(cls) -> str:
        return f'{cls.__name__.lower()}s'

    unique_id = Column(pg_UUID(as_uuid=True), primary_key=True, default=uuid4)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.postgres_url)


AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Предоставляет асинхронную сессию."""
    async with AsyncSessionLocal() as session:
        yield session
