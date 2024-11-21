from core.config import settings
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version,
)
