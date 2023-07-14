import asyncio
import logging

from aiogram import Bot, Dispatcher
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from tg_bot.config_data import config
from tg_bot.database.base import path
from tg_bot.utils.database.group import insert_all_groups
from tg_bot.utils.home_assist.entities import process_entities
from tg_bot.meddleware.db import DbSessionMiddleware
from tg_bot.services.storage import init_storage
from tg_bot.handlers import commands, admin, user, home_assistant


logger = logging.getLogger(__name__)


def include_all_routers(dp: Dispatcher) -> None:
    dp.include_router(home_assistant.router)
    dp.include_router(commands.router)
    dp.include_router(admin.router)
    dp.include_router(user.router)


async def main() -> None:
    logging.basicConfig(level=logging.INFO, format='%(filename)s:%(lineno)d #%(levelname)-8s'
                                                   '[%(asctime)s] - %(name)s - %(message)s')
    logger.info('Start bot')
    engine = create_async_engine(url=path, echo=True)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)
    bot: Bot = Bot(config.tg_bot.token, parse_mode='HTML')
    storage = init_storage(config.redis.is_need, config.redis.host)
    dp: Dispatcher = Dispatcher(storage=storage)
    dp.update.middleware(DbSessionMiddleware(session_pool=session_maker))

    include_all_routers(dp)

    await insert_all_groups(session_maker)
    await process_entities(session_maker)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
