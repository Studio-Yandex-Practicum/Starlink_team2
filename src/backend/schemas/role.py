from datetime import datetime

from pydantic import BaseModel, PositiveInt, Extra


class RoleBase(BaseModel):
    role_name: str

    class Config:
        extra = Extra.forbid


class RoleCreate(RoleBase):
    created_at: datetime = datetime.now()

    class Config:
        from_attributes = True


class RoleDB(RoleCreate):
    edited_at: datetime = None
