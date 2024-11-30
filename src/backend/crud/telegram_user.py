from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from backend.crud.base import CRUDBase
from backend.models import TelegramUser


class TelegramUserCRUD:
    async def get_multi(self, session: AsyncSession):
        query = select(TelegramUser).options(selectinload(TelegramUser.role), selectinload(TelegramUser.email))
        result = await session.execute(query)
        return result.scalars().all()


telegramuser_crud = TelegramUserCRUD()
