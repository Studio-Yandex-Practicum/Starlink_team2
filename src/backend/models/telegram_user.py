from sqlalchemy import Boolean, BigInteger, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as pg_UUID  # noqa
from sqlalchemy.orm import relationship

from backend.core.config import settings
from backend.models.base import AbstractModelForTime
from backend.models.quiz import Quiz
from backend.models.employee_email import EmployeeEmail
from backend.models.role import Role


class TelegramUser(AbstractModelForTime):
    """Модель пользователей телеграма."""

    username = Column(
        String(length=settings.username_max_length),
        unique=True,
        nullable=False,
    )
    role_id = Column(
        pg_UUID(as_uuid=True),
        ForeignKey(Role.unique_id),
        nullable=True,
    )
    name = Column(String(length=settings.username_max_length))
    last_name = Column(String(length=settings.username_max_length))
    email_id = Column(
        pg_UUID(as_uuid=True),
        ForeignKey(EmployeeEmail.unique_id),
        nullable=True,
    )
    active = Column(Boolean, default=True)
    # user_quiz = relationship(Quiz)
    # email = relationship('EmployeeEmail')
    telegram_id: Column[str] = Column(
        String,
        unique=True,
        nullable=False
    )

    def __repr__(self) -> str:
        return (
            f'{self.username=}; {self.role_id=}; '
            f'{self.name=}; {self.last_name=}; '
            f'{self.email_id=}; {self.active=}; '
            f'{super().__repr__()}'
        )
