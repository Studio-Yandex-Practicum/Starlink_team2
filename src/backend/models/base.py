from datetime import datetime

from sqlalchemy import Column, DateTime

from core.db import Base


class AbstractModelForTime(Base):
    """Абстрактная модель, в которой включено время создание и изменения."""

    __abstract__ = True

    created_at = Column(DateTime, default=datetime.now)
    edited_at = Column(DateTime)

    def __repr__(self) -> str:
        return f'{self.created_at=}; {self.edited_at=}.'
