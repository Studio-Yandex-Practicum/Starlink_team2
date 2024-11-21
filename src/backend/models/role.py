from sqlalchemy import CheckConstraint, Column, String

from core.db import preBase
from core.config import settings


class Role(preBase):
    """Модель ролей."""

    role_name = Column(String(length=settings.role_name_max_length),
                       unique=True, nullable=False,
                       check=CheckConstraint(f"length(role_name) BETWEEN {
                           settings.role_name_min_length} AND {
                               settings.role_name_max_length}"))
