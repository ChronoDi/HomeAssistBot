from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.filters import IsAdmin
from tg_bot.filters.users import IsUser
from tg_bot.keyboards.rooms import get_rooms_keyboard
from tg_bot.lexicon import lexicon
from tg_bot.states.home_assistant.control_rooms import FSMControlRooms
from tg_bot.utils.database.tables import check_is_empty
from tg_bot.database.models import Rooms
from tg_bot.states.home_assistant.edit_rooms import FSMEditRooms

router: Router = Router()


async def process_start_command(message: Message, state: FSMContext, session: AsyncSession):
    await state.clear()
    is_empty: bool = await check_is_empty(session, Rooms)

    if is_empty:
        await message.answer(text=lexicon['rooms_empty'] + ', ' + lexicon['edit_suggestion'])
    else:
        keyboard = await get_rooms_keyboard(session, need_last_buttons=False)
        await message.answer(text=lexicon["rooms"], reply_markup=keyboard)
        await state.set_state(FSMControlRooms.select_room)

async def process_edit_command(message: Message, state: FSMContext, session: AsyncSession):
    keyboard = await get_rooms_keyboard(session)
    await message.answer(text=lexicon["edit"], reply_markup=keyboard)
    await state.set_state(FSMEditRooms.edit_list_rooms)


def process_all_command() -> None:
    router.message.register(process_start_command, CommandStart(), IsUser())
    router.message.register(process_edit_command, Command(commands='edit'), IsAdmin())


process_all_command()
