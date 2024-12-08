from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_utils import EmailType

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
        session: AsyncSession,
        emails: list[EmployeeEmail],
        commit: bool = False,
    ) -> None | list[EmployeeEmail]:
        """Массовое удаление E-Mail из БД."""
        from backend.crud import telegramuser_crud

        for email_obj in emails:
            tg_user = await telegramuser_crud.get_tg_user_by_email_id(
                session,
                email_obj.unique_id,
            )
            await session.delete(email_obj)

            if tg_user is None:
                continue

            await telegramuser_crud.remove_role_id(
                session,
                tg_user,
                {'role_id': None},
                session,
            )
        if commit:
            await session.commit()
            return emails

        return None

    async def get_email(self, session, employee_email: str) -> EmployeeEmail:
        """Получение информации по E-Mail."""
        email = await session.execute(
            select(self.model).where(self.model.title == employee_email),
        )
        return email.scalars().first()

    async def get_free_emails(self) -> list[EmployeeEmail]:
        """Получение всех свободных E-Mail."""
        async with get_async_session() as session:
            return (
                (
                    await session.execute(
                        select(self.model).where(
                            self.model.users == None
                        ),  # noqa
                    )
                )
                .scalars()
                .all()
            )

    async def get_multi_emails(self, session) -> list[EmployeeEmail]:
        db_objs = await session.execute(
            select(self.model).order_by(self.model.created_at),
        )
        return db_objs.scalars().all()


employee_email_crud = EmployeeEmailCRUD(EmployeeEmail)
