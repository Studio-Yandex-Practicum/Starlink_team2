from datetime import date

from sqlalchemy import (Boolean, CheckConstraint, Column, Date, ForeignKey,
                        String)
from sqlalchemy.dialects.postgresql import UUID as pg_UUID
from core.db import preBase


class TelegramUser(preBase):
    """Модель пользователей телеграма."""

    username = Column(String(length=256), unique=True, nullable=False)
    role_id = Column(pg_UUID(as_uuid=True), ForeignKey("roles.unique_id"),
                     nullable=True)
    name = Column(String(length=256))
    last_name = Column(String(length=256))
    email_id = Column(pg_UUID(as_uuid=True), ForeignKey("emails.unique_id"),
                      nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(Date, default=date.today)

    __table_args__ = (CheckConstraint(
        'email_id IS NULL OR email_id IN (SELECT unique_id FROM emails)',
        name='check_email_id'),)
