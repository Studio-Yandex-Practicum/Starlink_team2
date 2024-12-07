from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Menu, Role
from bot import constants


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
    ) -> List[Menu] | None:
        """Получает элементы меню для replyKeyboard."""
        async with session() as asession:
            result = await asession.execute(
                select(Menu).where(Menu.guest_access.is_(True))
            )
            result = result.scalars().all()

            role_id_menus = await asession.execute(
                select(Menu)
                .join(Role.menus)
                .filter(Role.unique_id == role_id, Menu.parent == parent_id),
            )
            role_id_menus = role_id_menus.scalars().all()

            result.extend(role_id_menus)
            result = sorted(result, key=lambda x: x.title)

            menu_list = []
            for elem in result:
                menu_list.append(
                    {
                        constants.UNIQUE_ID_KEY: elem.unique_id,
                        constants.NAME_KEY: elem.title,
                        constants.PARENT_KEY: elem.parent,
                        constants.IS_FOLDER_KEY: elem.is_folder,
                        constants.ROLES_KEY: role_id,
                    },
                )
            return menu_list

    async def get_content_by_menu_name(
        self,
        session: AsyncSession,
        menu_name: str,
    ) -> Menu | None:
        """Получение контента по имени меню."""
        async with session() as asession:
            content = await asession.execute(
                select(Menu).where(Menu.title == menu_name),
            )
            content = content.scalars().first()
        return content if content else None

    async def get_content_by_menu_id(
        self,
        session: AsyncSession,
        unique_id: UUID,
    ) -> Menu | None:
        """Получение контента по ID меню."""
        async with session() as asession:
            content = await asession.execute(
                select(Menu).where(Menu.unique_id == unique_id),
            )
            content = content.scalars().first()
        return content if content else None

    async def get_menu_child_by_parent_id(
        self,
        session: AsyncSession,
        parent_id: UUID,
    ) -> Menu | None:
        """Получение контента по ID меню."""
        async with session() as asession:
            content = await asession.execute(
                select(Menu).where(Menu.parent == parent_id),
            )
            content = content.scalars().first()
        return content if content else None


telegram_menu_crud = CRUDTelegramMenu(Menu)
