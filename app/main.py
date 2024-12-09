from fastapi import FastAPI
from app.api import router
from app.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(router)