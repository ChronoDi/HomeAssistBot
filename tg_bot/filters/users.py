from aiogram.types import Message
from aiogram.filters import BaseFilter

from tg_bot.config_data import config


class IsUser(BaseFilter):
    keyword = 'is_user'

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in (config.tg_bot.users or config.tg_bot.admins)
