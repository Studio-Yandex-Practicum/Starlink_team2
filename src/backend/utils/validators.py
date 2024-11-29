import csv

from fastapi.exceptions import HTTPException


async def check_file_exist(filename) -> None:
    """Проверка, что файл действительно передан."""
    if not filename:
        raise HTTPException(
            status_code=400, detail='Приложите файл в формате csv.',
        )
async def check_file_extension(filename: str) -> None:
    """Проверка формата файла."""

    if filename.split('.')[-1] != 'csv':
        raise HTTPException(
            status_code=400, detail='Файл должен быть в расширении csv.',
        )


async def check_file_keys(reader: csv.DictReader) -> None:
    """Функия проверяющая наличие заголовков ['Сотрудник', 'Адрес почты']
    в таблице. Принимает на вход csv.DictReader.
    """
    fields = ['Сотрудник', 'Адрес почты']
    for field in reader.fieldnames:
        if field in fields:
            fields.remove(field)
    if len(fields) != 0:
        raise HTTPException(
            status_code=400, detail=f'Не хватате заголовков талицы: {fields}.',
        )
