from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel


class EmployeeEmailBase(BaseModel):
    """Базовая модель электронной почты пользователя."""
    title: str
    created_at: datetime = datetime.now()
    edited_at: Optional[datetime] = None
    unique_id: Optional[uuid4] = None
