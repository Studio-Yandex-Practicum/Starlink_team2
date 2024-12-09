import os

from datetime import date
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.crud import role_crud, telegramuser_crud
from backend.core.auth import (
    get_current_user_from_cookie,
    get_current_user_from_token,
)
from backend.models import Admin

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
    
    Функция получает информацию о пользователях Telegram,
        ролях и статистике регистрации
            для их последующего отображения на панели управления.

    Args:
        request (Request): Объект запроса от клиента.
        user (Admin, optional): Текущий пользователь, извлекаемый из токена.
            По умолчанию равен None.

    Returns:
        HTMLResponse: HTML-ответ с контекстом страницы,
            включающим информацию о пользователях,
                ролях и статистике регистрации.

    """
    try:
        user = await get_current_user_from_cookie(request)
    except Exception as _:
        user = None
    tgusers = await telegramuser_crud.get_multi()
    yesterday = datetime.now() - timedelta(days=1)
    tgusers_yesterday = [
        user for user in tgusers if user.created_at > yesterday
    ]
    today = date.today()
    tgusers_today = [
        user for user in tgusers if user.created_at.date() == today
    ]
    roles = await role_crud.get_multi()
    context = {
        "user": user,
        "request": request,
        "tgusers": tgusers,
        "roles": roles,
        "tgusers_yesterday": tgusers_yesterday,
        "tgusers_today": tgusers_today,

    }
    return templates.TemplateResponse('/dashboard.html', context)
