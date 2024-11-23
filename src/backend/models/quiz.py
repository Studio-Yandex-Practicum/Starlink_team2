from sqlalchemy import Boolean, Column, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as pg_UUID  # noqa
from sqlalchemy.orm import relationship

from core.config import settings
from models.base import AbstractModelForTime


class Quiz(AbstractModelForTime):
    """Модель квиза."""

    name = Column(String(settings.quiz_name_length), unique=True)
    description = Column(Text, nullable=True)
    active = Column(Boolean, default=False)
    edited_by = Column(pg_UUID, ForeignKey('users.unique_id'))
    created_by = Column(pg_UUID, ForeignKey('users.unique_id'))
    edited = relationship('Users')
    created = relationship('Users')

    def __repr__(self) -> str:
        return (
            f'{self.name=}; {self.description=}; {self.active=}; '
            f'{self.edited_by=}; {self.created=}; {super().__repr__()}'
        )
