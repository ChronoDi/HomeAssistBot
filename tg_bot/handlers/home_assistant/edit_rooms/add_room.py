from aiogram import Router
from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.keyboards.rooms import get_rooms_keyboard
from tg_bot.lexicon import lexicon
from tg_bot.states.home_assistant.edit_rooms import FSMEditRooms
from tg_bot.utils.database.rooms import add_room

add_room_router: Router = Router()


async def process_add_room_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=lexicon['input_name_room'])
    await state.set_state(FSMEditRooms.enter_room_name)


async def process_room_name(message: Message, state: FSMContext, session: AsyncSession):
    await add_room(session=session, name=message.text)
    keyboard = await get_rooms_keyboard(session)
    await message.answer(text=lexicon["edit"], reply_markup=keyboard)
    await state.set_state(FSMEditRooms.edit_list_rooms)


def process_all_handlers() -> None:
    add_room_router.callback_query.register(process_add_room_callback, Text(text=['add_room']),
                                            StateFilter(FSMEditRooms.edit_list_rooms))
    add_room_router.message.register(process_room_name, StateFilter(FSMEditRooms.enter_room_name))