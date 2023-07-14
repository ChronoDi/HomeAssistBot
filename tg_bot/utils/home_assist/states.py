from typing import Any

from tg_bot.utils.home_assist import get_client


def get_state_attribute(entity_id) -> dict[str, Any]:
   client = get_client()

   with client:
        state = client.get_state(entity_id=entity_id)

        return state.attributes