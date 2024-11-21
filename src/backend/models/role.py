from core.config import settings
from sqlalchemy import CheckConstraint, Column, String
from sqlalchemy.orm import relationship

from .base import AbstractModelForTime


class Roles(AbstractModelForTime):
    """Модель ролей."""

    __table_args__ = (CheckConstraint(
                            f"length(role_name) BETWEEN "
                            f"{settings.role_name_min_length} "
                            f"AND {settings.role_name_max_length}"),)

    role_name = Column(String(length=settings.role_name_max_length),
                       unique=True, nullable=False,
                     )
    menu = relationship('Menu')
