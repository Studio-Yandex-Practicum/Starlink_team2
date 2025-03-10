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

from backend.core.config import settings
from backend.models.base import AbstractModelForTime, Base
from backend.models.role import Role


class Menu(AbstractModelForTime):
    """Модель меню телеграм бота.

    - name: Название меню;
    - parent: UUID | null  родительского меню;
    - content: Наполнение кнопки;
    - is_folder: Является ли меню папкой;
    - image_link: Ссылка на картинку;
    - created_at: Дата и время создания;
    - edited_at: Дата и время редактирования;
    - created_at: Дата и время создания;
    - edited_at: Дата и время редактирования.
    """

    __table_args__ = (CheckConstraint("title != ''", name='name_empty'),)

    title = Column(String(settings.menu_name_length), unique=True)
    parent = Column(
        pg_UUID(as_uuid=True),
        ForeignKey('menus.unique_id'),
        nullable=True,
    )
    content = Column(Text)
    is_folder = Column(Boolean, default=False)
    image_link = Column(String(settings.image_link_max_length), nullable=True)
    role = relationship(Role, secondary='menu_role', back_populates='menus')
    parent_menu = relationship(
        'Menu',
        remote_side='Menu.unique_id',
    )
    guest_access = Column(Boolean, default=False)

    def __repr__(self) -> str:
        return (
            f'{self.title=}; {self.parent=}; '
            f'{self.content[:30]=}; {self.is_folder=}; '
            f'{self.image_link=}; {self.guest_access=}; '
            f'{super().__repr__()}'
        )


class MenuRole(Base):
    """Модель для связи меню и ролей."""

    __tablename__ = 'menu_role'

    menu_id = Column(
        pg_UUID(as_uuid=True),
        ForeignKey('menus.unique_id'),
    )
    role_id = Column(
        pg_UUID(as_uuid=True),
        ForeignKey(
            'roles.unique_id',
        ),
    )
