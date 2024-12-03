from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Extra


class RoleDelete(BaseModel):
    """Схема удаления Role."""

    unique_id: uuid4


class RoleBase(BaseModel):
    """Базовая схема Role."""

    title: str

    class Config:
        """Конфигурация базовой схемы Role."""

        extra = Extra.forbid


class RoleCreate(RoleBase):
    """Схема создания Role."""

    created_at: datetime = datetime.now()

    class Config:
        """Конфигурация схемы RoleCreate."""

        from_attributes = True


class RoleDB(RoleCreate):
    """Схема RoleDB."""

    edited_at: datetime = None
