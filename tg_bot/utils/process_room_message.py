from typing import Any

from tg_bot.utils.home_assist.entities import get_state
from tg_bot.utils.home_assist.states import get_state_attribute


def get_icon_state(name: str, current_state: str = None) -> str | None:

    if not current_state:
        current_state = get_state(name)

    if current_state == 'off':
        return '🔴'

    if current_state == 'on':
        return '🟢'

    if current_state == 'unavailable':
        return '⚫'

    return None


def get_unit_of_measurement(name: str) -> str:
    state: str = get_state(name=name)
    attributes: dict[str, Any] = get_state_attribute(name)

    if 'unit_of_measurement' in attributes:
        return attributes['unit_of_measurement']
    else:
        return get_icon_state(name, state)