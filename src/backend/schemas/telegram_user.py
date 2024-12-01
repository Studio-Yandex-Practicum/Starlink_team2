from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, PositiveInt, Extra

from backend.core.config import settings


class TelegramUserBase(BaseModel):
    username: str = Field(...)
    role_id: Optional[UUID] = None
    first_name: str = Field(None)
    last_name: str = Field(None)
    email_id: Optional[UUID] = None
    is_active: bool = True
    telegram_id: int = Field(...)

    class Config:
        str_max_length = settings.username_max_length
        extra = Extra.forbid


class TelegramUserCreate(TelegramUserBase):
    created_at: datetime = datetime.now()

    class Config:
        from_attributes = True


class TelegramUserDB(TelegramUserCreate):
    edited_at: datetime = None


class TelegramUserEdit(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role_id: Optional[UUID] = None
    email_id: Optional[UUID] = None
