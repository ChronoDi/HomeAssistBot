from aiogram.types import InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.keyboards.rooms import get_room_keyboard
from tg_bot.lexicon import lexicon
from tg_bot.utils.database.entities import creat_dict_from_entities_group
from tg_bot.utils.database.group import need_groups
from tg_bot.utils.database.rooms import take_room_id, take_room_friendly_name
from tg_bot.utils.process_room_message import get_icon_state, get_state, get_unit_of_measurement


def _process_binary_sensors(b_sensors: dict[str, str]) -> str:
    message: str = ''

    for name, friendly_name in b_sensors.items():
        icon_state = get_icon_state(name)
        message += f'{friendly_name}: {icon_state}\n'

    return message


def _process_sensors(sensors: dict[str, str]) -> str:
    message: str = ''

    for name, friendly_name in sensors.items():
        state = get_state(name)
        icon: str = get_icon_state(name, state)

        if icon:
            message += f'{friendly_name}: {icon}' + '\n'
        else:
            unit_of_measurement: str = get_unit_of_measurement(name)
            state = f'{state} {unit_of_measurement}' if unit_of_measurement else state
            message += f'{friendly_name}: {state}' + '\n'

    return message


async def show_room(room_name: str, session: AsyncSession) -> tuple[str, InlineKeyboardMarkup]:
    room_id: int = await take_room_id(session, room_name)
    room_friendly_name = await take_room_friendly_name(session, room_name)
    entity_dict: dict[str, dict[str: str]] = {}
    message: str = f'<b>{room_friendly_name}</b>: \n'

    for group in need_groups:
        temp_dict: dict[str: str] = await creat_dict_from_entities_group(session=session, group=group, room_id=room_id,
                                                                         need_name=True)
        entity_dict.update({group : temp_dict})

    message += lexicon['sensor'] + ':\n'
    message += _process_binary_sensors(entity_dict['binary_sensor'])
    entity_dict.pop('binary_sensor')
    message += _process_sensors(entity_dict['sensor'])
    entity_dict.pop('sensor')

    keyboard: InlineKeyboardMarkup = get_room_keyboard(entity_dict)
    entity_dict.clear()

    return message, keyboard
