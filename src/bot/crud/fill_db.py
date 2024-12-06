from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
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


async def create_data_in_db_no_check(
    model: EmployeeEmail | Menu | Role,
    data: list[dict],
) -> str:
    """Заполнение базы данных без проверки."""
    create_crud = CreateDataInDB(model)
    for item in data:
        await create_crud.fill_db_from_json(
            data=item,
            session=async_session,
        )
    message_to_send = 'Создано inline меню'
    return message_to_send


async def generate_menu(role_name: str) -> list[dict]:
    """Генерация меню."""
    async with async_session() as asession:
        role_access = await asession.execute(
            select(Role).where(Role.title == role_name),
        )
        role_access = role_access.scalars().first()
        role_access = role_access.unique_id
    count = 1
    menu_with_role = []
    while count < 30:
        menu_dict = {
            'title': f'Меню для {role_name} {count}',
            'content': f'Контент для {role_name} {count}',
            'role_access': role_access,
        }
        menu_with_role.append(menu_dict)
        count += 1
    return menu_with_role


async def generate_parent_menu(role_name: str, parent_id: UUID) -> list[dict]:
    """Генерация меню."""
    async with async_session() as asession:
        role_access = await asession.execute(
            select(Role).where(Role.title == role_name),
        )
        role_access = role_access.scalars().first()
        role_access = role_access.unique_id
    count = 1
    async with async_session() as asession:
        parent_menu_name = await asession.execute(
            select(Menu.title).where(Menu.unique_id == parent_id),
        )
        parent_menu_name = parent_menu_name.scalars().first()
    menu_with_parent = []
    while count < 30:
        menu_dict = {
            'title': f'Inline {parent_menu_name} for {role_name} {count}',
            'content': f'Content {parent_menu_name} for {role_name} {count}',
            'role_access': role_access,
            'parent': parent_id,
        }
        # print(menu_dict)
        menu_with_parent.append(menu_dict)
        count += 1
    return menu_with_parent


async def get_all_menu_id() -> list[dict]:
    """Получение всех id ролей."""
    async with async_session() as asession:
        role_id = await asession.execute(select(Menu.unique_id))
        role_id = role_id.scalars().all()
    return role_id
