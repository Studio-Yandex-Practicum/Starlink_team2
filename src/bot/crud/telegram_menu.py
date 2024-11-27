from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.menu import Menu
from bot.constants import ROLE_ID_KANDIDAT


class CRUDTelegramMenu:
    """Класс для работы с telegram меню в БД."""

    def __init__(self, model: Menu) -> None:
        """Инициализация класса.

        Args:
            model (TelegramUser): модель меню

        """
        self.model = model

    async def get_child_menu_for_role(
            self,
            session: AsyncSession,
            parent_id: int,
            role_id: Optional[str] = None,
    ) -> List[Menu]:
        """Получает дочерние элементы меню для inlineKeyboard с учетом роли.

        Args:
            session (async_sessionmaker[AsyncSession]): сессия БД
            parent_id (int): Идентификатор родительского элемента меню.
            role_id (str): Идентификатор роли пользователя.

        Returns:
            Если None, то возвращаются элементы без учета роли.
            :return: Список дочерних элементов меню.

        """
        async with session() as asession:
            if role_id:
                result = await asession.execute(
                    select(Menu).where(Menu.parent == parent_id),
                )
            return result.scalars().all()

    async def get_child_menu_for_guest(
            self,
            session: AsyncSession,
            parent_id: int,
    ) -> List[Menu]:
        """Получает дочерние элементы меню для inlineKeyboard для гостей.

        Args:
            session (async_sessionmaker[AsyncSession]): сессия БД
            parent_id (int): Идентификатор родительского элемента меню.

        Returns:
            List: Список дочерних элементов меню для гостей.

        """
        async with session() as asession:
            result = await asession.execute(
                select(Menu).where(Menu.parent == parent_id,
                                   Menu.role_access.is_(None)),
            )
        return result.scalars().all()

    async def get_parent_menu_for_role(
            self,
            session: AsyncSession,
            role_id: Optional[str] = None,
    ) -> List[Menu]:
        """Получает родительские элементы меню для replyKeyboard с учетом роли.

        Args:
            session: (async_sessionmaker[AsyncSession]): сессия БД
            role_id (str): Идентификатор роли пользователя.
            Если None, то возвращаются элементы без учета роли.

        Returns:
            List: Список родительских элементов меню.

        """
        async with session() as asession:
            if role_id:
                result = await asession.execute(
                    select(Menu).where(
                        Menu.role_access == role_id),
                )
            else:
                result = await asession.execute(
                    select(Menu).where(Menu.parent.is_(None)),
                )
            return result.scalars().all()

    async def get_parent_menu_for_guest(
            self,
            session: AsyncSession,
    ) -> List[Menu]:
        """Получает родительские элементы меню для replyKeyboard для гостей.

        Args:
            session: (async_sessionmaker[AsyncSession]): сессия БД

        Returns:
            list: Список родительских элементов меню для гостей.

        """
        async with session() as asession:
            result = await asession.execute(
                select(Menu).where(Menu.role_access == ROLE_ID_KANDIDAT))
            res = []
            for elem in result:
                res.append(elem._mapping['Menu'])
            return res


telegram_menu_crud = CRUDTelegramMenu(Menu)
