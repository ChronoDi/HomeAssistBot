from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    admins: list[int]


@dataclass
class Redis:
    is_need: bool
    host: str


@dataclass
class Config:
    tg_bot: TgBot
    redis: Redis


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'),
                               admins=list(map(int, env.list('ADMINS')))),
                  redis=Redis(host=env('REDIS_HOST'),
                              is_need=env.bool('USE_REDIS')),)
