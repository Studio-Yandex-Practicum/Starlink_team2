import os
from pathlib import Path

from anyio import open_file
from fastapi import APIRouter, Depends, File, Request, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.dialects.postgresql import UUID as pg_UUID  # noqa

from backend.core.auth import get_current_user_from_token
from backend.core.db import get_async_session
from backend.crud.employee_email import employee_email_crud
from backend.models.admin import Admin
from backend.utils.parser_csv import parsing_email_addresses_from_csv_file
from backend.utils.validators import check_file_exist, check_file_extension

router = APIRouter()

BASE_DIR = Path(__file__).parent.parent
FOLDER_DOWNLOADS = 'files'
FOLDER_TEMPLATES = 'templates'

templates = Jinja2Templates(directory=BASE_DIR / FOLDER_TEMPLATES)


@router.post('/load_emails', response_class=HTMLResponse)
async def load_data(
    request: Request,
    file: UploadFile = File(...),
    user: Admin = Depends(get_current_user_from_token),
) -> templates.TemplateResponse:
    """Получение файла с формы и его парсинг."""
    context = {
        'request': request,
        'user': user,
    }
    file_name = file.filename
    path = BASE_DIR / FOLDER_DOWNLOADS / file_name
    async with get_async_session() as session:

        try:
            await check_file_exist(file_name)
            await check_file_extension(file_name)

            async with await open_file(path, "wb") as f:
                await f.write(file.file.read())

            emails_for_remove = await employee_email_crud.get_multi()

            emails_for_adds_in_db = (
                await parsing_email_addresses_from_csv_file(
                    session,
                    path,
                    emails_for_remove,
                )
            )
            await employee_email_crud.remove_multi(session, emails_for_remove)

            session.add_all(emails_for_adds_in_db)
            await session.commit()

            context['total_add'] = len(emails_for_adds_in_db)
            context['total_remove'] = len(emails_for_remove)

        except HTTPException as e:
            context['errors'] = e.detail

    if file_name and os.path.exists(path):
        os.remove(path)

    return templates.TemplateResponse('load_employee_email.html', context)


@router.get('/load_emails', response_class=HTMLResponse)
async def main_parse(
    request: Request,
    user: Admin = Depends(get_current_user_from_token),
) -> HTMLResponse:
    """Отображение страницы загрузки файлов."""
    return templates.TemplateResponse(
        'load_employee_email.html',
        {'request': request, 'user': user},
    )
