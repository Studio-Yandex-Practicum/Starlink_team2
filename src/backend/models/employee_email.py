from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType

from backend.core.config import settings
from backend.models.base import AbstractModelForTime


class EmployeeEmail(AbstractModelForTime):
    """Модель с почтовыми адресами сотрудников.

    - title: Электронная почта сотрудника;
    - created_at: Дата и время создания;
    - edited_at: Дата и время редактирования.
    """

    __tablename__ = 'employee_emails'

    title = Column(
        EmailType(length=settings.email_length),
        unique=True,
    )
    users = relationship(
        "TelegramUser",
        back_populates="email",
        cascade="all, delete-orphan",
        single_parent=True,
    )

    def __repr__(self) -> str:
        return f'{self.title=}; {super().__repr__()}'
