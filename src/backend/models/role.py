from uuid import uuid4

from sqlalchemy import CheckConstraint, Column, String
from sqlalchemy.dialects.postgresql import UUID as pg_UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Role(Base):
    '''Модель ролей.'''
    __tablename__ = "roles"

    unique_id = Column(pg_UUID(as_uuid=True), primary_key=True, default=uuid4)
    role_name = Column(String(length=256), unique=True, nullable=False,
                       check=CheckConstraint(
                           "length(role_name) BETWEEN 1 AND 256"))
