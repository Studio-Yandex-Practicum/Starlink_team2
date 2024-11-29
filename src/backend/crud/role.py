from backend.crud.base import CRUDBase
from backend.models import Role


class CRUDRole(CRUDBase):
    pass


role_crud = CRUDRole(Role)
