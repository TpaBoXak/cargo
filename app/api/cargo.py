from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from pydantic import Field

from config import settings
from app import db_helper
from app.schemas.rates import RateBaseSchema
from app.schemas.responses import SuccessResponse
import app.dao.rates as rate_dao


router: APIRouter = APIRouter(prefix=settings.api.cargo_prefix)

@router.post(
    "/add",
    responses={
        200: {"model": SuccessResponse, "description": "Успешный ответ"},
        400: {"description": "Уже существует rate с таким title"},
        500: {"description": "Ошибка сервера при добавлении данных"}
    },
)
async def add_rate(
    rate_schema: RateBaseSchema,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """
    Добавляет новый тип груза в базу данных.
    """
    if await rate_dao.get_rate_id(session=session, rate_title=rate_schema.title):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already exists rate title data",
        )
    
    result: bool  = await rate_dao.add_rate(
        session=session, rate_schema=rate_schema)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error",
        )
    
    return SuccessResponse(message="rate successfully added")


@router.put(
    "/update",
    responses={
        200: {"model": SuccessResponse, "description": "Успешный ответ"},
        500: {"description": "Ошибка сервера при добавлении данных"}
    },
)
async def update_rate(
    rate_schema: RateBaseSchema,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """
    Изменяет существующий тип груза в базе данных.
    """
    result: bool = await rate_dao.update_rate(
        session=session, rate_schema=rate_schema)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error",
        )
    
    return SuccessResponse(message="rate successfully updated")


@router.delete(
    "/delete",
    responses={
        200: {"model": SuccessResponse, "description": "Успешный ответ"},
        400: {"description": "Нет rate с таким названием"},
        500: {"description": "Ошибка сервера при добавлении данных"}
    },
)
async def delete_rate(
    rate_title: str,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """
    Удаляет существующий тип груза в базе данных.
    """
    if not await rate_dao.get_rate_id(session=session, rate_title=rate_title):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already exists rate title data",
        )
    result: bool = await rate_dao.delete_rate(
        session=session, rate_title=rate_title)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error",
        )
    
    return SuccessResponse(message="rate successfully deleted")