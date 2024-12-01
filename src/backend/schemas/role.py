from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, PositiveInt, Extra


class RoleDelete(BaseModel):
    unique_id: uuid4


class RoleBase(BaseModel):
    title: str

    class Config:
        extra = Extra.forbid


class RoleCreate(RoleBase):
    created_at: datetime = datetime.now()

    class Config:
        from_attributes = True


class RoleDB(RoleCreate):
    edited_at: datetime = None
