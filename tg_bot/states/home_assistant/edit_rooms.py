from aiogram.filters.state import State, StatesGroup

class FSMEditRooms(StatesGroup):
    edit_list_rooms = State()
    enter_room_name = State()
    delete_room = State()
    edit_room_entities = State()
    select_group_entities = State()
    add_entity = State()