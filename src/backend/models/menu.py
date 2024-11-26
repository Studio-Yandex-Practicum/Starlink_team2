from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID as pg_UUID  # noqa
from sqlalchemy.orm import relationship

from .base import AbstractModelForTime
from core.config import settings


class Menu(AbstractModelForTime):
    """Модель меню телеграм бота."""

    __table_args__ = (
        # CheckConstraint('parent >= 0'),
        CheckConstraint("name != ''"),
    )

    name = Column(String(settings.menu_name_length), unique=True)
    parent = Column(Integer, unique=True)
    content = Column(Text)
    is_folder = Column(Boolean, default=False)
    image_link = Column(String(settings.image_link_max_length), nullable=True)
    role_access = Column(pg_UUID, ForeignKey('roles.unique_id'))
    role = relationship('Role')

    def __repr__(self) -> str:
        return (
            f'{self.name=}; {self.parent=}; '
            f'{self.content=}; {self.is_folder=}; '
            f'{self.image_link=}; {self.role_access=}'
            f'{super().__repr__()}'
        )
