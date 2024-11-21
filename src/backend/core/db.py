from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID as pg_UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from core.config import settings


class preBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    unique_id = Column(pg_UUID(as_uuid=True), primary_key=True, default=uuid4)


Base = declarative_base(cls=preBase)
engine = create_async_engine(
    f'postgresql+asyncpg://{settings.postgres_user}:'
    f'{settings.postgres_password}@{settings.postgres_host}/'
    f'{settings.postgres_db_name}',
)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session
