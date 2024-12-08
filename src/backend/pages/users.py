from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from backend.core.auth import get_current_user_from_token
from backend.core.config import templates
from backend.crud import employee_email_crud, role_crud, telegramuser_crud
from backend.models import Admin
from backend.schemas import TelegramUserEdit

router = APIRouter()


@router.get(
    "/",
    response_class=HTMLResponse,
    response_model_exclude_none=True,
)
async def users_view(
    request: Request,
    user: Admin = Depends(get_current_user_from_token),
) -> templates.TemplateResponse:
    """Обрабатывает запрос на страницу Пользователи.

    :param request: Объект запроса.
    :param user: Текущий пользователь (извлекается из токена).
    """
    tgusers = await telegramuser_crud.get_multi()

    context = {
        "user": user,
        "request": request,
        "tgusers": tgusers,
    }
    return templates.TemplateResponse("users.html", context)


@router.get(
    "/{unique_id}",
    response_class=HTMLResponse,
)
async def user_view(
    request: Request,
    unique_id: str,
    user: Admin = Depends(get_current_user_from_token),
) -> templates.TemplateResponse:
    """Обрабатывает запрос на страницу Редактирование Пользователя.

    :param request: Объект запроса.
    :param unique_id: ID Роли
    :param user: Текущий пользователь (извлекается из токена).
    """
    try:
        tguser = await telegramuser_crud.get(unique_id)
    except Exception:
        raise HTTPException(
            status_code=404,
            detail=f"Пользователь с ID {unique_id} не найден.",
        )

    roles = await role_crud.get_multi()
    emails = await employee_email_crud.get_free_emails()

    context = {
        "user": user,
        "request": request,
        "tguser": tguser,
        "roles": roles,
        "emails": emails,
    }
    return templates.TemplateResponse("user.html", context)


@router.post(
    "/{unique_id}",
    response_class=RedirectResponse,
    response_model=TelegramUserEdit,
    response_model_exclude_none=True,
)
async def user_edit(
    unique_id: str,
    first_name: str = Form(None),
    last_name: str = Form(None),
    email_id: Optional[str] = Form(None),
    role_id: Optional[str] = Form(None),
    user: Admin = Depends(get_current_user_from_token),
) -> RedirectResponse:
    """Обрабатывает запрос на страницу Редактирование Пользователя.

    :param unique_id: ID Пользователя
    :param first_name: Имя Пользователя
    :param last_name: Фамилия Пользователя
    :param email_id: ID Электронной почты Пользователя
    :param role_id: ID Роли Пользователя
    :param user: Текущий пользователь (извлекается из токена).
    """
    if email_id == '':
        email_id = None
    if role_id == '':
        role_id = None
    await telegramuser_crud.update(
        await telegramuser_crud.get(unique_id),
        TelegramUserEdit(
            first_name=first_name,
            last_name=last_name,
            role_id=role_id,
            email_id=email_id,
        ),
    )

    return RedirectResponse('/users', status_code=302)


@router.post(
    "/delete/{unique_id}",
    response_class=RedirectResponse,
)
async def user_delete(
    unique_id: str,
    user: Admin = Depends(get_current_user_from_token),
) -> RedirectResponse:
    """Обрабатывает запрос на удаление Пользователя.

    :param unique_id: ID Пользователя.
    :param user: Текущий пользователь (извлекается из токена).
    :return: RedirectResponse.
    """
    tguser = await telegramuser_crud.get(unique_id)
    await telegramuser_crud.remove(tguser)
    return RedirectResponse('/users', status_code=302)
