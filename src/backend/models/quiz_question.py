from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import UUID as pg_UUID  # noqa
from sqlalchemy.orm import relationship

from .base import AbstractModelForTime
from core.config import settings


class QuizQuestion(AbstractModelForTime):
    """Модель вопроса в квизе.

    Модель содержит:
    - quiz_id: идентификатор квиза, к которому относится вопрос;
    - image_link: ссылка на картинку вопроса;
    - number: номер вопроса;
    - content: текст вопроса;
    - active: состояние вопроса;
    - created_at: дата и время создания;
    - edited_at: дата и время редактирования.
    """

    __table_args__ = (
        CheckConstraint(
            f'length(image_link) BETWEEN '
            f'{settings.image_link_min_length} '
            f'AND {settings.image_link_max_length}',
        ),
        CheckConstraint('number >= 1'),
    )

    quiz_id = Column(pg_UUID, ForeignKey('quizs.unique_id'))
    image_link = Column(String(settings.image_link_max_length))
    content = Column(String(settings.content_max_length))
    number = Column(Integer)
    active = Column(Boolean, default=False)
    quiz = relationship('Quiz')

    def __repr__(self) -> str:
        return (
            f'{self.quiz_id=}; {self.image_link=}; '
            f'{self.content=}; {self.active=}; '
            f'{self.number=}; {super().__repr__()}; '
        )
