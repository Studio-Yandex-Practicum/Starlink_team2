from pathlib import Path
import re

from anyio import open_file
from sqlalchemy.ext.asyncio import AsyncSession

from backend.crud.employee_email import employee_email_crud
from backend.models.employee_email import EmployeeEmail
from backend.utils.validators import check_file_keys

STARLINKRUSSIA_PATTERN = re.compile(r'@starlinkrussia.ru$')
MILESTONERUSSIA_PATTERN = re.compile(r'@milestonerussia.ru$')
DELIMITER = ';'
MAX_READ_BYTES = 10 * 1024 * 1024


async def parsing_email_addresses_from_csv_file(
    session: AsyncSession,
    path: Path,
    emails_for_remove: list[EmployeeEmail],
    encoding: str = 'utf-8',
) -> list[EmployeeEmail]:
    """Парсит и добавляет данные в таблицу."""
    emails_for_adds_in_db = []
    async with await open_file(path, 'r', encoding=encoding) as f:
        files = await f.read(MAX_READ_BYTES)
        files = files.split('\n')

        await check_file_keys(files[0])

        for row in files[1:]:
            for column in row.split(DELIMITER):
                if not STARLINKRUSSIA_PATTERN.search(
                    column,
                ) and not MILESTONERUSSIA_PATTERN.search(column):
                    continue

                email_is_exist = await employee_email_crud.get_email(
                    session, column
                )

                if email_is_exist:
                    emails_for_remove.remove(email_is_exist)
                    continue

                db_new = EmployeeEmail(title=column)
                emails_for_adds_in_db.append(db_new)

    return emails_for_adds_in_db
