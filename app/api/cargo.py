from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from datetime import date
from typing import Annotated
from fastapi import Header

from config import settings
from app import db_helper
from app.schemas.rates import (
    RateBaseSchema,
    RateWithoutDateSchema,
    RateWithoutRate,
    CargoSchema,
)
from app.schemas.responses import SuccessResponse
import app.dao.rates as rate_dao
from app.utils.kafka_logs import kafka_log_action


router: APIRouter = APIRouter(prefix=settings.api.cargo_prefix)

@router.post(
    "/severaladd",
    responses={
        200: {"model": SuccessResponse, "description": "Успешный ответ"},
        400: {"description": "Уже существует rate с таким title"},
        500: {"description": "Ошибка сервера при добавлении данных"}
    },
)
@kafka_log_action("add_several_rate")
async def add_rate(
    data: dict[date, list[RateWithoutDateSchema]],
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """
    Добавляет несколько типов груза в базу данных.
    """
    for action_date in data:
        rate_list: list[RateWithoutDateSchema] = data.get(action_date)
        for rate in rate_list:
            if await rate_dao.get_rate(
                session=session, 
                rate_title=rate.cargo_type,
                action_date=action_date
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Already exists rate title: {rate.cargo_type}",
                )
            
            result: bool  = await rate_dao.add_rate(
                session=session, rate_schema=RateBaseSchema(
                    cargo_type=rate.cargo_type,
                    rate=rate.rate,
                    action_date=action_date
                )
            )
            
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Server error, rate title: {rate.cargo_type}",
                )
    
    return SuccessResponse(message="rate successfully added")


@router.post(
    "/add",
    responses={
        200: {"model": SuccessResponse, "description": "Успешный ответ"},
        400: {"description": "Уже существует rate с таким title"},
        500: {"description": "Ошибка сервера при добавлении данных"}
    },
)
@kafka_log_action("add_rate")
async def add_rate(
    rate_schema: RateBaseSchema,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """
    Добавляет новый тип груза в базу данных.
    """
    if await rate_dao.get_rate(
        session=session, 
        rate_title=rate_schema.cargo_type,
        action_date=rate_schema.action_date
    ):
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
@kafka_log_action("update_rate")
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
@kafka_log_action("delete_rate")
async def delete_rate(
    rate_schema: RateWithoutRate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """
    Удаляет существующий тип груза в базе данных.
    """
    if not await rate_dao.get_rate(
        session=session,
        rate_title=rate_schema.cargo_type,
        action_date=rate_schema.action_date
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not exists rate title data",
        )
    result: bool = await rate_dao.delete_rate(
        session=session, rate_schema=rate_schema)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error",
        )
    
    return SuccessResponse(message="rate successfully deleted")

@router.get(
    "/getrates",
    responses={
        200: {"description": "Расчитанная стоимость доставки"},
        400: {"description": "Нет rate с таким названием"},
    },
)
async def get_price(
    action_date: Annotated[date, Header(
            description="Дата в формате YYYY-MM-DD",
            example="2024-12-01"
        )
    ],
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """
    Показывает все возможные типы грузов за выбранную дату.
    """
    rate_titles = await rate_dao.get_rates_title(
        session=session,
        action_date=action_date
    )
    if not rate_titles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not exists rate title data",
        )
    print("ashgfahjsfhkajsfasfa", rate_titles)
    return rate_titles

@router.post(
    "/getprice",
    responses={
        200: {"description": "Расчитанная стоимость доставки"},
        400: {"description": "Нет rate с таким названием"},
    },
)
@kafka_log_action("price_calculation")
async def get_price(
    cargo_schema: CargoSchema,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """
    Расчитывает стоимость доставки.
    """
    rate = await rate_dao.get_rate(
        session=session,
        rate_title=cargo_schema.cargo_type,
        action_date=cargo_schema.action_date
    )
    if not rate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not exists rate title data",
        )
    
    return {
        "Value": rate.value * cargo_schema.declared_price
    }