import os

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from rich.console import Console

from backend.core.auth import (
    get_current_user_from_cookie,
    login_for_access_token,
)
from backend.core.config import settings
from backend.pages.login_form import LoginForm

router = APIRouter()
console = Console()


base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, '..', 'templates')
templates = Jinja2Templates(directory=template_dir)


@router.get("/auth/login", response_class=HTMLResponse)
async def login_get(request: Request) -> HTMLResponse:
    """Обрабатывает запрос на страницу входа в систему (GET).

    Args:
        request: Объект запроса.

    Returns:
        HTML-ответом с контекстом страницы.

    """
    context = {
        "request": request,
    }
    try:
        user = await get_current_user_from_cookie(request)
    except Exception as _:
        user = None

    if user:
        return RedirectResponse(
            '/dashboard',
            status_code=status.HTTP_302_FOUND,
        )
    return templates.TemplateResponse("login.html", context)


@router.post("/auth/login", response_class=HTMLResponse)
async def login_post(
    request: Request,
) -> Response:
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
            return templates.TemplateResponse("/login.html", form.__dict__)
    return templates.TemplateResponse("/index.html", form.__dict__)


@router.get("/auth/logout", response_class=HTMLResponse)
async def logout_get() -> RedirectResponse:
    """Обрабатывает запрос на выход из системы.

    Args:
        request: Объект запроса.

    Returns:
        Переадресация на страницу входа.

    """
    response = RedirectResponse(url="/")
    response.delete_cookie(settings.COOKIE_NAME)
    return response
