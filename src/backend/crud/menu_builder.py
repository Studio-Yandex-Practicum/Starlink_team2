from sqlalchemy import func, select

from backend.core.db import get_async_session
from backend.models.menu import Menu


async def count_rows() -> int:
    """Подсчет количества строк в таблице."""
    async with get_async_session() as session:
        count_rows = await session.execute(select(func.count(Menu.unique_id)))
        return count_rows.scalar()
