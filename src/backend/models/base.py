from datetime import datetime

from sqlalchemy import Column, DateTime

from backend.core.db import Base


class AbstractModelForTime(Base):
    """Абстрактная модель, в которой включено время создание и изменения.

    - created_at: Дата и время создания;
    - edited_at: Дата и время редактирования.
    """

    __abstract__ = True

    created_at = Column(DateTime, default=datetime.now)
    edited_at = Column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f'{self.created_at=}; {self.edited_at=}.'
