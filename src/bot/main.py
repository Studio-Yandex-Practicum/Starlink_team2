import asyncio

from commands import *  # noqa: F403
from loader import bot

asyncio.run(bot.polling(skip_pending=True))
