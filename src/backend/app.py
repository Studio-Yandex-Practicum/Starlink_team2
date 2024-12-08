import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from passlib.handlers.sha2_crypt import sha512_crypt as crypto
from rich import print as rich_print
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.core.config import settings
from backend.core.db import AsyncGenerator, get_async_session
from backend.models.admin import Admin
from backend.pages.auth_login import router as auth_login_router
from backend.pages.dashboard import router as dashboard_router
from backend.pages.index import router as index_router
from backend.pages.menus import router as menus_router
from backend.pages.parse_csv import router as parse_csv_router
from backend.pages.roles import router as roles_router
from backend.pages.users import router as users_router

load_dotenv()


async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Lifespan context manager для инициализации данных."""
    async with get_async_session() as session:
        try:
            result = await session.execute(select(Admin))
            user = result.scalars().first()
            if not user:
                user1 = Admin(
                    username=settings.ADMIN1_EMAIL,
                    hashed_password=crypto.hash(
                        settings.ADMIN1_PASSWORD,
                    ),
                )
                user2 = Admin(
                    username=settings.ADMIN2_EMAIL,
                    hashed_password=crypto.hash(
                        settings.ADMIN2_PASSWORD,
                    ),
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

app.include_router(parse_csv_router)
app.include_router(menus_router)
app.include_router(index_router)
app.include_router(auth_login_router)
app.include_router(dashboard_router)
app.include_router(users_router, prefix="/users")
app.include_router(roles_router, prefix="/roles")


base_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(base_dir, 'static')
app.mount("/static", StaticFiles(directory=static_dir), name="static")
template_dir = os.path.join(base_dir, 'templates')
templates = Jinja2Templates(directory=template_dir)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request,
                                 exc: StarletteHTTPException):
    if exc.status_code == 404:
        template = templates.get_template("404.html")
        return HTMLResponse(template.render(request=request))
    elif exc.status_code == 401:
        template = templates.get_template("401.html")
        return HTMLResponse(template.render(request=request))
    elif exc.status_code == 403:
        template = templates.get_template("403.html")
        return HTMLResponse(template.render(request=request))

@app.get("/nonexistent")
async def nonexistent():
    raise HTTPException(status_code=404, detail="Not Found")

@app.get("/forbidden")
async def forbidden():
    raise HTTPException(status_code=403, detail="Forbidden")

@app.get("/unauthorized")
async def unauthorized():
    raise HTTPException(status_code=401, detail="Unauthorized")
