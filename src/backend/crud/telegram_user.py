from backend.crud.base import CRUDBase
from backend.models import TelegramUser


class CRUDTelegramUser(CRUDBase):
    pass


telegramuser_crud = CRUDTelegramUser(TelegramUser)
