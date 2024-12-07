from typing import Optional
from uuid import uuid4

from pydantic import BaseModel


class MenuDB(BaseModel):
    """Схема модели."""

    title: str
    parent: Optional[str] = None
    content: Optional[str] = None
    is_folder: bool
    image_link: Optional[str] = None
    role_access: Optional[str] = None
    role: Optional[list] = []
    parent_menu: Optional[uuid4] = None
    guest_access: bool

    class Config:
        """Конфигурация модели."""

        from_attributes = True
