from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    admins: list[int]
    users: list[int]


@dataclass
class Redis:
    is_need: bool
    host: str


@dataclass
class HomeAssist:
    url: str
    token: str


@dataclass
class DataBase:
    host: str
    port: int
    user: str
    password: str
    db_name: str


@dataclass
class Config:
    tg_bot: TgBot
    redis: Redis
    home_assist: HomeAssist
    database: DataBase


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'),
                               admins=list(map(int, env.list('ADMINS'))),
                               users=list(map(int, env.list('USERS')))),
                  redis=Redis(host=env('REDIS_HOST'),
                              is_need=env.bool('USE_REDIS')),
                  home_assist=HomeAssist(url=env('HA_URL'),
                                         token=env('HA_TOKEN')),
                  database=DataBase(host=env('DB_HOST'),
                                    port=env.int('DB_PORT'),
                                    user=env('DB_USER'),
                                    password=env('DB_PASSWORD'),
                                    db_name=env('DB_NAME')))
