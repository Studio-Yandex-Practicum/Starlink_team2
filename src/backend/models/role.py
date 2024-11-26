from sqlalchemy import CheckConstraint, Column, String

from backend.core.config import settings
from backend.models.base import AbstractModelForTime


class Role(AbstractModelForTime):
    """Модель ролей сотрудников.

    - role_name: Название роли.
    - created_at: Дата и время создания;
    - edited_at: Дата и время редактирования.
    """

    __table_args__ = (
        CheckConstraint(
            f'length(role_name) BETWEEN '
            f'{settings.role_name_min_length} '
            f'AND {settings.role_name_max_length}',
        ),
    )

    role_name = Column(
        String(length=settings.role_name_max_length),
        unique=True,
        nullable=False,
    )

    def __repr__(self) -> str:
        return f'{self.role_name=}; {super().__repr__()}'
