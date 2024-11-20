from sqlalchemy import CheckConstraint, Column, String
from core.db import preBase


class Role(preBase):
    """Модель ролей."""

    role_name = Column(String(length=256), unique=True, nullable=False,
                       check=CheckConstraint(
                           "length(role_name) BETWEEN 1 AND 256"))
