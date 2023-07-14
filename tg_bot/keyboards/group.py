from aiogram.types import InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.keyboards.fabric import get_inline_keyboards
from tg_bot.lexicon import lexicon
from tg_bot.utils.database.group import creat_dict_from_groups

last_buttons_remove: dict[str: str] = {'back' : lexicon['back']}

async def get_groups_keyboard(session: AsyncSession, special_symbol: str = None) -> InlineKeyboardMarkup:
    room_dict: dict[str, str] = await creat_dict_from_groups(session)
    last_buttons = last_buttons_remove
    keyboard = get_inline_keyboards(width=(((len(room_dict) - 1) // 7) + 1),
                                    callback_names=room_dict,
                                    last_buttons=last_buttons,
                                    special_symbol=special_symbol)

    return keyboard