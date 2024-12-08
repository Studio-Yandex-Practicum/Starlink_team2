import os

from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from backend.core.auth import get_current_user_from_cookie

router = APIRouter()
base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, '..', 'templates')
templates = Jinja2Templates(directory=template_dir)


@router.get("/", response_class=HTMLResponse)
async def index(request: Request) -> RedirectResponse:
    """Обрабатывает запрос на главную страницу.

    :param request: Объект запроса.
    :return: HTML-ответом с контекстом страницы.
    """
    try:
        user = await get_current_user_from_cookie(request)
    except Exception as _:
        user = None

    if user is None:
        return RedirectResponse(
            '/auth/login',
            status_code=status.HTTP_302_FOUND,
        )
    return RedirectResponse("/dashboard", status_code=status.HTTP_302_FOUND)
