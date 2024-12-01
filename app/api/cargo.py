from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime


from config import settings
from app import db_helper


router: APIRouter = APIRouter(prefix=settings.api.cargo_prefix)