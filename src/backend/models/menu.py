from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID as pg_UUID  # noqa
from sqlalchemy.orm import relationship

from .base import AbstractModelForTime
from .role import Role
from core.config import settings


class Menu(AbstractModelForTime):
    """Модель меню телеграм бота.

    - name: Название меню;
    - parent: UUID | null  родительсткого меню;
    - content: Наполнение кнопки;
    - is_folder: Является ли меню папкой;
    - image_link: Ссылка на картинку;
    - role_access: Роль для отоброжения меню;
    - created_at: Дата и время создания;
    - edited_at: Дата и время редактирования;
    - created_at: Дата и время создания;
    - edited_at: Дата и время редактирования.
    """

    __table_args__ = (CheckConstraint("name != ''"),)

    name = Column(String(settings.menu_name_length), unique=True)
    parent = Column(pg_UUID(as_uuid=True), default=None)
    content = Column(Text)
    is_folder = Column(Boolean, default=False)
    image_link = Column(String(settings.image_link_max_length), nullable=True)
    role_access = Column(pg_UUID, ForeignKey('roles.unique_id'))
    role = relationship(Role)

    def __repr__(self) -> str:
        return (
            f'{self.name=}; {self.parent=}; '
            f'{self.content[:30]=}; {self.is_folder=}; '
            f'{self.image_link=}; {self.role_access=}'
            f'{super().__repr__()}'
        )
