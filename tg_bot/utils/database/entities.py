from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from tg_bot.database.models import Entities, Rooms, Groups


async def _take_entities_by_room(session: AsyncSession, room: str) -> list[Entities]:
    db_query = await session.execute(select(Entities).join(Rooms).where(Rooms.name == room))
    result = db_query.all()
    entities: list[Entities] = []

    for entity in result:
        for value in entity:
            entities.append(value)

    return entities


async def _take_entities_by_group(session: AsyncSession, group: str, room_name: str, room_id:int) -> list[Entities]:
    need_room_id = None

    if room_id:
        need_room_id = room_id

    if room_name:
        db_query = await session.execute(select(Rooms).where(Rooms.name == room_name))
        room_name: Rooms = db_query.scalar()
        need_room_id = room_name.id

    db_query = await session.execute(select(Entities).
                                     where(and_(Entities.group_id == group,
                                                Entities.room_id == need_room_id)))

    result = db_query.all()
    entities: list[Entities] = []


    for entity in result:
        for value in entity:
            entities.append(value)

    return entities


def _make_entities_dict(entities: list[Entities], need_name: bool) -> dict[str, str]:
    entities_dict: dict[str, str] = {}

    if entities:
        if need_name:
            for entity in entities:
                entities_dict.update({str(entity.name) : entity.friendly_name})
        else:
            for entity in entities:
                entities_dict.update({str(entity.id) : entity.friendly_name})


    return entities_dict


async def creat_dict_from_entities_rooms(session: AsyncSession, room_name: str = None, need_name: bool = False) -> dict[str, str]:
    entities = await _take_entities_by_room(session=session, room=room_name)

    return _make_entities_dict(entities, need_name)


async def creat_dict_from_entities_group(session: AsyncSession, group: str,
                                         room_name: str = None, room_id: int = None,
                                         need_name: bool = False) -> dict[str, str]:
    entities = await _take_entities_by_group(session=session, group=group, room_name=room_name, room_id=room_id)
    return _make_entities_dict(entities, need_name)


async def add_entity_to_room(session: AsyncSession, room_name: str, entity_id: int) -> None:
    db_query_room = await session.execute(select(Rooms).where(Rooms.name == room_name))
    room: Rooms = db_query_room.scalar()
    room_id = room.id
    db_query_entity = await session.execute(select(Entities).where(Entities.id == entity_id))
    entity: Entities = db_query_entity.scalar()
    entity.room_id = room_id
    await session.commit()


async def remove_entity_from_room(session: AsyncSession, entity_id: int) -> None:
    db_query = await session.execute(select(Entities).where(Entities.id == entity_id))
    entity: Entities = db_query.scalar()
    entity.room_id = None
    await session.commit()


async def commit_entity(session: async_sessionmaker[AsyncSession], name: str, friendly_names: str, group_id: str) -> None:
    async with session.begin() as connect:
        db_quarry = await connect.execute(select(Groups).filter_by(id=group_id))
        group: Groups = db_quarry.scalar()
        try:
            await connect.merge(
                Entities(name=name, friendly_name=friendly_names, group_id=group.id))
            await connect.commit()
        except IntegrityError as e:
            return


async def get_entity_group(entity_id: str, session: AsyncSession) -> str:
    db_query = await session.execute(select(Entities).where(Entities.name == entity_id))
    entity: Entities = db_query.scalar()

    return entity.group_id
