
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from passlib.handlers.sha2_crypt import sha512_crypt as crypto
from rich import print
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from backend.core.db import AsyncSessionLocal
from backend.pages.pages import router
from backend.models.admin import Admin
from backend.core.config import settings


load_dotenv()


app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version,
)


app.include_router(router)


base_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(base_dir, 'static')
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.on_event("startup")
async def startup():
    """
    Создание первых пользователей.
    """
    async with AsyncSessionLocal() as session:
        try:
            statement = select(Admin)
            result = await session.execute(statement)
            user = result.scalars().first()
            if not user:
                user1 = Admin(username="user1@gmail.com",
                              hashed_password=crypto.hash("12345"))
                user2 = Admin(username="user2@gmail.com",
                              hashed_password=crypto.hash("54321"))
                session.add_all([user1, user2])
                await session.commit()
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
