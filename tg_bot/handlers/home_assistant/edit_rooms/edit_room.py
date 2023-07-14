from aiogram import Router
from aiogram.filters import StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.keyboards.entities import get_room_entities_keyboard, get_group_entities_keyboard
from tg_bot.keyboards.group import get_groups_keyboard
from tg_bot.keyboards.rooms import get_rooms_keyboard
from tg_bot.lexicon import lexicon
from tg_bot.states.home_assistant.edit_rooms import FSMEditRooms
from tg_bot.utils.database.entities import creat_dict_from_entities_group, add_entity_to_room, remove_entity_from_room
from tg_bot.utils.slice_dict import slice_dict

edit_room_router: Router = Router()


async def process_edit_room_callback(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.update_data(room=callback.data)
    keyboard = await get_room_entities_keyboard(session=session, special_symbol='❌',room=callback.data)
    await callback.message.edit_text(text=lexicon['edit_entities'], reply_markup=keyboard)
    await state.set_state(FSMEditRooms.edit_room_entities)


async def process_back_callback(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    keyboard = await get_rooms_keyboard(session)
    await callback.message.edit_text(text=lexicon["edit"], reply_markup=keyboard)
    await state.set_state(FSMEditRooms.edit_list_rooms)


async def process_add_entity_callback(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    keyboard = await get_groups_keyboard(session)
    await callback.message.edit_text(text=lexicon['select_group'], reply_markup=keyboard)
    await state.set_state(FSMEditRooms.select_group_entities)


async def process_select_group_callback(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.update_data(group=callback.data)
    group = callback.data
    entities_dict: dict[str: str] = await creat_dict_from_entities_group(session=session, group=group)
    result_dict, num_pages = slice_dict(start_dict=entities_dict, num_elements=14)
    await state.update_data(entities=result_dict, num_pages=num_pages - 1, current_page = 0)
    await _change_entities(state=state, callback=callback, current_page=0)
    await state.set_state(FSMEditRooms.add_entity)


async def process_previous_entities(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_page = data['current_page']

    if current_page != 0:
        await _change_entities(state=state, callback=callback, current_page=current_page - 1)
        await state.update_data(current_page=current_page - 1)
    else:
        await callback.answer()


async def process_next_entities(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    num_pages = data['num_pages']
    current_page = data['current_page']

    if current_page != num_pages:
        await _change_entities(state=state, callback=callback, current_page=current_page + 1)
        await state.update_data(current_page=current_page + 1)
    else:
        await callback.answer()


async def process_entity_callback(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    room = data['room']
    current_page = data['current_page']
    await add_entity_to_room(session=session, room_name=room, entity_id=int(callback.data))
    new_dict: dict[str, dict[str, str]] = data['entities']
    new_dict[str(current_page)].pop(callback.data)
    await state.update_data(entities=new_dict)
    await _change_entities(state=state, callback=callback, current_page=current_page)


async def process_remove_entity(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    await remove_entity_from_room(session=session, entity_id=int(callback.data))
    room = data['room']
    keyboard = await get_room_entities_keyboard(session=session, special_symbol='❌', room=room)
    await callback.message.edit_text(text=lexicon['edit_entities'], reply_markup=keyboard)


async def _change_entities(state: FSMContext,callback: CallbackQuery, current_page: int) -> None:
    data = await state.get_data()
    keyboard = get_group_entities_keyboard(data['entities'][str(current_page)])
    await callback.message.edit_text(text=lexicon['select_entity'], reply_markup=keyboard)


def process_all_handlers() -> None:
    edit_room_router.callback_query.register(process_edit_room_callback, StateFilter(FSMEditRooms.edit_list_rooms))
    edit_room_router.callback_query.register(process_back_callback, Text(text='back'),
                                               StateFilter(FSMEditRooms.edit_room_entities,
                                                           FSMEditRooms.select_group_entities))
    edit_room_router.callback_query.register(process_add_entity_callback, Text(text='add_entity'),
                                             StateFilter(FSMEditRooms.edit_room_entities))
    edit_room_router.callback_query.register(process_remove_entity, StateFilter(FSMEditRooms.edit_room_entities))
    edit_room_router.callback_query.register(process_select_group_callback,
                                             StateFilter(FSMEditRooms.select_group_entities))
    edit_room_router.callback_query.register(process_previous_entities, Text(text='backward'),
                                             StateFilter(FSMEditRooms.add_entity))
    edit_room_router.callback_query.register(process_next_entities, Text(text='forward'),
                                             StateFilter(FSMEditRooms.add_entity))
    edit_room_router.callback_query.register(process_add_entity_callback, Text(text='back'),
                                             StateFilter(FSMEditRooms.add_entity))
    edit_room_router.callback_query.register(process_entity_callback, StateFilter(FSMEditRooms.add_entity))
