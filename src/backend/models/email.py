from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType

from core.config import settings
from models.base import AbstractModelForTime


class Email(AbstractModelForTime):
    """Модель Email."""

    email = Column(EmailType(length=settings.email_length), unique=True,
                   nullable=False)
    created_at = Column(DateTime, default=datetime.today)
    telegram_user = relationship('TelegramUser')
