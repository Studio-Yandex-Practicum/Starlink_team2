from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from backend.core.db import get_async_session
from backend.crud.base import CRUDBase, ModelType
from backend.models.menu import Menu
from backend.models.role import Role


class CRUDMenuBuilder(CRUDBase):
    """CRUD для работы с моделью Menu."""

    async def count_rows(self) -> int:
        """Подсчет количества строк в таблице."""
        async with get_async_session() as session:
            count_rows = await session.execute(
                select(func.count(self.model.unique_id)),
            )
            return count_rows.scalar()

    async def menus_folders(self) -> Optional[list[Menu]]:
        """Получение списка папок меню."""
        async with get_async_session() as session:
            items = await session.execute(
                select(self.model).filter(self.model.is_folder.is_(True)),
            )
            if items:
                return items.scalars().all()
            return None

    async def get_roles(self) -> Optional[list[Role]]:
        """Получение списка ролей."""
        async with get_async_session() as session:
            items = await session.execute(select(Role))
            if items:
                return items.scalars().all()
            return None

    async def get_role(self, role_id: str) -> Role:
        """Получение роли по id."""
        async with get_async_session() as session:
            item = await session.execute(
                select(Role).filter(Role.unique_id == role_id),
            )
            if item:
                return item.scalar()
            return None

    async def create_item(self, item: Menu) -> Menu:
        """Создание нового пункта меню."""
        async with get_async_session() as session:
            item = self.model(**item)
            session.add(item)
            await session.commit()
            return item

    async def create_role(self, name: str) -> None:
        """Создание новой роли."""
        async with get_async_session() as session:
            role = Role(role_name=name)
            session.add(role)
            await session.commit()

    async def get_multi(self) -> list[Menu]:
        """Получение всех объектов из модели."""
        async with get_async_session() as session:
            db_objs = await session.execute(
                select(self.model).options(
                    selectinload(self.model.role),
                    selectinload(self.model.parent_menu),
                ),
            )
        return db_objs.scalars().all()

    async def get(
        self,
        obj_id: str,
    ) -> Optional[Menu]:
        """Получение объекта ио ID."""
        async with get_async_session() as session:
            db_obj = await session.execute(
                select(self.model)
                .where(
                    self.model.unique_id == obj_id,
                )
                .options(
                    selectinload(self.model.role),
                    selectinload(self.model.parent_menu),
                ),
            )  # noqa
        return db_obj.scalars().first()

    async def update(self, db_obj: ModelType, roles: list) -> ModelType:
        """Обновление объекта в БД."""
        async with get_async_session() as session:
            db_obj.role = []
            session.add(db_obj)
            await session.flush()
            db_obj.role = roles
            session.add(db_obj)
            await session.commit()
        return db_obj

    async def delete(self, obj_id: str) -> None:
        """Удаление объекта из БД."""
        async with get_async_session() as session:
            item: Menu = await self.get(obj_id)
            item.role = []
            session.add(item)
            await session.flush()
            await session.delete(item)
            await session.commit()


menu_builder_crud = CRUDMenuBuilder(Menu)
