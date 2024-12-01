from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from app.schemas.rates import RateBaseSchema
from app.models.rates import Rate

async def add_rate(
    session: AsyncSession, rate_schema: RateBaseSchema
) -> bool:
    try:
        rate: Rate = Rate()
        rate.value = rate_schema.value
        rate.title = rate_schema.title
        session.add(rate)
    except:
        await session.rollback()
        return False
    else:
        await session.commit()
        return True
    
async def get_rate_id(
    session: AsyncSession, rate_title: str
) -> Optional[int]:
    stmt = select(Rate.id).where(Rate.title == rate_title)
    result = await session.execute(statement=stmt)
    return result.scalar()


async def update_rate(
            session: AsyncSession, rate_schema: RateBaseSchema
) -> bool:
    stmt = select(Rate).where(Rate.title == rate_schema.title)
    result = await session.execute(statement=stmt)
    rate: Rate = result.scalar()

    try:
        rate.value = rate_schema.value
        session.add(rate)
    except:
        await session.rollback()
        return False
    else:
        await session.commit()
        return True
    

async def delete_rate(
    session: AsyncSession, rate_title: str
) -> Optional[int]:
    stmt = select(Rate).where(Rate.title == rate_title)
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