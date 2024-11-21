from core.config import settings
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    ForeignKey,
    String,
)
from sqlalchemy.dialects.postgresql import UUID as pg_UUID
from sqlalchemy.orm import relationship

from .base import AbstractModelForTime


class TelegramUser(AbstractModelForTime):
    """Модель пользователей телеграма."""

    username = Column(String(length=settings.username_max_length), unique=True,
                      nullable=False)
    role_id = Column(pg_UUID(as_uuid=True), ForeignKey("roles.unique_id"),
                     nullable=True)
    name = Column(String(length=settings.username_max_length))
    last_name = Column(String(length=settings.username_max_length))
    email_id = Column(pg_UUID(as_uuid=True), ForeignKey("emails.unique_id"),
                      nullable=True)
    active = Column(Boolean, default=True)
    user_quiz = relationship('Quiz')
    email = relationship('Email')

    __table_args__ = (CheckConstraint(
        'email_id IS NULL OR email_id IN (SELECT unique_id FROM emails)',
        name='check_email_id'),)
