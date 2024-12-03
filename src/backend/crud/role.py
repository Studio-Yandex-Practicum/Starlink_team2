from backend.crud.base import CRUDBase
from backend.models import Role


class CRUDRole(CRUDBase):
    """CRUD для работы с моделью Role."""

    pass


role_crud = CRUDRole(Role)
