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
