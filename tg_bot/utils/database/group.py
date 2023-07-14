from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from tg_bot.database.models import Groups
from tg_bot.lexicon import lexicon
from tg_bot.utils.database.tables import take_all_rows

need_groups: list[str] = ['binary_sensor', 'sensor', 'button', 'light', 'switch']

async def creat_dict_from_groups(session: AsyncSession) -> dict[str, str]:
    groups: list[Groups] = await take_all_rows(session, Groups)
    room_dict: dict[str, str] = {}

    if groups:
        for group in groups:
            room_dict.update({group.id : group.friendly_name})

    return room_dict



async def _insert_group(session: async_sessionmaker[AsyncSession], name: str, friendly_name: str) -> None:
    async with session.begin() as connect:
        await connect.merge(Groups(id=name, friendly_name=friendly_name))
        await connect.commit()


async def insert_all_groups(session: async_sessionmaker[AsyncSession])  -> None:
    for group in need_groups:
        await _insert_group(session, name=group, friendly_name=lexicon[group] if group in lexicon else group)