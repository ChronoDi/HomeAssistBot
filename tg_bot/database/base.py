from sqlalchemy.orm import declarative_base

from tg_bot.config_data import config

Base = declarative_base()
path: str = f'postgresql+asyncpg://{config.database.user}:{config.database.password}' \
            f'@{config.database.host}/{config.database.db_name}'

