from datetime import datetime

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from backend.crud import employee_email_crud, role_crud, telegramuser_crud
from backend.core.auth import get_current_user_from_token
from backend.core.config import templates
from backend.core.db import AsyncSession, get_async_session
from backend.models import Admin, TelegramUser
from backend.schemas import EmployeeEmailBase, TelegramUserEdit


router = APIRouter()


@router.get(
    "/",
    response_class=HTMLResponse,
    # response_model=list[TelegramUserDB],
    response_model_exclude_none=True
)
async def users_view(
        request: Request,
        session: AsyncSession = Depends(get_async_session),
        user: Admin = Depends(get_current_user_from_token)
):
    """
    Обрабатывает запрос на страницу Пользователи.

    :param request: Объект запроса.
    :param session: Объект текущей сессии.
    :param user: Текущий пользователь (извлекается из токена).
    """
    tgusers = await telegramuser_crud.get_multi(session)

    context = {
        "user": user,
        "request": request,
        "tgusers": tgusers
    }
    return templates.TemplateResponse("users.html", context)


@router.get(
    "/{unique_id}",
    response_class=HTMLResponse,
    # response_model=TelegramUserCreate
)
async def user_view(
        request: Request,
        unique_id: str,
        session: AsyncSession = Depends(get_async_session),
        user: Admin = Depends(get_current_user_from_token)
):
    """
    Обрабатывает запрос на страницу Редактирование Пользователя.

    :param request: Объект запроса.
    :param unique_id: ID Роли
    :param session: Объект текущей сессии.
    :param user: Текущий пользователь (извлекается из токена).
     """

    tguser = await telegramuser_crud.get(unique_id, session)
    roles = await role_crud.get_multi(session)

    context = {
        "user": user,
        "request": request,
        "tguser": tguser,
        "roles": roles
    }
    return templates.TemplateResponse("user.html", context)


@router.post(
    "/{unique_id}",
    response_class=RedirectResponse,
    response_model=TelegramUserEdit,
    response_model_exclude_none=True
)
async def user_edit(
        unique_id: str,
        first_name=Form(None),
        last_name=Form(None),
        email=Form(None),
        role_id=Form(None),
        session: AsyncSession = Depends(get_async_session),
):
    """
    Обрабатывает запрос на страницу Редактирование Пользователя.

    :param unique_id: ID Пользователя
    :param first_name: Имя Пользователя
    :param last_name: Фамилия Пользователя
    :param email: Электронная почта Пользователя
    :param role_id: ID Роли Пользователя
    :param session: Объект текущей сессии.
     """

    tguser = await telegramuser_crud.get(unique_id, session)

    current_email_id = tguser.email_id

    existing_email = await employee_email_crud.get_email(session, email)
    if existing_email:
        new_email = existing_email
    else:
        new_email = await employee_email_crud.create(
            EmployeeEmailBase(title=email), session
        )

    tguser.email_id = new_email.unique_id
    tguser.first_name = first_name
    tguser.last_name = last_name
    tguser.role_id = role_id

    if current_email_id and current_email_id != new_email.unique_id:
        current_email = await employee_email_crud.get(current_email_id, session)
        if current_email:
            linked_users = await session.execute(
                select(TelegramUser).filter(TelegramUser.email_id == current_email_id)
            )
            if not linked_users.scalars().first():
                await employee_email_crud.remove(current_email, session)

    await session.commit()

    return RedirectResponse('/users', status_code=302)


@router.post(
    "/delete/{unique_id}",
    response_class=RedirectResponse,
)
async def user_delete(
        unique_id: str,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Обрабатывает запрос на удаление Пользователя.

    :param unique_id: ID Пользователя
    :param session: Объект текущей сессии.
     """
    tguser = await telegramuser_crud.get(unique_id, session)
    await telegramuser_crud.remove(
        tguser,
        session
    )
    return RedirectResponse('/users', status_code=302)
