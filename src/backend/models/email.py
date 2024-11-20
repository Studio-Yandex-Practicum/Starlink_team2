from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy_utils import EmailType

from core.db import preBase
from core.config import EMAIL_LENGTH


class Email(preBase):
    """Модель Email."""

    email = Column(EmailType(length=EMAIL_LENGTH), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.today)
