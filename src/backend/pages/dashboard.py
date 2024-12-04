import os

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.core.auth import (
    get_current_user_from_cookie,
    get_current_user_from_token,
)
from backend.models.admin import Admin

router = APIRouter()

base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, '..', 'templates')
templates = Jinja2Templates(directory=template_dir)


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
    return templates.TemplateResponse('/dashboard.html', context)