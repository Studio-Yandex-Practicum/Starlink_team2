from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.core.auth import get_current_user_from_token
from backend.crud.menu_builder import count_rows, get_roles, menus_folders
from backend.models.admin import Admin

router = APIRouter()
BASE_DIR = Path(__file__).parent.parent
FOLDER_TEMPLATES = 'templates'
templates = Jinja2Templates(directory=BASE_DIR / FOLDER_TEMPLATES)


@router.get('/menus', response_class=HTMLResponse)
async def get_menus(
    request: Request,
    user: Admin = Depends(get_current_user_from_token),
) -> HTMLResponse:
    """Отображение страницы с сгенерированным меню."""
    count = await count_rows()
    context = {'request': request, 'user': user, 'count_rows': count}
    return templates.TemplateResponse('menus.html', context)


@router.get('/munus/create', response_class=HTMLResponse)
async def create_menu_item_page(
    request: Request,
    user: Admin = Depends(get_current_user_from_token),
) -> HTMLResponse:
    """Отображение страницы с формой для создания меню."""
    get_folders_items = await menus_folders()
    roles = await get_roles()
    context = {
        'request': request,
        'user': user,
        'folders': get_folders_items,
        'roles': roles,
    }
    return templates.TemplateResponse('create_menu_item.html', context)
