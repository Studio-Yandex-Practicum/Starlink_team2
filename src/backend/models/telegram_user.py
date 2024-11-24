from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as pg_UUID  # noqa
from sqlalchemy.orm import relationship

from backend.core.config import settings
from backend.models.base import AbstractModelForTime


class TelegramUser(AbstractModelForTime):
    """Модель пользователей телеграма."""

    username = Column(
        String(length=settings.username_max_length),
        unique=True,
        nullable=False,
    )
    role_id = Column(
        pg_UUID(as_uuid=True),
        ForeignKey('roles.unique_id'),
        nullable=True,
    )
    name = Column(String(length=settings.username_max_length))
    last_name = Column(String(length=settings.username_max_length))
    email_id = Column(
        pg_UUID(as_uuid=True),
        ForeignKey("employee_emails.unique_id"),
        nullable=True,
    )
    active = Column(Boolean, default=True)
    user_quiz = relationship('Quiz')
    email = relationship('EmployeeEmail')

    def __repr__(self) -> str:
        return (
            f'{self.username=}; {self.role_id=}; '
            f'{self.name=}; {self.last_name=}; '
            f'{self.email_id=}; {self.active=}; '
            f'{super().__repr__()}'
        )
