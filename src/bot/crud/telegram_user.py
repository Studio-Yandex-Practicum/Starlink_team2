from typing import Optional

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from backend.models import EmployeeEmail, Role, TelegramUser

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

    async def get_minimal_user_role(
        self,
        session: async_sessionmaker[AsyncSession],
    ) -> Optional[UUID]:
        """Получение минимальной роли для пользователя."""
        async with session() as asession:
            minimal_role = await asession.execute(
                select(Role).where(Role.default_minimal_role.is_(True)),
            )
            return minimal_role.scalars().first()

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

        return await telegram_menu_crud.get_menu_for_role(
            session=session,
            role_id=user_role_id,
            parent_id=parent_id,
        )

    async def get_email_id_from_db(
        self,
        session: async_sessionmaker[AsyncSession],
        email: str,
    ) -> str | None:
        """Получение email_id из БД."""
        async with session() as asession:
            email_id = await asession.execute(
                select(EmployeeEmail).where(EmployeeEmail.title == email),
            )
        return email_id.scalars().first() if email_id else None

    async def add_email_to_telegram_user(
        self,
        session: async_sessionmaker[AsyncSession],
        username: str,
        email_id: UUID,
    ) -> Optional[TelegramUser]:
        """Добавление email_id в telegram_user."""
        async with session() as asession:
            user = await asession.execute(
                select(TelegramUser).where(
                    TelegramUser.username == username,
                ),
            )
            check_email = await asession.execute(
                select(TelegramUser).where(
                    TelegramUser.email_id == email_id,
                ),
            )
            check_email = check_email.scalar_one_or_none()
            if check_email is not None:
                return None
            user = user.scalar_one_or_none()
            role_id = await telegram_users_crud.get_minimal_user_role(
                session=session,
            )
            if user is not None:
                user.email_id = email_id
                if role_id is not None:
                    user.role_id = role_id.unique_id
                asession.add(user)
                await asession.commit()
                return user
            return None


telegram_users_crud = CRUDTelegramUsers(TelegramUser)
