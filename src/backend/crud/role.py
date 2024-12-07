from typing import Optional

from sqlalchemy import select

from backend.core.db import get_async_session
from backend.crud.base import CRUDBase
from backend.models import Role


class CRUDRole(CRUDBase):
    """CRUD для работы с моделью Role."""

    async def get_minimal_role(self) -> Optional[Role]:
        """Получить минимальную роль."""
        async with get_async_session() as session:
            item = await session.execute(
                select(self.model).filter(
                    self.model.default_minimal_role.is_(True),
                ),
            )
        return item.scalars().first()


role_crud = CRUDRole(Role)
