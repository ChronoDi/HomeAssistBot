from aiogram import Router
from aiogram.types import Message

from tg_bot.filters import IsAdmin
from tg_bot.lexicon import lexicon

router = Router()
router.message.filter(~IsAdmin())


async def process_message(message: Message):
    await message.answer(lexicon['user_echo'])


def process_all_handlers() -> None:
    router.message.register(process_message)


process_all_handlers()
