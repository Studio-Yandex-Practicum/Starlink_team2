from core.config import settings
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .base import AbstractModelForTime


class Quiz(AbstractModelForTime):
    """Модель квиза."""

    name = Column(String(settings.quiz_name_length), unique=True)
    description = Column(Text, nullable=True)
    active = Column(Boolean, default=False)
    edited_by = Column(Integer, ForeignKey('users.unique_id'))
    created_by = Column(Integer, ForeignKey('users.unique_id'))
    edited = relationship('Users')
    created = relationship('Users')

    def __repr__(self):
        return (f'{self.name=}; {self.description=}; {self.active=}; '
                f'{self.edited_by=}; {self.created=}; {super().__repr__()}')
