from sqlalchemy import Boolean, Column, String, Text

from core.config import settings
from models.base import AbstractModelForTime


class Quiz(AbstractModelForTime):
    """Модель квиза."""

    name = Column(String(settings.quiz_name_length), unique=True)
    description = Column(Text, nullable=True)
    active = Column(Boolean, default=False)

    #  Раскомментировать когда будет добавлена модель Users
    # edited_by = Column(Integer, ForeignKey('users.unique_id'))
    # created_by = Column(Integer, ForeignKey('users.unique_id'))
    # edited = relationship('Users')
    # created = relationship('Users')

    def __repr__(self) -> str:
        return f'{self.name=}; {self.description=}; {self.active=}; '

        # Раскомментировать когда будет добавлена модель Users
        #       f'{self.edited_by=}; {self.created=}; {super().__repr__()}')
