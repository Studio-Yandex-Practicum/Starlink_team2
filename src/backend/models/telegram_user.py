from sqlalchemy import (
    Boolean,
    BigInteger,
    Column,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as pg_UUID  # noqa
from sqlalchemy.orm import relationship

from core.config import settings
from models.base import AbstractModelForTime


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
    role = relationship('Role')
    name = Column(String(length=settings.username_max_length))
    last_name = Column(String(length=settings.username_max_length))
    email_id = Column(
        pg_UUID(as_uuid=True),
        ForeignKey('employee_emails.unique_id'),
        nullable=True,
        unique=True,
    )
    active = Column(Boolean, default=True)
    email = relationship('EmployeeEmail')
    telegram_id: Column[int] = Column(BigInteger, unique=True, nullable=False)

    def __repr__(self) -> str:
        return (
            f'{self.username=}; {self.role_id=}; '
            f'{self.name=}; {self.last_name=}; '
            f'{self.email_id=}; {self.active=}; '
            f'{super().__repr__()}'
        )
