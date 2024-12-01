from sqlalchemy import Column, String

from backend.core.db import Base


class Admin(Base):
    """Модель администратора web-приложения.

    Модель содержит:
    - username: псевдоним пользователя в виде электронной почты;
    - hashed_password: зашифрованный пароль пользователя;
    """

    __tablename__ = 'admins'
    username = Column(String, unique=True)
    hashed_password = Column(String)
