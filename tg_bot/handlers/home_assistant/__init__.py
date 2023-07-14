from aiogram import Router

from tg_bot.filters.admins import IsAdmin
from tg_bot.handlers.home_assistant.edit_rooms import add_room, edit_room, remove_room
from tg_bot.handlers.home_assistant.control_rooms import control_rooms

router: Router = Router()
router.message.filter(IsAdmin())


def process_home_assistant_handlers():
    add_room.process_all_handlers()
    remove_room.process_all_handlers()
    edit_room.process_all_handlers()
    control_rooms.process_all_handlers()


def include_home_assistant_routers():
    router.include_router(add_room.add_room_router)
    router.include_router(remove_room.remove_room_router)
    router.include_router(edit_room.edit_room_router)
    router.include_router(control_rooms.control_rooms_router)


process_home_assistant_handlers()
include_home_assistant_routers()
