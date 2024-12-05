from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from backend.models import EmployeeEmail, Menu, Role
from bot.db import async_session


class CreateDataInDB:
    """Класс для заполнения базы данных."""

    def __init__(self, model: EmployeeEmail | Menu | Role) -> None:
        """Инициализация класса."""
        self.model = model

    async def fill_db_from_json(
        self,
        data: dict,
        session: async_sessionmaker[AsyncSession],
    ) -> EmployeeEmail | Menu | Role:
        """Заполнение базы данных."""
        async with session() as asession:
            new_data = self.model(**data)
            asession.add(new_data)
            await asession.commit()
            return new_data

    async def check_db_is_empty(
        self,
        session: async_sessionmaker[AsyncSession],
    ) -> list | None:
        """Проверка базы данных на наличие данных."""
        async with session() as asession:
            db_objs = await asession.execute(select(self.model))
            return db_objs.scalars().first() if db_objs else None


async def create_data_in_db(
    model: EmployeeEmail | Menu | Role,
    data: list[dict],
) -> str:
    """Заполнение базы данных."""
    create_crud = CreateDataInDB(model)
    check_db = await create_crud.check_db_is_empty(session=async_session)
    if check_db is not None:
        message_to_send = 'База данных уже БЫЛА заполнена'
    else:
        for item in data:
            await create_crud.fill_db_from_json(
                data=item,
                session=async_session,
            )
        message_to_send = 'База данных УСПЕШНО заполнена'
    return message_to_send


async def generate_menu(role_name: str) -> list[dict]:
    """Генерация меню."""
    async with async_session() as asession:
        role_access = await asession.execute(
            select(Role).where(Role.role_name == role_name),
        )
        role_access = role_access.scalars().first()
        role_access = role_access.unique_id
    count = 1
    menu_with_role = []
    while count < 30:
        menu_dict = {
            'name': f'Меню для {role_name} {count}',
            'content': f'Контент для {role_name} {count}',
            'role_access': role_access,
        }
        menu_with_role.append(menu_dict)
        count += 1
    return menu_with_role
