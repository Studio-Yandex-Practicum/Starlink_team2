from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.core.auth import get_current_user_from_token
from backend.crud.menu_builder import count_rows, get_roles, menus_folders, create_roles
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
async def menu_item_page(
    request: Request,
    user: Admin = Depends(get_current_user_from_token),
) -> HTMLResponse:
    """Отображение страницы с формой для создания меню."""
    get_folders_items = await menus_folders()
    # await create_roles()
    roles = await get_roles()
    context = {
        'request': request,
        'user': user,
        'folders': get_folders_items,
        'roles': roles,
    }
    return templates.TemplateResponse('create_menu_item.html', context)


@router.post('/munus/create', response_class=HTMLResponse)
async def create_menu_item_page(
    request: Request,
    user: Admin = Depends(get_current_user_from_token),
) -> HTMLResponse:
    """Отображение страницы с формой для создания меню."""
    get_folders_items = await menus_folders()
    # await create_roles()
    roles = await get_roles()
    form = await request.form()
    form.items()
    item_name = form.get('item_name')
    parent = form.get('parent')
    is_folder = form.get('is_folder')
    roles_ = form.getlist('roles')
    for_quest = form.get('for_quest')
    menu_image = form.get('menu_image')
    print(item_name, parent, is_folder, roles_, for_quest, menu_image)
    contents = await menu_image.read()
    with open(menu_image.filename, 'wb') as f:
        f.write(contents)
    context = {
        'request': request,
        'user': user,
        'folders': get_folders_items,
        'roles': roles,
    }
    return templates.TemplateResponse('create_menu_item.html', context)