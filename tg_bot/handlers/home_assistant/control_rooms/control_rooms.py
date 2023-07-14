from aiogram import Router
from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.filters.users import IsUser
from tg_bot.keyboards.rooms import get_rooms_keyboard
from tg_bot.lexicon import lexicon
from tg_bot.states.home_assistant.control_rooms import FSMControlRooms
from tg_bot.utils.database.entities import get_entity_group
from tg_bot.utils.home_assist.entities import process_click_button
from tg_bot.utils.home_assist.rooms import show_room
from aiogram.exceptions import TelegramBadRequest

control_rooms_router: Router = Router()
control_rooms_router.message.filter(IsUser())


async def process_select_room_callback(callback: CallbackQuery, state: FSMContext,
                                       session: AsyncSession):
    await state.update_data(room=callback.data)
    room: str = callback.data
    text, keyboard = await show_room(room_name=room, session=session)
    await callback.message.edit_text(text=text, reply_markup = keyboard)
    await state.set_state(FSMControlRooms.control_room)


async def process_back_callback(callback: CallbackQuery, state: FSMContext,
                                        session: AsyncSession):
    keyboard = await get_rooms_keyboard(session, need_last_buttons=False)
    await callback.message.edit_text(text=lexicon["rooms"], reply_markup=keyboard)
    await state.clear()
    await state.set_state(FSMControlRooms.select_room)


async def process_switch_callback(callback: CallbackQuery, state: FSMContext,
                                       session: AsyncSession):
    entity_id = callback.data
    entity_group: str = await get_entity_group(entity_id, session)
    process_click_button(entity_id, entity_group)
    await _show_room(callback, state, session)


async def process_refresh_callback(callback: CallbackQuery, state: FSMContext,
                                       session: AsyncSession):
    await _show_room(callback, state, session)


async def _show_room(callback: CallbackQuery, state: FSMContext,
                                       session: AsyncSession):
    data = await state.get_data()
    room = data['room']
    text, keyboard = await show_room(room_name=room, session=session)
    try:
        await callback.message.edit_text(text=text, reply_markup=keyboard)
    except TelegramBadRequest:
        await callback.answer()

def process_all_handlers() -> None:
    control_rooms_router.callback_query.register(process_select_room_callback,
                                                 StateFilter(FSMControlRooms.select_room))
    control_rooms_router.callback_query.register(process_back_callback, Text(text='back'),
                                                 StateFilter(FSMControlRooms.control_room))
    control_rooms_router.callback_query.register(process_refresh_callback, Text(text='refresh'),
                                                 StateFilter(FSMControlRooms.control_room))
    control_rooms_router.callback_query.register(process_switch_callback,
                                                 StateFilter(FSMControlRooms.control_room))