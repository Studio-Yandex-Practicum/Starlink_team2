from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as pg_UUID  # noqa
from sqlalchemy.orm import relationship

from backend.core.config import settings
from backend.models.base import AbstractModelForTime
from backend.models.role import Role


class TelegramUser(AbstractModelForTime):
    """Модель пользователей телеграма.

    Модель содержит:
    - username: Псевдоним пользователя;
    - role_id: идентификатор роли;
    - name: Имя пользователя;
    - last_name: Фамилия пользователя;
    - email_id: идентификатор эмкейла пользователя;
    - active: Активный ли телеграм;
    - telegram_id: ID телеграма пользователя;
    - created_at: Дата и время создания;
    - edited_at: Дата и время редактирования.
    """

    username = Column(
        String(length=settings.username_max_length),
        unique=True,
    )
    role_id = Column(
        pg_UUID(as_uuid=True),
        ForeignKey('roles.unique_id', ondelete='SET NULL'),
        nullable=True,
    )
    first_name = Column(
        String(length=settings.username_max_length),
        nullable=True,
    )
    last_name = Column(
        String(length=settings.username_max_length),
        nullable=True,
    )
    email_id = Column(
        pg_UUID(as_uuid=True),
        ForeignKey('employee_emails.unique_id', ondelete='SET NULL'),
        nullable=True,
    )
    is_active = Column(Boolean, default=True)
    telegram_id: Column[int] = Column(
        BigInteger,
        unique=True,
    )
    email = relationship(
        "EmployeeEmail",
        back_populates="users",
    )
    role = relationship(Role)

    def __repr__(self) -> str:
        return (
            f'{self.username=}; {self.role_id=}; '
            f'{self.first_name=}; {self.last_name=}; '
            f'{self.email_id=}; {self.is_active=}; '
            f'{super().__repr__()}'
        )