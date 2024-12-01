from contextlib import asynccontextmanager
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from passlib.handlers.sha2_crypt import sha512_crypt as crypto
from rich import print as rich_print
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from backend.core.config import settings
from backend.core.db import AsyncGenerator, AsyncSessionLocal
from backend.models.admin import Admin
from backend.pages.pages import router as pages_router
from backend.pages.routers import main_router

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Lifespan context manager для инициализации данных."""
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Admin))
            user = result.scalars().first()
            if not user:
                user1 = Admin(username=os.getenv("ADMIN_USER1_USERNAME"),
                              hashed_password=crypto.hash(
                                  os.getenv("ADMIN_USER1_PASSWORD")),
                              )
                user2 = Admin(username=os.getenv("ADMIN_USER2_USERNAME"),
                              hashed_password=crypto.hash(
                                  os.getenv("ADMIN_USER2_PASSWORD")),
                              )
                session.add_all([user1, user2])
                await session.commit()
                rich_print("[green]Администраторы успешно созданы.[/green]")
        except SQLAlchemyError as e:
            rich_print(f"[red]Database error: {e}[/red]")
    yield


app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(main_router)
app.include_router(pages_router)

base_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(base_dir, 'static')
app.mount("/static", StaticFiles(directory=static_dir), name="static")
