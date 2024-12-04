from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class CreateDataInDB:
    def __init__(self, model) -> None:
        self.model = model

    async def fill_db_from_json(
        self, data: dict, session: async_sessionmaker[AsyncSession]
    ):
        async with session() as asession:
            new_data = self.model(**data)
            asession.add(new_data)
            await asession.commit()
            return new_data

    async def check_db_is_empty(
        self, session: async_sessionmaker[AsyncSession]
    ):
        async with session() as asession:
            db_objs = await asession.execute(select(self.model))
            return db_objs.scalars().first() if db_objs else None
