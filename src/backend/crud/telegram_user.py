from typing import Union
from uuid import uuid4

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.core.db import get_async_session
from backend.crud.base import CRUDBase, ModelType
from backend.models.telegram_user import TelegramUser
from backend.schemas.telegram_user import TelegramUserBase


class TelegramUserCRUD(
    CRUDBase[TelegramUser, TelegramUserBase, TelegramUserBase],
):
    """CRUD для работы с моделью TelegramUser."""

    async def get_multi(self) -> list[TelegramUser]:
        """Возвращает список всех TelegramUser."""
        async with get_async_session() as session:
            result = await session.execute(
                select(
                    TelegramUser,
                ).options(
                    selectinload(TelegramUser.role),
                    selectinload(TelegramUser.email),
                ),
            )
        return result.scalars().all()

    async def get(self, unique_id: int) -> Union[ModelType, None]:
        """Возвращает объект TelegramUser по unique_id."""
        async with get_async_session() as session:
            db_obj = await session.execute(
                select(self.model).where(
                    self.model.unique_id == unique_id,
                ).options(
                    selectinload(TelegramUser.role),
                    selectinload(TelegramUser.email),
                ),
            )
        return db_obj.scalars().first()

    async def get_tg_user_by_email_id(
        self,
        email_id: uuid4,
    ) -> TelegramUser:
        """Находит пользователя по email_id."""
        async with get_async_session() as session:
            email = await session.execute(
                select(self.model).where(self.model.email_id == email_id),  # noqa
            )
        return email.scalars().first()

    async def remove_role_id(
        self,
        db_obj: TelegramUser,
        data_obj: dict[str, None],
    ) -> TelegramUser:
        """Удаляет роль у пользователя."""
        obj_data = jsonable_encoder(db_obj)
        for field in obj_data:
            if field in data_obj:
                setattr(db_obj, field, data_obj[field])
        async with get_async_session() as session:
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
        return db_obj


telegramuser_crud = TelegramUserCRUD(TelegramUser)
