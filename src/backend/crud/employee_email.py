from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.crud.base import CRUDBase
from backend.crud.telegram_user import telegram_user_crud
from backend.models.employee_email import EmployeeEmail
from backend.schemas.employee_email import EmployeeEmailBase


class EmployeeEmailCRUD(
    CRUDBase[EmployeeEmail, EmployeeEmailBase, EmployeeEmailBase],
):
    """CRUD для работы с моделью EmployeeEmail."""

    async def remove_multi(
        self, session: AsyncSession, emails, commit: bool = False,
    ) -> None | list[EmployeeEmail]:
        """Массовое удаление эмейлов из БД."""
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

    async def get_email(self, session: AsyncSession, employee_email) -> EmployeeEmail:
        """Получение информации по эмейлу."""
        email = await session.execute(
            select(self.model).where(self.model.email == employee_email),
        )
        return email.scalars().first()


employee_email_crud = EmployeeEmailCRUD(EmployeeEmail)
