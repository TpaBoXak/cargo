from fastapi import APIRouter

from config import settings


api_router = APIRouter(prefix=settings.api.prefix)

from .cargo import router as auth_router
api_router.include_router(auth_router)