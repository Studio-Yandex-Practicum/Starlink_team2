from datetime import datetime
from uuid import uuid4

from sqlalchemy import CheckConstraint, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID as pg_UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Email(Base):
    """Модель Email."""
    __tablename__ = "emails"

    unique_id = Column(pg_UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String(length=256), unique=True, nullable=False,
                   check=CheckConstraint("email LIKE '%@%'"))
    created_at = Column(DateTime, default=datetime.today)
