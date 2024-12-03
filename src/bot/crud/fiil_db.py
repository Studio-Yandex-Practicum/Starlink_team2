from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from backend.models.telegram_user import EmployeeEmail
from bot.db import async_session


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


data = {'email': 'kirkill2024@yandex.by'}


async def main():
    async with async_session() as session:
        await CreateDataInDB(EmployeeEmail).fill_db_from_json(data, session)
