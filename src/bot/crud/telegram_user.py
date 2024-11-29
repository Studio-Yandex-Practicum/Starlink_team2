from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from backend.models.telegram_user import TelegramUser


class CRUDTelegramUsers:
    """Класс для работы с telegram пользователями в БД."""

    def __init__(self, model: TelegramUser) -> None:
        """Инициализация класса.

        Args:
            model (TelegramUser): модель пользователя

        """
        self.model = model

    async def check_user_exists(
        self, telegram_id: int, session: async_sessionmaker[AsyncSession],
    ) -> bool:
        """"Проверка существования пользователя в БД.

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
                            self.model.telegram_id == str(telegram_id),
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


telegram_users_crud = CRUDTelegramUsers(TelegramUser)
