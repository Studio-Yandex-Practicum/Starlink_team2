from fastapi import APIRouter

from backend.core.config import settings
from .roles import router as roles_router
from .users import router as users_router


main_router = APIRouter()
main_router.include_router(
    roles_router,
    prefix=settings.ROLES_PREFIX,
    tags=settings.ROLES_TAGS
)

main_router.include_router(
    users_router,
    prefix=settings.USERS_PREFIX,
    tags=settings.USERS_TAGS
)
