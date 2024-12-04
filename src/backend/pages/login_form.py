from typing import List, Optional

from fastapi import Request


class LoginForm:
    """Класс для обработки формы входа в систему."""

    def __init__(self, request: Request) -> None:
        """Инициализация класса."""
        self.request: Request = request
        self.errors: List = []
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self) -> None:
        """Получение данных из формы входа."""
        form = await self.request.form()
        self.username = form.get("username")
        self.password = form.get("password")

    async def is_valid(self) -> bool:
        """Валидация параметров введенных в форму."""
        if not self.username or not (self.username.__contains__("@")):
            self.errors.append("Email is required")
        if not self.password or not len(self.password) >= 4:
            self.errors.append("A valid password is required")
        if not self.errors:
            return True
        return False
