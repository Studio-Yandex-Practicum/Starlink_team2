from backend.crud.base import CRUDBase
from backend.models import User


class CRUDUser(CRUDBase):
    pass


user_crud = CRUDUser(User)
