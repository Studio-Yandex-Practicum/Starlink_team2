from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID as pg_UUID  # noqa
from sqlalchemy.orm import relationship

from .base import AbstractModelForTime


class UserQuize(AbstractModelForTime):
    """Модель участника квиза."""

    __table_args__ = (CheckConstraint('started_time < finished_time'),)

    user_id = Column(pg_UUID, ForeignKey('telegramusers.unique_id'))
    quize_id = Column(pg_UUID, ForeignKey('quizs.unique_id'))
    status = Column(Boolean, default=True)
    started_time = Column(DateTime, default=datetime.now)
    finished_time = Column(DateTime)
    telegram_user = relationship('TelegramUser')

    def __repr__(self) -> str:
        return (
            f'{self.user_id=}; {self.quize_id=}; '
            f'{self.status=}; {self.started_time=}; '
            f'{super().__repr__()}'
        )
