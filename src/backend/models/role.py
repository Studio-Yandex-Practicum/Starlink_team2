from sqlalchemy import Column, String, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID as pg_UUID
from sqlalchemy.orm import declarative_base
from uuid import uuid4

Base = declarative_base()


class Role(Base):
    __tablename__ = "roles"

    unique_id = Column(pg_UUID(as_uuid=True), primary_key=True, default=uuid4)
    role_name = Column(String(length=256), unique=True, nullable=False,
                       check=CheckConstraint(
                           "length(role_name) BETWEEN 1 AND 256"))
