from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from backend.crud.base import CRUDBase, ModelType
from backend.models import TelegramUser


class TelegramUserCRUD(CRUDBase):
    async def get_multi(self, session: AsyncSession):
        query = select(TelegramUser).options(selectinload(TelegramUser.role), selectinload(TelegramUser.email))
        result = await session.execute(query)
        return result.scalars().all()

    async def get(
            self,
            obj_id: int,
            session: AsyncSession
    ) -> Union[ModelType, None]:
        db_obj = await session.execute(
            select(self.model).where(
                self.model.unique_id == obj_id
            ).options(selectinload(TelegramUser.role), selectinload(TelegramUser.email))
        )
        return db_obj.scalars().first()


telegramuser_crud = TelegramUserCRUD(TelegramUser)
