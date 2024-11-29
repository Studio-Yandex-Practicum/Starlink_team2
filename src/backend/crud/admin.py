from backend.models.admin import Admin
from sqlalchemy import select
from backend.core.db import AsyncSessionLocal
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_user(username: str) -> Admin:
    """
    Извлекает пользователя из базы данных на
        основе предоставленного имени пользователя.

    :param username: Имя пользователя для получения.
    :type username: str
    :return: Полученный пользователь, если найден, иначе None.
    """
    async with AsyncSessionLocal() as session:
        try:
            query = select(Admin).filter(Admin.username == username)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            return user
        except Exception as e:
            logger.error(f"Error fetching user {username}: {e}")
            return None
