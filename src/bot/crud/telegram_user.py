from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.telegram_user import TelegramUser


class CRUDTelegramUsers:
    def __init__(self, model):
        self.model = model

    async def check_user_exists(
        self, telegram_id: int, session: AsyncSession
    ):
        user_check = (
            (
                await session.execute(
                    select(self.model).where(
                        self.model.telegram_id == telegram_id
                    )
                )
            )
            .scalars()
            .first()
        )
        return user_check


telegram_users_crud = CRUDTelegramUsers(TelegramUser)
