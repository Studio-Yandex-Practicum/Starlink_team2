from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType

from backend.core.config import settings
from backend.models.base import AbstractModelForTime


class EmployeeEmail(AbstractModelForTime):
    """Модель с почтовыми адресами сотрудников."""

    __tablename__ = 'employee_emails'

    email = Column(
        EmailType(length=settings.email_length),
        unique=True,
        nullable=False,
    )
    telegram_user = relationship('TelegramUser')

    def __repr__(self) -> str:
        return f'{self.email=}; {super().__repr__()}'
