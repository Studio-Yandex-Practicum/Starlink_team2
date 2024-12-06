from sqlalchemy import CheckConstraint, Column, String
from sqlalchemy.orm import relationship

from backend.core.config import settings
from backend.models.base import AbstractModelForTime

# from backend.models.menu import Menu


class Role(AbstractModelForTime):
    """Модель ролей сотрудников.

    - title: Название роли.
    - created_at: Дата и время создания;
    - edited_at: Дата и время редактирования.
    """

    __table_args__ = (
        CheckConstraint(
            f'length(title) BETWEEN '
            f'{settings.role_name_min_length} '
            f'AND {settings.role_name_max_length}',
        ),
    )

    title = Column(
        String(length=settings.role_name_max_length),
        unique=True,
    )
    menus = relationship(
        'Menu',
        back_populates='role',
        secondary='menu_role',
    )

    def __repr__(self) -> str:
        return f'{self.title=}; {super().__repr__()}'
