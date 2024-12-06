from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Menu, Role


class CRUDTelegramMenu:
    """Класс для работы с telegram меню в БД."""

    def __init__(self, model: Menu) -> None:
        """Инициализация класса."""
        self.model = model

    async def get_menu_for_role(
        self,
        session: AsyncSession,
        role_id: Optional[str] = None,
        parent_id: Optional[int] = None,
    ) -> List[Menu]:
        """Получает элементы меню для replyKeyboard."""
        async with session() as asession:
            result = await asession.execute(
                select(Menu).where(
                    Menu.parent == parent_id,
                    Menu.role_access == role_id,
                ),
            )
            result = result.scalars().all()
            menu_list = []
            for elem in result:
                menu_list.append(
                    {
                        'UniqueID': elem.unique_id,
                        'Name': elem.title,
                        'Parent': elem.parent,
                        'Is_folder': elem.is_folder,
                        'Roles': elem.role_access,
                    },
                )

                # res.append(menu_list.unique_id)
            return menu_list

    async def get_role_id_by_name(
        self,
        session: AsyncSession,
        role_name: str,
    ) -> list[dict] | None:
        """Получение id роли по имени."""
        async with session() as asession:
            role_access = await asession.execute(
                select(Role).where(Role.title == role_name),
            )
            role_access = role_access.scalars().first()
        return role_access.unique_id if role_access else None

    async def get_content_by_menu_name(
        self,
        session: AsyncSession,
        menu_name: str,
    ) -> str:
        """Получение контента по имени меню."""
        async with session() as asession:
            content = await asession.execute(
                select(Menu.content).where(Menu.title == menu_name),
            )
            content = content.scalars().first()
        return content if content else None


telegram_menu_crud = CRUDTelegramMenu(Menu)
