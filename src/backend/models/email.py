from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy_utils import EmailType

from core.db import preBase
from core.config import settings


class Email(preBase):
    """Модель Email."""

    email = Column(EmailType(length=settings.email_length), unique=True,
                   nullable=False)
    created_at = Column(DateTime, default=datetime.today)
