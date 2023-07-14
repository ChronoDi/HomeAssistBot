from aiogram import Router
from aiogram.filters import Text, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.keyboards.rooms import get_rooms_keyboard
from tg_bot.lexicon import lexicon
from tg_bot.states.home_assistant.edit_rooms import FSMEditRooms
from tg_bot.utils.database.rooms import remove_room

remove_room_router: Router = Router()


async def process_remove_room_callback(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    keyboard = await get_rooms_keyboard(session, special_symbol='❌', need_remove=True)
    await callback.message.edit_text(lexicon["select_room_to_remove"], reply_markup=keyboard)
    await state.set_state(FSMEditRooms.delete_room)


async def process_back_callback(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    keyboard = await get_rooms_keyboard(session)
    await callback.message.edit_text(text=lexicon["edit"], reply_markup=keyboard)
    await state.set_state(FSMEditRooms.edit_list_rooms)


async def process_remove_callback(callback: CallbackQuery, session: AsyncSession):
    await remove_room(session, callback.data)
    keyboard = await get_rooms_keyboard(session, special_symbol='❌', need_remove=True)
    await callback.message.edit_text(lexicon["select_room_to_remove"], reply_markup=keyboard)


def process_all_handlers() -> None:
    remove_room_router.callback_query.register(process_remove_room_callback, Text(text='remove_room'),
                                               StateFilter(FSMEditRooms.edit_list_rooms))
    remove_room_router.callback_query.register(process_back_callback, Text(text='back'),
                                               StateFilter(FSMEditRooms.delete_room))
    remove_room_router.callback_query.register(process_remove_callback, StateFilter(FSMEditRooms.delete_room))