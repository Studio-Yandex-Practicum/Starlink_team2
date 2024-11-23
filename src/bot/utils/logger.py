import logging
from logging.handlers import RotatingFileHandler

from utils.additional_functions import enshure_dir


def get_logger(
        name: str,
        directory: str = 'logs',
        exstenshion: str = 'log',
) -> logging.Logger:
    """Функция логгирования.

    :param name: Имя логгера.
    :param directory: Директория для логов.
    :param exstenshion: Расширение логов.
    """
    logger: logging.Logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )
    enshure_dir(directory)
    file = RotatingFileHandler(
        filename=f'{directory}/{name}.{exstenshion}',
        backupCount=10,
        encoding='utf-8',
        maxBytes=1024*1024*20,
    )
    file.setFormatter(formatter)
    file.setLevel(logging.INFO)
    logger.addHandler(file)
    return logger
