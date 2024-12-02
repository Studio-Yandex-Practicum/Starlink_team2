from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_utils import EmailType

from . import telegramuser_crud
from backend.core.db import get_async_session
from backend.crud.base import CRUDBase
from backend.models.employee_email import EmployeeEmail
from backend.schemas.employee_email import EmployeeEmailBase


class EmployeeEmailCRUD(
    CRUDBase[EmployeeEmail, EmployeeEmailBase, EmployeeEmailBase],
):
    """CRUD для работы с моделью EmployeeEmail."""

    async def remove_multi(
            self,
            emails: list[EmployeeEmail],
            commit: bool = False,
    ) -> None | list[EmployeeEmail]:
        """Массовое удаление эмейлов из БД."""
        async with get_async_session() as session:
            for email_obj in emails:
                tg_user = await telegram_user_crud.get_tg_user_by_using_email_id(
                    session, email_obj.unique_id,
                )
                await session.delete(email_obj)

                if tg_user is None:
                    continue

                await telegram_user_crud.remove_role_id(
                    tg_user,
                    {'role_id': None},
                    session,
                )
            if commit:
                await session.commit()
                return emails

        return None

    async def get_email(self, employee_email: EmailType) -> EmployeeEmail:
        """Получение информации по эмейлу."""
        async with get_async_session() as session:
            email = await session.execute(
                select(self.model).where(self.model.title == employee_email),
            )
        return email.scalars().first()

    async def get_free_emails(self) -> list[EmployeeEmail]:
        """Получение всех свободных почт"""
        async with get_async_session() as session:
            return (await session.execute(
                select(self.model).where(self.model.users == None)
            )).scalars().all()


employee_email_crud = EmployeeEmailCRUD(EmployeeEmail)
