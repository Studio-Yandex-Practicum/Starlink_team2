from dotenv import load_dotenv
from fastapi import FastAPI

from core.config import settings

load_dotenv()

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version,
)
