from aiogram.types import Message
from aiogram.filters import BaseFilter

from tg_bot.config_data import config


class IsAdmin(BaseFilter):
    keyword = 'is_admin'

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in config.tg_bot.admins
