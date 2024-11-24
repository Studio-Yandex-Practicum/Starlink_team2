from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from backend.models.telegram_user import TelegramUser


class CRUDTelegramUsers:
    def __init__(self, model):
        self.model = model

    async def check_user_exists(
        self, telegram_id: int, session: async_sessionmaker[AsyncSession]
    ):
        async with session() as asession:
            user_check = (
                (
                    await asession.execute(
                        select(self.model).where(
                            self.model.telegram_id == str(telegram_id)
                        )
                    )
                )
                .scalars()
                .first()
            )
            return user_check


telegram_users_crud = CRUDTelegramUsers(TelegramUser)
