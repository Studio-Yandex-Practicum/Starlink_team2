
from fastapi import Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from rich.console import Console

from backend.core.auth import (
    get_current_user_from_cookie,
    get_current_user_from_token,
    login_for_access_token,
)
from backend.core.config import settings, templates
from backend.models.admin import Admin

from .forms import LoginForm
from .routers import main_router as router

console = Console()


@router.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    """Обрабатывает запрос на главную страницу.

    :param request: Объект запроса.
    :return: HTML-ответом с контекстом страницы.
    """
    try:
        user = await get_current_user_from_cookie(request)
    except Exception as _:
        user = None
    context = {
        "user": user,
        "request": request,
    }
    return templates.TemplateResponse("index.html", context)


@router.get("/private", response_class=HTMLResponse)
async def private(
    request: Request,
    user: Admin = Depends(get_current_user_from_token),
) -> HTMLResponse:
    """Обрабатывает запрос на приватную страницу.

    :param request: Объект запроса.
    :param user: Текущий пользователь (извлекается из токена).
    :return: HTML-ответом с контекстом страницы.
        Возвращает 403 (Forbidden) если пользователь не авторизован.
    """
    try:
        user = await get_current_user_from_cookie(request)
    except Exception as _:
        user = None
    context = {
        "user": user,
        "request": request,
    }
    return templates.TemplateResponse("private.html", context)


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    user: Admin = Depends(get_current_user_from_token),
) -> HTMLResponse:
    """Обрабатывает запрос на страницу управления ботом.

    Args:
        request: Объект запроса.
        user: Текущий пользователь (извлекается из токена).

    Returns:
        HTML-ответом с контекстом страницы.

    """
    try:
        user = await get_current_user_from_cookie(request)
    except Exception as _:
        user = None
    context = {
        'user': user,
        'request': request,
    }
    return templates.TemplateResponse('dashboard.html', context)


@router.get("/auth/login", response_class=HTMLResponse)
async def login_get(request: Request) -> HTMLResponse:
    """Обрабатывает запрос на страницу входа в систему (GET).

    Args:
        request: Объект запроса.

    Returns:
        HTML-ответом с контекстом страницы.

    """
    try:
        user = await get_current_user_from_cookie(request)
    except Exception as _:
        user = None
    context = {
        "request": request,
        "user": user,
    }
    return templates.TemplateResponse("index.html", context)


@router.post("/auth/login", response_class=HTMLResponse)
async def login_post(request: Request) -> Response:
    """Обрабатывает запрос на вход в систему (POST).

    Args:
        request: Объект запроса.

    Returns:
        HTML-ответ с контекстом страницы входа,
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
            try:
                user = await get_current_user_from_cookie(request)
            except Exception as _:
                user = None
            return templates.TemplateResponse(
                "index.html",
                context={
                    "request": request,
                    "user": user,
                    "form": form.__dict__,
                },
            )
    return templates.TemplateResponse("index.html", form.__dict__)


@router.get("/auth/logout", response_class=HTMLResponse)
async def login_get() -> RedirectResponse:
    """Обрабатывает запрос на выход из системы.

    Args:
        request: Объект запроса.

    Returns:
        Переадресация на страницу входа.

    """
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie(settings.COOKIE_NAME)
    return response
