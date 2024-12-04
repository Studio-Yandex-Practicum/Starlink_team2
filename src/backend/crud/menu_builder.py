from typing import Optional

from sqlalchemy import func, select

from backend.core.db import get_async_session
from backend.crud.base import CRUDBase
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


menu_builder_crud = CRUDMenuBuilder(Menu)
