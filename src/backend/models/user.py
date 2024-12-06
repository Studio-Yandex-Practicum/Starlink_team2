from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import CheckConstraint, Column, String
from sqlalchemy.dialects.postgresql import UUID as pg_UUID  # noqa

from backend.core.config import settings

from .base import AbstractModelForTime


class User(SQLAlchemyBaseUserTable[pg_UUID], AbstractModelForTime):
    """Модель администратора.

    Модель содержит:
    - username: псевдоним пользователя;
    - name: имя пользователя;
    - email: электронная почта пользователя;
    - hashed_password: зашифрованный пароль пользователя;
    - is_active: активный ли аккаунт пользователя;
    - is_superuser: является ли пользователем админом;
    - is_verified: подтвержден ли аккаунт;
    - last_name: фамилия пользователя;
    - created_at: дата и время создания;
    - edited_at: дата и время редактирования.
    """

    __tablename__ = "users"

    __table_args__ = (
        CheckConstraint(
            "first_name !=''",
        ),
        CheckConstraint(
            "last_name != ''",
        ),
    )

    first_name = Column(String(settings.username_max_length), nullable=True)
    last_name = Column(String(settings.username_max_length), nullable=True)

    def __repr__(self) -> str:
        return f'{self.first_name=}; {self.last_name=}; {super().__repr__()}'
