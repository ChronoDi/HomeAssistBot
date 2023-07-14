from aiogram.filters.state import State, StatesGroup

class FSMControlRooms(StatesGroup):
    select_room = State()
    control_room = State()