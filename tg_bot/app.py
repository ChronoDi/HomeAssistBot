import asyncio
import logging

from aiogram import Bot, Dispatcher

from config_data import config
from services.storage import init_storage
from handlers import commands, admin, user


logger = logging.getLogger(__name__)


def include_all_routers(dp: Dispatcher) -> None:
    dp.include_router(commands.router)
    dp.include_router(admin.router)
    dp.include_router(user.router)


async def main() -> None:
    logging.basicConfig(level=logging.INFO, format='%(filename)s:%(lineno)d #%(levelname)-8s'
                                                   '[%(asctime)s] - %(name)s - %(message)s')
    logger.info('Start bot')
    bot: Bot = Bot(config.tg_bot.token, parse_mode='HTML')
    storage = init_storage(config.redis.is_need, config.redis.host)
    dp: Dispatcher = Dispatcher(storage=storage)

    include_all_routers(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
