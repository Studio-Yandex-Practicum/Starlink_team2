from sqlalchemy import Column
from sqlalchemy_utils import EmailType

from backend.core.config import settings
from backend.models.base import AbstractModelForTime


class EmployeeEmail(AbstractModelForTime):
    """Модель с почтовыми адресами сотрудников.

    - email: Электронная почта сотрудника;
    - created_at: Дата и время создания;
    - edited_at: Дата и время редактирования.
    """

    __tablename__ = 'employee_emails'

    email = Column(
        EmailType(length=settings.email_length),
        unique=True,
    )

    def __repr__(self) -> str:
        return f'{self.email=}; {super().__repr__()}'
