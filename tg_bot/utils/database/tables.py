from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count

from tg_bot.database.base import Base


async def check_is_empty(session: AsyncSession, base: Base) -> bool:
    db_query = await session.execute(select(count()).select_from(base))
    result = db_query.scalar()

    return result == 0


async def take_all_rows(session: AsyncSession, base: Base) -> list[Base]:
    db_query = await session.execute(select(base))
    result = db_query.all()
    entities: list[Base] = []

    for entity in result:
        for value in entity:
            entities.append(value)

    return entities