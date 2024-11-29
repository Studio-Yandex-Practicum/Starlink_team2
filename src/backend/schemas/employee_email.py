from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class EmployeeEmailBase(BaseModel):
    """Базовая модель электронной почты пользователя."""

    email: str
    created_at: datetime
    edited_at: Optional[datetime]
