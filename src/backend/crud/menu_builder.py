from typing import Optional

from sqlalchemy import func, select

from backend.core.db import get_async_session
from backend.models.menu import Menu
from backend.models.role import Role


async def count_rows() -> int:
    """Подсчет количества строк в таблице."""
    async with get_async_session() as session:
        count_rows = await session.execute(select(func.count(Menu.unique_id)))
        return count_rows.scalar()


async def menus_folders() -> Optional[list[Menu]]:
    """Получение списка папок меню."""
    async with get_async_session() as session:
        items = await session.execute(
            select(Menu).filter(Menu.is_folder.is_(True)),
        )
        if items:
            return items.scalars().all()
        return None


async def get_roles() -> Optional[list[Role]]:
    """Получение списка ролей."""
    async with get_async_session() as session:
        items = await session.execute(select(Role))
        if items:
            return items.scalars().all()
        return None
