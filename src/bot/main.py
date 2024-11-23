import asyncio
import logging

import handlers  # noqa
from loader import bot
from utils.logger import get_logger


async def main() -> None:
    """Запуск оболочки бота."""
    log = get_logger(__name__)
    try:
        log.info('Bot started')
        await bot.infinity_polling(
            skip_pending=True,
            logger_level=logging.INFO,
        )
        log.info('Bot stopped')
    except Exception as e:
        log.info(e)


if __name__ == '__main__':
    asyncio.run(
        main(),
    )
