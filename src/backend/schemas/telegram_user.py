from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, PositiveInt


class TelegramUserBase(BaseModel):
    """Базовая схема модели телеграм пользователя."""

    username: str
    role_id: uuid4
    email_id: uuid4
    name: Optional[str]
    last_name: Optional[str]
    active: bool
    telegram_id: PositiveInt
    created_at: datetime
    edited_at: Optional[datetime]
