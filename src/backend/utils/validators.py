import csv

from fastapi import status
from fastapi.exceptions import HTTPException

FILE_IS_MISSING = 'Приложите файл в формате csv.'
MUST_HAVE_CSV_EXTENSION = 'Файл должен быть в расширении csv.'


async def check_file_exist(filename: str) -> None:
    """Проверка, что файл действительно передан."""
    if not filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=FILE_IS_MISSING,
        )


async def check_file_extension(filename: str, extension: str = 'csv') -> None:
    """Проверка формата файла."""
    if filename.split('.')[-1] != extension:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=MUST_HAVE_CSV_EXTENSION,
        )


async def check_file_keys(reader: csv.DictReader) -> None:
    """Функия проверяющая наличие заголовков ['Сотрудник', 'Адрес почты'].

    Принимает на вход csv.DictReader.
    """
    fields = ['Сотрудник', 'Адрес почты']
    for field in reader.fieldnames:
        if field in fields:
            fields.remove(field)
    if len(fields) != 0:
        raise HTTPException(
            status_code=400, detail=f'Не хватате заголовков талицы: {fields}.',
        )
