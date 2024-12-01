from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from app.schemas.rates import (
    RateBaseSchema,
    RateWithoutRate
)
from app.models.rates import Rate

async def add_rate(
    session: AsyncSession, rate_schema: RateBaseSchema
) -> bool:
    try:
        rate: Rate = Rate()
        rate.value = rate_schema.rate
        rate.title = rate_schema.cargo_type
        rate.date_of_action = rate_schema.action_date
        session.add(rate)
    except:
        await session.rollback()
        return False
    else:
        await session.commit()
        return True
    
    
async def get_rate(
    session: AsyncSession, rate_title: str, action_date
) -> Optional[Rate]:
    stmt = select(Rate).where(
        Rate.title == rate_title,
        Rate.date_of_action == action_date
    )
    result = await session.execute(statement=stmt)
    return result.scalar()

async def get_rates_title(
    session: AsyncSession, action_date
) -> Optional[Rate]:
    stmt = select(Rate.title).where(
        Rate.date_of_action == action_date
    )
    result = await session.execute(statement=stmt)
    return [title[0] for title in result]


async def update_rate(
            session: AsyncSession, rate_schema: RateBaseSchema
) -> bool:
    stmt = select(Rate).where(Rate.title == rate_schema.cargo_type)
    result = await session.execute(statement=stmt)
    rate: Rate = result.scalar()

    try:
        rate.value = rate_schema.rate
        rate.date_of_action = rate_schema.action_date
        session.add(rate)
    except:
        await session.rollback()
        return False
    else:
        await session.commit()
        return True
    

async def delete_rate(
    session: AsyncSession, rate_schema: RateWithoutRate
) -> Optional[int]:
    stmt = select(Rate).where(
        Rate.title == rate_schema.cargo_type,
        Rate.date_of_action == rate_schema.action_date
    )
    result = await session.execute(statement=stmt)
    rate: Rate = result.scalar()

    try:
        await session.delete(rate)
    except:
        await session.rollback()
        return False
    else:
        await session.commit()
        return True