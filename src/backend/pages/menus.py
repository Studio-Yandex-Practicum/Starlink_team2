from pathlib import Path
from typing import Optional

import aiofiles
from fastapi import (
    APIRouter,
    Depends,
    Form,
    Request,
    Response,
    UploadFile,
    status,
)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from backend.core.auth import get_current_user_from_token
from backend.crud import menu_builder_crud
from backend.models.admin import Admin

router = APIRouter()
BASE_DIR = Path(__file__).parent.parent
FOLDER_TEMPLATES = 'templates'
templates = Jinja2Templates(directory=BASE_DIR / FOLDER_TEMPLATES)


@router.get('/menu', response_class=HTMLResponse)
async def menu_view(
    request: Request,
    user: Admin = Depends(get_current_user_from_token),
) -> HTMLResponse:
    """Отображение страницы с сгенерированным меню."""
    count = await menu_builder_crud.count_rows()
    items = await menu_builder_crud.get_multi()
    context = {
        'request': request,
        'user': user,
        'count_rows': count,
        'items': items,
    }
    return templates.TemplateResponse('menus.html', context)


@router.get('/create', response_class=HTMLResponse)
async def menu_item_page(
    request: Request,
    user: Admin = Depends(get_current_user_from_token),
) -> HTMLResponse:
    """Отображение страницы с формой для создания меню."""
    get_folders_items = await menu_builder_crud.menus_folders()
    # await create_roles()
    roles = await menu_builder_crud.get_roles()
    context = {
        'request': request,
        'user': user,
        'folders': get_folders_items,
        'roles': roles,
    }
    return templates.TemplateResponse('create_menu_item.html', context)


@router.post('/create', response_class=HTMLResponse)
async def create_menu_item_page(
    request: Request,
    menu_image: UploadFile = Form(),
    item_name: str = Form(),
    parent: str = Form(),
    is_folder: Optional[bool] = Form(default=False),
    roles: Optional[list] = Form(default=[]),
    for_quest: Optional[bool] = Form(default=False),
    content: Optional[str] = Form(default=''),
    user: Admin = Depends(get_current_user_from_token),
) -> HTMLResponse:
    """Отображение страницы с формой для создания меню."""
    get_folders_items = await menu_builder_crud.menus_folders()
    roles_ = roles
    roles = await menu_builder_crud.get_roles()
    if parent == 'none':
        parent: Optional[str] = None
    else:
        parent = await menu_builder_crud.get(parent)
        parent = parent.unique_id
    item = {
        'title': item_name,
        'parent': parent,
        'content': content,
        'is_folder': is_folder,
        'image_link': menu_image.filename,
        'role': [await menu_builder_crud.get_role(role) for role in roles_],
        'guest_access': for_quest,
    }
    try:
        await menu_builder_crud.create_item(item)
    except Exception as e:
        print(f'error: {e}')
    if menu_image.filename:
        contents = await menu_image.read()
        async with aiofiles.open(
            f'{BASE_DIR}/static/images/{menu_image.filename}',
            'wb',
        ) as f:
            await f.write(contents)
    context = {
        'request': request,
        'user': user,
        'folders': get_folders_items,
        'roles': roles,
    }
    return templates.TemplateResponse('create_menu_item.html', context)


@router.get(
    '/edit/{unique_id}',
    response_class=HTMLResponse,
)
async def edit_menu_item_page(
    request: Request,
    unique_id: str,
    user: Admin = Depends(get_current_user_from_token),
) -> HTMLResponse:
    """Отображение страницы с формой для редактирования элемента меню."""
    item = await menu_builder_crud.get(unique_id)
    if not item:
        return templates.TemplateResponse(
            '404.html',
            context={'request': request},
        )
    folder_items = await menu_builder_crud.menus_folders()
    roles = await menu_builder_crud.get_roles()
    context = {
        'request': request,
        'user': user,
        'folders': folder_items,
        'roles': roles,
        'item': item,
        'selected_roles': [role.unique_id for role in item.role],
    }
    return templates.TemplateResponse('edit_menu_item.html', context)


@router.post('/edit', response_class=HTMLResponse)
async def edit_menu_item(
    request: Request,
    menu_image: UploadFile = Form(),
    item_name: str = Form(),
    parent: str = Form(),
    is_folder: Optional[bool] = Form(default=False),
    roles: Optional[list] = Form(default=[]),
    for_quest: Optional[bool] = Form(default=False),
    content: Optional[str] = Form(default=''),
    unique_id: str = Form(),
    user: Admin = Depends(get_current_user_from_token),
) -> Response:
    """Редактирование меню."""
    errors = []
    item = await menu_builder_crud.get(unique_id)
    if not item:
        return templates.TemplateResponse(
            '404.html',
            context={'request': request},
        )
    item.content = content

    # if menu_image.filename:
    #     data.image_link = menu_image.filename
    try:
        await menu_builder_crud.update(item)
    except Exception as e:
        errors.append(e)
    print(errors)
    if menu_image.filename:
        contents = await menu_image.read()
        async with aiofiles.open(
            f'{BASE_DIR}/static/images/{menu_image.filename}',
            'wb',
        ) as f:
            await f.write(contents)
    return RedirectResponse('/menu', status_code=status.HTTP_302_FOUND)
