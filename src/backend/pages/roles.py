from datetime import datetime

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.exc import IntegrityError

from backend.core.auth import get_current_user_from_token
from backend.core.config import templates
from backend.crud import role_crud
from backend.models.admin import Admin
from backend.schemas import RoleCreate, RoleDB, RoleDelete

router = APIRouter()


@router.get(
    "/",
    response_class=HTMLResponse,
    response_model_exclude_none=True,
)
async def roles_view(
        request: Request,
        user: Admin = Depends(get_current_user_from_token),
) -> templates.TemplateResponse:
    """Обрабатывает запрос на страницу Роли.

    :param request: Объект запроса.
    :param user: Текущий пользователь (извлекается из токена).
    """
    roles = await role_crud.get_multi()

    context = {
        "user": user,
        "request": request,
        "roles": roles,
    }
    return templates.TemplateResponse("roles.html", context)


@router.post(
    "/",
    response_class=HTMLResponse,
)
async def roles_create(
        request: Request,
        title: str = Form(),
        user: Admin = Depends(get_current_user_from_token),
) -> templates.TemplateResponse:
    """Обрабатывает запрос на страницу Роли.

    :param request: Объект запроса.
    :param title: Название Роли.
    :param user: Текущий пользователь (извлекается из токена).
    """
    errors = set()

    try:
        await role_crud.create(RoleCreate(title=title))
    except IntegrityError:
        errors.add(f'Роль "{title}" уже есть в базе!')

    roles = await role_crud.get_multi()

    context = {
        "user": user,
        "request": request,
        "roles": roles,
        "errors": errors,
    }
    return templates.TemplateResponse("roles.html", context)


@router.get(
    "/{unique_id}",
    response_class=HTMLResponse,
)
async def role_view(
        request: Request,
        unique_id: str,
        user: Admin = Depends(get_current_user_from_token),
) -> templates.TemplateResponse:
    """Обрабатывает запрос на страницу Редактирование Роли.

    :param request: Объект запроса.
    :param unique_id: ID Роли
    :param user: Текущий пользователь (извлекается из токена).
    """
    try:
        role = await role_crud.get(unique_id)
    except Exception:
        raise HTTPException(
            status_code=404,
            detail=f"Роль с ID {unique_id} не найдена.",
        )

    context = {
        "user": user,
        "request": request,
        "role": role,
    }
    return templates.TemplateResponse("role.html", context)


@router.post(
    "/{unique_id}",
    response_class=RedirectResponse,
    response_model=RoleDB,
)
async def role_edit(
        unique_id: str,
        title: str = Form(),
        user: Admin = Depends(get_current_user_from_token),
) -> RedirectResponse:
    """Обрабатывает запрос на страницу Редактирование Роли.

    :param unique_id: ID Роли
    :param title: Название Роли
    :param user: Текущий пользователь (извлекается из токена).
    """
    role = await role_crud.get(unique_id)
    await role_crud.update(
        role,
        RoleDB(
            title=title,
            edited_at=datetime.now(),
        ),
    )
    return RedirectResponse('/roles', status_code=301)


@router.post(
    "/delete/{unique_id}",
    response_class=RedirectResponse,
    response_model=RoleDelete,
)
async def role_delete(
        unique_id: str,
        user: Admin = Depends(get_current_user_from_token),
) -> RedirectResponse:
    """Обрабатывает запрос на страницу удаление Роли.

    :param unique_id: ID Роли
    :param user: Текущий пользователь (извлекается из токена).
    """
    role = await role_crud.get(unique_id)
    await role_crud.remove(role)
    return RedirectResponse('/roles', status_code=301)
