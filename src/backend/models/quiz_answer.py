from sqlalchemy import Boolean, CheckConstraint, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as pg_UUID  # noqa
from sqlalchemy.orm import relationship

from .base import AbstractModelForTime
from backend.core.config import settings


class QuizAnswer(AbstractModelForTime):
    """Модель ответа на вопрос квиза.

    Модель содержит:
    - quiz_id: идентификатор квиза, к которому относится ответ;
    - question_id: идентификатор вопроса;
    - correct_answer: является ли ответ правильным;
    - active: доступность ответа для выбора;
    - content: текстовое описание ответа;
    - created_by: идентификатор пользователя, который создал опрос;
    - edited_by: идентификатор пользователя, который отредактировал опрос;
    - created_at: дата и время создания;
    - edited_at: дата и время редактирования.
    """

    __table_args__ = (
        CheckConstraint(
            f'length(content) BETWEEN '
            f'{settings.content_min_length} '
            f'AND {settings.content_max_length}',
        ),
    )

    quiz_id = Column(pg_UUID, ForeignKey('users.unique_id'))
    question_id = Column(pg_UUID, ForeignKey('quizquestions.unique_id'))
    correct_answer = Column(Boolean, default=False)
    active = Column(Boolean, default=False)
    content = Column(String(settings.content_max_length))
    created_by = relationship('User')
    edited_by = relationship('User')

    def __repr__(self) -> str:
        return (
            f'{self.quiz_id=}; {self.question_id=}; '
            f'{self.correct_answer=}; {self.active=}; '
            f'{self.content=}; {super().__repr__()}'
        )
