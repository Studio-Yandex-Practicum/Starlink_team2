from typing import Optional

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from backend.models import Role, TelegramUser

from .telegram_menu import telegram_menu_crud


class CRUDTelegramUsers:
    """Класс для работы с telegram пользователями в БД."""

    def __init__(self, model: TelegramUser) -> None:
        """Инициализация класса.

        Args:
            model (TelegramUser): модель пользователя

        """
        self.model = model

    async def check_user_exists(
        self,
        telegram_id: int,
        session: async_sessionmaker[AsyncSession],
    ) -> bool:
        """Проверка существования пользователя в БД.

        Args:
            telegram_id (int): telegram id пользователя
            session (async_sessionmaker[AsyncSession]): сессия БД

        Returns:
            bool: True - пользователь существует, False - пользователя нет

        """
        async with session() as asession:
            user_check = (
                (
                    await asession.execute(
                        select(self.model).where(
                            self.model.telegram_id == telegram_id,
                        ),
                    )
                )
                .scalars()
                .first()
            )
            return True if user_check else False

    async def check_user_email(
        self,
        session: async_sessionmaker[AsyncSession],
        username: str,
    ) -> bool:
        """Проверяет наличие email у пользователя.

        Args:
            username (str): Имя пользователя Telegram
            session (async_sessionmaker[AsyncSession]): сессия БД

        Returns:
            bool: True, если у пользователя есть email, иначе False.

        """
        async with session() as asession:
            chek_user_email_id = await asession.execute(
                select(TelegramUser).where(TelegramUser.username == username),
            )
        user = chek_user_email_id.scalar_one_or_none()
        return user.email_id is not None if user else False

    async def check_user_role(
        self,
        session: async_sessionmaker[AsyncSession],
        username: str,
    ) -> Optional[str]:
        """Проверяет роль пользователя.

        Args:
            username (str): Имя пользователя Telegram
            session (async_sessionmaker[AsyncSession]): сессия БД

        Returns:
            Идентификатор роли пользователя,
            если пользователь найден, иначе None.

        """
        async with session() as asession:
            chek_user_email_id = await asession.execute(
                select(TelegramUser).where(TelegramUser.username == username),
            )
        user = chek_user_email_id.scalar_one_or_none()
        return user.role_id is not None if user else False

    async def create_user(
        self,
        data: dict,
        session: async_sessionmaker[AsyncSession],
    ) -> TelegramUser:
        """Создание telegram пользователя в БД.

        Args:
            data: данные пользователя.
            session: сессия БД.

        Returns:
            new_user: созданный пользователь

        """
        async with session() as asession:
            new_user = self.model(**data)
            asession.add(new_user)
            await asession.commit()
            return new_user

    async def get_user_role(
        self,
        session: async_sessionmaker[AsyncSession],
        username: str,
    ) -> Optional[UUID]:
        """Получение роли пользователя."""
        async with session() as asession:
            user = await asession.execute(
                select(TelegramUser).where(TelegramUser.username == username),
            )
        user = user.scalar_one_or_none()
        return user.role_id

    async def get_menu_for_user_roles(
        self,
        session: async_sessionmaker[AsyncSession],
        username: str,
        parent_id: Optional[UUID] = None,
    ) -> list[dict] | None:
        """Функция для получения меню для пользователя."""
        user_role_id = await telegram_users_crud.get_user_role(
            session=session,
            username=username,
        )

        # тестовые роли для проверки работы бота - УДАЛИТЬ ПОСЛЕ ТЕСТИРОВАНИЯ
        # user_role_id = await self.get_role_id_by_name(
        #     session=session,
        #     role_name='Кандидат',
        # )
        # user_role_id = await self.get_role_id_by_name(
        #     session=session,
        #     role_name='Сотрудник',
        # )
        # тестовые роли для проверки работы бота - УДАЛИТЬ ПОСЛЕ ТЕСТИРОВАНИЯ

        # role_id_list = [user_role_id, test_role_id_1, test_role_id_2]
        role_id_list = [user_role_id]
        menu_items = []
        for role in role_id_list:
            menu_item = await telegram_menu_crud.get_menu_for_role(
                session=session,
                role_id=role,
                parent_id=parent_id,
            )
            menu_items.extend(menu_item)
        return menu_items

    # TO DELETE# TO DELETE# TO DELETE# TO DELETE# TO DELETE# TO DELETE
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


telegram_users_crud = CRUDTelegramUsers(TelegramUser)
