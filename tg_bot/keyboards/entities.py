from aiogram.types import InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.keyboards.fabric import get_inline_keyboards
from tg_bot.lexicon import lexicon
from tg_bot.utils.database.entities import creat_dict_from_entities_rooms

last_buttons_view: dict[str: str] = {'add_entity': lexicon['add_entity'], 'back': lexicon['back']}
last_buttons_back: dict[str: str] = {'back': lexicon['back']}
previous_next_back: dict[str: str] = {'backward': '<<', 'back': lexicon['back'], 'forward': '>>'}


async def get_room_entities_keyboard(session: AsyncSession,
                                     special_symbol: str = None,
                                     room: str = None) -> InlineKeyboardMarkup:
    entities_dict: dict[str, str] = await creat_dict_from_entities_rooms(session, room)
    last_buttons = last_buttons_view
    keyboard = get_inline_keyboards(width=(((len(entities_dict) - 1) // 7) + 1),
                                    callback_names=entities_dict,
                                    last_buttons=last_buttons,
                                    special_symbol=special_symbol)

    return keyboard


def get_group_entities_keyboard(need_dict: dict[str: str], special_symbol: str = None) -> InlineKeyboardMarkup:
    keyboard = get_inline_keyboards(2, callback_names=need_dict,
                                       last_buttons=previous_next_back,
                                       special_symbol=special_symbol)

    return keyboard