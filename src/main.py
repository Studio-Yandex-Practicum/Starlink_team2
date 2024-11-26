import asyncio
import logging

import uvicorn

import bot.handlers  # noqa
from bot.utils.logger import get_logger
from bot.loader import bot_instance


async def run_fastapi() -> None:
    """Запуск fastapi."""
    config = uvicorn.Config(app='backend.app:app', host='0.0.0.0', port=8000)
    server = uvicorn.Server(config=config)
    await server.serve()


async def run_bot() -> None:
    """Запуск оболочки бота."""
    log = get_logger(__name__)
    try:
        log.info('Bot started')
        await bot_instance.infinity_polling(
            skip_pending=True,
            logger_level=logging.INFO,
        )
        log.info('Bot stopped')
    except Exception as e:
        log.info(e)


async def main() -> None:
    """Запуск оболочки бота и fastapi."""
    await asyncio.gather(
        run_bot(),
        run_fastapi(),
    )


if __name__ == '__main__':
    asyncio.run(
        main(),
    )
