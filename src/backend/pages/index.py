import os

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


from backend.core.auth import get_current_user_from_cookie

router = APIRouter()
base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, '..', 'templates')
templates = Jinja2Templates(directory=template_dir)


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
    return templates.TemplateResponse("/index.html", context)
