import os
from typing import List, Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from rich.console import Console
from fastapi import APIRouter

from backend.models.admin import Admin
from backend.core.auth import get_current_user_from_cookie
from backend.core.auth import get_current_user_from_token
from backend.core.auth import login_for_access_token
from backend.core.config import settings
from backend.core.db import get_async_session
from backend.crud import role_crud, user_crud
from backend.schemas import RoleBase, RoleCreate, RoleDB, TelegramUserBase, TelegramUserCreate, TelegramUserDB


router = APIRouter()
console = Console()

base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, '..', 'templates')
templates = Jinja2Templates(directory=template_dir)


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Обрабатывает запрос на главную страницу.

    :param request: Объект запроса.
    :return: HTML-ответом с контекстом страницы.
    """
    try:
        user = await get_current_user_from_cookie(request)
    except:
        user = None
    context = {
        "user": user,
        "request": request,
    }
    return templates.TemplateResponse("login.html", context)


@router.get("/private", response_class=HTMLResponse)
async def private(
        request: Request,
        user: Admin = Depends(get_current_user_from_token)
):
    """
    Обрабатывает запрос на приватную страницу.

    :param request: Объект запроса.
    :param user: Текущий пользователь (извлекается из токена).
    :return: HTML-ответом с контекстом страницы.
        Возвращает 403 (Forbidden) если пользователь не авторизован.
    """
    context = {
        "user": user,
        "request": request
    }
    return templates.TemplateResponse("private.html", context)


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
        request: Request,
        user: Admin = Depends(get_current_user_from_token)
):
    """
    Обрабатывает запрос на страницу управления ботом.

    :param request: Объект запроса.
    :param user: Текущий пользователь (извлекается из токена).
    """
    context = {
        "user": user,
        "view_name": str(request.url).split('/')[-1],
        "request": request
    }
    return templates.TemplateResponse("dashboard.html", context)


@router.get(
    "/roles",
    response_class=HTMLResponse,
    response_model=list[RoleDB],
    response_model_exclude_none=True
)
async def roles_view(
        request: Request,
        session: AsyncSession = Depends(get_async_session),
        user: Admin = Depends(get_current_user_from_token)
):
    """
    Обрабатывает запрос на страницу Роли.

    :param request: Объект запроса.
    :param session: Объект текущей сессии.
    :param user: Текущий пользователь (извлекается из токена).
    """
    roles = await role_crud.get_multi(session)

    context = {
        "user": user,
        "request": request,
        "view_name": str(request.url).split('/')[-1],
        "roles": roles
    }
    return templates.TemplateResponse("roles.html", context)


@router.post(
    "/roles",
    response_class=HTMLResponse,
)
async def roles_create(
        request: Request,
        role_title=Form(),
        session: AsyncSession = Depends(get_async_session),
        user: Admin = Depends(get_current_user_from_token),
):
    """
    Обрабатывает запрос на страницу Роли.
    :param request: Объект запроса.
    :param role_title: Название Роли.
    :param session: Объект текущей сессии.
    :param user: Текущий пользователь (извлекается из токена).
    """
    errors = set()

    try:
        await role_crud.create({"role_title": role_title}, session)
    except IntegrityError:
        errors.add(f'Роль "{role_title}" уже есть в базе!')
        await session.rollback()
        await session.commit()

    roles = await role_crud.get_multi(session)

    context = {
        "user": user,
        "request": request,
        "view_name": str(request.url).split('/')[-1],
        "roles": roles,
        "errors": errors
    }
    return templates.TemplateResponse("roles.html", context)


@router.get(
    "/roles/{unique_id}",
    response_class=HTMLResponse,
    response_model=RoleCreate
)
async def role_view(
        request: Request,
        unique_id: str,
        session: AsyncSession = Depends(get_async_session),
        user: Admin = Depends(get_current_user_from_token)
):
    """
    Обрабатывает запрос на страницу Редактирование Роли.

    :param request: Объект запроса.
    :param unique_id: ID Роли
    :param session: Объект текущей сессии.
    :param user: Текущий пользователь (извлекается из токена).
     """

    role = await role_crud.get(unique_id, session)

    context = {
        "user": user,
        "request": request,
        "role": role,
    }
    return templates.TemplateResponse("role.html", context)


@router.post(
    "/roles/{unique_id}",
    response_class=RedirectResponse,
    response_model=RoleCreate
)
async def role_edit(
        unique_id: str,
        role_title=Form(),
        session: AsyncSession = Depends(get_async_session),
):
    """
    Обрабатывает запрос на страницу Редактирование Роли.

    :param unique_id: ID Роли
    :param role_title: Название Роли
    :param session: Объект текущей сессии.
     """

    role = await role_crud.get(unique_id, session)
    await role_crud.update(
        role,
        {'role_title': role_title},
        session
    )
    return RedirectResponse('/roles', status_code=302)


@router.post(
    "/roles/delete",
    response_class=RedirectResponse,
)
async def role_delete(
        unique_id: str = Form(),
        session: AsyncSession = Depends(get_async_session),
):
    """
    Обрабатывает запрос на страницу Редактирование Роли.

    :param unique_id: ID Роли
    :param session: Объект текущей сессии.
     """
    print("Roles DELETE")
    role = await role_crud.get(unique_id, session)
    await role_crud.remove(
        role,
        session
    )
    return RedirectResponse('/roles', status_code=302)


@router.get(
    "/users",
    response_class=HTMLResponse,
    response_model=list[TelegramUserDB],
    response_model_exclude_none=True
)
async def users_view(
        request: Request,
        session: AsyncSession = Depends(get_async_session),
        user: Admin = Depends(get_current_user_from_token)
):
    """
    Обрабатывает запрос на страницу Роли.

    :param request: Объект запроса.
    :param session: Объект текущей сессии.
    :param user: Текущий пользователь (извлекается из токена).
    """
    # all_roles = await user_crud.get_multi(session)

    context = {
        "user": user,
        "request": request,
        "view_name": str(request.url).split('/')[-1],
        # "users": all_users
    }
    return templates.TemplateResponse("users.html", context)


@router.get("/auth/login", response_class=HTMLResponse)
async def login_get(request: Request):
    """
    Обрабатывает запрос на страницу входа в систему (GET).

    :param request: Объект запроса.
    :return: HTML-ответом с контекстом страницы.
    """
    context = {
        "request": request,
    }
    return templates.TemplateResponse("login.html", context)


class LoginForm:
    """
    Класс для обработки формы входа в систему.
    """

    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get("username")
        self.password = form.get("password")

    async def is_valid(self):
        if not self.username or not (self.username.__contains__("@")):
            self.errors.append("Email is required")
        if not self.password or not len(self.password) >= 4:
            self.errors.append("A valid password is required")
        if not self.errors:
            return True
        return False


@router.post("/auth/login", response_class=HTMLResponse)
async def login_post(request: Request):
    """
    Обрабатывает запрос на вход в систему (POST).

    :param request: Объект запроса.
    :return: HTML-ответом с контекстом страницы входа,
        или RedirectResponse на dashboard.
    """
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            response = RedirectResponse("/dashboard", status.HTTP_302_FOUND)
            await login_for_access_token(response=response, form_data=form)
            form.__dict__.update(msg="Login Successful!")
            console.log("[green]Login successful!!!!")
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse("login.html", form.__dict__)
    return templates.TemplateResponse("login.html", form.__dict__)


@router.get("/auth/logout", response_class=HTMLResponse)
async def login_get():
    """
    Обрабатывает запрос на выход из системы.

    :param request: Объект запроса.
    :return: Переадресация на страницу входа.
    """
    response = RedirectResponse(url="/auth/login")
    response.delete_cookie(settings.COOKIE_NAME)
    return response
