import csv
import re
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from backend.crud.employee_email import employee_email_crud
from backend.models.employee_email import EmployeeEmail
from backend.utils.validators import check_file_keys

STARLINKRUSSIA_PATTERN = re.compile(r'@starlinkrussia.ru$')
MILESTONERUSSIA_PATTERN = re.compile(r'@milestonerussia.ru$')


async def parsing_email_addresses_from_csv_file(
    session: AsyncSession,
    path: Path,
    emails_for_remove: list[EmployeeEmail],
    encoding: str = 'utf-8',
) -> list[EmployeeEmail]:
    """Парсит и добавляет данные в таблицу."""
    emails_for_adds_in_db = []
    with open(path, 'r', encoding=encoding) as f:

        reader = csv.DictReader(f, delimiter=';')
        await check_file_keys(reader)

        for i in reader:
            email = i.get('Адрес почты')

            if not STARLINKRUSSIA_PATTERN.search(
                email,
            ) and not MILESTONERUSSIA_PATTERN.search(email):
                continue

            email_is_exist = await employee_email_crud.get_email(
                session, email,
            )

            if email_is_exist:
                emails_for_remove.remove(email_is_exist)
                continue

            db_new = EmployeeEmail(email=email)
            emails_for_adds_in_db.append(db_new)

    return emails_for_adds_in_db
