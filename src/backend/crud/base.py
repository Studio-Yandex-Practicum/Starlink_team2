from typing import Generic, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.db import Base

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Базовый CRUD."""

    def __init__(self, model: Type[ModelType]):
        """Инициализация класса с моделью."""
        self.model = model

    async def get(
        self, obj_id: int, session: AsyncSession,
    ) -> Optional[ModelType]:
        """Получение обьекта ио ID."""
        db_obj = await session.execute(
            select(self.model).where(self.model.unique_id == obj_id),
        )
        return db_obj.scalars().first()

    async def get_multi(
        self,
        session: AsyncSession,
    ) -> list[ModelType]:
        """Получение всех обьектов из модели."""
        db_objs = await session.execute(select(self.model))

        return db_objs.scalars().all()

    async def update(self, db_obj, obj_in, session: AsyncSession) -> ModelType:
        """Обновление обьекта в БД."""
        obj_data = jsonable_encoder(db_obj)
        update_obj = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_obj:
                setattr(db_obj, field, update_obj[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj: ModelType,
        session: AsyncSession,
    ) -> ModelType:
        """Удаление обьекта из БД."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj
