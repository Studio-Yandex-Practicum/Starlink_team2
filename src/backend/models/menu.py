from core.config import settings
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from .base import AbstractModelForTime


class Menu(AbstractModelForTime):
    """Модель меню телеграм бота."""

    __table_args__ = (CheckConstraint('parent >= 0'),
                      CheckConstraint('name != ""'))

    name = Column(String(settings.menu_name_length), unique=True)
    parent = Column(Integer)
    content = Column(Text)
    is_folder = Column(Boolean, default=False)
    image_link = Column(String(settings.menu_image_link_length))
    role_access = Column(Integer, ForeignKey('roles.unique_id'))
    role = relationship('Roles')

    def __repr__(self):
        return (f'{self.name=}; {self.parent=}; '
                f'{self.content}; {self.is_folder=}; '
                f'{self.image_link=}; {self.role_access=}'
                f'{super().__repr__()}'
                )
