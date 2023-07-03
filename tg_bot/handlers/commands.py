from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tg_bot.filters import IsAdmin
from tg_bot.lexicon import lexicon

router: Router = Router()
router.message.filter(IsAdmin())


async def process_start_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=lexicon['start'])


def process_all_command() -> None:
    router.message.register(process_start_command, CommandStart())


process_all_command()
