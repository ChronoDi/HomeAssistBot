from homeassistant_api import State
from sqlalchemy.ext.asyncio.session import async_sessionmaker, AsyncSession
from tg_bot.utils.database.entities import commit_entity
from tg_bot.utils.database.group import need_groups
from tg_bot.utils.home_assist import get_client


async def process_entities(session: async_sessionmaker[AsyncSession]) -> None:
    client = get_client()

    with client:
        entities = client.get_entities()

        for group_name, group in entities.items():
            if group_name in need_groups:
                for entity_name, entity in group.entities.items():
                    name = entity.state.entity_id
                    friendly_names = entity.state.attributes['friendly_name']
                    await commit_entity(session, name, friendly_names, group.group_id)



def process_click_button(entity_id:str, entity_group: str) -> None:
    client = get_client()

    with client:
        entity_domain = client.get_domain(entity_group)

        if entity_group == 'button':
            entity_domain.press(entity_id=entity_id)
        else:
            entity_domain.toggle(entity_id=entity_id)


def get_state(name: str) -> str:
    client = get_client()

    with client:
        state: State = client.get_state(entity_id=name)
        return state.state


