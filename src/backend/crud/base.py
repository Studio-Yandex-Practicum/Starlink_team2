from datetime import datetime
from typing import Generic, Optional, Type, TypeVar
from uuid import uuid4

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select

from backend.core.db import Base, get_async_session

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Базовый CRUD."""

    def __init__(self, model: Type[ModelType]) -> None:
        """Инициализация класса с моделью."""
        self.model = model

    async def get(
        self,
        obj_id: uuid4,
    ) -> Optional[ModelType]:
        """Получение объекта ио ID."""
        async with get_async_session() as session:
            db_obj = await session.execute(
                select(self.model).where(
                    self.model.unique_id == obj_id,
                ),  # noqa
            )
        return db_obj.scalars().first()

    async def create(
        self,
        obj_in_data: CreateSchemaType,
    ) -> list[ModelType]:
        """Создание нового объекта модели."""
        async with get_async_session() as session:
            db_obj = self.model(**obj_in_data.dict())
            db_obj.created_at = datetime.now()
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def get_multi(self) -> list[ModelType]:
        """Получение всех объектов из модели."""
        async with get_async_session() as session:
            db_objs = await session.execute(
                select(self.model).order_by(self.model.created_at),
            )
        return db_objs.scalars().all()

    async def update(
        self,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
    ) -> ModelType:
        """Обновление объекта в БД."""
        obj_data = jsonable_encoder(db_obj)
        update_obj = obj_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_obj:
                setattr(db_obj, field, update_obj[field])
        db_obj.edited_at = datetime.now()
        async with get_async_session() as session:
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def remove(self, db_obj: ModelType) -> ModelType:
        """Удаление объекта из БД."""
        async with get_async_session() as session:
            await session.delete(db_obj)
            await session.commit()
        return db_obj
