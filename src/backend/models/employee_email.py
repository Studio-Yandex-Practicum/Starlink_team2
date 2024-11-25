from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType

from core.config import settings
from models.base import AbstractModelForTime


class EmployeeEmail(AbstractModelForTime):
    """Модель с почтовыми адресами сотрудников."""

    __tablename__ = 'employee_emails'

    email = Column(
        EmailType(length=settings.email_length),
        unique=True,
        nullable=False,
    )

    def __repr__(self) -> str:
        return f'{self.email=}; {super().__repr__()}'
