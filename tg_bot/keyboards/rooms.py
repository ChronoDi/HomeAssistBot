from aiogram.types import InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.keyboards.fabric import get_inline_keyboards
from tg_bot.lexicon import lexicon

from tg_bot.utils.database.rooms import creat_dict_from_rooms
from tg_bot.utils.process_room_message import get_icon_state

last_buttons_view: dict[str: str] = {'add_room': lexicon['add_room'], 'remove_room': lexicon['remove_room']}
last_buttons_remove: dict[str: str] = {'back' : lexicon['back']}
last_buttons_refresh: dict[str: str] = {'refresh' : lexicon['refresh'] ,'back' : lexicon['back']}


def _get_last_buttons(need_remove: bool) -> dict[str, str]:
    if need_remove:
        return last_buttons_remove

    return  last_buttons_view


async def get_rooms_keyboard(session: AsyncSession, special_symbol: str = None,
                             need_remove = False, need_last_buttons=True) -> InlineKeyboardMarkup:
    room_dict: dict[str, str] = await creat_dict_from_rooms(session)
    last_buttons = None

    if need_last_buttons:
        last_buttons = _get_last_buttons(need_remove)

    keyboard = get_inline_keyboards(width=(((len(room_dict) - 1) // 7) + 1),
                                    callback_names=room_dict,
                                    last_buttons=last_buttons,
                                    special_symbol=special_symbol)

    return keyboard


def get_room_keyboard(entities_dict:dict[str, dict[str: str]]) -> InlineKeyboardMarkup:
    buttons: dict[str, str] = {}

    for group, entities in entities_dict.items():
        if group != 'button':
            for name, friendly_name in entities.items():
                icon: str = get_icon_state(name)
                entities_dict[group][name] = f'{icon} {entities_dict[group][name]}'

        buttons.update(entities)

    keyboard = get_inline_keyboards(width=(((len(entities_dict) - 1) // 7) + 1),
                                    callback_names=buttons,
                                    last_buttons=last_buttons_refresh)

    return keyboard



