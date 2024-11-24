from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import CheckConstraint, Column, String
from sqlalchemy.dialects.postgresql import UUID as pg_UUID  # noqa
from sqlalchemy.orm import relationship

from .base import AbstractModelForTime
from backend.core.config import settings


class User(SQLAlchemyBaseUserTable[pg_UUID], AbstractModelForTime):
    """Модель администратора.

    Модель содержит:
    - username: псевдоним пользователя;
    - name: имя пользователя;
    - email: электронная почта пользователя;
    - hashed_password: зашифрованный пароль пользователя;
    - is_active: активный ли акаунт пользователя;
    - is_superuser: является ли пользователем админом;
    - is_verified: подтвержден ли акаунт;
    - last_name: фамилия пользователя;
    - created_at: дата и время создания;
    - edited_at: дата и время редактирования.
    """

    __tablename__ = 'users'

    __table_args__ = (
        CheckConstraint(
            "name !=''",
        ),
        CheckConstraint(
            "last_name != ''",
        ),
    )

    name = Column(String(settings.username_max_length), nullable=True)
    last_name = Column(String(settings.username_max_length), nullable=True)
    # editer_quiz = relationship('Quiz')
    # created_quiz = relationship('Quiz')
    # editer_quiz_answer = relationship('QuizAnswer.id')
    # created_quiz_answer = relationship('QuizAnswer.id')

    def __repr__(self) -> str:
        return f'{self.name=}; {self.last_name=}; {super().__repr__()}'
