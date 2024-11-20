from datetime import datetime

from sqlalchemy import Column, DateTime
from core.db import preBase
from sqlalchemy_utils import EmailType


class Email(preBase):
    """Модель Email."""

    email = Column(EmailType(length=256), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.today)
