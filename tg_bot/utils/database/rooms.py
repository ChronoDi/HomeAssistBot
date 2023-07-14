from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import max

from tg_bot.database.models import Rooms
from tg_bot.utils.database.tables import take_all_rows, check_is_empty


async def creat_dict_from_rooms(session: AsyncSession) -> dict[str, str]:
    rooms = await take_all_rows(session, Rooms)
    room_dict: dict[str, str] = {}

    if rooms:
        for room in rooms:
            room_dict.update({room.name : room.friendly_name})

    return room_dict


async def add_room(session: AsyncSession, name: str) -> None:
    if await check_is_empty(session, Rooms):
        result = 0
    else:
        db_query = await session.execute(select(max(Rooms.id)).select_from(Rooms))
        result = db_query.scalar()

    await session.merge(Rooms(name=f'rooms_{result + 1}', friendly_name=name))
    await session.commit()


async def remove_room(session: AsyncSession, name: str):
    db_quarry = await session.execute(select(Rooms).where(Rooms.name == name))
    result = db_quarry.scalar()
    await session.delete(result)
    await session.commit()


async def take_room_id(session: AsyncSession, room_name: str) -> int:
    db_query = await session.execute(select(Rooms).where(Rooms.name == room_name))
    room: Rooms = db_query.scalar()

    return room.id

async def take_room_friendly_name(session: AsyncSession, room_name: str) -> str:
    db_query = await session.execute(select(Rooms).where(Rooms.name == room_name))
    room: Rooms = db_query.scalar()

    return room.friendly_name