from fastapi import APIRouter

from backend.pages.menus import router as menus_router

router = APIRouter()

MENUS_PRFIX = '/menus'
router.include_router(menus_router, prefix=MENUS_PRFIX, tags=['menus'])
