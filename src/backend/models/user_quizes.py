from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID as pg_UUID  # noqa
from sqlalchemy.orm import relationship

from .base import AbstractModelForTime
from .quiz import Quiz
from .telegram_user import TelegramUser


class UserQuize(AbstractModelForTime):
    """Модель участника квиза.

    Модель содержит:
    - tg_user_id: Идентификатор телеграма пользователя;
    - quiz_id: Идентификатор квиза
    - status: Статус квиза для пользователя;
    - started_time: начало прохождения квиза;
    - finished_time: Когда пользователь закончил квиз;
    - created_at: Дата и время создания;
    - edited_at: Дата и время редактирования.
    """

    tg_user_id = Column(pg_UUID, ForeignKey('telegramusers.unique_id'))
    quize_id = Column(pg_UUID, ForeignKey('quizs.unique_id'), unique=True)
    status = Column(Boolean, default=True)
    started_at = Column(DateTime, default=datetime.now)
    finished_at = Column(DateTime, nullable=True)
    telegram_user = relationship(TelegramUser)
    quiz = relationship(Quiz)

    def __repr__(self) -> str:
        return (
            f'{self.tg_user_id=}; {self.quiz_id=}; '
            f'{self.status=}; {self.started_at=}; '
            f'{super().__repr__()}'
        )
