from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.crud.base import CRUDBase
from backend.models.telegram_user import TelegramUser
from backend.schemas.telegram_user import TelegramUserBase


class TelegramUserCRUD(
    CRUDBase[TelegramUser, TelegramUserBase, TelegramUserBase],
):
    """CRUD для работы с моделью TelegramUser."""

    async def get_tg_user_by_using_email_id(
        self, session: AsyncSession, email_id,
    ) -> TelegramUser:
        """Находит пользователя по email_id."""
        email = await session.execute(
            select(self.model).where(self.model.email_id == email_id),
        )
        return email.scalars().first()

    async def remove_role_id(
        self, db_obj: TelegramUser, data_obj: dict[str:None], session: AsyncSession,
    ) -> TelegramUser:
        """Удаляет роль у пользователя."""
        obj_data = jsonable_encoder(db_obj)
        for field in obj_data:
            if field in data_obj:
                setattr(db_obj, field, data_obj[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


telegram_user_crud = TelegramUserCRUD(TelegramUser)
