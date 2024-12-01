import logging

from sqlalchemy import select

from backend.core.db import AsyncSessionLocal
from backend.models.admin import Admin

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_user(username: str) -> Admin:
    """Извлекает пользователя из базы данных.

    На основе предоставленного имени пользователя.

    :param username: Имя пользователя для получения.
    :type username: str
    :return: Полученный пользователь, если найден, иначе None.
    """
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(
                select(Admin).filter(Admin.username == username),
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error fetching user {username}: {e}")
            return None
